"""ASTRA-21/22/34: adquisición, sesiones, calidad y órdenes desacopladas de Tk."""
import hashlib
import math
import queue
import re
import threading
import time
import uuid
from collections import OrderedDict
from datetime import datetime,timezone
from wire import Demux, classify, control, PROFILE, OPERATIONS

class Tracker:
    def __init__(self):
        self.received=0;self.unique=0;self.duplicates=0;self.conflicts=0
        self.high=None;self.missing=[];self.cache=OrderedDict();self.uncertain=False
    @property
    def lost(self):return sum(b-a+1 for a,b in self.missing)
    def add(self,n,digest):
        self.received+=1
        if n in self.cache:
            if self.cache[n]!=digest:self.conflicts+=1;return 'conflict'
            self.duplicates+=1;return 'duplicate'
        if self.high is not None and n<=self.high:
            match=next(((a,b) for a,b in self.missing if a<=n<=b),None)
            if not match:return 'old_unverified'
            self.missing.remove(match);a,b=match
            if a<n:self.missing.append((a,n-1))
            if n<b:self.missing.append((n+1,b))
            self.missing.sort()
            result='late'
        else:
            if self.high is not None and n>self.high+1:
                if len(self.missing)<4096:self.missing.append((self.high+1,n-1))
                else:self.uncertain=True
            self.high=n;result='new'
        self.unique+=1;self.cache[n]=digest
        if len(self.cache)>4096:self.cache.popitem(last=False)
        return result

