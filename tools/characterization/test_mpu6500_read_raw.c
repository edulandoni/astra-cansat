#include "mpu6500.h"

#include <stdbool.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

#define MPU6500_I2C_ADDRESS_FOR_TEST (0x68U << 1)
#define MPU6500_ACCEL_X_REGISTER_FOR_TEST 0x3BU
#define MPU6500_BURST_LENGTH 14U

static HAL_StatusTypeDef mock_read_status = HAL_OK;
static uint8_t mock_read_bytes[MPU6500_BURST_LENGTH];
static uint16_t observed_device_address;
static uint16_t observed_register_address;
static uint16_t observed_length;
static int failures;

static void Expect(bool condition, const char *message) {
    if (!condition) {
        (void)fprintf(stderr, "FAIL: %s\n", message);
        ++failures;
    }
}

static void EncodeI16Be(uint8_t *destination, int16_t value) {
    const uint16_t bits = (uint16_t)value;

    destination[0] = (uint8_t)(bits >> 8U);
    destination[1] = (uint8_t)bits;
}

static void SetSample(int16_t ax, int16_t ay, int16_t az, int16_t gx, int16_t gy, int16_t gz) {
    memset(mock_read_bytes, 0xA5, sizeof(mock_read_bytes));
    EncodeI16Be(&mock_read_bytes[0], ax);
    EncodeI16Be(&mock_read_bytes[2], ay);
    EncodeI16Be(&mock_read_bytes[4], az);
    EncodeI16Be(&mock_read_bytes[8], gx);
    EncodeI16Be(&mock_read_bytes[10], gy);
    EncodeI16Be(&mock_read_bytes[12], gz);
}

static void ExpectReadOk(const char *name,
                         int16_t ax,
                         int16_t ay,
                         int16_t az,
                         int16_t gx,
                         int16_t gy,
                         int16_t gz) {
    I2C_HandleTypeDef i2c = {0};
    MPU6500_RawData data = {0};

    SetSample(ax, ay, az, gx, gy, gz);
    mock_read_status = HAL_OK;
    observed_device_address = 0U;
    observed_register_address = 0U;
    observed_length = 0U;

    Expect(MPU6500_ReadRaw(&i2c, &data) == HAL_OK, name);
    Expect((data.accel_x == ax) && (data.accel_y == ay) && (data.accel_z == az) &&
               (data.gyro_x == gx) && (data.gyro_y == gy) && (data.gyro_z == gz),
           "successful transfer converts and copies all axes");
    Expect(observed_device_address == MPU6500_I2C_ADDRESS_FOR_TEST, "driver uses MPU6500 address");
    Expect(observed_register_address == MPU6500_ACCEL_X_REGISTER_FOR_TEST, "burst starts at ACCEL_XOUT_H");
    Expect(observed_length == MPU6500_BURST_LENGTH, "driver requests the full 14-byte burst");
}

static void TestTransportFailureDoesNotModifyOutput(void) {
    I2C_HandleTypeDef i2c = {0};
    const MPU6500_RawData sentinel = {123, -234, 345, -456, 567, -678};
    MPU6500_RawData data = sentinel;

    memset(mock_read_bytes, 0x00, sizeof(mock_read_bytes));
    mock_read_status = HAL_ERROR;
    Expect(MPU6500_ReadRaw(&i2c, &data) == HAL_ERROR, "transport failure returns HAL_ERROR");
    Expect(memcmp(&data, &sentinel, sizeof(data)) == 0, "transport failure leaves output unchanged");
}

static void TestNullArguments(void) {
    I2C_HandleTypeDef i2c = {0};
    MPU6500_RawData data = {0};

    Expect(MPU6500_ReadRaw(NULL, &data) == HAL_ERROR, "NULL I2C handle returns HAL_ERROR");
    Expect(MPU6500_ReadRaw(&i2c, NULL) == HAL_ERROR, "NULL output returns HAL_ERROR");
}

HAL_StatusTypeDef HAL_I2C_IsDeviceReady(I2C_HandleTypeDef *i2c,
                                        uint16_t device_address,
                                        uint32_t trials,
                                        uint32_t timeout_ms) {
    (void)i2c;
    (void)device_address;
    (void)trials;
    (void)timeout_ms;
    return HAL_OK;
}

HAL_StatusTypeDef HAL_I2C_Mem_Read(I2C_HandleTypeDef *i2c,
                                   uint16_t device_address,
                                   uint16_t register_address,
                                   uint16_t register_address_size,
                                   uint8_t *data,
                                   uint16_t length,
                                   uint32_t timeout_ms) {
    (void)i2c;
    (void)register_address_size;
    (void)timeout_ms;
    observed_device_address = device_address;
    observed_register_address = register_address;
    observed_length = length;
    if (mock_read_status == HAL_OK) {
        memcpy(data, mock_read_bytes, length);
    }
    return mock_read_status;
}

HAL_StatusTypeDef HAL_I2C_Mem_Write(I2C_HandleTypeDef *i2c,
                                    uint16_t device_address,
                                    uint16_t register_address,
                                    uint16_t register_address_size,
                                    uint8_t *data,
                                    uint16_t length,
                                    uint32_t timeout_ms) {
    (void)i2c;
    (void)device_address;
    (void)register_address;
    (void)register_address_size;
    (void)data;
    (void)length;
    (void)timeout_ms;
    return HAL_OK;
}

int main(void) {
    ExpectReadOk("gyro zero vector is valid", 100, -200, 300, 0, 0, 0);
    ExpectReadOk("gyro minus-one vector is valid", 100, -200, 300, -1, -1, -1);
    ExpectReadOk("accelerometer zero vector is valid", 0, 0, 0, 100, -200, 300);
    ExpectReadOk("accelerometer minus-one vector is valid", -1, -1, -1, 100, -200, 300);
    ExpectReadOk("signed extrema are valid", INT16_MIN, INT16_MAX, INT16_MIN,
                 INT16_MAX, INT16_MIN, INT16_MAX);
    TestTransportFailureDoesNotModifyOutput();
    TestNullArguments();

    return failures == 0 ? 0 : 1;
}
