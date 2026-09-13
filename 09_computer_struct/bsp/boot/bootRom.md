# BootROM 简介

## 1. 什么是 BootROM

BootROM（Boot Read Only Memory）是芯片内部固化的一段启动代码。

当设备上电或复位后，CPU首先执行的就是BootROM中的代码。

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
Kernel/RTOS
```

---

## 2. BootROM 的作用

BootROM主要负责：

### ① CPU基础初始化

- 设置CPU运行模式
- 初始化栈指针
- 关闭或配置中断

### ② 查找启动设备

根据启动配置选择启动介质：

```text
SPI Flash
NAND Flash
NOR Flash
eMMC
SD Card
USB
Network
```

### ③ 加载BootLoader

将BootLoader从外部存储设备加载到RAM中：

```text
Flash
  │
  ▼
RAM
```

然后跳转执行：

```c
jump_to_bootloader();
```

---

## 3. BootROM 的位置

BootROM位于SoC内部：

```text
┌─────────────────┐
│      SoC        │
│                 │
│  CPU Core       │
│  BootROM        │
│  SRAM           │
└─────────────────┘
```

属于芯片的一部分。

---

## 4. BootROM 特点

### 固化在芯片内部

出厂时由芯片厂商烧录。

### 不可修改

用户无法重新编译或升级。

### 容量较小

一般：

```text
16KB ~ 512KB
```

### 最先执行

是系统启动链路中的第一阶段软件。

---

## 5. BootROM 启动流程

```text
CPU Reset
   │
   ▼
BootROM
   │
   ├──读取启动配置
   ├──选择启动设备
   ├──加载BootLoader
   └──校验镜像
   │
   ▼
BootLoader
```

---

## 6. BootROM 与 BootLoader 的区别

| 项目 | BootROM | BootLoader |
|--------|----------|------------|
| 存储位置 | SoC内部ROM | Flash/eMMC |
| 是否可修改 | 否 | 是 |
| 开发者 | 芯片厂商 | 用户/厂商 |
| 作用 | 加载BootLoader | 加载OS |
| 执行顺序 | 第一阶段 | 第二阶段 |

---

## 7. 常见处理器中的 BootROM

- STM32
- RK3588
- i.MX8
- TI AM系列
- 高通 Snapdragon
- 海思 Kirin
- Apple M系列

所有现代SoC几乎都内置BootROM。

---

## 8. 一句话总结

> BootROM是芯片内部固化的第一阶段启动程序，负责在系统上电后查找启动设备并加载BootLoader，是整个系统启动链路的起点。