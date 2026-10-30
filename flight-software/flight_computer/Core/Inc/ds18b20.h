#ifndef DS18B20_H
#define DS18B20_H

#include "stm32f4xx_hal.h"

#define DS18B20_CONVERSION_TIME_MS 750U

HAL_StatusTypeDef DS18B20_Init(void);
HAL_StatusTypeDef DS18B20_StartConversion(void);
HAL_StatusTypeDef DS18B20_ReadConversion(float *temperature_c);

#endif /* DS18B20_H */
