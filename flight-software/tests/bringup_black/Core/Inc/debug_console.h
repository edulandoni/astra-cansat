#ifndef DEBUG_CONSOLE_H
#define DEBUG_CONSOLE_H

#include "flight_data.h"
#include "i2c_bus_manager.h"
#include "stm32f4xx_hal.h"

#include <stdbool.h>
#include <stdint.h>

void DebugConsole_Init(UART_HandleTypeDef *uart);
void DebugConsole_Process(void);
HAL_StatusTypeDef DebugConsole_Write(const char *message);
bool DebugConsole_ReadCommand(uint8_t *command);
void DebugConsole_ShowDashboard(const FlightDataSnapshot *data,
                                const I2cBusStatus *i2c_status,
                                bool rtc_time_valid,
                                RTC_HandleTypeDef *rtc);
void DebugConsole_TxComplete(UART_HandleTypeDef *uart);
void DebugConsole_UartError(UART_HandleTypeDef *uart);

#endif /* DEBUG_CONSOLE_H */
