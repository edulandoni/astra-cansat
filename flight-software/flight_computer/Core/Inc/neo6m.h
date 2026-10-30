#ifndef NEO6M_H
#define NEO6M_H

#include "stm32f4xx_hal.h"

#include <stdbool.h>
#include <stdint.h>

typedef struct {
    bool data_valid;
    bool fix_valid;
    bool utc_valid;
    uint8_t satellites;
    int32_t latitude_deg_e7;
    int32_t longitude_deg_e7;
    int32_t altitude_mm;
    uint8_t utc_hours;
    uint8_t utc_minutes;
    uint8_t utc_seconds;
    uint32_t last_update_ms;
    uint32_t last_fix_ms;
} NEO6M_Data;

HAL_StatusTypeDef NEO6M_Init(UART_HandleTypeDef *uart);
void NEO6M_Process(void);
bool NEO6M_GetData(NEO6M_Data *data);
bool NEO6M_IsUartActive(uint32_t now_ms, uint32_t maximum_age_ms);
bool NEO6M_IsDataFresh(const NEO6M_Data *data, uint32_t now_ms, uint32_t maximum_age_ms);

/* Call these only from the matching HAL UART callbacks. */
void NEO6M_UART_RxCpltCallback(UART_HandleTypeDef *uart);
void NEO6M_UART_ErrorCallback(UART_HandleTypeDef *uart);

#endif /* NEO6M_H */
