#ifndef STM32F4XX_HAL_H
#define STM32F4XX_HAL_H

#include <stdint.h>

typedef enum {
    HAL_OK = 0x00U,
    HAL_ERROR = 0x01U,
    HAL_BUSY = 0x02U,
    HAL_TIMEOUT = 0x03U
} HAL_StatusTypeDef;

typedef struct {
    uint32_t unused;
} I2C_HandleTypeDef;

#define I2C_MEMADD_SIZE_8BIT 1U

HAL_StatusTypeDef HAL_I2C_IsDeviceReady(I2C_HandleTypeDef *i2c,
                                        uint16_t device_address,
                                        uint32_t trials,
                                        uint32_t timeout_ms);
HAL_StatusTypeDef HAL_I2C_Mem_Read(I2C_HandleTypeDef *i2c,
                                   uint16_t device_address,
                                   uint16_t register_address,
                                   uint16_t register_address_size,
                                   uint8_t *data,
                                   uint16_t length,
                                   uint32_t timeout_ms);
HAL_StatusTypeDef HAL_I2C_Mem_Write(I2C_HandleTypeDef *i2c,
                                    uint16_t device_address,
                                    uint16_t register_address,
                                    uint16_t register_address_size,
                                    uint8_t *data,
                                    uint16_t length,
                                    uint32_t timeout_ms);

#endif /* STM32F4XX_HAL_H */
