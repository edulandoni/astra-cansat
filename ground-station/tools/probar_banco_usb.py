"""ASTRA-20/21: capturo una sesión física USB sin cambiar el parser del banco.

No cargo firmware ni configuro RF. --scenario etiqueta el firmware ya cargado;
no lo selecciona ni envía telecomandos. Cada ejecución crea archivos nuevos.
"""
import argparse
import hashlib
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BANK = Path(__file__).resolve().parents[1] / 'banco-usb-v0.1'
sys.path.insert(0, str(BANK))
from protocol import Framer, Counter, parse
from storage import Recorder


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port', required=True)
    p.add_argument('--team', default='1000')
    p.add_argument('--baud', type=int, default=115200)
    p.add_argument('--seconds', type=float, default=137)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--scenario', choices=['NOMINAL', 'PACKET_LOSS', 'CORRUPTED_PACKET', 'GPS_LOSS', 'RESET'], default='NOMINAL')
    p.add_argument('--reset', action='store_true', help='Reinicio EN por RTS para empezar la misión del sketch; no es un corte de alimentación.')
    args = p.parse_args()
    if args.seconds <= 0 or len(args.team) != 4 or not args.team.isascii() or not args.team.isdigit():
        p.error('Duración positiva y TEAM de banco de cuatro dígitos requeridos')
    import serial
    recorder = Recorder(args.output, args.team)
    session = recorder.directory
    counter, framer = Counter(), Framer()
    intervals, states, counts = [], [], []
    rejected = 0
    previous = None
    error = None
    started_utc = datetime.now(timezone.utc).isoformat()
    raw_path = session / 'usb-original.bin'
    try:
        link = serial.Serial(port=None, baudrate=args.baud, timeout=.1)
        link.port, link.dtr, link.rts = args.port, False, False
        link.open()
        with link, raw_path.open('xb') as raw_file:
            if args.reset:
                link.rts = True
                time.sleep(.15)
                link.rts = False
                # El sketch conocido inicia a 1 s. Conservo el arranque en crudo;
                # excluyo sólo esta ventana explícita de 0,5 s del parser ASCII.
                until = time.monotonic() + .5
                while time.monotonic() < until:
                    data = link.read(512)
                    raw_file.write(data)
                    if data:
                        recorder.event(kind='startup_window', raw_hex=data.hex())
            until = time.monotonic() + args.seconds
            while time.monotonic() < until:
                data = link.read(512)
                raw_file.write(data)
                for raw in framer.feed(data):
                    now = time.monotonic()
                    try:
                        packet = parse(raw, args.team)
                        if len(packet.values) != 22:
                            raise ValueError('Extensión sin esquema acordado')
                    except (ValueError, UnicodeError) as exc:
                        rejected += 1
                        recorder.event(kind='rejected', reason=str(exc), raw_hex=raw.hex())
                        continue
                    recorder.event(kind='accepted', raw=raw.decode('ascii'))
                    if counter.add(packet.count):
                        recorder.save(packet)
                        counts.append(packet.count)
                        if previous is not None:
                            intervals.append(now-previous)
                        previous = now
                        if not states or states[-1] != packet.data['STATE']:
                            states.append(packet.data['STATE'])
                        print(f"RX {packet.count:03d} {packet.data['STATE']} h={packet.data['ALTITUDE']}", flush=True)
    except (OSError, serial.SerialException) as exc:
        error = str(exc)
        recorder.event(kind='capture_error', reason=error)
    finally:
        recorder.close()
    result = dict(source='ESP32 físico → CP210x → USB; datos de misión sintéticos',
                  started_utc=started_utc, ended_utc=datetime.now(timezone.utc).isoformat(),
                  port=args.port, baud=args.baud, team=args.team, scenario_label=args.scenario,
                  reset_rts_requested=args.reset, startup_window_seconds=.5 if args.reset else 0,
                  received=counter.received, unique=counter.unique, duplicates=counter.duplicates,
                  observed_gaps=counter.lost, counter_warning=counter.warning,
                  rejected=rejected, framing_overflows=framer.overflows, states=states,
                  first_count=counts[0] if counts else None, last_count=counts[-1] if counts else None,
                  interval_seconds=dict(min=min(intervals), median=statistics.median(intervals), max=max(intervals)) if intervals else None,
                  recording_error=recorder.error, capture_error=error,
                  nominal_complete=(args.scenario == 'NOMINAL' and counts == list(range(1,132)) and not rejected and not framer.overflows and not error and not recorder.error and states[-1:] == ['LANDED']),
                  limits='No acredita radio, sensores reales, autonomía, corte eléctrico o formato RF/CONAE v2 acordado. Ventana de arranque excluida explícitamente y conservada en crudo; no usar con firmware de inicio más rápido sin revisar esta condición.')
    result['files_sha256'] = {x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in session.iterdir() if x.is_file()}
    (session/'resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(session=str(session), **result), ensure_ascii=True), flush=True)
    return 1 if error or recorder.error else 0


if __name__ == '__main__':
    raise SystemExit(main())
