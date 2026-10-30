#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include "flight_data.h"
#include "stm32f4xx_hal.h"

#include <stdbool.h>
#include <stdint.h>

void SensorManager_Init(I2C_HandleTypeDef *i2c,
                        RTC_HandleTypeDef *rtc,
                        UART_HandleTypeDef *gps_uart,
                        uint32_t now_ms);
void SensorManager_ProcessContinuous(uint32_t now_ms);
void SensorManager_UpdateMpu6500(uint32_t now_ms);
bool SensorManager_UpdateBmp280(uint32_t now_ms);
void SensorManager_UpdateIna3221(uint32_t now_ms);
void SensorManager_StartDs18b20Conversion(uint32_t now_ms);
void SensorManager_StartAltitudeCalibration(void);
void SensorManager_ProcessAltitudeCalibrationSample(uint32_t now_ms, bool sample_valid);
void SensorManager_InvalidateI2cSensors(uint32_t now_ms);
void SensorManager_GetFlightData(uint32_t now_ms, FlightDataSnapshot *snapshot);
void SensorManager_GpsRxComplete(UART_HandleTypeDef *uart);
void SensorManager_GpsUartError(UART_HandleTypeDef *uart);

#endif /* SENSOR_MANAGER_H */
