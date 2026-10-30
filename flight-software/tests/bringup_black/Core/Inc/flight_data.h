#ifndef FLIGHT_DATA_H
#define FLIGHT_DATA_H

#include "mpu6500.h"
#include "neo6m.h"

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    SENSOR_HEALTH_OK,
    SENSOR_HEALTH_DEGRADED,
    SENSOR_HEALTH_RECOVERING,
    SENSOR_HEALTH_UNAVAILABLE
} SensorHealth;

typedef enum {
    SENSOR_ERROR_NONE,
    SENSOR_ERROR_READ,
    SENSOR_ERROR_NACK,
    SENSOR_ERROR_TIMEOUT,
    SENSOR_ERROR_BUS,
    SENSOR_ERROR_ARBITRATION_LOST,
    SENSOR_ERROR_IDENTITY,
    SENSOR_ERROR_INIT
} SensorError;

typedef struct {
    SensorHealth health;
    SensorError last_error;
    uint8_t consecutive_errors;
    uint16_t recovery_attempt_count;
    uint16_t recovery_success_count;
    uint16_t initialization_failures;
    uint32_t total_reads;
    uint32_t total_read_errors;
    uint32_t last_hal_error;
} SensorHealthSnapshot;

typedef struct {
    uint32_t timestamp_ms;

    uint32_t pressure_pa;
    float altitude_m;
    float environment_temperature_c;
    MPU6500_RawData imu_raw;
    NEO6M_Data gps;
    int32_t battery_voltage_mV;
    int32_t battery_current_mA;
    int32_t solar_voltage_mV;

    uint32_t altitude_reference_pressure_pa;
    bool altitude_reference_valid;
    bool pressure_available;
    bool pressure_valid;
    bool pressure_fresh;
    bool altitude_valid;
    bool environment_temperature_available;
    bool environment_temperature_valid;
    bool environment_temperature_fresh;
    bool imu_available;
    bool imu_valid;
    bool imu_fresh;
    bool gps_uart_active;
    bool gps_data_fresh;
    bool power_available;
    bool power_valid;
    bool power_fresh;

    /* TBR: no threshold is asserted until panel characterization is complete. */
    bool solar_present;
    bool solar_present_valid;

    SensorHealthSnapshot bmp280_health;
    SensorHealthSnapshot mpu6500_health;
    SensorHealthSnapshot ina3221_health;
} FlightDataSnapshot;

#endif /* FLIGHT_DATA_H */
