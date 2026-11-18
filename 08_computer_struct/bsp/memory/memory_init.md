# BSP 内存初始化

## 1. 概述

BSP 中的内存初始化主要负责让 CPU 能够正确使用系统内存，并为后续 Kernel、RTOS 和应用建立内存运行环境。

```text
CPU
 ↓
内存控制器初始化
 ↓
DDR初始化
 ↓
建立内存映射
 ↓
MMU / Cache配置
 ↓
内存可用
```

## 2. 主要初始化内容

### ① DDR 初始化

配置 DDR 控制器，使 CPU 能够正常访问 DDR。

```text
DDR Controller
      ↓
DDR PHY
      ↓
DDR Memory
```

主要包括：

```text
DDR时序
工作频率
容量
位宽
读写训练
```

---

### ② 内存检测

验证 DDR 是否能够正常读写：

```c
write(addr, data);
read(addr);
compare();
```

检查：

```text
地址
数据
容量
读写可靠性
```

---

### ③ 建立物理内存布局

描述系统物理内存的使用范围：

```text
0x00000000 ┌──────────────┐
           │ Boot / ROM   │
           ├──────────────┤
           │ Kernel       │
           ├──────────────┤
           │ DMA Memory   │
           ├──────────────┤
           │ Free Memory  │
           └──────────────┘
```

不同区域可以分配给：

```text
Kernel
DMA
Device
Application
Heap
```

---

### ④ MMU 初始化

建立：

```text
虚拟地址 → 物理地址
```

例如：

```text
Virtual Address
       ↓
     MMU
       ↓
Physical Address
       ↓
      DDR
```

同时设置内存属性：

```text
Normal Memory
Device Memory
Cacheable
Non-cacheable
```

---

### ⑤ Cache 初始化

配置：

```text
I-Cache
D-Cache
```

确定不同内存区域是否允许 Cache。

特别需要关注：

```text
CPU Cache
    ↕
   DMA
```

DMA 内存通常需要进行 Cache 一致性处理。

---

## 3. BSP 内存初始化流程

```text
Boot
 ↓
DDR Controller Init
 ↓
DDR PHY Init
 ↓
DDR Training
 ↓
DDR Memory Test
 ↓
建立物理内存布局
 ↓
建立页表
 ↓
配置 MMU / Cache
 ↓
交给 Kernel / RTOS
```

## 4. BSP 与内存管理的关系

BSP主要负责：

> **把硬件内存准备好，并告诉操作系统“有哪些内存、在哪里、怎么访问”。**

而后续的：

```text
物理页分配
虚拟内存分配
Heap
malloc()
Page Fault
```

通常由 Kernel / RTOS 的内存管理模块负责。

## 5. 总结

```text
BSP内存初始化
    │
    ├── DDR初始化
    ├── DDR检测
    ├── 物理内存布局
    ├── MMU / 页表
    └── Cache配置
             ↓
       内存运行环境
             ↓
        Kernel / RTOS
```

> **BSP 内存初始化的核心：初始化 DDR + 建立内存映射 + 配置 MMU/Cache，为操作系统提供可用的内存环境。**