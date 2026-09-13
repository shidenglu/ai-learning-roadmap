# SPI 总线

## 1. 什么是 SPI

SPI（Serial Peripheral Interface）是一种**同步、串行、全双工**通信总线，主要用于 MCU/SoC 与高速外设之间的数据通信。

典型设备：

```text
MCU
 │
 ├── Flash
 ├── ADC
 ├── DAC
 ├── LCD
 ├── Sensor
 └── FPGA
```

---

## 2. SPI 基本结构

SPI 通常由一个 Master 和一个或多个 Slave 组成：

```text
                MCU
              Master
                │
       ┌────────┼────────┐
       │        │        │
      MOSI     MISO     SCLK
       │        │        │
═══════╪════════╪════════╪════════ SPI BUS
       │        │        │
   ┌───┴───┐ ┌──┴───┐ ┌──┴───┐
   │Flash  │ │ ADC  │ │ LCD  │
   │ CS0   │ │ CS1  │ │ CS2  │
   └───────┘ └──────┘ └──────┘
```

---

## 3. SPI 四根信号线

| 信号    | 全称                  | 作用             |
| ----- | ------------------- | -------------- |
| MOSI  | Master Out Slave In | Master → Slave |
| MISO  | Master In Slave Out | Slave → Master |
| SCLK  | Serial Clock        | 时钟             |
| CS/SS | Chip Select         | 选择 Slave       |

其中：

```text
MOSI → 数据
MISO → 数据
SCLK → 时钟
CS   → 设备选择
```

---

## 4. SPI 通信过程

Master 首先拉低目标设备的 CS：

```text
CS = LOW
```

然后产生时钟：

```text
SCLK
 ┌─┐ ┌─┐ ┌─┐ ┌─┐
 └─┘ └─┘ └─┘ └─┘
```

同时进行数据传输：

```text
MOSI → → → → → Slave

MISO ← ← ← ← ← Slave
```

完成后：

```text
CS = HIGH
```

一次典型通信：

```text
CS
──────┐                    ┌────
      └────────────────────┘

SCLK
────┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐
    └─┘ └─┘ └─┘ └─┘

MOSI
─────── DATA ──────────────

MISO
─────── DATA ──────────────
```

---

## 5. SPI 是全双工

SPI 可以同时发送和接收：

```text
Master                    Slave

MOSI  ──────────────────►
      发送数据

MISO  ◄──────────────────
      接收数据
```

因此一个时钟周期可以同时完成：

```text
发送 1 bit
+
接收 1 bit
```

---

## 6. 多个 Slave

SPI 没有像 I2C 那样的设备地址。

通常使用独立的 CS：

```text
                 MCU
                  │
        ┌─────────┼─────────┐
        │         │         │
       CS0       CS1       CS2
        │         │         │
        ▼         ▼         ▼
      Flash      ADC       LCD
```

例如：

```text
CS0 = LOW → 选择 Flash

CS1 = LOW → 选择 ADC

CS2 = LOW → 选择 LCD
```

---

## 7. SPI 时钟模式

SPI 有 4 种常见模式：

| Mode   | CPOL | CPHA |
| ------ | ---: | ---: |
| Mode 0 |    0 |    0 |
| Mode 1 |    0 |    1 |
| Mode 2 |    1 |    0 |
| Mode 3 |    1 |    1 |

其中：

```text
CPOL → Clock Polarity
CPHA → Clock Phase
```

Master 和 Slave 的 SPI Mode 必须匹配。

---

## 8. SPI 数据传输

SPI 通常按照：

```text
8 bit
16 bit
32 bit
```

等方式传输。

例如发送：

```text
0x55
```

二进制：

```text
01010101
```

SCLK 每产生一个有效时钟边沿，传输一个 bit。

---

## 9. SPI 典型应用

### Flash

```text
MCU
 │
 │ SPI
 ▼
NOR Flash
```

用于：

```text
程序存储
配置数据
文件系统
```

### LCD

```text
MCU
 │
 │ SPI
 ▼
LCD
```

### ADC

```text
ADC
 │
 │ SPI
 ▼
MCU
```

用于高速采集。

---

## 10. SPI 与 I2C 对比

| 项目    | SPI           | I2C               |
| ----- | ------------- | ----------------- |
| 数据线   | MOSI + MISO   | SDA               |
| 时钟    | SCLK          | SCL               |
| 设备选择  | CS            | Address           |
| 全双工   | 是             | 否                 |
| 速度    | 高             | 较低                |
| 多设备   | 多 CS          | 多地址               |
| 硬件复杂度 | 简单            | 简单                |
| 典型应用  | Flash/LCD/ADC | Sensor/RTC/EEPROM |

---

## 11. SPI 驱动层次

```text
Application
     │
     ▼
Device Driver
     │
     ▼
SPI Driver
     │
     ▼
SPI Controller
     │
     ├── MOSI
     ├── MISO
     ├── SCLK
     └── CS
          │
          ▼
      SPI Device
```

例如：

```c
spi_transfer(tx_buf, rx_buf, len);
```

底层完成：

```text
CS LOW
   ↓
发送/接收数据
   ↓
CS HIGH
```

---

## 12. SPI 核心知识点

学习 SPI 重点掌握：

```text
MOSI
MISO
SCLK
CS
   ↓
Master / Slave
   ↓
全双工
   ↓
CPOL / CPHA
   ↓
SPI Mode 0/1/2/3
   ↓
CS 选择设备
```

一句话总结：

> **SPI 是一种使用 SCLK、MOSI、MISO 和 CS 进行高速同步、全双工通信的串行总线，常用于 Flash、LCD、ADC、DAC 等设备。**
