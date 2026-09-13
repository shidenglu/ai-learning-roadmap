# PCIe（PCI Express）总线

## 1. 什么是 PCIe

PCIe（Peripheral Component Interconnect Express）即：

```text
高速串行扩展总线
```

用于连接 CPU 与高速外设。

常见设备：

```text
GPU
NVMe SSD
网卡
AI加速卡
采集卡
```

---

# 2. PCIe 在计算机中的位置

```text
          CPU
           │
      PCIe Bus
           │
 ┌─────────┼─────────┐
 ▼         ▼         ▼
GPU      SSD       NIC
```

PCIe 是现代计算机最重要的高速总线之一。

---

# 3. PCIe 基本结构

PCIe 采用：

```text
点对点(Point-to-Point)
```

连接方式。

```text
CPU/Root Complex
          │
          ▼
      PCIe Link
          │
          ▼
       Endpoint
```

例如：

```text
CPU
 │
 ▼
PCIe
 │
 ▼
GPU
```

---

# 4. Lane（通道）

PCIe 的基本单位：

```text
Lane
```

每个 Lane 包含：

```text
TX+
TX-

RX+
RX-
```

即：

```text
发送差分对
接收差分对
```

因此 PCIe 是：

```text
全双工通信
```

---

# 5. 常见 PCIe 配置

| 配置  | Lane数量 |
| --- | ------ |
| x1  | 1      |
| x2  | 2      |
| x4  | 4      |
| x8  | 8      |
| x16 | 16     |

例如：

```text
GPU    → PCIe x16

NVMe   → PCIe x4
```

---

# 6. PCIe 数据传输

```text
CPU
 │
 ▼
PCIe Controller
 │
 ▼
PCIe Link
 │
 ▼
Device
```

数据以高速数据包形式传输：

```text
Packet
```

而不是传统并行总线方式。

---

# 7. PCIe 版本

| 版本       | 单 Lane 理论带宽 |
| -------- | ----------- |
| PCIe 1.0 | 250 MB/s    |
| PCIe 2.0 | 500 MB/s    |
| PCIe 3.0 | 985 MB/s    |
| PCIe 4.0 | 1.97 GB/s   |
| PCIe 5.0 | 3.94 GB/s   |
| PCIe 6.0 | 7.88 GB/s   |

例如：

```text
PCIe 4.0 x4

≈ 8 GB/s
```

---

# 8. PCIe 拓扑

```text
            CPU
             │
      PCIe Root Complex
             │
      ┌──────┴──────┐
      ▼             ▼
   GPU          PCIe Switch
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
        SSD                   NIC
```

---

# 9. PCIe 设备枚举

系统启动时：

```text
发现设备
    ↓
读取配置空间
    ↓
分配资源
    ↓
加载驱动
```

例如：

```text
GPU Driver

NVMe Driver

Network Driver
```

---

# 10. PCIe 与 DMA

PCIe 设备通常支持 DMA：

```text
Device
   │
   ▼
DMA Engine
   │
   ▼
DDR Memory
```

无需 CPU 逐字节搬运数据。

提高性能：

```text
低CPU占用

高速数据传输
```

---

# 11. PCIe 在 AI 中的作用

```text
CPU
 │
 ▼
PCIe
 │
 ▼
GPU
 │
 ▼
VRAM
```

训练模型时：

```text
数据
 ↓
DDR
 ↓
PCIe
 ↓
GPU
 ↓
显存
```

因此 PCIe 带宽会影响数据传输效率。

---

# 12. PCIe 驱动层次

```text
Application
      │
      ▼
Device Driver
      │
      ▼
PCIe Driver
      │
      ▼
PCIe Controller
      │
      ▼
PCIe Device
```

---

# 13. 常见应用

| 设备       | PCIe配置   |
| -------- | -------- |
| GPU      | x16      |
| NVMe SSD | x4       |
| 网卡       | x1/x4/x8 |
| AI加速卡    | x8/x16   |
| 视频采集卡    | x4/x8    |

---

# 14. PCIe 与其他总线对比

| 总线       | 典型用途      | 速度 |
| -------- | --------- | -- |
| UART     | 调试通信      | 低  |
| I2C      | 传感器       | 低  |
| SPI      | Flash/LCD | 中  |
| USB      | 外设连接      | 高  |
| Ethernet | 网络通信      | 高  |
| PCIe     | GPU/SSD   | 极高 |

---

# 15. 核心知识点

```text
PCIe
 │
 ├── Root Complex
 ├── Endpoint
 ├── Lane
 ├── x1/x4/x8/x16
 ├── Packet
 ├── DMA
 ├── Enumeration
 ├── PCIe 3.0
 ├── PCIe 4.0
 └── PCIe 5.0
```

---

# 16. 总结

PCIe 是现代计算机和服务器中最重要的高速总线。

核心链路：

```text
CPU
 │
 ▼
PCIe
 │
 ▼
GPU / SSD / NIC
```

核心特点：

```text
高速
全双工
点对点
可扩展
支持DMA
```

一句话总结：

> **PCIe 是一种面向高速设备的点对点串行总线，通过多 Lane 并行传输实现极高带宽，是 GPU、NVMe SSD、网卡等设备与 CPU 通信的核心通道。**
