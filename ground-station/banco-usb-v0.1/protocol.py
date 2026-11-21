"""Legacy v1 bench ASCII adapter, not an approved CONAE v2 wire profile.

See AVISO_BASELINE_V2.txt. RF framing/CRC/addressing remain unconfigured.
"""
import math
import re
from dataclasses import dataclass

FIELDS = 'TEAM_ID MISSION_TIME PACKET_COUNT MODE STATE ALTITUDE TEMPERATURE PRESSURE VOLTAGE CURRENT GYRO_R GYRO_P GYRO_Y ACCEL_R ACCEL_P ACCEL_Y GPS_TIME GPS_ALTITUDE GPS_LATITUDE GPS_LONGITUDE GPS_SATS CMD_ECHO'.split()
STATES = {'LAUNCH_PAD', 'ASCENT', 'APOGEE', 'DESCENT', 'PROBE_RELEASE', 'PAYLOAD_RELEASE', 'LANDED'}
NUMERIC = FIELDS[5:16] + FIELDS[17:20]

def utc_valid(value):
    return bool(re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d', value))

@dataclass
class Packet:
    values: list
    @property
    def data(self):
        return dict(zip(FIELDS, self.values))
    @property
    def count(self):
        return int(self.values[2])

def parse(raw, team):
    if not re.fullmatch(r'[0-9]{4}', team):
        raise ValueError('TEAM_ID configurado inválido')
    text = raw.decode('ascii', errors='strict')
    if not text.endswith('\r') or '\r' in text[:-1] or '\n' in text:
        raise ValueError('Framing: se requiere CR único')
    values = text[:-1].split(',')
    if len(values) < 22 or (len(values) > 22 and (len(values) < 24 or values[22] != '')):
        raise ValueError('Campos o separador opcional inválidos')
    if values[0] != team:
        raise ValueError('TEAM_ID ajeno')
    if not utc_valid(values[1]) or not utc_valid(values[16]):
        raise ValueError('Hora UTC inválida')
    if not re.fullmatch(r'[0-9]+', values[2]) or not re.fullmatch(r'[0-9]+', values[20]):
        raise ValueError('Contador o satélites inválidos')
    if values[3] not in {'F', 'S'} or values[4] not in STATES:
        raise ValueError('Modo o estado inválido')
    for name in NUMERIC:
        x = float(values[FIELDS.index(name)])
        if not math.isfinite(x):
            raise ValueError('Número no finito')
    if float(values[7]) <= 0 or float(values[8]) < 0 or float(values[9]) < 0:
        raise ValueError('Presión/alimentación inválida')
    if not -90 <= float(values[18]) <= 90 or not -180 <= float(values[19]) <= 180:
        raise ValueError('Coordenadas inválidas')
    if any(any(ord(c) < 32 or ord(c) > 126 for c in s) for s in values):
        raise ValueError('Caracteres de control')
    return Packet(values)

class Framer:
    """Bounded CR framing; discard overlong frames until their next CR."""
    def __init__(self, maximum=2048):
        self.buffer = bytearray()
        self.maximum = maximum
        self.discard = False
        self.overflows = 0
    def feed(self, data):
        result = []
        for b in data:
            if b == 13:
                if not self.discard and self.buffer:
                    result.append(bytes(self.buffer) + b'\r')
                self.buffer.clear()
                self.discard = False
            elif not self.discard:
                self.buffer.append(b)
                if len(self.buffer) > self.maximum:
                    self.buffer.clear()
                    self.discard = True
                    self.overflows += 1
        return result

class Counter:
    """Track observed gaps; no fabricated losses before first reception.

    A backwards unseen sequence is ambiguous (reset/late packet). Explicit
    session restart is required for a real counter reset; never normalize it.
    """
    def __init__(self):
        self.received = 0
        self.unique = 0
        self.duplicates = 0
        self.high = None
        self.missing = []
        self.seen = set()
        self.warning = ''
    @property
    def lost(self):
        return sum(b-a+1 for a,b in self.missing)
    def add(self, n):
        self.received += 1
        if n in self.seen:
            self.duplicates += 1
            if self.high is not None and n < self.high:
                self.warning = 'Contador anterior: duplicado/atrasado o reset; revisar sesión'
            return False
        self.seen.add(n)
        self.unique += 1
        if self.high is None:
            self.high = n
        elif n > self.high:
            if n > self.high + 1:
                self.missing.append((self.high+1, n-1))
            self.high = n
        else:
            found = False
            intervals = []
            for a,b in self.missing:
                if a <= n <= b:
                    found = True
                    if a < n: intervals.append((a,n-1))
                    if n < b: intervals.append((n+1,b))
                else:
                    intervals.append((a,b))
            self.missing = intervals
            if not found:
                self.warning = 'Contador retrocedió: revisar reset/sesión; no estimar pérdidas'
        return True
