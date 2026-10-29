/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "altitude.h"
#include "bmp280.h"
#include "ds18b20.h"
#include "ina3221.h"
#include "mpu6500.h"
#include "neo6m.h"

#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
#define CONSOLE_TX_BUFFER_SIZE 2048U

typedef struct {
    BMP280_Data data;
    bool available;
    bool valid;
    uint32_t last_update_ms;
    uint32_t last_init_attempt_ms;
} Bmp280State;

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

typedef enum {
    MPU_HEALTH_OK,
    MPU_HEALTH_DEGRADED,
    MPU_HEALTH_RECOVERING,
    MPU_HEALTH_UNAVAILABLE
} Mpu6500Health;

typedef enum {
    MPU_ERROR_NONE,
    MPU_ERROR_READ,
    MPU_ERROR_NACK,
    MPU_ERROR_TIMEOUT,
    MPU_ERROR_BUS,
    MPU_ERROR_ARBITRATION_LOST,
    MPU_ERROR_WHO_AM_I,
    MPU_ERROR_INIT
} Mpu6500Error;

typedef struct {
    MPU6500_RawData data;
    bool available;
    bool valid;
    bool report_init_result;
    bool recovery_attempt;
    uint8_t health;
    uint8_t last_error;
    uint8_t consecutive_errors;
    uint8_t who_am_i;
    uint16_t recovery_count;
    uint16_t initialization_failures;
    uint32_t total_reads;
    uint32_t total_read_errors;
    uint32_t last_update_ms;
    uint32_t last_error_ms;
    uint32_t last_hal_error;
    uint32_t first_error_ms;
    uint32_t first_hal_error;
    uint32_t last_init_attempt_ms;
    uint32_t initialization_start_ms;
    Mpu6500InitializationState initialization_state;
} Mpu6500State;

typedef struct {
    NEO6M_Data data;
    bool data_available;
    bool data_fresh;
    bool uart_active;
} GpsState;

typedef struct {
    uint32_t mpu6500_ms;
    uint32_t bmp280_ms;
    uint32_t ina3221_ms;
    uint32_t ds18b20_ms;
    uint32_t telemetry_ms;
    uint32_t status_led_ms;
} SchedulerState;

typedef struct {
    uint8_t buffer[CONSOLE_TX_BUFFER_SIZE];
    volatile uint16_t head;
    volatile uint16_t tail;
    volatile uint16_t active_length;
    volatile bool busy;
    uint32_t dropped_messages;
} ConsoleTxState;

typedef enum {
    ALT_CAL_IDLE,
    ALT_CAL_RUNNING
} AltitudeCalibrationPhase;

typedef struct {
    AltitudeCalibrationPhase state;
    uint64_t pressure_sum;
    uint32_t valid_samples;
    uint32_t sample_count;
    uint32_t last_sample_ms;
} AltitudeCalibrationState;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define SENSOR_RETRY_PERIOD_MS           5000U
#define SENSOR_DATA_MAX_AGE_MS           2000U
#define I2C_RECOVERY_COOLDOWN_MS         100U
#define MPU6500_PERIOD_MS                 20U
#define MPU6500_MAX_CONSECUTIVE_ERRORS    3U
#define MPU6500_REINIT_RETRY_PERIOD_MS    100U
#define BMP280_PERIOD_MS                  100U
#define INA3221_PERIOD_MS                 100U
#define DS18B20_PERIOD_MS                 1000U
#define DEBUG_TELEMETRY_PERIOD_MS         1000U
#define STATUS_LED_PERIOD_MS              1000U
#define ALTITUDE_CALIBRATION_SAMPLES     10U
#define ALTITUDE_CALIBRATION_MIN_SAMPLES 5U
#define GPS_DATA_MAX_AGE_MS              3000U
#define RTC_INITIALIZED_MAGIC            0xA5A5U
#define CONSOLE_DASHBOARD_MODE           1
#define DASHBOARD_CONTENT_WIDTH          68
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

RTC_HandleTypeDef hrtc;

UART_HandleTypeDef huart1;
UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
static Altitude_Reference altitude_reference;
static AltitudeCalibrationState altitude_calibration;
static Bmp280State bmp280;
static Ds18b20State ds18b20;
static GpsState gps;
static INA3221_Handle ina3221;
static Mpu6500State mpu6500;
static SchedulerState scheduler;
static ConsoleTxState console_tx;
static uint32_t ina3221_last_init_attempt_ms;
static uint32_t last_i2c_recovery_ms;
static bool rtc_time_valid;
static char telemetry_line[320];
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_RTC_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
static void StartConsoleTransmission(void) {
    uint16_t length;

    if (console_tx.busy || (console_tx.head == console_tx.tail)) {
        return;
    }

    if (console_tx.head > console_tx.tail) {
        length = console_tx.head - console_tx.tail;
    } else {
        length = CONSOLE_TX_BUFFER_SIZE - console_tx.tail;
    }

    console_tx.active_length = length;
    console_tx.busy = true;
    if (HAL_UART_Transmit_IT(&huart2, &console_tx.buffer[console_tx.tail], length) != HAL_OK) {
        console_tx.active_length = 0U;
        console_tx.busy = false;
    }
}

static HAL_StatusTypeDef ConsoleWrite(const char *message) {
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

    head = console_tx.head;
    if (head >= console_tx.tail) {
        free_space = (CONSOLE_TX_BUFFER_SIZE - head) + console_tx.tail - 1U;
    } else {
        free_space = console_tx.tail - head - 1U;
    }

    if (length > free_space) {
        ++console_tx.dropped_messages;
        return HAL_BUSY;
    }

    for (size_t index = 0U; index < length; ++index) {
        console_tx.buffer[head] = (uint8_t)message[index];
        head = (uint16_t)((head + 1U) % CONSOLE_TX_BUFFER_SIZE);
    }

    console_tx.head = head;
    StartConsoleTransmission();
    return HAL_OK;
}