class Engine:
    def __init__(self,store,team='1000',profile=PROFILE,source='USB_BENCH',timeout=3):
        self.store=store;self.team=team;self.profile=profile;self.source=source;self.timeout=timeout
        self.stop=threading.Event();self.lock=threading.RLock();self.outgoing=queue.Queue(100)
        self.updates=queue.Queue(250);self.commands=OrderedDict();self.command_seq=0
        self.demux=Demux();self.status='Sin conexión';self.link_at=None;self.value_at=None
        self.epoch=None;self.segment='unidentified';self.tracker=Tracker();self.latest=None
        self.gps=None;self.gps_at=None;self.invalid=0;self.diagnostics=0;self.overflows=0
        self.total_valid=0;self.total_unique=0;self.total_conflicts=0;self.ambiguous=False
        self.clock_frozen=0;self.clock_warning=False;self.previous_clock=None
        self.oracle={};self.finished=None;self.peer={};self.power=None;self.segment_serial=0
        self.connection_serial=0;self.handshake=None
        self.frames_received=0;self.control_received=0
        self.waiting_identity=False
        self.boot_probe_at=None
    def event(self,kind,**data):
        return self.store.emit(kind,source=self.source,profile=self.profile,team=self.team,segment=self.segment,**data)
    def context(self,boot,run,reason='metadata',preserve_command=None):
        epoch=(str(boot),str(run))
        self.boot_probe_at=None
        if self.waiting_identity:self.status='Conectado';self.waiting_identity=False
        if epoch==self.epoch:
            self.ambiguous=False
            return
        old=self.epoch;self.epoch=epoch;self.segment_serial+=1
        self.segment=f'{self.segment_serial:04d}_'+uuid.uuid4().hex[:12]
        self.latest=None;self.value_at=None;self.gps=None;self.gps_at=None
        self.tracker=Tracker();self.ambiguous=False;self.previous_clock=None;self.clock_frozen=0;self.clock_warning=False
        self.finished=None;self.oracle={}
        if old and old[0]!=epoch[0]:
            self.power=None
            self.handshake=None
            for c in self.commands.values():
                if c['id']!=preserve_command and c['state'] in {'queued','sent','accepted'}:
                    c['state']='unknown';c['reason']='Cambió el arranque del emisor'
        self.event('segment',boot=epoch[0],run=epoch[1],reason=reason)
    def new_legacy_segment(self):
        with self.lock:self.context('operator',uuid.uuid4().hex,'Declaración explícita; no prueba de reinicio físico')
    def connected(self):
        with self.lock:
            self.demux=Demux();self.status='Conectado';self.connection_serial+=1;self.peer={}
            self.latest=None;self.value_at=None;self.event('connected',connection=self.connection_serial)
            if self.profile==PROFILE and self.source!='REPLAY':
                self.handshake=self.command('POWER_STATUS')
                self.commands[self.handshake]['handshake_connection']=self.connection_serial
    def disconnected(self,reason):
        with self.lock:
            self.demux=Demux();self.status='Desconectado: '+reason
            self.latest=None;self.value_at=None;self.ambiguous=True
            self.peer={};self.handshake=None
            self.boot_probe_at=None
            self.event('disconnected',reason=reason)
            for c in self.commands.values():
                if c['state'] in {'queued','sent','accepted'}:c['state']='unknown';c['reason']='Interrupción del transporte'
            while not self.outgoing.empty():
                try:self.outgoing.get_nowait()
                except queue.Empty:break
    def feed(self,data):
        with self.lock:
            self.event('wire',raw_hex=data.hex())
            for kind,raw in self.demux.feed(data):
                if kind=='overflow':self.overflows+=1;self.event('overflow');continue
                self.frames_received+=1
                try:category,value=classify(raw,self.team,self.profile==PROFILE)
                except (ValueError,UnicodeError,TypeError) as exc:
                    self.invalid+=1;self.event('rejected',raw_hex=raw.hex(),reason=str(exc));continue
                if category=='diagnostic':
                    self.diagnostics+=1;self.event('diagnostic',raw_hex=raw.hex())
                    # ROM de mi banco ESP32: un reset sin hello no conserva la
                    # identidad anterior. No invento un boot a partir del texto.
                    if self.profile==PROFILE and re.fullmatch(rb'\s*rst:0x[0-9a-fA-F]+[^\r\n]*,\s*boot:0x[0-9a-fA-F]+[^\r\n]*\r',raw):
                        previous=self.epoch;self.epoch=None;self.peer={};self.handshake=None
                        self.latest=None;self.value_at=None;self.gps=None;self.gps_at=None;self.power=None
                        self.finished=None;self.ambiguous=True;self.waiting_identity=True
                        self.boot_probe_at=time.monotonic()+.5 if self.source!='REPLAY' else None
                        self.status='Conectado — arranque detectado; esperando identidad del firmware'
                        for c in self.commands.values():
                            if c['state'] in {'queued','sent','accepted'}:c['state']='unknown';c['reason']='Arranque ROM sin identidad nueva confirmada'
                        self.event('boot_observed',previous_epoch=previous,confirmed_identity=False)
                    continue
                self.link_at=time.monotonic()
                if category=='control':self.control_received+=1;self.on_control(value);continue
                self.on_packet(value,raw)
    def on_control(self,obj):
        self.event('control',message=obj)
        if obj['kind'] in {'hello','oracle'}:
            self.context(obj['boot'],obj['run'])
        kind=obj['kind']
        if kind=='hello':self.peer=obj;return
        if kind=='oracle':
            outcome=obj.get('outcome');n=obj.get('count')
            if outcome in {'emitted','omitted','corrupted'} and isinstance(n,int):
                # Total exacto + últimas 256 posiciones; el diario conserva todo.
                self.oracle[outcome]=self.oracle.get(outcome,0)+1
            return
        if kind=='done':
            if self.epoch==(obj['boot'],obj['run']):self.finished=obj
            else:self.event('stale_control',message=obj)
            return
        if kind=='result':
            ident=obj.get('id');c=self.commands.get(ident)
            if not c:
                self.event('unmatched_result',message=obj);return
            phase=obj.get('phase')
            if phase not in {'accepted','rejected','executed'}:return
            if phase=='executed' and ident==self.handshake and c.get('handshake_connection')==self.connection_serial:
                self.context(obj['boot'],obj['run'],'Respuesta a sondeo nuevo de esta conexión',preserve_command=ident)
                self.peer=dict(obj,kind='hello');self.handshake=None
            if c['state'] in {'unknown','timeout'}:c['late']=True
            # Un accepted tardío no degrada un resultado terminal.
            if phase=='accepted' and c['state'] in {'executed','rejected'}:return
            c['state']=phase;c['result']=obj
            if c['op']=='POWER_STATUS' and phase=='executed' and self.epoch==(obj['boot'],obj['run']):
                self.power=dict(voltage=obj.get('voltage'),solar_voltage=obj.get('solar_voltage'),at=time.monotonic(),synthetic=True)
    def on_packet(self,packet,raw):
        if self.epoch is None:
            if self.profile==PROFILE:
                self.invalid+=1;self.event('unidentified_packet',raw_hex=raw.hex());return
            self.context('legacy',uuid.uuid4().hex,'Contexto inicial no acreditado por el emisor')
        digest=hashlib.sha256(','.join(packet.values).encode('ascii')).hexdigest()
        result=self.tracker.add(packet.count,digest);self.total_valid+=1
        self.event('validated',count=packet.count,classification=result,raw_hex=raw.hex())
        if result=='conflict':self.total_conflicts+=1;return
        if self.profile!=PROFILE and result=='old_unverified' and self.tracker.high and packet.count<self.tracker.high:
            self.ambiguous=True;self.latest=None;self.value_at=None
            self.event('ambiguous_counter',count=packet.count);return
        if result not in {'new','late'}:return
        self.total_unique+=1;self.event('packet',values=packet.values,count=packet.count)
        if result=='late' or self.ambiguous:return
        self.latest=packet;self.value_at=time.monotonic()
        same=self.previous_clock==packet.data['MISSION_TIME']
        self.clock_frozen=self.clock_frozen+1 if same else 0
        self.clock_warning=self.clock_frozen>=3
        self.previous_clock=packet.data['MISSION_TIME']
        if int(packet.data['GPS_SATS'])>0:
            if self.gps is None or self.gps.get('GPS_TIME')!=packet.data['GPS_TIME']:
                self.gps=packet.data;self.gps_at=self.value_at
        try:self.updates.put_nowait((self.segment,packet))
        except queue.Full:
            try:self.updates.get_nowait()
            except queue.Empty:pass
            self.updates.put_nowait((self.segment,packet))
    def command(self,op,**args):
        with self.lock:
            if self.source=='REPLAY' or self.profile!=PROFILE:raise ValueError('El origen/perfil no admite órdenes de banco')
            if op not in OPERATIONS:raise ValueError('Orden desconocida')
            if sum(c['state'] in {'queued','sent','accepted'} for c in self.commands.values())>=32:raise ValueError('Órdenes pendientes: límite alcanzado')
            self.command_seq+=1;ident=self.store.session+':'+str(self.command_seq)
            obj=dict(kind='command',team=self.team,id=ident,seq=self.command_seq,client=self.store.session,op=op,args=args)
            try:self.outgoing.put_nowait(obj)
            except queue.Full:raise ValueError('Cola de transmisión llena')
            self.commands[ident]=dict(id=ident,op=op,state='queued',args=args,message=obj,deadline=time.monotonic()+self.timeout,late=False)
            if len(self.commands)>256:
                for k,c in list(self.commands.items()):
                    if c['state'] not in {'queued','sent','accepted'}:del self.commands[k];break
            self.event('command_queued',message=obj);return ident
    def repeat(self,ident):
        with self.lock:
            c=self.commands[ident]
            if c['state'] in {'queued','sent','accepted'}:raise ValueError('La orden todavía está pendiente')
            if self.profile!=PROFILE or self.source=='REPLAY':raise ValueError('Sólo banco bidireccional')
            obj=c['message'];self.outgoing.put_nowait(obj)
            self.event('command_repeat_requested',previous_state=c['state'],message=obj)
            c['state']='queued';c['deadline']=time.monotonic()+self.timeout
    def sent(self,obj):
        with self.lock:
            c=self.commands.get(obj['id'])
            if c and c['state']=='queued':
                c['state']='sent';c['deadline']=time.monotonic()+self.timeout
                self.event('command_sent',message=obj)
    def can_send(self,obj):
        with self.lock:return self.commands.get(obj['id'],{}).get('state')=='queued'
    def expire(self):
        with self.lock:
            now=time.monotonic()
            # Un único sondeo nuevo tras el arranque; no repito órdenes previas
            # ni sondeo indefinidamente un bootloader que no ejecuta firmware.
            if self.waiting_identity and self.boot_probe_at is not None and now>=self.boot_probe_at:
                self.boot_probe_at=None
                try:
                    self.handshake=self.command('POWER_STATUS')
                    self.commands[self.handshake]['handshake_connection']=self.connection_serial
                except (ValueError,queue.Full) as exc:self.event('identity_probe_not_queued',reason=str(exc))
            for c in self.commands.values():
                if c['state'] in {'queued','sent','accepted'} and now>c['deadline']:
                    c['state']='timeout';self.event('command_timeout',id=c['id'])
    def snapshot(self):
        with self.lock:
            now=time.monotonic();t=self.tracker
            return dict(status=self.status,source=self.source,profile=self.profile,segment=self.segment,epoch=self.epoch,
                        latest=self.latest.data if self.latest else None,link_age=None if self.link_at is None else now-self.link_at,
                        data_age=None if self.value_at is None else now-self.value_at,gps=self.gps,
                        gps_age=None if self.gps_at is None else now-self.gps_at,power=self.power,ambiguous=self.ambiguous,
                        clock_warning=self.clock_warning,received=t.received,unique=t.unique,duplicates=t.duplicates,
                        conflicts=t.conflicts,observed_gaps=t.lost,gaps_uncertain=t.uncertain,
                        invalid=self.invalid,diagnostics=self.diagnostics,overflows=self.overflows,
                        total_valid=self.total_valid,total_unique=self.total_unique,total_conflicts=self.total_conflicts,
                        frames_received=self.frames_received,control_received=self.control_received,
                        oracle=dict(self.oracle),done=self.finished,commands=[dict(c) for c in list(self.commands.values())[-12:]],storage=self.store.status())

def display(data):
    if not data:return {}
    out=dict(data)
    for k in ['GYRO_R','GYRO_P','GYRO_Y']:out[k]=f'{math.radians(float(data[k])):.4f}'
    return out


def telemetry_view(snapshot):
    """ASTRA-22/34: una posición sin fix no se presenta como medición válida."""
    values=display(snapshot.get('latest'));retained=set()
    if values and values['GPS_SATS']=='0':
        for key in ['GPS_TIME','GPS_ALTITUDE','GPS_LATITUDE','GPS_LONGITUDE']:
            values[key]=(snapshot.get('gps') or {}).get(key)
            retained.add(key)
    return values,retained
