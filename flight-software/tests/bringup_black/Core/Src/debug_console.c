#include "debug_console.h"

#include <limits.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

#define CONSOLE_TX_BUFFER_SIZE 2048U
#define DASHBOARD_CONTENT_WIDTH 68

typedef struct {
    uint8_t buffer[CONSOLE_TX_BUFFER_SIZE];
    volatile uint16_t head;
    volatile uint16_t tail;
    volatile uint16_t active_length;
    volatile bool busy;
    uint32_t dropped_messages;
    volatile uint32_t tx_errors;
} ConsoleTxState;

static UART_HandleTypeDef *console_uart;
static ConsoleTxState tx;
static char telemetry_line[320];

static void StartTransmission(void) {
    uint16_t length;

    if ((console_uart == NULL) || tx.busy || (tx.head == tx.tail)) {
        return;
    }
    length = tx.head > tx.tail ? (uint16_t)(tx.head - tx.tail)
                               : (uint16_t)(CONSOLE_TX_BUFFER_SIZE - tx.tail);
    tx.active_length = length;
    tx.busy = true;
    if (HAL_UART_Transmit_IT(console_uart, &tx.buffer[tx.tail], length) != HAL_OK) {
        tx.active_length = 0U;
        tx.busy = false;
    }
}

static void SendDashboardBorder(void) {
    (void)DebugConsole_Write("+----------------------------------------------------------------------+\r\n");
}

static void SendDashboardLine(const char *format, ...) {
    char content[DASHBOARD_CONTENT_WIDTH + 1U];
    va_list arguments;

    va_start(arguments, format);
    (void)vsnprintf(content, sizeof(content), format, arguments);
    va_end(arguments);
    (void)snprintf(telemetry_line,
                   sizeof(telemetry_line),
                   "| %-*.*s |\r\n",
                   DASHBOARD_CONTENT_WIDTH,
                   DASHBOARD_CONTENT_WIDTH,
                   content);
    (void)DebugConsole_Write(telemetry_line);
}

static void FormatCoordinate(char *buffer, size_t capacity, int32_t coordinate_deg_e7) {
    const int64_t signed_value = coordinate_deg_e7;
    const uint64_t magnitude = signed_value < 0 ? (uint64_t)(-signed_value) : (uint64_t)signed_value;

    (void)snprintf(buffer,
                   capacity,
                   "%c%lu.%07lu",
                   signed_value < 0 ? '-' : '+',
                   (unsigned long)(magnitude / 10000000ULL),
                   (unsigned long)(magnitude % 10000000ULL));
}

static const char *SensorHealthText(SensorHealth health) {
    switch (health) {
        case SENSOR_HEALTH_OK:
            return "OK";
        case SENSOR_HEALTH_DEGRADED:
            return "DEGRADED";
        case SENSOR_HEALTH_RECOVERING:
            return "RECOVERING";
        case SENSOR_HEALTH_UNAVAILABLE:
        default:
            return "UNAVAILABLE";
    }
}

static const char *SensorErrorText(SensorError error) {
    switch (error) {
        case SENSOR_ERROR_NONE:
            return "NONE";
        case SENSOR_ERROR_READ:
            return "READ";
        case SENSOR_ERROR_NACK:
            return "NACK";
        case SENSOR_ERROR_TIMEOUT:
            return "TIMEOUT";
        case SENSOR_ERROR_BUS:
            return "BUS";
        case SENSOR_ERROR_ARBITRATION_LOST:
            return "ARLO";
        case SENSOR_ERROR_IDENTITY:
            return "WHO_AM_I";
        case SENSOR_ERROR_INIT:
        default:
            return "INIT";
    }
}

static const char *I2cHealthText(I2cBusHealth health) {
    switch (health) {
        case I2C_BUS_HEALTH_OK:
            return "OK";
        case I2C_BUS_HEALTH_DEGRADED:
            return "DEGRADED";
        case I2C_BUS_HEALTH_RECOVERING:
        default:
            return "RECOVERING";
    }
}

static const char *I2cHalErrorText(uint32_t error) {
    if ((error & HAL_I2C_ERROR_TIMEOUT) != 0U) {
        return "TIMEOUT";
    }
    if ((error & HAL_I2C_ERROR_BERR) != 0U) {
        return "BERR";
    }
    if ((error & HAL_I2C_ERROR_ARLO) != 0U) {
        return "ARLO";
    }
    if ((error & HAL_I2C_ERROR_AF) != 0U) {
        return "NACK";
    }
    return "NONE";
}

