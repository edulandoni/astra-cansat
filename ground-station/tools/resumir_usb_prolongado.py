"""ASTRA-21/22/34: verifico una captura cerrada; no acelero ni invento duración."""
import argparse
import csv
import hashlib
import json
import math
import statistics
import sys
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'banco-usb-v0.1'))
from protocol import FIELDS

def summarize(root,output,expected,minimum_seconds=7200):
    root=Path(root);output=Path(output)
    if output.exists():raise ValueError('Elijo una salida nueva; no reemplazo resultados')
    summary_path=root/'storage-summary.json'
    if not summary_path.is_file():raise ValueError('La captura todavía no tiene cierre de almacenamiento')
    storage=json.loads(summary_path.read_text(encoding='utf-8'))
    groups=defaultdict(list);health=[];kinds=Counter();classifications=Counter();errors=[];events=0;environment=None
    journals=sorted(root.glob('journal*.jsonl'))
    if not journals:raise ValueError('No encontré diario bruto')
    scoped=defaultdict(Counter)
    for path in journals:
        with path.open(encoding='utf-8') as h:
            for line_number,line in enumerate(h,1):
                try:e=json.loads(line)
                except ValueError:errors.append(dict(file=path.name,line=line_number));continue
                if not isinstance(e,dict):errors.append(dict(file=path.name,line=line_number));continue
                events+=1;kinds[e.get('kind')]+=1;scoped[e.get('segment')][e.get('kind')]+=1
                if e.get('kind')=='packet':groups[e['segment']].append(e)
                elif e.get('kind')=='gui_health':health.append(e)
                elif e.get('kind')=='validated':classifications[(e.get('segment'),e.get('classification'))]+=1
                elif e.get('kind')=='environment':environment=e
    if not groups:raise ValueError('No hay telemetría para evaluar')
    segment,packets=max(groups.items(),key=lambda item:len(item[1]))
    stamps=[e.get('received_elapsed_seconds') for e in packets]
    monotonic_valid=all(isinstance(v,(float,int)) and math.isfinite(v) for v in stamps)
    duration=stamps[-1]-stamps[0] if monotonic_valid else None
    intervals=[b-a for a,b in zip(stamps,stamps[1:])] if monotonic_valid else []
    utc=[datetime.fromisoformat(e['received_utc']).timestamp() for e in packets]
    during=[e for e in health if packets[0]['seq']<=e['seq']<=packets[-1]['seq']]
    callback_gaps=[b['elapsed']-a['elapsed'] for a,b in zip(during,during[1:])]
    memory=[e['working_set_bytes'] for e in during if isinstance(e.get('working_set_bytes'),int)]
    csv_files=list((root/'segments'/segment).glob('Flight_*.csv'))
    rows=[];header=[]
    if len(csv_files)==1:
        with csv_files[0].open(encoding='utf-8',newline='') as h:
            reader=csv.reader(h);header=next(reader,[]);rows=list(reader)
    source_sha={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
    destinations=[{k:v for k,v in d.items() if k!='root'} for d in storage['destinations']]
    queue_bounded=all(e.get('history_size',0)<=300 and e.get('update_queue',0)<=250 and all(d['pending']<=d['capacity'] for d in e['storage']) for e in during)
    active_errors={key:scoped[segment][key] for key in ['rejected','overflow','source_error','disconnected']}
    clocks=[]
    for e in packets:
        hour,minute,second=map(int,e['values'][1].split(':'));clocks.append(hour*3600+minute*60+second)
    clock_steps=Counter((b-a)%86400 for a,b in zip(clocks,clocks[1:]))
    checks=dict(source_usb=all(e.get('source')=='USB_BENCH' for e in packets),
                monotonic_timestamps=monotonic_valid,
                at_least_required_real_seconds=duration is not None and duration>=minimum_seconds,
                expected_counter_sequence=[e.get('count') for e in packets]==list(range(1,expected+1)),
                csv_equals_packets=len(csv_files)==1 and header==list(FIELDS) and rows==[e['values'] for e in packets],
                synthetic_mode_declared=all(e['values'][3]=='S' for e in packets),
                mission_clock_advances=bool(clock_steps) and set(clock_steps)=={1},
                no_active_frame_errors=not any(active_errors.values()),
                no_duplicates_or_conflicts=classifications[(segment,'duplicate')]==0 and classifications[(segment,'conflict')]==0,
                writers_drained=all(d['pending']==0 and d['dropped']==0 and not d['error'] for d in destinations),
                raw_conserved=len(journals)==1 and events==storage['events'] and all(d['saved']==events for d in destinations if d['kind']=='raw'),
                gui_progress_observed=len(during)>=2 and bool(callback_gaps) and max(callback_gaps)<=10,
                bounded_observed_containers=bool(during) and queue_bounded,
                memory_reader_initialized_once=bool(during) and all(e.get('memory_reader_initializations')==1 for e in during),
                input_read_clean=not errors)
    result=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),source='USB_BENCH' if checks['source_usb'] else 'OTHER',
                segment=segment,packets=len(packets),expected_packets=expected,minimum_real_seconds=minimum_seconds,
                first_received_utc=packets[0]['received_utc'],last_received_utc=packets[-1]['received_utc'],
                monotonic_span_seconds=duration,utc_span_seconds=utc[-1]-utc[0],
                interval_seconds=dict(min=min(intervals),median=statistics.median(intervals),mean=statistics.mean(intervals),max=max(intervals)) if intervals else None,
                gui=dict(observations_during_flow=len(during),maximum_callback_gap_seconds=max(callback_gaps) if callback_gaps else None,
                         observed_working_set_bytes=dict(min=min(memory),max=max(memory),first=memory[0],last=memory[-1]) if memory else None,
                         memory_reader_initializations=sorted(set(e.get('memory_reader_initializations',0) for e in during)),
                         maximum_history=max((e.get('history_size',0) for e in during),default=0),maximum_display_queue=max((e.get('update_queue',0) for e in during),default=0)),
                checks=checks,passed=all(checks.values()),active_errors=active_errors,total_events_by_kind=dict(kinds),
                mission_clock_step_histogram=dict(clock_steps),states=dict(Counter(e['values'][4] for e in packets)),
                read_errors=errors,destinations=destinations,source_files_sha256=source_sha,
                software_source_sha256=environment.get('source_sha256') if environment else None,
                limits='Ensayo de flujo USB sintético, sin RF ni autonomía. Working set es memoria residente observada, no prueba universal de ausencia de fugas. GUI observada por callbacks y contenedores; un intervalo de más de10s entre registros impide aprobar continuidad por este analizador. No equiparo cantidad acelerada o ventana abierta a dos horas reales.')
    output.mkdir(parents=True)
    with (output/'health.csv').open('x',encoding='utf-8',newline='') as h:
        writer=csv.writer(h);writer.writerow(['elapsed_seconds','unique','working_set_bytes','history_size','display_queue','pending','dropped'])
        for e in health:writer.writerow([e['elapsed'],e['totals']['total_unique'],e.get('working_set_bytes'),e.get('history_size'),e.get('update_queue'),sum(d['pending'] for d in e['storage']),sum(d['dropped'] for d in e['storage'])])
    with (output/'resultado.json').open('x',encoding='utf-8',newline='\n') as h:json.dump(result,h,ensure_ascii=False,indent=2)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--output',required=True,type=Path)
    p.add_argument('--expected',required=True,type=int);p.add_argument('--minimum-seconds',default=7200,type=float)
    a=p.parse_args();r=summarize(a.root,a.output,a.expected,a.minimum_seconds)
    print(json.dumps(dict(passed=r['passed'],packets=r['packets'],monotonic_seconds=r['monotonic_span_seconds'],checks=r['checks']),ensure_ascii=True))
    raise SystemExit(0 if r['passed'] else 2)
