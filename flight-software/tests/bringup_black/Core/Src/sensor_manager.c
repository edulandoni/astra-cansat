#include "sensor_manager.h"

#include "altitude.h"
#include "bmp280.h"
#include "ds18b20.h"
#include "flight_config.h"
#include "i2c_bus_manager.h"
#include "ina3221.h"
#include "mpu6500.h"
#include "neo6m.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    SensorHealth health;
    SensorError last_error;
    uint8_t consecutive_errors;
    bool recovery_pending;
    uint16_t recovery_attempt_count;
    uint16_t recovery_success_count;
    uint16_t initialization_failures;
    uint32_t total_reads;
    uint32_t total_read_errors;
    uint32_t last_update_ms;
    uint32_t last_error_ms;
    uint32_t last_hal_error;
    uint32_t last_init_attempt_ms;
} SensorState;

typedef enum {
    DS18B20_STATE_IDLE,
    DS18B20_STATE_CONVERTING
} Ds18b20ConversionState;

typedef struct {
    float temperature_c;
    bool initialized;
    bool available;
    bool valid;
    uint32_t last_update_ms;
    uint32_t conversion_start_ms;
    Ds18b20ConversionState conversion_state;
} Ds18b20State;

typedef enum {
    MPU6500_INIT_IDLE,
    MPU6500_INIT_WAITING
} Mpu6500InitializationState;

typedef struct {
    SensorState common;
    MPU6500_RawData data;
    bool available;
    bool valid;
    bool report_init_result;
    uint8_t who_am_i;
    uint32_t first_error_ms;
    uint32_t first_hal_error;
    uint32_t initialization_start_ms;
    Mpu6500InitializationState initialization_state;
} Mpu6500State;

typedef struct {
    NEO6M_Data data;
    bool data_available;
    bool data_fresh;
    bool uart_active;
} GpsState;

typedef enum {
    ALTITUDE_CALIBRATION_IDLE,
    ALTITUDE_CALIBRATION_RUNNING
} AltitudeCalibrationPhase;

typedef struct {
    AltitudeCalibrationPhase phase;
    uint64_t pressure_sum;
    uint32_t valid_samples;
    uint32_t sample_count;
    uint32_t last_sample_ms;
} AltitudeCalibrationState;

static I2C_HandleTypeDef *i2c_bus;
static RTC_HandleTypeDef *rtc;
static SensorManagerMessageSink report_message;
static Altitude_Reference altitude_reference;
static AltitudeCalibrationState altitude_calibration;
static BMP280_Data bmp280_data;
static SensorState bmp280;
static bool bmp280_available;
static bool bmp280_valid;
static Ds18b20State ds18b20;
static GpsState gps;
static INA3221_Handle ina3221;
static SensorState ina3221_health;
static Mpu6500State mpu6500;

static void IncrementUint16Saturated(uint16_t *counter) {
    if (*counter < UINT16_MAX) {
        ++(*counter);
    }
}

static void ReportMessage(const char *message) {
    if (report_message != NULL) {
        report_message(message);
    }
}

static void IncrementUint32Saturated(uint32_t *counter) {
    if (*counter < UINT32_MAX) {
        ++(*counter);
    }
}

static bool DataIsFresh(bool valid, uint32_t last_update_ms, uint32_t now_ms) {
    return valid && ((now_ms - last_update_ms) <= SENSOR_DATA_MAX_AGE_MS);
}

static SensorError ClassifyI2cError(uint32_t hal_error, SensorError fallback_error) {
    if ((hal_error & HAL_I2C_ERROR_TIMEOUT) != 0U) {
        return SENSOR_ERROR_TIMEOUT;
    }
    if ((hal_error & HAL_I2C_ERROR_BERR) != 0U) {
        return SENSOR_ERROR_BUS;
    }
    if ((hal_error & HAL_I2C_ERROR_ARLO) != 0U) {
        return SENSOR_ERROR_ARBITRATION_LOST;
    }
    if ((hal_error & HAL_I2C_ERROR_AF) != 0U) {
        return SENSOR_ERROR_NACK;
    }
    return fallback_error;
}

