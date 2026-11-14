# BSP 中的 MMU 初始化

## 1. 作用

BSP 中的 MMU 初始化主要负责建立系统启动阶段所需的**基础地址映射**，让 CPU 能够正确访问 DDR 和外设寄存器。

```text
CPU
 ↓
MMU
 ↓
VA → PA
 ↓
DDR / Device
```

## 2. BSP 主要做的事情

```text
① 创建基础页表
② 建立 VA → PA 映射
③ 配置内存属性
④ 配置访问权限
⑤ 设置页表基地址
⑥ 开启 MMU
```

### 建立地址映射

例如：

```text
Virtual Address       Physical Address
0xFFFF000000000000 → 0x80000000   DDR
0xFFFF000010000000 → 0x40000000   UART
```

### 配置内存属性

```text
DDR
→ Normal Memory
→ Cacheable

UART / GIC
→ Device Memory
→ Non-cacheable
```

### 设置页表

ARM64 中主要配置：

```text
TTBR0_EL1
TTBR1_EL1
TCR_EL1
MAIR_EL1
```

分别用于指定页表、地址空间和内存属性等信息。

### 开启 MMU

完成页表及相关寄存器配置后：

```text
MMU OFF
   ↓
建立基础映射
   ↓
配置 MMU
   ↓
MMU ON
```

之后 CPU 的内存访问经过：

```text
VA → MMU → PA
```

## 3. BSP MMU 初始化流程

```text
MMU Init
   ↓
创建页表
   ↓
建立基础 VA → PA 映射
   ↓
配置 Memory Attribute
   ↓
配置访问权限
   ↓
设置 TTBR / TCR / MAIR
   ↓
开启 MMU
```

## 4. BSP 与 Kernel 的边界

BSP 只负责：

> **建立系统启动所需的基础 MMU 环境。**

后续完整的：

```text
虚拟内存管理
页分配
进程地址空间
Page Fault
```

通常由 Kernel / RTOS 的内存管理模块负责。

## 5. 总结

> **BSP 中的 MMU 初始化 = 建立基础页表和地址映射 + 配置内存属性 + 开启 MMU，为后续 OS 运行提供基本的虚拟地址环境。**