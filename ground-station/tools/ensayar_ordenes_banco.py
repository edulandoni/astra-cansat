"""ASTRA-20/24: prueba USB de guardas; sólo perfil sintético, sin cargar firmware o activar RF."""
import argparse
import hashlib
import json
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

CORE=Path(__file__).resolve().parents[1]/'banco-usb-v0.2'
sys.path.insert(0,str(CORE))
from engine import Engine
from journal import Store
from sources import serial_loop
from campaign import wait_for
from quality import quality_flags


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error('Conservo capturas: elegir una salida nueva')
    args.output.mkdir(parents=True)
    store=Store(args.output);engine=Engine(store);cases=[];error=None
    thread=threading.Thread(target=lambda:serial_loop(engine,args.port),daemon=True);thread.start()
    def order(op,want='executed',reason=None,**arguments):
        ident=engine.command(op,**arguments)
        wait_for(engine,lambda:engine.commands[ident]['state'] in {'executed','rejected','unknown','timeout'},6)
        command=engine.commands[ident]
        passed=command['state']==want and (reason is None or command.get('result',{}).get('reason')==reason)
        cases.append(dict(op=op,args=arguments,id=ident,state=command['state'],reason=command.get('result',{}).get('reason'),passed=passed))
        if not passed:raise RuntimeError('Resultado inesperado: '+op)
        return ident
    try:
        wait_for(engine,lambda:bool(engine.peer),10)
        if not engine.peer.get('synthetic'):raise RuntimeError('El extremo no se identificó como banco sintético')
        order('STOP');order('CAL_ZERO');order('SET_TIME',utc_seconds=int(datetime.now(timezone.utc).timestamp())%86400)
        order('RUN',want='rejected',reason='BAD_ARGUMENT',scenario='INVALID',samples=131)
        order('RUN',want='rejected',reason='BAD_ARGUMENT',scenario='NOMINAL',samples=0)
        order('SET_TIME',want='rejected',reason='BAD_TIME',utc_seconds=86400)
        before=engine.total_unique;epoch=engine.epoch
        with engine.lock:
            ident=engine.command('RUN',scenario='NOMINAL',samples=4)
            engine.commands[ident]['message']['team']='1001'  # Ficticio y ajeno; no es destino de vuelo.
        wait_for(engine,lambda:engine.commands[ident]['state'] in {'executed','rejected','unknown','timeout'},6)
        passed=engine.commands[ident]['state']=='timeout' and engine.total_unique==before and engine.epoch==epoch
        cases.append(dict(op='RUN_WRONG_TEAM',team='1001',state=engine.commands[ident]['state'],new_packets=engine.total_unique-before,passed=passed))
        if not passed:raise RuntimeError('La prueba de equipo ajeno no conservó el contexto esperado')
        order('POWER_STATUS')
        ident=order('RUN',scenario='NOMINAL',samples=131);run=engine.epoch
        wait_for(engine,lambda:engine.tracker.high is not None and engine.tracker.high>=5,12)
        before=engine.tracker.high;engine.repeat(ident)
        wait_for(engine,lambda:engine.commands[ident]['state']=='executed',6)
        passed=engine.epoch==run and engine.tracker.high>=before
        cases.append(dict(op='REPEAT_RUN',count_before=before,count_after=engine.tracker.high,same_run=engine.epoch==run,passed=passed))
        if not passed:raise RuntimeError('RUN repetido cambió la ejecución')
        wait_for(engine,lambda:engine.tracker.high>=12,20)
        order('CAL_ZERO',want='rejected',reason='NOT_LAUNCH_PAD')
        order('SET_TIME',want='rejected',reason='NOT_LAUNCH_PAD',utc_seconds=0)
        wait_for(engine,lambda:engine.finished is not None,140)
        snap=engine.snapshot();cases.append(dict(op='COMPLETE_MISSION',unique=snap['unique'],lost=snap['observed_gaps'],
                                               invalid=snap['invalid'],quality=quality_flags(snap),
                                               passed=snap['unique']==131 and snap['observed_gaps']==0 and snap['invalid']==0))
        order('STOP')
    except Exception as exc:
        error=str(exc)
    finally:
        engine.stop.set();thread.join(3);store.close()
    closed_clean=all(d['pending']==0 and d['dropped']==0 and not d['error'] for d in store.status())
    report=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),source='USB_BENCH',profile='bench-usb-0.2',
                cases=cases,error=error,passed=error is None and all(c['passed'] for c in cases) and closed_clean,storage_closed_clean=closed_clean,
                storage=[{k:v for k,v in d.items() if k!='root'} for d in store.status()],
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in CORE.glob('*.py')},
                limits='Sólo USB sintético. La ausencia de respuesta a equipo ajeno se observa en este banco; no prueba addressing RF, autenticación ni una actuación física. Sin reinicio, carga de firmware o transmisión de radio.')
    (args.output/'resultado.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2))
    raise SystemExit(0 if report['passed'] else 2)


if __name__=='__main__':main()
