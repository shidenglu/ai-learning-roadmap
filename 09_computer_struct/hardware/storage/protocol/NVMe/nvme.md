# NVMe 协议简介

## 1. 什么是 NVMe

NVMe（Non-Volatile Memory Express）是一种专门为 **非易失性存储器，尤其是 SSD** 设计的高速存储协议。

核心目标：

* 低延迟
* 高并发
* 高吞吐
* 充分利用 PCIe 带宽

典型结构：

```text
CPU
 ↓
PCIe
 ↓
NVMe Protocol
 ↓
SSD Controller
 ↓
NAND Flash
```

> **PCIe 是传输通道，NVMe 是存储通信协议。**

---

## 2. NVMe 解决什么问题

传统 SATA SSD：

```text
CPU
 ↓
SATA
 ↓
AHCI
 ↓
SSD
```

AHCI 最初主要面向传统硬盘设计，并发能力有限。

NVMe：

```text
CPU
 ↓
PCIe
 ↓
NVMe
 ↓
SSD
```

针对高速 NAND/SSD 重新设计，减少协议开销，提高并发能力。

---

## 3. NVMe 核心架构

```text
+----------------------+
| Application          |
+----------------------+
          ↓
+----------------------+
| File System          |
+----------------------+
          ↓
+----------------------+
| Block Layer          |
+----------------------+
          ↓
+----------------------+
| NVMe Driver          |
+----------------------+
          ↓
+----------------------+
| PCIe                  |
+----------------------+
          ↓
+----------------------+
| NVMe Controller      |
+----------------------+
          ↓
+----------------------+
| NAND Flash           |
+----------------------+
```

---

## 4. Queue：NVMe 的核心

NVMe 最重要的设计之一是**多队列（Multi-Queue）**。

主要包括：

```text
Submission Queue (SQ)
        ↓
    提交命令

Completion Queue (CQ)
        ↓
    返回结果
```

完整流程：

```text
CPU
 ↓
Submission Queue
 ↓
NVMe Controller
 ↓
NAND
 ↓
Completion Queue
 ↓
CPU
```

---

## 5. Submission Queue

SQ（Submission Queue）用于存放主机提交给 SSD 的命令。

例如：

```text
Read
Write
Flush
Identify
```

CPU：

```text
构造 Command
      ↓
写入 SQ
      ↓
通知 SSD
```

---

## 6. Completion Queue

CQ（Completion Queue）用于 SSD 返回命令执行结果。

```text
SSD Controller
      ↓
执行命令
      ↓
写入 CQ
      ↓
Interrupt / Polling
      ↓
CPU
```

因此：

```text
SQ → SSD
CQ ← SSD
```

---

## 7. NVMe Command

一个 NVMe 命令包含：

```text
+----------------------+
| Opcode               |
+----------------------+
| Namespace ID         |
+----------------------+
| Start LBA            |
+----------------------+
| Length               |
+----------------------+
| PRP / SGL            |
+----------------------+
| Control              |
+----------------------+
```

常见命令：

| 命令           | 功能     |
| ------------ | ------ |
| Read         | 读取数据   |
| Write        | 写入数据   |
| Flush        | 刷新缓存   |
| Identify     | 获取设备信息 |
| Create Queue | 创建队列   |
| Delete Queue | 删除队列   |

---

## 8. NVMe 数据传输

NVMe 不负责直接搬运大量数据，而是通过 **DMA** 访问主机内存。

```text
Host Memory
     ↑
     │ DMA
     ↓
NVMe Controller
     ↓
NAND
```

例如读取：

```text
NAND
 ↓
NVMe Controller
 ↓ DMA
Host Memory
 ↓
CPU
```

这样 CPU 不需要参与每一个字节的数据搬运。

---

## 9. Namespace

NVMe 使用 Namespace 表示逻辑存储空间。

```text
NVMe Controller
 ├── Namespace 1
 ├── Namespace 2
 └── Namespace 3
```

可以理解为：

```text
Namespace ≈ 逻辑磁盘
```

Linux 中常见：

```bash
/dev/nvme0n1
```

其中：

```text
nvme0 → Controller 0
n1    → Namespace 1
```

---

## 10. NVMe 与 PCIe 的关系

```text
+----------------+
| NVMe Protocol  |
+----------------+
| PCIe Transport |
+----------------+
| Physical Layer |
+----------------+
```

可以简单理解：

```text
PCIe
 ↓
负责“把数据传过去”

NVMe
 ↓
负责“告诉 SSD 做什么”
```

例如：

```text
CPU
 │
 │ PCIe
 ▼
NVMe SSD
 │
 │ NVMe Read Command
 ▼
读取指定 LBA
```

---

## 11. NVMe 的主要优势

### 多队列

```text
CPU Core 0 → SQ0
CPU Core 1 → SQ1
CPU Core 2 → SQ2
CPU Core 3 → SQ3
```

适合多核 CPU。

### 低延迟

减少传统存储协议中的中间层。

### 高并发

支持大量并行 I/O 请求。

### 高带宽

可以充分利用：

```text
PCIe 3.0
PCIe 4.0
PCIe 5.0
PCIe 6.0
...
```

---

## 12. SATA 与 NVMe

| 项目   | SATA SSD   | NVMe SSD  |
| ---- | ---------- | --------- |
| 传输总线 | SATA       | PCIe      |
| 存储协议 | ATA/AHCI体系 | NVMe      |
| 队列   | 少          | 多         |
| 并发能力 | 较低         | 高         |
| 延迟   | 较高         | 较低        |
| 带宽   | ~600 MB/s  | 数 GB/s 以上 |
| 设计目标 | 传统存储       | 高速非易失性存储  |

---

## 13. Linux 中的 NVMe 软件栈

```text
Application
     ↓
File System
     ↓
Block Layer
     ↓
NVMe Driver
     ↓
PCIe Driver
     ↓
PCIe Hardware
     ↓
NVMe Controller
```

常用命令：

```bash
nvme list
lsblk
```

典型设备：

```text
/dev/nvme0n1
/dev/nvme0n1p1
```

---

## 14. 一句话总结

**NVMe 是一种运行在 PCIe 上、面向高速非易失性存储设备设计的存储协议，其核心是多队列、DMA 和低协议开销，从而实现低延迟、高吞吐和高并发的 SSD 访问。**