static const char *I2cLastErrorText(const I2cBusStatus *status) {
    switch (status->last_stuck_state) {
        case I2C_STUCK_SDA:
            return "SDA_STUCK";
        case I2C_STUCK_SCL:
            return "SCL_STUCK";
        case I2C_STUCK_BOTH:
            return "BOTH_STUCK";
        case I2C_STUCK_NONE:
        default:
            return I2cHalErrorText(status->last_hal_error);
    }
}

void DebugConsole_Init(UART_HandleTypeDef *uart) {
    console_uart = uart;
}

void DebugConsole_Process(void) {
    StartTransmission();
}

HAL_StatusTypeDef DebugConsole_Write(const char *message) {
    size_t length;
    uint16_t free_space;
    uint16_t head;

    if (message == NULL) {
        return HAL_ERROR;
    }
    length = strlen(message);
    if (length >= CONSOLE_TX_BUFFER_SIZE) {
        return HAL_ERROR;
    }

    head = tx.head;
    free_space = head >= tx.tail ? (uint16_t)((CONSOLE_TX_BUFFER_SIZE - head) + tx.tail - 1U)
                                 : (uint16_t)(tx.tail - head - 1U);
    if (length > free_space) {
        if (tx.dropped_messages < UINT32_MAX) {
            ++tx.dropped_messages;
        }
        return HAL_BUSY;
    }

    for (size_t index = 0U; index < length; ++index) {
        tx.buffer[head] = (uint8_t)message[index];
        head = (uint16_t)((head + 1U) % CONSOLE_TX_BUFFER_SIZE);
    }
    tx.head = head;
    StartTransmission();
    return HAL_OK;
}

bool DebugConsole_ReadCommand(uint8_t *command) {
    return (command != NULL) && (HAL_UART_Receive(console_uart, command, 1U, 0U) == HAL_OK);
}

