"""ASTRA-20/21/24: campaña reproducible; cada resultado declara su origen."""
import argparse
import csv
import hashlib
import json
import threading
import sys
import time
from datetime import datetime,timezone
from pathlib import Path
from journal import Store
from engine import Engine
from mission import expected
from sources import PCBench,serial_loop
from wire import PROFILE,SCENARIOS

def wait_for(engine,predicate,timeout):
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        if predicate():return
        if engine.stop.wait(.05):break
    raise TimeoutError('No se cumplió la condición del ensayo dentro del tiempo previsto')

def order(engine,op,**args):
    ident=engine.command(op,**args)
    wait_for(engine,lambda:engine.commands[ident]['state'] in {'executed','rejected','unknown','timeout'},engine.timeout+2)
    if engine.commands[ident]['state']!='executed':raise RuntimeError(str(engine.commands[ident]))
    return ident

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port');p.add_argument('--output',type=Path,required=True);p.add_argument('--backup',type=Path)
    p.add_argument('--scenarios',nargs='+',choices=SCENARIOS,default=SCENARIOS)
    p.add_argument('--samples',type=int,default=131);p.add_argument('--period',type=float,default=1)
    p.add_argument('--reset-once',action='store_true');p.add_argument('--repeat-run',action='store_true')
    a=p.parse_args()
    if a.samples<1 or a.samples>100000 or a.period<=0:p.error('Cantidad/período inválidos')
    if a.port and a.period!=1:p.error('En USB real el período de firmware es 1 s')
    s=Store(a.output,a.backup);e=Engine(s,source='USB_BENCH' if a.port else 'PC_BENCH')
    code={str(p.relative_to(Path(__file__).parent)):hashlib.sha256(p.read_bytes()).hexdigest()
          for p in Path(__file__).parent.rglob('*') if p.is_file() and p.suffix in {'.py','.ino'} and 'runs' not in p.parts}
    e.event('environment',python=sys.version,source_sha256=code)
    source=(lambda:serial_loop(e,a.port,reset_once=a.reset_once)) if a.port else (lambda:PCBench(e).run_loop(a.period))
    def runner():
        try:source()
        except Exception as exc:e.status='ERROR: '+str(exc);e.event('source_error',reason=str(exc));e.stop.set()
    t=threading.Thread(target=runner,daemon=True);t.start()
    result=dict(started_utc=datetime.now(timezone.utc).isoformat(),source=e.source,profile=PROFILE,
                samples=a.samples,period=a.period,cases=[],error=None,source_sha256=code)
    try:
        wait_for(e,lambda:bool(e.peer),10)
        order(e,'CAL_ZERO')
        now=datetime.now(timezone.utc);order(e,'SET_TIME',utc_seconds=now.hour*3600+now.minute*60+now.second)
        order(e,'POWER_STATUS')
        for scenario in a.scenarios:
            invalid_before=e.invalid
            started=time.monotonic();ident=order(e,'RUN',scenario=scenario,samples=a.samples)
            if a.repeat_run:
                wait_for(e,lambda:e.tracker.received>=min(5,a.samples),15*a.period+2)
                before=e.tracker.high;e.repeat(ident)
                wait_for(e,lambda:e.commands[ident]['state']=='executed',5)
                e.event('repeat_run_check',count_before=before)
            wait_for(e,lambda:e.finished is not None,a.samples*a.period*1.15+20)
            snap=e.snapshot();truth=expected(scenario,a.samples)
            case=dict(scenario=scenario,segment=e.segment,elapsed_seconds=time.monotonic()-started,
                      unique=snap['unique'],received=snap['received'],rejected=snap['invalid']-invalid_before,
                      duplicates=snap['duplicates'],observed_gaps=snap['observed_gaps'],oracle=snap['oracle'],
                      expected={k:len(v) for k,v in truth.items()},last_state=snap['latest']['STATE'] if snap['latest'] else None)
            # invalid es acumulado de la campaña; comparo tramas por segmento del diario al cerrar.
            case['unique_matches']=case['unique']==len(truth['emitted'])
            case['oracle_matches']=case['oracle']=={k:len(v) for k,v in truth.items() if v}
            case['rejections_match']=case['rejected']==len(truth['corrupted'])
            case['gaps_match']=case['observed_gaps']==len(truth['omitted'])+len(truth['corrupted'])
            result['cases'].append(case);print(json.dumps(case,ensure_ascii=True),flush=True)
    except Exception as exc:
        result['error']=str(exc);print('ERROR: '+str(exc),flush=True)
    finally:
        e.stop.set();t.join(3);s.close()
    result['ended_utc']=datetime.now(timezone.utc).isoformat();result['storage']=s.status()
    result['all_cases_match']=not result['error'] and all(c['unique_matches'] and c['oracle_matches'] and c['rejections_match'] and c['gaps_match'] for c in result['cases']) and len(result['cases'])==len(a.scenarios)
    result['limits']='Datos sintéticos; USB físico sólo si source=USB_BENCH. Sin RF, autonomía o prueba eléctrica acreditadas. Rechazos se cuentan por segmento en el diario.'
    primary=s.roots[0]
    primary.mkdir(parents=True,exist_ok=True)
    with (primary/'campaign-result.json').open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
    print(json.dumps(dict(path=str(primary),result=result),ensure_ascii=True),flush=True)
    return 0 if result['all_cases_match'] else 1

if __name__=='__main__':raise SystemExit(main())
