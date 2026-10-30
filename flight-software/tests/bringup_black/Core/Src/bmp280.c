#include "bmp280.h"

#define BMP280_I2C_ADDRESS      (0x76U << 1)
#define BMP280_EXPECTED_CHIP_ID 0x58U
#define BMP280_REGISTER_CHIP_ID 0xD0U
#define BMP280_REGISTER_CALIB   0x88U
#define BMP280_REGISTER_DATA    0xF7U
#define BMP280_REGISTER_CONFIG  0xF5U
#define BMP280_REGISTER_CONTROL 0xF4U
#define BMP280_I2C_TIMEOUT_MS   10U
#define BMP280_READY_TRIALS     1U

typedef struct {
    uint16_t t1;
    int16_t t2;
    int16_t t3;
    uint16_t p1;
    int16_t p2;
    int16_t p3;
    int16_t p4;
    int16_t p5;
    int16_t p6;
    int16_t p7;
    int16_t p8;
    int16_t p9;
} BMP280_Calibration;

static BMP280_Calibration calibration;
static int32_t temperature_fine;
static uint8_t initialized;

static uint16_t read_u16_le(const uint8_t *bytes) {
    return (uint16_t)bytes[0] | ((uint16_t)bytes[1] << 8);
}

static int16_t read_i16_le(const uint8_t *bytes) {
    return (int16_t)read_u16_le(bytes);
}

static HAL_StatusTypeDef read_calibration(I2C_HandleTypeDef *i2c) {
    uint8_t bytes[24];

    if (HAL_I2C_Mem_Read(i2c,
                         BMP280_I2C_ADDRESS,
                         BMP280_REGISTER_CALIB,
                         I2C_MEMADD_SIZE_8BIT,
                         bytes,
                         sizeof(bytes),
                         BMP280_I2C_TIMEOUT_MS) != HAL_OK) {
        return HAL_ERROR;
    }

    calibration.t1 = read_u16_le(&bytes[0]);
    calibration.t2 = read_i16_le(&bytes[2]);
    calibration.t3 = read_i16_le(&bytes[4]);
    calibration.p1 = read_u16_le(&bytes[6]);
    calibration.p2 = read_i16_le(&bytes[8]);
    calibration.p3 = read_i16_le(&bytes[10]);
    calibration.p4 = read_i16_le(&bytes[12]);
    calibration.p5 = read_i16_le(&bytes[14]);
    calibration.p6 = read_i16_le(&bytes[16]);
    calibration.p7 = read_i16_le(&bytes[18]);
    calibration.p8 = read_i16_le(&bytes[20]);
    calibration.p9 = read_i16_le(&bytes[22]);

    if ((calibration.t1 == 0U) || (calibration.t1 == UINT16_MAX) || (calibration.p1 == 0U) ||
        (calibration.p1 == UINT16_MAX)) {
        return HAL_ERROR;
    }

    return HAL_OK;
}

static int32_t compensate_temperature(int32_t raw_temperature) {
    int32_t var1;
    int32_t var2;

    var1 = ((((raw_temperature >> 3) - ((int32_t)calibration.t1 * 2)) * (int32_t)calibration.t2) >> 11);
    var2 = (((((raw_temperature >> 4) - (int32_t)calibration.t1) *
              ((raw_temperature >> 4) - (int32_t)calibration.t1)) >>
             12) *
            (int32_t)calibration.t3) >>
           14;

    temperature_fine = var1 + var2;
    return (temperature_fine * 5 + 128) >> 8;
}

