# DRAM（动态随机存取存储器）详解

# 1. 什么是DRAM

DRAM：

```text
Dynamic Random Access Memory
动态随机存取存储器
```

是现代计算机中最主要的主存（Main Memory）。

例如：

```text
DDR3
DDR4
DDR5
LPDDR4
LPDDR5
```

本质上都属于DRAM。

---

# 2. DRAM在计算机中的位置

存储层次结构：

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
SSD/HDD
```

特点：

```text
速度介于Cache和磁盘之间
容量远大于Cache
成本远低于SRAM
```

---

# 3. 为什么需要DRAM

如果全部使用Cache中的SRAM：

```text
速度很快
但是成本极高
面积极大
```

例如：

```text
64GB SRAM
```

几乎不可实现。

因此采用：

```text
SRAM -> Cache
DRAM -> 主存
```

的结构。

---

# 4. DRAM的核心思想

DRAM使用：

```text
电容
+
晶体管
```

存储1bit数据。

结构：

```text
      Word Line
          │
          ▼
      ┌─────┐
Bit ─▶│ T   │
Line  └─┬───┘
        │
      ┌─▼─┐
      │ C │
      └───┘
```

其中：

```text
T = 晶体管
C = 电容
```

---

# 5. DRAM如何存储数据

电容有电：

```text
1
```

电容无电：

```text
0
```

例如：

```text
有电荷 -> 1
无电荷 -> 0
```

---

# 6. 为什么叫动态存储器

因为电容会漏电。

例如：

```text
1
 ↓
慢慢放电
 ↓
0
```

如果不处理：

```text
数据会丢失
```

因此必须定期刷新。

这就是：

```text
Dynamic
动态
```

的来源。

---

# 7. Refresh机制

DRAM必须周期性刷新。

典型要求：

```text
64ms
```

内所有单元必须刷新一次。

流程：

```text
读取
↓
重新写回
↓
恢复电荷
```

---

# 8. DRAM单元结构

一个Cell：

```text
1T1C
```

即：

```text
1个晶体管
1个电容
```

优点：

```text
面积小
成本低
容量大
```

---

# 9. SRAM与DRAM对比

SRAM：

```text
6个晶体管
```

DRAM：

```text
1个晶体管
+
1个电容
```

---

| 项目 | SRAM  | DRAM |
| -- | ----- | ---- |
| 速度 | 快     | 慢    |
| 面积 | 大     | 小    |
| 成本 | 高     | 低    |
| 刷新 | 不需要   | 需要   |
| 用途 | Cache | 主存   |

---

# 10. DRAM阵列结构

大量Cell组成矩阵：

```text
      Column

      0 1 2 3
      ↓ ↓ ↓ ↓

R0 -> x x x x
R1 -> x x x x
R2 -> x x x x
R3 -> x x x x
```

称为：

```text
Memory Array
```

---

# 11. 行(Row)和列(Column)

访问数据：

```text
先选行
再选列
```

例如：

```text
Row 100
Column 200
```

即可定位一个Cell。

---

# 12. Word Line

控制：

```text
行选择
```

例如：

```text
WL0
WL1
WL2
```

激活某一行：

```text
Activate Row
```

---

# 13. Bit Line

负责：

```text
数据读写
```

例如：

```text
BL0
BL1
BL2
```

连接到感应放大器。

---

# 14. Sense Amplifier

由于电容非常小：

```text
几十fF
```

读出信号极弱。

因此需要：

```text
Sense Amplifier
```

完成：

```text
放大
判决
恢复
```

---

# 15. DRAM读取过程

读取地址：

```text
(Row, Column)
```

流程：

```text
Activate Row
 ↓
Sense Amplifier
 ↓
Read Column
 ↓
返回数据
```

---

# 16. DRAM写入过程

```text
Activate Row
 ↓
Write Data
 ↓
