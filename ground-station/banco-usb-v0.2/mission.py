"""Modelo ilustrativo de banco. Alturas/energía ficticias, no vuelo previsto."""
import math
from wire import SCENARIOS

def model(t):
    if t<10:return 0.,'LAUNCH_PAD'
    if t<30:
        u=t-10;return 50*u-1.25*u*u,'ASCENT'
    if t==30:return 500.,'APOGEE'
    u=t-30
    if u<100/15:return 500-15*u,'DESCENT'
    h=max(0.,400-5*(u-100/15))
    if h==0:return 0.,'LANDED'
    return h,('PROBE_RELEASE' if t==37 else 'PAYLOAD_RELEASE')

def clock(seconds):
    seconds=int(seconds)%86400
    return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'

def sample(t,scenario='NOMINAL',team='1000',base=46800,offset=0.):
    if scenario not in SCENARIOS:raise ValueError('Escenario desconocido')
    if scenario=='PACKET_LOSS' and t%10==5:return None,'omitted'
    if scenario=='RESET' and 60<=t<63:return None,'omitted'
    h,state=model(t)
    gps_lost=scenario=='GPS_LOSS' and 50<=t<65
    gt=49 if gps_lost else t;gh=model(gt)[0]+30
    v=[team,clock(base+t),str(t+1),'S',state,
       f'{h+offset:.1f}',f'{23-.0065*h:.1f}',f'{101.325*(1-2.25577e-5*h)**5.25588:.1f}',
       f'{max(3.6,4.1-.5*t/7200):.2f}',f'{.28 if t==37 else .18:.2f}',
       f'{2*math.sin(t/5):.2f}',f'{math.cos(t/6):.2f}',f'{math.sin(t/7):.2f}',
       '0.00','0.00',f'{9.81 if state in {"LAUNCH_PAD","LANDED"} else 9.81+.2*math.sin(t):.2f}',
       clock(base+gt),f'{gh:.1f}',f'{-34.6+gt*.000001:.4f}',f'{-58.4+gt*.000001:.4f}',str(0 if gps_lost else 9),'NONE']
    corrupt=scenario=='CORRUPTED_PACKET' and t%13==6
    if corrupt:v[7]='BAD'
    return (','.join(v)+'\r').encode('ascii'),('corrupted' if corrupt else 'emitted')

def expected(scenario,samples=131):
    result={'emitted':[],'omitted':[],'corrupted':[]}
    for t in range(samples):result[sample(t,scenario)[1]].append(t+1)
    return result
