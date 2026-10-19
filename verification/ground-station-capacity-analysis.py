"""Calculos de investigacion, sin conexion a hardware ni datos de vuelo."""
import json
import math
from pathlib import Path

def airtime_ms(payload_bytes, sf, bw_hz=125000, cr=1, preamble=8, crc=True, implicit=False):
    de = int((2 ** sf / bw_hz) >= 0.016)
    symbols = 8 + max(math.ceil((8 * payload_bytes - 4 * sf + 28 + 16 * int(crc) - 20 * int(implicit)) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25 + symbols) * 2 ** sf / bw_hz * 1000

def semtech_integer_ms(payload_bytes, sf, bw_hz=125000, cr=1, preamble=8, crc=True, implicit=False):
    de = ((bw_hz == 125000 and sf in (11,12)) or (bw_hz == 250000 and sf == 12))
    numerator = max(8 * payload_bytes + 16 * int(crc) - 4 * sf + (0 if implicit else 20) + 8, 0)
    denominator = 4 * (sf - 2 * int(de))
    intermediate = math.ceil(numerator / denominator) * (cr + 4) + preamble + 12
    return math.ceil(1000 * ((4 * intermediate + 1) * 2 ** (sf - 2)) / bw_hz)

fields = ['1000','13:14:02','7200','F','DESCENT','400.0','25.0','96.0','3.8','0.25','-12.50','1.20','-3.10','0.10','0.20','9.80','13:14:02','726.0','-34.6000','-58.4000','12','CXON']
assert len(fields) == 22
frame = ','.join(fields) + '\r'
assert frame.isascii()
example_bytes = len(frame.encode('ascii'))
commands = ['CMD,1000,CX,ON','CMD,1000,CX,OFF','CMD,1000,ST,13:35:59','CMD,1000,ST,GPS','CMD,1000,CAL','CMD,1000,MEC,DEVICE,ON','CMD,1000,MEC,DEVICE,OFF']
command_bytes = max(len(c.encode('ascii')) for c in commands)

checks = 0
for bw in (125000,250000,500000):
    for sf in range(7,13):
        for crc in (False,True):
            for implicit in (False,True):
                for payload in (1,20,50,100,150,200,250,255):
                    for cr in (1,2,3,4):
                        a = math.ceil(airtime_ms(payload,sf,bw,cr,crc=crc,implicit=implicit))
                        b = semtech_integer_ms(payload,sf,bw,cr,crc=crc,implicit=implicit)
                        assert a == b, (payload,sf,bw,cr,crc,implicit,a,b)
                        checks += 1

air = []
for sf in range(7,13):
    for payload in (example_bytes,200,250):
        tx = airtime_ms(payload,sf)
        cmd = airtime_ms(command_bytes,sf)
        air.append({'sf':sf,'payload_bytes':payload,'telemetry_ms':round(tx,3),'command_ms':round(cmd,3),'one_telemetry_and_command_ms':round(tx+cmd,3),'two_telemetry_and_command_ms':round(2*tx+cmd,3),'remaining_1Hz_ms':round(1000-tx-cmd,3)})

R = 287.05
T = 288.15
g = 9.80665
p = 101325.0
scale = R*T/g
pressure = {'assumptions':{'temperature_K':T,'pressure_Pa':p,'model':'isothermal local hypsometric sensitivity'},'height_step_for_0_1kPa_m':round(scale/p*100,4),'half_quantization_step_m':round(scale/p*50,4),'pressure_change_for_0_1m_Pa':round(p/scale*0.1,4)}
filtering = []
for c in (2,4,8,16):
    n = math.ceil(math.log(0.25)/math.log(1-1/c))
    filtering.append({'coefficient':c,'samples_to_75_percent':n,'response_seconds_at_2Hz':n/2,'response_seconds_at_10Hz':n/10})

result = {'kind':'analisis_teorico_no_ensayo_fisico','semtech_formula_comparisons':checks,'radio_assumptions':{'bandwidth_Hz':125000,'coding_rate':'4/5','preamble_symbols':8,'header':'explicit','crc':True,'period_ms':1000,'excluded':'guard times, switching, host delay, extra framing, acknowledgements and retries'},'example_packet':{'text':frame,'field_count':22,'bytes':example_bytes,'accel_units':'PENDIENTE ACLARACION CONAE; valores solo ilustrativos','gps_signs':'PENDIENTE ACLARACION CONAE; ejemplo convencional sur/oeste negativo'},'example_command_max_bytes':command_bytes,'airtime':air,'pressure_quantization':pressure,'filter_response':filtering,'sources':['https://github.com/Lora-net/LoRaMac-node/blob/master/src/radio/sx1276/sx1276.c','https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf','https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027.pdf']}
Path(__file__).with_name('ground-station-capacity-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'comparisons':checks,'sample_packet_bytes':example_bytes,'sample_command_bytes':command_bytes,'airtime_200B':[x for x in air if x['payload_bytes']==200],'pressure':pressure,'filtering':filtering},indent=2))

