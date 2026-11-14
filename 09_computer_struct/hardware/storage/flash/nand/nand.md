# NAND Flash 简介

## 1. 什么是 NAND Flash

NAND Flash（闪存）是一种**非易失性存储器（Non-Volatile Memory）**，断电后数据不会丢失。

其内部利用**浮栅晶体管（Floating Gate Transistor）**存储电子，通过电子数量表示数据 0 和 1。NAND 结构采用串联方式连接存储单元，因此具有：

* 容量大
* 成本低
* 功耗低
* 写入速度快

目前广泛应用于：

* SSD
* U盘
* eMMC
* UFS
* SD卡
* 手机存储
* 嵌入式系统数据存储

NAND Flash 已成为现代存储设备的核心技术。

---

## 2. NAND Flash 存储层级

```text
Device
 └── Die
      └── Plane
           └── Block
                └── Page
                     └── Cell
```

| 层级     | 说明          |
| ------ | ----------- |
| Cell   | 最小存储单元      |
| Page   | 最小读写单位      |
| Block  | 最小擦除单位      |
| Plane  | 多个 Block 组成 |
| Die    | 独立存储芯片      |
| Device | 完整 NAND 芯片  |

NAND Flash 采用典型的：

```text
读  -> Page
写  -> Page
擦除 -> Block
```

即：

* Read Unit = Page
* Program Unit = Page
* Erase Unit = Block

这是 NAND Flash 最重要的特征。

---

## 3. Page 与 Block

典型组织结构：

```text
Block0
 ├── Page0
 ├── Page1
 ├── ...
 └── Page255

Block1
 ├── Page0
 ├── ...
```

常见规格：

| 项目      | 大小            |
| ------- | ------------- |
| Page    | 4KB ~ 16KB    |
| OOB     | 64B ~ 数百B     |
| Block   | 128~512 Pages |
| Block容量 | 1MB~8MB       |

Page 中包含：

```text
+----------------+
| Data Area      |
+----------------+
| OOB Area       |
+----------------+
```

OOB（Out Of Band）主要存放：

* ECC校验码
* 坏块标记
* Wear Leveling信息
* 文件系统元数据

---

## 4. NAND Flash 基本操作

### 读取(Read)

```text
Page -> Buffer -> Host
```

特点：

* 速度最快
* 按 Page 读取

---

### 写入(Program)

```text
Host -> Buffer -> Page
```

特点：

* 只能把 1 写成 0
* 不能直接把 0 写回 1

---

### 擦除(Erase)

```text
Block -> 全部变为1
```

特点：

* 只能按 Block 擦除
* 擦除后才能重新写入

因此：

```text
修改数据

= 读旧数据
+ 擦除Block
+ 重写数据
```

---

## 5. NAND Flash 类型

### SLC

Single Level Cell

```text
1 Cell = 1 Bit
```

特点：

* 速度最快
* 寿命最长
* 成本最高

---

### MLC

Multi Level Cell

```text
1 Cell = 2 Bits
```

特点：

* 容量提升
* 成本下降
* 寿命降低

---

### TLC

Triple Level Cell

```text
1 Cell = 3 Bits
```

特点：

* 主流消费级SSD
* 容量大
* 成本低

---

### QLC

Quad Level Cell

```text
1 Cell = 4 Bits
```

特点：

* 容量最大
* 成本最低
* 寿命最短

容量：

```text
SLC < MLC < TLC < QLC
```

寿命：

```text
SLC > MLC > TLC > QLC
```

---

## 6. NAND Flash 的问题

### 坏块（Bad Block）

出厂时可能已经存在坏块：

```text
Factory Bad Block
```

使用过程中也可能产生：

```text
Runtime Bad Block
```

因此必须进行：

* 坏块管理(BBM)
* ECC纠错

---

### 擦写寿命有限

每次擦除都会损伤氧化层。

典型寿命：

| 类型  | P/E次数      |
| --- | ---------- |
| SLC | 6万~10万次    |
| MLC | 3000~5000次 |
| TLC | 数千次        |
| QLC | 更低         |

---

## 7. 为什么 SSD 需要控制器

NAND Flash 本身并不智能。

SSD Controller 负责：

* 地址映射(FTL)
* ECC纠错
* 坏块管理
* 垃圾回收(GC)
* 磨损均衡(Wear Leveling)
* 缓存管理

```text
CPU
 ↓
SSD Controller
 ↓
NAND Flash
```

因此 SSD 的性能不仅取决于 NAND，也取决于控制器。

---

## 8. NAND Flash 与 NOR Flash 对比

| 项目    | NAND   | NOR        |
| ----- | ------ | ---------- |
| 容量    | 大      | 小          |
| 成本    | 低      | 高          |
| 读速度   | 一般     | 快          |
| 写速度   | 快      | 慢          |
| 擦除速度  | 快      | 慢          |
| XIP执行 | 不支持    | 支持         |
| 应用    | SSD/U盘 | BootROM/固件 |

通常：

```text
NOR Flash
    ↓
存代码

NAND Flash
    ↓
存数据
```

---

## 9. 一句话总结

**NAND Flash 是一种以 Page 为读写单位、以 Block 为擦除单位的非易失性存储器，具有高容量、低成本的特点，是 SSD、UFS、eMMC、U盘等现代存储设备的核心存储介质。**
