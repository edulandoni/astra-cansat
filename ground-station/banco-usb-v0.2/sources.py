"""ASTRA-20/21: USB, emulador PC y reproducción; un dueño del puerto."""
import json
import queue
import time
import uuid
from pathlib import Path
from wire import PROFILE,control,SCENARIOS
from mission import sample

class PCBench:
    def __init__(self,engine):
        self.engine=engine;self.boot=uuid.uuid4().hex[:16];self.run='idle';self.active=False
        self.tick=0;self.samples=131;self.scenario='NOMINAL';self.base=46800;self.offset=12.
        self.high=0;self.memo={};self.client=None
    def send(self,**obj):self.engine.feed(control(dict(team=self.engine.team,boot=self.boot,run=self.run,**obj)))
    def hello(self):self.send(kind='hello',synthetic=True,scenario=self.scenario)
    def execute(self,obj):
        if obj['client']!=self.client:self.client=obj['client'];self.high=0;self.memo={}
        ident=obj['id'];seq=obj['seq']
        signature=json.dumps(obj,sort_keys=True)
        if ident in self.memo:
            old,msg=self.memo[ident]
            if old==signature:self.send(**msg)
            else:self.send(kind='result',id=ident,phase='rejected',reason='ID_CONFLICT')
            return
        if seq<=self.high:self.send(kind='result',id=ident,phase='rejected',reason='ID_EXPIRED');return
        self.high=seq;op=obj['op'];args=obj.get('args',{})
        if op=='RUN' and (args.get('scenario','NOMINAL') not in SCENARIOS or not 1<=args.get('samples',131)<=100000):
            self.send(kind='result',id=ident,phase='rejected',reason='BAD_ARGUMENT');return
        self.send(kind='result',id=ident,phase='accepted')
        msg=dict(kind='result',id=ident,phase='executed',synthetic=True,op=op)
        if op=='RUN':
            self.run=obj['client']+'_'+str(seq);self.active=True;self.tick=0
            self.scenario=args.get('scenario','NOMINAL');self.samples=int(args.get('samples',131));self.hello()
        elif op=='STOP':self.active=False
        elif op=='CAL_ZERO':
            if self.active and self.tick>=10:msg.update(phase='rejected',reason='NOT_LAUNCH_PAD')
            else:self.offset=0.;msg['altitude_zero']=0.
        elif op=='SET_TIME':
            if self.active and self.tick>=10:msg.update(phase='rejected',reason='NOT_LAUNCH_PAD')
            else:
                value=args.get('utc_seconds',-1)
                if not isinstance(value,int) or not 0<=value<86400:msg.update(phase='rejected',reason='BAD_TIME')
                else:self.base=value;msg['utc_seconds']=self.base
        elif op=='POWER_STATUS':msg.update(voltage=4.1,solar_voltage=2.5)
        else:msg.update(phase='rejected',reason='UNKNOWN_OPERATION')
        self.memo[ident]=(signature,msg)
        if len(self.memo)>64:del self.memo[next(iter(self.memo))]
        self.send(**msg)
    def run_loop(self,period=1):
        self.engine.connected();self.hello();next_tick=time.monotonic()+period
        while not self.engine.stop.is_set():
            try:
                obj=self.engine.outgoing.get(timeout=.02)
                if self.engine.can_send(obj):self.engine.sent(obj);self.execute(obj)
            except queue.Empty:pass
            if self.active and time.monotonic()>=next_tick:
                raw,outcome=sample(self.tick,self.scenario,self.engine.team,self.base,self.offset)
                self.send(kind='oracle',count=self.tick+1,outcome=outcome,scenario=self.scenario)
                if raw:self.engine.feed(raw)
                self.tick+=1;next_tick=time.monotonic()+period
                if self.tick>=self.samples:self.active=False;self.send(kind='done',samples=self.samples,scenario=self.scenario)
            if not self.active:next_tick=time.monotonic()+period
            self.engine.expire()

def serial_loop(engine,port,baud=115200,reset_once=False):
    import serial
    from serial.tools import list_ports
    reset_done=False;ever_connected=False
    while not engine.stop.is_set():
        try:
            candidate=port
            if ever_connected:
                ports=[p for p in list_ports.comports() if p.vid==0x10c4 and p.pid==0xea60]
                if len(ports)!=1:raise serial.SerialException('Puerto ausente o varios candidatos CP210x; no selecciono uno arbitrario')
                candidate=ports[0].device
            link=serial.Serial(port=None,baudrate=baud,timeout=.05,write_timeout=.5)
            link.port=candidate;link.dtr=False;link.rts=False;link.open()
            with link:
                engine.connected();ever_connected=True
                if reset_once and not reset_done:
                    link.rts=True;engine.stop.wait(.15);link.rts=False;reset_done=True
                    engine.event('bench_reset',method='RTS',power_cycle=False)
                while not engine.stop.is_set():
                    data=link.read(512)
                    if data:engine.feed(data)
                    try:obj=engine.outgoing.get_nowait()
                    except queue.Empty:obj=None
                    if obj and engine.can_send(obj):
                        raw=control(obj)
                        if link.write(raw)!=len(raw):raise serial.SerialException('Escritura parcial de orden')
                        engine.sent(obj)
                    engine.expire()
        except (serial.SerialException,OSError) as exc:
            engine.disconnected(str(exc));engine.stop.wait(1)

def replay_loop(engine,path,speed=1):
    if speed<=0:raise ValueError('Velocidad positiva requerida')
    engine.connected();previous=None;segment=None
    from datetime import datetime
    with Path(path).open(encoding='utf-8') as h:
        for line in h:
            if engine.stop.is_set():break
            e=json.loads(line);kind=e.get('kind')
            if kind not in {'wire','accepted','packet','segment'}:continue
            # Formato v0.2 se reproduce desde wire; v0.1 desde accepted.
            if kind=='segment':
                engine.context(e.get('boot','replay'),e.get('run',e.get('segment','legacy')),'Registro reproducido');continue
            if kind=='packet':continue
            stamp=e.get('received_elapsed_seconds')
            if stamp is None:stamp=datetime.fromisoformat(e['received_utc']).timestamp()
            if previous is not None:engine.stop.wait(max(0,stamp-previous)/speed)
            previous=stamp
            if kind=='wire':engine.feed(bytes.fromhex(e['raw_hex']))
            elif kind=='accepted':
                if engine.epoch is None:engine.context('replay','legacy','Captura v0.1 declarada')
                engine.feed(e['raw'].encode('ascii'))
    engine.status='Reproducción terminada'
