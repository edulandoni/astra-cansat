import queue
import threading
import time
from protocol import Framer, Counter, parse
from simulator import sample

class Acquisition:
    def __init__(self, recorder, team='1000', scenario='NOMINAL', port=None, baud=115200):
        self.recorder, self.team, self.scenario = recorder, team, scenario
        self.port, self.baud = port, baud
        self.counter = Counter()
        self.invalid = 0
        self.status = 'Iniciando'
        self.latest = None
        self.last_rx = None
        self.lock = threading.Lock()
        self.updates = queue.Queue(maxsize=250)
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.run,daemon=True)
    def ingest(self, raw):
        try:
            packet = parse(raw,self.team)
            if len(packet.values) != 22:
                raise ValueError('Extensión opcional aún sin esquema de columnas acordado')
        except (ValueError,UnicodeError) as exc:
            self.invalid += 1
            self.recorder.event(kind='rejected',reason=str(exc),raw_hex=raw.hex())
            return
        self.recorder.event(kind='accepted',raw=raw.decode('ascii'))
        self.last_rx = time.monotonic()
        fresh = self.counter.add(packet.count)
        if fresh:
            self.recorder.save(packet)
            # Late packets fill history without replacing current live values.
            with self.lock:
                if self.latest is None or packet.count > self.latest.count:
                    self.latest = packet
            try:
                self.updates.put_nowait(packet)
            except queue.Full:
                # Presentation may lag; acquisition and storage continue.
                self.updates.get_nowait()
                self.updates.put_nowait(packet)
    def run(self):
        try:
            if self.port:
                self.serial_loop()
            else:
                self.status = 'SIMULACIÓN PC — sin radio'
                for t in range(131):
                    if self.stop.is_set(): break
                    raw = sample(t,self.team,self.scenario)
                    if raw: self.ingest(raw)
                    self.stop.wait(1)
                self.status = 'Misión simulada terminada'
        except Exception as exc:
            self.status = f'ERROR: {exc}'
        finally:
            self.recorder.close()
    def serial_loop(self):
        try:
            import serial
        except ImportError:
            self.status = 'Falta pyserial: instalar requirements.txt'
            return
        while not self.stop.is_set():
            try:
                with serial.Serial(self.port,self.baud,timeout=.2) as link:
                    # New framer for each connection; no joining stale fragments.
                    framer = Framer()
                    self.status = f'USB {self.port} conectado'
                    while not self.stop.is_set():
                        data = link.read(512)
                        before = framer.overflows
                        for raw in framer.feed(data): self.ingest(raw)
                        if framer.overflows > before:
                            self.invalid += framer.overflows-before
                            self.recorder.event(kind='framing_overflow')
            except (serial.SerialException,OSError) as exc:
                self.status = f'Desconectado; reintentando: {exc}'
                self.recorder.event(kind='disconnect',reason=str(exc))
                self.stop.wait(2)
