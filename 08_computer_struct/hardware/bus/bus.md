# 常见总线（Bus）详解

## 1. 什么是总线（Bus）

总线（Bus）是一组用于在计算机系统中传输数据、地址和控制信号的公共通信通道。

简单来说：

> 总线就是连接 CPU、内存和各种外设的数据高速公路。

例如：

```text
CPU
 │
 ├───────────── Bus ─────────────┐
 │                               │
 ▼                               ▼
Memory                        UART
                               SPI
                               I2C
                               GPIO
```

CPU、内存和外设之间并不是直接连接，而是通过总线进行通信。

---

# 2. 总线分类

按照应用场景，可以分为：

```text
总线系统
│
├── 芯片内部总线（On-Chip Bus）
│   ├── AXI
│   ├── AHB
│   ├── APB
│   └── Wishbone
│
├── 板级总线（Board Bus）
│   ├── PCIe
│   ├── USB
│   └── Ethernet
│
└── 外设总线（Peripheral Bus）
    ├── UART
    ├── SPI
    ├── I2C
    ├── CAN
    ├── LIN
    └── I2S
```

---

# 3. AXI总线

## 全称

```text
Advanced eXtensible Interface
```

AXI 是 ARM AMBA 架构中的高性能总线。

---

## 通信对象

```text
CPU  <----> DDR

CPU  <----> DMA

CPU  <----> GPU

CPU  <----> NPU

DMA  <----> DDR

GPU  <----> DDR
```

---

## 系统结构

```text
           CPU
             │
             ▼

         AXI BUS

      ┌───┼────┬────┐

      ▼   ▼    ▼    ▼

     DDR DMA  GPU  NPU
```

---

## 特点

* 高带宽
* 支持突发传输（Burst）
* 支持流水线
* 支持多 Master
* 支持多 Slave
* 支持乱序执行
* 支持 QoS

---

## 典型应用

```text
ARM Cortex-A

手机 SoC

AI 芯片

GPU

NPU

DDR控制器
```

---

# 4. AHB总线

## 全称

```text
Advanced High-performance Bus
```

AHB 是 AMBA 中的中高速总线。

---

## 通信对象

```text
CPU ↔ SRAM

CPU ↔ DMA

CPU ↔ Ethernet

CPU ↔ USB
```

---

## 系统结构

```text
       CPU
         │
         ▼

      AHB BUS

   ┌────┼─────┐

   ▼    ▼     ▼

 SRAM DMA  ETH
```

---

## 特点

* 中高速
* 支持 Burst
* 单时钟设计
* 硬件简单

---

## 典型应用

```text
SRAM控制器

DMA控制器

USB控制器

网络控制器
```

---

# 5. APB总线

## 全称

```text
Advanced Peripheral Bus
```

APB 用于连接低速外设。

---

## 通信对象

```text
CPU ↔ UART

CPU ↔ SPI

CPU ↔ I2C

CPU ↔ GPIO

CPU ↔ Timer

CPU ↔ Watchdog
```

---

## 系统结构

```text
      CPU
        │
        ▼

    AXI/AHB

        │

    APB Bridge

        │

      APB BUS

   ┌────┼─────┐

 UART SPI GPIO
```

---

## 特点

* 结构简单
* 功耗低
* 面积小
* 不支持 Burst

---

## 典型应用

```text
UART

SPI

I2C

GPIO

RTC

Timer
```

---

# 6. PCIe总线

## 全称

```text
PCI Express
```

PC和服务器最重要的高速总线。

---

## 通信对象

```text
CPU ↔ GPU

CPU ↔ SSD

CPU ↔ FPGA

CPU ↔ 网卡
```

---

## 系统结构

```text
         CPU
           │

        PCIe

    ┌────┼─────┐

    ▼    ▼     ▼

   GPU SSD   NIC
```

---

## 特点

* 点对点通信
* 全双工
* 高带宽
* 支持热插拔

---

## 典型设备

### GPU

```text
RTX5090

RTX4090

A100

H100
```

### SSD

```text
三星980Pro

SN850X

P44 Pro
```

### 网卡

```text
Intel X710

Mellanox CX6
```

---

# 7. USB总线

## 全称

```text
Universal Serial Bus
```

通用串行总线。

---

## 通信对象

```text
PC ↔ 鼠标

PC ↔ 键盘

PC ↔ 摄像头

PC ↔ 手机

PC ↔ U盘
```

---

## 系统结构

```text
PC

 │

USB Host

 │

 ├── Mouse
 ├── Keyboard
 ├── Camera
 └── Phone
```

---

## 特点

* 热插拔
* 即插即用
* Host/Device模式

---

## 典型应用

```text
鼠标

键盘

摄像头

打印机

手机
```

---

# 8. UART总线

## 全称

```text
Universal Asynchronous Receiver Transmitter
```

异步串口通信。

---

## 通信对象

```text
CPU ↔ MCU

MCU ↔ GPS

MCU ↔ 蓝牙模块

MCU ↔ WiFi模块

Linux ↔ 调试终端
```

---

## 接线方式

```text
CPU TX -------- RX Device

CPU RX -------- TX Device

GND   -------- GND
```

---

## 特点

* 异步通信
* 仅需两根数据线
* 使用广泛

---

## 常见波特率

```text
9600

115200

921600

1500000
```

---

# 9. SPI总线

## 全称

```text
Serial Peripheral Interface
```

高速同步串行总线。