static size_t AppendText(char *buffer, size_t capacity, size_t offset, const char *format, ...) {
    int written;
    va_list arguments;

    if ((buffer == NULL) || (format == NULL) || (capacity == 0U) || (offset >= capacity)) {
        return offset;
    }

    va_start(arguments, format);
    written = vsnprintf(&buffer[offset], capacity - offset, format, arguments);
    va_end(arguments);

    if (written < 0) {
        buffer[offset] = '\0';
        return offset;
    }

    if ((size_t)written >= (capacity - offset)) {
        return capacity - 1U;
    }

    return offset + (size_t)written;
}

static bool SensorDataIsFresh(bool valid, uint32_t last_update_ms, uint32_t now_ms) {
    if (!valid) {
        return false;
    }

    return (now_ms - last_update_ms) <= SENSOR_DATA_MAX_AGE_MS;
}

HAL_StatusTypeDef SetMissionRtc(const RTC_TimeTypeDef *time, const RTC_DateTypeDef *date) {
    RTC_TimeTypeDef rtc_time;
    RTC_DateTypeDef rtc_date;

    if ((time == NULL) || (date == NULL) || (time->Hours > 23U) || (time->Minutes > 59U) ||
        (time->Seconds > 59U) || (date->WeekDay < RTC_WEEKDAY_MONDAY) ||
        (date->WeekDay > RTC_WEEKDAY_SUNDAY) || (date->Month < 1U) || (date->Month > 12U) ||
        (date->Date < 1U) || (date->Date > 31U) ||
        (date->Year > 99U)) {
        return HAL_ERROR;
    }

    rtc_time = *time;
    rtc_time.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
    rtc_time.StoreOperation = RTC_STOREOPERATION_RESET;
    rtc_date = *date;

    rtc_time_valid = false;
    HAL_RTCEx_BKUPWrite(&hrtc, RTC_BKP_DR0, 0U);
    if ((HAL_RTC_SetTime(&hrtc, &rtc_time, RTC_FORMAT_BIN) != HAL_OK) ||
        (HAL_RTC_SetDate(&hrtc, &rtc_date, RTC_FORMAT_BIN) != HAL_OK)) {
        return HAL_ERROR;
    }

    HAL_RTCEx_BKUPWrite(&hrtc, RTC_BKP_DR0, RTC_INITIALIZED_MAGIC);
    if (HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR0) != RTC_INITIALIZED_MAGIC) {
        return HAL_ERROR;
    }

    rtc_time_valid = true;
    return HAL_OK;
}

static bool I2cErrorRequiresRecovery(uint32_t error) {
    const uint32_t recoverable_errors = HAL_I2C_ERROR_BERR | HAL_I2C_ERROR_ARLO | HAL_I2C_ERROR_TIMEOUT;

    return (error & recoverable_errors) != 0U;
}

static bool I2cBusIsStuck(void) {
    return HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_9) == GPIO_PIN_RESET;
}

static void RecoverI2cBusWithClockPulses(void) {
    GPIO_InitTypeDef gpio = {0};

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8 | GPIO_PIN_9, GPIO_PIN_SET);
    gpio.Pin = GPIO_PIN_8 | GPIO_PIN_9;
    gpio.Mode = GPIO_MODE_OUTPUT_OD;
    gpio.Pull = GPIO_PULLUP;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &gpio);

    for (uint32_t pulse = 0U; (pulse < 9U) && I2cBusIsStuck(); ++pulse) {
        HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_RESET);
        HAL_Delay(1U);
        HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_SET);
        HAL_Delay(1U);
    }

    // Generate a STOP while both pins are still open-drain outputs.
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8 | GPIO_PIN_9, GPIO_PIN_RESET);
    HAL_Delay(1U);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_SET);
    HAL_Delay(1U);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_SET);
    HAL_Delay(1U);
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_8 | GPIO_PIN_9);
}

static void RecoverI2cPeripheralIfNeeded(uint32_t now_ms) {
    uint32_t error = HAL_I2C_GetError(&hi2c1);
    bool bus_stuck = I2cBusIsStuck();

    if (!I2cErrorRequiresRecovery(error) && !bus_stuck) {
        return;
    }

    if ((last_i2c_recovery_ms != 0U) && ((now_ms - last_i2c_recovery_ms) < I2C_RECOVERY_COOLDOWN_MS)) {
        return;
    }

    last_i2c_recovery_ms = now_ms;
    (void)HAL_I2C_DeInit(&hi2c1);
    if (bus_stuck) {
        RecoverI2cBusWithClockPulses();
    } else {
        // This exceptional 2 ms settle time is short and only follows a bus-level fault.
        HAL_Delay(2U);
    }
    MX_I2C1_Init();
}

static uint8_t ClassifyMpu6500Error(uint32_t hal_error, uint8_t fallback_error) {
    if ((hal_error & HAL_I2C_ERROR_TIMEOUT) != 0U) {
        return MPU_ERROR_TIMEOUT;
    }
    if ((hal_error & HAL_I2C_ERROR_BERR) != 0U) {
        return MPU_ERROR_BUS;
    }
    if ((hal_error & HAL_I2C_ERROR_ARLO) != 0U) {
        return MPU_ERROR_ARBITRATION_LOST;
    }
    if ((hal_error & HAL_I2C_ERROR_AF) != 0U) {
        return MPU_ERROR_NACK;
    }

    return fallback_error;
}

static void SetMpu6500LastError(uint8_t fallback_error, uint32_t now_ms) {
    mpu6500.last_hal_error = HAL_I2C_GetError(&hi2c1);
    mpu6500.last_error = ClassifyMpu6500Error(mpu6500.last_hal_error, fallback_error);
    mpu6500.last_error_ms = now_ms;
}

static void IncrementMpu6500InitializationFailures(void) {
    if (mpu6500.initialization_failures < UINT16_MAX) {
        ++mpu6500.initialization_failures;
    }
}

static bool InitializeBmp280(bool report_result) {
    bmp280.last_init_attempt_ms = HAL_GetTick();
    bmp280.valid = false;
    bmp280.available = BMP280_Init(&hi2c1) == HAL_OK;

    if (report_result) {
        if (bmp280.available) {
            (void)ConsoleWrite("BMP280 OK\r\n");
        } else {
            (void)ConsoleWrite("BMP280 INIT FAIL\r\n");
        }
    }

    return bmp280.available;
}

