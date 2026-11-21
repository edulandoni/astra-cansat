"""ASTRA-21/22: continuidad y presentación sin deducir mensajes no observados."""
import tempfile,unittest
from pathlib import Path
from engine import Engine
from journal import Store
from sources import PCBench
from mission import sample
from ui_model import presentation,controls,command_text
from quality import quality_flags

class UITests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.store=Store(self.tmp.name);self.now=[100.]
        self.e=Engine(self.store,clock=lambda:self.now[0]);self.b=PCBench(self.e)
        self.e.connected();self.b.hello()
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def packet(self,t):self.e.feed(sample(t)[0])
    def test_disconnect_age_pending_and_deduplicated_outage(self):
        self.packet(10);self.assertTrue(self.store.drain());self.now[0]+=2
        self.e.disconnected('USB retirado');self.now[0]+=5;self.e.disconnected('Sigue ausente')
        s=self.e.snapshot();v=presentation(s)
        self.assertEqual(len(s['interruptions']),1);self.assertEqual(s['interruptions'][0]['duration'],5)
        self.assertEqual(s['last_sample_age'],7);self.assertIsNone(s['latest'])
        self.assertEqual(v['values']['PACKET_COUNT'],'11');self.assertTrue(v['old'])
        self.assertIn('desconectada',v['title']);self.assertIn('no es una medición actual',v['note'])
        self.assertIn('no determinables',v['interruption']);self.assertFalse(any(controls(s).values()))
        self.assertEqual(v['gap_value'],'Por determinar');self.assertIn('Ya observados',v['gap_note'])
        self.assertEqual(s['storage'][1]['pending'],0);self.assertEqual(s['observed_gaps'],0)
    def test_same_identity_gap_and_late_repair(self):
        self.packet(10);self.e.disconnected('corte');self.now[0]+=6
        self.e.connected();self.b.hello();self.packet(15)
        s=self.e.snapshot();c=s['interruptions'][-1]
        self.assertEqual(c['result'],'same_run');self.assertEqual(c['gap_at_resume'],4)
        self.assertEqual(s['observed_gaps'],4)
        self.assertEqual(presentation(s)['gap_value'],'4')
        self.packet(11);self.assertEqual(self.e.snapshot()['observed_gaps'],3)
        self.assertEqual(c['duration'],6)
    def test_restart_does_not_invent_missing_packets_or_current_values(self):
        self.packet(80);self.e.disconnected('USB');self.now[0]+=20
        self.e.connected();self.b.boot='new-boot';self.b.hello()
        s=self.e.snapshot();self.assertEqual(s['interruptions'][-1]['result'],'restarted')
        self.assertIsNone(s['interruptions'][-1]['gap_at_resume']);self.assertEqual(s['observed_gaps'],0)
        v=presentation(s);self.assertTrue(v['old']);self.assertIn('no puedo determinar',v['interruption'])
        self.assertIn('desconocida',v['gap_note'])
        self.packet(0);self.assertFalse(presentation(self.e.snapshot())['old'])
        self.assertEqual(self.e.snapshot()['last_counter'],1)
    def test_new_run_is_not_restart_or_loss(self):
        self.packet(10);self.e.disconnected('corte');self.e.connected();self.b.run='another-run';self.b.hello()
        c=self.e.snapshot()['interruptions'][-1];self.assertEqual(c['result'],'new_run');self.assertIsNone(c['gap_at_resume'])
    def test_manual_close_does_not_claim_auto_reconnect(self):
        self.packet(1);self.e.disconnected('Cierre manual del puerto')
        v=presentation(self.e.snapshot());self.assertIn('Conectar USB',v['explanation'])
        self.assertNotIn('automáticamente',v['explanation']);self.e.connected();self.assertFalse(self.e.snapshot()['manual_closed'])
    def test_controls_and_stopped_expectation(self):
        self.packet(0);self.assertTrue(controls(self.e.snapshot())['CAL_ZERO'])
        self.packet(20);self.assertFalse(controls(self.e.snapshot())['CAL_ZERO'])
        self.e.command('STOP');obj=self.e.outgoing.get()
        while obj['op']!='STOP':obj=self.e.outgoing.get()
        self.e.sent(obj);self.b.execute(obj);self.now[0]+=10
        s=self.e.snapshot();self.assertTrue(s['paused']);self.assertFalse(quality_flags(s)['telemetry_stale'])
        self.assertEqual(presentation(s)['title'],'Ensayo detenido')
        self.assertFalse(controls(s)['STOP']);self.assertTrue(controls(s)['RUN'])
        s['source']='REPLAY';self.assertFalse(any(controls(s).values()))
    def test_legacy_no_identity_does_not_confirm_gap(self):
        self.e.profile='legacy-usb-0.1';self.packet(10);self.e.disconnected('corte');self.e.connected();self.packet(20)
        self.assertEqual(self.e.snapshot()['interruptions'][-1]['result'],'unknown')
    def test_command_status_does_not_equate_sent_with_executed(self):
        c={'op':'RUN','state':'timeout','result':{},'late':False}
        self.assertIn('no sé si se ejecutó',command_text(c))
        c.update(state='unknown');self.assertIn('desconocido',command_text(c))
        c.update(state='rejected',result={'reason':'NOT_LAUNCH_PAD'})
        self.assertIn('Sólo se permite',command_text(c))
        c.update(state='executed',result={'boot':'old','run':'old-run'})
        self.assertIn('otra ejecución',command_text(c,('new','idle')))
        self.assertNotIn('otra ejecución',command_text(c,('old','old-run')))

if __name__=='__main__':unittest.main(verbosity=2)