static uint32_t compensate_pressure(int32_t raw_pressure) {
    int64_t var1;
    int64_t var2;
    int64_t pressure;

    var1 = (int64_t)temperature_fine - 128000;
    var2 = var1 * var1 * (int64_t)calibration.p6;
    var2 += var1 * (int64_t)calibration.p5 * 131072;
    var2 += (int64_t)calibration.p4 * 34359738368LL;
    var1 = ((var1 * var1 * (int64_t)calibration.p3) >> 8) + (var1 * (int64_t)calibration.p2 * 4096);
    var1 = ((((int64_t)1 << 47) + var1) * (int64_t)calibration.p1) >> 33;

    if (var1 == 0) {
        return 0U;
    }

    pressure = 1048576 - raw_pressure;
    pressure = (((pressure << 31) - var2) * 3125) / var1;
    var1 = ((int64_t)calibration.p9 * (pressure >> 13) * (pressure >> 13)) >> 25;
    var2 = ((int64_t)calibration.p8 * pressure) >> 19;
    pressure = ((pressure + var1 + var2) >> 8) + ((int64_t)calibration.p7 * 16);

    if (pressure <= 0) {
        return 0U;
    }

    return (uint32_t)(pressure >> 8);
}

HAL_StatusTypeDef BMP280_Init(I2C_HandleTypeDef *i2c) {
    uint8_t chip_id = 0U;
    uint8_t config = 0x40U;
    uint8_t control = 0x2FU;

    initialized = 0U;
    if ((i2c == NULL) ||
        (HAL_I2C_IsDeviceReady(i2c, BMP280_I2C_ADDRESS, BMP280_READY_TRIALS, BMP280_I2C_TIMEOUT_MS) != HAL_OK) ||
        (HAL_I2C_Mem_Read(i2c,
                          BMP280_I2C_ADDRESS,
                          BMP280_REGISTER_CHIP_ID,
                          I2C_MEMADD_SIZE_8BIT,
                          &chip_id,
                          1U,
                          BMP280_I2C_TIMEOUT_MS) != HAL_OK) ||
        (chip_id != BMP280_EXPECTED_CHIP_ID) || (read_calibration(i2c) != HAL_OK) ||
        (HAL_I2C_Mem_Write(i2c,
                           BMP280_I2C_ADDRESS,
                           BMP280_REGISTER_CONFIG,
                           I2C_MEMADD_SIZE_8BIT,
                           &config,
                           1U,
                           BMP280_I2C_TIMEOUT_MS) != HAL_OK) ||
        (HAL_I2C_Mem_Write(i2c,
                           BMP280_I2C_ADDRESS,
                           BMP280_REGISTER_CONTROL,
                           I2C_MEMADD_SIZE_8BIT,
                           &control,
                           1U,
                           BMP280_I2C_TIMEOUT_MS) != HAL_OK)) {
        return HAL_ERROR;
    }

    initialized = 1U;
    return HAL_OK;
}

void BMP280_Invalidate(void) {
    initialized = 0U;
}

HAL_StatusTypeDef BMP280_Read(I2C_HandleTypeDef *i2c, BMP280_Data *data) {
    uint8_t bytes[6];
    int32_t raw_pressure;
    int32_t raw_temperature;
    BMP280_Data sample;

    if ((i2c == NULL) || (data == NULL) || (initialized == 0U) ||
        (HAL_I2C_Mem_Read(i2c,
                          BMP280_I2C_ADDRESS,
                          BMP280_REGISTER_DATA,
                          I2C_MEMADD_SIZE_8BIT,
                          bytes,
                          sizeof(bytes),
                          BMP280_I2C_TIMEOUT_MS) != HAL_OK)) {
        return HAL_ERROR;
    }

    raw_pressure = ((int32_t)bytes[0] << 12) | ((int32_t)bytes[1] << 4) | ((int32_t)bytes[2] >> 4);
    raw_temperature = ((int32_t)bytes[3] << 12) | ((int32_t)bytes[4] << 4) | ((int32_t)bytes[5] >> 4);

    if ((raw_pressure == 0x80000L) || (raw_temperature == 0x80000L)) {
        return HAL_ERROR;
    }

    sample.temperature_centi_c = compensate_temperature(raw_temperature);
    sample.pressure_pa = compensate_pressure(raw_pressure);
    if (sample.pressure_pa == 0U) {
        return HAL_ERROR;
    }

    *data = sample;
    return HAL_OK;
}