static void SetLastError(SensorState *sensor,
                         SensorError fallback_error,
                         I2cFaultSource source,
                         uint32_t now_ms) {
    sensor->last_hal_error = HAL_I2C_GetError(i2c_bus);
    sensor->last_error = ClassifyI2cError(sensor->last_hal_error, fallback_error);
    sensor->last_error_ms = now_ms;
    I2cBusManager_RecordFault(source, sensor->last_hal_error, now_ms);
}

static bool InitializeBmp280(bool report_result, bool recovery_attempt, uint32_t now_ms) {
    bmp280.last_init_attempt_ms = now_ms;
    bmp280_valid = false;
    if (recovery_attempt) {
        IncrementUint16Saturated(&bmp280.recovery_attempt_count);
        bmp280.recovery_pending = true;
        bmp280.health = SENSOR_HEALTH_RECOVERING;
    }
    bmp280_available = BMP280_Init(i2c_bus) == HAL_OK;

    if (bmp280_available) {
        bmp280.health = SENSOR_HEALTH_RECOVERING;
        bmp280.consecutive_errors = 0U;
    } else {
        bmp280.health = SENSOR_HEALTH_UNAVAILABLE;
        SetLastError(&bmp280, SENSOR_ERROR_INIT, I2C_FAULT_SOURCE_BMP280, now_ms);
        IncrementUint16Saturated(&bmp280.initialization_failures);
    }

    if (report_result) {
        ReportMessage(bmp280_available ? "BMP280 OK\r\n" : "BMP280 INIT FAIL\r\n");
    }
    return bmp280_available;
}

static bool InitializeMpu6500(bool report_result,
                              bool recovery_attempt,
                              bool perform_detection,
                              uint32_t now_ms) {
    uint8_t who_am_i = 0U;
    char message[64];

    mpu6500.common.last_init_attempt_ms = now_ms;
    mpu6500.valid = false;
    mpu6500.available = false;
    mpu6500.report_init_result = report_result;
    if (recovery_attempt) {
        IncrementUint16Saturated(&mpu6500.common.recovery_attempt_count);
        mpu6500.common.recovery_pending = true;
    }
    mpu6500.common.health = SENSOR_HEALTH_RECOVERING;
    mpu6500.initialization_state = MPU6500_INIT_IDLE;

    if (perform_detection) {
        if (MPU6500_Detect(i2c_bus, &who_am_i) != HAL_OK) {
            mpu6500.who_am_i = who_am_i;
            mpu6500.common.health = SENSOR_HEALTH_UNAVAILABLE;
            SetLastError(&mpu6500.common, SENSOR_ERROR_IDENTITY, I2C_FAULT_SOURCE_MPU6500, now_ms);
            IncrementUint16Saturated(&mpu6500.common.initialization_failures);
            if (report_result) {
                (void)snprintf(message, sizeof(message), "MPU6500 FAIL | WHO_AM_I=0x%02X\r\n", who_am_i);
                ReportMessage(message);
            }
            return false;
        }
        mpu6500.who_am_i = who_am_i;
    }

    if (MPU6500_BeginInitialization(i2c_bus) != HAL_OK) {
        mpu6500.common.health = SENSOR_HEALTH_UNAVAILABLE;
        SetLastError(&mpu6500.common, SENSOR_ERROR_INIT, I2C_FAULT_SOURCE_MPU6500, now_ms);
        IncrementUint16Saturated(&mpu6500.common.initialization_failures);
        return false;
    }

    mpu6500.initialization_start_ms = now_ms;
    mpu6500.initialization_state = MPU6500_INIT_WAITING;
    return true;
}

static void ServiceMpu6500Initialization(uint32_t now_ms) {
    char message[64];

    if ((mpu6500.initialization_state != MPU6500_INIT_WAITING) ||
        ((now_ms - mpu6500.initialization_start_ms) < MPU6500_STARTUP_TIME_MS)) {
        return;
    }

    mpu6500.initialization_state = MPU6500_INIT_IDLE;
    mpu6500.available = MPU6500_FinishInitialization(i2c_bus) == HAL_OK;
    if (!mpu6500.available) {
        mpu6500.valid = false;
        mpu6500.common.health = SENSOR_HEALTH_UNAVAILABLE;
        SetLastError(&mpu6500.common, SENSOR_ERROR_INIT, I2C_FAULT_SOURCE_MPU6500, now_ms);
        IncrementUint16Saturated(&mpu6500.common.initialization_failures);
    } else {
        mpu6500.common.consecutive_errors = 0U;
        mpu6500.common.health =
            mpu6500.common.recovery_pending ? SENSOR_HEALTH_RECOVERING : SENSOR_HEALTH_DEGRADED;
    }

    if (mpu6500.report_init_result) {
        (void)snprintf(message,
                       sizeof(message),
                       mpu6500.available ? "MPU6500 OK | WHO_AM_I=0x%02X\r\n"
                                         : "MPU6500 FAIL | WHO_AM_I=0x%02X\r\n",
                       mpu6500.who_am_i);
        ReportMessage(message);
        mpu6500.report_init_result = false;
    }
}

