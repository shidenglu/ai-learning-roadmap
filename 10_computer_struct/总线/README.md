# 总线（Bus）原理详解

## 1. 什么是总线

总线（Bus）是计算机中用于连接各个硬件模块并传输信息的公共通信通道。

简单理解：

```text
CPU
 │
 ├──── 总线 ──── 内存
 │
 ├──── 总线 ──── 网卡
 │
 ├──── 总线 ──── 硬盘
 │
 └──── 总线 ──── 显卡
```

总线就像城市中的公路：

* CPU、内存、外设是不同建筑
* 数据是汽车
* 总线是道路

没有总线，各个硬件之间将无法通信。

---

# 2. 为什么需要总线

假设系统有：

```text
CPU
RAM
SSD
GPU
NIC
```

如果采用点对点连接：

```text
CPU ↔ RAM
CPU ↔ SSD
CPU ↔ GPU
CPU ↔ NIC
RAM ↔ SSD
RAM ↔ GPU
...
```

连接数量会急剧增加。

采用总线后：

```text
         CPU
          │
 ┌────────┼────────┐
 │        │        │
RAM      SSD      GPU
 │        │        │
 └────────┼────────┘
          │
        BUS
```

所有设备共享通信通道，大大降低硬件复杂度。

---

# 3. 总线的组成

经典计算机体系结构中，总线由三部分组成：

```text
System Bus
│
├── 地址总线 Address Bus
├── 数据总线 Data Bus
└── 控制总线 Control Bus
```

---

# 4. 地址总线（Address Bus）

## 作用

指定访问目标。

例如：

```c
a = array[100];
```

CPU需要告诉内存：

```text
我要访问哪个地址？
```

地址信息通过地址总线发送。

---

## 特点

### 单向传输

```text
CPU ─────→ Memory
```

通常由CPU发出地址。

---

## 地址总线宽度

例如：

### 16位地址总线

```text
2^16 = 65536
```

可寻址：

```text
64KB
```

---

### 32位地址总线

```text
2^32
```

可寻址：

```text
4GB
```

---

### 64位地址总线

```text
2^64
```

理论可寻址：

```text
16EB
```

（Exabyte）

---

# 5. 数据总线（Data Bus）

## 作用

传输真正的数据。

例如：

```text
内存读取
```

```text
CPU
 ↑
Data Bus
 ↑
RAM
```

---

## 特点

### 双向传输

```text
CPU ←→ Memory
```

既能读：

```text
Memory → CPU
```

也能写：

```text
CPU → Memory
```

---

## 数据总线宽度

### 8位

```text
一次传输1字节
```

---

### 32位

```text
一次传输4字节
```

---

### 64位

```text
一次传输8字节
```

例如：

```text
64bit总线
1GHz
```

理论带宽：

```text
8 × 1G
=
8GB/s
```

---

# 6. 控制总线（Control Bus）

## 作用

控制通信过程。

例如：

```text
读内存？
写内存？
中断？
DMA请求？
```

都通过控制总线完成。

---

## 常见控制信号

### Read

```text
Memory Read
```

通知内存：

```text
请把数据发出来
```

---

### Write

```text
Memory Write
```

通知内存：

```text
请保存数据
```

---

### Interrupt

```text
IRQ
```

设备向CPU发起中断。

---

### DMA Request

```text
DMA_REQ
```

DMA请求总线控制权。

---

# 7. 一次内存读取过程

例如：

```c
x = a;
```

CPU执行过程：

### 第一步

地址总线发送：

```text
Address Bus

0x1000
```

---

### 第二步

控制总线发送：

```text
READ
```

---

### 第三步

RAM读取数据：

```text
123
```

---

### 第四步

数据总线返回：

```text
Data Bus

123
```

---

### 第五步

CPU寄存器接收：

```text
R0 = 123
```

整个过程：

```text
CPU
 │
 │ 地址
 ▼
Address Bus
 │
 ▼
RAM

READ
 │
 ▼
Control Bus

123
 │
 ▼
Data Bus
 │
 ▼
CPU
```

---

# 8. 总线仲裁（Bus Arbitration）

问题：

多个设备同时访问总线：

```text
CPU
DMA
GPU
NIC
```

怎么办？

---

必须进行仲裁：

```text
谁先使用总线
谁后使用总线
```

例如：

```text
CPU 请求
DMA 请求
```

仲裁器决定：

```text
Grant → DMA
```

DMA获得总线控制权。

---

# 9. DMA与总线

这是嵌入式开发中最常见的场景。

---

## 普通方式

```text
Device
 ↓
CPU
 ↓
Memory
```

CPU参与搬运。

---

## DMA方式

```text
Device
 ↓
DMA
 ↓
Memory
```

CPU只负责配置DMA。

DMA直接获得总线控制权。

优点：

```text
降低CPU负载
提高吞吐量
```

---

# 10. 现代总线

早期：

```text
ISA
PCI
FSB
```

都是共享总线。

---

现代CPU：

共享总线逐渐被高速点对点互连取代。

例如：

## PCIe

```text
PCI Express
```

特点：

```text
高速串行
点对点连接
```

---

## Intel

```text
QPI
UPI
```

---

## AMD

```text
Infinity Fabric
```

---

## ARM SoC

```text
AMBA
AXI
AHB
APB
```

广泛用于手机和嵌入式芯片。

---

# 11. ARM体系中的总线

ARM SoC通常采用：

```text
CPU
 │
 AXI
 │
 ├── DDR Controller
 ├── DMA
 ├── GPU
 ├── USB
 ├── Ethernet
 └── PCIe
```

---

## AXI

高速总线

用于：

```text
CPU
DMA
DDR
GPU
```

---

## AHB

中速总线

用于：

```text
USB
Ethernet
```

---

## APB

低速总线

用于：

```text
UART
SPI
I2C
GPIO
Timer
```

---

# 12. 总结

## 总线是什么

```text
计算机内部的数据高速公路
```

---

## 三大组成

| 总线   | 功能      |
| ---- | ------- |
| 地址总线 | 指定访问位置  |
| 数据总线 | 传输数据    |
| 控制总线 | 控制读写和时序 |

---

## 数据流动过程

```text
CPU
 ↓ 地址总线
Memory
 ↑ 数据总线
CPU
```

---

## 现代发展方向

```text
共享总线
 ↓
高速互连
 ↓
PCIe
AXI
Infinity Fabric
```

---

## 对嵌入式工程师最重要的部分

```text
总线
 ↓
DMA
 ↓
Cache
 ↓
MMU
 ↓
PCIe
 ↓
AXI
```

理解这条链路之后，就能够真正理解 ARM SoC 内部的数据流动过程。