---

## 通信对象

```text
MCU ↔ Flash

MCU ↔ ADC

MCU ↔ DAC

MCU ↔ FPGA

MCU ↔ LCD
```

---

## 信号线

```text
MOSI

MISO

SCLK

CS
```

---

## 结构

```text
             Master

               MCU

               │

     ┌─────────┼─────────┐

     ▼         ▼         ▼

   Flash      ADC       LCD
```

---

## 特点

* 全双工
* 高速度
* 硬件简单

---

# 10. I2C总线

## 全称

```text
Inter-Integrated Circuit
```

低速控制总线。

---

## 通信对象

```text
MCU ↔ RTC

MCU ↔ EEPROM

MCU ↔ 温度传感器

MCU ↔ PMIC
```

---

## 信号线

```text
SDA

SCL
```

---

## 结构

```text
       MCU

        │

 SDA ───┼─────────────

 SCL ───┼─────────────

        │
 ┌──────┼──────┐

 ▼      ▼      ▼

RTC   EEPROM  Sensor
```

---

## 特点

* 两根线
* 支持多设备
* 地址寻址

---

# 11. CAN总线

## 全称

```text
Controller Area Network
```

汽车电子领域最重要的总线。

---

## 通信对象

```text
发动机ECU

变速箱ECU

ABS

ESP

仪表盘
```

---

## 结构

```text
Engine ECU

      │

      CAN

      │

 ┌────┼─────┐

 ▼    ▼     ▼

ABS ESP Dashboard
```

---

## 特点

* 多主机
* 广播通信
* 抗干扰强
* 实时性高

---

## 应用

```text
汽车电子

工业控制

机器人
```

---

# 12. LIN总线

## 全称

```text
Local Interconnect Network
```

低成本车载网络。

---

## 通信对象

```text
车窗

车灯

雨刷

座椅

后视镜
```

---

## 特点

* 单线通信
* 成本低
* 主从结构

---

## 应用

```text
车身电子
```

---

# 13. I2S总线

## 全称

```text
Inter-IC Sound
```

音频数据传输总线。

---

## 通信对象

```text
CPU ↔ Codec

CPU ↔ DAC

CPU ↔ Audio DSP
```

---

## 结构

```text
CPU

 │

 I2S

 │

Codec

 │

Speaker
```

---

## 应用

```text
音箱

手机

耳机

车载音频
```

---

# 14. Ethernet

## 全称

```text
Ethernet
```

以太网。

---

## 通信对象

```text
PC ↔ PC

PC ↔ Server

Server ↔ Server

Switch ↔ Router
```

---

## 结构

```text
PC

 │

Ethernet

 │

Switch

 │

Server
```

---

## 速率

```text
10 Mbps

100 Mbps

1 Gbps

10 Gbps

100 Gbps

400 Gbps
```

---

# 15. 总线层次结构

典型 ARM SoC：

```text
                     CPU
                      │
                      ▼

                   AXI BUS
                      │

      ┌───────────────┼───────────────┐

      ▼               ▼               ▼

     DDR             DMA             GPU

                      │

                      ▼

                  AXI Bridge

                      │

                      ▼

                   AHB BUS

                      │

       ┌──────────────┼──────────────┐

       ▼              ▼              ▼

      USB            ETH           SRAM

                      │

                      ▼

                  AHB Bridge

                      │

                      ▼

                   APB BUS

      ┌───────┬────────┬────────┬────────┐

      ▼       ▼        ▼        ▼

    UART     SPI      I2C      GPIO
```

---

# 16. 常见总线总结表

| 总线       | 主要通信对象            | 典型设备      | 速度等级 |
| -------- | ----------------- | --------- | ---- |
| AXI      | CPU、DDR、DMA、GPU   | SoC内部高速互联 | 极高   |
| AHB      | CPU、SRAM、USB、ETH  | 中速互联      | 高    |
| APB      | CPU、UART、SPI、GPIO | 低速外设      | 中低   |
| PCIe     | CPU、GPU、SSD       | PC扩展设备    | 极高   |
| USB      | PC、手机、鼠标          | 外部设备      | 中高   |
| UART     | MCU、GPS、蓝牙        | 串口设备      | 低    |
| SPI      | MCU、Flash、ADC     | 高速外设      | 高    |
| I2C      | MCU、RTC、Sensor    | 控制设备      | 低    |
| CAN      | ECU、ABS、仪表        | 汽车电子      | 中    |
| LIN      | 车窗、车灯             | 车身电子      | 低    |
| I2S      | CPU、Codec         | 音频系统      | 中高   |
| Ethernet | PC、服务器            | 网络通信      | 极高   |

---

# 17. 一张图理解所有总线

```text
                         CPU
                          │
          ┌───────────────┼───────────────┐
          │                               │

          ▼                               ▼

       AXI/AHB                        PCIe
          │                               │
          ▼                               ▼

       DDR DMA                        GPU SSD

          │
          ▼

         APB

  ┌───────┼─────────┬────────┐

  ▼       ▼         ▼        ▼

UART     SPI       I2C      GPIO

  │        │         │

GPS      Flash     RTC

Bluetooth ADC      Sensor


外部世界：

PC ←→ USB ←→ 鼠标/键盘/U盘

汽车 ←→ CAN ←→ ECU/ABS/ESP

音频 ←→ I2S ←→ Codec/DAC

网络 ←→ Ethernet ←→ Switch/Server
```