static bool InitializeIna3221(bool report_result, bool recovery_attempt, uint32_t now_ms) {
    HAL_StatusTypeDef init_status;
    char message[48];

    ina3221_health.last_init_attempt_ms = now_ms;
    if (recovery_attempt) {
        IncrementUint16Saturated(&ina3221_health.recovery_attempt_count);
        ina3221_health.recovery_pending = true;
        ina3221_health.health = SENSOR_HEALTH_RECOVERING;
    }
    init_status = recovery_attempt ? INA3221_Reinitialize(&ina3221, i2c_bus)
                                   : INA3221_Init(&ina3221, i2c_bus);
    if (init_status != HAL_OK) {
        ina3221_health.health = SENSOR_HEALTH_UNAVAILABLE;
        SetLastError(&ina3221_health, SENSOR_ERROR_INIT, I2C_FAULT_SOURCE_INA3221, now_ms);
        IncrementUint16Saturated(&ina3221_health.initialization_failures);
        if (report_result) {
            ReportMessage("INA3221 INIT FAIL\r\n");
        }
        return false;
    }

    ina3221_health.health = SENSOR_HEALTH_RECOVERING;
    ina3221_health.consecutive_errors = 0U;
    if (report_result) {
        (void)snprintf(message, sizeof(message), "INA3221 OK | ADDR=0x%02X\r\n", INA3221_GetAddress(&ina3221));
        ReportMessage(message);
    }
    return true;
}

static void ServiceDs18b20Conversion(uint32_t now_ms) {
    float temperature_c;

    if ((ds18b20.conversion_state != DS18B20_STATE_CONVERTING) ||
        ((now_ms - ds18b20.conversion_start_ms) < DS18B20_CONVERSION_TIME_MS)) {
        return;
    }

    ds18b20.conversion_state = DS18B20_STATE_IDLE;
    if (DS18B20_ReadConversion(&temperature_c) != HAL_OK) {
        ds18b20.available = false;
        ds18b20.valid = false;
        return;
    }
    ds18b20.temperature_c = temperature_c;
    ds18b20.available = true;
    ds18b20.valid = true;
    ds18b20.last_update_ms = now_ms;
}

static void CopyHealthSnapshot(const SensorState *source, SensorHealthSnapshot *destination) {
    destination->health = source->health;
    destination->last_error = source->last_error;
    destination->consecutive_errors = source->consecutive_errors;
    destination->recovery_attempt_count = source->recovery_attempt_count;
    destination->recovery_success_count = source->recovery_success_count;
    destination->initialization_failures = source->initialization_failures;
    destination->total_reads = source->total_reads;
    destination->total_read_errors = source->total_read_errors;
    destination->last_hal_error = source->last_hal_error;
}

void SensorManager_Init(I2C_HandleTypeDef *i2c,
                        RTC_HandleTypeDef *rtc_handle,
                        UART_HandleTypeDef *gps_uart,
                        SensorManagerMessageSink message_sink,
                        uint32_t now_ms) {
    i2c_bus = i2c;
    rtc = rtc_handle;
    report_message = message_sink;

    if (NEO6M_Init(gps_uart) != HAL_OK) {
        ReportMessage("GPS RX INIT FAIL\r\n");
    }
    if (DS18B20_Init() == HAL_OK) {
        ds18b20.initialized = true;
        ds18b20.conversion_state = DS18B20_STATE_IDLE;
    } else {
        ds18b20.available = false;
        ReportMessage("DWT INIT FAIL\r\n");
    }

    Altitude_LoadReference(rtc, &altitude_reference);
    (void)InitializeBmp280(true, false, now_ms);
    (void)InitializeMpu6500(true, false, true, now_ms);
    (void)InitializeIna3221(true, false, now_ms);
}

