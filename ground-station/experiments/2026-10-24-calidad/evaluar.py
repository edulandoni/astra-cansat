"""ASTRA-34: comparo reglas conocidas del banco con avisos medidos en reloj virtual."""
import argparse
import csv
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CORE = Path(__file__).resolve().parents[2] / 'banco-usb-v0.2'
sys.path.insert(0, str(CORE))
from engine import Engine
from journal import Store
from mission import sample
from quality import quality_flags
from sources import PCBench

CASES = [
    ('nominal', None, None, 'any'),
    ('altura_constante', None, None, 'any'),
    ('gps_sin_fix', 50., 65., 'gps_no_fix'),
    ('hora_gps_congelada', 10., 20., 'gps_stale'),
    ('hora_mision_congelada', 10., 20., 'mission_clock_frozen'),
    ('telemetria_pausada_con_control_activo', 10., 16., 'telemetry_stale'),
]


def previous_rules(s):
    """Reglas documentadas de app.py anterior; no emulo toda la GUI histórica."""
    data = s['latest']
    return dict(telemetry_stale=bool(data and s['data_age'] > 3),
                gps_no_fix=bool(data and data['GPS_SATS'] == '0'),
                gps_stale=False, mission_clock_frozen=s['clock_warning'])


def run_case(name, onset, end, target):
    clock = [1000.]
    trace = []
    with tempfile.TemporaryDirectory() as directory:
        store = Store(directory)
        engine = Engine(store, source='PC_BENCH', clock=lambda: clock[0])
        bench = PCBench(engine); bench.hello()
        try:
            for step in range(524):
                t = step / 4
                clock[0] = 1000 + t
                if step % 4 == 0:
                    tick = int(t)
                    if name == 'telemetria_pausada_con_control_activo' and onset <= t < end:
                        bench.hello()  # Mismo contexto; enlace válido sin medición nueva.
                    else:
                        raw = sample(tick, 'GPS_LOSS' if name == 'gps_sin_fix' else 'NOMINAL')[0]
                        fields = raw[:-1].decode().split(',')
                        if name == 'altura_constante': fields[5] = '0.0'
                        if name == 'hora_gps_congelada' and onset <= t < end: fields[16] = '13:00:09'
                        if name == 'hora_mision_congelada' and onset <= t < end: fields[1] = '13:00:09'
                        engine.feed((','.join(fields) + '\r').encode())
                s = engine.snapshot(); flags = quality_flags(s); old = previous_rules(s)
                selected = any(flags[k] for k in old) if target == 'any' else flags[target]
                previous = any(old.values()) if target == 'any' else old[target]
                trace.append(dict(case=name, t=t, alert=selected, previous_alert=previous,
                                  telemetry_age=s['data_age'], gps_age=s['gps_age'], link_age=s['link_age'],
                                  gps_stale=flags['gps_stale'], telemetry_stale=flags['telemetry_stale']))
        finally:
            store.close()
    in_fault = lambda r: onset is not None and onset <= r['t'] < end
    detections = [r['t'] for r in trace if r['alert'] and in_fault(r)]
    previous = [r['t'] for r in trace if r['previous_alert'] and in_fault(r)]
    recovered = next((r['t'] for r in trace if end is not None and r['t'] >= end and not r['alert']), None)
    result = dict(case=name, target=target, onset_s=onset, end_s=end,
                  first_detection_s=min(detections) if detections else None,
                  detection_delay_from_first_fault_s=min(detections)-onset if detections else None,
                  previous_first_detection_s=min(previous) if previous else None,
                  recovery_s=recovered,
                  unexpected_positive_observations=sum(r['alert'] and not in_fault(r) for r in trace),
                  separate_gps_alerts_during_telemetry_pause=sum(r['gps_stale'] for r in trace) if name.startswith('telemetria_') else None)
    result['passed'] = result['unexpected_positive_observations'] == 0 and (onset is None or bool(detections))
    if name == 'hora_gps_congelada': result['passed'] &= not previous
    if name.startswith('telemetria_'): result['passed'] &= result['separate_gps_alerts_during_telemetry_pause'] == 0
    return result, trace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Elijo salida nueva; conservo resultados previos')
    results = []; traces = []
    for case in CASES:
        result, trace = run_case(*case); results.append(result); traces.extend(trace)
    report = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), source='VIRTUAL_CLOCK_SOFTWARE',
                  grid_seconds=.25, thresholds_seconds=dict(telemetry=3, gps=3), cases=results,
                  source_sha256={name:hashlib.sha256((CORE/name).read_bytes()).hexdigest()
                                 for name in ['engine.py','quality.py','mission.py','journal.py']},
                  passed=all(r['passed'] for r in results),
                  limits=['Casos elegidos, no tasa estadística de fallas ni confiabilidad de vuelo.',
                          'Tiempos de regla sobre reloj virtual; no latencia física ni demora máxima de GUI.',
                          'La comparación anterior reproduce reglas declaradas, no ejecuta una GUI histórica.',
                          'Altitud constante no prueba sensor averiado; no agrego rangos no acordados.',
                          'Los umbrales son de banco, no decisiones del ICD.'])
    args.output.mkdir(parents=True)
    (args.output/'resultado.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (args.output/'trazas.csv').open('x',encoding='utf-8',newline='') as h:
        writer=csv.DictWriter(h,fieldnames=list(traces[0]));writer.writeheader();writer.writerows(traces)
    print(json.dumps(report,ensure_ascii=True,indent=2))
    raise SystemExit(0 if report['passed'] else 2)


if __name__ == '__main__': main()
