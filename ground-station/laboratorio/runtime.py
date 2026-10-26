"""ASTRA-41: reutilizo el receptor real con un emisor exclusivamente de PC."""
import sys
import threading
import json
import uuid
from pathlib import Path

AREA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AREA / 'banco-usb-v0.2'))
sys.path.insert(0, str(AREA / 'tools'))
from engine import Engine
from journal import Store
from sources import PCBench
from mission import sample
from wire import FIELDS
from airtime_lora import airtime
from recover import recover


class Simulation:
    def __init__(self, output, scenario='NOMINAL', speed=5):
        if scenario not in ('NOMINAL', 'PACKET_LOSS', 'CORRUPTED_PACKET', 'GPS_LOSS', 'RESET'):
            raise ValueError('Escenario desconocido')
        if speed not in (1, 5, 10):
            raise ValueError('Velocidad desconocida')
        self.store = Store(output)
        self.engine = Engine(self.store, source='PC_BENCH')
        self.bench = PCBench(self.engine)
        self.thread = threading.Thread(target=self.bench.run_loop, args=(1/speed,), daemon=True)
        self.thread.start()
        self.engine.command('RUN', scenario=scenario, samples=131)

    def close(self):
        self.engine.stop.set()
        self.thread.join(2)
        self.store.close()


def packet_at(t):
    raw, _ = sample(int(t), 'NOMINAL', '1000', 46800, 12.)
    return raw, list(zip(FIELDS, raw.decode('ascii').strip().split(',')))


def radio_rows(payload, bw=125000, cr=1):
    return [airtime(payload, sf, bw, cr, 8, 1, 0) for sf in range(7,13)]


def recovery_demo(output, mode='complementarias'):
    """Creo fuentes sintéticas nuevas; nunca uso ni altero archivos de vuelo."""
    if mode not in ('complementarias','ausente_en_ambas','conflicto'):
        raise ValueError('Demostración desconocida')
    root=Path(output)/('recuperacion_'+uuid.uuid4().hex)
    root.mkdir(parents=True,exist_ok=False)
    inputs=[]
    for name,counts in [('copia_A',[1,2,3,5,6,7,8]),('copia_B',[1,3,4,5,6,8,9,10])]:
        path=root/(name+'.jsonl'); inputs.append(path)
        with path.open('x',encoding='utf-8') as h:
            for count in counts:
                if mode=='ausente_en_ambas' and count==10:continue
                _,pairs=packet_at(count-1); values=[v for _,v in pairs]
                if mode=='conflicto' and name=='copia_B' and count==1:values[6]='24.0'
                event=dict(kind='packet',pc_session='demo_pc',segment='demo_mision',team='1000',values=values,seq=count)
                h.write(json.dumps(event)+'\n')
    result=recover(inputs,root/'reconstruccion')
    summary=dict(mode=mode,synthetic=True,independent_media_test=False,expected_counts=list(range(1,11)),
                 candidates=result['candidates'],written=result['written'],conflicts=len(result['conflicts']),
                 originals_unchanged=result['originals_unchanged'],root=str(root))
    (root/'resumen-demo.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    return summary


def chart_runs(points):
    """No uno huecos de contador ni identidades diferentes."""
    runs=[]
    for point in points:
        if not runs or point[0]!=runs[-1][-1][0] or point[1]!=runs[-1][-1][1]+1:runs.append([])
        runs[-1].append(point)
    return runs
