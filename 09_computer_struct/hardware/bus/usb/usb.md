# USB（Universal Serial Bus）通用串行总线

## 1. 什么是 USB

USB（Universal Serial Bus）即：

```text
通用串行总线
```

是一种用于连接计算机与外部设备的高速通信总线。

常见设备：

```text
U盘
鼠标
键盘
摄像头
打印机
手机
开发板
```

---

# 2. USB 基本结构

```text
        Host
         │
         ▼
      USB Bus
         │
 ┌───────┼───────┐
 ▼       ▼       ▼
U盘    鼠标    键盘
```

USB 采用：

```text
主机（Host）
    ↓
设备（Device）
```

模式通信。

---

# 3. USB 信号线

USB 2.0 主要包含：

| 信号   | 作用 |
| ---- | -- |
| VBUS | 电源 |
| GND  | 地  |
| D+   | 数据 |
| D-   | 数据 |

```text
VBUS
GND
D+
D-
```

---

# 4. USB 通信模式

USB 由 Host 发起通信：

```text
PC
 │
 ▼
USB Host
 │
 ▼
USB Device
```

例如：

```text
PC
 │
 ▼
读取U盘数据
```

设备不能主动发送数据。

---

# 5. USB 枚举（Enumeration）

设备插入后：

```text
插入设备
    ↓
识别设备
    ↓
分配地址
    ↓
读取描述符
    ↓
加载驱动
    ↓
开始通信
```

这个过程称为：

```text
USB Enumeration
```

---

# 6. USB 传输类型

| 类型          | 用途     |
| ----------- | ------ |
| Control     | 设备管理   |
| Bulk        | U盘、打印机 |
| Interrupt   | 鼠标、键盘  |
| Isochronous | 音频、视频  |

例如：

```text
鼠标 → Interrupt

U盘 → Bulk

摄像头 → Isochronous
```

---

# 7. USB 速度

| 标准      | 理论速率     |
| ------- | -------- |
| USB 1.1 | 12 Mbps  |
| USB 2.0 | 480 Mbps |
| USB 3.0 | 5 Gbps   |
| USB 3.1 | 10 Gbps  |
| USB 3.2 | 20 Gbps  |
| USB4    | 40+ Gbps |

---

# 8. USB 设备分类

常见 USB Class：

| Class   | 设备    |
| ------- | ----- |
| HID     | 鼠标、键盘 |
| MSC     | U盘    |
| CDC     | 虚拟串口  |
| Audio   | 声卡    |
| Video   | 摄像头   |
| Printer | 打印机   |

---

# 9. USB 驱动层次

```text
Application
      │
      ▼
USB Class Driver
      │
      ▼
USB Core
      │
      ▼
USB Controller
      │
      ▼
USB Device
```

---

# 10. USB OTG

OTG（On-The-Go）允许设备动态切换角色：

```text
手机 ←→ U盘
```

可以作为：

```text
Host

或者

Device
```

工作。

---

# 11. USB 在嵌入式中的应用

```text
MCU
 │
 ├── USB Device
 │      └── 虚拟串口(CDC)
 │
 ├── USB MSC
 │      └── U盘功能
 │
 └── USB HID
        └── 键盘/鼠标
```

常见开发板调试串口：

```text
PC
 │
 ▼
USB CDC
 │
 ▼
UART
```

---

# 12. USB 与 UART 对比

| 项目   | USB  | UART  |
| ---- | ---- | ----- |
| 通信方式 | 主从   | 点对点   |
| 速度   | 高    | 较低    |
| 热插拔  | 支持   | 不支持   |
| 设备识别 | 自动枚举 | 无     |
| 多设备  | 支持   | 通常不支持 |
| 驱动模型 | 复杂   | 简单    |

---

# 13. 核心知识点

```text
USB
 │
 ├── Host
 ├── Device
 ├── Enumeration
 ├── Endpoint
 ├── HID
 ├── CDC
 ├── MSC
 ├── USB2.0
 ├── USB3.0
 └── OTG
```

---

# 14. 总结

USB 是现代计算机最常用的外设通信总线之一。

核心通信链路：

```text
Host
  │
  ▼
USB Controller
  │
  ▼
USB Bus
  │
  ▼
Device
```

核心特点：

```text
高速
热插拔
自动识别
统一接口
支持供电
```

一句话总结：

> **USB 是一种主从式高速串行总线，通过枚举机制自动识别设备，广泛应用于计算机、手机和嵌入式设备之间的数据通信与供电。**
