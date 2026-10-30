#include "app.h"

#if defined(CHARACTERIZE_MPU)
#include "mpu6500.h"
#elif defined(CHARACTERIZE_SOLAR)
#include "ina3221.h"
#else
#error "Select CHARACTERIZE_MPU or CHARACTERIZE_SOLAR"
#endif

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define OUTPUT_TIMEOUT_MS 100U

static I2C_HandleTypeDef *test_i2c;
static UART_HandleTypeDef *output_uart;
static uint32_t sample_index;
static uint32_t last_sample_ms;
static bool ready;

#if defined(CHARACTERIZE_MPU)
#define SAMPLE_PERIOD_MS 20U
#define ACCEL_LSB_PER_G 16384LL
#define GYRO_LSB_PER_DPS 131LL

static uint32_t initialization_started_ms;
static bool initialization_waiting;
#else
#define SAMPLE_PERIOD_MS 100U
static INA3221_Handle ina3221;
#endif

static bool IsDue(uint32_t now_ms) {
    return (now_ms - last_sample_ms) >= SAMPLE_PERIOD_MS;
}

static void AdvanceSchedule(uint32_t now_ms) {
    last_sample_ms += SAMPLE_PERIOD_MS;
    if ((now_ms - last_sample_ms) >= SAMPLE_PERIOD_MS) {
        last_sample_ms = now_ms;
    }
}

static bool WriteLine(const char *line) {
    const size_t length = strlen(line);

    return (length <= UINT16_MAX) &&
           (HAL_UART_Transmit(output_uart, (uint8_t *)line, (uint16_t)length, OUTPUT_TIMEOUT_MS) == HAL_OK);
}

#if defined(CHARACTERIZE_MPU)
static void FormatScaled(char *buffer, size_t capacity, int16_t raw, int64_t divisor) {
    const int64_t scaled = ((int64_t)raw * 1000000LL) / divisor;
    const uint64_t magnitude = scaled < 0 ? (uint64_t)(-scaled) : (uint64_t)scaled;

    (void)snprintf(buffer,
                   capacity,
                   "%s%lu.%06lu",
                   scaled < 0 ? "-" : "",
                   (unsigned long)(magnitude / 1000000ULL),
                   (unsigned long)(magnitude % 1000000ULL));
}

static void FinishMpuInitialization(uint32_t now_ms) {
    if (!initialization_waiting ||
        ((now_ms - initialization_started_ms) < MPU6500_STARTUP_TIME_MS)) {
        return;
    }

    initialization_waiting = false;
    ready = MPU6500_FinishInitialization(test_i2c) == HAL_OK;
    if (ready) {
        last_sample_ms = now_ms - SAMPLE_PERIOD_MS;
        (void)WriteLine("sample,timestamp_ms,accel_raw_x,accel_raw_y,accel_raw_z,accel_x_g,accel_y_g,accel_z_g,gyro_raw_x,gyro_raw_y,gyro_raw_z,gyro_x_dps,gyro_y_dps,gyro_z_dps\r\n");
    }
}

static void CaptureMpu(uint32_t now_ms) {
    MPU6500_RawData data;
    char ax[20];
    char ay[20];
    char az[20];
    char gx[20];
    char gy[20];
    char gz[20];
    char line[256];

    if (!ready || !IsDue(now_ms)) {
        return;
    }
    AdvanceSchedule(now_ms);
    if (MPU6500_ReadRaw(test_i2c, &data) != HAL_OK) {
        return;
    }

    FormatScaled(ax, sizeof(ax), data.accel_x, ACCEL_LSB_PER_G);
    FormatScaled(ay, sizeof(ay), data.accel_y, ACCEL_LSB_PER_G);
    FormatScaled(az, sizeof(az), data.accel_z, ACCEL_LSB_PER_G);
    FormatScaled(gx, sizeof(gx), data.gyro_x, GYRO_LSB_PER_DPS);
    FormatScaled(gy, sizeof(gy), data.gyro_y, GYRO_LSB_PER_DPS);
    FormatScaled(gz, sizeof(gz), data.gyro_z, GYRO_LSB_PER_DPS);

    (void)snprintf(line,
                   sizeof(line),
                   "%lu,%lu,%d,%d,%d,%s,%s,%s,%d,%d,%d,%s,%s,%s\r\n",
                   (unsigned long)sample_index,
                   (unsigned long)now_ms,
                   data.accel_x,
                   data.accel_y,
                   data.accel_z,
                   ax,
                   ay,
                   az,
                   data.gyro_x,
                   data.gyro_y,
                   data.gyro_z,
                   gx,
                   gy,
                   gz);
    if (WriteLine(line)) {
        ++sample_index;
    }
}
#else
static void CaptureSolar(uint32_t now_ms) {
    char line[96];

    if (!ready || !IsDue(now_ms)) {
        return;
    }
    AdvanceSchedule(now_ms);
    if (INA3221_Read(&ina3221, now_ms) != HAL_OK) {
        return;
    }

    (void)snprintf(line,
                   sizeof(line),
                   "%lu,%lu,%ld,%ld\r\n",
                   (unsigned long)sample_index,
                   (unsigned long)now_ms,
                   (long)ina3221.data.solar_voltage_mV,
                   (long)ina3221.data.battery_voltage_mV);
    if (WriteLine(line)) {
        ++sample_index;
    }
}
#endif

void App_Init(I2C_HandleTypeDef *i2c,
              RTC_HandleTypeDef *rtc,
              UART_HandleTypeDef *gps_uart,
              UART_HandleTypeDef *debug_uart) {
    (void)rtc;
    (void)gps_uart;
    test_i2c = i2c;
    output_uart = debug_uart;

#if defined(CHARACTERIZE_MPU)
    if ((MPU6500_Detect(test_i2c, NULL) == HAL_OK) &&
        (MPU6500_BeginInitialization(test_i2c) == HAL_OK)) {
        initialization_started_ms = HAL_GetTick();
        initialization_waiting = true;
    }
#else
    ready = INA3221_Init(&ina3221, test_i2c) == HAL_OK;
    if (ready) {
        last_sample_ms = HAL_GetTick() - SAMPLE_PERIOD_MS;
        (void)WriteLine("sample,timestamp_ms,solar_voltage_mV,battery_voltage_mV\r\n");
    }
#endif
}

void App_Process(void) {
    const uint32_t now_ms = HAL_GetTick();

#if defined(CHARACTERIZE_MPU)
    FinishMpuInitialization(now_ms);
    CaptureMpu(now_ms);
#else
    CaptureSolar(now_ms);
#endif
}

bool App_IsRtcTimeValid(void) {
    return false;
}

HAL_StatusTypeDef App_SetMissionRtc(const RTC_TimeTypeDef *time, const RTC_DateTypeDef *date) {
    (void)time;
    (void)date;
    return HAL_ERROR;
}

void App_UartTxComplete(UART_HandleTypeDef *uart) {
    (void)uart;
}

void App_UartRxComplete(UART_HandleTypeDef *uart) {
    (void)uart;
}

void App_UartError(UART_HandleTypeDef *uart) {
    (void)uart;
}
