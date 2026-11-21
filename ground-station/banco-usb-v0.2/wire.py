"""ASTRA-20/21/24: perfil USB experimental; no es el ICD de vuelo."""
import json
import math
import re
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]/'banco-usb-v0.1'))
from protocol import FIELDS, parse

PROFILE = 'bench-usb-0.2'
SCENARIOS = ['NOMINAL','PACKET_LOSS','CORRUPTED_PACKET','GPS_LOSS','RESET']
OPERATIONS = {'RUN','STOP','CAL_ZERO','SET_TIME','POWER_STATUS'}

def control(message):
    obj = dict(v=PROFILE, **message)
    return b'@BENCH '+json.dumps(obj,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode('ascii')+b'\r'

def decode(raw, team='1000'):
    if raw.startswith(b'@BENCH '):
        def nonfinite(value):raise ValueError('Constante JSON no finita')
        try:obj=json.loads(raw[7:-1].decode('ascii'),parse_constant=nonfinite)
        except RecursionError:raise ValueError('JSON demasiado profundo')
        if not isinstance(obj,dict):raise ValueError('Objeto JSON requerido')
        if obj.get('v')!=PROFILE or obj.get('team')!=team:
            raise ValueError('Perfil/destino de banco inválido')
        if obj.get('kind') not in {'hello','result','oracle','done'}:
            raise ValueError('Clase de mensaje de banco inválida')
        for key in ['boot','run']:
            if not isinstance(obj.get(key),str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}',obj[key]):raise ValueError('Identidad de banco inválida')
        if obj['kind']=='result':
            if not isinstance(obj.get('id'),str) or len(obj['id'])>128 or obj.get('phase') not in {'accepted','executed','rejected'}:raise ValueError('Respuesta inválida')
            for key in ['voltage','solar_voltage']:
                if key in obj and (type(obj[key]) not in (int,float) or not math.isfinite(obj[key]) or obj[key]<0):raise ValueError('Alimentación inválida')
        if obj['kind']=='oracle' and (type(obj.get('count')) is not int or obj['count']<1 or obj.get('outcome') not in {'emitted','omitted','corrupted'}):raise ValueError('Oráculo inválido')
        return 'control',obj
    packet=parse(raw,team)
    if len(packet.values)!=22:
        raise ValueError('Esquema de 22 columnas requerido')
    return 'telemetry',packet

class Demux:
    """Conservo bytes originales; separo CR/LF de diagnóstico explícitamente.

    Sólo el perfil de banco admite el LF residual de las líneas ROM CR/LF.
    El parser heredado sigue validando sin modificaciones.
    """
    def __init__(self, maximum=2048):
        self.buffer=bytearray();self.maximum=maximum;self.discard=False
    def feed(self,data):
        result=[]
        for byte in data:
            if byte==13:
                raw=bytes(self.buffer)+b'\r';self.buffer.clear()
                if self.discard:
                    result.append(('overflow',b''));self.discard=False
                elif raw!=b'\r':result.append(('frame',raw))
            elif not self.discard:
                self.buffer.append(byte)
                if len(self.buffer)>self.maximum:
                    self.buffer.clear();self.discard=True
        return result

def classify(raw, team, bench=True):
    # La transformación queda registrada por Engine junto con el raw original.
    candidate=raw.lstrip(b'\n') if bench else raw
    if candidate.startswith(b'@BENCH ') or re.match(rb'^\d{4},',candidate):
        return decode(candidate,team)
    return 'diagnostic',{'text':raw.decode('ascii',errors='replace')}
