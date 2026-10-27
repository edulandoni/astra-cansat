#ifndef BMP280_H
#define BMP280_H

#include "stm32f4xx_hal.h"

#include <stdint.h>

typedef struct
{
  int32_t temperature_centi_c;
  uint32_t pressure_pa;
} BMP280_Data;

HAL_StatusTypeDef BMP280_Init(I2C_HandleTypeDef *i2c);
HAL_StatusTypeDef BMP280_Read(I2C_HandleTypeDef *i2c, BMP280_Data *data);

#endif /* BMP280_H */
