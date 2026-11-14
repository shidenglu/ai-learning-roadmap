# Flash（闪存）详解

# 1. 什么是Flash

Flash（闪存）是一种：

```text
Non-Volatile Memory
非易失性存储器
```

特点：

```text
断电不丢失数据
容量大
功耗低
可重复擦写
```

现代设备几乎都在使用Flash：

```text
U盘
SSD
手机存储
eMMC
UFS
SPI Flash
NOR Flash
NAND Flash
```

---

# 2. 为什么叫Flash

1984年东芝发明这种存储器时：

```text
一次擦除大量数据
像闪电一样快
```

因此命名：

```text
Flash Memory
```

---

# 3. Flash在计算机中的位置

存储层次：

```text
CPU Register
    ↓
L1 Cache
    ↓
L2 Cache
    ↓
L3 Cache
    ↓
DRAM
    ↓
Flash
    ↓
HDD
```

特点：

```text
速度慢于DRAM
快于机械硬盘
断电不丢失
```

---

# 4. Flash与DRAM区别

| 项目   | DRAM | Flash |
| ---- | ---- | ----- |
| 断电保存 | 否    | 是     |
| 速度   | 快    | 较慢    |
| 容量   | 中等   | 大     |
| 成本   | 高    | 低     |
| 刷新   | 需要   | 不需要   |

---

# 5. Flash的基本原理

Flash利用：

```text
Floating Gate
浮栅晶体管
```

保存数据。

结构：

```text
      Control Gate
            │
            ▼
      ┌─────────┐
      │ Floating│
      │  Gate   │
      └─────────┘
            │
      ┌─────────┐
      │ Channel │
      └─────────┘
```

---

# 6. 浮栅是什么

浮栅是一个：

```text
被绝缘层包围的导体
```

电子进入后：

```text
无法轻易逃出
```

因此：

```text
断电后仍能保存数据
```

---

# 7. 数据如何存储

浮栅有电子：

```text
1
```

或者：

```text
0
```

通过检测晶体管阈值电压判断。

---

# 8. Flash读操作

读取过程：

```text
控制器
 ↓
检测阈值电压
 ↓
判断0或1
```

特点：

```text
速度较快
不会损伤数据
```

---

# 9. Flash写操作

写入过程：

```text
高电压
 ↓
电子注入浮栅
 ↓
保存数据
```

称为：

```text
Program
编程
```

---

# 10. Flash擦除操作

Flash不能直接覆盖写。

例如：

```text
0 → 1
```

无法直接修改。

必须：

```text
擦除
 ↓
重新写入
```

---

# 11. 为什么擦除很重要

Flash特点：

```text
读最快
写次之
擦除最慢
```

因此：

```text
擦除是性能瓶颈
```

---

# 12. Flash最小操作单位

## 读

通常：

```text
Page
```

例如：

```text
4KB
8KB
16KB
```

---

## 写

也是：

```text
Page
```

---

## 擦除

必须按：

```text
Block
```

进行。

例如：

```text
256 Pages
```

组成：

```text
1 Block
```

---

# 13. Flash组织结构

```text
Flash
│
├── Die
│
├── Plane
│
├── Block
│
└── Page
```

---

# 14. Page

Page是最小读写单位。

例如：

```text
4KB
```

---

# 15. Block

多个Page组成：

```text
Block
```

例如：

```text
256 × 4KB
=
1MB
```

---

# 16. NOR Flash

结构：

```text
并联连接
```

特点：

```text
随机读取快
支持XIP
容量较小
价格较高
```

---

典型应用：

```text
Bootloader
MCU程序存储
BIOS
固件
```

---

# 17. NAND Flash

结构：

```text
串联连接
```

特点：

```text
容量大
成本低
写入快
```

---

典型应用：

```text
SSD
eMMC
UFS
TF卡
U盘
```

---

# 18. NOR与NAND对比

| 项目   | NOR | NAND |
| ---- | --- | ---- |
| 读取速度 | 快   | 较快   |
| 写入速度 | 慢   | 快    |
| 容量   | 小   | 大    |
| 成本   | 高   | 低    |
| XIP  | 支持  | 不支持  |

---

# 19. XIP

XIP：

```text
Execute In Place
原地执行
```

例如：

```text
CPU
 ↓
直接从Flash取指
```

