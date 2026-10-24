"""ASTRA-18/25: cálculo offline de airtime SX1276; nunca configura una radio.

Referencia: datasheet Semtech SX1276 rev4, sección4.1.1.7, p31.
Todas las entradas son hipótesis explícitas, no un Radio Profile aprobado.
"""
import argparse
import json
import math

def airtime(payload,sf,bw,cr,preamble,crc,implicit,de=None):
    if not isinstance(payload,int) or not 1<=payload<=255:raise ValueError('Payload LoRa: 1..255 bytes')
    if not isinstance(sf,int) or not 6<=sf<=12:raise ValueError('SF: entero 6..12')
    if not math.isfinite(bw) or not 7800<=bw<=500000:raise ValueError('BW del cálculo: 7800..500000 Hz; confirmar valor soportado')
    if not isinstance(cr,int) or not 1<=cr<=4:raise ValueError('CR: 1=4/5 a 4=4/8')
    if not isinstance(preamble,int) or not 6<=preamble<=65535:raise ValueError('Preámbulo: 6..65535 símbolos')
    if crc not in [0,1] or implicit not in [0,1]:raise ValueError('CRC/IH: 0 o 1')
    if sf==6 and not implicit:raise ValueError('SF6 requiere encabezado implícito')
    symbol=2**sf/bw
    if de is None:de=int(symbol>.016)
    if de not in [0,1] or (symbol>.016 and not de):raise ValueError('DE requerido si símbolo supera16ms')
    symbols=8+max(math.ceil((8*payload-4*sf+28+16*crc-20*implicit)/(4*(sf-2*de)))*(cr+4),0)
    seconds=(preamble+4.25+symbols)*symbol
    return dict(payload_bytes=payload,sf=sf,bw_hz=bw,cr_code=cr,preamble=preamble,crc=crc,implicit=implicit,de=de,
                symbol_seconds=symbol,payload_symbols=symbols,airtime_seconds=seconds,
                one_packet_per_second_air_fraction=seconds,
                fits_one_second_before_commands_and_guards=seconds<1,
                note='Sólo cálculo. No incluye órdenes, ACK, guardas, reintentos ni restricciones de potencia/regulación. No configura RF.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name,typ in [('payload',int),('sf',int),('bw',float),('cr',int),('preamble',int),('crc',int),('implicit',int)]:p.add_argument('--'+name,required=True,type=typ)
    p.add_argument('--de',type=int,choices=[0,1])
    a=p.parse_args()
    try:print(json.dumps(airtime(**vars(a)),ensure_ascii=True,indent=2))
    except ValueError as exc:p.error(str(exc))
