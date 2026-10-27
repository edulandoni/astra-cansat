#ifndef ALTITUDE_H
#define ALTITUDE_H

#include "stm32f4xx_hal.h"

#include <stdint.h>

typedef struct
{
  uint32_t reference_pressure_pa;
  uint8_t valid;
} Altitude_Reference;

void Altitude_LoadReference(RTC_HandleTypeDef *rtc,
                            Altitude_Reference *reference);
HAL_StatusTypeDef Altitude_SaveReference(RTC_HandleTypeDef *rtc,
                                        Altitude_Reference *reference,
                                        uint32_t pressure_pa);
HAL_StatusTypeDef Altitude_Calculate(const Altitude_Reference *reference,
                                    uint32_t pressure_pa,
                                    float *altitude_m);

#endif /* ALTITUDE_H */