void SensorManager_ProcessContinuous(uint32_t now_ms) {
    NEO6M_Process();
    gps.data_available = NEO6M_GetData(&gps.data);
    gps.data_fresh = gps.data_available && NEO6M_IsDataFresh(&gps.data, now_ms, GPS_DATA_MAX_AGE_MS);
    gps.uart_active = NEO6M_IsUartActive(now_ms, GPS_DATA_MAX_AGE_MS);
    ServiceDs18b20Conversion(now_ms);
    ServiceMpu6500Initialization(now_ms);
}

bool SensorManager_UpdateBmp280(uint32_t now_ms) {
    BMP280_Data sample;

    if (!bmp280_available) {
        if ((now_ms - bmp280.last_init_attempt_ms) >= BMP280_REINIT_RETRY_PERIOD_MS) {
            (void)InitializeBmp280(false, true, now_ms);
        }
        return false;
    }

    if (BMP280_Read(i2c_bus, &sample) != HAL_OK) {
        bmp280_valid = false;
        bmp280.health = bmp280.recovery_pending ? SENSOR_HEALTH_RECOVERING : SENSOR_HEALTH_DEGRADED;
        IncrementUint32Saturated(&bmp280.total_read_errors);
        if (bmp280.consecutive_errors < UINT8_MAX) {
            ++bmp280.consecutive_errors;
        }
        SetLastError(&bmp280, SENSOR_ERROR_READ, I2C_FAULT_SOURCE_BMP280, now_ms);
        if (bmp280.consecutive_errors >= BMP280_MAX_CONSECUTIVE_ERRORS) {
            bmp280.health = SENSOR_HEALTH_RECOVERING;
            bmp280_available = false;
            (void)InitializeBmp280(false, true, now_ms);
        }
        return false;
    }

    bmp280_data = sample;
    bmp280_available = true;
    bmp280_valid = true;
    bmp280.health = SENSOR_HEALTH_OK;
    bmp280.consecutive_errors = 0U;
    bmp280.last_update_ms = now_ms;
    if (bmp280.recovery_pending) {
        IncrementUint16Saturated(&bmp280.recovery_success_count);
        bmp280.recovery_pending = false;
    }
    I2cBusManager_RecordValidTransaction(now_ms);
    return true;
}

void SensorManager_UpdateMpu6500(uint32_t now_ms) {
    MPU6500_RawData sample;
    uint8_t who_am_i = 0U;

    if (mpu6500.initialization_state == MPU6500_INIT_WAITING) {
        return;
    }
    if (!mpu6500.available) {
        if ((now_ms - mpu6500.common.last_init_attempt_ms) >= MPU6500_REINIT_RETRY_PERIOD_MS) {
            (void)InitializeMpu6500(false, true, true, now_ms);
        }
        return;
    }

    IncrementUint32Saturated(&mpu6500.common.total_reads);
    if (MPU6500_ReadRaw(i2c_bus, &sample) != HAL_OK) {
        mpu6500.valid = false;
        mpu6500.common.health =
            mpu6500.common.recovery_pending ? SENSOR_HEALTH_RECOVERING : SENSOR_HEALTH_DEGRADED;
        IncrementUint32Saturated(&mpu6500.common.total_read_errors);
        if (mpu6500.common.consecutive_errors < UINT8_MAX) {
            ++mpu6500.common.consecutive_errors;
        }
        SetLastError(&mpu6500.common, SENSOR_ERROR_READ, I2C_FAULT_SOURCE_MPU6500, now_ms);
        if (mpu6500.common.total_read_errors == 1U) {
            mpu6500.first_error_ms = now_ms;
            mpu6500.first_hal_error = mpu6500.common.last_hal_error;
        }
        if (mpu6500.common.consecutive_errors < MPU6500_MAX_CONSECUTIVE_ERRORS) {
            return;
        }
        if (MPU6500_Detect(i2c_bus, &who_am_i) == HAL_OK) {
            mpu6500.who_am_i = who_am_i;
            mpu6500.common.consecutive_errors = 0U;
            return;
        }

        mpu6500.who_am_i = who_am_i;
        mpu6500.common.health = SENSOR_HEALTH_RECOVERING;
        SetLastError(&mpu6500.common, SENSOR_ERROR_IDENTITY, I2C_FAULT_SOURCE_MPU6500, now_ms);
        /* WHO_AM_I was just attempted; do not repeat the same blocking probe. */
        (void)InitializeMpu6500(false, true, false, now_ms);
        return;
    }

    mpu6500.data = sample;
    mpu6500.available = true;
    mpu6500.valid = true;
    mpu6500.common.health = SENSOR_HEALTH_OK;
    mpu6500.common.consecutive_errors = 0U;
    mpu6500.common.last_update_ms = now_ms;
    if (mpu6500.common.recovery_pending) {
        IncrementUint16Saturated(&mpu6500.common.recovery_success_count);
        mpu6500.common.recovery_pending = false;
    }
    I2cBusManager_RecordValidTransaction(now_ms);
}