static bool InitializeMpu6500(bool report_result, bool recovery_attempt, uint32_t now_ms) {
    uint8_t who_am_i = 0U;

    mpu6500.last_init_attempt_ms = now_ms;
    mpu6500.valid = false;
    mpu6500.available = false;
    mpu6500.report_init_result = report_result;
    mpu6500.recovery_attempt = recovery_attempt;
    mpu6500.health = MPU_HEALTH_RECOVERING;
    mpu6500.initialization_state = MPU6500_INIT_IDLE;

    if (MPU6500_Detect(&hi2c1, &who_am_i) != HAL_OK) {
        mpu6500.who_am_i = who_am_i;
        mpu6500.health = MPU_HEALTH_UNAVAILABLE;
        SetMpu6500LastError(MPU_ERROR_WHO_AM_I, now_ms);
        IncrementMpu6500InitializationFailures();
        if (report_result) {
            char message[64];

            (void)snprintf(message, sizeof(message), "MPU6500 FAIL | WHO_AM_I=0x%02X\r\n", who_am_i);
            (void)ConsoleWrite(message);
        }
        return false;
    }

    mpu6500.who_am_i = who_am_i;
    if (MPU6500_BeginInitialization(&hi2c1) != HAL_OK) {
        mpu6500.health = MPU_HEALTH_UNAVAILABLE;
        SetMpu6500LastError(MPU_ERROR_INIT, now_ms);
        IncrementMpu6500InitializationFailures();
        return false;
    }

    mpu6500.initialization_start_ms = now_ms;
    mpu6500.initialization_state = MPU6500_INIT_WAITING;
    return true;
}

static void ServiceMpu6500Initialization(uint32_t now_ms) {
    char message[64];

    if (mpu6500.initialization_state != MPU6500_INIT_WAITING) {
        return;
    }

    if ((now_ms - mpu6500.initialization_start_ms) < MPU6500_STARTUP_TIME_MS) {
        return;
    }

    mpu6500.initialization_state = MPU6500_INIT_IDLE;
    mpu6500.available = MPU6500_FinishInitialization(&hi2c1) == HAL_OK;
    if (!mpu6500.available) {
        mpu6500.valid = false;
        mpu6500.health = MPU_HEALTH_UNAVAILABLE;
        SetMpu6500LastError(MPU_ERROR_INIT, now_ms);
        IncrementMpu6500InitializationFailures();
        RecoverI2cPeripheralIfNeeded(now_ms);
    } else {
        mpu6500.consecutive_errors = 0U;
        mpu6500.health = MPU_HEALTH_DEGRADED;
        if (mpu6500.recovery_attempt && (mpu6500.recovery_count < UINT16_MAX)) {
            ++mpu6500.recovery_count;
        }
    }

    if (mpu6500.report_init_result) {
        if (mpu6500.available) {
            (void)snprintf(message, sizeof(message), "MPU6500 OK | WHO_AM_I=0x%02X\r\n", mpu6500.who_am_i);
        } else {
            (void)snprintf(message, sizeof(message), "MPU6500 FAIL | WHO_AM_I=0x%02X\r\n", mpu6500.who_am_i);
        }
        (void)ConsoleWrite(message);
        mpu6500.report_init_result = false;
    }
}

static bool InitializeIna3221(bool report_result) {
    char message[48];

    ina3221_last_init_attempt_ms = HAL_GetTick();
    if (INA3221_Init(&ina3221, &hi2c1) != HAL_OK) {
        if (report_result) {
            (void)ConsoleWrite("INA3221 INIT FAIL\r\n");
        }
        return false;
    }

    if (report_result) {
        (void)snprintf(message, sizeof(message), "INA3221 OK | ADDR=0x%02X\r\n", INA3221_GetAddress(&ina3221));
        (void)ConsoleWrite(message);
    }

    return true;
}

static void InitializeApplication(void) {
    // GPS RX has priority 5; debug TX must never delay the NMEA receive path.
    HAL_NVIC_SetPriority(USART2_IRQn, 6U, 0U);
    HAL_NVIC_EnableIRQ(USART2_IRQn);

    if (NEO6M_Init(&huart1) != HAL_OK) {
        (void)ConsoleWrite("GPS RX INIT FAIL\r\n");
    }

    if (DS18B20_Init() == HAL_OK) {
        ds18b20.initialized = true;
        ds18b20.conversion_state = DS18B20_STATE_IDLE;
    } else {
        ds18b20.initialized = false;
        ds18b20.available = false;
        (void)ConsoleWrite("DWT INIT FAIL\r\n");
    }

    Altitude_LoadReference(&hrtc, &altitude_reference);
    RecoverI2cPeripheralIfNeeded(HAL_GetTick());
    (void)InitializeBmp280(true);
    (void)InitializeMpu6500(true, false, HAL_GetTick());
    (void)InitializeIna3221(true);
}

