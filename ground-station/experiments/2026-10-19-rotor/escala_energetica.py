"""Estimo una escala gravitatoria ilustrativa; no simulo la aerodinámica del rotor."""
import argparse
import csv
import json
import math
from pathlib import Path

G=9.80665

def evaluate(mass_kg,apogee_m,release_fraction,speed_m_s):
    if not all(math.isfinite(x) and x>0 for x in [mass_kg,apogee_m,release_fraction,speed_m_s]):
        raise ValueError('Parámetros finitos y positivos requeridos.')
    if release_fraction>1:raise ValueError('La fracción no puede superar 1.')
    height=apogee_m*release_fraction
    gravity_j=mass_kg*G*height
    time_s=height/speed_m_s
    cases=[]
    for eta in [0.01,0.05,0.10,0.20]:
        electric_j=gravity_j*eta
        row={'hypothetical_global_efficiency':eta,
             'electric_energy_j':electric_j,'electric_energy_wh':electric_j/3600,
             'average_electric_power_w':electric_j/time_s,
             'equivalent_minutes_at_1w':electric_j/60,
             'fraction_of_hypothetical_1w_2h_budget':electric_j/7200}
        assert math.isclose(row['average_electric_power_w']*time_s,electric_j)
        assert 0<electric_j<=gravity_j
        cases.append(row)
    return {'inputs':{'constant_descending_mass_kg':mass_kg,'illustrative_apogee_m':apogee_m,
                      'illustrative_rotor_release_fraction':release_fraction,
                      'assumed_constant_descent_m_s':speed_m_s,'g_m_s2':G},
            'reference_total_gravity_wh':mass_kg*G*apogee_m/3600,
            'rotor_phase_height_m':height,'rotor_phase_gravity_j':gravity_j,
            'rotor_phase_gravity_wh':gravity_j/3600,
            'assumed_phase_duration_s':time_s,
            'gravitational_power_scale_w':mass_kg*G*speed_m_s,'cases':cases,
            'limits':['500 m y los rendimientos globales son hipótesis, no datos de vuelo ni eficiencia medida.',
                      'Uso masa constante: si separo contenedor o piezas debo recalcular cada fase.',
                      'La escala mgh corresponde al cambio gravitatorio del tramo; no suma energía del viento ni cambios de energía cinética.',
                      'No toda esa energía está disponible en el eje; las pérdidas aerodinámicas y eléctricas forman parte del rendimiento global supuesto.',
                      'No predigo RPM, torque, despliegue, estabilidad, velocidad real ni admisibilidad reglamentaria.',
                      'Aumentar la carga eléctrica cambia el freno del generador y puede cambiar la autorrotación y el descenso; aquí no resuelvo ese acoplamiento.',
                      'No puedo alimentar la espera de dos horas dentro del cohete mediante un rotor que aún no recibe flujo.']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--masa-kg',type=float,default=.5)
    p.add_argument('--apogeo-m',type=float,default=500)
    p.add_argument('--fraccion-despliegue',type=float,default=.8)
    p.add_argument('--descenso-m-s',type=float,default=5)
    p.add_argument('--salida',type=Path,required=True)
    a=p.parse_args()
    if a.salida.exists():p.error('Conservo versiones: elegir una salida nueva.')
    result=evaluate(a.masa_kg,a.apogeo_m,a.fraccion_despliegue,a.descenso_m_s)
    a.salida.mkdir(parents=True,exist_ok=False)
    with (a.salida/'escala.json').open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    with (a.salida/'escenarios.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(result['cases'][0]));writer.writeheader();writer.writerows(result['cases'])
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
