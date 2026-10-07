# eMMC 简介

## 1. 什么是 eMMC

eMMC（Embedded MultiMedia Card）是一种集成式嵌入式存储器。

其内部集成了：

```text
+----------------------+
| eMMC                 |
|                      |
| +------------------+ |
| | NAND Flash       | |
| +------------------+ |
| | eMMC Controller  | |
| +------------------+ |
+----------------------+
```

即：

```text
eMMC = NAND Flash + Flash Controller
```

控制器负责：

* 坏块管理（BBM）
* ECC纠错
* 磨损均衡（Wear Leveling）
* 垃圾回收（GC）
* 地址映射（FTL）

因此上层软件无需直接管理 NAND Flash。

---

## 2. eMMC 在系统中的位置

```text
+---------+
|   CPU   |
+---------+
     |
     | eMMC Bus
     |
+---------+
|  eMMC   |
+---------+
```

CPU 通过 eMMC 控制器访问存储空间。

对于操作系统而言：

```text
eMMC
 ↓
Block Device
 ↓
文件系统
```

表现为普通块设备。

---

## 3. eMMC 内部结构

```text
eMMC
 ├── Host Interface
 ├── eMMC Controller
 ├── Cache
 └── NAND Flash
```

控制器完成：

```text
Logical Address
        ↓
FTL映射
        ↓
Physical Block
        ↓
NAND Flash
```

用户无需关心：

* Page
* Block
* Bad Block
* ECC

这些均由 eMMC 内部处理。

---

## 4. eMMC 分区结构

典型组成：

```text
eMMC
 ├── Boot Partition 1
 ├── Boot Partition 2
 ├── RPMB
 ├── User Area
 └── GP Partition
```

### Boot Partition

存放：

* BootLoader
* 启动代码

---

### RPMB

Replay Protected Memory Block

特点：

* 防篡改
* 支持认证
* 安全存储

常用于：

* 密钥
* 安全配置
* 认证信息

---

### User Area

最大区域：

```text
Kernel
RootFS
Application
User Data
```

---

### GP Partition

General Purpose Partition

用户自定义分区。

---

## 5. eMMC 启动流程

```text
Power On
    ↓
BootROM
    ↓
eMMC Boot Partition
    ↓
BootLoader
    ↓
Kernel
    ↓
RootFS
```

因此很多 SoC 支持：

```text
Boot From eMMC
```

直接从 eMMC 启动系统。

---

## 6. eMMC 主要接口信号

### 数据线

```text
DAT0~DAT7
```

支持：

```text
1-bit
4-bit
8-bit
```

模式。

---

### 命令线

```text
CMD
```

发送命令。

---

### 时钟线

```text
CLK
```

同步数据传输。

---

典型连接：

```text
CPU
 ├── CLK
 ├── CMD
 └── DAT[0:7]
         ↓
        eMMC
```

---

## 7. eMMC 工作模式

### Legacy

```text
26 MHz
```

较早模式。

---

### High Speed

```text
52 MHz
```

传统高速模式。

---

### HS200

```text
200 MHz
SDR
```

理论带宽：

```text
200 MB/s
```

---

### HS400

```text
200 MHz DDR
```

理论带宽：

```text
400 MB/s
```

当前主流高性能模式。

---

## 8. Linux中的eMMC

启动后通常显示：

```bash
/dev/mmcblk0
```

分区：

```bash
/dev/mmcblk0p1
/dev/mmcblk0p2
```

查看：

```bash
lsblk
cat /proc/partitions
```

查看设备信息：

```bash
cat /sys/block/mmcblk0/device/name
```

查看容量：

```bash
cat /sys/block/mmcblk0/size
```

---

## 9. eMMC 与 NAND Flash 的关系

```text
Raw NAND
 ├── ECC
 ├── FTL
 ├── Bad Block
 ├── Wear Leveling
 └── 驱动开发

eMMC
 └── 控制器全部处理
```

因此：

```text
开发难度

Raw NAND
    ↑
    |
    |
eMMC
```

eMMC 对软件更加友好。

---

## 10. eMMC、UFS、SSD 对比

| 项目   | eMMC  | UFS   | SSD       |
| ---- | ----- | ----- | --------- |
| 存储介质 | NAND  | NAND  | NAND      |
| 控制器  | 内置    | 内置    | 内置        |
| 接口   | MMC   | M-PHY | SATA/PCIe |
| 并发能力 | 低     | 高     | 高         |
| 性能   | 中     | 高     | 很高        |
| 成本   | 低     | 中     | 高         |
| 应用   | 嵌入式设备 | 手机    | PC/服务器    |

性能关系：

```text
eMMC < UFS < NVMe SSD
```

---

## 11. eMMC 优缺点

### 优点

* 成本低
* 集成度高
* 使用简单
* 可靠性高
* 易于系统启动

### 缺点

* 性能有限
* 并发能力弱
* 升级困难
* 容量扩展受限

---

## 12. 一句话总结

**eMMC 本质上是“NAND Flash + Flash控制器”的集成存储设备，对外提供标准块设备接口，内部完成 ECC、坏块管理、磨损均衡和地址映射，是嵌入式系统中最常见的启动和数据存储方案之一。**
