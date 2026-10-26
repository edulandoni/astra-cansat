"""ASTRA-41: reutilizo el receptor real con un emisor exclusivamente de PC."""
import sys
import threading
from pathlib import Path

AREA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AREA / 'banco-usb-v0.2'))
sys.path.insert(0, str(AREA / 'tools'))
from engine import Engine
from journal import Store
from sources import PCBench
from mission import sample
from wire import FIELDS
from airtime_lora import airtime


class Simulation:
    def __init__(self, output, scenario='NOMINAL', speed=5):
        if scenario not in ('NOMINAL', 'PACKET_LOSS', 'CORRUPTED_PACKET', 'GPS_LOSS', 'RESET'):
            raise ValueError('Escenario desconocido')
        if speed not in (1, 5, 10):
            raise ValueError('Velocidad desconocida')
        self.store = Store(output)
        self.engine = Engine(self.store, source='PC_BENCH')
        self.bench = PCBench(self.engine)
        self.thread = threading.Thread(target=self.bench.run_loop, args=(1/speed,), daemon=True)
        self.thread.start()
        self.engine.command('RUN', scenario=scenario, samples=131)

    def close(self):
        self.engine.stop.set()
        self.thread.join(2)
        self.store.close()


def packet_at(t):
    raw, _ = sample(int(t), 'NOMINAL', '1000', 46800, 12.)
    return raw, list(zip(FIELDS, raw.decode('ascii').strip().split(',')))


def radio_rows(payload, bw=125000, cr=1):
    return [airtime(payload, sf, bw, cr, 8, 1, 0) for sf in (7, 9, 10, 11, 12)]
