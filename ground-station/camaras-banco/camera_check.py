"""ASTRA-39: captura local explícita. No busco ni abro puertos automáticamente."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import secrets
import time
import zlib
from datetime import datetime, timezone

PROFILE = 'camera-usb-0.1'
MAX_FRAME = 512 * 1024

class ProtocolError(ValueError):
    pass

class Decoder:
    """Encuadre acotado: cabecera, bytes JPEG y cierre con identidad coincidente."""
    def __init__(self):
        self.buf = bytearray()
        self.header = None
        self.payload = None

    def feed(self, data):
        events = []
        # Proceso en bloques acotados incluso si el llamador entrega una ráfaga grande.
        for start in range(0, len(data), 1024):
            self.buf.extend(data[start:start+1024])
            while True:
                if self.header is not None and self.payload is None:
                    n = self.header['length']
                    if len(self.buf) < n:
                        break
                    self.payload = bytes(self.buf[:n]); del self.buf[:n]
                nl = self.buf.find(b'\n')
                if nl < 0:
                    if len(self.buf) > 1024:
                        raise ProtocolError('Cabecera o diagnóstico demasiado largo')
                    break
                if nl > 1024:
                    raise ProtocolError('Cabecera o diagnóstico demasiado largo')
                line = bytes(self.buf[:nl]).rstrip(b'\r'); del self.buf[:nl+1]
                if not line:
                    continue
                if not line.startswith(b'@CAM '):
                    if self.header is not None:
                        raise ProtocolError('Diagnóstico intercalado antes del cierre')
                    events.append({'event': 'diagnostic', 'hex': line.hex()})
                    continue
                try:
                    msg = json.loads(line[5:])
                except (ValueError, UnicodeError) as exc:
                    raise ProtocolError('Control ilegible') from exc
                if not isinstance(msg, dict) or type(msg.get('v')) is not int or msg['v'] != 1:
                    raise ProtocolError('Versión de control incompatible')
                if self.header is not None:
                    h = self.header
                    if msg.get('event') != 'end' or any(msg.get(k) != h.get(k) for k in ('id','boot')):
                        raise ProtocolError('Cierre de otra captura o reinicio durante foto')
                    if (zlib.crc32(self.payload) & 0xffffffff) != int(h['crc32'], 16):
                        raise ProtocolError('Foto dañada: CRC distinto')
                    events.append({**h, 'payload': self.payload})
                    self.header = self.payload = None
                elif msg.get('event') == 'frame':
                    n = msg.get('length')
                    if type(n) is not int or not 4 <= n <= MAX_FRAME:
                        raise ProtocolError('Tamaño de foto fuera del límite')
                    if not re.fullmatch(r'[0-9a-fA-F]{8}', str(msg.get('crc32',''))):
                        raise ProtocolError('CRC inválido')
                    if not all(re.fullmatch(r'[0-9a-fA-F]{16}', str(msg.get(k,''))) for k in ('id','boot')):
                        raise ProtocolError('Identidad de foto inválida')
                    self.header = msg
                elif msg.get('event') in ('info','error'):
                    events.append(msg)
                else:
                    raise ProtocolError('Evento inesperado')
        return events

    def finish(self):
        if self.header is not None or self.buf:
            raise ProtocolError('Transferencia incompleta')

def check_image(frame):
    from PIL import Image
    data = frame['payload']
    with Image.open(io.BytesIO(data)) as im:
        if im.format != 'JPEG':
            raise ProtocolError('El contenido no es JPEG')
        im.verify()
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        if im.size != (frame.get('width'), frame.get('height')):
            raise ProtocolError('Dimensiones distintas de la cabecera')
        if im.size != (640,480) or im.mode != 'RGB':
            raise ProtocolError('El banco espera JPEG VGA codificado en color')
        return {'width': im.width, 'height': im.height, 'mode': im.mode,
                'sha256': hashlib.sha256(data).hexdigest(), 'decoded': True}

def validate_peer(info, expected_device=None, require_ready=True):
    if info.get('profile') != PROFILE or (require_ready and info.get('camera_ready') is not True):
        raise ProtocolError('Cámara/perfil no preparado')
    if not re.fullmatch(r'[0-9a-fA-F]{16}', str(info.get('device',''))):
        raise ProtocolError('Identidad de unidad inválida')
    if expected_device and info['device'].lower() != expected_device.lower():
        raise ProtocolError('El puerto corresponde a otra cámara; no envío captura ni escritura SD')

def check_result(info, frame, require_sd=False):
    validate_peer(info)
    if frame.get('boot') != info.get('boot') or frame.get('device') != info.get('device'):
        raise ProtocolError('La cámara reinició después de identificarla')
    request_us, capture_us = frame.get('request_us'), frame.get('capture_us')
    if type(request_us) is not int or type(capture_us) is not int or not 0 <= request_us <= capture_us:
        raise ProtocolError('No se acredita captura posterior a la solicitud')
    image = check_image(frame)
    saved = frame.get('saved') is True and frame.get('sd_status') == 'READBACK_OK'
    if require_sd and not saved:
        raise ProtocolError('Foto recibida, pero guardado/lectura SD sin comprobar: '+str(frame.get('sd_status')))
    return {**image, 'sd_readback_verified_by_device': saved,
            'power_loss_survival_verified': False, 'continuous_video_verified': False}

def receive(port, raw_file, decoder, request_id, expected, budget=30):
    deadline = time.monotonic()+budget
    while time.monotonic() < deadline:
        data = port.read(1024)
        if not data:
            continue
        if raw_file.tell()+len(data) > 2*1024*1024:
            raise ProtocolError('Límite del registro de recepción alcanzado')
        raw_file.write(data); raw_file.flush()
        for msg in decoder.feed(data):
            if msg.get('event') == 'diagnostic':
                diagnostic = bytes.fromhex(msg['hex']).decode('ascii',errors='replace')
                if 'waiting for download' in diagnostic or 'DOWNLOAD_BOOT(' in diagnostic:
                    raise ProtocolError('La placa está en modo programación; no está ejecutando la cámara. Hace falta un arranque normal, sin BOOT/IO0 pulsado.')
            if msg.get('id') != request_id:
                continue
            if msg.get('event') == 'error':
                raise ProtocolError('La cámara informó: '+str(msg.get('reason')))
            if msg.get('event') == expected:
                return msg
    raise TimeoutError('Sin resultado completo en el tiempo de espera; no reenvío la orden')

def restart_before_capture(port, previous_file, sleep=time.sleep):
    """Reinicio RTS explícito; conservo los bytes previos en lugar de descartarlos."""
    pending = port.in_waiting
    if not 0 <= pending <= 4096:
        raise ProtocolError('Demasiados bytes previos al reinicio; no descarto el registro')
    prior = port.read(pending) if pending else b''
    previous_file.write(prior); previous_file.flush()
    if len(prior) != pending:
        raise ProtocolError('Lectura previa al reinicio incompleta')
    port.dtr = False
    port.rts = True
    sleep(.1)
    port.rts = False
    sleep(1.5)
    return len(prior)

def main():
    parser = argparse.ArgumentParser(description='Chequeo USB de una cámara; no es protocolo de vuelo.')
    parser.add_argument('--port', required=True)
    parser.add_argument('--label', required=True, help='Identificación física, por ejemplo camara-a')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--save-sd', action='store_true', help='Escribo un archivo nuevo; nunca formateo ni borro')
    parser.add_argument('--show', action='store_true')
    parser.add_argument('--reset-once', action='store_true', help='Reinicio RTS explícito antes de identificar; no corta alimentación ni carga firmware')
    parser.add_argument('--expect-device', help='Identidad física ya comprobada; rechazo otra unidad antes de pedir foto o guardar')
    parser.add_argument('--init-once', action='store_true', help='Reinicializo el sensor una vez antes del chequeo; sólo si el firmware anuncia INIT')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,32}', args.label):
        parser.error('Etiqueta: sólo letras, números, guion y guion bajo, hasta 32 caracteres')
    if args.expect_device and not re.fullmatch(r'[0-9a-fA-F]{16}',args.expect_device):
        parser.error('La identidad esperada debe tener 16 dígitos hexadecimales')
    import serial
    # Abro sin provocar un reset por DTR/RTS; la identidad se consulta explícitamente.
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')+'_'+secrets.token_hex(4)
    out = args.output/run_id
    out.mkdir(parents=True, exist_ok=False)
    result = {'started_utc': datetime.now(timezone.utc).isoformat(), 'label': args.label,
              'port': args.port, 'profile': PROFILE, 'sd_requested': args.save_sd,
              'reset_requested': args.reset_once,
              'initialization_requested': args.init_once,
              'receiver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'result': 'incomplete', 'photos_are_private_by_default': True}
    image_path = out/'foto.jpg'
    try:
        with (out/'received.bin').open('xb') as raw:
            port = serial.Serial(port=None, baudrate=115200, timeout=.2, write_timeout=3)
            port.dtr=False; port.rts=False; port.port=args.port
            with port:
                if args.reset_once:
                    with (out/'pre_reset.bin').open('xb') as prior:
                        result['pre_reset_bytes'] = restart_before_capture(port,prior)
                    result['reset_sequence_sent'] = True
                decoder = Decoder()
                request_id = secrets.token_hex(8)
                port.write(f'INFO {request_id}\n'.encode('ascii')); port.flush()
                info = receive(port, raw, decoder, request_id, 'info')
                result['info'] = info
                if args.init_once:
                    validate_peer(info,args.expect_device,require_ready=False)
                    if 'INIT' not in info.get('commands',[]):
                        raise ProtocolError('Este firmware no anuncia INIT; no envío una orden desconocida')
                    result['info_before_init'] = info
                    request_id = secrets.token_hex(8)
                    port.write(f'INIT {request_id}\n'.encode('ascii')); port.flush()
                    info = receive(port,raw,decoder,request_id,'info')
                    result['info'] = info
                validate_peer(info,args.expect_device)
                request_id = secrets.token_hex(8)
                command = 'SAVE' if args.save_sd else 'PHOTO'
                result['request_id'] = request_id
                port.write(f'{command} {request_id}\n'.encode('ascii')); port.flush()
                frame = receive(port, raw, decoder, request_id, 'frame')
                # Conservo la foto recibida aunque falle su decodificación o el chequeo SD.
                with image_path.open('xb') as f:
                    f.write(frame['payload'])
                result['frame'] = {k:v for k,v in frame.items() if k != 'payload'}
                result['validation'] = check_result(info, frame, False)
                if args.save_sd and not result['validation']['sd_readback_verified_by_device']:
                    result['result'] = 'photo_checked_sd_failed'
                    raise ProtocolError('Foto comprobada, pero guardado/lectura SD sin comprobar: '+str(frame.get('sd_status')))
                result['result'] = 'photo_and_sd_checked' if args.save_sd else 'photo_checked_sd_not_tested'
    except Exception as exc:
        result['error'] = str(exc)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        with (out/'resultado.json').open('x', encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        print('Archivos conservados en:',out)
    if args.show:
        import tkinter as tk
        from PIL import Image,ImageTk
        root=tk.Tk();root.title('ASTRA — Comprobación de cámara — '+args.label)
        tk.Label(root,text=args.label+' · Foto del chequeo '+result['finished_utc']).pack(padx=10,pady=8)
        photo=ImageTk.PhotoImage(Image.open(image_path))
        tk.Label(root,image=photo).pack()
        tk.Label(root,text='Foto guardada y leída en SD' if args.save_sd else 'Foto recibida por USB; SD sin comprobar').pack(pady=8)
        root.mainloop()

if __name__ == '__main__':
    main()
