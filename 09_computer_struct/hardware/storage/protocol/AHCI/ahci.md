# AHCI 协议简介

## 1. 什么是 AHCI

AHCI（Advanced Host Controller Interface）是由 Intel 提出的**主机控制器接口规范**，主要用于规定操作系统如何通过 SATA 控制器访问 SATA 存储设备。

典型结构：

```text
CPU
 ↓
SATA Driver
 ↓
AHCI
 ↓
SATA Controller
 ↓
SATA Link
 ↓
HDD / SSD
```

> **AHCI 不是 SATA 总线，而是 SATA Host Controller 的软件接口规范。**

---

## 2. AHCI 解决什么问题

早期 SATA 控制器可以使用厂商私有接口，操作系统需要针对不同控制器编写驱动。

AHCI 提供统一的控制器编程接口：

```text
Operating System
       ↓
   AHCI Driver
       ↓
  AHCI Controller
       ↓
      SATA
```

这样不同厂商的 SATA 控制器可以采用统一的软件访问方式。

---

## 3. AHCI 的核心功能

AHCI 主要提供：

* SATA 设备管理
* 命令队列
* DMA 数据传输
* NCQ
* 热插拔
* 端口管理
* 中断管理

---

## 4. AHCI 控制器结构

一个典型 AHCI Controller 包含多个 Port：

```text
              AHCI Controller
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
     Port 0        Port 1        Port 2
       ↓             ↓             ↓
      SSD           HDD           SSD
```

每个 Port 可以连接一个 SATA 设备。

---

## 5. Command List

AHCI 使用 **Command List** 管理 SATA 命令。

```text
Command List
 ├── Command 0
 ├── Command 1
 ├── Command 2
 └── ...
```

每个命令对应一个：

```text
Command Header
       ↓
Command Table
       ↓
SATA Command
```

例如：

```text
Read
Write
Identify
Flush
```

---

## 6. DMA 数据传输

AHCI 支持 DMA，数据不需要 CPU 逐字节搬运。

```text
Host Memory
     ↑
     │ DMA
     ↓
AHCI Controller
     ↓
SATA Device
```

例如写操作：

```text
CPU
 ↓
创建命令
 ↓
AHCI Command List
 ↓
DMA
 ↓
SATA SSD
```

这样可以降低 CPU 负担。

---

## 7. NCQ

NCQ（Native Command Queuing）是 SATA 设备的重要功能。

例如 CPU 提交：

```text
Read A
Read B
Read C
Read D
```

设备可以根据自身情况调整执行顺序：

```text
Read B
Read D
Read A
Read C
```

目的：

* 提高 I/O 效率
* 减少机械硬盘寻道
* 提高并发访问性能

AHCI 最多支持：

```text
32 个命令
```

---

## 8. AHCI 与 SATA 的关系

两者处于不同层次：

```text
+----------------------+
| Operating System     |
+----------------------+
          ↓
+----------------------+
| AHCI Driver          | ← 软件接口规范
+----------------------+
          ↓
+----------------------+
| AHCI Controller      |
+----------------------+
          ↓
+----------------------+
| SATA Link            | ← 串行传输链路
+----------------------+
          ↓
+----------------------+
| SATA HDD / SSD       |
+----------------------+
```

简单理解：

```text
AHCI
 ↓
规定“Host 如何控制 SATA Controller”

SATA
 ↓
负责“Controller 如何与设备进行串行通信”
```

---

## 9. AHCI 与 NVMe 对比

| 项目    | AHCI         | NVMe     |
| ----- | ------------ | -------- |
| 面向设备  | SATA HDD/SSD | PCIe SSD |
| 所在体系  | SATA         | PCIe     |
| 设计目标  | 传统存储         | 高速 SSD   |
| 队列    | 1            | 多队列      |
| 单队列深度 | 32           | 可达 65535 |
| 并发能力  | 较低           | 很高       |
| 延迟    | 较高           | 较低       |
| DMA   | 支持           | 支持       |

---

## 10. Linux 中的 AHCI

Linux 通常通过：

```text
libata
  ↓
AHCI Driver
  ↓
SATA Controller
```

常见驱动模块：

```bash
ahci
libata
```

查看 SATA 控制器：

```bash
lspci | grep -i sata
```

查看磁盘：

```bash
lsblk
```

典型 SATA 磁盘：

```text
/dev/sda
/dev/sdb
```

---

## 11. AHCI 工作流程

以读取数据为例：

```text
1. 应用发起 Read
        ↓
2. 文件系统
        ↓
3. Block Layer
        ↓
4. AHCI Driver 创建命令
        ↓
5. Command List
        ↓
6. AHCI Controller
        ↓
7. SATA Link
        ↓
8. SSD/HDD
        ↓
9. DMA → Host Memory
        ↓
10. 中断通知 CPU
```

---

## 12. 一句话总结

**AHCI 是一种 SATA 主机控制器接口规范，通过统一的寄存器、Command List、DMA、NCQ 和中断机制，让操作系统能够标准化地控制 SATA HDD/SSD。**

核心关系：

```text
AHCI
 ↓
控制 SATA Controller

SATA
 ↓
连接 Host 与 Storage Device

HDD / SSD
 ↓
```
