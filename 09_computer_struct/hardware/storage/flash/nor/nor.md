# NOR Flash 简介

## 1. 什么是 NOR Flash

NOR Flash（Not OR Flash）是一种**非易失性存储器（Non-Volatile Memory）**，断电后数据不会丢失。

其内部采用并联连接结构，支持像内存一样随机访问，因此可以直接执行代码（XIP，eXecute In Place）。

主要特点：

* 随机读取速度快
* 支持代码直接运行（XIP）
* 容量较小
* 成本较高
* 擦写速度较慢

典型应用：

* BootLoader
* BIOS/UEFI
* MCU固件
* 嵌入式系统程序存储
* FPGA配置文件

---

## 2. NOR Flash 存储结构

```text
Device
 └── Sector
      └── Page
           └── Cell
```

典型容量：

| 项目     | 大小        |
| ------ | --------- |
| Page   | 256B~512B |
| Sector | 4KB~64KB  |
| Chip   | MB~GB级    |

NOR Flash 的地址空间连续映射：

```text
CPU Address
     ↓
NOR Flash
     ↓
直接读取指令
```

因此 CPU 可以直接从 Flash 取指执行。

---

## 3. NOR Flash 基本操作

### 读取(Read)

```text
CPU
 ↓
Address
 ↓
NOR Flash
 ↓
Data
```

特点：

* 支持字节随机访问
* 读取速度快
* 可直接执行代码(XIP)

---

### 写入(Program)

```text
Host
 ↓
Page Program
 ↓
NOR Flash
```

特点：

* 只能将 1 写成 0
* 不能直接将 0 改成 1

---

### 擦除(Erase)

```text
Sector Erase
```

或：

```text
Block Erase
```

擦除后：

```text
11111111
```

全部恢复为 1。

---

## 4. NOR Flash 典型存储布局

```text
+----------------+
| BootLoader     |
+----------------+
| Kernel         |
+----------------+
| RootFS         |
+----------------+
| Config         |
+----------------+
```

嵌入式系统常见启动流程：

```text
Power On
   ↓
CPU
   ↓
NOR Flash
   ↓
BootLoader
   ↓
Kernel
```

CPU 上电后即可直接执行 NOR 中的代码。

---

## 5. XIP（Execute In Place）

NOR Flash 最大优势：

```text
Code
 ↓
NOR Flash
 ↓
CPU直接执行
```

无需：

```text
Flash
 ↓
RAM
 ↓
CPU
```

优点：

* 节省RAM
* 启动速度快
* 软件架构简单

因此广泛用于：

* MCU
* RTOS
* BootROM
* BSP

---

## 6. NOR Flash 常见接口

### Parallel NOR

```text
CPU
 ↓
地址总线
数据总线
 ↓
NOR
```

特点：

* 速度快
* 引脚多

---

### SPI NOR

```text
CPU
 ↓
SPI
 ↓
NOR
```

特点：

* 引脚少
* 成本低
* 应用最广

---

### QSPI NOR

```text
CPU
 ↓
QSPI
 ↓
NOR
```

特点：

* 4线并行传输
* 支持XIP
* 速度更高

---

## 7. NOR Flash 常见命令

| 命令           | 功能      |
| ------------ | ------- |
| Read ID      | 读取芯片ID  |
| Read Data    | 读取数据    |
| Page Program | 页写入     |
| Sector Erase | 扇区擦除    |
| Block Erase  | 块擦除     |
| Chip Erase   | 整片擦除    |
| Read Status  | 读取状态寄存器 |
| Write Enable | 写使能     |

典型操作流程：

```text
Write Enable
      ↓
Program/Erase
      ↓
Busy
      ↓
Ready
```

---

## 8. NOR Flash 与 NAND Flash 对比

| 项目    | NOR Flash | NAND Flash |
| ----- | --------- | ---------- |
| 随机读取  | 快         | 慢          |
| 顺序读写  | 一般        | 快          |
| 擦除速度  | 慢         | 快          |
| 容量    | 小         | 大          |
| 成本    | 高         | 低          |
| XIP执行 | 支持        | 不支持        |
| 坏块管理  | 基本无需      | 必须         |
| 应用    | 存代码       | 存数据        |

通常：

```text
NOR
 ↓
BootLoader
固件
配置

NAND
 ↓
文件系统
用户数据
大容量存储
```

---

## 9. NOR Flash 在嵌入式系统中的位置

```text
                +--------+
                |  CPU   |
                +--------+
                    |
         +----------+----------+
         |                     |
         v                     v
   NOR Flash             DDR RAM
(程序存储)              (运行空间)
```

启动时：

```text
NOR Flash
     ↓
BootLoader
     ↓
Kernel
     ↓
Application
```

因此 NOR Flash 经常被称为：

```text
代码存储器(Code Storage)
```

---

## 10. 一句话总结

**NOR Flash 是一种支持随机访问和 XIP（直接执行代码）的非易失性存储器，具有读取速度快、可靠性高的特点，主要用于 BootLoader、固件和嵌入式系统程序存储。**
