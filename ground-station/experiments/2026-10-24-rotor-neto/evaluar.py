"""ASTRA-36: balance incremental hipotético; no modelo aerodinámico ni diseño aprobado."""
import argparse
import json
import math
from pathlib import Path


def evaluate(*, mass_kg, height_m, descent_m_s, efficiency, extra_load_w, standby_s):
    values=(mass_kg,height_m,descent_m_s,efficiency,extra_load_w,standby_s)
    if any(type(x) not in (float,int) or not math.isfinite(x) for x in values):raise ValueError('Entradas numéricas finitas')
    if min(mass_kg,height_m,descent_m_s)<=0 or not 0<=efficiency<=1 or min(extra_load_w,standby_s)<0:raise ValueError('Entradas fuera del dominio del modelo')
    available=mass_kg*9.80665*height_m
    active_s=height_m/descent_m_s
    generated=efficiency*available
    overhead=extra_load_w*(active_s+standby_s)
    return dict(inputs=dict(zip(['mass_kg','height_m','descent_m_s','efficiency','extra_load_w','standby_s'],values)),
                active_seconds=active_s,gravity_ceiling_j=available,generated_wh=generated/3600,
                incremental_consumption_wh=overhead/3600,net_incremental_wh=(generated-overhead)/3600,
                break_even_global_efficiency=overhead/available,
                interpretation='Diferencia energética hipotética; un valor positivo no valida despliegue, estabilidad, masa o velocidad.',
                limits='Sin energía de viento ni cambios cinéticos. Rendimiento global incluye cadena de conversión; la carga extra debe excluir pérdidas ya incluidas para no descontarlas dos veces. No resto el consumo común del CanSat: comparo sólo el agregado. No acredita autonomía previa al descenso.')


def scenarios():
    base=dict(mass_kg=.5,height_m=400.,descent_m_s=5.,efficiency=.1)
    return {name:evaluate(**{**base,**changes}) for name,changes in [
        ('sin_carga_extra',dict(extra_load_w=0.,standby_s=0.)),
        ('auxiliar_solo_en_descenso',dict(extra_load_w=.2,standby_s=0.)),
        ('auxiliar_dos_horas_previas',dict(extra_load_w=.2,standby_s=7200.)),
        ('sin_generacion_con_auxiliar',dict(efficiency=0.,extra_load_w=.2,standby_s=0.))]}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=dict(hypotheses_only=True,cases=scenarios(),recommendation='Continúo sólo como investigación opcional; no presupuesto energía útil ni sustituyo recuperación/paneles/autonomía sin ensayos y acuerdo de responsables.')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
    print(json.dumps({k:v['net_incremental_wh'] for k,v in result['cases'].items()},ensure_ascii=True))
