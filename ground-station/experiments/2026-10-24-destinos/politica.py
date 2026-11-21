"""ASTRA-18/24: política lógica sobre metadatos de prueba, sin formato RF elegido."""
import argparse
import json
from pathlib import Path


def decide(frame, *, team, local, peer, version):
    # integrity_checked es un resultado del futuro decodificador, no un bit
    # recibido que deba creerse. Aquí no calculo CRC ni autentico a nadie.
    if not isinstance(frame,dict):return 'MALFORMED'
    for field in ['team','source','destination','version']:
        if not isinstance(frame.get(field),str) or not frame[field]:return 'MISSING_METADATA'
    if type(frame.get('broadcast')) is not bool:return 'UNKNOWN_DESTINATION_POLICY'
    if frame['broadcast']:return 'BROADCAST_REJECTED'
    if frame['team']!=team:return 'FOREIGN_TEAM'
    if frame['destination']!=local:return 'OTHER_DESTINATION'
    if frame['source']!=peer:return 'UNEXPECTED_SOURCE'
    if frame['version']!=version:return 'UNSUPPORTED_VERSION'
    if frame.get('integrity_checked') is not True:return 'INTEGRITY_NOT_VERIFIED'
    return 'ACCEPT'


def run():
    context=dict(team='TEAM_BENCH',local='ground',peer='flight',version='POLICY_EXPERIMENT_1')
    good=dict(team='TEAM_BENCH',source='flight',destination='ground',version='POLICY_EXPERIMENT_1',broadcast=False,integrity_checked=True)
    vectors=[('propio',good,'ACCEPT'),('equipo_ajeno',{**good,'team':'OTHER'},'FOREIGN_TEAM'),
             ('destino_otro',{**good,'destination':'elsewhere'},'OTHER_DESTINATION'),
             ('origen_no_esperado',{**good,'source':'elsewhere'},'UNEXPECTED_SOURCE'),
             ('version_incompatible',{**good,'version':'other'},'UNSUPPORTED_VERSION'),
             ('integridad_fallida',{**good,'integrity_checked':False},'INTEGRITY_NOT_VERIFIED'),
             ('integridad_no_comprobada',{k:v for k,v in good.items() if k!='integrity_checked'},'INTEGRITY_NOT_VERIFIED'),
             ('broadcast',{**good,'broadcast':True},'BROADCAST_REJECTED'),
             ('broadcast_sin_politica',{k:v for k,v in good.items() if k!='broadcast'},'UNKNOWN_DESTINATION_POLICY'),
             ('sin_destino',{k:v for k,v in good.items() if k!='destination'},'MISSING_METADATA'),
             ('broadcast_no_booleano',{**good,'broadcast':'false'},'UNKNOWN_DESTINATION_POLICY')]
    results=[]
    for name,frame,want in vectors:
        got=decide(frame,**context);results.append(dict(case=name,input=frame,expected=want,actual=got,passed=got==want))
    return dict(context=context,vectors=results,passed=all(r['passed'] for r in results),
                scope='Metadatos ficticios; no bytes de vuelo o perfil adoptado, CRC calculado, autenticación o RF. No resuelve colisiones ni impide recepción física de otras señales.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=run();a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
    print(json.dumps(dict(passed=result['passed'],vectors=len(result['vectors'])),ensure_ascii=True))
    raise SystemExit(0 if result['passed'] else 2)
