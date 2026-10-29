#ifndef INA3221_H
#define INA3221_H

#include "stm32f4xx_hal.h"

#include <stdbool.h>
#include <stdint.h>

/*
 * The fitted shunts are marked R100. This is interpreted as 0.100 ohm,
 * but has not been verified electrically. Keep this value configurable.
 */
#define INA3221_SHUNT_MILLIOHMS      100U
#define INA3221_DATA_MAX_AGE_MS      2000U
#define INA3221_ADDRESS_NOT_DETECTED 0xFFU

typedef struct {
    int32_t battery_voltage_mV;
    int32_t battery_shunt_uV;
    int32_t battery_current_mA;
    int32_t solar_voltage_mV;
    uint32_t timestamp_ms;
    bool valid;
} INA3221_Data;

typedef struct {
    I2C_HandleTypeDef *i2c;
    INA3221_Data data;
    uint8_t address_7bit;
    bool ready;
} INA3221_Handle;

HAL_StatusTypeDef INA3221_Init(INA3221_Handle *device, I2C_HandleTypeDef *i2c);
bool INA3221_IsReady(const INA3221_Handle *device);
uint8_t INA3221_GetAddress(const INA3221_Handle *device);
HAL_StatusTypeDef INA3221_Read(INA3221_Handle *device, uint32_t now_ms);
bool INA3221_IsDataFresh(const INA3221_Handle *device, uint32_t now_ms, uint32_t max_age_ms);

#endif /* INA3221_H */
