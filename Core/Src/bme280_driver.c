#include "bme280_driver.h"

void BME280_Init(I2C_HandleTypeDef *hi2c, BME280_Handle *dev) {
    // configure humidity (0xF2) -> Oversampling x1
    uint8_t hum_reg = 0x01;
    HAL_I2C_Mem_Write(hi2c, BME280_I2C_ADDR, 0xF2, 1, &hum_reg, 1, 100);

    // configure temp & press (0xF4) -> Oversampling x1, Normal Mode
    uint8_t meas_reg = 0x27; 
    HAL_I2C_Mem_Write(hi2c, BME280_I2C_ADDR, 0xF4, 1, &meas_reg, 1, 100);

    uint8_t dat1[26];
    uint8_t dat2[7];

    // --- BLOCK 1: T1-T3, P1-P9, H1 (register 0x88 - 0xA1) ---
    HAL_I2C_Mem_Read(hi2c, BME280_I2C_ADDR, 0x88, 1, dat1, 26, 100);

    // temperature
    dev->dig_T1 = (uint16_t)((dat1[1] << 8) | dat1[0]);
    dev->dig_T2 = (int16_t)((dat1[3] << 8) | dat1[2]);
    dev->dig_T3 = (int16_t)((dat1[5] << 8) | dat1[4]);

    // pressure
    dev->dig_P1 = (uint16_t)((dat1[7] << 8) | dat1[6]);
    dev->dig_P2 = (int16_t)((dat1[9] << 8) | dat1[8]);
    dev->dig_P3 = (int16_t)((dat1[11] << 8) | dat1[10]);
    dev->dig_P4 = (int16_t)((dat1[13] << 8) | dat1[12]);
    dev->dig_P5 = (int16_t)((dat1[15] << 8) | dat1[14]);
    dev->dig_P6 = (int16_t)((dat1[17] << 8) | dat1[16]);
    dev->dig_P7 = (int16_t)((dat1[19] << 8) | dat1[18]);
    dev->dig_P8 = (int16_t)((dat1[21] << 8) | dat1[20]);
    dev->dig_P9 = (int16_t)((dat1[23] << 8) | dat1[22]);

    // humidity part 1
    dev->dig_H1 = dat1[25];

    // --- BLOCK 2: H2-H6 (register 0xE1 - 0xE7) ---
    HAL_I2C_Mem_Read(hi2c, BME280_I2C_ADDR, 0xE1, 1, dat2, 7, 100);

    dev->dig_H2 = (int16_t)((dat2[1] << 8) | dat2[0]);
    dev->dig_H3 = dat2[2];
    
    // H4 und H5 teilen sich dat2[4] (Register 0xE5)
    // H4: MSB (0xE4) + lower 4 bits of 0xE5
    dev->dig_H4 = (int16_t)((dat2[3] << 4) | (dat2[4] & 0x0F));
    
    // H5: MSB (0xE6) + upper 4 bits of 0xE5
    dev->dig_H5 = (int16_t)((dat2[5] << 4) | (dat2[4] >> 4));
    
    dev->dig_H6 = (int8_t)dat2[6];
}

HAL_StatusTypeDef BME280_ReadRawData(I2C_HandleTypeDef *hi2c, uint8_t *raw_data_array) {
    // Burst Read 0xF7 - 0xFE
    return HAL_I2C_Mem_Read(hi2c, BME280_I2C_ADDR, 0xF7, 1, raw_data_array, 8, 100);
}

float BME280_CalculateTemperature(uint8_t *raw_data, BME280_Handle *dev) {
    // raw data of 3 Bytes (20-bit)
    // raw[3]=MSB, raw[4]=LSB, raw[5]=XLSB
    int32_t adc_T = (int32_t)((raw_data[3] << 12) | (raw_data[4] << 4) | (raw_data[5] >> 4));

    // formula by datasheet
    float var1, var2, T;
    var1 = (((float)adc_T) / 16384.0f - ((float)dev->dig_T1) / 1024.0f) * ((float)dev->dig_T2);
    var2 = ((((float)adc_T) / 131072.0f - ((float)dev->dig_T1) / 8192.0f) *
            (((float)adc_T) / 131072.0f - ((float)dev->dig_T1) / 8192.0f)) * ((float)dev->dig_T3);
    
    dev->t_fine = (int32_t)(var1 + var2); // essential for pressure and humidity
    T = (var1 + var2) / 5120.0f;
    
    return T;
}

float BME280_CalculatePressure(uint8_t *raw_data, BME280_Handle *dev) {
    // raw data
    // raw[0]=MSB, raw[1]=LSB, raw[2]=XLSB
    int32_t adc_P = (int32_t)((raw_data[0] << 12) | (raw_data[1] << 4) | (raw_data[2] >> 4));

    // formula
    float var1, var2, p;
    var1 = ((float)dev->t_fine / 2.0f) - 64000.0f;
    var2 = var1 * var1 * ((float)dev->dig_P6) / 32768.0f;
    var2 = var2 + var1 * ((float)dev->dig_P5) * 2.0f;
    var2 = (var2 / 4.0f) + ((float)dev->dig_P4 * 65536.0f);
    var1 = (((float)dev->dig_P3 * var1 * var1 / 524288.0f) + ((float)dev->dig_P2 * var1)) / 524288.0f;
    var1 = (1.0f + var1 / 32768.0f) * ((float)dev->dig_P1);

    if (var1 == 0.0f) return 0; // do not divide by zero

    p = 1048576.0f - (float)adc_P;
    p = (p - (var2 / 4096.0f)) * 6250.0f / var1;
    var1 = ((float)dev->dig_P9) * p * p / 2147483648.0f;
    var2 = p * ((float)dev->dig_P8) / 32768.0f;
    p = p + (var1 + var2 + ((float)dev->dig_P7)) / 16.0f;

    return p / 100.0f; // result in hPa
}

float BME280_CalculateHumidity(uint8_t *raw_data, BME280_Handle *dev) {
    // raw data
    // raw[6]=MSB, raw[7]=LSB
    int32_t adc_H = (int32_t)((raw_data[6] << 8) | raw_data[7]);

    // formula
    float h = (((float)dev->t_fine) - 76800.0f);
    h = (adc_H - (((float)dev->dig_H4) * 64.0f + ((float)dev->dig_H5) / 16384.0f * h)) *
        (((float)dev->dig_H2) / 65536.0f * (1.0f + ((float)dev->dig_H6) / 67108864.0f * h *
        (1.0f + ((float)dev->dig_H3) / 67108864.0f * h)));
    h = h * (1.0f - ((float)dev->dig_H1) * h / 524288.0f);

    if (h > 100.0f) h = 100.0f;
    if (h < 0.0f) h = 0.0f;

    return h; // result in % relative humidity
}