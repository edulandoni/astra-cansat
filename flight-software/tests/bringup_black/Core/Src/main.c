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
#include "stdio.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;
I2C_HandleTypeDef hi2c2;

RTC_HandleTypeDef hrtc;

UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */

RTC_TimeTypeDef rtcTime;
RTC_DateTypeDef rtcDate;
float temperature;
char tx_buffer[160];
HAL_StatusTypeDef bmp_status;
uint8_t bmp_chip_id = 0;
HAL_StatusTypeDef bmp_read_status;

#define BMP280_ADDR (0x76U << 1)

typedef struct
{
  uint16_t T1;
  int16_t  T2;
  int16_t  T3;

  uint16_t P1;
  int16_t  P2;
  int16_t  P3;
  int16_t  P4;
  int16_t  P5;
  int16_t  P6;
  int16_t  P7;
  int16_t  P8;
  int16_t  P9;
} BMP280_Calib_t;

BMP280_Calib_t bmp_cal;

int32_t bmp_t_fine;
int32_t bmp_temperature_centi;
uint32_t bmp_pressure_pa;
HAL_StatusTypeDef bmp_data_status;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_RTC_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_I2C1_Init(void);
static void MX_I2C2_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/

/* USER CODE BEGIN 0 */
static void delay_us(uint32_t us){
    uint32_t start = DWT->CYCCNT;
    uint32_t ticks = us * (SystemCoreClock / 1000000U);
    while ((DWT->CYCCNT - start) < ticks);
}

static void DWT_Delay_Init(void){
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    DWT->CYCCNT = 0;
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
}

static void DS18B20_Low(void){
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);
}

static void DS18B20_Release(void){
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);
}

static uint8_t DS18B20_Reset(void){
    uint8_t presence;
    DS18B20_Low();
    delay_us(480);
    DS18B20_Release();
    delay_us(70);
    presence = (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_1) == GPIO_PIN_RESET);
    delay_us(410);
    return presence;
}

static void DS18B20_WriteBit(uint8_t bit){
    DS18B20_Low();
    if (bit){
        delay_us(6);
        DS18B20_Release();
        delay_us(64);
    }
    else{
        delay_us(60);
        DS18B20_Release();
        delay_us(10);
    }
}

static uint8_t DS18B20_ReadBit(void){
    uint8_t bit;
    DS18B20_Low();
    delay_us(3);
    DS18B20_Release();
    delay_us(10);
    bit = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_1);
    delay_us(53);
    return bit;
}

static void DS18B20_WriteByte(uint8_t data){
    for (uint8_t i = 0; i < 8; i++){
        DS18B20_WriteBit(data & 0x01);
        data >>= 1;
    }
}

static uint8_t DS18B20_ReadByte(void){
    uint8_t data = 0;
    for (uint8_t i = 0; i < 8; i++){
        if (DS18B20_ReadBit())
            data |= (1U << i);
    }
    return data;
}

static float DS18B20_ReadTemperature(void){
    uint8_t lsb;
    uint8_t msb;
    int16_t raw;
    if (!DS18B20_Reset())
        return -1000.0f;
    DS18B20_WriteByte(0xCC);   // Skip ROM
    DS18B20_WriteByte(0x44);   // Convert T
    HAL_Delay(750);
    if (!DS18B20_Reset())
        return -1000.0f;
    DS18B20_WriteByte(0xCC);   // Skip ROM
    DS18B20_WriteByte(0xBE);   // Read Scratchpad
    lsb = DS18B20_ReadByte();
    msb = DS18B20_ReadByte();
    raw = (int16_t)((msb << 8) | lsb);
    return (float)raw / 16.0f;
}
static HAL_StatusTypeDef BMP280_ReadCalibration(void)
{
    uint8_t c[24];

    if (HAL_I2C_Mem_Read(&hi2c1, BMP280_ADDR, 0x88,
                         I2C_MEMADD_SIZE_8BIT, c, 24, 100) != HAL_OK)
    {
        return HAL_ERROR;
    }

    bmp_cal.T1 = (uint16_t)(c[0]  | (c[1]  << 8));
    bmp_cal.T2 = (int16_t) (c[2]  | (c[3]  << 8));
    bmp_cal.T3 = (int16_t) (c[4]  | (c[5]  << 8));

    bmp_cal.P1 = (uint16_t)(c[6]  | (c[7]  << 8));
    bmp_cal.P2 = (int16_t) (c[8]  | (c[9]  << 8));
    bmp_cal.P3 = (int16_t) (c[10] | (c[11] << 8));
    bmp_cal.P4 = (int16_t) (c[12] | (c[13] << 8));
    bmp_cal.P5 = (int16_t) (c[14] | (c[15] << 8));
    bmp_cal.P6 = (int16_t) (c[16] | (c[17] << 8));
    bmp_cal.P7 = (int16_t) (c[18] | (c[19] << 8));
    bmp_cal.P8 = (int16_t) (c[20] | (c[21] << 8));
    bmp_cal.P9 = (int16_t) (c[22] | (c[23] << 8));

    return HAL_OK;
}