void SensorManager_UpdateIna3221(uint32_t now_ms) {
    if (!INA3221_IsReady(&ina3221)) {
        if ((now_ms - ina3221_health.last_init_attempt_ms) >= INA3221_REINIT_RETRY_PERIOD_MS) {
            (void)InitializeIna3221(false, true, now_ms);
        }
        return;
    }

    if (INA3221_Read(&ina3221, now_ms) != HAL_OK) {
        ina3221_health.health =
            ina3221_health.recovery_pending ? SENSOR_HEALTH_RECOVERING : SENSOR_HEALTH_DEGRADED;
        IncrementUint32Saturated(&ina3221_health.total_read_errors);
        if (ina3221_health.consecutive_errors < UINT8_MAX) {
            ++ina3221_health.consecutive_errors;
        }
        SetLastError(&ina3221_health, SENSOR_ERROR_READ, I2C_FAULT_SOURCE_INA3221, now_ms);
        if (ina3221_health.consecutive_errors >= INA3221_MAX_CONSECUTIVE_ERRORS) {
            ina3221_health.health = SENSOR_HEALTH_RECOVERING;
            INA3221_Invalidate(&ina3221);
            (void)InitializeIna3221(false, true, now_ms);
        }
        return;
    }

    ina3221_health.health = SENSOR_HEALTH_OK;
    ina3221_health.consecutive_errors = 0U;
    ina3221_health.last_update_ms = now_ms;
    if (ina3221_health.recovery_pending) {
        IncrementUint16Saturated(&ina3221_health.recovery_success_count);
        ina3221_health.recovery_pending = false;
    }
    I2cBusManager_RecordValidTransaction(now_ms);
}

void SensorManager_StartDs18b20Conversion(uint32_t now_ms) {
    if (!ds18b20.initialized || (ds18b20.conversion_state != DS18B20_STATE_IDLE)) {
        return;
    }
    if (DS18B20_StartConversion() != HAL_OK) {
        ds18b20.available = false;
        ds18b20.valid = false;
        return;
    }
    ds18b20.available = true;
    ds18b20.conversion_start_ms = now_ms;
    ds18b20.conversion_state = DS18B20_STATE_CONVERTING;
}

void SensorManager_StartAltitudeCalibration(void) {
    /* Repeating Z intentionally restarts the sample window from zero. */
    altitude_calibration.phase = ALTITUDE_CALIBRATION_RUNNING;
    altitude_calibration.pressure_sum = 0U;
    altitude_calibration.valid_samples = 0U;
    altitude_calibration.sample_count = 0U;
    altitude_calibration.last_sample_ms = 0U;
}

void SensorManager_ProcessAltitudeCalibrationSample(uint32_t now_ms, bool sample_valid) {
    uint32_t average_pressure_pa;
    HAL_StatusTypeDef save_status = HAL_ERROR;

    if (altitude_calibration.phase != ALTITUDE_CALIBRATION_RUNNING) {
        return;
    }
    altitude_calibration.last_sample_ms = now_ms;
    ++altitude_calibration.sample_count;
    if (sample_valid) {
        altitude_calibration.pressure_sum += bmp280_data.pressure_pa;
        ++altitude_calibration.valid_samples;
    }
    if (altitude_calibration.sample_count < ALTITUDE_CALIBRATION_SAMPLES) {
        return;
    }

    altitude_calibration.phase = ALTITUDE_CALIBRATION_IDLE;
    if (altitude_calibration.valid_samples >= ALTITUDE_CALIBRATION_MIN_SAMPLES) {
        average_pressure_pa =
            (uint32_t)(altitude_calibration.pressure_sum / altitude_calibration.valid_samples);
        save_status = Altitude_SaveReference(rtc, &altitude_reference, average_pressure_pa);
    }
    ReportMessage(save_status == HAL_OK ? "ALT ZERO OK\r\n" : "ALT ZERO FAIL\r\n");
}

