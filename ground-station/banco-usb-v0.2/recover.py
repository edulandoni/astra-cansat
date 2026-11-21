"""ASTRA-21: reconstrucción nueva por sesión/segmento, sin pisar originales."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from wire import FIELDS,parse

def records(path):
    if path.suffix.lower()=='.csv':
        # Sólo el árbol creado por Store acredita el contexto del CSV.
        # No invento sesión para un archivo aislado o renombrado.
        if path.parent.parent.name!='segments':
            yield 0,None,'CSV sin contexto: seleccionar el archivo en su árbol original';return
        with path.open(encoding='utf-8',newline='') as h:
            reader=csv.reader(h)
            if next(reader,None)!=list(FIELDS):
                yield 1,None,'Encabezado CSV incompatible';return
            for n,row in enumerate(reader,2):
                yield n,dict(kind='packet',pc_session=path.parent.parent.parent.name,segment=path.parent.name,team=row[0] if row else '',values=row),None
    else:
        with path.open('rb') as h:
            for n,line in enumerate(h,1):
                try:yield n,json.loads(line),None
                except (ValueError,UnicodeError):yield n,None,'Registro incompleto o inválido'

def recover(inputs,output):
    output=Path(output)
    if output.exists():raise ValueError('Elegir destino nuevo; conservo los originales')
    merged={};origins={};conflicts=[];errors=[];fingerprints={}
    for filename in inputs:
        path=Path(filename);fingerprints[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            for lineno,e,error in records(path):
                if error:errors.append(dict(file=str(path),line=lineno,reason=error));continue
                if not isinstance(e,dict):errors.append(dict(file=str(path),line=lineno,reason='Evento no es objeto'));continue
                if e.get('kind')=='validated' and e.get('classification')=='conflict':
                    # El receptor conserva el primer paquete y deja la segunda
                    # versión contradictoria en el diario, sin duplicar el CSV.
                    # Ignorar esa marca volvería falsamente limpia la recuperación.
                    conflicts.append(dict(key=[e.get(k) for k in ['pc_session','segment','team','count']],
                                          source=str(path),line=lineno,reason='Conflicto registrado durante adquisición'))
                    continue
                if e.get('kind')!='packet':continue
                try:
                    values=e['values'];packet=parse((','.join(values)+'\r').encode('ascii'),e['team'])
                    if len(values)!=22:raise ValueError('Columnas incorrectas')
                    if not all(isinstance(e[k],str) and re.fullmatch(r'[A-Za-z0-9_-]{1,80}',e[k]) for k in ['pc_session','segment']):raise ValueError('Identidad no apta para ruta')
                    key=(e['pc_session'],e['segment'],e['team'],packet.count)
                except (KeyError,ValueError,UnicodeError,TypeError):errors.append(dict(file=str(path),line=lineno,reason='Paquete inválido'));continue
                if key in merged and merged[key]!=values:conflicts.append(dict(key=key,source=str(path),line=lineno))
                else:merged[key]=values
                origins.setdefault(key,[]).append(dict(file=str(path),line=lineno,seq=e.get('seq')))
        except (OSError,UnicodeError,csv.Error) as exc:errors.append(dict(file=str(path),line=None,reason=str(exc)))
    output.mkdir(parents=True)
    report=dict(inputs_sha256=fingerprints,conflicts=conflicts,read_errors=errors,candidates=len(merged),written=False)
    # Un error de lectura también impide declarar reconstrucción limpia.
    if not conflicts and not errors:
        for scope in sorted({k[:3] for k in merged}):
            pc,segment,team=scope;dest=output/pc/segment;dest.mkdir(parents=True,exist_ok=True)
            with (dest/f'Flight_{team}.csv').open('x',encoding='utf-8',newline='') as h:
                w=csv.writer(h);w.writerow(FIELDS);w.writerows(merged[k] for k in sorted(merged) if k[:3]==scope)
        with (output/'provenance.jsonl').open('x',encoding='utf-8') as h:
            for key in sorted(origins):h.write(json.dumps(dict(key=key,sources=origins[key]),ensure_ascii=True)+'\n')
        report['written']=True
    report['originals_unchanged']=all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in fingerprints.items())
    with (output/'recovery-result.json').open('x',encoding='utf-8') as h:json.dump(report,h,ensure_ascii=False,indent=2)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',nargs='+',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();print(json.dumps(recover(a.input,a.output),ensure_ascii=True,indent=2))