static int32_t BMP280_CompensateTemperature(int32_t adc_T)
{
    int32_t var1;
    int32_t var2;

    var1 =
        ((((adc_T >> 3) - ((int32_t)bmp_cal.T1 << 1))) *
          ((int32_t)bmp_cal.T2)) >> 11;

    var2 =
        (((((adc_T >> 4) - ((int32_t)bmp_cal.T1)) *
           ((adc_T >> 4) - ((int32_t)bmp_cal.T1))) >> 12) *
         ((int32_t)bmp_cal.T3)) >> 14;

    bmp_t_fine = var1 + var2;

    return (bmp_t_fine * 5 + 128) >> 8;
}

static uint32_t BMP280_CompensatePressure(int32_t adc_P){

    int64_t var1;
    int64_t var2;
    int64_t p;

    var1 = ((int64_t)bmp_t_fine) - 128000;
    var2 = var1 * var1 * (int64_t)bmp_cal.P6;
    var2 += (var1 * (int64_t)bmp_cal.P5) << 17;
    var2 += ((int64_t)bmp_cal.P4) << 35;

    var1 =
        ((var1 * var1 * (int64_t)bmp_cal.P3) >> 8) +
        ((var1 * (int64_t)bmp_cal.P2) << 12);

    var1 =
        (((((int64_t)1) << 47) + var1) *
         (int64_t)bmp_cal.P1) >> 33;

    if (var1 == 0)
        return 0;

    p = 1048576 - adc_P;
    p = (((p << 31) - var2) * 3125) / var1;

    var1 =
        ((int64_t)bmp_cal.P9 * (p >> 13) * (p >> 13)) >> 25;

    var2 =
        ((int64_t)bmp_cal.P8 * p) >> 19;

    p =
        ((p + var1 + var2) >> 8) +
        ((int64_t)bmp_cal.P7 << 4);

    return (uint32_t)(p >> 8);   // Pa
}

static HAL_StatusTypeDef BMP280_Init(void){
    uint8_t config = 0x40;
    uint8_t ctrl_meas = 0x2F;

    if (BMP280_ReadCalibration() != HAL_OK)
        return HAL_ERROR;

    if (HAL_I2C_Mem_Write(&hi2c1, BMP280_ADDR, 0xF5,
                          I2C_MEMADD_SIZE_8BIT,
                          &config, 1, 100) != HAL_OK)
        return HAL_ERROR;

    if (HAL_I2C_Mem_Write(&hi2c1, BMP280_ADDR, 0xF4,
                          I2C_MEMADD_SIZE_8BIT,
                          &ctrl_meas, 1, 100) != HAL_OK)
        return HAL_ERROR;

    return HAL_OK;
}