无需复制到RAM。

NOR Flash支持。

---

# 20. NAND Flash单元类型

## SLC

Single Level Cell

```text
1 Cell
=
1 bit
```

特点：

```text
最快
最可靠
最贵
```

---

## MLC

Multi Level Cell

```text
1 Cell
=
2 bit
```

---

## TLC

Triple Level Cell

```text
1 Cell
=
3 bit
```

---

## QLC

Quad Level Cell

```text
1 Cell
=
4 bit
```

---

# 21. Flash寿命

每次擦除都会损伤Flash。

典型寿命：

```text
SLC
100000次
```

```text
MLC
10000次
```

```text
TLC
3000次
```

```text
QLC
1000次左右
```

---

# 22. Wear Leveling

磨损均衡技术。

目的：

```text
避免某些Block过度使用
```

例如：

```text
Block0
Block1
Block2
```

轮流写入。

---

# 23. Bad Block

生产过程中：

```text
部分Block损坏
```

属于正常现象。

Flash会记录：

```text
Bad Block Table
```

---

# 24. ECC

Flash存在位翻转问题。

需要：

```text
ECC
Error Correcting Code
```

进行纠错。

例如：

```text
BCH
LDPC
```

---

# 25. Flash Controller

现代Flash系统都有控制器：

```text
Controller
```

负责：

```text
ECC
Wear Leveling
坏块管理
地址映射
```

---

# 26. SSD中的Flash

SSD结构：

```text
SSD
│
├── Controller
├── DRAM Cache
└── NAND Flash
```

---

# 27. FTL

FTL：

```text
Flash Translation Layer
```

作用：

```text
逻辑地址
 ↓
物理地址
```

转换。

---

# 28. Flash与DMA

数据读取：

```text
Flash
 ↓
Controller
 ↓
DMA
 ↓
DDR
```

无需CPU逐字节搬运。

---

# 29. MCU中的Flash

例如：

```text
STM32
NXP
GD32
```

结构：

```text
Flash
 ↓
存放程序
```

---

程序：

```c
int main()
{
    while(1);
}
```

最终保存在：

```text
Internal Flash
```

中。

---

# 30. ARM启动过程

上电：

```text
Reset
 ↓
BootROM
 ↓
Flash
 ↓
程序入口
```

CPU从Flash读取指令。

---

# 31. Linux系统中的Flash

常见：

```text
SPI NOR
SPI NAND
eMMC
UFS
```

查看：

```bash
cat /proc/mtd
```

---

# 32. Flash与文件系统

裸Flash不能直接使用传统文件系统。

常见：

```text
JFFS2
YAFFS2
UBIFS
```

专门针对Flash设计。

---

# 33. Flash性能指标

## Read

读取速度：

```text
MB/s
GB/s
```

---

## Program

写入速度：

```text
MB/s
```

---

## Erase

擦除时间：

```text
ms
```

---

## Endurance

寿命：

```text
P/E Cycle
```

---

# 34. Flash发展趋势

```text
2D NAND
 ↓
3D NAND
 ↓
176 Layer
 ↓
232 Layer
 ↓
300+ Layer
```

容量持续提升。

---

# 35. 总结

## Flash是什么

```text
非易失性存储器
```

利用：

```text
Floating Gate
```

保存数据。

---

## 核心特点

```text
断电不丢失
容量大
成本低
可擦写
```

---

## 两大类型

```text
NOR Flash
NAND Flash
```

---

## 核心结构

```text
Page
Block
Plane
Die
```

---

## 关键技术

```text
ECC
Wear Leveling
Bad Block
FTL
```

---

## 在嵌入式和操作系统中的位置

```text
CPU
 ↓
Cache
 ↓
DRAM
 ↓
Flash
 ↓
SSD/eMMC/UFS
```

---

## 对嵌入式和OS工程师最重要的知识链路

```text
Flash
 ↓
ECC
 ↓
Wear Leveling
 ↓
FTL
 ↓
DMA
 ↓
文件系统
 ↓
Bootloader
 ↓
Linux MTD
```

掌握这条链路后，就能进一步学习：

```text
SPI NOR
SPI NAND
eMMC
UFS
SSD控制器
NVMe
UBIFS
JFFS2
```

以及现代嵌入式系统和存储系统的设计原理。
