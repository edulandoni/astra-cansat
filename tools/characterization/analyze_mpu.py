#!/usr/bin/env python3
"""Report MPU6500 statistics and optional six-position calibration estimates."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
import statistics
import sys


ACCEL_COLUMNS = ["accel_x_g", "accel_y_g", "accel_z_g"]
GYRO_COLUMNS = ["gyro_x_dps", "gyro_y_dps", "gyro_z_dps"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="*", type=Path, help="One or more MPU CSV files")
    parser.add_argument("--plus-x", type=Path)
    parser.add_argument("--minus-x", type=Path)
    parser.add_argument("--plus-y", type=Path)
    parser.add_argument("--minus-y", type=Path)
    parser.add_argument("--plus-z", type=Path)
    parser.add_argument("--minus-z", type=Path)
    return parser.parse_args()


def load_columns(path: Path) -> dict[str, list[float]]:
    values = {name: [] for name in ACCEL_COLUMNS + GYRO_COLUMNS}
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        missing = set(values) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        for line_number, row in enumerate(reader, 2):
            try:
                for name in values:
                    values[name].append(float(row[name]))
            except (TypeError, ValueError) as error:
                raise ValueError(f"{path}:{line_number}: invalid numeric value") from error
    if not values[ACCEL_COLUMNS[0]]:
        raise ValueError(f"{path}: no samples")
    return values


def stats(values: list[float]) -> tuple[int, float, float, float, float, float, float]:
    mean = statistics.fmean(values)
    deviation = statistics.stdev(values) if len(values) > 1 else 0.0
    minimum = min(values)
    maximum = max(values)
    rms = math.sqrt(statistics.fmean(value * value for value in values))
    return len(values), mean, deviation, minimum, maximum, maximum - minimum, rms


def report_file(path: Path) -> None:
    columns = load_columns(path)
    print(f"\n{path}")
    print("axis                 count          mean       std_dev           min           max          p2p           rms")
    for name in ACCEL_COLUMNS + GYRO_COLUMNS:
        count, mean, deviation, minimum, maximum, peak_to_peak, rms = stats(columns[name])
        print(f"{name:20} {count:7d} {mean:13.6f} {deviation:13.6f} {minimum:13.6f} "
              f"{maximum:13.6f} {peak_to_peak:13.6f} {rms:13.6f}")


def report_six_position(args: argparse.Namespace) -> None:
    pairs = {
        "x": (args.plus_x, args.minus_x, "accel_x_g"),
        "y": (args.plus_y, args.minus_y, "accel_y_g"),
        "z": (args.plus_z, args.minus_z, "accel_z_g"),
    }
    supplied = [path for plus, minus, _ in pairs.values() for path in (plus, minus) if path]
    if not supplied:
        return
    if len(supplied) != 6:
        raise ValueError("six-position estimate requires all --plus/--minus X/Y/Z files")

    print("\nSix-position estimates (measured data only; not applied to firmware)")
    print("axis        plus_mean_g  minus_mean_g    bias_g  sensitivity_g_per_g  correction_gain")
    for axis, (plus_path, minus_path, column) in pairs.items():
        plus_mean = statistics.fmean(load_columns(plus_path)[column])
        minus_mean = statistics.fmean(load_columns(minus_path)[column])
        bias = (plus_mean + minus_mean) / 2.0
        sensitivity = (plus_mean - minus_mean) / 2.0
        correction = math.nan if sensitivity == 0.0 else 1.0 / sensitivity
        print(f"{axis:4} {plus_mean:18.9f} {minus_mean:13.9f} {bias:11.9f} "
              f"{sensitivity:20.9f} {correction:16.9f}")


def main() -> int:
    args = parse_args()
    if not args.csv and not any((args.plus_x, args.minus_x, args.plus_y, args.minus_y, args.plus_z, args.minus_z)):
        print("provide CSV files or all six-position options", file=sys.stderr)
        return 2
    try:
        for path in args.csv:
            report_file(path)
        report_six_position(args)
    except (OSError, ValueError) as error:
        print(f"analysis failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
