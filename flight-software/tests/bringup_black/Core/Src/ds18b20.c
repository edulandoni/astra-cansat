#include "ds18b20.h"

#include "main.h"

#include <stdint.h>

#define DS18B20_CMD_SKIP_ROM        0xCCU
#define DS18B20_CMD_CONVERT         0x44U
#define DS18B20_CMD_READ_SCRATCHPAD 0xBEU
#define DS18B20_CONVERSION_TIME_MS  750U

static void delay_us(uint32_t microseconds)
{
  const uint32_t ticks_per_us = SystemCoreClock / 1000000U;
  const uint32_t start = DWT->CYCCNT;
  const uint32_t delay_ticks = microseconds * ticks_per_us;

  while ((DWT->CYCCNT - start) < delay_ticks)
  {
    __NOP();
  }
}

static void drive_low(void)
{
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_RESET);
}

static void release_bus(void)
{
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
}

static uint8_t reset_bus(void)
{
  uint8_t present;

  drive_low();
  delay_us(480U);
  release_bus();
  delay_us(70U);
  present = (HAL_GPIO_ReadPin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin) ==
             GPIO_PIN_RESET);
  delay_us(410U);
  return present;
}

static void write_bit(uint8_t bit)
{
  drive_low();
  if (bit != 0U)
  {
    delay_us(6U);
    release_bus();
    delay_us(64U);
  }
  else
  {
    delay_us(60U);
    release_bus();
    delay_us(10U);
  }
}

static uint8_t read_bit(void)
{
  uint8_t bit;

  drive_low();
  delay_us(3U);
  release_bus();
  delay_us(10U);
  bit = (uint8_t)HAL_GPIO_ReadPin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin);
  delay_us(53U);
  return bit;
}

static void write_byte(uint8_t byte)
{
  uint8_t bit_index;

  for (bit_index = 0U; bit_index < 8U; ++bit_index)
  {
    write_bit(byte & 0x01U);
    byte >>= 1;
  }
}

static uint8_t read_byte(void)
{
  uint8_t byte = 0U;
  uint8_t bit_index;

  for (bit_index = 0U; bit_index < 8U; ++bit_index)
  {
    if (read_bit() != 0U)
    {
      byte |= (uint8_t)(1U << bit_index);
    }
  }

  return byte;
}

static uint8_t crc8(const uint8_t *data, uint8_t length)
{
  uint8_t crc = 0U;
  uint8_t byte_index;

  for (byte_index = 0U; byte_index < length; ++byte_index)
  {
    uint8_t value = data[byte_index];
    uint8_t bit_index;

    for (bit_index = 0U; bit_index < 8U; ++bit_index)
    {
      const uint8_t mix = (crc ^ value) & 0x01U;
      crc >>= 1;
      if (mix != 0U)
      {
        crc ^= 0x8CU;
      }
      value >>= 1;
    }
  }

  return crc;
}

HAL_StatusTypeDef DS18B20_Init(void)
{
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
  DWT->CYCCNT = 0U;
  DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;

  return ((DWT->CTRL & DWT_CTRL_CYCCNTENA_Msk) != 0U) ? HAL_OK : HAL_ERROR;
}

HAL_StatusTypeDef DS18B20_ReadTemperature(float *temperature_c)
{
  uint8_t scratchpad[9];
  uint8_t index;
  int16_t raw_temperature;

  if ((temperature_c == NULL) || (reset_bus() == 0U))
  {
    return HAL_ERROR;
  }

  write_byte(DS18B20_CMD_SKIP_ROM);
  write_byte(DS18B20_CMD_CONVERT);
  HAL_Delay(DS18B20_CONVERSION_TIME_MS);

  if (reset_bus() == 0U)
  {
    return HAL_ERROR;
  }

  write_byte(DS18B20_CMD_SKIP_ROM);
  write_byte(DS18B20_CMD_READ_SCRATCHPAD);
  for (index = 0U; index < sizeof(scratchpad); ++index)
  {
    scratchpad[index] = read_byte();
  }

  if (crc8(scratchpad, 8U) != scratchpad[8])
  {
    return HAL_ERROR;
  }

  raw_temperature = (int16_t)(((uint16_t)scratchpad[1] << 8) |
                              (uint16_t)scratchpad[0]);
  *temperature_c = (float)raw_temperature / 16.0f;
  return HAL_OK;
}
