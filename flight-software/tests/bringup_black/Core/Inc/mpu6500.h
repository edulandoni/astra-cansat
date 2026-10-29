#ifndef MPU6500_H
#define MPU6500_H

#include "stm32f4xx_hal.h"

#include <stdint.h>

#define MPU6500_EXPECTED_WHO_AM_I 0x70U
#define MPU6500_STARTUP_TIME_MS    100U

typedef struct {
    int16_t accel_x;
    int16_t accel_y;
    int16_t accel_z;
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
} MPU6500_RawData;

HAL_StatusTypeDef MPU6500_Detect(I2C_HandleTypeDef *i2c, uint8_t *who_am_i);
HAL_StatusTypeDef MPU6500_BeginInitialization(I2C_HandleTypeDef *i2c);
HAL_StatusTypeDef MPU6500_FinishInitialization(I2C_HandleTypeDef *i2c);
HAL_StatusTypeDef MPU6500_ReadRaw(I2C_HandleTypeDef *i2c, MPU6500_RawData *data);

#endif /* MPU6500_H */
