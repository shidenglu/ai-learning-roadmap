# MAC（Media Access Control）简介

## 1. 什么是 MAC

**MAC（Media Access Control，介质访问控制）**是 Ethernet 数据链路层的核心控制模块，负责：

* Ethernet 帧的发送与接收
* MAC 地址管理
* 帧校验
* 数据包过滤
* DMA 数据搬运
* 中断处理
* MAC 与 PHY 之间的数据交换

简单理解：

> **MAC 负责处理 Ethernet Frame，PHY 负责处理物理信号。**

---

## 2. MAC 在网络中的位置

```text
CPU
 │
 │ AXI / PCIe
 ▼
MAC
 │
 │ RGMII / SGMII / GMII
 ▼
PHY
 │
 ▼
Ethernet
```

完整软件/硬件路径：

```text
Application
    │
  Socket
    │
  TCP/IP
    │
Network Driver
    │
  MAC Driver
    │
    MAC
    │
    PHY
    │
 Ethernet
```

---

## 3. MAC 的基本结构

```text
                 MAC
        ┌──────────────────┐
        │                  │
DDR ◄──►│   DMA Engine     │
        │                  │
        │   TX Engine      │
        │   RX Engine      │
        │                  │
        │   MAC Address    │
        │   Frame Filter   │
        │   CRC Check      │
        │   FIFO / Buffer  │
        │   Interrupt      │
        │                  │
        └────────┬─────────┘
                 │
              PHY Interface
                 │
                PHY
```

---

## 4. Ethernet Frame

MAC 处理的基本单位是 **Ethernet Frame（以太网帧）**：

```text
┌────────┬────────┬────────┬──────┬────────┬─────┐
│ Preamble│Dst MAC│Src MAC│Type  │ Payload│ FCS │
└────────┴────────┴────────┴──────┴────────┴─────┘
```

| 字段          | 作用        |
| ----------- | --------- |
| Preamble    | 帧同步       |
| Dst MAC     | 目的 MAC 地址 |
| Src MAC     | 源 MAC 地址  |
| Type/Length | 协议类型/长度   |
| Payload     | 数据        |
| FCS         | CRC 校验    |

---

## 5. MAC 地址

MAC 地址通常为 **48 bit**：

```text
00:11:22:33:44:55
```

MAC 可以根据目的 MAC 地址进行帧过滤：

```text
收到 Ethernet Frame
        │
        ▼
检查 Dst MAC
        │
   ┌────┴────┐
   │         │
匹配       不匹配
   │         │
接收       丢弃
```

常见类型：

* Unicast
* Multicast
* Broadcast

广播地址：

```text
FF:FF:FF:FF:FF:FF
```

---

## 6. MAC 发送数据

```text
DDR
 │
 │ DMA
 ▼
MAC TX
 │
 │ Ethernet Frame
 ▼
PHY
 │
 ▼
Ethernet
```

MAC Driver 通常将发送数据放入 TX Buffer，并配置 TX Descriptor：

```text
TX Descriptor
├── Buffer Address
├── Length
├── Status
└── Control
```

MAC 通过 DMA 读取数据并发送。

---

## 7. MAC 接收数据

```text
Ethernet
    │
    ▼
   PHY
    │
    ▼
 MAC RX
    │
    │ DMA
    ▼
   DDR
    │
    ▼
MAC Driver
    │
    ▼
 TCP/IP
```

通常使用 **RX Descriptor Ring**：

```text
RX0 → RX1 → RX2 → RX3
 ↑                   │
 └───────────────────┘
```

MAC 收到数据后，通过 DMA 写入 DDR。

---

## 8. MAC 与 DMA

高速网络通信中，MAC 通常集成 DMA：

```text
        MAC
         │
    ┌────▼────┐
    │   DMA   │
    └────┬────┘
         │
         ▼
        DDR
```

作用：

> **减少 CPU 参与数据搬运，提高网络吞吐率。**

核心机制：

```text
Descriptor
    ↓
Buffer
    ↓
DMA
    ↓
DDR
```

---

