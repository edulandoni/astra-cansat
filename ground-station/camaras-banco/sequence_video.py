"""ASTRA-39: MP4 derivado, sin alterar JPEG ni sustituir tiempos de captura."""
from datetime import datetime,timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import secrets
from sequence_player import Archive


def export_video(folder,expected_device,output):
    import av
    archive=Archive(folder,expected_device)
    first=archive.frames[0]['capture_us'];timestamps=[f['capture_us']-first for f in archive.frames]
    destination=Path(output)/('video_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')+'_'+secrets.token_hex(4))
    destination.mkdir(parents=True,exist_ok=False);video=destination/'secuencia.mp4';result=dict(state='incomplete',source_origin=archive.report['origin'],audio=False)
    try:
        with video.open('xb') as target,av.open(target,'w',format='mp4') as container:
            stream=container.add_stream('libx264',rate=25)
            stream.width=640;stream.height=480;stream.pix_fmt='yuv420p'
            stream.time_base=Fraction(1,1000000);stream.codec_context.time_base=Fraction(1,1000000)
            stream.codec_context.max_b_frames=0;stream.options={'crf':'18','preset':'fast'}
            for i,stamp in enumerate(timestamps):
                frame=av.VideoFrame.from_image(archive.image(i).convert('RGB'))
                frame.pts=stamp;frame.time_base=Fraction(1,1000000)
                for packet in stream.encode(frame):container.mux(packet)
            for packet in stream.encode():container.mux(packet)
        decoded=[]
        with av.open(str(video)) as container:
            if len(container.streams.audio):raise ValueError('Exportación con audio no solicitado')
            for frame in container.decode(video=0):
                if (frame.width,frame.height)!=(640,480) or frame.pts is None:raise ValueError('Cuadro exportado inválido')
                decoded.append(round(frame.pts*frame.time_base*1000000))
            duration_us=container.duration
        if len(decoded)!=len(timestamps):raise ValueError('Cantidad de cuadros exportados diferente')
        error=max(abs(a-b) for a,b in zip(decoded,timestamps))
        if error>1000:raise ValueError('Tiempos exportados difieren más de 1 ms')
        unchanged=True
        for f in archive.frames:
            if hashlib.sha256((archive.root/f['file']).read_bytes()).hexdigest()!=f['sha256']:unchanged=False
        if not unchanged:raise ValueError('Una imagen original cambió durante la exportación')
        result.update(state='verified',frames=len(decoded),source_timestamps_us=timestamps,decoded_timestamps_us=decoded,
            max_timestamp_error_us=error,first_to_last_seconds=timestamps[-1]/1e6,container_duration_us=duration_us,
            originals_unchanged=True,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),video=str(video),pyav_version=av.__version__,
            note='MP4 H.264 derivado con recompresión; JPEG originales conservados. Sin interpolación ni audio. Tiempos relativos del emisor, no exposición exacta ni UTC. La duración final del último cuadro pertenece al contenedor; no se midió como captura.')
        return result
    except Exception as exc:
        result['error']=str(exc);raise
    finally:
        result['recorded_utc']=datetime.now(timezone.utc).isoformat()
        with (destination/'exportacion.json').open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
