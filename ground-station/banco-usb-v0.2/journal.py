"""ASTRA-21: escritores independientes y acotados; nunca confundo RX con durable."""
import csv
import json
import os
import threading
import time
import uuid
from collections import deque
from datetime import datetime,timezone
from pathlib import Path
from wire import FIELDS

def utc():return datetime.now(timezone.utc).isoformat()

def intervals(values):
    out=[]
    for n in values:
        if out and n==out[-1][1]+1:out[-1][1]=n
        else:out.append([n,n])
    return out

class Writer:
    def __init__(self,root,kind,capacity=600,hook=None):
        self.root=Path(root);self.kind=kind;self.capacity=capacity;self.hook=hook
        self.queue=deque();self.lock=threading.Lock();self.wake=threading.Event();self.stop=threading.Event()
        self.saved=0;self.error='';self.dropped=0;self.drop_ranges=[];self.ledger_truncated=False
        self.last_seq=None;self.handles={};self.active=False;self.generation=0
        self.thread=threading.Thread(target=self.run,daemon=True);self.thread.start()
    def submit(self,event):
        with self.lock:
            if len(self.queue)>=self.capacity:
                self.dropped+=1;n=event['seq']
                if self.drop_ranges and self.drop_ranges[-1][1]+1==n:self.drop_ranges[-1][1]=n
                elif len(self.drop_ranges)<256:self.drop_ranges.append([n,n])
                else:self.ledger_truncated=True
                return False
            self.queue.append(event);self.wake.set();return True
    def write(self,e):
        if self.hook:self.hook(self.kind,e)
        suffix='' if self.generation==0 else '.recovery-'+str(self.generation)
        name='journal'+suffix+'.jsonl' if self.kind=='raw' else 'segments/'+e['segment']+'/Flight_'+e['team']+suffix+'.csv'
        if name not in self.handles:
            # Una sola salida activa por escritor: la cantidad de misiones no
            # puede acumular archivos abiertos indefinidamente.
            if self.kind=='csv':
                for handle,_ in self.handles.values():handle.close()
                self.handles.clear()
            path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True)
            exists=path.exists()
            h=path.open('a',encoding='utf-8',newline='');writer=csv.writer(h) if self.kind=='csv' else None
            self.handles[name]=(h,writer)
            if writer and not exists:writer.writerow(FIELDS)
        h,w=self.handles[name]
        if w:w.writerow(e['values'])
        else:h.write(json.dumps(e,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n')
        h.flush();os.fsync(h.fileno())
    def run(self):
        while not self.stop.is_set():
            with self.lock:e=self.queue[0] if self.queue else None
            if e is None:self.wake.wait(.1);self.wake.clear();continue
            try:
                self.active=True;self.write(e)
                with self.lock:
                    self.queue.popleft();self.saved+=1;self.last_seq=e['seq'];self.error=''
            except (OSError,ValueError) as exc:
                self.error=str(exc)
                # Una escritura parcial puede existir: conservo el original y
                # no la declaro confirmada. Al recuperar abro un archivo nuevo.
                for h,_ in self.handles.values():
                    try:h.close()
                    except OSError:pass
                self.handles.clear()
                self.generation+=1
                if not self.stop.wait(.25):continue
            finally:self.active=False
        for h,_ in self.handles.values():
            try:h.close()
            except OSError:pass
    def status(self):
        with self.lock:return dict(kind=self.kind,saved=self.saved,pending=len(self.queue),error=self.error,dropped=self.dropped,
                                  dropped_seq_ranges=list(self.drop_ranges),loss_ledger_truncated=self.ledger_truncated,
                                  last_confirmed_seq=self.last_seq,capacity=self.capacity)

class Store:
    def __init__(self,root,backup=None,capacity=600,hooks=None):
        self.started_monotonic=time.monotonic()
        self.session=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')+'_'+uuid.uuid4().hex[:12]
        if backup and Path(root).resolve()==Path(backup).resolve():raise ValueError('Los destinos deben ser diferentes')
        self.roots=[Path(root)/self.session]+([Path(backup)/self.session] if backup else [])
        self.writers=[]
        for i,p in enumerate(self.roots):
            for kind in ['raw','csv']:
                self.writers.append(Writer(p,kind,capacity,(hooks or {}).get((i,kind))))
        self.seq=0;self.lock=threading.Lock();self.closed=False
    def emit(self,kind,**data):
        with self.lock:
            self.seq+=1
            e=dict(seq=self.seq,pc_session=self.session,received_utc=utc(),received_elapsed_seconds=time.monotonic()-self.started_monotonic,kind=kind,**data)
            # Serializo antes de repartir: ningún consumidor modifica el evento.
            json.dumps(e,allow_nan=False)
            for w in self.writers:
                if w.kind=='raw' or kind=='packet':w.submit(e)
            return e
    def status(self):return [dict(destination=i//2,root=str(w.root),**w.status()) for i,w in enumerate(self.writers)]
    def drain(self,timeout=5):
        end=time.monotonic()+timeout
        while time.monotonic()<end:
            if all(w.status()['pending']==0 for w in self.writers):return True
            time.sleep(.02)
        return False
    def close(self,timeout=5):
        if self.closed:return
        self.drain(timeout)
        for w in self.writers:w.stop.set();w.wake.set()
        for w in self.writers:w.thread.join(2)
        report=dict(pc_session=self.session,closed_utc=utc(),events=self.seq,destinations=self.status(),
                    note='Confirmado significa flush+fsync completados; no certifica resistencia eléctrica. Una escritura cuyo resultado es incierto puede quedar parcial o duplicada y debe reconciliarse.')
        for root in self.roots:
            try:
                root.mkdir(parents=True,exist_ok=True)
                with (root/'storage-summary.json').open('x',encoding='utf-8') as h:json.dump(report,h,ensure_ascii=False,indent=2)
            except OSError:pass
        self.closed=True
