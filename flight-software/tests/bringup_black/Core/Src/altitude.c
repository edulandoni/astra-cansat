#include "altitude.h"

#include <math.h>

#define ALTITUDE_BACKUP_MAGIC       0x5A45524FU
#define ALTITUDE_MIN_PRESSURE_PA    30000U
#define ALTITUDE_MAX_PRESSURE_PA    120000U
#define ALTITUDE_SEA_LEVEL_SCALE_M  44330.0f
#define ALTITUDE_PRESSURE_EXPONENT  0.19029495f

static uint8_t pressure_is_plausible(uint32_t pressure_pa)
{
  return (pressure_pa >= ALTITUDE_MIN_PRESSURE_PA) &&
         (pressure_pa <= ALTITUDE_MAX_PRESSURE_PA);
}

void Altitude_LoadReference(RTC_HandleTypeDef *rtc,
                            Altitude_Reference *reference)
{
  uint32_t stored_pressure;

  if (reference == NULL)
  {
    return;
  }

  reference->reference_pressure_pa = 0U;
  reference->valid = 0U;
  if ((rtc == NULL) ||
      (HAL_RTCEx_BKUPRead(rtc, RTC_BKP_DR2) != ALTITUDE_BACKUP_MAGIC))
  {
    return;
  }

  stored_pressure = HAL_RTCEx_BKUPRead(rtc, RTC_BKP_DR1);
  if (pressure_is_plausible(stored_pressure) != 0U)
  {
    reference->reference_pressure_pa = stored_pressure;
    reference->valid = 1U;
  }
}

HAL_StatusTypeDef Altitude_SaveReference(RTC_HandleTypeDef *rtc,
                                        Altitude_Reference *reference,
                                        uint32_t pressure_pa)
{
  if ((rtc == NULL) || (reference == NULL) ||
      (pressure_is_plausible(pressure_pa) == 0U))
  {
    return HAL_ERROR;
  }

  HAL_RTCEx_BKUPWrite(rtc, RTC_BKP_DR1, pressure_pa);
  HAL_RTCEx_BKUPWrite(rtc, RTC_BKP_DR2, ALTITUDE_BACKUP_MAGIC);
  if ((HAL_RTCEx_BKUPRead(rtc, RTC_BKP_DR1) != pressure_pa) ||
      (HAL_RTCEx_BKUPRead(rtc, RTC_BKP_DR2) != ALTITUDE_BACKUP_MAGIC))
  {
    return HAL_ERROR;
  }

  reference->reference_pressure_pa = pressure_pa;
  reference->valid = 1U;
  return HAL_OK;
}

HAL_StatusTypeDef Altitude_Calculate(const Altitude_Reference *reference,
                                    uint32_t pressure_pa,
                                    float *altitude_m)
{
  float pressure_ratio;
  float result;

  if ((reference == NULL) || (altitude_m == NULL) ||
      (reference->valid == 0U) ||
      (pressure_is_plausible(reference->reference_pressure_pa) == 0U) ||
      (pressure_is_plausible(pressure_pa) == 0U))
  {
    return HAL_ERROR;
  }

  pressure_ratio = (float)pressure_pa /
                   (float)reference->reference_pressure_pa;
  result = ALTITUDE_SEA_LEVEL_SCALE_M *
           (1.0f - powf(pressure_ratio, ALTITUDE_PRESSURE_EXPONENT));
  if (!isfinite(result))
  {
    return HAL_ERROR;
  }

  *altitude_m = result;
  return HAL_OK;
}