存入Cell
```

---

# 17. 读操作是破坏性的

DRAM读取时：

```text
电容电荷被释放
```

因此：

```text
读完必须写回
```

称为：

```text
Read Restore
```

---

# 18. Bank结构

现代DRAM被划分为多个Bank。

例如：

```text
Bank0
Bank1
Bank2
Bank3
...
```

---

作用：

```text
提高并行度
```

例如：

```text
CPU访问Bank0

同时

DMA访问Bank1
```

---

# 19. Rank结构

多个Chip组成：

```text
Rank
```

例如：

```text
8个x8芯片
```

组成：

```text
64bit Rank
```

---

# 20. Channel结构

CPU通过Channel访问内存。

例如：

```text
Single Channel
Dual Channel
Quad Channel
```

---

双通道：

```text
Channel0
Channel1
```

可同时工作。

带宽翻倍。

---

# 21. DDR是什么

DDR：

```text
Double Data Rate
双倍数据速率
```

特点：

```text
上升沿传输
下降沿传输
```

例如：

```text
时钟
↑ ↓ ↑ ↓ ↑ ↓
```

每周期传输两次数据。

---

# 22. DDR发展历程

```text
DDR
DDR2
DDR3
DDR4
DDR5
```

速度越来越高。

---

大致速率：

| 类型   | 速率         |
| ---- | ---------- |
| DDR3 | 1600 MT/s  |
| DDR4 | 3200 MT/s  |
| DDR5 | 6400+ MT/s |

---

# 23. 内存控制器

现代CPU内部集成：

```text
Memory Controller
```

结构：

```text
CPU
 │
IMC
 │
DDR
```

IMC：

```text
Integrated Memory Controller
```

---

# 24. DRAM访问流程

CPU执行：

```c
x = a[100];
```

流程：

```text
CPU
 ↓
L1 Cache
 ↓
L2 Cache
 ↓
L3 Cache
 ↓
Memory Controller
 ↓
DRAM
 ↓
返回数据
```

---

# 25. Cache Miss

当Cache中没有数据：

```text
Cache Miss
```

发生：

```text
CPU
 ↓
DRAM访问
```

此时延迟会急剧增加。

---

# 26. DRAM访问延迟

典型：

```text
50ns~100ns
```

而：

```text
L1 Cache
```

仅：

```text
1ns左右
```

因此：

```text
DRAM比L1慢几十倍
```

甚至上百倍。

---

# 27. DRAM带宽

例如：

```text
DDR4-3200
64bit
```

理论带宽：

```text
25.6 GB/s
```

计算：

```text
3200 MT/s
× 8 Byte
=
25.6 GB/s
```

---

# 28. ECC内存

ECC：

```text
Error Correcting Code
```

增加校验位。

例如：

```text
64bit Data
+
8bit ECC
```

---

作用：

```text
检测错误
纠正错误
```

服务器广泛使用。

---

# 29. DRAM与DMA

DMA访问：

```text
网卡
 ↓
DMA
 ↓
DRAM
```

无需CPU搬运。

例如：

```text
网卡收包
SSD读写
GPU传输
```

都依赖DRAM。

---

# 30. 总结

## DRAM是什么

```text
主存储器
```

利用：

```text
晶体管
+
电容
```

保存数据。

---

## 核心特点

```text
容量大
成本低
需要刷新
速度低于SRAM
```

---

## 关键结构

```text
Cell
Row
Column
Bank
Rank
Channel
```

---

## 数据访问路径

```text
CPU
 ↓
Cache
 ↓
Memory Controller
 ↓
DRAM
```

---

## 对操作系统和体系结构工程师最重要的知识链路

```text
CPU
 ↓
Cache
 ↓
TLB
 ↓
MMU
 ↓
Memory Controller
 ↓
DRAM
 ↓
DMA
 ↓
SSD/网卡/GPU
```

理解这条链路后，就能进一步学习：

```text
DDR控制器
Cache一致性
NUMA
DMA
AXI总线
虚拟内存
```

以及现代 ARM SoC 和 x86 CPU 的内存系统设计原理。
