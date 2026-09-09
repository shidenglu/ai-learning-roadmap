# BSP Clock 初始化

## 1. 概述

Clock 初始化负责配置芯片内部的**时钟源、PLL、分频器和时钟门控**，为 CPU、总线和外设提供正确的工作时钟。

```text
外部晶振
   ↓
PLL
   ↓
分频器
   ↓
┌───────┬───────┬───────┐
│ CPU   │ Bus   │ 外设  │
└───────┴───────┴───────┘
```

---

## 2. 主要初始化内容

### ① 配置时钟源

选择基础时钟源：

```text
外部晶振
内部RC
PLL输出
```

例如：

```text
24MHz Crystal
      ↓
    PLL
```

---

### ② 配置 PLL

PLL（Phase Locked Loop）用于提高或调整时钟频率。

```text
24MHz
  ↓
 PLL
  ↓
1200MHz
```

常用于产生：

```text
CPU Clock
DDR Clock
GPU Clock
```

---

### ③ 配置分频器

将高频时钟分配成不同频率：

```text
1200MHz
   │
   ├── /1 → CPU   1200MHz
   ├── /2 → Bus    600MHz
   └── /4 → 外设   300MHz
```

---

### ④ 配置时钟门控

控制外设时钟是否开启：

```text
Clock
  │
  ├── UART  → ON
  ├── SPI   → ON
  ├── I2C   → OFF
  └── USB   → OFF
```

不使用的外设可以关闭时钟以降低功耗。

---

### ⑤ 配置外设时钟

不同外设通常需要不同的工作频率：

```text
UART → 24MHz
SPI  → 100MHz
I2C  → 50MHz
Timer → 24MHz
```

具体频率由芯片硬件设计决定。

---

## 3. Clock 初始化流程

```text
Boot
 ↓
选择时钟源
 ↓
配置 PLL
 ↓
等待 PLL 锁定
 ↓
配置分频器
 ↓
配置 CPU/Bus 时钟
 ↓
开启外设时钟
 ↓
配置外设时钟
 ↓
Clock Init 完成
```

---

## 4. BSP 中的典型代码

```c
void clock_init(void)
{
    clock_source_init();

    pll_init();

    bus_clock_init();

    cpu_clock_init();

    peripheral_clock_init();
}
```

---

## 5. Clock 与其他模块的关系

```text
              Clock
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      CPU      DDR      Bus
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
             UART       SPI        Timer
```

没有正确的 Clock 配置，很多硬件模块无法正常工作。

---

## 6. 总结

> **BSP Clock 初始化的核心就是：配置时钟源 → 配置 PLL → 配置分频 → 开启时钟门控 → 为 CPU、总线和外设提供正确的工作时钟。**