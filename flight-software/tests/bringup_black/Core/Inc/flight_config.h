#ifndef FLIGHT_CONFIG_H
#define FLIGHT_CONFIG_H

/* Cooperative scheduler periods. These values are hardware-validated. */
#define MPU6500_PERIOD_MS                  20U
#define BMP280_PERIOD_MS                  100U
#define INA3221_PERIOD_MS                 100U
#define DS18B20_PERIOD_MS                1000U
#define DEBUG_TELEMETRY_PERIOD_MS        1000U
#define STATUS_LED_PERIOD_MS             1000U

#define SENSOR_DATA_MAX_AGE_MS           2000U
#define GPS_DATA_MAX_AGE_MS              3000U

#define MPU6500_MAX_CONSECUTIVE_ERRORS      3U
#define MPU6500_REINIT_RETRY_PERIOD_MS     100U
#define BMP280_MAX_CONSECUTIVE_ERRORS       3U
#define BMP280_REINIT_RETRY_PERIOD_MS      100U
#define INA3221_MAX_CONSECUTIVE_ERRORS      3U
#define INA3221_REINIT_RETRY_PERIOD_MS     100U

#define I2C_RECOVERY_COOLDOWN_MS           100U
#define I2C_BUS_ERROR_WINDOW_MS            100U
#define I2C_BUS_ERROR_SOURCE_THRESHOLD       2U
#define I2C_STUCK_CONFIRMATION_MS             2U

#define ALTITUDE_CALIBRATION_SAMPLES        10U
#define ALTITUDE_CALIBRATION_MIN_SAMPLES     5U
#define RTC_INITIALIZED_MAGIC            0xA5A5U

/*
 * TBR: determine both thresholds from the planned panel characterization.
 * solar_present remains invalid until those values have experimental support.
 */
#define SOLAR_PRESENT_THRESHOLD_MV_TBR       0U
#define SOLAR_PRESENT_HYSTERESIS_MV_TBR      0U

#endif /* FLIGHT_CONFIG_H */
