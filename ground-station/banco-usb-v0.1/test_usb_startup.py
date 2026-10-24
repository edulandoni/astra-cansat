"""ASTRA-21/22: separo arranque de banco sin reiniciar al reconectar.

Puerto simulado: estas pruebas no acreditan una desconexión USB física.
"""
import json
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
from acquisition import Acquisition
from simulator import sample
from storage import Recorder


class NoWaitEvent:
    def __init__(self):
        self.stopped = False
    def is_set(self):
        return self.stopped
    def set(self):
        self.stopped = True
    def wait(self, seconds):
        return self.stopped


class StartupTests(unittest.TestCase):
    def run_port(self, bench_reset):
        with tempfile.TemporaryDirectory() as tmp:
            recorder = Recorder(tmp, '1000')
            acq = Acquisition(recorder, port='COM_TEST', bench_reset=bench_reset)
            acq.stop = NoWaitEvent()
            links = []
            class Disconnected(Exception):
                pass
            class Link:
                def __init__(self, *args, **kwargs):
                    self.resets = 0
                    self.connection = len(links)
                    self.reads = 0
                    links.append(self)
                @property
                def rts(self):
                    return False
                @rts.setter
                def rts(self, value):
                    if value:
                        self.resets += 1
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def read(self, maximum):
                    self.reads += 1
                    if bench_reset and self.connection == 0 and self.reads == 1:
                        return b'ROM boot diagnostic\r\n'
                    if self.connection == 0:
                        if self.reads == (2 if bench_reset else 1):
                            return sample(0)
                        raise Disconnected('Interrupción de puerto simulada')
                    acq.stop.set()
                    return sample(1)
            fake = types.SimpleNamespace(Serial=Link, SerialException=Disconnected)
            clock = iter(n*.3 for n in range(100))
            with patch.dict('sys.modules', {'serial':fake}), patch('acquisition.time.monotonic', side_effect=lambda:next(clock)):
                acq.serial_loop()
            recorder.close()
            events = [json.loads(x) for x in (recorder.directory/'reception.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(acq.counter.unique, 2)
            self.assertEqual(acq.invalid, 0)
            self.assertEqual(len(links), 2)
            return links, events

    def test_bench_boot_preserved_and_reset_only_first_connection(self):
        links, events = self.run_port(True)
        self.assertEqual([x.resets for x in links], [1,0])
        self.assertEqual(sum(x['kind']=='bench_reset' for x in events), 1)
        self.assertEqual([bytes.fromhex(x['raw_hex']) for x in events if x['kind']=='startup_window'], [b'ROM boot diagnostic\r\n'])
        self.assertEqual(sum(x['kind']=='disconnect' for x in events), 1)

    def test_normal_serial_never_resets_or_discards_startup_window(self):
        links, events = self.run_port(False)
        self.assertEqual([x.resets for x in links], [0,0])
        self.assertFalse(any(x['kind'] in {'bench_reset','startup_window'} for x in events))


if __name__ == '__main__':
    unittest.main()
