"""Investigo límites del banco existente con datos ficticios, sin modificarlo."""
import argparse
import csv
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

GROUND=Path(__file__).resolve().parents[2]
BANK=GROUND/'banco-usb-v0.1'
sys.path.insert(0,str(BANK))
from simulator import sample
from protocol import parse,FIELDS
from acquisition import Acquisition
from storage import Recorder

def change(raw, **fields):
    values=raw.decode('ascii').rstrip('\r').split(',')
    for key,value in fields.items(): values[FIELDS.index(key)]=str(value)
    return (','.join(values)+'\r').encode('ascii')

def accepted(frames):
    ok=bad=0
    for raw in frames:
        try: parse(raw,'1000');ok+=1
        except (ValueError,UnicodeError): bad+=1
    return {'accepted':ok,'rejected':bad}

def investigate():
    rows=[]
    def add(name,observation,**facts):
        rows.append({'case':name,'observation':observation,**facts})

    nominal=accepted([sample(t) for t in range(131)])
    assert nominal=={'accepted':131,'rejected':0}
    add('control_nominal','El parser acepta la misión sintética base.',**nominal)
    foreign=accepted([sample(20,team='1001')])
    assert foreign=={'accepted':0,'rejected':1}
    add('control_equipo_ajeno','El parser rechaza el identificador ajeno de banco.',**foreign)

    for name,field,value in [('salto_altitud','ALTITUDE','3000.0'),
                             ('temperatura_extrema','TEMPERATURE','999.0'),
                             ('giro_extremo','GYRO_R','9999.0')]:
        result=accepted([change(sample(60),**{field:value})])
        add(name,'Un número finito con formato correcto atraviesa el parser; no hay una alarma semántica en esta capa.',
            injected_field=field,injected_value=value,**result)

    frames=[change(sample(t),ALTITUDE=parse(sample(49),'1000').data['ALTITUDE']) for t in range(50,70)]
    result=accepted(frames)
    add('altura_congelada','El parser acepta veinte alturas iguales mientras la presión sintética cambia. Esto no identifica por sí solo qué sensor falló.',
        pressure_distinct=len({parse(f,'1000').data['PRESSURE'] for f in frames}),**result)

    frames=[change(sample(t),MISSION_TIME='13:00:50') for t in range(51,61)]
    add('reloj_congelado','Acepta diez horas de misión iguales con contadores crecientes; una hora bien escrita no acredita avance temporal.',
        counters=[parse(f,'1000').count for f in frames],**accepted(frames))

    with tempfile.TemporaryDirectory() as root:
        recorder=Recorder(root,'1000');a=Acquisition(recorder)
        try:
            a.ingest(sample(20));a.ingest(change(sample(20),ALTITUDE='3000.0'))
            add('duplicado_con_contenido_distinto','El segundo paquete con el mismo contador se cuenta como duplicado y queda en raw, pero no se compara su contenido para avisar conflicto.',
                received=a.counter.received,duplicates=a.counter.duplicates,
                displayed_altitude=a.latest.data['ALTITUDE'],warning=a.counter.warning,
                invalid=a.invalid)
        finally:recorder.close()

    with tempfile.TemporaryDirectory() as root:
        recorder=Recorder(root,'1000');a=Acquisition(recorder)
        try:
            for t in range(100,106):a.ingest(sample(t))
            previous=a.latest.count
            for t in range(6):a.ingest(sample(t))
            add('reinicio_real_de_contador_modelado','Con un contador que vuelve al inicio hay aviso de ambigüedad. La recepción continúa pero latest conserva el contador alto anterior. Necesito acordar cómo distinguir sesiones.',
                latest_before=previous,latest_after=a.latest.count,
                received=a.counter.received,warning=a.counter.warning,
                latest_state=a.latest.data['STATE'],recent_reception=a.last_rx is not None)
        finally:recorder.close()

    with tempfile.TemporaryDirectory() as root:
        recorder=Recorder(root,'1000');a=Acquisition(recorder)
        with patch.object(recorder,'event',side_effect=OSError('FALLO_SINTETICO_REGISTRO_RAW')):
            a.run()
        add('fallo_escritura_raw','Una excepción sintética al registrar raw termina el worker con ERROR. No hay continuidad degradada ni recuperación automática en esta ruta.',
            status=a.status,received=a.counter.received,files_closed=recorder.raw.closed)

    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
             [BANK/'simulator.py',BANK/'protocol.py',BANK/'acquisition.py',BANK/'storage.py']}
    return {'captured_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'Sondeo de software con entradas deliberadamente modificadas; sin hardware, RF ni evaluación estadística de fiabilidad.',
            'baseline_source_sha256':sources,'cases':rows,
            'not_implemented':['monitor semántico','estimación automática de causa','integración GUI','cambio de formato o ICD','recuperación durable del registro'],
            'limits':['Casos de demostración escogidos; no estiman probabilidad real de fallas.',
                      'Un valor extremo, constante o discordante requiere contexto; no establece por sí solo un sensor averiado.',
                      'Presión y altura barométrica pueden derivarse del mismo sensor y no son redundancia independiente.',
                      'La GUI ya distingue algunos datos retenidos y avisos de contador; el sondeo no afirma ausencia de todas las advertencias.']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--salida',type=Path,required=True)
    args=p.parse_args()
    if args.salida.exists():p.error('Conservo las salidas anteriores: elegir un directorio nuevo.')
    result=investigate()
    args.salida.mkdir(parents=True,exist_ok=False)
    (args.salida/'resultados.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (args.salida/'resumen.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['caso','aceptados_parser','rechazados_parser','observacion'])
        for row in result['cases']:writer.writerow([row['case'],row.get('accepted',''),row.get('rejected',''),row['observation']])
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
