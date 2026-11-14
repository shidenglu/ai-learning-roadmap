# CPU 初始化

## 1. 概述

CPU 初始化是系统上电或复位后，对 CPU 运行环境进行基础配置，使其能够执行后续的 BootLoader、BSP、Kernel 等代码。

```text
CPU Reset
   ↓
CPU 初始化
   ↓
BootLoader / BSP
   ↓
Kernel / RTOS
```

## 2. 主要过程

```text
┌──────────────────┐
│   CPU Reset      │
├──────────────────┤
│ 设置运行级别     │
│ 设置 Stack       │
│ 设置异常向量     │
│ 配置CPU寄存器    │
│ 配置 Cache/MMU   │
│ 配置中断         │
│ 多核初始化       │
├──────────────────┤
│   进入 C 代码    │
└──────────────────┘
```

### ① 设置运行环境

确定 CPU 的运行级别和执行状态。

ARM64 常见：

```text
EL0 → 用户态
EL1 → Kernel
EL2 → Hypervisor
EL3 → Secure Monitor
```

### ② 设置 Stack

设置栈指针 `SP`，建立 C 语言运行所需的栈环境。

```asm
ldr x0, =stack_top
mov sp, x0
```

### ③ 设置异常向量

设置异常向量基地址，例如：

```asm
msr VBAR_EL1, x0
```

用于处理：

```text
IRQ / FIQ
同步异常
SError
```

### ④ 配置 CPU 寄存器

根据系统需求配置：

```text
PSTATE
SCTLR
DAIF
TPIDR
```

等系统寄存器。

### ⑤ 配置 Cache / MMU

根据启动阶段需求配置：

```text
Cache
MMU
TLB
页表
```

### ⑥ 初始化中断

配置 CPU 与 GIC 的关系，为后续中断处理做准备。

### ⑦ 多核初始化

SMP 系统中通常先启动主 CPU：

```text
CPU0 → 启动
CPU1 → 等待
CPU2 → 等待
CPU3 → 等待
```

其他 CPU 后续由 Kernel/RTOS 启动。

## 3. 最终结果

CPU 完成初始化后：

```text
CPU
 ↓
有栈
 ↓
有异常处理机制
 ↓
具备基本内存访问能力
 ↓
具备中断处理能力
 ↓
进入 C 代码
```

## 4. 总结

> **CPU 初始化就是把刚复位的 CPU 配置成一个能够正常执行代码、访问内存、处理异常和中断的基本运行环境。**