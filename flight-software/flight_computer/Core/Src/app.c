#include "app.h"

#include "command_handler.h"
#include "debug_console.h"
#include "flight_config.h"
#include "flight_data.h"
#include "i2c_bus_manager.h"
#include "main.h"
#include "sensor_manager.h"

#include <stdint.h>

typedef struct {
    uint32_t mpu6500_ms;
    uint32_t bmp280_ms;
    uint32_t ina3221_ms;
    uint32_t ds18b20_ms;
    uint32_t telemetry_ms;
    uint32_t status_led_ms;
} SchedulerState;

static RTC_HandleTypeDef *mission_rtc;
static SchedulerState scheduler;
static bool rtc_time_valid;
static FlightDataSnapshot debug_flight_data;
static I2cBusStatus debug_i2c_status;

static bool IsLeapYear(uint16_t year) {
    return ((year % 4U) == 0U) && (((year % 100U) != 0U) || ((year % 400U) == 0U));
}

static uint8_t DaysInMonth(uint8_t month, uint8_t rtc_year) {
    static const uint8_t days_by_month[] = {
        31U, 28U, 31U, 30U, 31U, 30U, 31U, 31U, 30U, 31U, 30U, 31U
    };
    uint8_t days;

    if ((month < 1U) || (month > 12U)) {
        return 0U;
    }

    days = days_by_month[month - 1U];
    /* STM32 RTC years 00..99 represent 2000..2099 in this application. */
    if ((month == 2U) && IsLeapYear((uint16_t)(2000U + rtc_year))) {
        ++days;
    }
    return days;
}

static bool ScheduledTaskIsDue(uint32_t now_ms, uint32_t last_run_ms, uint32_t period_ms) {
    return (now_ms - last_run_ms) >= period_ms;
}

static void AdvanceTaskSchedule(uint32_t *last_run_ms, uint32_t now_ms, uint32_t period_ms) {
    *last_run_ms += period_ms;

    /* Execute once after a long pause, then discard backlog instead of bursting. */
    if ((now_ms - *last_run_ms) >= period_ms) {
        *last_run_ms = now_ms;
    }
}

static void InitializeScheduler(uint32_t now_ms) {
    scheduler.mpu6500_ms = now_ms - MPU6500_PERIOD_MS;
    scheduler.bmp280_ms = now_ms - BMP280_PERIOD_MS;
    scheduler.ina3221_ms = now_ms - INA3221_PERIOD_MS;
    scheduler.ds18b20_ms = now_ms - DS18B20_PERIOD_MS;
    scheduler.telemetry_ms = now_ms - DEBUG_TELEMETRY_PERIOD_MS;
    scheduler.status_led_ms = now_ms - STATUS_LED_PERIOD_MS;
}

static void ProcessCommands(void) {
    uint8_t byte;

    while (DebugConsole_ReadCommand(&byte)) {
        CommandHandler_Execute(CommandHandler_DecodeDebugByte(byte));
    }
}

static void ReportSensorMessage(const char *message) {
    (void)DebugConsole_Write(message);
}

static void SendDebugTelemetry(uint32_t now_ms) {
    SensorManager_GetFlightData(now_ms, &debug_flight_data);
    I2cBusManager_GetStatus(&debug_i2c_status);
    DebugConsole_ShowDashboard(&debug_flight_data, &debug_i2c_status, rtc_time_valid, mission_rtc);
}

static void RunScheduledTasks(uint32_t now_ms) {
    if (ScheduledTaskIsDue(now_ms, scheduler.mpu6500_ms, MPU6500_PERIOD_MS)) {
        SensorManager_UpdateMpu6500(now_ms);
        AdvanceTaskSchedule(&scheduler.mpu6500_ms, now_ms, MPU6500_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.bmp280_ms, BMP280_PERIOD_MS)) {
        const bool sample_valid = SensorManager_UpdateBmp280(now_ms);

        SensorManager_ProcessAltitudeCalibrationSample(now_ms, sample_valid);
        AdvanceTaskSchedule(&scheduler.bmp280_ms, now_ms, BMP280_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.ina3221_ms, INA3221_PERIOD_MS)) {
        SensorManager_UpdateIna3221(now_ms);
        AdvanceTaskSchedule(&scheduler.ina3221_ms, now_ms, INA3221_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.ds18b20_ms, DS18B20_PERIOD_MS)) {
        SensorManager_StartDs18b20Conversion(now_ms);
        AdvanceTaskSchedule(&scheduler.ds18b20_ms, now_ms, DS18B20_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.telemetry_ms, DEBUG_TELEMETRY_PERIOD_MS)) {
        SendDebugTelemetry(now_ms);
        AdvanceTaskSchedule(&scheduler.telemetry_ms, now_ms, DEBUG_TELEMETRY_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.status_led_ms, STATUS_LED_PERIOD_MS)) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
        AdvanceTaskSchedule(&scheduler.status_led_ms, now_ms, STATUS_LED_PERIOD_MS);
    }
}

