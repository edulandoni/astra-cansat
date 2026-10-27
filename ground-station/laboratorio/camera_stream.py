"""ASTRA-39/41: flujo JPEG de mantenimiento, acotado y con identidad obligatoria."""
import hashlib
import ipaddress
from urllib.parse import urlsplit


def stream_url(value):
    url = urlsplit(value.strip())
    try:
        ip = ipaddress.ip_address(url.hostname or '')
        port = url.port or 80
    except ValueError as exc:
        raise ValueError('Ingresá una dirección IP local válida.') from exc
    if (url.scheme != 'http' or ip.version != 4 or not ip.is_private
            or ip.is_multicast or ip.is_unspecified or url.username or url.password
            or url.query or url.fragment or url.path not in ('', '/', '/stream')):
        raise ValueError('Usá HTTP con la IP local de la cámara y la ruta /stream, sin credenciales ni parámetros.')
    return f'http://{ip}:{port}/stream'


class StreamParser:
    """Multipart propio: no acepta un JPEG viejo como otro cuadro nuevo."""
    MAX_FRAME = 512 * 1024
    MAX_HEADER = 4096

    def __init__(self, device, boundary=b'astra-frame'):
        if not device or not boundary or len(boundary) > 70:
            raise ValueError('Identidad y separador requeridos.')
        self.device = device.lower()
        self.boundary = b'--' + boundary + b'\r\n'
        self.buffer = bytearray()
        self.pending = None
        self.boot = None
        self.last = None
        self.duplicates = 0
        self.skipped = 0

    def feed(self, chunk):
        if len(chunk) > 65536:
            raise ValueError('Bloque de red excesivo.')
        self.buffer.extend(chunk)
        frames = []
        while True:
            if self.pending is None:
                if self.buffer.startswith(b'\r\n'):
                    del self.buffer[:2]
                end = self.buffer.find(b'\r\n\r\n')
                if end < 0:
                    if len(self.buffer) > self.MAX_HEADER:
                        raise ValueError('Cabecera de imagen excesiva.')
                    break
                if end > self.MAX_HEADER or not self.buffer.startswith(self.boundary):
                    raise ValueError('Separador o cabecera de imagen inválidos.')
                headers = {}
                for line in bytes(self.buffer[len(self.boundary):end]).split(b'\r\n'):
                    key, sep, value = line.partition(b':')
                    key = key.strip().lower()
                    if not sep or key in headers:
                        raise ValueError('Cabecera repetida o inválida.')
                    headers[key] = value.strip().decode('ascii')
                try:
                    meta = dict(length=int(headers[b'content-length']),
                                device=headers[b'x-device'].lower(),
                                boot=headers[b'x-boot'],
                                index=int(headers[b'x-frame-id']),
                                capture_us=int(headers[b'x-capture-us']))
                    valid_type = headers[b'content-type'] == 'image/jpeg'
                except (KeyError, ValueError) as exc:
                    raise ValueError('Faltan identidad o tiempos de la cámara.') from exc
                if (not valid_type or meta['device'] != self.device
                        or not 4 <= meta['length'] <= self.MAX_FRAME
                        or len(meta['boot']) != 16
                        or any(c not in '0123456789abcdef' for c in meta['boot'])
                        or meta['index'] < 1 or meta['capture_us'] < 0):
                    raise ValueError('Imagen ajena o metadatos fuera de límites.')
                if self.boot is not None and meta['boot'] != self.boot:
                    raise ValueError('La cámara reinició. Reconectá para comprobar el nuevo arranque.')
                self.pending = meta
                del self.buffer[:end + 4]
            length = self.pending['length']
            if len(self.buffer) < length + 2:
                break
            jpeg = bytes(self.buffer[:length])
            if self.buffer[length:length + 2] != b'\r\n' or not jpeg.startswith(b'\xff\xd8') or not jpeg.endswith(b'\xff\xd9'):
                raise ValueError('Imagen truncada o terminación inválida.')
            del self.buffer[:length + 2]
            meta, self.pending = self.pending, None
            digest = hashlib.sha256(jpeg).hexdigest()
            if self.last:
                index, stamp, previous = self.last
                if meta['index'] == index and meta['capture_us'] == stamp and digest == previous:
                    self.duplicates += 1
                    continue
                if meta['index'] <= index or meta['capture_us'] <= stamp:
                    raise ValueError('Contador repetido con conflicto o imagen fuera de orden.')
                self.skipped += meta['index'] - index - 1
            self.boot = meta['boot']
            self.last = meta['index'], meta['capture_us'], digest
            frames.append((meta, jpeg))
        return frames
