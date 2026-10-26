"""ASTRA-41: cierre Qt fuera de pantalla, también durante recuperación."""
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import tempfile
import time
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from app import Laboratory


class CloseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])
        assert cls.app.platformName()=='offscreen'

    def test_close_during_recovery_preserves_result(self):
        from pathlib import Path
        with tempfile.TemporaryDirectory() as folder,patch('serial.tools.list_ports.comports',return_value=[]):
            w=Laboratory({'output':folder});w.show();self.app.processEvents()
            w.recover('complementarias');w.close()
            end=time.monotonic()+8
            while w.isVisible() and time.monotonic()<end:self.app.processEvents();time.sleep(.01)
            self.assertFalse(w.isVisible());self.assertEqual(w.jobs,[])
            self.assertEqual(len(list(Path(folder).rglob('recovery-result.json'))),1)

if __name__=='__main__':unittest.main()
