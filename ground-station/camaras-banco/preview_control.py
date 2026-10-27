"""ASTRA-39: activación local explícita. No guarda claves, no reinicia ni reintenta."""
import argparse
import getpass
import json
import re
import secrets
import time
from camera_check import validate_peer
from camera_session import read_registry


def exchange(port, verb, expected, password=None, clock=time.monotonic):
    def send(command, event):
        ident = secrets.token_hex(8)
        line = f'{command} {ident}' + (f' {password}' if command == 'WIFI_ON' else '')
        port.write((line+'\n').encode('ascii'))
        port.flush()
        until = clock()+15
        while clock() < until:
            raw = port.read_until(b'\n', 1025)
            if len(raw) > 1024:
                raise ValueError('Respuesta demasiado larga.')
            if b'waiting for download' in raw:
                raise ValueError('La cámara espera programación; necesita arranque normal.')
            if not raw.startswith(b'@CAM '):
                continue
            message = json.loads(raw[5:])
            if message.get('id') != ident:
                continue
            if message.get('event') == 'error':
                reason=str(message.get('reason'))
                explanation={
                    'WIFI_ALREADY_ACTIVE':'La red de esta cámara ya está activa. Desactivala por USB antes de generar otra clave.',
                    'CAMERA_INIT_FAILED':'El sensor no está preparado. No se activó la vista previa.',
                    'PREVIEW_MEMORY_FAILED':'No hay memoria disponible para la vista previa.',
                    'AP_START_FAILED':'No pude iniciar la red local de la cámara.',
                }.get(reason,'La cámara rechazó la operación: '+reason)
                raise ValueError(explanation)
            if message.get('event') == event:
                return message
        raise TimeoutError('Sin confirmación; resultado desconocido. No repito la orden.')
    if verb not in ('WIFI_ON', 'WIFI_OFF'):
        raise ValueError('Operación de mantenimiento desconocida.')
    if verb == 'WIFI_ON' and not re.fullmatch('[0-9a-fA-F]{16}',password or ''):
        raise ValueError('La clave local debe tener 16 caracteres hexadecimales.')
    info = send('INFO','info')
    validate_peer(info,expected)
    if verb not in info.get('commands',[]):
        raise ValueError('El firmware conectado no anuncia mantenimiento Wi-Fi; no envío la orden.')
    result = send(verb,'wifi_ready' if verb == 'WIFI_ON' else 'wifi_off')
    if result.get('boot') != info.get('boot'):
        raise ValueError('Cambió el arranque: resultado desconocido.')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',required=True)
    p.add_argument('--registry',required=True)
    p.add_argument('--camera',type=int,choices=[1,2],required=True)
    p.add_argument('--off',action='store_true')
    args=p.parse_args()
    expected=read_registry(args.registry)[f'camera{args.camera}']
    password=None if args.off else getpass.getpass('Clave Wi-Fi de mantenimiento (16 hex, no se guarda): ')
    result=activate(args.port,expected,not args.off,password)
    password=None
    if args.off:print('Wi-Fi desactivado según la cámara; el puerto quedó cerrado.')
    else:print('Red local: '+result['ssid']+'\nDirección: http://'+result['ip']+':81/stream\nConectá la PC a esa red con tu clave y abrí la vista previa. No se inició grabación.')


def activate(port_name,expected,enabled,password=None):
    import serial
    port=serial.Serial(port=None,baudrate=115200,timeout=.2,write_timeout=3)
    port.dtr=False;port.rts=False;port.port=port_name
    with port:
        return exchange(port,'WIFI_ON' if enabled else 'WIFI_OFF',expected,password)


if __name__=='__main__':main()
