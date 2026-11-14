# USB（Universal Serial Bus）简介

## 1. 什么是USB

USB（Universal Serial Bus，通用串行总线）是一种用于连接计算机与外部设备的高速串行通信总线。

主要特点：

- 即插即用（Plug and Play）
- 热插拔（Hot Plug）
- 自动枚举（Enumeration）
- 统一接口标准
- 支持供电和数据传输

---

## 2. USB系统组成

```text
Host（主机）
    │
USB Hub
    │
Device（设备）
```

### Host

负责总线管理：

- PC
- 手机
- 开发板

### Device

被管理设备：

- U盘
- 键盘
- 鼠标
- 摄像头
- USB网卡

### Hub

USB扩展器。

---

## 3. USB通信模型

USB采用主从模式：

```text
Host
  ↓
Device
```

特点：

- 主机发起通信
- 设备不能主动发送数据
- 所有数据由Host调度

---

## 4. USB传输类型

### Control Transfer（控制传输）

用于：

- 设备枚举
- 配置设备
- 获取描述符

典型命令：

```text
GET_DESCRIPTOR
SET_ADDRESS
SET_CONFIGURATION
```

---

### Bulk Transfer（批量传输）

用于：

- U盘
- 打印机

特点：

- 数据量大
- 保证正确性
- 不保证实时性

---

### Interrupt Transfer（中断传输）

用于：

- 键盘
- 鼠标

特点：

- 小数据量
- 周期性传输
- 响应快

---

### Isochronous Transfer（同步传输）

用于：

- 摄像头
- 麦克风
- 音频设备

特点：

- 实时性高
- 允许少量数据丢失

---

## 5. USB枚举过程

设备插入后：

```text
设备连接
    ↓
检测插入
    ↓
复位设备
    ↓
获取Device Descriptor
    ↓
分配设备地址
    ↓
获取Configuration Descriptor
    ↓
配置设备
    ↓
设备可用
```

---

## 6. USB描述符

### Device Descriptor

描述设备基本信息：

```text
VID
PID
USB版本
设备类别
```

---

### Configuration Descriptor

描述配置参数：

```text
接口数量
供电能力
功耗
```

---

### Interface Descriptor

描述功能接口：

```text
HID
MSC
CDC
UVC
```

---

### Endpoint Descriptor

描述通信端点：

```text
端点号
方向
传输类型
```

---

## 7. Endpoint（端点）

USB通信的基本单位。

```text
EP0
 └── 控制端点

EP1~EP15
 ├── IN
 └── OUT
```

方向：

```text
IN
设备 → 主机

OUT
主机 → 设备
```

---

## 8. USB设备类型

### HID

Human Interface Device

```text
键盘
鼠标
游戏手柄
```

---

### MSC

Mass Storage Class

```text
U盘
移动硬盘
```

---

### CDC

Communication Device Class

```text
USB转串口
4G模块
调试串口
```

---

### UVC

USB Video Class

```text
USB摄像头
```

---

### Audio

```text
USB耳机
USB麦克风
```

---

## 9. USB版本

| 版本 | 速率 |
|--------|--------|
| USB1.1 | 12 Mbps |
| USB2.0 | 480 Mbps |
| USB3.0 | 5 Gbps |
| USB3.1 | 10 Gbps |
| USB3.2 | 20 Gbps |
| USB4 | 40~80 Gbps |

---

## 10. USB软件架构

```text
Application
      ↓
USB Class Driver
      ↓
USB Core
      ↓
USB Controller Driver
      ↓
USB PHY
      ↓
USB Device
```

---

## 11. 常见USB控制器

| 控制器 | 用途 |
|----------|----------|
| OHCI | USB1.1 |
| UHCI | USB1.1 |
| EHCI | USB2.0 |
| XHCI | USB3.x |
| DWC2 | 嵌入式USB2.0 |
| DWC3 | 嵌入式USB3.0 |

---

## 12. USB核心特点总结

```text
总线类型：
    串行总线

通信模式：
    Host-Device

支持：
    即插即用
    热插拔

传输方式：
    Control
    Bulk
    Interrupt
    Isochronous

典型设备：
    U盘
    键盘
    鼠标
    摄像头
    USB串口
```