"""ASTRA-39: verificación offline de una secuencia JPEG de banco.

Preparo la aceptación de grabación; el firmware instalado aún no genera
este formato. No abro puertos, no escribo en la SD y no declaro video probado.
"""
import argparse
import hashlib
import io
import json
import re
import zlib
from pathlib import Path
from PIL import Image

PROFILE='camera-sequence-0.1'
MAX_FRAMES=120
MAX_JPEG=512*1024


def integer(value, minimum, maximum):
    return type(value) is int and minimum<=value<=maximum


def verify(folder, expected_device=None):
    root=Path(folder).resolve(strict=True)
    manifest=root/'sequence.json'
    if manifest.is_symlink():raise ValueError('El manifiesto debe ser un archivo local de la secuencia')
    with manifest.open('rb') as h:raw=h.read(128*1024+1)
    if len(raw)>128*1024:raise ValueError('Manifiesto demasiado grande')
    obj=json.loads(raw)
    if not isinstance(obj,dict) or type(obj.get('v')) is not int or obj['v']!=1 or obj.get('profile')!=PROFILE:raise ValueError('Perfil incompatible')
    if obj.get('origin') not in ('pc-fixture','camera'):raise ValueError('Origen no declarado')
    if obj['origin']=='camera':
        if not isinstance(expected_device,str) or not re.fullmatch(r'[a-f0-9]{16}',expected_device):raise ValueError('Elegir la identidad de cámara esperada desde el registro privado')
        if obj.get('device')!=expected_device:raise ValueError('Cámara diferente de la esperada')
    if not isinstance(obj.get('boot'),str) or not re.fullmatch(r'[a-f0-9]{16}',obj['boot']):raise ValueError('Arranque inválido')
    frames=obj.get('frames')
    if not isinstance(frames,list) or not 0<=len(frames)<=MAX_FRAMES:raise ValueError('Cantidad de cuadros fuera de límite')
    if not integer(obj.get('expected_frames'),1,MAX_FRAMES):raise ValueError('Cantidad esperada inválida')
    if type(obj.get('closed')) is not bool:raise ValueError('Falta estado de cierre')
    errors=[]; checked=[]; names=set(); previous=None; hashes={}
    for index, frame in enumerate(frames,1):
        try:
            if not isinstance(frame,dict):raise ValueError('Metadato de cuadro inválido')
            name=frame.get('file','')
            if not isinstance(name,str) or not re.fullmatch(r'frame_[0-9]{4}\.jpg',name):raise ValueError('Nombre de cuadro inválido')
            if name in names:raise ValueError('Archivo repetido')
            names.add(name)
            if type(frame.get('index')) is not int or frame['index']!=index:raise ValueError('Índice no consecutivo')
            if frame.get('boot')!=obj['boot']:raise ValueError('Arranque diferente en el cuadro')
            stamp=frame.get('capture_us')
            if not integer(stamp,0,2**63-1) or (previous is not None and stamp<=previous):raise ValueError('Tiempo no creciente')
            previous=stamp
            if not integer(frame.get('bytes'),4,MAX_JPEG):raise ValueError('Longitud fuera de límite')
            path=root/name
            if path.is_symlink() or path.resolve().parent!=root:raise ValueError('Ruta fuera de la secuencia')
            if path.stat().st_size!=frame['bytes']:raise ValueError('Longitud diferente')
            with path.open('rb') as h:data=h.read(MAX_JPEG+1)
            if len(data)!=frame['bytes']:raise ValueError('Archivo cambió durante la lectura')
            hashes[name]=hashlib.sha256(data).hexdigest()
            crc=f'{zlib.crc32(data)&0xffffffff:08x}'
            if frame.get('crc32')!=crc:raise ValueError('CRC diferente')
            with Image.open(io.BytesIO(data)) as picture:
                if picture.format!='JPEG' or picture.size!=(640,480) or picture.mode!='RGB':raise ValueError('Formato, dimensiones o color incompatibles')
                picture.load()
            checked.append(dict(index=index,file=name,capture_us=stamp,bytes=len(data),sha256=hashes[name]))
        except (OSError,ValueError,TypeError,Image.DecompressionBombError) as exc:
            errors.append(dict(index=index,reason=str(exc)))
    if len(frames)!=obj['expected_frames']:errors.append(dict(reason='Cantidad declarada diferente de la esperada'))
    if not obj['closed']:errors.append(dict(reason='Secuencia sin cierre confirmado'))
    def bounded_hash(path):
        if path.is_symlink():return None
        try:
            with path.open('rb') as h:data=h.read(MAX_JPEG+1)
        except OSError:return None
        return hashlib.sha256(data).hexdigest() if len(data)<=MAX_JPEG else None
    with manifest.open('rb') as h:manifest_same=h.read(128*1024+1)==raw
    unchanged=(manifest_same and all(bounded_hash(root/name)==sha for name,sha in hashes.items())) if len(hashes)==len(frames) else None
    if unchanged is False:errors.append(dict(reason='Los archivos cambiaron durante la lectura'))
    elapsed=(checked[-1]['capture_us']-checked[0]['capture_us'])/1e6 if len(checked)>1 else None
    intervals=[(b['capture_us']-a['capture_us'])/1e6 for a,b in zip(checked,checked[1:])]
    return dict(profile=PROFILE,origin=obj['origin'],complete=not errors,expected_frames=obj['expected_frames'],
                checked_frames=len(checked),errors=errors,frames=checked,originals_unchanged=unchanged,
                fingerprinted_files=len(hashes),declared_files=len(frames),
                first_to_last_seconds=elapsed,intervals_seconds=intervals,
                mean_interval_fps=(len(checked)-1)/elapsed if elapsed and not errors else None,
                note='Cadencia entre marcas declaradas desde arranque; no mide exposición, reloj UTC, continuidad física, audio ni energía. pc-fixture es simulación.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder',type=Path)
    p.add_argument('--expect-device')
    args=p.parse_args()
    try:
        result=verify(args.folder,args.expect_device)
        print(json.dumps(result,ensure_ascii=True,indent=2))
        return 0 if result['complete'] else 1
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps(dict(complete=False,error=str(exc)),ensure_ascii=True));return 2

if __name__=='__main__':raise SystemExit(main())
