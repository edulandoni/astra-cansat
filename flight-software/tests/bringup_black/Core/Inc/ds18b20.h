#ifndef DS18B20_H
#define DS18B20_H

#include "stm32f4xx_hal.h"

HAL_StatusTypeDef DS18B20_Init(void);
HAL_StatusTypeDef DS18B20_ReadTemperature(float *temperature_c);

#endif /* DS18B20_H */