static void StartDs18b20Conversion(uint32_t now_ms) {
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

static void ServiceDs18b20Conversion(uint32_t now_ms) {
    float temperature_c;

    if (ds18b20.conversion_state != DS18B20_STATE_CONVERTING) {
        return;
    }

    if ((now_ms - ds18b20.conversion_start_ms) < DS18B20_CONVERSION_TIME_MS) {
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

static bool UpdateBmp280(uint32_t now_ms) {
    BMP280_Data sample;

    if (!bmp280.available) {
        if ((now_ms - bmp280.last_init_attempt_ms) < SENSOR_RETRY_PERIOD_MS) {
            return false;
        }

        if (!InitializeBmp280(false)) {
            RecoverI2cPeripheralIfNeeded(now_ms);
            return false;
        }
    }

    if (BMP280_Read(&hi2c1, &sample) != HAL_OK) {
        uint32_t error = HAL_I2C_GetError(&hi2c1);

        bmp280.valid = false;
        if (error != HAL_I2C_ERROR_NONE) {
            bmp280.available = false;
            bmp280.last_init_attempt_ms = now_ms;
        }
        RecoverI2cPeripheralIfNeeded(now_ms);
        return false;
    }

    bmp280.data = sample;
    bmp280.available = true;
    bmp280.valid = true;
    bmp280.last_update_ms = now_ms;
    return true;
}

static void UpdateMpu6500(uint32_t now_ms) {
    MPU6500_RawData sample;
    uint8_t who_am_i = 0U;

    if (mpu6500.initialization_state == MPU6500_INIT_WAITING) {
        return;
    }

    if (!mpu6500.available) {
        if ((now_ms - mpu6500.last_init_attempt_ms) < MPU6500_REINIT_RETRY_PERIOD_MS) {
            return;
        }

        (void)InitializeMpu6500(false, true, now_ms);
        return;
    }

    ++mpu6500.total_reads;
    if (MPU6500_ReadRaw(&hi2c1, &sample) != HAL_OK) {
        mpu6500.valid = false;
        mpu6500.health = MPU_HEALTH_DEGRADED;
        ++mpu6500.total_read_errors;
        if (mpu6500.consecutive_errors < UINT8_MAX) {
            ++mpu6500.consecutive_errors;
        }
        SetMpu6500LastError(MPU_ERROR_READ, now_ms);
        if (mpu6500.total_read_errors == 1U) {
            mpu6500.first_error_ms = now_ms;
            mpu6500.first_hal_error = mpu6500.last_hal_error;
        }

        if (mpu6500.consecutive_errors < MPU6500_MAX_CONSECUTIVE_ERRORS) {
            return;
        }

        if (MPU6500_Detect(&hi2c1, &who_am_i) == HAL_OK) {
            mpu6500.who_am_i = who_am_i;
            mpu6500.consecutive_errors = 0U;
            return;
        }

        mpu6500.who_am_i = who_am_i;
        mpu6500.health = MPU_HEALTH_RECOVERING;
        SetMpu6500LastError(MPU_ERROR_WHO_AM_I, now_ms);
        RecoverI2cPeripheralIfNeeded(now_ms);
        (void)InitializeMpu6500(false, true, now_ms);
        return;
    }

    mpu6500.data = sample;
    mpu6500.available = true;
    mpu6500.valid = true;
    mpu6500.health = MPU_HEALTH_OK;
    mpu6500.consecutive_errors = 0U;
    mpu6500.last_update_ms = now_ms;
}

static void UpdateIna3221(uint32_t now_ms) {
    if (!INA3221_IsReady(&ina3221)) {
        if ((now_ms - ina3221_last_init_attempt_ms) < SENSOR_RETRY_PERIOD_MS) {
            return;
        }

        if (!InitializeIna3221(false)) {
            RecoverI2cPeripheralIfNeeded(now_ms);
            return;
        }
    }

    if (INA3221_Read(&ina3221, now_ms) != HAL_OK) {
        ina3221_last_init_attempt_ms = now_ms;
        RecoverI2cPeripheralIfNeeded(now_ms);
    }
}

static void UpdateNavigation(uint32_t now_ms) {
    NEO6M_Process();
    gps.data_available = NEO6M_GetData(&gps.data);
    gps.data_fresh = gps.data_available && NEO6M_IsDataFresh(&gps.data, now_ms, GPS_DATA_MAX_AGE_MS);
    gps.uart_active = NEO6M_IsUartActive(now_ms, GPS_DATA_MAX_AGE_MS);
}

static void StartAltitudeCalibration(void) {
    // A repeated Z command deliberately restarts the calibration from zero.
    altitude_calibration.state = ALT_CAL_RUNNING;
    altitude_calibration.pressure_sum = 0U;
    altitude_calibration.valid_samples = 0U;
    altitude_calibration.sample_count = 0U;
    altitude_calibration.last_sample_ms = 0U;
}

static void ProcessAltitudeCalibrationSample(uint32_t now_ms, bool sample_valid) {
    uint32_t average_pressure_pa;
    HAL_StatusTypeDef save_status = HAL_ERROR;

    if (altitude_calibration.state != ALT_CAL_RUNNING) {
        return;
    }

    altitude_calibration.last_sample_ms = now_ms;
    ++altitude_calibration.sample_count;
    if (sample_valid) {
        altitude_calibration.pressure_sum += bmp280.data.pressure_pa;
        ++altitude_calibration.valid_samples;
    }

    if (altitude_calibration.sample_count < ALTITUDE_CALIBRATION_SAMPLES) {
        return;
    }

    altitude_calibration.state = ALT_CAL_IDLE;
    if (altitude_calibration.valid_samples >= ALTITUDE_CALIBRATION_MIN_SAMPLES) {
        average_pressure_pa =
            (uint32_t)(altitude_calibration.pressure_sum / altitude_calibration.valid_samples);
        save_status = Altitude_SaveReference(&hrtc, &altitude_reference, average_pressure_pa);
    }

    if (save_status == HAL_OK) {
        (void)ConsoleWrite("ALT ZERO OK\r\n");
    } else {
        (void)ConsoleWrite("ALT ZERO FAIL\r\n");
    }
}

static void ProcessCommand(uint8_t command) {
    if ((command != (uint8_t)'Z') && (command != (uint8_t)'z')) {
        return;
    }

    StartAltitudeCalibration();
}

static void ProcessConsoleCommands(void) {
    uint8_t command;

    while (HAL_UART_Receive(&huart2, &command, 1U, 0U) == HAL_OK) {
        ProcessCommand(command);
    }
}

static size_t AppendCoordinate(size_t offset, const char *label, int32_t coordinate_deg_e7) {
    int64_t signed_value = coordinate_deg_e7;
    uint64_t magnitude;

    if (signed_value < 0) {
        magnitude = (uint64_t)(-signed_value);
    } else {
        magnitude = (uint64_t)signed_value;
    }

    return AppendText(telemetry_line,
                      sizeof(telemetry_line),
                      offset,
                      " | %s %c%lu.%07lu",
                      label,
                      (signed_value < 0) ? '-' : '+',
                      (unsigned long)(magnitude / 10000000ULL),
                      (unsigned long)(magnitude % 10000000ULL));
}

static void SendTelemetryLine(size_t length) {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length, "\r\n");
    (void)length;
    (void)ConsoleWrite(telemetry_line);
}

static void SendEnvironmentTelemetry(uint32_t now_ms) {
    RTC_TimeTypeDef rtc_time;
    RTC_DateTypeDef rtc_date;
    HAL_StatusTypeDef rtc_status = HAL_ERROR;
    bool ds18b20_fresh;
    bool bmp280_fresh;
    float altitude_m = 0.0f;
    size_t length = 0U;

    if (rtc_time_valid) {
        rtc_status = HAL_RTC_GetTime(&hrtc, &rtc_time, RTC_FORMAT_BIN);
        if (rtc_status == HAL_OK) {
            rtc_status = HAL_RTC_GetDate(&hrtc, &rtc_date, RTC_FORMAT_BIN);
        }
    }

    length = AppendText(telemetry_line, sizeof(telemetry_line), length, "ENV | ");
    if (rtc_status == HAL_OK) {
        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            "TIME %02u:%02u:%02u",
                            rtc_time.Hours,
                            rtc_time.Minutes,
                            rtc_time.Seconds);
    } else if (!rtc_time_valid) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "TIME NOT SET");
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "TIME FAIL");
    }

    ds18b20_fresh = SensorDataIsFresh(ds18b20.valid, ds18b20.last_update_ms, now_ms);
    if (ds18b20_fresh) {
        int32_t centi_c = (int32_t)(ds18b20.temperature_c * 100.0f);
        int64_t signed_temperature = centi_c;
        uint64_t magnitude =
            signed_temperature < 0 ? (uint64_t)(-signed_temperature) : (uint64_t)signed_temperature;

        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            " | DS18B20 %c%lu.%02lu C",
                            signed_temperature < 0 ? '-' : '+',
                            (unsigned long)(magnitude / 100U),
                            (unsigned long)(magnitude % 100U));
    } else if (!ds18b20.available) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | DS18B20 UNAVAILABLE");
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | DS18B20 STALE");
    }

    bmp280_fresh = SensorDataIsFresh(bmp280.valid, bmp280.last_update_ms, now_ms);
    if (bmp280_fresh) {
        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            " | BMP280 %lu.%02lu hPa",
                            (unsigned long)(bmp280.data.pressure_pa / 100U),
                            (unsigned long)(bmp280.data.pressure_pa % 100U));
    } else if (!bmp280.available) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | BMP280 UNAVAILABLE");
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | BMP280 INVALID");
    }

    if (altitude_reference.valid != 0U) {
        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            " | P0 %lu.%02lu hPa",
                            (unsigned long)(altitude_reference.reference_pressure_pa / 100U),
                            (unsigned long)(altitude_reference.reference_pressure_pa % 100U));
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | P0 NOT SET");
    }

    if (bmp280_fresh &&
        (Altitude_Calculate(&altitude_reference, bmp280.data.pressure_pa, &altitude_m) == HAL_OK)) {
        int32_t altitude_cm = (int32_t)(altitude_m * 100.0f);
        int64_t signed_altitude = altitude_cm;
        uint64_t magnitude = signed_altitude < 0 ? (uint64_t)(-signed_altitude) : (uint64_t)signed_altitude;

        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            " | ALT %c%lu.%02lu m",
                            signed_altitude < 0 ? '-' : '+',
                            (unsigned long)(magnitude / 100U),
                            (unsigned long)(magnitude % 100U));
    } else if (altitude_reference.valid == 0U) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | ALT NOT CALIBRATED");
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, " | ALT INVALID");
    }

    SendTelemetryLine(length);
}

