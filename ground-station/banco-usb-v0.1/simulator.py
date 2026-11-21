"""Deterministic synthetic mission, not a prediction of the real flight."""
import math

SCENARIOS = ['NOMINAL', 'PACKET_LOSS', 'CORRUPTED_PACKET', 'GPS_LOSS', 'RESET']

def sample(t, team='1000', scenario='NOMINAL'):
    if t < 10:
        altitude, velocity, state = 0., 0., 'LAUNCH_PAD'
    elif t < 30:
        u = t-10
        altitude, velocity, state = 50*u-1.25*u*u, 50-2.5*u, 'ASCENT'
    elif t == 30:
        altitude, velocity, state = 500., 0., 'APOGEE'
    elif t < 40:
        u = t-30
        altitude, velocity, state = 500.-u*u, -2*u, 'DESCENT'
    elif t == 40:
        altitude, velocity, state = 400., -5., 'PROBE_RELEASE'
    elif t < 120:
        altitude, velocity, state = 400.-5*(t-40), -5., 'PAYLOAD_RELEASE'
    else:
        altitude, velocity, state = 0., 0., 'LANDED'
    # 13:00 UTC is a fixed synthetic clock, not local wall clock.
    utc = f'{13+(t//3600):02d}:{(t//60)%60:02d}:{t%60:02d}'
    gps_lost = scenario == 'GPS_LOSS' and 50 <= t < 65
    sats = 0 if gps_lost else 9
    # During GPS loss retain last fix (t=49), never substitute invented zeros.
    gps_t = 49 if gps_lost else t
    gps_alt = 400.-5*(49-40)+30 if gps_lost else altitude+30
    gps_utc = f'13:{gps_t//60:02d}:{gps_t%60:02d}'
    values = [team, utc, str(t+1), 'S', state,
        f'{altitude:.1f}', f'{23-.0065*altitude:.1f}',
        f'{101.325*(1-2.25577e-5*altitude)**5.25588:.1f}',
        f'{4.1-.0008*t:.1f}', f'{.18+(.1 if t==40 else 0):.2f}',
        f'{2*math.sin(t/5):.2f}', f'{math.cos(t/6):.2f}', f'{math.sin(t/7):.2f}',
        '0.00', '0.00', f'{9.81 if state in {"LAUNCH_PAD","LANDED"} else 9.81+0.2*math.sin(t):.2f}',
        gps_utc, f'{gps_alt:.1f}', f'{-34.6+gps_t*.000001:.4f}',
        f'{-58.4+gps_t*.000001:.4f}', str(sats), 'NONE']
    # RESET models an FSW task interruption, preserving counter/mission clock.
    # An actual ESP32 power cycle is NOT covered by this in-memory scenario.
    if scenario == 'RESET' and 60 <= t < 63:
        return None
    if scenario == 'PACKET_LOSS' and t % 10 == 5:
        return None
    if scenario == 'CORRUPTED_PACKET' and t % 13 == 6:
        values[7] = 'BAD'
    return (','.join(values)+'\r').encode('ascii')
