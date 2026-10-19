"""Demuestro recuperación offline de copias de una misma sesión de laboratorio."""
import argparse
import csv
import hashlib
import json
import tempfile
from pathlib import Path

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        return reader.fieldnames,list(reader)

def reconcile(primary,backup):
    header,left=read(primary);other,right=read(backup)
    if header!=other or not header or not {'TEAM_ID','PACKET_COUNT'}<=set(header):
        raise ValueError('Esquemas incompatibles.')
    merged={};origins={};conflicts=[]
    for source,rows in [('principal',left),('respaldo',right)]:
        for row in rows:
            if None in row or any(value is None for value in row.values()):
                raise ValueError('Fila incompleta: no la trato como un registro recuperado.')
            if not row['PACKET_COUNT'].isdigit():raise ValueError('Contador inválido.')
            key=(row['TEAM_ID'],int(row['PACKET_COUNT']))
            if key in merged and row!=merged[key]:
                conflicts.append({'team':key[0],'packet_count':key[1],
                                  'fields':[h for h in header if row[h]!=merged[key][h]]})
            else:merged[key]=row
            origins.setdefault(key,set()).add(source)
    result={'primary_rows':len(left),'backup_rows':len(right),'unique_candidates':len(merged),
            'conflicts':conflicts,'recovered_from_backup':[
                {'team':k[0],'packet_count':k[1]} for k in sorted(origins)
                if origins[k]=={'respaldo'}]}
    return header,merged,origins,result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--principal',type=Path,required=True)
    p.add_argument('--respaldo',type=Path,required=True)
    p.add_argument('--salida',type=Path,required=True)
    p.add_argument('--misma-sesion-de-laboratorio',action='store_true')
    args=p.parse_args()
    if not args.misma_sesion_de_laboratorio:p.error('No mezclar vuelos o reinicios: necesito una sesión de laboratorio identificada.')
    if args.salida.exists():p.error('Elegir una salida nueva para preservar las anteriores.')
    sources={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in
             [('principal',args.principal),('respaldo',args.respaldo)]}
    header,merged,origins,result=reconcile(args.principal,args.respaldo)
    result['original_sha256']=sources
    result['scope']='Copias de una misma sesión del experimento; no resuelve identificación de sesión de vuelo ni autenticidad de datos.'

    # Control negativo: una copia contradictoria debe bloquear la reconstrucción.
    _,rows=read(args.respaldo)
    with tempfile.TemporaryDirectory() as tmp:
        altered=Path(tmp)/'contradictorio.csv'
        if rows:
            rows[0]=dict(rows[0]);rows[0]['ALTITUDE']='9999.0'
        with altered.open('x',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=header);writer.writeheader();writer.writerows(rows)
        *_,negative=reconcile(args.principal,altered)
        assert negative['conflicts'],'El control negativo debe encontrar la contradicción.'
        result['negative_control']=negative['conflicts']

    args.salida.mkdir(parents=True,exist_ok=False)
    if not result['conflicts']:
        with (args.salida/'recuperado.csv').open('x',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=header);writer.writeheader()
            writer.writerows(merged[key] for key in sorted(merged))
        with (args.salida/'procedencia.csv').open('x',encoding='utf-8',newline='') as f:
            writer=csv.writer(f);writer.writerow(['TEAM_ID','PACKET_COUNT','fuentes'])
            for key in sorted(origins):writer.writerow([*key,' + '.join(sorted(origins[key]))])
        result['candidate_written']=True
    else:result['candidate_written']=False
    for name,path in [('principal',args.principal),('respaldo',args.respaldo)]:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==sources[name]
    result['originals_unchanged']=True
    with (args.salida/'resultado.json').open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
