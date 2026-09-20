# SATA 接口简介

## 1. 什么是 SATA

SATA（Serial ATA，Serial Advanced Technology Attachment）是一种用于连接存储设备的高速串行接口标准。

主要用于：

* HDD（机械硬盘）
* SSD（固态硬盘）
* 光驱（DVD/CD）

作用：

```text
CPU
 ↓
芯片组/SATA控制器
 ↓
SATA接口
 ↓
SSD/HDD
```

---

## 2. SATA 发展历程

| 版本       | 速率       | 理论带宽     |
| -------- | -------- | -------- |
| SATA 1.0 | 1.5 Gbps | 150 MB/s |
| SATA 2.0 | 3.0 Gbps | 300 MB/s |
| SATA 3.0 | 6.0 Gbps | 600 MB/s |

目前最常见的是：

```text
SATA III (6Gbps)
```

---

## 3. SATA 架构

```text
Application
      ↓
File System
      ↓
Block Layer
      ↓
AHCI Driver
      ↓
SATA Controller
      ↓
SATA Cable
      ↓
SSD/HDD
```

SATA 本质上是：

```text
Host <------> Storage Device
```

点对点通信架构。

---

## 4. SATA 接口组成

### 数据接口

```text
7 Pin
```

负责：

* 数据发送
* 数据接收

结构：

```text
TX+
TX-
GND
RX+
RX-
GND
GND
```

---

### 电源接口

```text
15 Pin
```

提供：

| 电压   | 用途    |
| ---- | ----- |
| 3.3V | 少量设备  |
| 5V   | SSD   |
| 12V  | HDD电机 |

---

## 5. SATA 数据传输

采用：

```text
Serial Transmission
```

即：

```text
1 Bit
 ↓
1 Bit
 ↓
1 Bit
```

连续发送。

相比旧式 PATA：

```text
PATA
 ├── 并行传输
 └── 多线缆

SATA
 ├── 串行传输
 └── 少引脚
```

优点：

* 速度更高
* 干扰更小
* 布线简单

---

## 6. AHCI

AHCI（Advanced Host Controller Interface）是 SATA 标准软件接口。

提供：

* DMA传输
* 热插拔
* NCQ队列管理

```text
OS
 ↓
AHCI Driver
 ↓
SATA Controller
```

Linux常见驱动：

```text
ahci
libata
```

---

## 7. NCQ

NCQ（Native Command Queuing）

允许硬盘：

```text
请求1
请求2
请求3
请求4
```

重新排序执行：

```text
请求2
请求4
请求1
请求3
```

作用：

* 减少寻道时间
* 提高并发性能
* 提升随机读写效率

机械硬盘收益最明显。

---

## 8. SATA SSD 与 SATA HDD

### SATA HDD

```text
SATA
 ↓
控制器
 ↓
磁盘
 ↓
磁头
```

特点：

* 容量大
* 价格低
* 速度慢

---

### SATA SSD

```text
SATA
 ↓
SSD Controller
 ↓
NAND Flash
```

特点：

* 无机械结构
* 延迟低
* 速度快

但仍受 SATA 带宽限制：

```text
≈ 550 MB/s
```

---

## 9. SATA 与 NVMe 对比

| 项目   | SATA SSD | NVMe SSD         |
| ---- | -------- | ---------------- |
| 接口   | SATA     | PCIe             |
| 协议   | AHCI     | NVMe             |
| 理论带宽 | 600 MB/s | 数 GB/s ~ 数十 GB/s |
| 延迟   | 较高       | 更低               |
| 并发队列 | 32       | 65535            |
| 性能   | 中        | 高                |

性能关系：

```text
SATA SSD
      <
NVMe SSD
```

---

## 10. SATA 在 Linux 中

查看设备：

```bash
lsblk
```

查看接口信息：

```bash
lspci | grep SATA
```

查看磁盘：

```bash
fdisk -l
```

典型设备名：

```text
/dev/sda
/dev/sdb
/dev/sdc
```

---

## 11. SATA 与存储体系关系

```text
                +------+
                | CPU  |
                +------+
                    |
                PCIe总线
                    |
          +----------------+
          | SATA Controller|
          +----------------+
                    |
                 SATA
                    |
          +----------------+
          | HDD / SSD      |
          +----------------+
```

---

## 12. 一句话总结

**SATA 是一种用于连接 HDD、SSD 等存储设备的串行接口标准，采用 AHCI 协议和点对点通信架构，最高支持 6Gbps（约 600MB/s）带宽，是传统 PC 和嵌入式系统中广泛使用的存储接口。**
