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
#include "mpu6500.h"
#include "neo6m.h"

#include <stdarg.h>
#include <stdio.h>
#include <string.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define MAIN_CYCLE_PERIOD_MS          1000U
#define CONSOLE_TIMEOUT_MS            100U
#define ALTITUDE_CALIBRATION_SAMPLES  10U
#define ALTITUDE_CALIBRATION_MIN_SAMPLES 5U
#define ALTITUDE_CALIBRATION_DELAY_MS 100U
#define GPS_DATA_MAX_AGE_MS            3000U
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
static BMP280_Data bmp280_data;
static MPU6500_RawData mpu6500_data;
static uint8_t bmp280_available;
static uint8_t mpu6500_available;
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
static void Console_Write(const char *message)
{
  size_t length;

  if (message == NULL)
  {
    return;
  }

  length = strlen(message);
  if (length > UINT16_MAX)
  {
    length = UINT16_MAX;
  }

  (void)HAL_UART_Transmit(&huart2, (const uint8_t *)message,
                          (uint16_t)length, CONSOLE_TIMEOUT_MS);
}

static size_t AppendText(char *buffer, size_t capacity, size_t offset,
                         const char *format, ...)
{
  int written;
  va_list arguments;

  if ((buffer == NULL) || (format == NULL) || (offset >= capacity))
  {
    return offset;
  }

  va_start(arguments, format);
  written = vsnprintf(&buffer[offset], capacity - offset, format, arguments);
  va_end(arguments);
  if (written < 0)
  {
    buffer[offset] = '\0';
    return offset;
  }

  if ((size_t)written >= (capacity - offset))
  {
    return capacity - 1U;
  }

  return offset + (size_t)written;
}

static size_t AppendCoordinate(char *buffer, size_t capacity, size_t offset,
                               const char *label, int32_t coordinate_deg_e7)
{
  const int64_t signed_value = coordinate_deg_e7;
  const uint64_t magnitude = (signed_value < 0) ?
                             (uint64_t)(-signed_value) :
                             (uint64_t)signed_value;

  return AppendText(buffer, capacity, offset, " | %s %c%lu.%07lu", label,
                    (signed_value < 0) ? '-' : '+',
                    (unsigned long)(magnitude / 10000000ULL),
                    (unsigned long)(magnitude % 10000000ULL));
}

static void RecoverI2cBus(void)
{
  (void)HAL_I2C_DeInit(&hi2c1);
  HAL_Delay(2U);
  MX_I2C1_Init();
}

static void InitializeMpu6500(void)
{
  uint8_t who_am_i = 0U;
  char message[64];

  mpu6500_available = 0U;
  if (MPU6500_Detect(&hi2c1, &who_am_i) != HAL_OK)
  {
    (void)snprintf(message, sizeof(message),
                   "MPU6500 FAIL | WHO_AM_I=0x%02X\r\n", who_am_i);
    Console_Write(message);
    return;
  }

  if (MPU6500_Init(&hi2c1) != HAL_OK)
  {
    Console_Write("MPU6500 INIT FAIL\r\n");
    return;
  }

  mpu6500_available = 1U;
  (void)snprintf(message, sizeof(message),
                 "MPU6500 OK | WHO_AM_I=0x%02X\r\n", who_am_i);
  Console_Write(message);
}

static HAL_StatusTypeDef CalibrateAltitude(void)
{
  uint64_t pressure_sum = 0U;
  uint32_t valid_samples = 0U;
  uint32_t sample_index;

  if (bmp280_available == 0U)
  {
    RecoverI2cBus();
    bmp280_available = (BMP280_Init(&hi2c1) == HAL_OK);
  }

  for (sample_index = 0U;
       sample_index < ALTITUDE_CALIBRATION_SAMPLES;
       ++sample_index)
  {
    BMP280_Data sample;

    if (BMP280_Read(&hi2c1, &sample) == HAL_OK)
    {
      pressure_sum += sample.pressure_pa;
      ++valid_samples;
    }

    if ((sample_index + 1U) < ALTITUDE_CALIBRATION_SAMPLES)
    {
      HAL_Delay(ALTITUDE_CALIBRATION_DELAY_MS);
    }
  }

  if (valid_samples < ALTITUDE_CALIBRATION_MIN_SAMPLES)
  {
    bmp280_available = 0U;
    return HAL_ERROR;
  }

  return Altitude_SaveReference(&hrtc, &altitude_reference,
                                (uint32_t)(pressure_sum / valid_samples));
}

