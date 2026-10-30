#include "i2c_bus_manager.h"

#include "flight_config.h"
#include "main.h"

#include <limits.h>

typedef struct {
    I2C_HandleTypeDef *i2c;
    I2cBusRecoveryCallback recovery_callback;
    I2cBusHealth health;
    uint8_t recent_fault_sources;
    uint8_t recent_bus_error_count;
    I2cStuckState observed_stuck_state;
    I2cStuckState requested_stuck_state;
    I2cStuckState last_stuck_state;
    bool recovery_requested;
    bool recovery_pending;
    bool valid_transaction_since_fault;
    uint16_t recovery_attempt_count;
    uint16_t recovery_success_count;
    uint32_t window_start_ms;
    uint32_t stuck_since_ms;
    uint32_t total_bus_errors;
    uint32_t last_recovery_ms;
    uint32_t last_hal_error;
} I2cBusManagerState;

static I2cBusManagerState bus;

static void IncrementUint16Saturated(uint16_t *counter) {
    if (*counter < UINT16_MAX) {
        ++(*counter);
    }
}

static void IncrementUint32Saturated(uint32_t *counter) {
    if (*counter < UINT32_MAX) {
        ++(*counter);
    }
}

static bool ErrorIsBusLevel(uint32_t error) {
    const uint32_t bus_errors = HAL_I2C_ERROR_BERR | HAL_I2C_ERROR_ARLO | HAL_I2C_ERROR_TIMEOUT;

    return (error & bus_errors) != 0U;
}

static bool SdaIsLow(void) {
    return HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_9) == GPIO_PIN_RESET;
}

static bool SclIsLow(void) {
    return HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_8) == GPIO_PIN_RESET;
}

static I2cStuckState GetStuckState(void) {
    const bool sda_low = SdaIsLow();
    const bool scl_low = SclIsLow();

    if (sda_low && scl_low) {
        return I2C_STUCK_BOTH;
    }
    if (sda_low) {
        return I2C_STUCK_SDA;
    }
    if (scl_low) {
        return I2C_STUCK_SCL;
    }
    return I2C_STUCK_NONE;
}

static uint8_t CountFaultSources(uint8_t sources) {
    uint8_t count = 0U;

    while (sources != 0U) {
        count = (uint8_t)(count + (sources & 1U));
        sources >>= 1U;
    }
    return count;
}

static I2cStuckState InspectGpioLinesPersistently(void) {
    const I2cStuckState candidate = GetStuckState();

    if (candidate == I2C_STUCK_NONE) {
        return I2C_STUCK_NONE;
    }

    for (uint32_t sample = 0U; sample < 2U; ++sample) {
        HAL_Delay(1U);
        if (GetStuckState() != candidate) {
            return I2C_STUCK_NONE;
        }
    }
    return candidate;
}

static I2cStuckState RecoverStuckBusWithClockPulses(void) {
    GPIO_InitTypeDef gpio = {0};
    I2cStuckState stuck_state;

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8 | GPIO_PIN_9, GPIO_PIN_SET);
    gpio.Pin = GPIO_PIN_8 | GPIO_PIN_9;
    gpio.Mode = GPIO_MODE_OUTPUT_OD;
    gpio.Pull = GPIO_PULLUP;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &gpio);

    stuck_state = InspectGpioLinesPersistently();
    if (stuck_state == I2C_STUCK_SDA) {
        for (uint32_t pulse = 0U; (pulse < 9U) && SdaIsLow(); ++pulse) {
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_RESET);
            HAL_Delay(1U);
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_SET);
            HAL_Delay(1U);

            if (SclIsLow()) {
                stuck_state = SdaIsLow() ? I2C_STUCK_BOTH : I2C_STUCK_SCL;
                break;
            }
        }

        if (!SclIsLow()) {
            /* A STOP is safe only when SCL can actually be released high. */
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8 | GPIO_PIN_9, GPIO_PIN_RESET);
            HAL_Delay(1U);
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_SET);
            HAL_Delay(1U);
            if (!SclIsLow()) {
                HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_SET);
                HAL_Delay(1U);
            }
        }
    }

    /* A line held physically low is observable but cannot be released by clocking. */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_8 | GPIO_PIN_9);
    return stuck_state;
}

static void RecoverBus(uint32_t now_ms) {
    I2cStuckState inspected_stuck_state;

    bus.health = I2C_BUS_HEALTH_RECOVERING;
    bus.recovery_pending = true;
    bus.valid_transaction_since_fault = false;
    IncrementUint16Saturated(&bus.recovery_attempt_count);
    (void)HAL_I2C_DeInit(bus.i2c);
    inspected_stuck_state = RecoverStuckBusWithClockPulses();
    if (inspected_stuck_state != I2C_STUCK_NONE) {
        bus.last_stuck_state = inspected_stuck_state;
    } else if (bus.requested_stuck_state != I2C_STUCK_NONE) {
        bus.last_stuck_state = bus.requested_stuck_state;
    }

    /* The handle retains the CubeMX configuration across HAL_I2C_DeInit(). */
    if (HAL_I2C_Init(bus.i2c) != HAL_OK) {
        Error_Handler();
    }
    if (bus.recovery_callback != NULL) {
        bus.recovery_callback(now_ms);
    }

    bus.last_recovery_ms = now_ms;
    bus.recovery_requested = false;
    bus.observed_stuck_state = I2C_STUCK_NONE;
    bus.requested_stuck_state = I2C_STUCK_NONE;
    bus.recent_fault_sources = I2C_FAULT_SOURCE_NONE;
    bus.recent_bus_error_count = 0U;
    bus.window_start_ms = now_ms;
}