static void SendMpu6500Telemetry(uint32_t now_ms) {
    size_t length = 0U;

    length = AppendText(telemetry_line, sizeof(telemetry_line), length, "IMU | ");
    if (SensorDataIsFresh(mpu6500.valid, mpu6500.last_update_ms, now_ms)) {
        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            "MPU RAW A[%d,%d,%d] G[%d,%d,%d]",
                            mpu6500.data.accel_x,
                            mpu6500.data.accel_y,
                            mpu6500.data.accel_z,
                            mpu6500.data.gyro_x,
                            mpu6500.data.gyro_y,
                            mpu6500.data.gyro_z);
    } else if (!mpu6500.available) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "MPU6500 UNAVAILABLE");
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "MPU6500 INVALID");
    }

    SendTelemetryLine(length);
}

static void SendGpsTelemetry(void) {
    size_t length = 0U;

    length = AppendText(telemetry_line, sizeof(telemetry_line), length, "GPS | ");
    if (!gps.uart_active) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "NO DATA");
    } else if (!gps.data_fresh) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "NMEA INVALID OR STALE");
    } else if (!gps.data.fix_valid) {
        length =
            AppendText(telemetry_line, sizeof(telemetry_line), length, "NO FIX | SATS %u", gps.data.satellites);
        if (gps.data.utc_valid) {
            length = AppendText(telemetry_line,
                                sizeof(telemetry_line),
                                length,
                                " | UTC %02u:%02u:%02u",
                                gps.data.utc_hours,
                                gps.data.utc_minutes,
                                gps.data.utc_seconds);
        }
    } else {
        int64_t altitude_mm = gps.data.altitude_mm;
        uint64_t altitude_magnitude = altitude_mm < 0 ? (uint64_t)(-altitude_mm) : (uint64_t)altitude_mm;

        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "FIX | SATS %u", gps.data.satellites);
        length = AppendCoordinate(length, "LAT", gps.data.latitude_deg_e7);
        length = AppendCoordinate(length, "LON", gps.data.longitude_deg_e7);
        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            " | ALT %c%lu.%01lu m | UTC %02u:%02u:%02u",
                            altitude_mm < 0 ? '-' : '+',
                            (unsigned long)(altitude_magnitude / 1000ULL),
                            (unsigned long)((altitude_magnitude % 1000ULL) / 100ULL),
                            gps.data.utc_hours,
                            gps.data.utc_minutes,
                            gps.data.utc_seconds);
    }

    SendTelemetryLine(length);
}

