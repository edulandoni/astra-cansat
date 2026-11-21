"""ASTRA-25: cálculo offline, con entradas y procedencia explícitas. No configura RF."""
import argparse
import json
import math
from pathlib import Path

FIELDS=('frequency_mhz','distance_m','tx_power_dbm','tx_gain_dbi','rx_gain_dbi',
        'tx_cable_loss_db','rx_cable_loss_db','polarization_loss_db','other_loss_db',
        'rx_sensitivity_dbm','required_margin_db')
LOSSES=('tx_cable_loss_db','rx_cable_loss_db','polarization_loss_db','other_loss_db')


def evaluate(profile):
    values=profile.get('values',{});sources=profile.get('sources',{})
    missing=[]
    for name in FIELDS:
        value=values.get(name)
        if value is None:missing.append(name);continue
        if type(value) not in (float,int) or not math.isfinite(value):raise ValueError('Número finito requerido: '+name)
        if name in ('frequency_mhz','distance_m') and value<=0:raise ValueError('Valor positivo requerido: '+name)
        if (name in LOSSES or name=='required_margin_db') and value<0:raise ValueError('Pérdida/margen objetivo no negativo: '+name)
        if not isinstance(sources.get(name),str) or not sources[name].strip() or sources[name].strip().upper()=='TBD':
            raise ValueError('Falta procedencia explícita para '+name)
    frequency,distance=values.get('frequency_mhz'),values.get('distance_m')
    fspl=20*math.log10(4*math.pi*distance*frequency*1e6/299792458) if frequency and distance else None
    core=('tx_power_dbm','tx_gain_dbi','rx_gain_dbi',*LOSSES)
    rx=None if fspl is None or any(values.get(k) is None for k in core) else (
        sum(values[k] for k in ['tx_power_dbm','tx_gain_dbi','rx_gain_dbi'])-sum(values[k] for k in LOSSES)-fspl)
    sensitivity=values.get('rx_sensitivity_dbm')
    margin=rx-sensitivity if rx is not None and sensitivity is not None else None
    objective=values.get('required_margin_db')
    return dict(label=profile.get('label'),example_only=profile.get('example_only',False),
                missing=missing,fspl_db=fspl,received_power_dbm=rx,margin_db=margin,
                headroom_above_required_db=margin-objective if margin is not None and objective is not None else None,
                additional_loss_sweep=[dict(extra_loss_db=loss,margin_db=margin-loss if margin is not None else None)
                                       for loss in [0,3,6,10]],
                values=values,sources=sources,
                limits='Referencia de espacio libre, no alcance medido. Ganancias en la dirección real y sensibilidad del mismo modo/perfil. No incluye automáticamente suelo, interferencia, shadowing o normativa. TBD no se reemplaza por cero.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():p.error('Elijo archivo nuevo; no reemplazo resultados')
    try:result=evaluate(json.loads(a.input.read_text(encoding='utf-8')))
    except (ValueError,TypeError) as exc:p.error(str(exc))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=True,indent=2))


if __name__=='__main__':main()
