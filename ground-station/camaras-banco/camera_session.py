"""ASTRA-39: rondas de chequeo local con identidades y evidencias separadas."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import secrets
import subprocess
import sys
import zlib
from camera_check import MAX_FRAME, ProtocolError, check_result, validate_peer


def read_registry(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    cameras = data.get('cameras')
    if data.get('version') != 1 or not isinstance(cameras, dict) or set(cameras) != {'camera1', 'camera2'}:
        raise ValueError('Necesito las dos identidades registradas de cámara 1 y cámara 2.')
    if any(not isinstance(value, str) or not re.fullmatch(r'[0-9a-fA-F]{16}', value) for value in cameras.values()):
        raise ValueError('Las identidades de las cámaras no son válidas.')
    cameras = {key: value.lower() for key, value in cameras.items()}
    if len(set(cameras.values())) != 2:
        raise ValueError('Las dos cámaras deben tener identidades distintas.')
    return cameras


def read_evidence(folder, expected_device):
    folder = Path(folder)
    if (folder / 'resultado.json').stat().st_size > 64 * 1024:
        raise ProtocolError('El resultado supera el límite permitido.')
    result = json.loads((folder / 'resultado.json').read_text(encoding='utf-8'))
    if not isinstance(result.get('info'), dict) or not isinstance(result.get('frame'), dict):
        raise ProtocolError(result.get('error') or 'No llegó una foto completa; conservo el resultado del intento.')
    validate_peer(result['info'], expected_device)
    frame = result['frame']
    if frame.get('id') != result.get('request_id'):
        raise ProtocolError('La foto no corresponde al pedido registrado.')
    photo = folder / 'foto.jpg'
    if not 4 <= photo.stat().st_size <= MAX_FRAME:
        raise ProtocolError('El archivo de foto supera el límite permitido.')
    payload = photo.read_bytes()
    if len(payload) != frame.get('length') or f'{zlib.crc32(payload) & 0xffffffff:08x}' != frame.get('crc32'):
        raise ProtocolError('La foto conservada no coincide con su transferencia.')
    validation = check_result(result['info'], {**frame, 'payload': payload})
    if validation['sha256'] != result.get('validation', {}).get('sha256'):
        raise ProtocolError('La huella de la foto no coincide con su resultado.')
    stamp = datetime.fromisoformat(result['finished_utc'])
    if stamp.tzinfo is None:
        raise ProtocolError('El resultado no tiene zona horaria.')
    return {'photo': str(photo.resolve()), 'finished_utc': stamp.isoformat(),
            'sd_ok': validation['sd_readback_verified_by_device'],
            'sd_requested': result.get('sd_requested') is True,
            'error': result.get('error', ''), 'folder': str(folder.resolve()),
            'photo_sha256': validation['sha256']}


def capture(camera, device, port, output, save_sd, reset=False, runner=subprocess.run):
    """Una ejecución del receptor existente; sin reintentos ni selección de puerto."""
    if camera not in ('camera1', 'camera2') or not re.fullmatch(r'COM[1-9][0-9]*', port):
        raise ValueError('Seleccioná una cámara y un puerto COM explícito.')
    if not re.fullmatch(r'[0-9a-fA-F]{16}', device):
        raise ValueError('Identidad de cámara inválida.')
    attempt = Path(output).resolve() / ('chequeo_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ') + '_' + secrets.token_hex(4))
    attempt.mkdir(parents=True, exist_ok=False)
    args = [sys.executable, str(Path(__file__).with_name('camera_check.py')),
            '--port', port, '--label', camera, '--expect-device', device, '--output', str(attempt)]
    if save_sd:
        args.append('--save-sd')
    if reset:
        args.append('--reset-once')
    # No termino un proceso por timeout mientras puede estar cerrando un archivo SD.
    # El receptor aplica sus propios límites de espera y siempre conserva su resultado.
    with (attempt / 'salida.txt').open('xb') as stdout, (attempt / 'diagnostico.txt').open('xb') as stderr:
        completed = runner(args, stdout=stdout, stderr=stderr,
                           creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    results = list(attempt.glob('*/resultado.json'))
    if len(results) != 1:
        raise ProtocolError('No llegó un resultado único. Conservo el diagnóstico en ' + str(attempt))
    evidence = read_evidence(results[0].parent, device)
    evidence['operation_ok'] = completed.returncode == 0 and (not save_sd or evidence['sd_ok'])
    if not evidence['operation_ok'] and not evidence['error']:
        evidence['error'] = 'La operación terminó sin confirmación completa.'
    return evidence


@dataclass
class Round:
    number: int = 1
    results: dict = field(default_factory=dict)
    photos: dict = field(default_factory=dict)
    busy: str | None = None

    def start(self, camera):
        if camera not in ('camera1', 'camera2'):
            raise ValueError('Cámara desconocida.')
        if self.busy:
            raise ValueError('Hay una comprobación en curso; espero su resultado.')
        self.busy = camera
        self.results.pop(camera, None)

    def finish(self, camera, result):
        if self.busy != camera:
            raise ValueError('El resultado no corresponde a la comprobación en curso.')
        self.results[camera] = result
        if result.get('photo'):
            self.photos[camera] = result
        self.busy = None

    def new(self):
        if self.busy:
            raise ValueError('Espero a que termine la comprobación.')
        self.number += 1
        self.results.clear()

    def summary(self):
        checked = sum(bool(r.get('operation_ok') and r.get('sd_ok')) for r in self.results.values())
        if self.busy:
            return 'Comprobación en curso. No desconectes la cámara ni retires la tarjeta.'
        return f'{checked} de 2 cámaras con foto y SD comprobadas en esta ronda · por turnos'
