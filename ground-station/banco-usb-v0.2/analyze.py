"""ASTRA-20/21: contraste offline del diario físico con el oráculo declarado."""
import argparse
import csv
import hashlib
import json
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from mission import expected

def analyze(root,samples=131):
    root=Path(root);path=root/'journal.jsonl'
    events=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    segments={};commands=Counter();repeat=[]
    for e in events:
        if e['kind']=='command_repeat_requested':repeat.append(e['message']['id'])
        if e['kind']=='command_queued':commands[e['message']['op']]+=1
        if e['kind']=='control' and e['message']['kind']=='oracle':
            segments.setdefault(e['segment'],e['message']['scenario'])
    cases=[]
    for segment,scenario in segments.items():
        scoped=[e for e in events if e.get('segment')==segment]
        packets=[e for e in scoped if e['kind']=='packet']
        rejected=[e for e in scoped if e['kind']=='rejected']
        oracle=Counter(e['message']['outcome'] for e in scoped if e['kind']=='control' and e['message']['kind']=='oracle')
        counts=[e['count'] for e in packets];truth=expected(scenario,samples)
        target={k:len(v) for k,v in truth.items()}
        times=[datetime.fromisoformat(e['received_utc']).timestamp() for e in packets]
        dt=[b-a for a,b in zip(times,times[1:])]
        with (root/'segments'/segment/'Flight_1000.csv').open(encoding='utf-8',newline='') as h:rows=list(csv.reader(h))[1:]
        gps_missing=[e for e in packets if e['values'][20]=='0']
        lastfix=None;gps_retained=True
        for e in packets:
            v=e['values']
            if v[20]=='0':gps_retained &= lastfix is not None and v[16:20]==lastfix
            else:lastfix=v[16:20]
        checks=dict(counts_equal_expected=counts==truth['emitted'],oracle_equal_expected=all(oracle[k]==v for k,v in target.items()),
                    rejected_equal_expected=len(rejected)==target['corrupted'],csv_equal_packets=rows==[e['values'] for e in packets],
                    gps_retained=gps_retained,gps_missing_expected=len(gps_missing)==(15 if scenario=='GPS_LOSS' else 0))
        cases.append(dict(segment=segment,scenario=scenario,unique=len(packets),rejected_in_segment=len(rejected),oracle=dict(oracle),
                          elapsed_first_to_last=(times[-1]-times[0]) if times else None,
                          interval_min=min(dt) if dt else None,interval_median=statistics.median(dt) if dt else None,interval_max=max(dt) if dt else None,
                          checks=checks,passed=all(checks.values())))
    storage=json.loads((root/'storage-summary.json').read_text(encoding='utf-8'))
    return dict(source='USB_BENCH' if any(e.get('source')=='USB_BENCH' for e in events) else 'PC_BENCH',
                input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),events=len(events),cases=cases,
                command_requests=dict(commands),manual_repeat_ids=repeat,
                storage=[{k:v for k,v in z.items() if k!='root'} for z in storage['destinations']],
                all_cases_match=bool(cases) and all(c['passed'] for c in cases),
                note='Análisis posterior del original conservado. Los rechazos del primer campaign-result eran acumulados; aquí se calculan por segmento. No acredita RF, autonomía, reinicio físico ni ensayo prolongado.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--samples',type=int,default=131)
    a=p.parse_args();result=analyze(a.root,a.samples)
    with a.output.open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=True))
