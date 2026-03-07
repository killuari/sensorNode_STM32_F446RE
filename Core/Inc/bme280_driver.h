#ifndef BME280_DRIVER_H
#define BME280_DRIVER_H

#define BME280_I2C_ADDR (0x76 << 1)

#include "stm32f4xx_hal.h"

typedef struct {
    uint16_t dig_T1;
    int16_t  dig_T2;
    int16_t  dig_T3;

    uint16_t dig_P1;
    int16_t  dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9;

    uint8_t  dig_H1;
    int16_t  dig_H2;
    uint8_t  dig_H3;
    int16_t  dig_H4, dig_H5;
    int8_t   dig_H6;
} BME280_CalibData;

// initialize sensor (wake from sleep mode)
void BME280_Init(I2C_HandleTypeDef *hi2c, BME280_CalibData *calib);

// burst read 0xF7 to 0xFE
HAL_StatusTypeDef BME280_ReadRawData(uint8_t *raw_data_array);

// convert raw data to readable data
float BME280_CalculateTemperature(uint8_t *raw_data);
float BME280_CalculatePressure(uint8_t *raw_data);
float BME280_CalculateHumidity(uint8_t *raw_data);

#endif