void I2cBusManager_Init(I2C_HandleTypeDef *i2c, I2cBusRecoveryCallback recovery_callback) {
    bus.i2c = i2c;
    bus.recovery_callback = recovery_callback;
    bus.health = I2C_BUS_HEALTH_OK;
}

void I2cBusManager_RecordFault(I2cFaultSource source, uint32_t error, uint32_t now_ms) {
    if (!ErrorIsBusLevel(error)) {
        return;
    }

    if ((bus.recent_bus_error_count == 0U) ||
        ((now_ms - bus.window_start_ms) > I2C_BUS_ERROR_WINDOW_MS)) {
        bus.window_start_ms = now_ms;
        bus.recent_fault_sources = I2C_FAULT_SOURCE_NONE;
        bus.recent_bus_error_count = 0U;
    }

    if (!bus.recovery_pending) {
        bus.health = I2C_BUS_HEALTH_DEGRADED;
    }
    bus.last_hal_error = error;
    bus.last_stuck_state = I2C_STUCK_NONE;
    bus.valid_transaction_since_fault = false;
    IncrementUint32Saturated(&bus.total_bus_errors);
    if (bus.recent_bus_error_count < UINT8_MAX) {
        ++bus.recent_bus_error_count;
    }
    bus.recent_fault_sources |= (uint8_t)source;

    /* Repeated faults from one device remain isolated to that device. */
    if (CountFaultSources(bus.recent_fault_sources) >= I2C_BUS_ERROR_SOURCE_THRESHOLD) {
        if (!bus.recovery_requested) {
            bus.requested_stuck_state = I2C_STUCK_NONE;
        }
        bus.recovery_requested = true;
    }
}

void I2cBusManager_RecordValidTransaction(uint32_t now_ms) {
    bus.valid_transaction_since_fault = true;
    if (bus.recovery_pending) {
        IncrementUint16Saturated(&bus.recovery_success_count);
        bus.recovery_pending = false;
        bus.health = I2C_BUS_HEALTH_DEGRADED;
        bus.window_start_ms = now_ms;
    }
}

void I2cBusManager_Process(uint32_t now_ms) {
    I2cStuckState stuck_state;

    if ((bus.health == I2C_BUS_HEALTH_DEGRADED) && bus.valid_transaction_since_fault &&
        !bus.recovery_requested && !bus.recovery_pending &&
        ((now_ms - bus.window_start_ms) > I2C_BUS_ERROR_WINDOW_MS)) {
        bus.recent_fault_sources = I2C_FAULT_SOURCE_NONE;
        bus.recent_bus_error_count = 0U;
        bus.health = I2C_BUS_HEALTH_OK;
    }

    /* I2C1 is synchronous; outside a driver transaction both lines should be high. */
    stuck_state = GetStuckState();
    if (stuck_state == I2C_STUCK_NONE) {
        bus.observed_stuck_state = I2C_STUCK_NONE;
    } else if (stuck_state != bus.observed_stuck_state) {
        bus.observed_stuck_state = stuck_state;
        bus.stuck_since_ms = now_ms;
    } else if (((now_ms - bus.stuck_since_ms) >= I2C_STUCK_CONFIRMATION_MS) &&
               !bus.recovery_requested) {
        bus.last_stuck_state = stuck_state;
        bus.requested_stuck_state = stuck_state;
        bus.valid_transaction_since_fault = false;
        IncrementUint32Saturated(&bus.total_bus_errors);
        bus.recovery_requested = true;
        if (!bus.recovery_pending) {
            bus.health = I2C_BUS_HEALTH_DEGRADED;
        }
    }

    if (!bus.recovery_requested) {
        return;
    }
    if ((bus.last_recovery_ms != 0U) &&
        ((now_ms - bus.last_recovery_ms) < I2C_RECOVERY_COOLDOWN_MS)) {
        return;
    }
    RecoverBus(now_ms);
}

void I2cBusManager_GetStatus(I2cBusStatus *status) {
    if (status == NULL) {
        return;
    }

    status->health = bus.health;
    status->last_stuck_state = bus.last_stuck_state;
    status->recovery_attempt_count = bus.recovery_attempt_count;
    status->recovery_success_count = bus.recovery_success_count;
    status->total_bus_errors = bus.total_bus_errors;
    status->last_hal_error = bus.last_hal_error;
}
