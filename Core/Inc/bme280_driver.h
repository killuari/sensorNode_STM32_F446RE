#ifndef BME280_DRIVER_H
#define BME280_DRIVER_H

#include "stm32f4xx_hal.h"

// 1. Die Initialisierung (weckt den Sensor auf)
void BME280_Init(I2C_HandleTypeDef *hi2c);

// 2. Die reine Datenbeschaffung (Burst Read von 0xF7 bis 0xFE)
HAL_StatusTypeDef BME280_ReadRawData(uint8_t *raw_data_array);

// 3. Die Konvertierungen (nehmen die Rohdaten und machen Menschen-Zahlen daraus)
float BME280_CalculateTemperature(uint8_t *raw_data);
float BME280_CalculatePressure(uint8_t *raw_data);
float BME280_CalculateHumidity(uint8_t *raw_data);

#endif