# SSD（Solid State Drive）固态硬盘

## 1. 什么是 SSD

SSD（Solid State Drive）即：

```text
固态硬盘
```

是一种使用 **NAND Flash** 存储数据的非易失性存储设备。

特点：

```text
断电不丢数据
无机械结构
读写速度快
抗震能力强
```

---

# 2. SSD 基本结构

```text
           SSD
            │
    ┌───────┼───────┐
    │               │
Controller      NAND Flash
    │               │
    └───────┬───────┘
            │
          DRAM
```

主要由：

```text
Controller（控制器）
NAND Flash（闪存）
DRAM Cache（缓存）
```

组成。

---

# 3. SSD 工作原理

数据写入流程：

```text
CPU
 │
 ▼
SSD Controller
 │
 ▼
NAND Flash
```

数据读取流程：

```text
NAND Flash
 │
 ▼
SSD Controller
 │
 ▼
CPU
```

控制器负责：

```text
地址映射
坏块管理
磨损均衡
ECC纠错
```

---

# 4. SSD 与 HDD 对比

| 项目    | SSD        | HDD |
| ----- | ---------- | --- |
| 存储介质  | NAND Flash | 磁盘  |
| 机械结构  | 无          | 有   |
| 速度    | 快          | 较慢  |
| 噪音    | 无          | 有   |
| 抗震    | 强          | 弱   |
| 功耗    | 低          | 较高  |
| 容量价格比 | 较高         | 较低  |

---

# 5. SSD 常见接口

| 接口               | 典型速率       |
| ---------------- | ---------- |
| SATA SSD         | 约 550 MB/s |
| NVMe PCIe 3.0 x4 | 约 3.5 GB/s |
| NVMe PCIe 4.0 x4 | 约 7 GB/s   |
| NVMe PCIe 5.0 x4 | 10+ GB/s   |

---

# 6. SSD 存储单元

NAND Flash 以 Cell 保存数据。

| 类型  | 每单元位数 |
| --- | ----- |
| SLC | 1 bit |
| MLC | 2 bit |
| TLC | 3 bit |
| QLC | 4 bit |

特点：

```text
SLC
速度最快
寿命最长

QLC
容量最大
成本最低
```

目前主流：

```text
TLC
```

---

# 7. SSD 数据组织

```text
SSD
 │
 ├── Block（块）
 │
 └── Page（页）
```

例如：

```text
Block
 ├── Page0
 ├── Page1
 ├── Page2
 └── ...
```

特点：

```text
按页写入

按块擦除
```

---

# 8. SSD 核心技术

### FTL

Flash Translation Layer

```text
逻辑地址(LBA)
        ↓
物理Flash地址
```

负责地址映射。

---

### Wear Leveling

磨损均衡：

```text
避免某些块频繁擦写
```

延长寿命。

---

### Garbage Collection

垃圾回收：

```text
整理无效数据
释放空间
```

---

### ECC

错误校验：

```text
检测并纠正数据错误
```

提高可靠性。

---

# 9. SSD 在系统中的位置

```text
Application
      │
      ▼
File System
      │
      ▼
Block Driver
      │
      ▼
SATA/NVMe Driver
      │
      ▼
SSD Controller
      │
      ▼
NAND Flash
```

---

# 10. 常见应用

| 场景    | 类型                  |
| ----- | ------------------- |
| PC    | SATA SSD / NVMe SSD |
| 服务器   | 企业级 NVMe SSD        |
| 笔记本   | M.2 NVMe SSD        |
| 嵌入式设备 | eMMC / UFS / SSD    |
| 数据中心  | PCIe SSD            |

---

# 11. 核心知识点

```text
SSD
 │
 ├── NAND Flash
 ├── Controller
 ├── DRAM Cache
 ├── SATA
 ├── NVMe
 ├── FTL
 ├── Wear Leveling
 ├── Garbage Collection
 ├── ECC
 └── TLC/QLC
```

---

# 12. 总结

SSD 是一种基于 NAND Flash 的高速存储设备。

核心结构：

```text
CPU
 │
 ▼
SSD Controller
 │
 ▼
NAND Flash
```

核心优势：

```text
高速
低延迟
无机械结构
低功耗
高可靠性
```

一句话总结：

> **SSD 本质上是由控制器管理 NAND Flash 的高速非易失性存储设备，通过 FTL、磨损均衡和 ECC 等技术实现高性能和高可靠的数据存储。**
