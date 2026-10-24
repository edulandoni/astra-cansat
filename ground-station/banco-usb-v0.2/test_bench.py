"""ASTRA-20/21/22/34: ensayos de software, no sustituyen el USB físico."""
import csv
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from journal import Store
from engine import Engine,display,telemetry_view
from wire import control,PROFILE,Demux,parse
from mission import sample,model,expected
from sources import PCBench,replay_loop
from recover import recover

class BenchTests(unittest.TestCase):
    def setup_engine(self,root,**kwargs):
        store=Store(root,**kwargs);engine=Engine(store,source='PC_BENCH');bench=PCBench(engine)
        bench.hello();return store,engine,bench
    def test_all_scenarios_model_and_framing(self):
        for scenario in ['NOMINAL','PACKET_LOSS','CORRUPTED_PACKET','GPS_LOSS','RESET']:
            with self.subTest(scenario=scenario),tempfile.TemporaryDirectory() as d:
                s,e,b=self.setup_engine(d)
                for t in range(131):
                    raw,outcome=sample(t,scenario)
                    b.send(kind='oracle',count=t+1,outcome=outcome)
                    if raw:
                        # Varias tramas y fragmentación byte a byte.
                        for byte in raw:e.feed(bytes([byte]))
                oracle=expected(scenario)
                self.assertEqual(e.total_unique,len(oracle['emitted']))
                self.assertEqual(e.invalid,len(oracle['corrupted']))
                self.assertEqual(e.tracker.lost,len(oracle['omitted'])+len(oracle['corrupted']))
                self.assertTrue(s.drain());s.close()
        self.assertAlmostEqual(model(36)[0],410.)
        self.assertAlmostEqual(model(37)[0],398.3333333333)
        self.assertEqual(model(117)[1],'LANDED')
    def test_independent_raw_failure_and_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            fail=[True]
            def fault(kind,event):
                if fail[0]:raise OSError('Fallo raw inyectado')
            s=Store(Path(d)/'primary',Path(d)/'backup',hooks={(0,'raw'):fault})
            e=Engine(s);PCBench(e).hello()
            for t in range(20):e.feed(sample(t)[0])
            time.sleep(.3)
            statuses=s.status()
            self.assertEqual(e.total_unique,20)
            self.assertEqual(statuses[1]['saved'],20)
            self.assertEqual(statuses[3]['saved'],20)
            self.assertTrue(statuses[0]['error']);self.assertGreater(statuses[0]['pending'],0)
            fail[0]=False;self.assertTrue(s.drain(5));self.assertFalse(s.status()[0]['error']);s.close()
    def test_bounded_overflow_is_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            def fault(*args):raise OSError('Disco no disponible')
            s=Store(d,capacity=3,hooks={(0,'raw'):fault,(0,'csv'):fault})
            e=Engine(s);PCBench(e).hello()
            for t in range(30):e.feed(sample(t)[0])
            self.assertEqual(e.total_unique,30)
            for z in s.status():
                self.assertLessEqual(z['pending'],3);self.assertGreater(z['dropped'],0);self.assertTrue(z['dropped_seq_ranges'])
            s.close(.01)
    def test_epochs_conflicts_and_gps(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d)
            e.feed(sample(0)[0]);e.feed(sample(0)[0])
            bad=sample(0)[0].replace(b',0.0,',b',99.0,',1);e.feed(bad)
            self.assertEqual(e.tracker.duplicates,1);self.assertEqual(e.total_conflicts,1)
            self.assertEqual(e.latest.data['ALTITUDE'],'0.0')
            for t in [49,50]:e.feed(sample(t,'GPS_LOSS')[0])
            self.assertEqual(e.latest.data['GPS_SATS'],'0');self.assertIsNotNone(e.gps)
            b.boot='another_boot';b.hello()
            self.assertIsNone(e.latest);self.assertIsNone(e.gps);self.assertEqual(e.tracker.received,0)
            e.feed(sample(0)[0]);self.assertEqual(e.latest.count,1);s.close()
    def test_command_duplicates_timeout_and_late_result(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d)
            ident=e.command('RUN',scenario='NOMINAL',samples=131);obj=e.outgoing.get()
            e.sent(obj);b.execute(obj);run=b.run;b.tick=20;b.execute(obj)
            self.assertEqual(b.tick,20);self.assertEqual(b.run,run)
            conflicting=dict(obj,args=dict(scenario='GPS_LOSS'));b.execute(conflicting)
            self.assertEqual(e.commands[ident]['state'],'rejected')
            pending=e.command('POWER_STATUS');obj=e.outgoing.get();e.sent(obj)
            with patch('engine.time.monotonic',return_value=time.monotonic()+5):e.expire()
            self.assertEqual(e.commands[pending]['state'],'timeout')
            b.execute(obj);self.assertTrue(e.commands[pending]['late']);self.assertEqual(e.commands[pending]['state'],'executed')
            pending=e.command('POWER_STATUS');b.boot='reset';b.hello()
            self.assertEqual(e.commands[pending]['state'],'unknown');s.close()
    def test_legacy_ambiguity_and_SI(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(d);e=Engine(s,profile='legacy-usb-0.1')
            e.feed(sample(100)[0]);e.feed(sample(0)[0]);self.assertTrue(e.ambiguous);self.assertIsNone(e.latest)
            e.new_legacy_segment();e.feed(sample(0)[0]);self.assertEqual(e.latest.count,1)
            self.assertAlmostEqual(float(display({'GYRO_R':'180','GYRO_P':'0','GYRO_Y':'-180'})['GYRO_R']),3.1416,places=4)
            s.close()
    def test_clock_freeze_and_nominal_no_false_alarm(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d)
            for t in range(15):e.feed(sample(t)[0])
            self.assertFalse(e.clock_warning)
            for t in range(15,20):
                raw=sample(t)[0];fields=raw[:-1].decode().split(',');fields[1]='13:00:14';e.feed((','.join(fields)+'\r').encode())
            self.assertTrue(e.clock_warning);e.feed(sample(20)[0]);self.assertFalse(e.clock_warning);s.close()
    def test_replay_and_recovery_preserve_input_and_scope(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(Path(d)/'source')
            for t in range(20):e.feed(sample(t)[0])
            s.close();original=s.roots[0]/'journal.jsonl'
            dest=Store(Path(d)/'replay');re=Engine(dest,source='REPLAY')
            replay_loop(re,original,10000);dest.close()
            self.assertEqual(re.total_unique,20)
            with self.assertRaises(ValueError):re.command('RUN')
            result=recover([original],Path(d)/'recovered')
            self.assertTrue(result['written']);self.assertTrue(result['originals_unchanged'])
            csv_source=next(s.roots[0].rglob('Flight_1000.csv'))
            result=recover([csv_source],Path(d)/'csv-only')
            self.assertTrue(result['written']);self.assertEqual(result['candidates'],20)
            result=recover([original,csv_source],Path(d)/'both')
            self.assertTrue(result['written']);self.assertEqual(result['candidates'],20)
            data=[json.loads(line) for line in original.read_text(encoding='utf-8').splitlines()]
            packet=next(x for x in data if x['kind']=='packet');packet['values'][5]='9999.0'
            conflicting=Path(d)/'conflict.jsonl';conflicting.write_text(json.dumps(packet)+'\n',encoding='utf-8')
            result=recover([original,conflicting],Path(d)/'blocked')
            self.assertFalse(result['written']);self.assertTrue(result['conflicts'])
    def test_malformed_control_and_late_result_never_rewind_epoch(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d)
            for raw in [b'@BENCH []\r',b'@BENCH {"v":"bench-usb-0.2","team":"1000","kind":[]}\r',
                        b'@BENCH {"v":"bench-usb-0.2","team":"1000","kind":"hello","boot":"b","run":"r","x":NaN}\r']:
                e.feed(raw)
            self.assertEqual(e.invalid,3)
            ident=e.command('POWER_STATUS');obj=e.outgoing.get();e.sent(obj)
            oldboot=b.boot;b.boot='newboot';b.hello();epoch=e.epoch
            e.feed(control(dict(team='1000',kind='result',id=ident,phase='executed',boot=oldboot,run='idle',voltage=4.1,solar_voltage=2.5)))
            self.assertEqual(e.epoch,epoch);self.assertIsNone(e.power);self.assertTrue(e.commands[ident]['late']);s.close()
    def test_reconnect_handshake_recovers_a_missed_boot_announcement(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d)
            old=e.epoch;e.feed(sample(0)[0]);e.disconnected('Corte simulado')
            b.boot='reconnectedboot';b.run='idle'
            e.connected();ident=e.handshake;obj=e.outgoing.get();e.sent(obj)
            b.execute(obj) # El puerto perdió el hello inicial del arranque.
            self.assertNotEqual(e.epoch,old);self.assertEqual(e.epoch[0],'reconnectedboot')
            self.assertEqual(e.commands[ident]['state'],'executed');self.assertFalse(e.commands[ident]['late'])
            self.assertFalse(e.ambiguous);self.assertIsNotNone(e.peer);s.close()

    def test_rom_download_boot_invalidates_old_values_without_hello(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d);e.feed(sample(0)[0]);old=e.segment
            pending=e.command('POWER_STATUS')
            e.feed(b'\nrst:0x1 (POWERON_RESET),boot:0x3 (DOWNLOAD_BOOT(UART0/UART1/SDIO_REI_REO_V2))\r\nwaiting for download\r')
            self.assertIsNone(e.latest);self.assertIsNone(e.epoch);self.assertIsNone(e.gps)
            self.assertTrue(e.ambiguous);self.assertTrue(e.waiting_identity)
            self.assertEqual(e.commands[pending]['state'],'unknown')
            # Sin anuncio nuevo no acepto una muestra bajo el contexto anterior.
            e.feed(sample(0)[0]);self.assertEqual(e.total_unique,1)
            b.boot='boot_after_button';b.hello();e.feed(sample(0)[0])
            self.assertNotEqual(e.segment,old);self.assertEqual(e.latest.count,1)
            self.assertFalse(e.waiting_identity);self.assertFalse(e.ambiguous)
            s.close()

    def test_rom_probe_recovers_missed_hello_without_repeating_old_orders(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d);e.feed(sample(0)[0])
            e.feed(b'\nrst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)\r')
            with patch('engine.time.monotonic',return_value=time.monotonic()+.6):e.expire()
            ident=e.handshake;self.assertIsNotNone(ident);obj=e.outgoing.get_nowait()
            b.boot='new_boot_without_hello';b.run='idle';e.sent(obj);b.execute(obj)
            self.assertEqual(e.epoch,(b.boot,'idle'));self.assertFalse(e.waiting_identity)
            self.assertEqual(e.commands[ident]['state'],'executed');self.assertIsNone(e.boot_probe_at)
            s.close()

    def test_long_burst_and_foreign_team_recover_without_mixing_telemetry(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(d)
            stream=b'@BENCH '+b'x'*2400+b'\r'+sample(0,team='1234')[0]+b'log de prueba\r'+sample(0)[0]
            for i in range(0,len(stream),13):e.feed(stream[i:i+13])
            self.assertEqual(e.overflows,1);self.assertEqual(e.invalid,1)
            self.assertEqual(e.diagnostics,1);self.assertEqual(e.total_unique,1)
            self.assertEqual(e.latest.count,1);self.assertFalse(e.stop.is_set())
            s.close()

    def test_run_identity_does_not_repeat_between_pc_sessions(self):
        with tempfile.TemporaryDirectory() as d:
            s,e,b=self.setup_engine(Path(d)/'first')
            e.command('RUN',scenario='NOMINAL',samples=10);b.execute(e.outgoing.get_nowait());first=b.run;boot=b.boot
            second=Store(Path(d)/'second');other=Engine(second,source='PC_BENCH');b.engine=other
            other.command('RUN',scenario='NOMINAL',samples=10);b.execute(other.outgoing.get_nowait())
            self.assertEqual(b.boot,boot);self.assertNotEqual(b.run,first)
            self.assertTrue(b.run.startswith(second.session+'_'))
            s.close();second.close()

    def test_replay_prefers_monotonic_elapsed_over_a_wall_clock_step(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'clock-step.jsonl'
            records=[dict(kind='segment',boot='recorded',run='one')]
            for tick,elapsed,stamp in [(0,2.,'2026-10-24T03:00:10+00:00'),(1,4.,'2026-10-24T03:00:09+00:00')]:
                records.append(dict(kind='wire',received_elapsed_seconds=elapsed,received_utc=stamp,raw_hex=sample(tick)[0].hex()))
            path.write_text('\n'.join(json.dumps(e) for e in records)+'\n',encoding='utf-8')
            store=Store(Path(d)/'out');engine=Engine(store,source='REPLAY')
            with patch.object(engine.stop,'wait',return_value=False) as wait:replay_loop(engine,path,speed=2)
            self.assertEqual(wait.call_args.args[0],1.)
            self.assertEqual(engine.total_unique,2)
            a=store.emit('check');b=store.emit('check')
            self.assertGreaterEqual(b['received_elapsed_seconds'],a['received_elapsed_seconds'])
            store.close()



class GPSPresentationTests(unittest.TestCase):
    def test_no_fix_never_promotes_untrusted_coordinates(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(d);e=Engine(s);b=PCBench(e);b.hello()
            try:
                raw=sample(50,'GPS_LOSS')[0]
                fields=raw[:-1].decode().split(',');fields[17:20]=['0.0','0.0000','0.0000']
                e.feed((','.join(fields)+'\r').encode())
                view,retained=telemetry_view(e.snapshot())
                self.assertIsNone(view['GPS_LATITUDE']);self.assertIsNone(view['GPS_TIME'])
                self.assertEqual(view['GPS_SATS'],'0');self.assertIn('GPS_LONGITUDE',retained)
                e.feed(sample(51)[0]);last=e.gps.copy()
                fields[2]='54';e.feed((','.join(fields)+'\r').encode())
                view,retained=telemetry_view(e.snapshot())
                for key in retained:self.assertEqual(view[key],last[key])
                self.assertEqual(e.latest.data['GPS_LATITUDE'],'0.0000')
                e.feed(sample(54)[0]);view,retained=telemetry_view(e.snapshot())
                self.assertFalse(retained);self.assertEqual(view['GPS_LATITUDE'],e.latest.data['GPS_LATITUDE'])
            finally:s.close()

class MemoryInstrumentationTests(unittest.TestCase):
    @unittest.skipUnless(__import__('sys').platform=='win32','Medidor de Windows')
    def test_memory_queries_do_not_accumulate_ctypes_pointer_types(self):
        import ctypes
        from app import working_set_bytes,windows_memory_api
        self.assertGreater(working_set_bytes(),0)
        initial=len(ctypes._pointer_type_cache)
        for _ in range(500):self.assertGreater(working_set_bytes(),0)
        self.assertEqual(len(ctypes._pointer_type_cache),initial)
        self.assertEqual(windows_memory_api.cache_info().misses,1)

if __name__=='__main__':unittest.main(verbosity=2)
