# NVMe 接口简介

## 1. 什么是 NVMe

NVMe（Non-Volatile Memory Express）是一种专门为 **SSD** 设计的高速存储协议。

其运行在：

```text
NVMe Protocol
      ↓
PCIe Bus
      ↓
SSD
```

之上。

目的：

* 降低存储访问延迟
* 提高并发能力
* 充分发挥 NAND Flash 性能

---

## 2. NVMe 与 SATA 的区别

传统 SSD：

```text
SSD
 ↓
SATA
 ↓
AHCI
 ↓
CPU
```

NVMe SSD：

```text
SSD
 ↓
PCIe
 ↓
NVMe
 ↓
CPU
```

特点：

* 不再经过 SATA 控制器
* 不使用 AHCI 协议
* 直接利用 PCIe 高带宽

---

## 3. NVMe 架构

```text
Application
      ↓
File System
      ↓
Block Layer
      ↓
NVMe Driver
      ↓
PCIe Controller
      ↓
NVMe SSD
```

核心思想：

```text
CPU ←→ NVMe Queue ←→ SSD
```

通过队列实现高并发访问。

---

## 4. PCIe 与 NVMe 的关系

很多人容易混淆：

| 名称   | 类型   |
| ---- | ---- |
| PCIe | 总线接口 |
| NVMe | 存储协议 |

关系：

```text
PCIe = 公路
NVMe = 交通规则
SSD  = 汽车
```

即：

```text
NVMe SSD
 = PCIe + NVMe
```

---

## 5. PCIe 通道（Lane）

PCIe 采用 Lane 传输数据：

```text
PCIe x1
PCIe x2
PCIe x4
PCIe x8
PCIe x16
```

NVMe SSD 常见：

```text
PCIe x4
```

结构：

```text
Lane0
Lane1
Lane2
Lane3
```

4条链路同时传输数据。

---

## 6. 常见 NVMe 规格

| 接口          | 理论带宽      |
| ----------- | --------- |
| PCIe 3.0 x4 | ≈ 4 GB/s  |
| PCIe 4.0 x4 | ≈ 8 GB/s  |
| PCIe 5.0 x4 | ≈ 16 GB/s |
| PCIe 6.0 x4 | ≈ 32 GB/s |

性能远高于：

```text
SATA III
≈ 600 MB/s
```

---

## 7. NVMe 队列机制

AHCI：

```text
1 Queue
32 Commands
```

NVMe：

```text
65535 Queues
65535 Commands/Queue
```

示意：

```text
CPU Core0 → SQ0
CPU Core1 → SQ1
CPU Core2 → SQ2
CPU Core3 → SQ3

             ↓

          NVMe SSD
```

优势：

* 多核并行
* 高IOPS
* 低延迟

---

## 8. Submission Queue 与 Completion Queue

### SQ（提交队列）

CPU提交请求：

```text
Read
Write
Flush
```

放入：

```text
Submission Queue
```

---

### CQ（完成队列）

SSD处理完成后：

```text
Completion Queue
```

通知CPU。

流程：

```text
CPU
 ↓
SQ
 ↓
NVMe SSD
 ↓
CQ
 ↓
CPU
```

---

## 9. NVMe 命名空间（Namespace）

NVMe 引入：

```text
Namespace
```

类似：

```text
逻辑磁盘
```

示例：

```text
NVMe SSD
 ├── Namespace1
 ├── Namespace2
 └── Namespace3
```

每个 Namespace 可以独立管理。

---

## 10. Linux 中的 NVMe

查看设备：

```bash
nvme list
```

查看块设备：

```bash
lsblk
```

典型设备：

```text
/dev/nvme0n1
/dev/nvme0n1p1
/dev/nvme0n1p2
```

含义：

```text
nvme0
  ↓
控制器0

n1
  ↓
Namespace1

p1
  ↓
分区1
```

---

## 11. NVMe SSD 内部结构

```text
+-------------------+
| NVMe Controller   |
+-------------------+
| DRAM Cache        |
+-------------------+
| FTL               |
+-------------------+
| ECC               |
+-------------------+
| NAND Flash        |
+-------------------+
```

控制器负责：

* FTL地址映射
* ECC纠错
* 坏块管理
* Wear Leveling
* Garbage Collection

---

## 12. SATA SSD 与 NVMe SSD 对比

| 项目   | SATA SSD | NVMe SSD       |
| ---- | -------- | -------------- |
| 总线   | SATA     | PCIe           |
| 协议   | AHCI     | NVMe           |
| 理论带宽 | 600 MB/s | 数 GB/s~数十 GB/s |
| 队列数  | 1        | 65535          |
| 队列深度 | 32       | 65535          |
| 延迟   | 较高       | 更低             |
| IOPS | 较低       | 更高             |
| 并发能力 | 一般       | 极强             |

---

## 13. 存储体系结构关系

```text
                +------+
                | CPU  |
                +------+
                    |
                PCIe总线
                    |
          +----------------+
          | NVMe Controller|
          +----------------+
                    |
                NAND Flash
```

数据路径：

```text
CPU
 ↓
PCIe
 ↓
NVMe
 ↓
SSD Controller
 ↓
NAND Flash
```

---

## 14. 一句话总结

**NVMe 是运行在 PCIe 总线上的高性能存储协议，通过多队列并行机制大幅降低访问延迟并提升吞吐量，已成为现代 SSD 的主流接口标准。**
