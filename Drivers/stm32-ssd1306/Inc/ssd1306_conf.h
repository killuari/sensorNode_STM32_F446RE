/**
 * Private configuration file for the SSD1306 library.
 * It is configured for STM32F0, I2C and including all fonts.
 */

#ifndef __SSD1306_CONF_H__
#define __SSD1306_CONF_H__

// Choose microcontroller family
#define STM32F4

// Choose I2C as bus
#define SSD1306_USE_I2C

// I2C Configuration
#define SSD1306_I2C_PORT        hi2c1
#define SSD1306_I2C_ADDR        (0x3C << 1)

// Include fonts
#define SSD1306_INCLUDE_FONT_7x10
#define SSD1306_INCLUDE_FONT_11x18

// adjust horizontal screen offset
#define SSD1306_X_OFFSET 2

#endif /* __SSD1306_CONF_H__ */