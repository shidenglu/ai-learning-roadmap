# USB协议栈（USB Stack）简介

## 1. 什么是USB协议栈

USB协议栈（USB Stack）是实现USB通信协议的软件系统，负责完成：

- USB设备发现
- 设备枚举
- 数据传输
- 设备管理
- Class驱动管理

本质上：

```text
USB协议栈 = USB协议实现软件
```

---

## 2. USB协议栈分层

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
USB Bus
```

---

## 3. Application层

用户应用程序。

例如：

```text
文件系统
USB摄像头应用
USB串口终端
键盘输入程序
```

通过USB驱动访问设备。

---

## 4. Class Driver层

实现具体设备协议。

常见Class：

| Class | 设备 |
|---------|---------|
| HID | 键盘、鼠标 |
| MSC | U盘、移动硬盘 |
| CDC | USB转串口 |
| UVC | 摄像头 |
| Audio | 麦克风、耳机 |

例如：

```text
USB Mouse
    ↓
HID Driver
```

---

## 5. USB Core层

USB协议栈核心。

主要功能：

- 设备枚举
- 描述符解析
- 地址管理
- Endpoint管理
- Transfer管理

核心流程：

```text
设备插入
    ↓
枚举
    ↓
获取Descriptor
    ↓
分配地址
    ↓
配置设备
    ↓
加载Class驱动
```

---

## 6. Controller Driver层

USB控制器驱动。

负责：

- 操作USB控制器寄存器
- DMA管理
- Endpoint配置
- 中断处理

常见控制器：

```text
EHCI
XHCI
DWC2
DWC3
```

---

## 7. PHY层

USB物理层。

负责：

- USB信号发送
- USB信号接收
- 电气特性控制

例如：

```text
USB2.0 PHY
USB3.0 PHY
Type-C PHY
```

---

## 8. USB Host协议栈

主机模式：

```text
PC
开发板
手机OTG
```

结构：

```text
Application
      ↓
Class Driver
      ↓
USB Host Core
      ↓
Host Controller
      ↓
USB Device
```

负责管理所有USB设备。

---

## 9. USB Device协议栈

设备模式：

```text
U盘
USB网卡
USB串口
摄像头
```

结构：

```text
USB Device
      ↓
USB Device Core
      ↓
USB Controller
      ↓
USB Host
```

负责响应Host请求。

---

## 10. USB枚举过程

设备插入：

```text
Device Connect
      ↓
Bus Reset
      ↓
Get Device Descriptor
      ↓
Set Address
      ↓
Get Configuration Descriptor
      ↓
Set Configuration
      ↓
Load Class Driver
      ↓
Ready
```

---

## 11. 数据传输流程

```text
Application
      ↓
Class Driver
      ↓
USB Core
      ↓
Endpoint
      ↓
USB Controller
      ↓
USB Bus
```

---

## 12. USB协议栈目录结构示例

```text
usb/
├── core/
│   ├── usb_core.c
│   ├── usb_enum.c
│   └── usb_transfer.c
│
├── host/
│   └── usb_host.c
│
├── device/
│   └── usb_device.c
│
├── class/
│   ├── hid.c
│   ├── msc.c
│   ├── cdc.c
│   └── uvc.c
│
├── controller/
│   ├── ehci.c
│   ├── xhci.c
│   ├── dwc2.c
│   └── dwc3.c
│
└── phy/
    └── usb_phy.c
```

---

## 13. 总结

USB协议栈本质是一套实现USB协议的软件框架。

核心组成：

```text
Application
    ↓
Class Driver
    ↓
USB Core
    ↓
Controller Driver
    ↓
PHY
```

核心功能：

- 设备枚举
- 描述符解析
- Endpoint管理
- 数据传输
- Class驱动管理

常见设备：

```text
键盘(HID)
鼠标(HID)
U盘(MSC)
USB串口(CDC)
摄像头(UVC)
音频设备(Audio)
```