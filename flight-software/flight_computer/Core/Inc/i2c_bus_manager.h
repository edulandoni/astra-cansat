#ifndef I2C_BUS_MANAGER_H
#define I2C_BUS_MANAGER_H

#include "stm32f4xx_hal.h"

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    I2C_BUS_HEALTH_OK,
    I2C_BUS_HEALTH_DEGRADED,
    I2C_BUS_HEALTH_RECOVERING
} I2cBusHealth;

typedef enum {
    I2C_FAULT_SOURCE_NONE = 0U,
    I2C_FAULT_SOURCE_MPU6500 = (1U << 0),
    I2C_FAULT_SOURCE_BMP280 = (1U << 1),
    I2C_FAULT_SOURCE_INA3221 = (1U << 2)
} I2cFaultSource;

typedef enum {
    I2C_STUCK_NONE,
    I2C_STUCK_SDA,
    I2C_STUCK_SCL,
    I2C_STUCK_BOTH
} I2cStuckState;

typedef struct {
    I2cBusHealth health;
    I2cStuckState last_stuck_state;
    uint16_t recovery_attempt_count;
    uint16_t recovery_success_count;
    uint32_t total_bus_errors;
    uint32_t last_hal_error;
} I2cBusStatus;

typedef void (*I2cBusRecoveryCallback)(uint32_t now_ms);

void I2cBusManager_Init(I2C_HandleTypeDef *i2c, I2cBusRecoveryCallback recovery_callback);
void I2cBusManager_Process(uint32_t now_ms);
void I2cBusManager_RecordFault(I2cFaultSource source, uint32_t error, uint32_t now_ms);
void I2cBusManager_RecordValidTransaction(uint32_t now_ms);
void I2cBusManager_GetStatus(I2cBusStatus *status);

#endif /* I2C_BUS_MANAGER_H */
