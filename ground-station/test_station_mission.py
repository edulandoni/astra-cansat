"""ASTRA-22 acceptance smoke test. Run on an authorized Qt machine."""
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import station
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QTabBar
from ui_model import FIELDS_INFO


APP = station.QApplication.instance() or station.QApplication([])
station.configure_font(APP)
FIXTURE = (Path(station.__file__).parent / "evidence" / "2026-10-24-banco02"
           / "replay-tramas-aceptadas-entrada-04.jsonl")


def wait_for(check, timeout=12):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        APP.processEvents()
        if check():
            return
        time.sleep(0.025)
    raise AssertionError("Condition did not become true before the timeout")


class MissionViewTest(unittest.TestCase):
    def test_replay_and_fault_indications(self):
        with tempfile.TemporaryDirectory() as output:
            window = station.Station(output)
            window.resize(1600, 1000)
            window.show()
            try:
                APP.processEvents()
                self.assertEqual(set(window.readings), set(FIELDS_INFO))
                page = window.operation_page
                self.assertFalse(any(tabs.isVisible() for tabs in window.findChildren(QTabBar)))
                for widget in (*window.readings.values(), *window.mission_plots):
                    self.assertTrue(widget.isVisible())
                    upper = widget.mapTo(page, QPoint(0, 0))
                    lower = widget.mapTo(page, widget.rect().bottomRight())
                    self.assertTrue(page.rect().contains(upper))
                    self.assertTrue(page.rect().contains(lower))
                self.assertTrue(all(value.text() == "—" for value in window.readings.values()))
                window.start("replay", replay=FIXTURE, speed=10)
                wait_for(lambda: all(len(plot.points) >= 2 for plot in window.mission_plots))
                self.assertIn("REPRODUCCIÓN", window.signal.text())
                for label in window.readings.values():
                    self.assertLessEqual(label.heightForWidth(label.width()), label.height())
                self.assertFalse(any(b.isEnabled() for b in window.telemetry.command_buttons.values()))

                captured = station.source_view(window.source)
                snapshot = dict(captured["snapshot"])
                snapshot["storage"] = [dict(w, error="Injected writer failure")
                                       if w["destination"] == 0 and w["kind"] == "csv" else w
                                       for w in snapshot["storage"]]
                snapshot["latest"] = dict(snapshot["latest"], GPS_SATS="0")
                with patch.object(station, "source_view",
                                  return_value=dict(captured, old=True, snapshot=snapshot)):
                    window.refresh()
                self.assertIn("conservada", window.detail.text())
                self.assertIn("REVISAR GUARDADO", window.primary.text())
                self.assertEqual(window.readings["GPS_LATITUDE"].text(), "Sin solución")
            finally:
                window.stop()
                if window.source:
                    wait_for(lambda: window.source.closed)
                window.close()
                APP.processEvents()
            self.assertTrue(list(Path(output).rglob("storage-summary.json")))


if __name__ == "__main__":
    unittest.main()