void App_Init(I2C_HandleTypeDef *i2c,
              RTC_HandleTypeDef *rtc,
              UART_HandleTypeDef *gps_uart,
              UART_HandleTypeDef *debug_uart) {
    const uint32_t now_ms = HAL_GetTick();

    mission_rtc = rtc;
    rtc_time_valid = HAL_RTCEx_BKUPRead(mission_rtc, RTC_BKP_DR0) == RTC_INITIALIZED_MAGIC;

    DebugConsole_Init(debug_uart);
    /* GPS RX uses priority 5; debug TX must never delay the NMEA receive path. */
    HAL_NVIC_SetPriority(USART2_IRQn, 6U, 0U);
    HAL_NVIC_EnableIRQ(USART2_IRQn);

    I2cBusManager_Init(i2c, SensorManager_InvalidateI2cSensors);
    SensorManager_Init(i2c, rtc, gps_uart, ReportSensorMessage, now_ms);
    InitializeScheduler(now_ms);
}

void App_Process(void) {
    const uint32_t now_ms = HAL_GetTick();

    ProcessCommands();
    DebugConsole_Process();
    SensorManager_ProcessContinuous(now_ms);
    I2cBusManager_Process(now_ms);
    RunScheduledTasks(now_ms);
}

bool App_IsRtcTimeValid(void) {
    return rtc_time_valid;
}

HAL_StatusTypeDef App_SetMissionRtc(const RTC_TimeTypeDef *time, const RTC_DateTypeDef *date) {
    RTC_TimeTypeDef rtc_time;
    RTC_DateTypeDef rtc_date;

    if ((time == NULL) || (date == NULL) || (time->Hours > 23U) || (time->Minutes > 59U) ||
        (time->Seconds > 59U) || (date->WeekDay < RTC_WEEKDAY_MONDAY) ||
        (date->WeekDay > RTC_WEEKDAY_SUNDAY) || (date->Month < 1U) || (date->Month > 12U) ||
        (date->Date < 1U) || (date->Year > 99U) ||
        (date->Date > DaysInMonth(date->Month, date->Year))) {
        return HAL_ERROR;
    }

    rtc_time = *time;
    rtc_time.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
    rtc_time.StoreOperation = RTC_STOREOPERATION_RESET;
    rtc_date = *date;

    rtc_time_valid = false;
    HAL_RTCEx_BKUPWrite(mission_rtc, RTC_BKP_DR0, 0U);
    if ((HAL_RTC_SetTime(mission_rtc, &rtc_time, RTC_FORMAT_BIN) != HAL_OK) ||
        (HAL_RTC_SetDate(mission_rtc, &rtc_date, RTC_FORMAT_BIN) != HAL_OK)) {
        return HAL_ERROR;
    }

    HAL_RTCEx_BKUPWrite(mission_rtc, RTC_BKP_DR0, RTC_INITIALIZED_MAGIC);
    if (HAL_RTCEx_BKUPRead(mission_rtc, RTC_BKP_DR0) != RTC_INITIALIZED_MAGIC) {
        return HAL_ERROR;
    }
    rtc_time_valid = true;
    return HAL_OK;
}

void App_UartTxComplete(UART_HandleTypeDef *uart) {
    DebugConsole_TxComplete(uart);
}

void App_UartRxComplete(UART_HandleTypeDef *uart) {
    SensorManager_GpsRxComplete(uart);
}

void App_UartError(UART_HandleTypeDef *uart) {
    SensorManager_GpsUartError(uart);
    DebugConsole_UartError(uart);
}

/* Kept as a compatibility entry point for existing mission-control code. */
HAL_StatusTypeDef SetMissionRtc(const RTC_TimeTypeDef *time, const RTC_DateTypeDef *date) {
    return App_SetMissionRtc(time, date);
}
