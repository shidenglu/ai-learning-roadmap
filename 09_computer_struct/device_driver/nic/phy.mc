# PHY（Physical Layer）简介

## 1. 什么是 PHY

**PHY（Physical Layer，物理层芯片）**负责将 MAC 输出的数字数据转换成可以在物理介质上传输的电信号/光信号，同时完成接收方向的反向转换。

简单理解：

> **MAC 负责“数据帧”，PHY 负责“物理信号”。**

---

## 2. PHY 在网络中的位置

```text
CPU
 │
 │ AXI / PCIe / ...
 ▼
NIC / MAC
 │
 │ RGMII / SGMII / GMII
 ▼
PHY
 │
 │ 电信号 / 光信号
 ▼
RJ45 / SFP
 │
 ▼
Ethernet Network
```

---

## 3. PHY 的基本结构

```text
              PHY
       ┌───────────────┐
       │               │
MAC ──►│ TX            │──► Ethernet
       │               │
MAC ◄──│ RX            │◄── Ethernet
       │               │
       │ Auto-Negotiation
       │ Link Detect
       │ Clock / PLL
       │ PCS / PMA     │
       └───────────────┘
```

主要功能：

| 功能                | 作用        |
| ----------------- | --------- |
| TX                | 发送物理信号    |
| RX                | 接收物理信号    |
| Auto Negotiation  | 自动协商速率/双工 |
| Link Detect       | 检测网线连接状态  |
| Clock             | 提供/恢复通信时钟 |
| Signal Processing | 编码、解码、均衡等 |
| PCS/PMA           | 完成物理层相关处理 |

---

## 4. MAC 与 PHY

MAC 和 PHY 通常通过专用接口连接：

```text
┌──────────┐       ┌──────────┐
│   MAC    │──────►│   PHY    │
│          │◄──────│          │
└──────────┘       └────┬─────┘
                         │
                      Ethernet
```

常见接口：

| 接口    | 特点                 |
| ----- | ------------------ |
| MII   | 早期 10/100M         |
| RMII  | 简化 MII，常见于 MCU     |
| GMII  | Gigabit Ethernet   |
| RGMII | Reduced GMII，嵌入式常见 |
| SGMII | 高速串行接口             |
| XFI   | 更高速的 10GbE 接口      |

---

## 5. PHY 的发送过程

```text
MAC
 │
 │ Ethernet Frame
 ▼
PHY
 │
 ├─ 编码
 ├─ 串并转换
 ├─ 信号调制/处理
 └─ 电气驱动
 │
 ▼
网线
```

PHY 将 MAC 的数字数据转换成适合传输的物理信号。

---

## 6. PHY 的接收过程

```text
网线
 │
 ▼
PHY
 │
 ├─ 接收物理信号
 ├─ 信号恢复
 ├─ 解码
 └─ 串并转换
 │
 ▼
MAC
 │
 ▼
Ethernet Frame
```

---

## 7. Auto-Negotiation

PHY 通常支持**自动协商**，用于确定双方支持的：

* 速率
* 双工模式
* 部分高级能力

例如：

```text
设备 A                 设备 B
  │                      │
  │── 能力交换 ─────────►│
  │◄─ 能力交换 ──────────│
  │                      │
  └──── 协商结果 ─────────┘

结果：
1000 Mbps
Full Duplex
```

---

## 8. Link 状态

PHY 可以检测网络链路状态：

```text
Link Down
    │
    │ 插入网线
    ▼
Link Training / Negotiation
    │
    ▼
Link Up
```

驱动通常需要读取：

```text
Link Status
Speed
Duplex
```

例如：

```text
Link:   UP
Speed:  1000 Mbps
Duplex: Full
```

---

## 9. PHY 管理接口：MDIO

MAC/CPU 通常通过 **MDIO** 管理 PHY。

典型接口：

```text
CPU / MAC
   │
   ├── MDC   ─────► PHY
   │
   └── MDIO  ◄───► PHY
```

| 信号   | 作用   |
| ---- | ---- |
| MDC  | 管理时钟 |
| MDIO | 管理数据 |

通过 MDIO 可以：

* 读取 PHY ID
* 读取 Link 状态
* 设置速率
* 设置双工模式
* 配置 PHY 参数
* 读取状态寄存器

---

## 10. PHY 寄存器

PHY 内部存在大量寄存器，例如：

```text
PHY Register
├── Control Register
├── Status Register
├── PHY ID
├── Auto-Negotiation
├── Link Status
└── Vendor Specific
```

驱动通常通过 MDIO：

```text
MDIO Read
MDIO Write
```

访问这些寄存器。

---

## 11. PHY Driver

典型软件结构：

```text
Application
     │
   Socket
     │
   TCP/IP
     │
Ethernet Driver
     │
   MAC Driver
     │
   PHY Driver
     │
    MDIO
     │
     PHY
     │
 Ethernet
```

PHY Driver 主要负责：

* PHY 初始化
* PHY ID 检测
* Auto-Negotiation
* Link 状态检测
* Speed 配置
* Duplex 配置
* PHY 特殊寄存器配置

---

## 12. PHY 与 MAC 的关系

```text
          Ethernet
              │
             PHY
              │
      RGMII / SGMII
              │
             MAC
              │
             DMA
              │
             DDR
```

可以记住：

> **MAC 处理 Ethernet Frame，PHY 处理 Physical Signal。**

---

## 13. PHY 常见速率

| 类型         |     典型速率 |
| ---------- | -------: |
| 10BASE-T   |  10 Mbps |
| 100BASE-TX | 100 Mbps |
| 1000BASE-T |   1 Gbps |
| 2.5GBASE-T | 2.5 Gbps |
| 10GBASE-T  |  10 Gbps |

---

## 14. PHY、MAC、NIC 的关系

```text
             NIC
      ┌──────────────┐
      │              │
      │     MAC      │
      │      │       │
      │      ▼       │
      │     PHY      │
      │              │
      └──────┬───────┘
             │
          Ethernet
```

三者可以简单理解：

| 名称  | 主要职责         |
| --- | ------------ |
| NIC | 整体网络接口设备     |
| MAC | Ethernet 帧处理 |
| PHY | 物理信号处理       |

---

## 15. 嵌入式典型结构

以 MCU/SoC + GMAC 为例：

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
               
GMAC ── RGMII ── PHY ── RJ45 ── Network
                  │
                 MDIO
                  │
                GMAC
```

这里：

* **GMAC**：负责 Ethernet MAC
* **DMA**：搬运数据
* **RGMII**：MAC ↔ PHY 数据接口
* **MDIO**：MAC ↔ PHY 管理接口
* **PHY**：完成物理层信号处理

---

## 16. PHY 核心知识

学习 PHY 重点掌握：

```text
PHY
├── MAC ↔ PHY
├── MII / RMII / GMII / RGMII / SGMII
├── MDIO / MDC
├── PHY Register
├── PHY ID
├── Auto-Negotiation
├── Link Up / Down
├── Speed
├── Duplex
└── PHY Driver
```

---

## 17. 一句话总结

> **PHY 是 Ethernet 的物理层器件，位于 MAC 与网线/光纤之间，负责数字数据与物理信号之间的转换，并提供链路检测、自动协商、速率和双工配置等功能。**

最核心的数据路径：

```text
发送：
DDR → DMA → MAC → RGMII/SGMII → PHY → 网线

接收：
网线 → PHY → RGMII/SGMII → MAC → DMA → DDR

管理：
CPU/MAC ── MDIO/MDC ──► PHY
```
