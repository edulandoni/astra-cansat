"""ASTRA-39/24: propietario único del USB de grabación; nunca reinicia ni reintenta órdenes."""
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import queue
import secrets
import time
from camera_check import validate_peer


class CommandRejected(ValueError):pass


class RecorderLink:
    def __init__(self, port, device, raw=None, clock=time.monotonic):
        self.port, self.device, self.raw, self.clock = port, device, raw, clock
        self.buffer=bytearray();self.messages=deque();self.boot=None
        self.last_seq=None;self.logged=0

    def _feed(self,data):
        if len(data)>4096:raise ValueError('Bloque USB fuera de límite.')
        if self.raw:
            self.logged+=len(data)
            if self.logged>16*1024*1024:raise ValueError('Registro USB lleno; el estado de cámara queda desconocido.')
            self.raw.write(data);self.raw.flush()
        self.buffer.extend(data)
        while b'\n' in self.buffer:
            line,_,rest=self.buffer.partition(b'\n');self.buffer=bytearray(rest)
            if len(line)>4096:raise ValueError('Respuesta USB excesiva.')
            if b'waiting for download' in line or b'DOWNLOAD_BOOT(' in line:raise ValueError('La placa espera programación; no reinicio una grabación automáticamente.')
            if not line.startswith(b'@CAM '):continue
            obj=json.loads(line[5:])
            if not isinstance(obj,dict) or obj.get('v')!=1 or obj.get('event') not in ('info','error','recorder'):
                raise ValueError('Respuesta incompatible con grabación.')
            self.messages.append(obj)
            if len(self.messages)>64:raise ValueError('Demasiadas respuestas pendientes.')
        if len(self.buffer)>4096:raise ValueError('Respuesta incompleta excesiva.')

    def request(self,command,event='recorder',budget=3,ident=None):
        ident=ident or secrets.token_hex(8)
        if not re.fullmatch('[a-f0-9]{16}',ident):raise ValueError('Identificador de orden inválido.')
        verb,*args=command.split()
        line=' '.join([verb,ident,*args])+'\n'
        self.port.write(line.encode('ascii'));self.port.flush()
        until=self.clock()+budget
        while self.clock()<until:
            while self.messages:
                msg=self.messages.popleft()
                if msg.get('id')!=ident:continue
                if self.boot and msg.get('boot')!=self.boot:raise ValueError('La cámara reinició; resultado desconocido.')
                if msg['event']=='error':
                    reason=str(msg.get('reason'))
                    messages={'WIFI_MUST_BE_OFF':'Desactivá el Wi-Fi de la cámara por USB antes de iniciar grabación.',
                              'RECORDING_BUSY':'Ya hay una grabación en curso. Usá Consultar grabación.',
                              'RUN_MISMATCH':'La parada no corresponde a la grabación actual.',
                              'RUN_ARGUMENT_CONFLICT':'La misma orden de inicio tiene una duración diferente.'}
                    raise CommandRejected(messages.get(reason,'Orden rechazada: '+reason))
                if msg['event']!=event:raise ValueError('Confirmación de otro tipo.')
                if event=='recorder':self.validate_status(msg)
                return msg
            data=self.port.read(512)
            if data:self._feed(data)
        raise TimeoutError('Sin confirmación. La cámara podría seguir grabando; no repito la orden.')

    def identify(self):
        info=self.request('INFO',event='info',budget=10)
        validate_peer(info,self.device)
        if not re.fullmatch('[a-f0-9]{16}',info.get('boot','')):raise ValueError('Identidad de arranque inválida.')
        if not {'REC_START','REC_STOP','REC_STATUS'}<=set(info.get('commands',[])):
            raise ValueError('Este firmware no anuncia grabación continua; no envío órdenes nuevas.')
        self.boot=info['boot'];return info

    def validate_status(self,r):
        if r.get('profile')!='camera-recorder-0.1' or r.get('device')!=self.device or r.get('boot')!=self.boot:
            raise ValueError('Reporte de otro perfil, cámara o arranque.')
        for field in ['report_seq','frames_captured','frames_written','frames_readback','bytes_written','uptime_ms','last_write_ms','free_bytes','segments_closed']:
            if type(r.get(field)) is not int or r[field]<0:raise ValueError('Contador de grabación inválido: '+field)
        if self.last_seq is not None and r['report_seq']<=self.last_seq:raise ValueError('Reporte repetido: no renuevo el estado.')
        if (type(r.get('recording')) is not bool or r['frames_captured']<r['frames_written'] or r['frames_readback']!=r['frames_written'] or r['last_write_ms']>r['uptime_ms']):
            raise ValueError('Progreso de grabación contradictorio.')
        if r.get('state') not in ('IDLE','RECORDING','CLOSING','COMPLETE','FAILED') or r['recording']!=(r['state']=='RECORDING'):
            raise ValueError('Estado de grabación contradictorio.')
        if r['state']!='IDLE' and not re.fullmatch('[a-f0-9]{16}',r.get('run','')):raise ValueError('Falta identidad de ejecución.')
        self.last_seq=r['report_seq']

    def start(self,seconds,ident=None):
        if type(seconds) is not int or not 1<=seconds<=3600:raise ValueError('Duración de banco entre 1 y 3600 segundos.')
        ident=ident or secrets.token_hex(8)
        r=self.request(f'REC_START {self.boot} {seconds}',budget=15,ident=ident)
        if r.get('run')!=ident:raise ValueError('El inicio corresponde a otra ejecución.')
        return r

    def status(self):return self.request('REC_STATUS')

    def stop(self,run,ident=None):
        if not re.fullmatch('[a-f0-9]{16}',run):raise ValueError('Ejecución inválida para detener.')
        r=self.request(f'REC_STOP {self.boot} {run}',budget=15,ident=ident)
        if r.get('run')!=run:raise ValueError('La parada corresponde a otra ejecución.')
        return r


def monitor(port_name,device,output,seconds,start,stop_event,detach_event,events,serial_factory=None):
    """El cierre del monitor no envía STOP; la duración límite vive en la cámara."""
    destination=Path(output)/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_')+secrets.token_hex(5))
    destination.mkdir(parents=True,exist_ok=False)
    result=dict(state='UNKNOWN',last=None,folder=str(destination),independent_readback_verified=False)
    try:
        if serial_factory is None:
            import serial
            serial_factory=serial.Serial
        port=serial_factory(port=None,baudrate=115200,timeout=.2,write_timeout=3)
        port.dtr=False;port.rts=False;port.port=port_name
        with port,(destination/'received.bin').open('xb') as raw,(destination/'status.jsonl').open('x',encoding='utf-8') as journal:
            link=RecorderLink(port,device,raw);link.identify()
            r=link.start(seconds) if start else link.status()
            stopping=False
            while True:
                event={'report':r,'received_at':time.monotonic()}
                journal.write(json.dumps(event,ensure_ascii=False)+'\n');journal.flush()
                if events.full():
                    try:events.get_nowait()
                    except queue.Empty:pass
                events.put_nowait(event);result['last']=r
                if not r['recording']:
                    result['state']=r['state'];break
                if detach_event.is_set():result['state']='DETACHED';break
                if stop_event.is_set() and not stopping:
                    stopping=True;r=link.stop(r['run']);continue
                if detach_event.wait(1):result['state']='DETACHED';break
                r=link.status()
    except CommandRejected as exc:
        result.update(state='REJECTED',error=str(exc),automatic_retry=False)
    except Exception as exc:
        result.update(state='UNKNOWN',error=str(exc),automatic_retry=False)
    (destination/'monitor-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result