static void ProcessConsoleCommand(void)
{
  uint8_t character;

  if (HAL_UART_Receive(&huart2, &character, 1U, 0U) != HAL_OK)
  {
    return;
  }

  if ((character == (uint8_t)'Z') || (character == (uint8_t)'z'))
  {
    Console_Write((CalibrateAltitude() == HAL_OK) ?
                  "ALT ZERO OK\r\n" : "ALT ZERO FAIL\r\n");
  }
}

static void RunOneCycle(void)
{
  RTC_TimeTypeDef rtc_time;
  RTC_DateTypeDef rtc_date;
  HAL_StatusTypeDef rtc_status;
  HAL_StatusTypeDef ds18b20_status;
  HAL_StatusTypeDef bmp280_status;
  HAL_StatusTypeDef mpu6500_status;
  HAL_StatusTypeDef altitude_status = HAL_ERROR;
  NEO6M_Data gps_data;
  bool gps_data_available;
  bool gps_data_fresh;
  bool gps_uart_active;
  float ds18b20_temperature_c = 0.0f;
  float altitude_m = 0.0f;
  size_t length = 0U;

  rtc_status = HAL_RTC_GetTime(&hrtc, &rtc_time, RTC_FORMAT_BIN);
  if (rtc_status == HAL_OK)
  {
    rtc_status = HAL_RTC_GetDate(&hrtc, &rtc_date, RTC_FORMAT_BIN);
  }

  ds18b20_status = DS18B20_ReadTemperature(&ds18b20_temperature_c);

  bmp280_status = BMP280_Read(&hi2c1, &bmp280_data);
  if (bmp280_status != HAL_OK)
  {
    bmp280_available = 0U;
    RecoverI2cBus();
    if (BMP280_Init(&hi2c1) == HAL_OK)
    {
      bmp280_available = 1U;
      bmp280_status = BMP280_Read(&hi2c1, &bmp280_data);
    }
  }
  bmp280_available = (bmp280_status == HAL_OK);

  if (bmp280_status == HAL_OK)
  {
    altitude_status = Altitude_Calculate(&altitude_reference,
                                         bmp280_data.pressure_pa,
                                         &altitude_m);
  }

  if (mpu6500_available == 0U)
  {
    uint8_t who_am_i;
    if ((MPU6500_Detect(&hi2c1, &who_am_i) == HAL_OK) &&
        (MPU6500_Init(&hi2c1) == HAL_OK))
    {
      mpu6500_available = 1U;
    }
  }
  mpu6500_status = (mpu6500_available != 0U) ?
                   MPU6500_ReadRaw(&hi2c1, &mpu6500_data) : HAL_ERROR;
  if (mpu6500_status != HAL_OK)
  {
    mpu6500_available = 0U;
  }

  NEO6M_Process();
  gps_data_available = NEO6M_GetData(&gps_data);
  gps_data_fresh = gps_data_available &&
                   NEO6M_IsDataFresh(&gps_data, HAL_GetTick(),
                                     GPS_DATA_MAX_AGE_MS);
  gps_uart_active = NEO6M_IsUartActive(HAL_GetTick(), GPS_DATA_MAX_AGE_MS);

  if (rtc_status == HAL_OK)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        "TIME %02u:%02u:%02u",
                        rtc_time.Hours, rtc_time.Minutes, rtc_time.Seconds);
  }
  else
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        "TIME FAIL");
  }

  if (ds18b20_status == HAL_OK)
  {
    const int32_t centi_c = (int32_t)(ds18b20_temperature_c * 100.0f);
    const int32_t magnitude = (centi_c < 0) ? -centi_c : centi_c;
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | DS18B20 %c%ld.%02ld C",
                        (centi_c < 0) ? '-' : '+',
                        (long)(magnitude / 100), (long)(magnitude % 100));
  }
  else
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | DS18B20 FAIL");
  }

  if (bmp280_status == HAL_OK)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | BMP280 %lu.%02lu hPa",
                        (unsigned long)(bmp280_data.pressure_pa / 100U),
                        (unsigned long)(bmp280_data.pressure_pa % 100U));
  }
  else
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | BMP280 FAIL");
  }

  if (altitude_status == HAL_OK)
  {
    const int32_t altitude_cm = (int32_t)(altitude_m * 100.0f);
    const int32_t magnitude = (altitude_cm < 0) ? -altitude_cm : altitude_cm;
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | P0 %lu.%02lu hPa | ALT %c%ld.%02ld m",
                        (unsigned long)(altitude_reference.reference_pressure_pa / 100U),
                        (unsigned long)(altitude_reference.reference_pressure_pa % 100U),
                        (altitude_cm < 0) ? '-' : '+',
                        (long)(magnitude / 100), (long)(magnitude % 100));
  }
  else if (altitude_reference.valid == 0U)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | ALT NOT CALIBRATED");
  }
  else
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | ALT INVALID");
  }

  if (mpu6500_status == HAL_OK)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | MPU RAW A[%d,%d,%d] G[%d,%d,%d]",
                        mpu6500_data.accel_x, mpu6500_data.accel_y,
                        mpu6500_data.accel_z, mpu6500_data.gyro_x,
                        mpu6500_data.gyro_y, mpu6500_data.gyro_z);
  }
  else
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | MPU6500 FAIL");
  }

  if (!gps_uart_active)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | GPS NO DATA");
  }
  else if (!gps_data_fresh)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | GPS NMEA INVALID");
  }
  else if (!gps_data.fix_valid)
  {
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | GPS NO FIX | SATS %u", gps_data.satellites);
    if (gps_data.utc_valid)
    {
      length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                          " | UTC %02u:%02u:%02u", gps_data.utc_hours,
                          gps_data.utc_minutes, gps_data.utc_seconds);
    }
  }
  else
  {
    const int64_t altitude_mm = gps_data.altitude_mm;
    const uint64_t altitude_magnitude = (altitude_mm < 0) ?
                                        (uint64_t)(-altitude_mm) :
                                        (uint64_t)altitude_mm;

    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | GPS FIX | SATS %u",
                        gps_data.satellites);
    length = AppendCoordinate(telemetry_line, sizeof(telemetry_line), length,
                              "LAT",
                              gps_data.latitude_deg_e7);
    length = AppendCoordinate(telemetry_line, sizeof(telemetry_line), length,
                              "LON",
                              gps_data.longitude_deg_e7);
    length = AppendText(telemetry_line, sizeof(telemetry_line), length,
                        " | ALT %c%lu.%01lu m | UTC %02u:%02u:%02u",
                        (altitude_mm < 0) ? '-' : '+',
                        (unsigned long)(altitude_magnitude / 1000ULL),
                        (unsigned long)((altitude_magnitude % 1000ULL) / 100ULL),
                        gps_data.utc_hours, gps_data.utc_minutes,
                        gps_data.utc_seconds);
  }

  length = AppendText(telemetry_line, sizeof(telemetry_line), length, "\r\n");
  (void)HAL_UART_Transmit(&huart2, (const uint8_t *)telemetry_line,
                          (uint16_t)length,
                          CONSOLE_TIMEOUT_MS);
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
    if (NEO6M_Init(&huart1) != HAL_OK)
    {
      Console_Write("GPS RX INIT FAIL\r\n");
    }

    if (DS18B20_Init() != HAL_OK)
    {
      Console_Write("DWT INIT FAIL\r\n");
    }

    Altitude_LoadReference(&hrtc, &altitude_reference);
    bmp280_available = (BMP280_Init(&hi2c1) == HAL_OK);
    Console_Write((bmp280_available != 0U) ?
                  "BMP280 OK\r\n" : "BMP280 INIT FAIL\r\n");
    InitializeMpu6500();

    /* USER CODE END 2 */
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    const uint32_t cycle_start = HAL_GetTick();

    ProcessConsoleCommand();
    RunOneCycle();
    HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);

    const uint32_t elapsed = HAL_GetTick() - cycle_start;
    if (elapsed < MAIN_CYCLE_PERIOD_MS)
    {
      HAL_Delay(MAIN_CYCLE_PERIOD_MS - elapsed);
    }
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

  if (HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR0) != 0xA5A5)
  {
    RTC_TimeTypeDef sTime = {0};
    RTC_DateTypeDef sDate = {0};

    sTime.Hours = 10;
    sTime.Minutes = 0;
    sTime.Seconds = 0;
    sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
    sTime.StoreOperation = RTC_STOREOPERATION_RESET;

    if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BIN) != HAL_OK)
    {
      Error_Handler();
    }

    sDate.WeekDay = RTC_WEEKDAY_SUNDAY;
    sDate.Month = RTC_MONTH_OCTOBER;
    sDate.Date = 25;
    sDate.Year = 26;

    if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BIN) != HAL_OK)
    {
      Error_Handler();
    }

    HAL_RTCEx_BKUPWrite(&hrtc, RTC_BKP_DR0, 0xA5A5);
  }

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

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  if (huart == &huart1)
  {
    NEO6M_UART_RxCpltCallback(huart);
  }
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
{
  if (huart == &huart1)
  {
    NEO6M_UART_ErrorCallback(huart);
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