static void SendIna3221Telemetry(uint32_t now_ms) {
    size_t length = 0U;

    length = AppendText(telemetry_line, sizeof(telemetry_line), length, "INA | ");
    if (INA3221_IsDataFresh(&ina3221, now_ms, INA3221_DATA_MAX_AGE_MS)) {
        int32_t current_ma = ina3221.data.battery_current_mA;
        int64_t signed_current = current_ma;
        uint64_t current_magnitude = signed_current < 0 ? (uint64_t)(-signed_current) : (uint64_t)signed_current;

        length = AppendText(telemetry_line,
                            sizeof(telemetry_line),
                            length,
                            "VBAT %ld.%03ld V | IBAT %c%lu.%03lu A | VPANEL %ld.%03ld V",
                            (long)(ina3221.data.battery_voltage_mV / 1000),
                            (long)(ina3221.data.battery_voltage_mV % 1000),
                            signed_current < 0 ? '-' : '+',
                            (unsigned long)(current_magnitude / 1000U),
                            (unsigned long)(current_magnitude % 1000U),
                            (long)(ina3221.data.solar_voltage_mV / 1000),
                            (long)(ina3221.data.solar_voltage_mV % 1000));
    } else if (!INA3221_IsReady(&ina3221)) {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "FAIL | UNAVAILABLE");
    } else {
        length = AppendText(telemetry_line, sizeof(telemetry_line), length, "FAIL | INVALID OR STALE");
    }

    SendTelemetryLine(length);
}

static void SendDashboardBorder(void) {
    (void)ConsoleWrite("+----------------------------------------------------------------------+\r\n");
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
    (void)ConsoleWrite(telemetry_line);
}

static void FormatCoordinate(char *buffer, size_t capacity, int32_t coordinate_deg_e7) {
    int64_t signed_value = coordinate_deg_e7;
    uint64_t magnitude;

    if (signed_value < 0) {
        magnitude = (uint64_t)(-signed_value);
    } else {
        magnitude = (uint64_t)signed_value;
    }

    (void)snprintf(buffer,
                   capacity,
                   "%c%lu.%07lu",
                   signed_value < 0 ? '-' : '+',
                   (unsigned long)(magnitude / 10000000ULL),
                   (unsigned long)(magnitude % 10000000ULL));
}

static const char *Mpu6500HealthText(uint8_t health) {
    switch (health) {
        case MPU_HEALTH_OK:
            return "OK";
        case MPU_HEALTH_DEGRADED:
            return "DEGRADED";
        case MPU_HEALTH_RECOVERING:
            return "RECOVERING";
        case MPU_HEALTH_UNAVAILABLE:
        default:
            return "UNAVAILABLE";
    }
}

static const char *Mpu6500ErrorText(uint8_t error) {
    switch (error) {
        case MPU_ERROR_NONE:
            return "NONE";
        case MPU_ERROR_READ:
            return "READ";
        case MPU_ERROR_NACK:
            return "NACK";
        case MPU_ERROR_TIMEOUT:
            return "TIMEOUT";
        case MPU_ERROR_BUS:
            return "BUS";
        case MPU_ERROR_ARBITRATION_LOST:
            return "ARLO";
        case MPU_ERROR_WHO_AM_I:
            return "WHO_AM_I";
        case MPU_ERROR_INIT:
        default:
            return "INIT";
    }
}