static HAL_StatusTypeDef BMP280_ReadData(void){
    uint8_t data[6];

    if (HAL_I2C_Mem_Read(&hi2c1, BMP280_ADDR, 0xF7,
                         I2C_MEMADD_SIZE_8BIT,
                         data, 6, 100) != HAL_OK)
    {
        return HAL_ERROR;
    }

    int32_t adc_P =
        ((int32_t)data[0] << 12) |
        ((int32_t)data[1] << 4) |
        ((int32_t)data[2] >> 4);

    int32_t adc_T =
        ((int32_t)data[3] << 12) |
        ((int32_t)data[4] << 4) |
        ((int32_t)data[5] >> 4);

    bmp_temperature_centi = BMP280_CompensateTemperature(adc_T);
    bmp_pressure_pa = BMP280_CompensatePressure(adc_P);

    return HAL_OK;
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

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
  MX_I2C2_Init();
  /* USER CODE BEGIN 2 */
  DWT_Delay_Init();
  BMP280_Init();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

    while (1)
    {
        uint32_t cycle_start = HAL_GetTick();
        HAL_RTC_GetTime(&hrtc, &rtcTime, RTC_FORMAT_BIN);
        HAL_RTC_GetDate(&hrtc, &rtcDate, RTC_FORMAT_BIN);

        temperature = DS18B20_ReadTemperature();

        int32_t temp100 = (int32_t)(temperature * 100.0f);
        int32_t temp_abs = (temp100 < 0) ? -temp100 : temp100;
        char temp_sign = (temp100 < 0) ? '-' : '+';

        bmp_status = HAL_I2C_IsDeviceReady(&hi2c1,
          0x76 << 1, 3, 100);

        if (bmp_status == HAL_OK) {
            bmp_data_status = BMP280_ReadData();
        }

        if (bmp_status != HAL_OK) {
          HAL_I2C_DeInit(&hi2c1);
          HAL_Delay(2);
          MX_I2C1_Init();
          bmp_status = HAL_I2C_IsDeviceReady(&hi2c1,
          0x76 << 1, 3, 100);
        }

        if (bmp_status == HAL_OK) {
          bmp_read_status = HAL_I2C_Mem_Read(
            &hi2c1, 0x76 <<1, 0xD0,
            I2C_MEMADD_SIZE_8BIT, &bmp_chip_id,
            1, 100);
        }

        const char *bmp_text =
          (bmp_status == HAL_OK) ? "BMP280 I2C OK" : "BMP280 I2C FAIL";

        int len = snprintf(
            tx_buffer,
            sizeof(tx_buffer),
            "TIME %02u:%02u:%02u | TEMP_INT %c%ld.%02ld C | "
            "PRESS %lu.%02lu hPa | BMP_TEMP %ld.%02ld C \r\n",
            rtcTime.Hours,
            rtcTime.Minutes,
            rtcTime.Seconds,
            temp_sign,
            (long)(temp_abs / 100),
            (long)(temp_abs % 100),
            (unsigned long)(bmp_pressure_pa / 100),
            (unsigned long)(bmp_pressure_pa % 100),
            (long)(bmp_temperature_centi / 100),
            (long)(bmp_temperature_centi % 100)
        );

        if (len > 0)
        {
            uint16_t tx_len =
                (len < sizeof(tx_buffer))
                ? (uint16_t)len
                : (uint16_t)(sizeof(tx_buffer) - 1);

            HAL_UART_Transmit(
                &huart1,
                (uint8_t *)tx_buffer,
                tx_len,
                HAL_MAX_DELAY
            );
        }

        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);

        uint32_t elapsed = HAL_GetTick() - cycle_start;

        if (elapsed < 1000U) {
          HAL_Delay(1000U - elapsed);
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
  * @brief I2C2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C2_Init(void)
{

  /* USER CODE BEGIN I2C2_Init 0 */

  /* USER CODE END I2C2_Init 0 */

  /* USER CODE BEGIN I2C2_Init 1 */

  /* USER CODE END I2C2_Init 1 */
  hi2c2.Instance = I2C2;
  hi2c2.Init.ClockSpeed = 100000;
  hi2c2.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c2.Init.OwnAddress1 = 0;
  hi2c2.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c2.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c2.Init.OwnAddress2 = 0;
  hi2c2.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c2.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C2_Init 2 */

  /* USER CODE END I2C2_Init 2 */

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
  huart1.Init.BaudRate = 115200;
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