## 9. MAC 与 PHY

MAC 和 PHY 通过专用接口连接：

```text
┌─────────┐      RGMII      ┌─────────┐
│   MAC   │◄───────────────►│   PHY   │
└─────────┘                 └────┬────┘
                                 │
                              Ethernet
```

常见接口：

| 接口    | 典型用途          |
| ----- | ------------- |
| MII   | 10/100 Mbps   |
| RMII  | 10/100 Mbps   |
| GMII  | Gigabit       |
| RGMII | Gigabit，嵌入式常见 |
| SGMII | 高速串行          |

---

## 10. MAC 管理 PHY

MAC/CPU 通常通过 **MDIO/MDC** 管理 PHY：

```text
MAC
 │
 ├── MDC ──────► PHY
 │
 └── MDIO ◄────► PHY
```

可以完成：

* PHY ID 读取
* Link 状态读取
* Speed 配置
* Duplex 配置
* Auto-Negotiation 配置
* PHY 寄存器读写

---

## 11. MAC 常见功能

| 功能           | 作用                |
| ------------ | ----------------- |
| TX           | 发送 Ethernet Frame |
| RX           | 接收 Ethernet Frame |
| MAC Address  | 地址识别              |
| CRC/FCS      | 帧校验               |
| Filtering    | 帧过滤               |
| DMA          | 内存数据搬运            |
| Descriptor   | 描述 DMA Buffer     |
| Interrupt    | 通知 CPU            |
| Flow Control | 流量控制              |
| VLAN         | VLAN 帧处理          |

---

## 12. MAC Driver

典型驱动结构：

```text
Application
      │
    Socket
      │
    TCP/IP
      │
Network Stack
      │
  MAC Driver
      │
      ├── MAC Register
      ├── TX/RX
      ├── DMA
      ├── Descriptor
      └── Interrupt
      │
     MAC
      │
     PHY
```

MAC Driver 主要负责：

* MAC 初始化
* MAC 地址配置
* TX/RX 初始化
* DMA 初始化
* Descriptor Ring 初始化
* 中断处理
* Link 状态处理
* MAC 寄存器配置

---

## 13. MAC、PHY、NIC 的关系

```text
                NIC
        ┌─────────────────┐
        │                 │
        │      MAC        │
        │       │         │
        │       ▼         │
        │      PHY        │
        │                 │
        └────────┬────────┘
                 │
              Ethernet
```

简单理解：

| 模块  | 主要职责         |
| --- | ------------ |
| NIC | 整体网络接口设备     |
| MAC | Ethernet 帧处理 |
| PHY | 物理信号处理       |

---

## 14. 嵌入式典型结构

```text
                 CPU
                  │
                 AXI
                  │
                GMAC
                  │
                 DMA
                  │
                 DDR

GMAC ── RGMII ── PHY ── RJ45 ── Ethernet
                  │
                 MDIO
                  │
                 GMAC
```

其中：

* **GMAC**：Gigabit MAC
* **DMA**：搬运网络数据
* **RGMII**：MAC ↔ PHY 数据接口
* **MDIO**：MAC ↔ PHY 管理接口
* **PHY**：物理层信号处理

---

## 15. MAC 核心知识

```text
MAC
├── Ethernet Frame
├── MAC Address
├── TX / RX
├── DMA
├── Descriptor
├── Ring Buffer
├── CRC / FCS
├── Frame Filter
├── RGMII / SGMII
├── MDIO / MDC
├── Interrupt
└── MAC Driver
```

---

## 16. 一句话总结

> **MAC 是 Ethernet 数据链路层的核心控制器，负责 Ethernet Frame 的收发、MAC 地址处理、帧过滤、CRC 校验以及通过 DMA 与内存交换数据。**

最核心的数据路径：

```text
发送：
DDR → DMA → MAC → RGMII/SGMII → PHY → Ethernet

接收：
Ethernet → PHY → RGMII/SGMII → MAC → DMA → DDR

PHY 管理：
CPU/MAC ── MDIO/MDC ──► PHY
```
