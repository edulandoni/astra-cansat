"""Ensayo recepción y registro con sustitutos de software; no conecto hardware."""
import argparse
import csv
import hashlib
import json
import shutil
import sys
import tempfile
import time
import types
from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch

BANK=Path(__file__).resolve().parents[2]/'banco-usb-v0.1'
sys.path.insert(0,str(BANK))
from simulator import sample
from storage import Recorder
from acquisition import Acquisition

def csv_counts(path):
    with path.open(encoding='utf-8',newline='') as f:
        return [int(row['PACKET_COUNT']) for row in csv.DictReader(f)]

def events(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]

def load_frame(t):
    # Reutilizo valores de práctica: esto es carga de datos, no trayectoria física.
    fields=sample(t%131).decode('ascii').rstrip('\r').split(',')
    fields[2]=str(t+1)
    seconds=13*3600+t
    fields[1]=f'{seconds//3600:02}:{seconds//60%60:02}:{seconds%60:02}'
    return (','.join(fields)+'\r').encode('ascii')

class TransientWriter:
    def __init__(self,writer): self.writer=writer;self.calls=0
    def writerow(self,row):
        current=self.calls;self.calls+=1
        if 10<=current<20: raise OSError('FALLO_SINTETICO_CSV_PRINCIPAL')
        self.writer.writerow(row)

class NoDelayStop:
    def __init__(self): self.flag=False;self.waits=[]
    def is_set(self): return self.flag
    def set(self): self.flag=True
    def wait(self,seconds): self.waits.append(seconds);return self.flag

class VirtualSerialError(Exception): pass

class VirtualLink:
    def __init__(self,steps,stop): self.steps=iter(steps);self.stop=stop
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def read(self,maximum):
        try: item=next(self.steps)
        except StopIteration: self.stop.set();return b''
        if isinstance(item,Exception):raise item
        assert len(item)<=maximum
        return item

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida',type=Path,required=True)
    args=parser.parse_args()
    if args.salida.exists():parser.error('Elegir una salida nueva: conservo las anteriores.')
    args.salida.mkdir(parents=True,exist_ok=False)
    results=[]

    with tempfile.TemporaryDirectory() as tmp:
        r=Recorder(Path(tmp)/'primary','1000');a=Acquisition(r)
        started=time.perf_counter()
        try:
            for t in range(7200):a.ingest(load_frame(t))
            counts={'received':a.counter.received,'unique':a.counter.unique,
                    'invalid':a.invalid,'presentation_queue':a.updates.qsize(),
                    'latest_count':a.latest.count}
            elapsed=time.perf_counter()-started
        finally:r.close()
        stored=csv_counts(r.paths[0]);raw=events(r.directory/'reception.jsonl')
        assert stored==list(range(1,7201))
        assert counts['received']==7200 and counts['presentation_queue']==250
        assert len(raw)==7200
        results.append({'case':'7200_paquetes_sin_consumidor_de_pantalla',**counts,
                        'csv_rows':len(stored),'raw_events':len(raw),
                        'elapsed_seconds':elapsed,
                        'csv_sha256':hashlib.sha256(r.paths[0].read_bytes()).hexdigest(),
                        'observation':'Conservo los 7200 registros en CSV y raw aunque solo quedan 250 actualizaciones en la cola de presentación. No ejecuto la GUI ni dos horas de operación real.'})

    with tempfile.TemporaryDirectory() as tmp:
        r=Recorder(Path(tmp)/'primary','1000',Path(tmp)/'backup');a=Acquisition(r)
        r.writers[0]=TransientWriter(r.writers[0])
        try:
            for t in range(31):a.ingest(sample(t))
            error=r.error
        finally:r.close()
        primary=csv_counts(r.paths[0]);backup=csv_counts(r.paths[1]);raw=events(r.directory/'reception.jsonl')
        missing=sorted(set(backup)-set(primary))
        assert primary==list(range(1,11))+list(range(21,32))
        assert backup==list(range(1,32)) and len(raw)==31
        target=args.salida/'fallo_csv';target.mkdir()
        shutil.copyfile(r.paths[0],target/'principal.csv')
        shutil.copyfile(r.paths[1],target/'respaldo.csv')
        shutil.copyfile(r.directory/'reception.jsonl',target/'reception.jsonl')
        results.append({'case':'csv_principal_falla_diez_escrituras_y_vuelve',
                        'received':a.counter.received,'primary_csv_rows':len(primary),
                        'backup_csv_rows':len(backup),'raw_events':len(raw),
                        'missing_primary_counts':missing,'error_reported':error,
                        'observation':'El CSV de respaldo y raw conservan los 31 mensajes. El principal recupera escritura pero no rellena los diez faltantes. Son dos carpetas del mismo disco, no soportes independientes.'})

    with tempfile.TemporaryDirectory() as tmp:
        r=Recorder(Path(tmp)/'primary','1000');a=Acquisition(r,port='PUERTO_FICTICIO')
        a.stop=NoDelayStop()
        partial=sample(0)[:20]
        plans=[VirtualSerialError('APERTURA_SINTETICA_FALLIDA'),
               [partial,VirtualSerialError('DESCONEXION_SINTETICA')],
               [sample(1)[:7],sample(1)[7:]+sample(2)]]
        opened=[]
        def factory(port,baud,timeout):
            opened.append({'port':port,'baud':baud,'timeout':timeout})
            plan=plans.pop(0)
            if isinstance(plan,Exception):raise plan
            return VirtualLink(plan,a.stop)
        fake_serial=types.ModuleType('serial')
        fake_serial.Serial=factory;fake_serial.SerialException=VirtualSerialError
        with patch.dict(sys.modules,{'serial':fake_serial}):a.run()
        stored=csv_counts(r.paths[0]);raw=events(r.directory/'reception.jsonl')
        disconnected=sum(e.get('kind')=='disconnect' for e in raw)
        assert stored==[2,3] and a.invalid==0
        assert len(opened)==3 and disconnected==2 and a.stop.waits==[2,2]
        target=args.salida/'conexion_virtual';target.mkdir()
        shutil.copyfile(r.paths[0],target/'recibidos.csv')
        shutil.copyfile(r.directory/'reception.jsonl',target/'reception.jsonl')
        results.append({'case':'apertura_fallida_corte_y_reconexion_virtual',
                        'open_attempts':len(opened),'disconnect_events':disconnected,
                        'retry_delays_requested_seconds':a.stop.waits,
                        'csv_packet_counts':stored,'invalid':a.invalid,
                        'files_closed':r.raw.closed,
                        'observation':'Ejecuto el bucle serie real con un sustituto que entrega bytes/excepciones. Descarta el fragmento anterior al corte y recibe los dos paquetes completos de la nueva conexión. Las esperas de 2 s se registran sin realizarlas; no prueba controlador USB, COM real ni temporización física.'})

    report={'captured_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'Experimentos de integración de software, sin GUI ejecutada, hardware, RF ni cortes físicos.',
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                             [BANK/'acquisition.py',BANK/'storage.py',BANK/'protocol.py',BANK/'simulator.py']},
            'cases':results,'checks':'Todas las comprobaciones de conteos y contenido especificadas en el experimento se cumplieron.'}
    with (args.salida/'resultados.json').open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    manifest={str(p.relative_to(args.salida)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in args.salida.rglob('*') if p.is_file()}
    with (args.salida/'manifest.json').open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
