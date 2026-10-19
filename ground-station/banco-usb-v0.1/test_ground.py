import csv
import tempfile
import unittest
from pathlib import Path
from protocol import FIELDS, Framer, Counter, parse
from simulator import sample, SCENARIOS
from storage import Recorder
from acquisition import Acquisition

class GroundTests(unittest.TestCase):
    def test_full_nominal_and_states(self):
        packets=[parse(sample(t),'1000') for t in range(131)]
        self.assertEqual(len(packets),131)
        self.assertEqual(packets[-1].data['STATE'],'LANDED')
        self.assertEqual(set(p.data['STATE'] for p in packets),
            {'LAUNCH_PAD','ASCENT','APOGEE','DESCENT','PROBE_RELEASE','PAYLOAD_RELEASE','LANDED'})
        self.assertEqual(max(float(p.data['ALTITUDE']) for p in packets),500)
        self.assertTrue(all(len(p.values)==22 for p in packets))
    def test_framing_all_chunk_sizes(self):
        wire=sample(0)+sample(1)+sample(2)
        for n in range(1,len(wire)+1):
            framer=Framer()
            packets=[]
            for i in range(0,len(wire),n): packets.extend(framer.feed(wire[i:i+n]))
            self.assertEqual(packets,[sample(0),sample(1),sample(2)])
    def test_overlong_recovers(self):
        f=Framer(200)
        self.assertEqual(f.feed(b'x'*10000+b'\r'+sample(0)),[sample(0)])
        self.assertEqual(f.overflows,1)
    def test_strict_validation(self):
        raw=sample(0)
        for bad in [raw.replace(b'1000',b'1001',1),raw[:-1]+b'\r\n',
                    raw.replace(b'101.3',b'nan'),raw.replace(b'13:00:00',b'99:00:00',1),
                    raw.replace(b',0.18,',b',-1.00,'),b'\xff\r']:
            with self.assertRaises((ValueError,UnicodeError)): parse(bad,'1000')
    def test_gaps_late_duplicates(self):
        c=Counter()
        for n in [100,101,104]: c.add(n)
        self.assertEqual(c.lost,2)
        c.add(102)
        self.assertEqual(c.lost,1)
        c.add(102)
        self.assertEqual(c.duplicates,1)
        c.add(103)
        self.assertEqual(c.lost,0)
        self.assertEqual(c.received,6)
        self.assertEqual(c.unique,5)
        c.add(1)
        self.assertTrue(c.warning)
        self.assertEqual(c.lost,0)
    def test_large_gap_is_bounded(self):
        c=Counter()
        c.add(1); c.add(1000000000)
        self.assertEqual(c.lost,999999998)
        self.assertEqual(len(c.missing),1)
    def test_scenarios_and_recording(self):
        expected={'NOMINAL':(131,0,0),'PACKET_LOSS':(118,13,0),
                  'CORRUPTED_PACKET':(121,10,10),'GPS_LOSS':(131,0,0),'RESET':(128,3,0)}
        for scenario in SCENARIOS:
            with self.subTest(scenario=scenario),tempfile.TemporaryDirectory() as d:
                r=Recorder(Path(d)/'primary','1000',Path(d)/'backup')
                a=Acquisition(r,scenario=scenario)
                for t in range(131):
                    raw=sample(t,scenario=scenario)
                    if raw: a.ingest(raw)
                r.close()
                self.assertEqual((a.counter.received,a.counter.lost,a.invalid),expected[scenario])
                with r.paths[0].open() as f: rows=list(csv.reader(f))
                self.assertEqual(rows[0],FIELDS)
                self.assertEqual(len(rows),expected[scenario][0]+1)
                self.assertEqual(r.paths[0].read_bytes(),r.paths[1].read_bytes())
    def test_gps_loss_retains_last_fix(self):
        last=parse(sample(49,scenario='GPS_LOSS'),'1000').data
        lost=parse(sample(50,scenario='GPS_LOSS'),'1000').data
        self.assertEqual(lost['GPS_SATS'],'0')
        for k in ['GPS_TIME','GPS_ALTITUDE','GPS_LATITUDE','GPS_LONGITUDE']:
            self.assertEqual(last[k],lost[k])
    def test_sessions_do_not_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            a=Recorder(d,'1000'); a.close()
            b=Recorder(d,'1000'); b.close()
            self.assertNotEqual(a.paths,b.paths)

if __name__=='__main__': unittest.main(verbosity=2)
