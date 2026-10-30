#!/usr/bin/env python3
"""Capture and validate ASTRA characterization CSV from a serial port."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import sys


MPU_FIELDS = [
    "sample", "timestamp_ms",
    "accel_raw_x", "accel_raw_y", "accel_raw_z",
    "accel_x_g", "accel_y_g", "accel_z_g",
    "gyro_raw_x", "gyro_raw_y", "gyro_raw_z",
    "gyro_x_dps", "gyro_y_dps", "gyro_z_dps",
]
SOLAR_FIELDS = ["sample", "timestamp_ms", "solar_voltage_mV", "battery_voltage_mV"]
SCHEMAS = {"mpu": MPU_FIELDS, "solar": SOLAR_FIELDS}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Serial port, for example COM7")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--output", required=True, type=Path, help="Destination CSV path")
    parser.add_argument("--schema", choices=["auto", "mpu", "solar"], default="auto")
    parser.add_argument("--host-timestamp", action="store_true", help="Append host_timestamp_utc")
    parser.add_argument("--timeout", type=float, default=1.0, help="Serial read timeout in seconds")
    return parser.parse_args()


def parse_numeric_row(fields: list[str], row: list[str]) -> None:
    if len(row) != len(fields):
        raise ValueError(f"expected {len(fields)} columns, received {len(row)}")
    for name, value in zip(fields, row):
        if name in {"sample", "timestamp_ms", "accel_raw_x", "accel_raw_y", "accel_raw_z",
                    "gyro_raw_x", "gyro_raw_y", "gyro_raw_z", "solar_voltage_mV",
                    "battery_voltage_mV"}:
            int(value)
        else:
            float(value)


def main() -> int:
    args = parse_args()
    try:
        import serial  # type: ignore
    except ImportError:
        print("pyserial is required: python -m pip install pyserial", file=sys.stderr)
        return 2

    expected = SCHEMAS.get(args.schema)
    accepted = 0
    rejected = 0
    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with serial.Serial(args.port, args.baud, timeout=args.timeout) as port, \
                args.output.open("w", newline="", encoding="utf-8") as output:
            writer = csv.writer(output)
            header_written = False
            try:
                while True:
                    raw = port.readline()
                    if not raw:
                        continue
                    try:
                        text = raw.decode("ascii").strip()
                    except UnicodeDecodeError:
                        rejected += 1
                        continue
                    if not text:
                        continue
                    row = next(csv.reader([text]))

                    if row in SCHEMAS.values():
                        detected = row
                        if expected is not None and detected != expected:
                            raise RuntimeError(f"serial schema does not match --schema {args.schema}")
                        expected = detected
                        if not header_written:
                            writer.writerow(expected + (["host_timestamp_utc"] if args.host_timestamp else []))
                            output.flush()
                            header_written = True
                        continue

                    if expected is None:
                        rejected += 1
                        continue
                    try:
                        parse_numeric_row(expected, row)
                    except ValueError:
                        rejected += 1
                        continue
                    if not header_written:
                        writer.writerow(expected + (["host_timestamp_utc"] if args.host_timestamp else []))
                        header_written = True
                    if args.host_timestamp:
                        row.append(datetime.now(timezone.utc).isoformat(timespec="milliseconds"))
                    writer.writerow(row)
                    output.flush()
                    accepted += 1
            except KeyboardInterrupt:
                pass
    except (OSError, RuntimeError, serial.SerialException) as error:
        print(f"capture failed: {error}", file=sys.stderr)
        return 1

    print(f"captured {accepted} rows; rejected {rejected}; output: {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
