# Power（电源管理）简介

## 1. 什么是 Power

Power 是嵌入式系统中的**电源管理子系统**，负责：

```text
供电
稳压
电压转换
上电/下电控制
功耗管理
```

---

## 2. Power 基本结构

```text
电池 / 电源
     │
     ▼
PMIC
     │
 ┌───┼────┐
 ▼   ▼    ▼
CPU  DDR  外设
```

PMIC（Power Management IC）是电源管理的核心芯片。

---

## 3. 常见电源模块

| 模块           | 作用    |
| ------------ | ----- |
| PMIC         | 电源管理  |
| LDO          | 低压差稳压 |
| Buck         | 降压    |
| Boost        | 升压    |
| Buck-Boost   | 升降压   |
| Power Switch | 电源开关  |
| Charger      | 电池充电  |

---

## 4. LDO

LDO（Low Dropout Regulator）用于降压稳压。

```text
5V
 │
 ▼
LDO
 │
 ▼
3.3V
```

特点：

```text
电路简单
噪声低
效率较低
```

---

## 5. Buck

Buck 用于降压：

```text
12V
 │
 ▼
Buck
 │
 ▼
5V
```

特点：

```text
效率高
适合大电流供电
```

---

## 6. Boost

Boost 用于升压：

```text
3.7V
 │
 ▼
Boost
 │
 ▼
5V
```

常用于：

```text
电池供电
背光
显示设备
```

---

## 7. Power Domain

SoC 通常划分多个电源域：

```text
Power Domain
 │
 ├── CPU
 ├── GPU
 ├── DDR
 ├── Peripheral
 └── Analog
```

不同模块可以独立控制电源。

---

## 8. Power Management

系统根据负载调整功耗：

```text
运行
 ↓
降低频率/电压
 ↓
Idle
 ↓
关闭部分模块
 ↓
Sleep
```

常见技术：

```text
DVFS
Clock Gating
Power Gating
Sleep/Wakeup
```

---

## 9. Power Sequencing

多个电源通常需要按照规定顺序启动：

```text
Power ON
   ↓
1.8V
   ↓
3.3V
   ↓
Core Voltage
   ↓
Peripheral
   ↓
System Ready
```

关闭时也可能需要遵循特定顺序。

---

## 10. Power 与 GPIO

GPIO 可以控制电源使能：

```text
CPU
 │
 ▼
GPIO
 │
 ▼
EN
 │
 ▼
Power IC
 │
 ▼
Peripheral
```

例如：

```c
gpio_set_value(POWER_EN, 1);
```

开启外设电源。

---

## 11. Power 与 Timer

Timer 可以配合电源管理实现：

```text
定时唤醒
低功耗休眠
周期性采样
```

例如：

```text
Sleep
  ↓
Timer
  ↓
Wakeup
  ↓
CPU运行
  ↓
再次Sleep
```

---

## 12. Power 驱动层次

```text
Application
      │
      ▼
Power Management
      │
      ▼
PMIC Driver
      │
      ▼
I2C / SPI / GPIO
      │
      ▼
PMIC
      │
      ▼
Power Rail
```

---

## 13. 常见应用

| 场景   | Power 功能 |
| ---- | -------- |
| 手机   | 电池管理     |
| MCU  | 低功耗      |
| SoC  | 多电源域管理   |
| LCD  | 背光供电     |
| GPU  | 高功率供电    |
| SSD  | 电源管理     |
| 工控设备 | 稳压/保护    |

---

## 14. 核心知识点

```text
Power
 │
 ├── PMIC
 ├── LDO
 ├── Buck
 ├── Boost
 ├── Power Domain
 ├── Power Sequencing
 ├── DVFS
 ├── Clock Gating
 ├── Power Gating
 └── Sleep/Wakeup
```

---

## 15. 总结

Power 管理的核心就是：

```text
稳定供电
    +
合理分配
    +
动态控制
    +
降低功耗
```

典型结构：

```text
Battery / Adapter
       │
       ▼
      PMIC
       │
 ┌─────┼─────┐
 ▼     ▼     ▼
CPU   DDR   Peripheral
```

一句话总结：

> **Power 是负责整个系统供电、电压转换、电源域控制以及低功耗管理的子系统，是嵌入式系统稳定运行和降低功耗的基础。**
