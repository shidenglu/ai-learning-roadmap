# NIC（Network Interface Controller）简介

## 1. 什么是 NIC

**NIC（Network Interface Controller，网络接口控制器）**是计算机连接网络的硬件设备，负责：

* 发送网络数据
* 接收网络数据
* MAC 地址管理
* 数据帧收发
* DMA 数据搬运
* 网络中断处理
* 与 PHY 进行通信

简单理解：

> **NIC = CPU/内存与物理网络之间的数据收发控制器**

---

## 2. NIC 在计算机中的位置

```text
             Application
                  │
             Socket / API
                  │
              TCP/IP
                  │
          Network Driver
                  │
             NIC Driver
                  │
          ┌─────────────┐
          │     NIC     │
          │ Controller  │
          └──────┬──────┘
                 │
                PHY
                 │
          Ethernet Cable
                 │
              Network
```

---

## 3. NIC 的基本结构

```text
             CPU
              │
          PCIe / SoC Bus
              │
      ┌───────▼────────┐
      │      NIC       │
      │                │
      │ TX/RX Engine   │
      │ DMA Engine     │
      │ MAC Controller │
      │ Buffer / FIFO  │
      │ Interrupt      │
      └───────┬────────┘
              │
             MAC
              │
             PHY
              │
           Ethernet
```

### 主要模块

| 模块          | 作用              |
| ----------- | --------------- |
| MAC         | 负责以太网帧的收发       |
| PHY         | 负责数字信号与物理信号转换   |
| DMA         | NIC 与内存之间高速搬运数据 |
| FIFO/Buffer | 临时缓存收发数据        |
| Interrupt   | 通知 CPU 数据收发完成   |
| MAC Address | 网络接口的硬件地址       |

---

## 4. MAC 与 PHY

NIC 网络接口通常可以分为：

```text
NIC
├── MAC
└── PHY
```

### MAC

**MAC（Media Access Control）**负责：

* Ethernet Frame 收发
* MAC 地址
* CRC 校验
* 帧过滤
* DMA
* 中断

### PHY

**PHY（Physical Layer）**负责：

* 数字信号 ↔ 电信号/光信号
* 线路编码
* 速率协商
* Link 状态检测

```text
CPU
 │
 NIC MAC
 │
 PHY
 │
 RJ45
 │
 网线
```

---

## 5. NIC 发送数据

例如应用发送一个 TCP 数据：

```text
Application
     │
     ▼
   Socket
     │
     ▼
    TCP
     │
     ▼
    IP
     │
     ▼
Ethernet
     │
     ▼
 NIC Driver
     │
     ▼
    NIC
     │
    DMA
     │
     ▼
   PHY
     │
     ▼
   Network
```

NIC 通常通过 **DMA** 从内存读取数据，然后发送到网络。

---

## 6. NIC 接收数据

接收过程反过来：

```text
Network
   │
   ▼
  PHY
   │
   ▼
  NIC
   │
  DMA
   │
   ▼
   DDR
   │
   ▼
NIC Driver
   │
   ▼
Ethernet
   │
   ▼
   IP
   │
   ▼
   TCP
   │
   ▼
 Socket
   │
   ▼
Application
```

核心：

> **NIC 收到数据 → DMA 搬到内存 → 中断/轮询通知驱动 → 网络协议栈处理**

---

## 7. DMA 与 Descriptor

NIC 通常不会让 CPU 一个字节一个字节搬数据，而是使用：

* DMA
* Descriptor Ring（描述符环）

例如：

```text
RX Descriptor Ring

+-----+     +-----+     +-----+
| RX0 | --> | RX1 | --> | RX2 |
+-----+     +-----+     +-----+
   ↑                       │
   └───────────────────────┘
```

Descriptor 通常记录：

```text
Buffer Address
Buffer Length
Packet Length
Status
Flags
```

因此 NIC 可以直接把网络数据 DMA 到 DDR 中。

---

## 8. TX / RX

NIC 最核心的两个方向：

| 方向 | 含义          |
| -- | ----------- |
| TX | Transmit，发送 |
| RX | Receive，接收  |

