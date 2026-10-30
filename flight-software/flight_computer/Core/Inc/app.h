#ifndef APP_H
#define APP_H

#include "stm32f4xx_hal.h"

#include <stdbool.h>

void App_Init(I2C_HandleTypeDef *i2c,
              RTC_HandleTypeDef *rtc,
              UART_HandleTypeDef *gps_uart,
              UART_HandleTypeDef *debug_uart);
void App_Process(void);
bool App_IsRtcTimeValid(void);
HAL_StatusTypeDef App_SetMissionRtc(const RTC_TimeTypeDef *time, const RTC_DateTypeDef *date);
void App_UartTxComplete(UART_HandleTypeDef *uart);
void App_UartRxComplete(UART_HandleTypeDef *uart);
void App_UartError(UART_HandleTypeDef *uart);

#endif /* APP_H */
