"""ASTRA-39: lectura independiente de grabación segmentada, sin modificar originales."""
import hashlib
import json
from pathlib import Path
import re
from sequence_verify import verify as verify_segment


def read_object(path,limit=128*1024):
    if path.is_symlink():raise ValueError('Metadatos con enlace simbólico.')
    with path.open('rb') as f:data=f.read(limit+1)
    if len(data)>limit:raise ValueError('Metadatos fuera de límite.')
    obj=json.loads(data)
    if not isinstance(obj,dict):raise ValueError('Metadatos inválidos.')
    return obj,hashlib.sha256(data).hexdigest()


def verify_recording(folder,expected_device):
    if not re.fullmatch('[a-f0-9]{16}',expected_device or ''):raise ValueError('Elegí la identidad esperada desde el registro privado.')
    root=Path(folder).resolve(strict=True)
    start,start_hash=read_object(root/'session-start.json')
    end,end_hash=read_object(root/'session-result.json')
    for obj in (start,end):
        if obj.get('v')!=1 or obj.get('profile')!='camera-recording-0.1' or obj.get('origin')!='camera' or obj.get('device')!=expected_device:
            raise ValueError('Origen, perfil o cámara diferentes de los esperados.')
        for name in ('boot','run'):
            if not re.fullmatch('[a-f0-9]{16}',obj.get(name,'')):raise ValueError('Contexto de grabación inválido.')
    if (start['boot'],start['run'])!=(end['boot'],end['run']):raise ValueError('Los metadatos corresponden a contextos distintos.')
    if type(start.get('requested_seconds')) is not int or not 1<=start['requested_seconds']<=3600 or start.get('segment_limit')!=60:
        raise ValueError('Límites de la grabación inválidos.')
    for key in ('segments_closed','frames_captured','frames_written','bytes_written','started_us','finished_us'):
        if type(end.get(key)) is not int or end[key]<0:raise ValueError('Resumen con contadores inválidos.')
    if not 1<=end['segments_closed']<=600 or end['finished_us']<end['started_us'] or end['started_us']!=start.get('started_us'):
        raise ValueError('Cantidad de segmentos o tiempos inválidos.')
    errors=[];reports=[];all_frames=[];total_frames=total_bytes=0;previous=None;first=None;intervals=[]
    hashes={'session-start.json':start_hash,'session-result.json':end_hash}
    actual=sorted(p.name for p in root.iterdir() if p.name.startswith('segment_'))
    expected=[f'segment_{i:04}' for i in range(1,end['segments_closed']+1)]
    if actual!=expected:errors.append('Segmentos faltantes, adicionales o sin cierre.')
    for name in expected:
        directory=root/name
        if directory.is_symlink() or directory.resolve().parent!=root:raise ValueError('Segmento fuera de la grabación.')
        try:
            report=verify_segment(directory,expected_device)
            if not report['complete']:raise ValueError('Segmento incompleto: '+str(report['errors']))
            meta,manifest_hash=read_object(directory/'sequence.json')
            if meta.get('boot')!=start['boot']:raise ValueError('Cambió el arranque dentro de la grabación.')
            if not 1<=len(report['frames'])<=60:raise ValueError('Segmento fuera de límite.')
            hashes[name+'/sequence.json']=manifest_hash
            for frame,declared in zip(report['frames'],meta['frames']):
                if previous is not None:
                    if frame['capture_us']<=previous:raise ValueError('Tiempo no creciente entre segmentos.')
                    intervals.append((frame['capture_us']-previous)/1e6)
                if first is None:first=frame['capture_us']
                previous=frame['capture_us']
                if not start['started_us']<=frame['capture_us']<=end['finished_us']:raise ValueError('Cuadro fuera de la ventana declarada.')
                side_name=frame['file'].replace('.jpg','.json')
                side,side_hash=read_object(directory/side_name,4096)
                if any(side.get(k)!=declared.get(k) for k in ('index','boot','capture_us','bytes','crc32')):raise ValueError('Índice lateral en conflicto con el manifiesto.')
                hashes[name+'/'+side_name]=side_hash;hashes[name+'/'+frame['file']]=frame['sha256']
                total_frames+=1;total_bytes+=frame['bytes']
                all_frames.append(dict(frame,index=total_frames,file=name+'/'+frame['file']))
            reports.append(dict(segment=name,frames=report['checked_frames'],first_to_last_seconds=report['first_to_last_seconds']))
        except (ValueError,OSError,TypeError) as exc:errors.append(name+': '+str(exc))
    if end.get('closed') is not True or end.get('reason') not in ('STOP_REQUESTED','DURATION_LIMIT'):errors.append('La grabación no tiene cierre correcto.')
    if total_frames!=end['frames_written'] or total_bytes!=end['bytes_written'] or end['frames_captured']<end['frames_written']:errors.append('Totales de cuadros/bytes incompatibles con los archivos.')
    for name,expected_hash in hashes.items():
        p=root/name
        if p.is_symlink():errors.append('La ruta cambió durante la verificación: '+name);continue
        digest=hashlib.sha256()
        try:
            with p.open('rb') as f:
                for block in iter(lambda:f.read(65536),b''):digest.update(block)
            if digest.hexdigest()!=expected_hash:errors.append('El archivo cambió durante la verificación: '+name)
        except OSError:errors.append('No pude revalidar '+name)
    elapsed=(previous-first)/1e6 if first is not None and previous is not None else None
    return dict(complete=not errors,origin='camera',segments=reports,frames=all_frames,checked_frames=total_frames,bytes_checked=total_bytes,errors=errors,
                first_to_last_seconds=elapsed,mean_interval_fps=(total_frames-1)/elapsed if elapsed and not errors else None,
                maximum_interval_seconds=max(intervals) if intervals else None,
                originals_unchanged=not any('cambió' in e or 'revalidar' in e for e in errors),
                note='Tiempos declarados desde arranque. No demuestra exposición exacta, vuelo, batería o ausencia de huecos fuera de la ventana.')
