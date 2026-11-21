"""ASTRA-39: solicitud explícita de una secuencia de banco, sin reintento/reset.

El cierre comunicado por cámara es un reporte. La prueba requiere después
el lector y sequence_verify.py; no envío cuadros por RF ni activo Wi-Fi.
"""
import argparse
from datetime import datetime,timezone
import json
import re
import secrets
import time
from pathlib import Path
from camera_check import validate_peer,ProtocolError


class Controls:
    def __init__(self):self.buffer=bytearray();self.messages=[]
    def feed(self,data):
        if len(data)>4096:raise ProtocolError('Bloque de recepción demasiado grande')
        self.buffer.extend(data)
        while b'\n' in self.buffer:
            line,_,rest=self.buffer.partition(b'\n');self.buffer=bytearray(rest)
            if len(line)>1024:raise ProtocolError('Control demasiado largo')
            if b'waiting for download' in line or b'DOWNLOAD_BOOT(' in line:raise ProtocolError('La placa espera programación; hace falta arranque normal')
            if not line.startswith(b'@CAM '):continue
            try:obj=json.loads(line[5:])
            except (ValueError,UnicodeError) as exc:raise ProtocolError('Control inválido') from exc
            if not isinstance(obj,dict) or type(obj.get('v')) is not int or obj['v']!=1:raise ProtocolError('Versión incompatible')
            if obj.get('event') not in ('info','error','sequence'):raise ProtocolError('Respuesta incompatible con secuencia')
            self.messages.append(obj)
            if len(self.messages)>128:raise ProtocolError('Demasiados controles pendientes')
        if len(self.buffer)>1024:raise ProtocolError('Control incompleto demasiado largo')


def receive(port,raw,decoder,request_id,event,budget,clock=time.monotonic):
    until=clock()+budget
    while clock()<until:
        while decoder.messages:
            msg=decoder.messages.pop(0)
            if msg.get('id')==request_id and msg.get('event') in (event,'error'):return msg
        data=port.read(512)
        if data:
            if raw.tell()+len(data)>2*1024*1024:raise ProtocolError('Registro de recepción fuera de límite')
            raw.write(data);raw.flush();decoder.feed(data)
    raise TimeoutError('Sin confirmación: resultado desconocido. No reenvío la orden.')


def request(port,raw,expected_device,ids=lambda:secrets.token_hex(8)):
    decoder=Controls(); ident=ids()
    port.write(f'INFO {ident}\n'.encode('ascii'));port.flush()
    info=receive(port,raw,decoder,ident,'info',15)
    if info['event']=='error':return dict(state='reported_error',phase='INFO',response=info)
    validate_peer(info,expected_device)
    if not re.fullmatch(r'[0-9a-f]{16}',str(info.get('boot',''))):raise ProtocolError('Arranque inválido')
    if 'CLIP' not in info.get('commands',[]):raise ProtocolError('El firmware no anuncia CLIP; no envío una orden desconocida')
    ident=ids();port.write(f'CLIP {ident}\n'.encode('ascii'));port.flush()
    msg=receive(port,raw,decoder,ident,'sequence',60)
    if msg.get('boot')!=info['boot']:raise ProtocolError('Arranque cambió: resultado de secuencia desconocido')
    if msg['event']=='error':return dict(state='reported_error',phase='CLIP',response=msg)
    if msg.get('device')!=info['device']:raise ProtocolError('Respuesta de otra unidad')
    if msg.get('path')!=f"/ASTRA_SEQ_{info['boot']}_{ident}":raise ProtocolError('Carpeta no corresponde a la solicitud')
    if type(msg.get('frames')) is not int or not 0<=msg['frames']<=12 or msg.get('expected_frames')!=12 or type(msg.get('closed')) is not bool:raise ProtocolError('Resumen de secuencia inválido')
    if msg['closed'] and (msg['frames']!=12 or msg.get('reason')!='COMPLETE'):raise ProtocolError('Cierre contradictorio')
    return dict(state='reported_closed' if msg['closed'] else 'reported_partial',response=msg,
                independent_readback_verified=False,
                note='Es el reporte del emisor: falta lector, integridad/decodificación y revisión temporal de la escena.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',required=True);p.add_argument('--expect-device',required=True)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    if not re.fullmatch(r'[a-f0-9]{16}',args.expect_device):p.error('Identidad de 16 hexadecimales del registro privado')
    destination=args.output/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_')+secrets.token_hex(5))
    destination.mkdir(parents=True,exist_ok=False)
    result=dict(state='not_sent',source='camera',physical_test_completed=False)
    try:
        import serial
        port=serial.Serial(port=None,baudrate=115200,timeout=.2,write_timeout=3)
        port.dtr=False;port.rts=False;port.port=args.port
        with port,(destination/'received.bin').open('xb') as raw:
            result=request(port,raw,args.expect_device)
    except (OSError,ValueError,TimeoutError) as exc:result=dict(state='unknown_or_not_sent',error=str(exc),automatic_retry=False)
    finally:
        with (destination/'request-result.json').open('x',encoding='utf-8') as out:json.dump(result,out,ensure_ascii=False,indent=2)
    print(json.dumps(dict(folder=str(destination),**result),ensure_ascii=True))
    return 0 if result['state']=='reported_closed' else 1

if __name__=='__main__':raise SystemExit(main())
