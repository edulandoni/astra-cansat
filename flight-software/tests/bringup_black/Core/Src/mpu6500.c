#include "mpu6500.h"

#include <stdbool.h>
#include <stddef.h>

#define MPU6500_I2C_ADDRESS        (0x68U << 1)
#define MPU6500_REGISTER_WHO_AM_I  0x75U
#define MPU6500_REGISTER_PWR_MGMT  0x6BU
#define MPU6500_REGISTER_GYRO_CFG  0x1BU
#define MPU6500_REGISTER_ACCEL_CFG 0x1CU
#define MPU6500_REGISTER_ACCEL_X   0x3BU
#define MPU6500_I2C_TIMEOUT_MS     10U
#define MPU6500_READY_TRIALS       1U

static int16_t read_i16_be(const uint8_t *bytes) {
    return (int16_t) (((uint16_t) bytes[0] << 8) | (uint16_t) bytes[1]);
}

static bool bytes_are_all(const uint8_t *bytes, size_t length, uint8_t expected) {
    for (size_t index = 0U; index < length; ++index) {
        if (bytes[index] != expected) {
            return false;
        }
    }

    return true;
}

HAL_StatusTypeDef MPU6500_Detect(I2C_HandleTypeDef *i2c, uint8_t *who_am_i) {
    uint8_t identity = 0U;

    if ((i2c == NULL) ||
        (HAL_I2C_IsDeviceReady(i2c, MPU6500_I2C_ADDRESS, MPU6500_READY_TRIALS, MPU6500_I2C_TIMEOUT_MS) != HAL_OK) ||
        (HAL_I2C_Mem_Read(i2c,
                          MPU6500_I2C_ADDRESS,
                          MPU6500_REGISTER_WHO_AM_I,
                          I2C_MEMADD_SIZE_8BIT,
                          &identity,
                          1U,
                          MPU6500_I2C_TIMEOUT_MS) != HAL_OK)) {
        return HAL_ERROR;
    }

    if (who_am_i != NULL) {
        *who_am_i = identity;
    }

    return (identity == MPU6500_EXPECTED_WHO_AM_I) ? HAL_OK : HAL_ERROR;
}

HAL_StatusTypeDef MPU6500_BeginInitialization(I2C_HandleTypeDef *i2c) {
    uint8_t value = 0x01U;

    if (i2c == NULL) {
        return HAL_ERROR;
    }

    return HAL_I2C_Mem_Write(i2c,
                             MPU6500_I2C_ADDRESS,
                             MPU6500_REGISTER_PWR_MGMT,
                             I2C_MEMADD_SIZE_8BIT,
                             &value,
                             1U,
                             MPU6500_I2C_TIMEOUT_MS);
}

HAL_StatusTypeDef MPU6500_FinishInitialization(I2C_HandleTypeDef *i2c) {
    uint8_t value = 0x00U;

    if (i2c == NULL) {
        return HAL_ERROR;
    }

    /* FS_SEL=0 and AFS_SEL=0 preserve +/-250 dps and +/-2 g ranges. */
    if ((HAL_I2C_Mem_Write(i2c,
                           MPU6500_I2C_ADDRESS,
                           MPU6500_REGISTER_GYRO_CFG,
                           I2C_MEMADD_SIZE_8BIT,
                           &value,
                           1U,
                           MPU6500_I2C_TIMEOUT_MS) != HAL_OK) ||
        (HAL_I2C_Mem_Write(i2c,
                           MPU6500_I2C_ADDRESS,
                           MPU6500_REGISTER_ACCEL_CFG,
                           I2C_MEMADD_SIZE_8BIT,
                           &value,
                           1U,
                           MPU6500_I2C_TIMEOUT_MS) != HAL_OK)) {
        return HAL_ERROR;
    }

    return HAL_OK;
}

HAL_StatusTypeDef MPU6500_ReadRaw(I2C_HandleTypeDef *i2c, MPU6500_RawData *data) {
    uint8_t bytes[14];
    MPU6500_RawData sample;

    if ((i2c == NULL) || (data == NULL) ||
        (HAL_I2C_Mem_Read(i2c,
                          MPU6500_I2C_ADDRESS,
                          MPU6500_REGISTER_ACCEL_X,
                          I2C_MEMADD_SIZE_8BIT,
                          bytes,
                          sizeof(bytes),
                          MPU6500_I2C_TIMEOUT_MS) != HAL_OK)) {
        return HAL_ERROR;
    }

    if (bytes_are_all(&bytes[0], 6U, 0x00U) || bytes_are_all(&bytes[0], 6U, 0xFFU) ||
        bytes_are_all(&bytes[8], 6U, 0x00U) || bytes_are_all(&bytes[8], 6U, 0xFFU)) {
        return HAL_ERROR;
    }

    sample.accel_x = read_i16_be(&bytes[0]);
    sample.accel_y = read_i16_be(&bytes[2]);
    sample.accel_z = read_i16_be(&bytes[4]);
    sample.gyro_x = read_i16_be(&bytes[8]);
    sample.gyro_y = read_i16_be(&bytes[10]);
    sample.gyro_z = read_i16_be(&bytes[12]);
    *data = sample;

    return HAL_OK;
}
