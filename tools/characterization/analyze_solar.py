#!/usr/bin/env python3
"""Report descriptive statistics for measured solar characterization CSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import statistics
import sys


def percentile(sorted_values: list[float], percent: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * percent / 100.0
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return sorted_values[lower] * (1.0 - fraction) + sorted_values[upper] * fraction


def load(path: Path) -> list[float]:
    values: list[float] = []
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if "solar_voltage_mV" not in (reader.fieldnames or []):
            raise ValueError(f"{path}: missing solar_voltage_mV")
        for line_number, row in enumerate(reader, 2):
            try:
                values.append(float(row["solar_voltage_mV"]))
            except (TypeError, ValueError) as error:
                raise ValueError(f"{path}:{line_number}: invalid solar_voltage_mV") from error
    if not values:
        raise ValueError(f"{path}: no samples")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="+", type=Path, help="CSV files, e.g. covered.csv indoor.csv")
    args = parser.parse_args()
    print("file,count,mean_mV,median_mV,std_dev_mV,min_mV,p05_mV,p25_mV,p75_mV,p95_mV,max_mV")
    try:
        for path in args.csv:
            values = sorted(load(path))
            deviation = statistics.stdev(values) if len(values) > 1 else 0.0
            print(f"{path},{len(values)},{statistics.fmean(values):.3f},{statistics.median(values):.3f},"
                  f"{deviation:.3f},{values[0]:.3f},{percentile(values, 5):.3f},"
                  f"{percentile(values, 25):.3f},{percentile(values, 75):.3f},"
                  f"{percentile(values, 95):.3f},{values[-1]:.3f}")
    except (OSError, ValueError) as error:
        print(f"analysis failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
