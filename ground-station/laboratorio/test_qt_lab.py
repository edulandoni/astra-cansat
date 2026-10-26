"""ASTRA-41/22: Qt fuera de pantalla; nunca ocupa el escritorio ni abre USB."""
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication,QLabel
from qt_app import Laboratory
from qt_model import Source,source_view
from runtime import sample


class QtLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])
        assert cls.app.platformName()=='offscreen'

    def test_initial_state_and_entire_tour_offscreen(self):
        with patch('serial.Serial',side_effect=AssertionError('No abrir puertos')),patch('serial.tools.list_ports.comports',return_value=[]):
            w=Laboratory();w.show();self.app.processEvents()
            self.assertIsNone(w.source)
            self.assertEqual(w.origin.text(),'SIN FUENTE DE DATOS')
            self.assertTrue(all(v.text()=='—' for v in w.metric_values.values()))
            for i in range(7):
                w.show_step(i);w.story_demo();self.app.processEvents()
                self.assertEqual(w.step,i)
                self.assertTrue(w.story_title.text());self.assertTrue(w.story_proof.text())
            for key in w.nav:w.go(key);self.app.processEvents()
            self.assertEqual(w.documents.count(),12)
            w.close();self.app.processEvents()

    def test_usb_disconnect_never_starts_pc_emitter(self):
        ready=threading.Event()
        def cable(engine,port,**kwargs):
            engine.connected();engine.context('testboot','testmission')
            engine.feed(sample(0)[0]);ready.set();engine.stop.wait()
        with tempfile.TemporaryDirectory() as folder,patch('qt_model.serial_loop',side_effect=cable),patch('qt_model.PCBench',side_effect=AssertionError('No simular al desconectar')):
            source=Source(folder,'usb',port='COM_TEST')
            try:
                self.assertTrue(ready.wait(2));before=source.engine.snapshot()['total_valid']
                source.engine.disconnected('Desconexión de prueba')
                view=source_view(source)
                self.assertEqual(view['mode'],'usb');self.assertEqual(view['title'],'Placa desconectada')
                self.assertTrue(view['old']);self.assertEqual(source.engine.snapshot()['total_valid'],before)
                self.assertIn('USB',view['badge']);self.assertNotIn('SIN PLACA',view['badge'])
            finally:
                source.stop();source.closer.join(5);self.assertTrue(source.closed)

    def test_explicit_pc_simulation_and_safe_close(self):
        with tempfile.TemporaryDirectory() as folder,patch('serial.Serial',side_effect=AssertionError('La simulación no usa USB')),patch('serial.tools.list_ports.comports',return_value=[]):
            w=Laboratory({'output':folder});w.start_source('pc',speed=10)
            until=time.monotonic()+3
            while w.source.engine.snapshot()['total_valid']<2 and time.monotonic()<until:
                self.app.processEvents();time.sleep(.02)
            w.refresh();self.assertIn('SIMULACIÓN',w.origin.text());self.assertGreater(w.source.engine.snapshot()['total_valid'],0)
            w.close()
            until=time.monotonic()+6
            while not w.source.closed and time.monotonic()<until:self.app.processEvents();time.sleep(.02)
            self.app.processEvents();self.assertTrue(w.source.closed)
            self.assertTrue(all(not t.thread.is_alive() for t in w.source.store.writers))

    def test_missing_port_and_no_fake_packet(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):Source(folder,'usb')
            self.assertEqual(source_view(None)['values'],{})

    def test_replay_is_readonly_and_preserves_original(self):
        import hashlib
        from runtime import Store,Engine
        with tempfile.TemporaryDirectory() as folder,patch('serial.Serial',side_effect=AssertionError('La reproducción no usa USB')):
            store=Store(Path(folder)/'original');engine=Engine(store,source='PC_BENCH')
            engine.connected();engine.context('testboot','testmission');engine.feed(sample(0)[0]);store.close()
            journal=store.roots[0]/'journal.jsonl';before=hashlib.sha256(journal.read_bytes()).hexdigest()
            source=Source(Path(folder)/'reproduccion','replay',replay=journal,speed=10)
            try:
                source.worker.join(3);self.assertFalse(source.worker.is_alive())
                view=source_view(source);self.assertIn('REPRODUCCIÓN',view['badge'])
                self.assertGreater(source.engine.snapshot()['total_valid'],0)
                self.assertEqual(hashlib.sha256(journal.read_bytes()).hexdigest(),before)
                self.assertNotEqual(source.store.roots[0],store.roots[0])
            finally:source.stop();source.closer.join(5)


if __name__=='__main__':unittest.main()
