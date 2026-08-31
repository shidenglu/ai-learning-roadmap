# I2C（IIC）总线

## 1. 什么是 I2C

I2C（Inter-Integrated Circuit）是一种**同步、串行、半双工、多设备通信总线**，主要用于 MCU/SoC 与低速外设之间的通信。

典型设备：

```text
MCU
 │
 ├── RTC
 ├── EEPROM
 ├── 温度传感器
 ├── IMU
 ├── PMIC
 └── IO Expander
```

---

## 2. I2C 两根信号线

| 信号  | 含义           | 作用  |
| --- | ------------ | --- |
| SDA | Serial Data  | 数据线 |
| SCL | Serial Clock | 时钟线 |

多个设备共享 SDA 和 SCL：

```text
             MCU
              │
        ┌─────┴─────┐
        │           │
       SDA         SCL
        │           │
════════╪═══════════╪════════ I2C BUS
        │           │
    ┌───┼───┬───────┼───┐
    ▼   ▼   ▼       ▼
   RTC EEPROM     Sensor PMIC
```

---

## 3. Master 和 Slave

```text
Master
  │
  │ 发起通信、产生时钟
  ▼
I2C Bus
  │
  ├── Slave 0x50 → EEPROM
  ├── Slave 0x68 → RTC
  └── Slave 0x40 → Sensor
```

Master 通过 **Slave Address** 区分不同设备。

---

## 4. I2C 基本通信过程

一次典型通信：

```text
START
  ↓
Slave Address
  ↓
R/W
  ↓
ACK
  ↓
Data
  ↓
ACK/NACK
  ↓
STOP
```

读取设备寄存器通常：

```text
START
  ↓
Device Address + WRITE
  ↓
Register Address
  ↓
REPEATED START
  ↓
Device Address + READ
  ↓
Data
  ↓
NACK
  ↓
STOP
```

---

## 5. ACK / NACK

每发送 8 bit 数据后，第 9 个时钟用于：

```text
ACK  → 接收成功
NACK → 不确认 / 结束读取
```

---

## 6. I2C 地址

最常见的是 **7-bit 地址**。

例如：

```text
Device Address = 0x68
```

读写位：

```text
WRITE = 0
READ  = 1
```

形成地址字节：

```text
Address Byte = (Address << 1) | R/W
```

例如：

```text
0x68 << 1 = 0xD0

WRITE → 0xD0
READ  → 0xD1
```

---

## 7. I2C 电气特性

I2C 通常采用：

```text
Open Drain / Open Collector
        +
Pull-up Resistor
```

结构：

```text
VCC
 │
 R
 │
 ├──────── SDA
 │
 └── Device
      │
     GND
```

设备只能主动：

```text
拉低
```

释放总线后：

```text
Pull-up → 拉高
```

---

## 8. 常见速率

| 模式              |       典型速率 |
| --------------- | ---------: |
| Standard Mode   | 100 kbit/s |
| Fast Mode       | 400 kbit/s |
| Fast Mode Plus  |   1 Mbit/s |
| High-Speed Mode | 3.4 Mbit/s |

---

## 9. I2C 与 SPI、UART 对比

| 项目   | I2C        | SPI       | UART   |
| ---- | ---------- | --------- | ------ |
| 信号线  | 2          | 4+        | 2      |
| 时钟   | 有          | 有         | 无      |
| 多设备  | 支持         | 支持        | 通常不支持  |
| 地址   | 有          | 无，使用CS    | 无      |
| 全双工  | 否          | 是         | 是      |
| 典型应用 | Sensor/RTC | Flash/LCD | GPS/调试 |

---

## 10. I2C 驱动层次

```text
Application
     │
     ▼
Device Driver
     │
     ▼
I2C Driver
     │
     ▼
I2C Controller
     │
     ▼
SDA / SCL
     │
     ▼
I2C Device
```

例如：

```c
i2c_read_reg(0x68, 0x10, &data);
```

底层最终完成：

```text
START
 → Address
 → ACK
 → Register
 → ACK
 → RESTART
 → Address + READ
 → DATA
 → NACK
 → STOP
```

---

## 11. 核心知识点

学习 I2C 重点掌握：

```text
SDA / SCL
    ↓
START / STOP
    ↓
Slave Address
    ↓
READ / WRITE
    ↓
ACK / NACK
    ↓
Register Read / Write
    ↓
Open Drain + Pull-up
```

一句话总结：

> **I2C 是一种使用 SDA 和 SCL 两根线，通过设备地址实现多设备通信的同步串行总线，非常适合连接 RTC、EEPROM、传感器、PMIC 等低速外设。**