void SensorManager_InvalidateI2cSensors(uint32_t now_ms) {
    BMP280_Invalidate();
    bmp280_available = false;
    bmp280_valid = false;
    bmp280.health = SENSOR_HEALTH_RECOVERING;
    bmp280.consecutive_errors = 0U;
    bmp280.last_init_attempt_ms = now_ms;

    mpu6500.available = false;
    mpu6500.valid = false;
    mpu6500.common.health = SENSOR_HEALTH_RECOVERING;
    mpu6500.common.consecutive_errors = 0U;
    mpu6500.initialization_state = MPU6500_INIT_IDLE;
    mpu6500.common.last_init_attempt_ms = now_ms;

    INA3221_Invalidate(&ina3221);
    ina3221_health.health = SENSOR_HEALTH_RECOVERING;
    ina3221_health.consecutive_errors = 0U;
    ina3221_health.last_init_attempt_ms = now_ms;
}

void SensorManager_GetFlightData(uint32_t now_ms, FlightDataSnapshot *snapshot) {
    bool pressure_fresh;

    if (snapshot == NULL) {
        return;
    }
    memset(snapshot, 0, sizeof(*snapshot));
    snapshot->timestamp_ms = now_ms;

    pressure_fresh = DataIsFresh(bmp280_valid, bmp280.last_update_ms, now_ms);
    snapshot->pressure_pa = bmp280_data.pressure_pa;
    snapshot->pressure_available = bmp280_available;
    snapshot->pressure_valid = bmp280_valid;
    snapshot->pressure_fresh = pressure_fresh;
    snapshot->altitude_reference_pressure_pa = altitude_reference.reference_pressure_pa;
    snapshot->altitude_reference_valid = altitude_reference.valid != 0U;
    snapshot->altitude_valid = pressure_fresh &&
        (Altitude_Calculate(&altitude_reference, bmp280_data.pressure_pa, &snapshot->altitude_m) == HAL_OK);

    snapshot->environment_temperature_c = ds18b20.temperature_c;
    snapshot->environment_temperature_available = ds18b20.available;
    snapshot->environment_temperature_valid = ds18b20.valid;
    snapshot->environment_temperature_fresh = DataIsFresh(ds18b20.valid, ds18b20.last_update_ms, now_ms);

    snapshot->imu_raw = mpu6500.data;
    snapshot->imu_available = mpu6500.available;
    snapshot->imu_valid = mpu6500.valid;
    snapshot->imu_fresh = DataIsFresh(mpu6500.valid, mpu6500.common.last_update_ms, now_ms);
    snapshot->gps = gps.data;
    snapshot->gps_uart_active = gps.uart_active;
    snapshot->gps_data_fresh = gps.data_fresh;

    snapshot->battery_voltage_mV = ina3221.data.battery_voltage_mV;
    snapshot->battery_current_mA = ina3221.data.battery_current_mA;
    snapshot->solar_voltage_mV = ina3221.data.solar_voltage_mV;
    snapshot->power_available = INA3221_IsReady(&ina3221);
    snapshot->power_valid = ina3221.data.valid;
    snapshot->power_fresh = INA3221_IsDataFresh(&ina3221, now_ms, INA3221_DATA_MAX_AGE_MS);
    snapshot->solar_present = false;
    snapshot->solar_present_valid = false;

    CopyHealthSnapshot(&bmp280, &snapshot->bmp280_health);
    CopyHealthSnapshot(&mpu6500.common, &snapshot->mpu6500_health);
    CopyHealthSnapshot(&ina3221_health, &snapshot->ina3221_health);
}

void SensorManager_GpsRxComplete(UART_HandleTypeDef *uart) {
    NEO6M_UART_RxCpltCallback(uart);
}

void SensorManager_GpsUartError(UART_HandleTypeDef *uart) {
    NEO6M_UART_ErrorCallback(uart);
}
