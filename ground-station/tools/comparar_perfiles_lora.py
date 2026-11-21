"""ASTRA-40: matriz offline de hipótesis de payload/SF/BW/CR, sin acceso a radio."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from airtime_lora import airtime


def comparison():
    rows = []
    for bw in (125000, 250000, 500000):
        for sf in (7, 9, 10):
            for cr in (1, 4):
                for payload in (50, 55, 60, 100, 124, 255):
                    row = airtime(payload, sf, bw, cr, 8, 1, 0)
                    row.update(airtime_ms=round(row['airtime_seconds'] * 1000, 6),
                               airtime_fraction_at_1hz_percent=round(row['airtime_seconds'] * 100, 6),
                               arithmetic_remainder_in_1s_ms=round(1000 - row['airtime_seconds'] * 1000, 6),
                               approved_radio_profile=False, measured_rf_reliability=None,
                               measured_cpu_cost=None, measured_battery_energy=None)
                    rows.append(row)
    return {'generated_utc': datetime.now(timezone.utc).isoformat(), 'jira': 'ASTRA-40',
            'assumptions': {'payload_includes_all_application_bytes': True,
                            'preamble_symbols': 8, 'explicit_header': True, 'physical_crc': True,
                            'telemetry_period_seconds': 1, 'command_ack_guard_times': 'TBD',
                            'frequency_power_antenna_regulatory_approval': 'TBD'},
            'rows': rows,
            'limits': ['No configuro radio ni transmito.',
                       'No sumo encabezado físico/CRC a payload: la fórmula ya los contempla.',
                       'El encabezado propio de aplicación sí debe contarse dentro del payload.',
                       'Resto aritmético positivo no prueba espacio suficiente para comandos ni cumplimiento de régimen.',
                       'El cálculo de tiempo no mide PER, RSSI/SNR, movimiento, CPU o energía.',
                       'Los límites de LoRaWAN no se trasladan a un enlace SX1276 propio.'],
            'source_sha256': {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                              for name in ('airtime_lora.py', 'comparar_perfiles_lora.py')}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Archivo nuevo; nunca sobrescribo una matriz anterior')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as output:
        json.dump(comparison(), output, ensure_ascii=False, indent=2)
        output.write('\n')
    print('Matriz de 108 hipótesis conservada en', args.output)
