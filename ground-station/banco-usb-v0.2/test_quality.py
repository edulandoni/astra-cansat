"""ASTRA-34: regresiones de alertas, con reloj explícito y sin esperar tiempo real."""
import tempfile
import threading
import json
import unittest
from engine import Engine
from journal import Store
from mission import sample
from quality import quality_flags
from sources import PCBench


class QualityTests(unittest.TestCase):
    def test_pending_journal_event_is_a_snapshot_not_a_mutable_reference(self):
        with tempfile.TemporaryDirectory() as d:
            gate=threading.Event()
            def hold(*args):gate.wait(2)
            store=Store(d,hooks={(0,'raw'):hold})
            try:
                nested={'ranges':[[1,2]]}
                returned=store.emit('snapshot_test',details=nested)
                nested['ranges'][0][1]=99
                returned['details']['ranges'][0][1]=88
                gate.set();self.assertTrue(store.drain())
            finally:gate.set();store.close()
            saved=json.loads((store.roots[0]/'journal.jsonl').read_text().splitlines()[0])
            self.assertEqual(saved['details']['ranges'],[[1,2]])

    def test_gps_clock_stops_while_telemetry_and_link_continue(self):
        with tempfile.TemporaryDirectory() as d:
            now=[1000.]
            store=Store(d);engine=Engine(store,clock=lambda:now[0]);bench=PCBench(engine);bench.hello()
            try:
                engine.feed(sample(0)[0])
                for t in range(1,5):
                    now[0]=1000.+t
                    fields=sample(t)[0][:-1].decode().split(',');fields[16]='13:00:00'
                    engine.feed((','.join(fields)+'\r').encode())
                snap=engine.snapshot();flags=quality_flags(snap)
                self.assertTrue(flags['gps_stale']);self.assertFalse(flags['telemetry_stale'])
                self.assertEqual(snap['gps_age'],4);self.assertEqual(snap['data_age'],0)
                now[0]=1005.;engine.feed(sample(5)[0]);self.assertFalse(quality_flags(engine.snapshot())['gps_stale'])
            finally:store.close()

    def test_control_traffic_does_not_refresh_telemetry_and_does_not_blame_gps(self):
        with tempfile.TemporaryDirectory() as d:
            now=[1000.];store=Store(d);engine=Engine(store,clock=lambda:now[0]);bench=PCBench(engine)
            try:
                bench.hello();engine.feed(sample(0)[0]);now[0]+=3.25;bench.hello()
                snap=engine.snapshot();flags=quality_flags(snap)
                self.assertEqual(snap['link_age'],0);self.assertTrue(flags['telemetry_stale'])
                self.assertFalse(flags['gps_stale'])
                bench.send(kind='done',samples=1,scenario='NOMINAL')
                self.assertFalse(quality_flags(engine.snapshot())['telemetry_stale'])
            finally:store.close()

    def test_no_fix_storage_limits_and_invalid_thresholds(self):
        s={'latest':{'GPS_SATS':'0'},'gps_age':100,'data_age':0,'storage':[{'error':'disk','dropped':2,'loss_ledger_truncated':True}]}
        flags=quality_flags(s)
        self.assertTrue(flags['gps_no_fix']);self.assertFalse(flags['gps_stale'])
        self.assertTrue(flags['storage_error']);self.assertTrue(flags['known_storage_loss']);self.assertTrue(flags['loss_detail_incomplete'])
        for value in [0,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):quality_flags({},gps_max_age=value)


if __name__=='__main__':unittest.main(verbosity=2)
