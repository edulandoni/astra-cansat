#include "ina3221.h"

#include <string.h>

#define INA3221_ADDRESS_FIRST             0x40U
#define INA3221_ADDRESS_LAST              0x43U
#define INA3221_REGISTER_CONFIG           0x00U
#define INA3221_REGISTER_SHUNT_CH1        0x01U
#define INA3221_REGISTER_BUS_CH1          0x02U
#define INA3221_REGISTER_BUS_CH2          0x04U
#define INA3221_REGISTER_MANUFACTURER_ID  0xFEU
#define INA3221_REGISTER_DIE_ID           0xFFU
#define INA3221_MANUFACTURER_ID           0x5449U
#define INA3221_DIE_ID                    0x3220U
#define INA3221_CONFIG_CH1_CH2_CONTINUOUS 0x6127U
#define INA3221_I2C_TIMEOUT_MS            20U
#define INA3221_BUS_LSB_MV                8
#define INA3221_SHUNT_LSB_UV              40
#define INA3221_BUS_MAX_MV                26000

static HAL_StatusTypeDef ReadRegister(const INA3221_Handle *device, uint8_t reg, uint16_t *value) {
    uint8_t bytes[2];

    if ((device == NULL) || (device->i2c == NULL) || (value == NULL) ||
        (device->address_7bit == INA3221_ADDRESS_NOT_DETECTED)) {
        return HAL_ERROR;
    }

    if (HAL_I2C_Mem_Read(device->i2c,
                         (uint16_t)(device->address_7bit << 1U),
                         reg,
                         I2C_MEMADD_SIZE_8BIT,
                         bytes,
                         sizeof(bytes),
                         INA3221_I2C_TIMEOUT_MS) != HAL_OK) {
        return HAL_ERROR;
    }

    *value = (uint16_t)(((uint16_t)bytes[0] << 8U) | bytes[1]);
    return HAL_OK;
}

static HAL_StatusTypeDef WriteRegister(const INA3221_Handle *device, uint8_t reg, uint16_t value) {
    uint8_t bytes[2] = {(uint8_t)(value >> 8U), (uint8_t)value};

    if ((device == NULL) || (device->i2c == NULL) || (device->address_7bit == INA3221_ADDRESS_NOT_DETECTED)) {
        return HAL_ERROR;
    }

    return HAL_I2C_Mem_Write(device->i2c,
                             (uint16_t)(device->address_7bit << 1U),
                             reg,
                             I2C_MEMADD_SIZE_8BIT,
                             bytes,
                             sizeof(bytes),
                             INA3221_I2C_TIMEOUT_MS);
}

static int32_t DecodeBusMillivolts(uint16_t raw) {
    return (int32_t)((raw >> 3U) * INA3221_BUS_LSB_MV);
}

static int32_t DecodeShuntMicrovolts(uint16_t raw) {
    int32_t signed_raw = (int16_t)raw;

    return (signed_raw / 8) * INA3221_SHUNT_LSB_UV;
}

HAL_StatusTypeDef INA3221_Init(INA3221_Handle *device, I2C_HandleTypeDef *i2c) {
    uint8_t address;

    if ((device == NULL) || (i2c == NULL)) {
        return HAL_ERROR;
    }

    memset(device, 0, sizeof(*device));
    device->i2c = i2c;
    device->address_7bit = INA3221_ADDRESS_NOT_DETECTED;

    for (address = INA3221_ADDRESS_FIRST; address <= INA3221_ADDRESS_LAST; ++address) {
        uint16_t manufacturer_id;
        uint16_t die_id;

        device->address_7bit = address;
        if ((HAL_I2C_IsDeviceReady(i2c, (uint16_t)(address << 1U), 1U, INA3221_I2C_TIMEOUT_MS) == HAL_OK) &&
            (ReadRegister(device, INA3221_REGISTER_MANUFACTURER_ID, &manufacturer_id) == HAL_OK) &&
            (ReadRegister(device, INA3221_REGISTER_DIE_ID, &die_id) == HAL_OK) &&
            (manufacturer_id == INA3221_MANUFACTURER_ID) && (die_id == INA3221_DIE_ID) &&
            (WriteRegister(device, INA3221_REGISTER_CONFIG, INA3221_CONFIG_CH1_CH2_CONTINUOUS) == HAL_OK)) {
            device->ready = true;
            return HAL_OK;
        }
    }

    device->address_7bit = INA3221_ADDRESS_NOT_DETECTED;
    device->ready = false;
    return HAL_ERROR;
}

bool INA3221_IsReady(const INA3221_Handle *device) {
    return (device != NULL) && device->ready;
}

uint8_t INA3221_GetAddress(const INA3221_Handle *device) {
    return (device != NULL) ? device->address_7bit : INA3221_ADDRESS_NOT_DETECTED;
}

HAL_StatusTypeDef INA3221_Read(INA3221_Handle *device, uint32_t now_ms) {
    uint16_t bus_ch1_raw;
    uint16_t shunt_ch1_raw;
    uint16_t bus_ch2_raw;
    INA3221_Data sample = {0};

    if ((device == NULL) || !device->ready ||
        (ReadRegister(device, INA3221_REGISTER_BUS_CH1, &bus_ch1_raw) != HAL_OK) ||
        (ReadRegister(device, INA3221_REGISTER_SHUNT_CH1, &shunt_ch1_raw) != HAL_OK) ||
        (ReadRegister(device, INA3221_REGISTER_BUS_CH2, &bus_ch2_raw) != HAL_OK)) {
        if (device != NULL) {
            device->data.valid = false;
            device->ready = false;
        }
        return HAL_ERROR;
    }

    sample.battery_shunt_uV = DecodeShuntMicrovolts(shunt_ch1_raw);
    /* The bus register measures VIN1-. Add the shunt drop to estimate BAT+ at VIN1+. */
    sample.battery_voltage_mV = DecodeBusMillivolts(bus_ch1_raw) + (sample.battery_shunt_uV / 1000);
    sample.battery_current_mA = sample.battery_shunt_uV / (int32_t)INA3221_SHUNT_MILLIOHMS;
    sample.solar_voltage_mV = DecodeBusMillivolts(bus_ch2_raw);

    if ((sample.battery_voltage_mV < 0) || (sample.battery_voltage_mV > INA3221_BUS_MAX_MV) ||
        (sample.solar_voltage_mV < 0) || (sample.solar_voltage_mV > INA3221_BUS_MAX_MV)) {
        device->data.valid = false;
        return HAL_ERROR;
    }

    sample.timestamp_ms = now_ms;
    sample.valid = true;
    device->data = sample;
    return HAL_OK;
}

bool INA3221_IsDataFresh(const INA3221_Handle *device, uint32_t now_ms, uint32_t max_age_ms) {
    return (device != NULL) && device->data.valid && ((now_ms - device->data.timestamp_ms) <= max_age_ms);
}