```text
          NIC
       ┌───────┐
Memory │       │ Network
  ────►│  TX   │────►
       │       │
  ◄────│  RX   │◄────
       └───────┘
```

---

## 9. NIC 中断

NIC 收到数据后，可以通过中断通知 CPU：

```text
Network
   ↓
 NIC
   ↓
 DMA
   ↓
 DDR
   ↓
 Interrupt
   ↓
 CPU
   ↓
 NIC Driver
```

常见机制：

* RX interrupt
* TX complete interrupt
* Link change interrupt
* Error interrupt

高速网卡通常还会使用 **NAPI/轮询**等机制降低大量中断带来的 CPU 开销。

---

## 10. NIC 常见接口

### PCIe NIC

服务器、PC 常见：

```text
CPU
 │
PCIe
 │
 NIC
 │
 PHY
 │
Ethernet
```

例如：

* 1GbE
* 10GbE
* 25GbE
* 40GbE
* 100GbE

### SoC 集成 NIC

嵌入式系统中通常：

```text
CPU
 │
AXI/AHB
 │
GMAC
 │
RGMII / SGMII
 │
PHY
 │
Ethernet
```

常见接口：

| 接口    | 用途           |
| ----- | ------------ |
| RGMII | MAC ↔ PHY    |
| RMII  | MAC ↔ PHY    |
| GMII  | MAC ↔ PHY    |
| SGMII | 高速 MAC ↔ PHY |
| MII   | MAC ↔ PHY    |

---

## 11. NIC 驱动软件结构

```text
Application
      │
    Socket
      │
    TCP/IP
      │
 Ethernet Layer
      │
 Network Stack
      │
 NIC Driver
      │
 NIC Controller
      │
     DMA
      │
     PHY
      │
   Ethernet
```

Linux 中常见：

```text
Application
    ↓
Socket
    ↓
TCP/IP
    ↓
Network Device
    ↓
NIC Driver
    ↓
NIC Hardware
```

嵌入式系统中也常见：

```text
lwIP
  ↓
Ethernet Driver
  ↓
GMAC
  ↓
DMA
  ↓
PHY
```

---

## 12. NIC 与网卡

严格来说：

```text
NIC = 网络接口控制器
网卡 = 完整的网络接口硬件设备
```

一块网卡通常包含：

```text
NIC Controller
      +
PHY
      +
EEPROM / Flash
      +
RJ45 / SFP
```

现代计算机中 NIC 也可能直接集成在：

* SoC
* 主板芯片
* CPU 平台

---

## 13. 常见网络参数

| 参数          | 含义       |
| ----------- | -------- |
| MAC Address | 网卡硬件地址   |
| Link Speed  | 链路速率     |
| Duplex      | 半双工/全双工  |
| MTU         | 最大传输单元   |
| RX          | 接收       |
| TX          | 发送       |
| DMA         | 直接内存访问   |
| PHY         | 物理层芯片    |
| MAC         | 数据链路层控制器 |

---

## 14. NIC、MAC、PHY 的关系

```text
        NIC
         │
   ┌─────┴─────┐
   │           │
  MAC         PHY
   │           │
帧处理       物理信号
   │           │
   └─────┬─────┘
         │
       Network
```

可以简单记忆：

> **NIC 是整体，MAC 负责帧，PHY 负责物理信号。**

---

## 15. NIC 核心知识

学习 NIC 时重点掌握：

```text
NIC
├── MAC
├── PHY
├── TX / RX
├── DMA
├── Descriptor
├── Ring Buffer
├── Interrupt
├── RGMII / SGMII
├── Ethernet Frame
├── MAC Address
└── NIC Driver
```

---

## 16. 一句话总结

> **NIC 是计算机的网络接口控制器，通过 MAC + PHY + DMA + TX/RX + 中断等机制，实现 CPU/内存与 Ethernet 网络之间的高速数据收发。**

最重要的数据路径：

```text
发送：
DDR → DMA → NIC/MAC → PHY → Ethernet

接收：
Ethernet → PHY → NIC/MAC → DMA → DDR
```
