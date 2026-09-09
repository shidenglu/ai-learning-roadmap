# BootLoader 简介

## 1. 什么是 BootLoader

BootLoader（Boot Loader）是系统启动过程中负责**加载和启动操作系统**的一段软件。

它通常由芯片厂商、板卡厂商或用户开发，可以根据具体硬件平台进行修改。

```text
Power On
   │
   ▼
BootROM
   │
   ▼
BootLoader
   │
   ▼
Kernel / RTOS
   │
   ▼
Application
```

---

## 2. BootLoader 的主要作用

### ① 初始化硬件

完成操作系统运行所需要的基础硬件初始化：

```text
CPU
DDR
Clock
UART
GIC
Timer
MMU
```

例如：

```c
cpu_init();
clock_init();
ddr_init();
uart_init();
```

---

### ② 加载操作系统

从存储设备读取OS镜像：

```text
eMMC / SD / Flash
        │
        ▼
       DDR
        │
        ▼
 Kernel / RTOS
```

例如：

```text
bootloader
    │
    ├──读取 Kernel
    ├──读取 Device Tree
    └──加载到 DDR
```

---

### ③ 校验镜像

启动前可以检查：

```text
CRC
Hash
Signature
```

用于保证镜像完整性和安全性。

---

### ④ 设置启动参数

向Kernel传递：

```text
内存大小
设备信息
启动参数
Device Tree
命令行参数
```

---

### ⑤ 跳转到操作系统

完成准备后：

```c
jump_to_kernel();
```

CPU开始执行Kernel。

---

## 3. BootLoader 的典型结构

```text
BootLoader
│
├── Startup
│   └── CPU初始化
│
├── Hardware Init
│   ├── DDR
│   ├── Clock
│   ├── UART
│   └── GIC
│
├── Storage
│   ├── eMMC
│   ├── SD
│   └── Flash
│
├── Image Loader
│   └── 加载Kernel
│
├── Security
│   └── 镜像校验
│
└── Kernel Jump
    └── 跳转Kernel
```

---

## 4. 常见 BootLoader

### U-Boot

嵌入式Linux中非常常见：

```text
BootROM
   ↓
U-Boot
   ↓
Linux Kernel
```

### 其他

```text
Barebox
GRUB
Windows Boot Manager
自研BootLoader
```

---

## 5. BootROM 与 BootLoader

| 项目 | BootROM | BootLoader |
|---|---|---|
| 位置 | SoC内部 | Flash/eMMC等 |
| 是否可修改 | 通常不可 | 可以 |
| 开发者 | 芯片厂商 | 板卡/OS厂商 |
| 主要作用 | 加载BootLoader | 加载OS |
| 启动阶段 | 第一阶段 | 后续阶段 |

---

## 6. BootLoader 与 BSP 的关系

两者容易混淆：

```text
BootLoader
    │
    ├── CPU初始化
    ├── DDR初始化
    ├── Clock初始化
    └── UART初始化
             │
             ▼
           BSP
             │
             ▼
           RTOS
```

BootLoader负责**把系统启动起来并加载OS**。

BSP负责**让OS适配具体硬件平台**。

实际工程中两者可能存在代码复用，例如BootLoader和BSP可能共同使用UART、GIC、Timer、DDR等底层代码。

---

## 7. 完整启动链路

```text
┌──────────────┐
│   Power On   │
└──────┬───────┘
       ↓
┌──────────────┐
│   BootROM    │
│  选择启动设备 │
└──────┬───────┘
       ↓
┌──────────────┐
│  BootLoader  │
│ 初始化硬件    │
│ 加载OS镜像    │
└──────┬───────┘
       ↓
┌──────────────┐
│  Kernel/RTOS │
│    BSP       │
└──────┬───────┘
       ↓
┌──────────────┐
│ Application  │
└──────────────┘
```

## 8. 一句话总结

> **BootLoader就是系统启动阶段的“加载器”，负责初始化必要硬件、加载并校验操作系统镜像，最后把CPU控制权交给Kernel或RTOS。**