void DebugConsole_ShowDashboard(const FlightDataSnapshot *data,
                                const I2cBusStatus *i2c_status,
                                bool rtc_time_valid,
                                RTC_HandleTypeDef *rtc) {
    static bool dashboard_started;
    RTC_TimeTypeDef rtc_time;
    RTC_DateTypeDef rtc_date;
    HAL_StatusTypeDef rtc_status = HAL_ERROR;
    char rtc_text[16] = "NOT SET";
    char temperature_text[20] = "STALE";
    char pressure_text[20] = "INVALID";
    char reference_text[20] = "NOT SET";
    char altitude_text[20] = "INVALID";
    char gps_status[16] = "NO DATA";
    char satellites_text[8] = "--";
    char latitude_text[20] = "--";
    char longitude_text[20] = "--";
    char gps_altitude_text[20] = "--";
    char gps_utc_text[16] = "--";
    char battery_text[20] = "INVALID";
    char current_text[20] = "INVALID";
    char solar_text[20] = "INVALID";

    if ((data == NULL) || (i2c_status == NULL) || (rtc == NULL)) {
        return;
    }
    if (!dashboard_started) {
        /* Dashboard mode hides the cursor; "\033[?25h" restores it. */
        (void)DebugConsole_Write("\033[2J\033[H\033[?25l");
        dashboard_started = true;
    } else {
        (void)DebugConsole_Write("\033[H");
    }

    if (rtc_time_valid) {
        rtc_status = HAL_RTC_GetTime(rtc, &rtc_time, RTC_FORMAT_BIN);
        if (rtc_status == HAL_OK) {
            rtc_status = HAL_RTC_GetDate(rtc, &rtc_date, RTC_FORMAT_BIN);
        }
    }
    if (rtc_status == HAL_OK) {
        (void)snprintf(rtc_text, sizeof(rtc_text), "%02u:%02u:%02u", rtc_time.Hours, rtc_time.Minutes, rtc_time.Seconds);
    }

    if (data->environment_temperature_fresh) {
        const int32_t centi_c = (int32_t)(data->environment_temperature_c * 100.0f);
        const int64_t signed_temperature = centi_c;
        const uint64_t magnitude = signed_temperature < 0 ? (uint64_t)(-signed_temperature)
                                                          : (uint64_t)signed_temperature;
        (void)snprintf(temperature_text,
                       sizeof(temperature_text),
                       "%c%lu.%02lu C",
                       signed_temperature < 0 ? '-' : '+',
                       (unsigned long)(magnitude / 100U),
                       (unsigned long)(magnitude % 100U));
    } else if (!data->environment_temperature_available) {
        (void)snprintf(temperature_text, sizeof(temperature_text), "UNAVAILABLE");
    }

    if (data->pressure_fresh) {
        (void)snprintf(pressure_text,
                       sizeof(pressure_text),
                       "%lu.%02lu hPa",
                       (unsigned long)(data->pressure_pa / 100U),
                       (unsigned long)(data->pressure_pa % 100U));
    } else if (!data->pressure_available) {
        (void)snprintf(pressure_text, sizeof(pressure_text), "UNAVAILABLE");
    } else if (data->pressure_valid) {
        (void)snprintf(pressure_text, sizeof(pressure_text), "STALE");
    }

    if (data->altitude_reference_valid) {
        (void)snprintf(reference_text,
                       sizeof(reference_text),
                       "%lu.%02lu hPa",
                       (unsigned long)(data->altitude_reference_pressure_pa / 100U),
                       (unsigned long)(data->altitude_reference_pressure_pa % 100U));
    }
    if (data->altitude_valid) {
        const int32_t altitude_cm = (int32_t)(data->altitude_m * 100.0f);
        const int64_t signed_altitude = altitude_cm;
        const uint64_t magnitude = signed_altitude < 0 ? (uint64_t)(-signed_altitude)
                                                       : (uint64_t)signed_altitude;
        (void)snprintf(altitude_text,
                       sizeof(altitude_text),
                       "%c%lu.%02lu m",
                       signed_altitude < 0 ? '-' : '+',
                       (unsigned long)(magnitude / 100U),
                       (unsigned long)(magnitude % 100U));
    } else if (!data->altitude_reference_valid) {
        (void)snprintf(altitude_text, sizeof(altitude_text), "NOT SET");
    } else if (!data->pressure_available) {
        (void)snprintf(altitude_text, sizeof(altitude_text), "UNAVAILABLE");
    } else if (data->pressure_valid) {
        (void)snprintf(altitude_text, sizeof(altitude_text), "STALE");
    }

    if (data->gps_uart_active) {
        if (!data->gps_data_fresh) {
            (void)snprintf(gps_status, sizeof(gps_status), "STALE");
        } else {
            (void)snprintf(satellites_text, sizeof(satellites_text), "%u", data->gps.satellites);
            if (data->gps.utc_valid) {
                (void)snprintf(gps_utc_text,
                               sizeof(gps_utc_text),
                               "%02u:%02u:%02u",
                               data->gps.utc_hours,
                               data->gps.utc_minutes,
                               data->gps.utc_seconds);
            }
            if (!data->gps.fix_valid) {
                (void)snprintf(gps_status, sizeof(gps_status), "NO FIX");
            } else {
                const int64_t altitude_mm = data->gps.altitude_mm;
                const uint64_t magnitude = altitude_mm < 0 ? (uint64_t)(-altitude_mm) : (uint64_t)altitude_mm;
                (void)snprintf(gps_status, sizeof(gps_status), "FIX");
                FormatCoordinate(latitude_text, sizeof(latitude_text), data->gps.latitude_deg_e7);
                FormatCoordinate(longitude_text, sizeof(longitude_text), data->gps.longitude_deg_e7);
                (void)snprintf(gps_altitude_text,
                               sizeof(gps_altitude_text),
                               "%c%lu.%01lu m",
                               altitude_mm < 0 ? '-' : '+',
                               (unsigned long)(magnitude / 1000ULL),
                               (unsigned long)((magnitude % 1000ULL) / 100ULL));
            }
        }
    }

    if (data->power_fresh) {
        const int64_t signed_current = data->battery_current_mA;
        const uint64_t magnitude = signed_current < 0 ? (uint64_t)(-signed_current)
                                                      : (uint64_t)signed_current;
        (void)snprintf(battery_text,
                       sizeof(battery_text),
                       "%ld.%03ld V",
                       (long)(data->battery_voltage_mV / 1000),
                       (long)(data->battery_voltage_mV % 1000));
        (void)snprintf(current_text,
                       sizeof(current_text),
                       "%c%lu.%03lu A",
                       signed_current < 0 ? '-' : '+',
                       (unsigned long)(magnitude / 1000U),
                       (unsigned long)(magnitude % 1000U));
        (void)snprintf(solar_text,
                       sizeof(solar_text),
                       "%ld.%03ld V",
                       (long)(data->solar_voltage_mV / 1000),
                       (long)(data->solar_voltage_mV % 1000));
    } else if (!data->power_available) {
        (void)snprintf(battery_text, sizeof(battery_text), "UNAVAILABLE");
        (void)snprintf(current_text, sizeof(current_text), "UNAVAILABLE");
        (void)snprintf(solar_text, sizeof(solar_text), "UNAVAILABLE");
    } else if (data->power_valid) {
        (void)snprintf(battery_text, sizeof(battery_text), "STALE");
        (void)snprintf(current_text, sizeof(current_text), "STALE");
        (void)snprintf(solar_text, sizeof(solar_text), "STALE");
    }

    SendDashboardBorder();
    SendDashboardLine("ASTRA FLIGHT COMPUTER");
    SendDashboardBorder();
    SendDashboardLine("SYSTEM");
    SendDashboardLine("RTC          %-20s STATUS       RUNNING", rtc_text);
    SendDashboardLine("I2C %-10s ERR %-6lu ATT %-5u OK %-5u LAST %s",
                      I2cHealthText(i2c_status->health),
                      (unsigned long)i2c_status->total_bus_errors,
                      i2c_status->recovery_attempt_count,
                      i2c_status->recovery_success_count,
                      I2cLastErrorText(i2c_status));
    SendDashboardLine("BMP %-11s ERR %-10lu ATT %-5u OK %-5u INIT %-5u",
                      SensorHealthText(data->bmp280_health.health),
                      (unsigned long)data->bmp280_health.total_read_errors,
                      data->bmp280_health.recovery_attempt_count,
                      data->bmp280_health.recovery_success_count,
                      data->bmp280_health.initialization_failures);
    SendDashboardLine("INA %-11s ERR %-10lu ATT %-5u OK %-5u INIT %-5u",
                      SensorHealthText(data->ina3221_health.health),
                      (unsigned long)data->ina3221_health.total_read_errors,
                      data->ina3221_health.recovery_attempt_count,
                      data->ina3221_health.recovery_success_count,
                      data->ina3221_health.initialization_failures);
    SendDashboardBorder();
    SendDashboardLine("ENVIRONMENT");
    SendDashboardLine("DS18B20      %-20s P0           %s", temperature_text, reference_text);
    SendDashboardLine("BMP280       %-20s ALTITUDE     %s", pressure_text, altitude_text);
    SendDashboardBorder();
    SendDashboardLine("IMU - MPU6500                  STATUS       %s",
                      SensorHealthText(data->mpu6500_health.health));
    if (data->imu_fresh) {
        SendDashboardLine("ACCEL        X:%+7d      Y:%+7d      Z:%+7d",
                          data->imu_raw.accel_x,
                          data->imu_raw.accel_y,
                          data->imu_raw.accel_z);
        SendDashboardLine("GYRO         X:%+7d      Y:%+7d      Z:%+7d",
                          data->imu_raw.gyro_x,
                          data->imu_raw.gyro_y,
                          data->imu_raw.gyro_z);
    } else {
        SendDashboardLine("ACCEL        --");
        SendDashboardLine("GYRO         --");
    }
    SendDashboardLine("READS %lu ERR %lu C %u ATT %u OK %u INIT %u LAST %s",
                      (unsigned long)data->mpu6500_health.total_reads,
                      (unsigned long)data->mpu6500_health.total_read_errors,
                      data->mpu6500_health.consecutive_errors,
                      data->mpu6500_health.recovery_attempt_count,
                      data->mpu6500_health.recovery_success_count,
                      data->mpu6500_health.initialization_failures,
                      SensorErrorText(data->mpu6500_health.last_error));
    SendDashboardBorder();
    SendDashboardLine("GPS");
    SendDashboardLine("STATUS       %-20s SATELLITES   %s", gps_status, satellites_text);
    SendDashboardLine("LAT          %-20s LON          %s", latitude_text, longitude_text);
    SendDashboardLine("GPS ALT      %-20s GPS UTC      %s", gps_altitude_text, gps_utc_text);
    SendDashboardBorder();
    SendDashboardLine("POWER - INA3221                  SOLAR        %s", solar_text);
    SendDashboardLine("BATTERY      %-20s CURRENT      %s", battery_text, current_text);
    SendDashboardBorder();
}

void DebugConsole_TxComplete(UART_HandleTypeDef *uart) {
    if (uart != console_uart) {
        return;
    }
    tx.tail = (uint16_t)((tx.tail + tx.active_length) % CONSOLE_TX_BUFFER_SIZE);
    tx.active_length = 0U;
    tx.busy = false;
    StartTransmission();
}

void DebugConsole_UartError(UART_HandleTypeDef *uart) {
    if (uart != console_uart) {
        return;
    }
    tx.tail = tx.head;
    tx.active_length = 0U;
    tx.busy = false;
    if (tx.tx_errors < UINT32_MAX) {
        ++tx.tx_errors;
    }
}
