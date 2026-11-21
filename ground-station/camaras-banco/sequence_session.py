"""ASTRA-39: una solicitud CLIP explícita, sin reset ni reintento."""
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import secrets
import subprocess
import sys


def record(camera,device,port,output,runner=subprocess.run):
    if camera not in ('camera1','camera2') or not re.fullmatch(r'COM[1-9][0-9]*',port):raise ValueError('Cámara y puerto explícitos requeridos')
    if not re.fullmatch(r'[a-f0-9]{16}',device):raise ValueError('Identidad no válida')
    attempt=Path(output)/('secuencia_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')+'_'+secrets.token_hex(4))
    attempt.mkdir(parents=True,exist_ok=False)
    args=[sys.executable,str(Path(__file__).with_name('sequence_request.py')),'--port',port,'--expect-device',device,'--output',str(attempt)]
    with (attempt/'salida.txt').open('xb') as stdout,(attempt/'diagnostico.txt').open('xb') as stderr:
        done=runner(args,stdout=stdout,stderr=stderr,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    results=list(attempt.glob('*/request-result.json'))
    if len(results)!=1:raise ValueError('Sin resultado único de grabación; conservo el diagnóstico en '+str(attempt))
    result=json.loads(results[0].read_text(encoding='utf-8'))
    if not isinstance(result,dict):raise ValueError('Resultado de grabación inválido')
    response=result.get('response') or {}
    if result.get('state')=='reported_closed':
        if not isinstance(response,dict) or response.get('device')!=device or response.get('closed') is not True or response.get('frames')!=12 or response.get('expected_frames')!=12 or response.get('reason')!='COMPLETE':raise ValueError('Cierre de secuencia contradictorio')
        boot=response.get('boot','');ident=response.get('id','')
        if not re.fullmatch(r'[a-f0-9]{16}',boot) or not re.fullmatch(r'[a-f0-9]{16}',ident) or response.get('path')!=f'/ASTRA_SEQ_{boot}_{ident}':raise ValueError('Identidad o carpeta de secuencia incompatible')
    return dict(camera=camera,reported_closed=done.returncode==0 and result.get('state')=='reported_closed',
                state=result.get('state'),frames=response.get('frames'),path=response.get('path'),
                error=result.get('error') or response.get('reason',''),folder=str(results[0].parent),
                independent_readback_verified=False,finished_utc=datetime.now(timezone.utc).isoformat())
