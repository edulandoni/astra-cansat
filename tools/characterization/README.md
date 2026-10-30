# ASTRA characterization tools

These tools capture measured MPU6500 and solar-panel data without changing the
flight application. No calibration constants, solar thresholds, or hysteresis
values are selected here.

## Build and flash the experimental firmware

From `flight-software/tests/characterization_firmware`:

```text
cmake --preset mpu
cmake --build --preset mpu

cmake --preset solar
cmake --build --preset solar
```

Flash the required `build/<target>/characterization.elf` with the normal STM32
programmer/debugger. Both targets reuse the Flight Computer startup, clocks,
pinout, I2C setup, USART2 setup, and existing sensor driver. USART2 output is
115200 baud, 8-N-1. A sensor initialization failure intentionally produces no
CSV rows; investigate wiring/power rather than recording an empty trial.

## Capture

Install the only non-standard Python dependency:

```text
python -m pip install pyserial
```

Examples (replace the port and filenames):

```text
python tools/characterization/capture_serial.py --port COM7 --baud 115200 --schema mpu --output data/mpu_plus_x.csv --host-timestamp
python tools/characterization/capture_serial.py --port COM7 --baud 115200 --schema solar --output data/solar_covered.csv --host-timestamp
```

Stop with Ctrl+C. The logger validates column count and numeric fields, flushes
each accepted sample, and closes the serial port and CSV cleanly.

MPU CSV columns:

```text
sample,timestamp_ms,accel_raw_x,accel_raw_y,accel_raw_z,accel_x_g,accel_y_g,accel_z_g,gyro_raw_x,gyro_raw_y,gyro_raw_z,gyro_x_dps,gyro_y_dps,gyro_z_dps
```

Solar CSV columns:

```text
sample,timestamp_ms,solar_voltage_mV,battery_voltage_mV
```

`host_timestamp_utc` is appended only when `--host-timestamp` is used.

## Physical test record

For every CSV, record the hardware serial/revision, firmware Git commit, fixture
and orientation, condition name, start/end time and duration, supply/battery
state, ambient temperature if available, operator, and any motion/disturbance.
Use separate stationary MPU runs for +X, -X, +Y, -Y, +Z, -Z and gyro bias.
For a gyro scale-factor run, also record the independent angular-rate reference
and its uncertainty. Suggested solar condition names are `covered`, `indoor`,
`window`, `flashlight`, and `sun`; these are labels, not automatic classes.

## Analyze measured data

```text
python tools/characterization/analyze_mpu.py data/mpu_stationary.csv
python tools/characterization/analyze_mpu.py --plus-x data/mpu_plus_x.csv --minus-x data/mpu_minus_x.csv --plus-y data/mpu_plus_y.csv --minus-y data/mpu_minus_y.csv --plus-z data/mpu_plus_z.csv --minus-z data/mpu_minus_z.csv
python tools/characterization/analyze_solar.py data/solar_covered.csv data/solar_indoor.csv data/solar_sun.csv
```

The six-position calculation reports estimates from the supplied measurements;
it does not write constants or modify firmware.

## Host logic test

```text
cmake -S tools/characterization -B tools/characterization/build
cmake --build tools/characterization/build
ctest --test-dir tools/characterization/build --output-on-failure
```

The tested hysteresis helper takes both thresholds as arguments. It is not
linked to the Flight Computer. Threshold selection remains TBR pending measured
solar data.
