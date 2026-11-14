# BSP（Board Support Package，板级支持包）

## 1. BSP简介

BSP（Board Support Package）是操作系统与硬件平台之间的适配层，负责完成开发板硬件初始化和驱动适配，使操作系统能够在特定硬件平台上运行。

简单来说：

> BSP = 操作系统 + 硬件平台之间的桥梁

---

## 2. BSP在系统中的位置

```text
┌─────────────────────┐
│     Application     │
├─────────────────────┤
│      Middleware     │
├─────────────────────┤
│        RTOS         │
├─────────────────────┤
│         BSP         │
├─────────────────────┤
│      Hardware       │
└─────────────────────┘
```

---

## 3. BSP主要功能

### CPU初始化

- CPU模式配置
- Cache配置
- MMU配置
- 多核启动(SMP)

### 时钟初始化

- PLL配置
- CPU时钟
- 总线时钟
- 外设时钟

### DDR初始化

- DDR控制器配置
- DDR训练
- 内存映射建立

### 中断初始化

- GIC初始化
- 中断向量表建立
- 中断注册

### Timer初始化

- 系统Tick
- 延时功能
- 调度时钟源

### 串口初始化

- UART配置
- 调试输出
- Boot日志打印

### GPIO初始化

- 引脚复用
- 输入输出配置

### 外设初始化

- SPI
- I2C
- CAN
- USB
- Ethernet
- PCIe

---

## 4. BSP启动流程

```text
Power On
   │
   ▼
BootROM
   │
   ▼
BootLoader
   │
   ▼
startup.S
   │
   ▼
CPU Init
   │
   ▼
Clock Init
   │
   ▼
DDR Init
   │
   ▼
Interrupt Init
   │
   ▼
UART Init
   │
   ▼
Board Init
   │
   ▼
RTOS/Linux Start
   │
   ▼
main()
```

---

## 5. BSP目录结构示例

```text
bsp/
├── startup.S
├── board.c
├── clock.c
├── ddr.c
├── gic.c
├── timer.c
├── uart.c
├── gpio.c
├── spi.c
├── i2c.c
├── eth.c
└── bsp.h
```

---

## 6. BSP与驱动的区别

| BSP | Driver |
|------|---------|
| 面向硬件平台 | 面向设备功能 |
| 完成硬件初始化 | 提供访问接口 |
| 与具体板卡相关 | 与具体设备相关 |
| OS移植必须开发 | 功能扩展需要开发 |

示例：

```text
BSP：
    开启UART时钟
    配置UART寄存器

Driver：
    open()
    read()
    write()
    ioctl()
```

---

## 7. BSP核心作用

### 硬件抽象

屏蔽不同硬件平台差异。

### 系统移植

支持RTOS/Linux快速移植。

### 统一接口

向上层提供统一硬件访问方式。

### 系统启动

完成系统上电后的基础环境构建。

---

## 8. BSP的本质

```text
          BSP
      ┌─────────┐
      │ 翻译官  │
      └─────────┘
       ▲       ▲
       │       │
      OS    Hardware
```

BSP本质上是：

> 硬件适配层（Hardware Adaptation Layer）

负责屏蔽硬件细节，让同一个操作系统能够运行在不同开发板和处理器平台上。

---

## 9. 一句话总结

BSP（板级支持包）负责完成CPU、内存、中断、时钟及外设初始化，为RTOS/Linux提供运行环境，是操作系统与硬件平台之间的桥梁。