static void SendDashboardTelemetry(uint32_t now_ms) {
    static bool dashboard_started;
    RTC_TimeTypeDef rtc_time;
    RTC_DateTypeDef rtc_date;
    HAL_StatusTypeDef rtc_status = HAL_ERROR;
    bool ds18b20_fresh;
    bool bmp280_fresh;
    bool mpu6500_fresh;
    bool ina3221_fresh;
    float altitude_m = 0.0f;
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

    if (!dashboard_started) {
        // To restore the cursor outside dashboard mode, send "\033[?25h".
        (void)ConsoleWrite("\033[2J\033[H\033[?25l");
        dashboard_started = true;
    } else {
        (void)ConsoleWrite("\033[H");
    }

    if (rtc_time_valid) {
        rtc_status = HAL_RTC_GetTime(&hrtc, &rtc_time, RTC_FORMAT_BIN);
        if (rtc_status == HAL_OK) {
            rtc_status = HAL_RTC_GetDate(&hrtc, &rtc_date, RTC_FORMAT_BIN);
        }
    }
    if (rtc_status == HAL_OK) {
        (void)snprintf(rtc_text,
                       sizeof(rtc_text),
                       "%02u:%02u:%02u",
                       rtc_time.Hours,
                       rtc_time.Minutes,
                       rtc_time.Seconds);
    }

    ds18b20_fresh = SensorDataIsFresh(ds18b20.valid, ds18b20.last_update_ms, now_ms);
    if (ds18b20_fresh) {
        int32_t centi_c = (int32_t)(ds18b20.temperature_c * 100.0f);
        int64_t signed_temperature = centi_c;
        uint64_t magnitude =
            signed_temperature < 0 ? (uint64_t)(-signed_temperature) : (uint64_t)signed_temperature;

        (void)snprintf(temperature_text,
                       sizeof(temperature_text),
                       "%c%lu.%02lu C",
                       signed_temperature < 0 ? '-' : '+',
                       (unsigned long)(magnitude / 100U),
                       (unsigned long)(magnitude % 100U));
    } else if (!ds18b20.available) {
        (void)snprintf(temperature_text, sizeof(temperature_text), "UNAVAILABLE");
    }

    bmp280_fresh = SensorDataIsFresh(bmp280.valid, bmp280.last_update_ms, now_ms);
    if (bmp280_fresh) {
        (void)snprintf(pressure_text,
                       sizeof(pressure_text),
                       "%lu.%02lu hPa",
                       (unsigned long)(bmp280.data.pressure_pa / 100U),
                       (unsigned long)(bmp280.data.pressure_pa % 100U));
    } else if (!bmp280.available) {
        (void)snprintf(pressure_text, sizeof(pressure_text), "UNAVAILABLE");
    } else if (bmp280.valid) {
        (void)snprintf(pressure_text, sizeof(pressure_text), "STALE");
    }

    if (altitude_reference.valid != 0U) {
        (void)snprintf(reference_text,
                       sizeof(reference_text),
                       "%lu.%02lu hPa",
                       (unsigned long)(altitude_reference.reference_pressure_pa / 100U),
                       (unsigned long)(altitude_reference.reference_pressure_pa % 100U));
    }

    if (bmp280_fresh &&
        (Altitude_Calculate(&altitude_reference, bmp280.data.pressure_pa, &altitude_m) == HAL_OK)) {
        int32_t altitude_cm = (int32_t)(altitude_m * 100.0f);
        int64_t signed_altitude = altitude_cm;
        uint64_t magnitude =
            signed_altitude < 0 ? (uint64_t)(-signed_altitude) : (uint64_t)signed_altitude;

        (void)snprintf(altitude_text,
                       sizeof(altitude_text),
                       "%c%lu.%02lu m",
                       signed_altitude < 0 ? '-' : '+',
                       (unsigned long)(magnitude / 100U),
                       (unsigned long)(magnitude % 100U));
    } else if (altitude_reference.valid == 0U) {
        (void)snprintf(altitude_text, sizeof(altitude_text), "NOT SET");
    } else if (!bmp280.available) {
        (void)snprintf(altitude_text, sizeof(altitude_text), "UNAVAILABLE");
    } else if (bmp280.valid) {
        (void)snprintf(altitude_text, sizeof(altitude_text), "STALE");
    }

    mpu6500_fresh =
        (mpu6500.last_update_ms != 0U) && ((now_ms - mpu6500.last_update_ms) <= SENSOR_DATA_MAX_AGE_MS);

    if (gps.uart_active) {
        if (!gps.data_fresh) {
            (void)snprintf(gps_status, sizeof(gps_status), "STALE");
        } else {
            (void)snprintf(satellites_text, sizeof(satellites_text), "%u", gps.data.satellites);
            if (gps.data.utc_valid) {
                (void)snprintf(gps_utc_text,
                               sizeof(gps_utc_text),
                               "%02u:%02u:%02u",
                               gps.data.utc_hours,
                               gps.data.utc_minutes,
                               gps.data.utc_seconds);
            }

            if (!gps.data.fix_valid) {
                (void)snprintf(gps_status, sizeof(gps_status), "NO FIX");
            } else {
                int64_t altitude_mm = gps.data.altitude_mm;
                uint64_t magnitude = altitude_mm < 0 ? (uint64_t)(-altitude_mm) : (uint64_t)altitude_mm;

                (void)snprintf(gps_status, sizeof(gps_status), "FIX");
                FormatCoordinate(latitude_text, sizeof(latitude_text), gps.data.latitude_deg_e7);
                FormatCoordinate(longitude_text, sizeof(longitude_text), gps.data.longitude_deg_e7);
                (void)snprintf(gps_altitude_text,
                               sizeof(gps_altitude_text),
                               "%c%lu.%01lu m",
                               altitude_mm < 0 ? '-' : '+',
                               (unsigned long)(magnitude / 1000ULL),
                               (unsigned long)((magnitude % 1000ULL) / 100ULL));
            }
        }
    }

    ina3221_fresh = INA3221_IsDataFresh(&ina3221, now_ms, INA3221_DATA_MAX_AGE_MS);
    if (ina3221_fresh) {
        int32_t current_ma = ina3221.data.battery_current_mA;
        int64_t signed_current = current_ma;
        uint64_t magnitude =
            signed_current < 0 ? (uint64_t)(-signed_current) : (uint64_t)signed_current;

        (void)snprintf(battery_text,
                       sizeof(battery_text),
                       "%ld.%03ld V",
                       (long)(ina3221.data.battery_voltage_mV / 1000),
                       (long)(ina3221.data.battery_voltage_mV % 1000));
        (void)snprintf(current_text,
                       sizeof(current_text),
                       "%c%lu.%03lu A",
                       signed_current < 0 ? '-' : '+',
                       (unsigned long)(magnitude / 1000U),
                       (unsigned long)(magnitude % 1000U));
        (void)snprintf(solar_text,
                       sizeof(solar_text),
                       "%ld.%03ld V",
                       (long)(ina3221.data.solar_voltage_mV / 1000),
                       (long)(ina3221.data.solar_voltage_mV % 1000));
    } else if (!INA3221_IsReady(&ina3221)) {
        (void)snprintf(battery_text, sizeof(battery_text), "UNAVAILABLE");
        (void)snprintf(current_text, sizeof(current_text), "UNAVAILABLE");
        (void)snprintf(solar_text, sizeof(solar_text), "UNAVAILABLE");
    } else if (ina3221.data.valid) {
        (void)snprintf(battery_text, sizeof(battery_text), "STALE");
        (void)snprintf(current_text, sizeof(current_text), "STALE");
        (void)snprintf(solar_text, sizeof(solar_text), "STALE");
    }

    SendDashboardBorder();
    SendDashboardLine("ASTRA FLIGHT COMPUTER");
    SendDashboardBorder();
    SendDashboardLine("SYSTEM");
    SendDashboardLine("RTC          %-20s STATUS       RUNNING", rtc_text);
    SendDashboardBorder();
    SendDashboardLine("ENVIRONMENT");
    SendDashboardLine("DS18B20      %-20s P0           %s", temperature_text, reference_text);
    SendDashboardLine("BMP280       %-20s ALTITUDE     %s", pressure_text, altitude_text);
    SendDashboardBorder();
    SendDashboardLine("IMU - MPU6500                  STATUS       %s", Mpu6500HealthText(mpu6500.health));
    if (mpu6500_fresh) {
        SendDashboardLine("ACCEL        X:%+7d      Y:%+7d      Z:%+7d",
                          mpu6500.data.accel_x,
                          mpu6500.data.accel_y,
                          mpu6500.data.accel_z);
        SendDashboardLine("GYRO         X:%+7d      Y:%+7d      Z:%+7d",
                          mpu6500.data.gyro_x,
                          mpu6500.data.gyro_y,
                          mpu6500.data.gyro_z);
    } else {
        SendDashboardLine("ACCEL        --");
        SendDashboardLine("GYRO         --");
    }
    SendDashboardLine("READS %lu  ERR %lu  CONSEC %u  REC %u  INIT %u  LAST %s",
                      (unsigned long)mpu6500.total_reads,
                      (unsigned long)mpu6500.total_read_errors,
                      mpu6500.consecutive_errors,
                      mpu6500.recovery_count,
                      mpu6500.initialization_failures,
                      Mpu6500ErrorText(mpu6500.last_error));
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

static void SendDebugTelemetry(uint32_t now_ms) {
    if (CONSOLE_DASHBOARD_MODE != 0) {
        SendDashboardTelemetry(now_ms);
    } else {
        SendEnvironmentTelemetry(now_ms);
        SendMpu6500Telemetry(now_ms);
        SendGpsTelemetry();
        SendIna3221Telemetry(now_ms);
    }
}

static bool ScheduledTaskIsDue(uint32_t now_ms, uint32_t last_run_ms, uint32_t period_ms) {
    return (now_ms - last_run_ms) >= period_ms;
}

static void AdvanceTaskSchedule(uint32_t *last_run_ms, uint32_t now_ms, uint32_t period_ms) {
    *last_run_ms += period_ms;

    // Execute once after a long pause, then discard backlog instead of running bursts.
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

static void ProcessContinuousServices(uint32_t now_ms) {
    StartConsoleTransmission();
    UpdateNavigation(now_ms);
    ServiceDs18b20Conversion(now_ms);
    ServiceMpu6500Initialization(now_ms);
}

static void UpdateStatusIndicator(void) {
    HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
}

static void RunScheduledTasks(uint32_t now_ms) {
    if (ScheduledTaskIsDue(now_ms, scheduler.mpu6500_ms, MPU6500_PERIOD_MS)) {
        UpdateMpu6500(now_ms);
        AdvanceTaskSchedule(&scheduler.mpu6500_ms, now_ms, MPU6500_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.bmp280_ms, BMP280_PERIOD_MS)) {
        bool sample_valid = UpdateBmp280(now_ms);

        ProcessAltitudeCalibrationSample(now_ms, sample_valid);
        AdvanceTaskSchedule(&scheduler.bmp280_ms, now_ms, BMP280_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.ina3221_ms, INA3221_PERIOD_MS)) {
        UpdateIna3221(now_ms);
        AdvanceTaskSchedule(&scheduler.ina3221_ms, now_ms, INA3221_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.ds18b20_ms, DS18B20_PERIOD_MS)) {
        StartDs18b20Conversion(now_ms);
        AdvanceTaskSchedule(&scheduler.ds18b20_ms, now_ms, DS18B20_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.telemetry_ms, DEBUG_TELEMETRY_PERIOD_MS)) {
        SendDebugTelemetry(now_ms);
        AdvanceTaskSchedule(&scheduler.telemetry_ms, now_ms, DEBUG_TELEMETRY_PERIOD_MS);
    }

    if (ScheduledTaskIsDue(now_ms, scheduler.status_led_ms, STATUS_LED_PERIOD_MS)) {
        UpdateStatusIndicator();
        AdvanceTaskSchedule(&scheduler.status_led_ms, now_ms, STATUS_LED_PERIOD_MS);
    }
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {
    /* USER CODE BEGIN 1 */

    /* USER CODE END 1 */

    /* MCU Configuration--------------------------------------------------------*/

    /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
    HAL_Init();

    /* USER CODE BEGIN Init */

    /* USER CODE END Init */

    /* Configure the system clock */
    SystemClock_Config();

    /* USER CODE BEGIN SysInit */

    /* USER CODE END SysInit */

    /* Initialize all configured peripherals */
    MX_GPIO_Init();
    MX_RTC_Init();
    MX_USART1_UART_Init();
    MX_I2C1_Init();
    MX_USART2_UART_Init();
    /* USER CODE BEGIN 2 */
    InitializeApplication();
    InitializeScheduler(HAL_GetTick());

    /* USER CODE END 2 */
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
    while (1) {
        const uint32_t now_ms = HAL_GetTick();

        ProcessConsoleCommands();
        ProcessContinuousServices(now_ms);
        RunScheduledTasks(now_ms);
    }
/* USER CODE END WHILE */

/* USER CODE BEGIN 3 */
/* USER CODE END 3 */
}


/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE|RCC_OSCILLATORTYPE_LSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.LSEState = RCC_LSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSE;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  HAL_RCC_MCOConfig(RCC_MCO1, RCC_MCO1SOURCE_HSE, RCC_MCODIV_3);
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief RTC Initialization Function
  * @param None
  * @retval None
  */
static void MX_RTC_Init(void)
{

  /* USER CODE BEGIN RTC_Init 0 */

  /* USER CODE END RTC_Init 0 */

  /* USER CODE BEGIN RTC_Init 1 */

  /* USER CODE END RTC_Init 1 */

  /** Initialize RTC Only
  */
  hrtc.Instance = RTC;
  hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
  hrtc.Init.AsynchPrediv = 127;
  hrtc.Init.SynchPrediv = 255;
  hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
  hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
  hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
  if (HAL_RTC_Init(&hrtc) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN RTC_Init 2 */

  rtc_time_valid = HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR0) == RTC_INITIALIZED_MAGIC;

  /* USER CODE END RTC_Init 2 */
}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 9600;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin : PC13 */
  GPIO_InitStruct.Pin = GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pin : DS18B20_DQ_Pin */
  GPIO_InitStruct.Pin = DS18B20_DQ_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(DS18B20_DQ_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : PA8 */
  GPIO_InitStruct.Pin = GPIO_PIN_8;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStruct.Alternate = GPIO_AF0_MCO;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

void USART2_IRQHandler(void) {
    HAL_UART_IRQHandler(&huart2);
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart != &huart2) {
        return;
    }

    console_tx.tail = (uint16_t)((console_tx.tail + console_tx.active_length) % CONSOLE_TX_BUFFER_SIZE);
    console_tx.active_length = 0U;
    console_tx.busy = false;
    StartConsoleTransmission();
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart == &huart1) {
        NEO6M_UART_RxCpltCallback(huart);
    }
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart) {
    if (huart == &huart1) {
        NEO6M_UART_ErrorCallback(huart);
    } else if (huart == &huart2) {
        console_tx.tail = console_tx.head;
        console_tx.active_length = 0U;
        console_tx.busy = false;
        ++console_tx.dropped_messages;
    }
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
