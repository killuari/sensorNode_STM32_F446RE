# STM32 Environmental Sensor Node (BME280 + OLED)

![C](https://img.shields.io/badge/Language-C-blue.svg)
![Microcontroller](https://img.shields.io/badge/MCU-STM32F446RE-orange.svg)
![Framework](https://img.shields.io/badge/Framework-STM32Cube_HAL-lightgrey.svg)
![Build](https://img.shields.io/badge/Build-CMake-green.svg)

An embedded environmental monitoring system built on the STM32F4 platform. This project reads temperature, pressure, and humidity data from a **BME280** sensor and visualizes it in real-time on an **SSD1306/SH1106 OLED display**. It features a custom lightweight sensor driver, robust I2C error handling, and a modular CMake build architecture.

---

## Project Showcase

![Hardware Setup](docs/images/hardware_setup_placeholder.jpg)

---

## Key Features
* **Custom BME280 Driver:** A lightweight, custom-written C driver avoiding third-party libraries. Reads raw ADC values and performs 32-bit/64-bit compensation calculations.
* **OLED Visualization:** Uses an SSD1306 compatible library (adapted for SH1106 memory mapping) with an animated boot sequence and clean UI.
* **Robust Error Handling (Self-Healing):** Implements hot-plug detection. If the sensor or I2C connection is temporarily lost, the system logs an error via UART, gracefully waits, and automatically reinitializes once the connection is restored without requiring a hard reset.
---

## Hardware Requirements

* **Microcontroller:** STM32 Nucleo-64 (STM32F446RE used in this build)
* **Sensor:** BME280 (Temperature, Humidity, Pressure) via I2C
* **Display:** 1.3" or 0.96" OLED Display (SSD1306 or SH1106 controller) via I2C
* **Misc:** Breadboard, Jumper Wires

### Wiring Diagram

![Fritzing Wiring Diagram](docs/images/fritzing_diagram_placeholder.png)

### Pinout Configuration

| Component | Pin Function | STM32 Pin | Note |
| :--- | :--- | :--- | :--- |
| **BME280** | VIN (VCC) | 3V3 | Requires 3.3V|
| **BME280** | GND | GND | |
| **BME280** | SCL | PB8 (I2C1_SCL) | Check your specific CubeMX pinout |
| **BME280** | SDA | PB9 (I2C1_SDA) | Check your specific CubeMX pinout |
| **OLED** | VCC | 3V3 | |
| **OLED** | GND | GND | |
| **OLED** | SCL | PB8 (I2C1_SCL) | Shared I2C Bus |
| **OLED** | SDA | PB9 (I2C1_SDA) | Shared I2C Bus |

---

## Project Structure

This project uses a modern CMake approach, integrating STM32CubeMX generated code as a subdirectory to keep the main application clean.

```text
├── cmake/stm32cubemx/           # Auto-generated HAL and startup code (untouched)
├── Core/
│   ├── Inc/                     # Main application headers (main.h)
│   └── Src/                     # Main application logic (main.c)
├── Drivers/
└──   └── stm32-ssd1306/           # OLED driver library
```
---

## Installation and Build

### Prerequisites

* [Visual Studio Code](https://code.visualstudio.com/)
* [STM32 VS Code Extension](https://marketplace.visualstudio.com/items?itemName=stmicroelectronics.stm32-vscode-extension)
* ARM GNU Toolchain (`arm-none-eabi-gcc`)
* CMake build system

### Steps

1. **Clone the repository:**
```bash
git clone [https://github.com/YourUsername/STM32-Environmental-Node.git](https://github.com/YourUsername/STM32-Environmental-Node.git)
cd STM32-Environmental-Node

```


2. **Configure with CMake:**
Open the folder in VS Code. The STM32 extension or CMake Tools should automatically detect the `CMakeLists.txt`. Run the configuration step (or run `cmake -B build -G Ninja`).
3. **Build the Project:**
Click the "Build" button in the VS Code status bar (or run `cmake --build build`).
4. **Flash to Target:**
Connect your Nucleo board via USB. Use the VS Code STM32 Extension to "Flash" the device, or use STM32CubeProgrammer directly with the generated `.elf` or `.bin` file.

---

## 💻 Usage & Serial Output

1. Power the board.
2. The OLED will show an animated `Booting...` screen.
3. Open a Serial Monitor (e.g., PuTTY, TeraTerm, or VS Code Serial Monitor) and connect to the ST-Link Virtual COM port.
* **Baud Rate:** `115200`
* **Data Bits:** `8`
* **Parity:** `None`
* **Stop Bits:** `1`



**Example Serial Output:**

```text
Started BME280 Driver!
Temp: 24.50 C | Pressure: 1012.30 hPa | Humidity: 45.20 %
Temp: 24.52 C | Pressure: 1012.31 hPa | Humidity: 45.25 %
WARNING: Lost connection to the BME280 sensor!
-> Sensor reconnected and initialized!
Temp: 24.51 C | Pressure: 1012.30 hPa | Humidity: 45.22 %

```

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.