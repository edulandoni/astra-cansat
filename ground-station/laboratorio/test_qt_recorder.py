import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import time,unittest
from PySide6.QtWidgets import QApplication
from qt_recorder import RecorderPanel


def status(seq,frames):
    return dict(device='camera1',boot='boot1',segment='segment1',report_seq=seq,frames_captured=frames,frames_written=frames,bytes_written=frames*1000,uptime_ms=2000,last_write_ms=2000,recording=True,error='',segments_closed=0)


class PanelTests(unittest.TestCase):
    def tearDown(self):
        from qt_test_cleanup import cleanup_widgets
        cleanup_widgets()

    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])

    def test_explicit_buttons_and_detach_not_stop(self):
        calls=[];w=RecorderPanel(lambda *a:calls.append(a))
        try:
            self.assertFalse(w.active);w.start_button.click();self.assertEqual(calls,[(True,1,30)])
            w.prepare('camera1');w.detach_button.click()
            self.assertTrue(w.detach_event.is_set());self.assertFalse(w.stop_event.is_set())
        finally:w.timer.stop();w.close()

    def test_received_written_progress_and_stale(self):
        w=RecorderPanel(lambda *a:None)
        try:
            w.prepare('camera1')
            w.events.put(dict(report=status(1,0),received_at=time.monotonic()));w.refresh()
            self.assertIn('INICIO SIN GUARDADO',w.status.text())
            w.events.put(dict(report=status(2,5),received_at=time.monotonic()));w.refresh()
            self.assertIn('GUARDADO EN PROGRESO',w.status.text())
            w.health.received_at-=4;w.refresh();self.assertIn('ESTADO DESCONOCIDO',w.status.text())
            w.finished(dict(state='DETACHED',last=status(2,5)))
            self.assertIn('podría continuar',w.status.text());self.assertFalse(w.active)
        finally:w.timer.stop();w.close()

    def test_stop_is_explicit_and_cannot_be_repeated_by_button(self):
        w=RecorderPanel(lambda *a:None)
        try:
            w.prepare('camera1');w.stop_button.click()
            self.assertTrue(w.stop_event.is_set());self.assertFalse(w.stop_button.isEnabled())
        finally:w.timer.stop();w.close()


if __name__=='__main__':unittest.main()
