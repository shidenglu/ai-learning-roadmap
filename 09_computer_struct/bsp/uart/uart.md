# 串口（UART）详解

# 1. 什么是串口

串口（Serial Port）是一种**串行通信接口**，用于设备之间的数据传输。

所谓串行通信，就是：

```text
一次只传输 1 bit 数据
```

例如发送字符：

```text
'A'
```

ASCII码：

```text
01000001
```

串口会按照顺序逐位发送：

```text
0 → 1 → 0 → 0 → 0 → 0 → 0 → 1
```

---

# 2. 为什么需要串口

计算机中的设备需要互相通信：

```text
PC
MCU
传感器
GPS模块
4G模块
蓝牙模块
```

例如：

```text
STM32 ←→ GPS
STM32 ←→ WiFi模块
PC ←→ 单片机
```

这些设备之间的数据交换通常通过串口完成。

---

# 3. 串口通信特点

优点：

```text
硬件简单
成本低
实现容易
传输距离较远
```

缺点：

```text
速度较低
抗干扰能力一般
```

---

# 4. 串行通信与并行通信

## 串行通信

```text
发送端                    接收端

TX -------------------- RX
```

一次发送：

```text
1 bit
```

---

## 并行通信

```text
D0 ---------------- D0
D1 ---------------- D1
D2 ---------------- D2
...
D7 ---------------- D7
```

一次发送：

```text
8 bit
```

即：

```text
1 Byte
```

---

对比：

| 项目   | 串行通信 | 并行通信 |
| ---- | ---- | ---- |
| 线路数量 | 少    | 多    |
| 成本   | 低    | 高    |
| 距离   | 远    | 近    |
| 抗干扰  | 较好   | 较差   |
| 速度   | 较低   | 较高   |

---

# 5. UART简介

最常见的串口标准：

```text
UART
```

全称：

```text
Universal Asynchronous Receiver Transmitter
通用异步收发器
```

几乎所有MCU都支持UART：

```text
STM32
NXP
ESP32
RK3588
ARM SoC
```

---

# 6. UART引脚

最基本的UART只需要两根信号线：

```text
TX
RX
```

连接方式：

```text
设备A                设备B

TX ---------------- RX

RX ---------------- TX
```

注意：

```text
TX 接 RX
RX 接 TX
```

需要交叉连接。

---

# 7. UART数据帧格式

发送一个字符时：

```text
起始位
数据位
停止位
```

例如：

```text
发送字符'A'
```

ASCII：

```text
01000001
```

数据帧：

```text
空闲
 ↓
起始位(0)
 ↓
01000001
 ↓
停止位(1)
```

表示：

```text
|Start| Data |Stop|
```

---

# 8. 波特率

波特率（Baud Rate）：

```text
每秒传输多少个符号
```

UART中通常：

```text
1符号 = 1bit
```

所以：

```text
9600 Baud
```

表示：

```text
9600 bit/s
```

---

常见波特率：

```text
9600
19200
38400
57600
115200
921600
```

最常见：

```text
115200
```

---

# 9. UART参数配置

常见配置：

```text
115200 8N1
```

含义：

### 115200

```text
波特率
```

---

### 8

```text
8位数据位
```

---

### N

```text
No Parity
无校验位
```

---

### 1

```text
1位停止位
```

---

即：

```text
115200 8N1
```

---

# 10. 校验位

用于检测传输错误。

## 奇校验

```text
Odd Parity
```

保证：

```text
1的个数为奇数
```

---

## 偶校验

```text
Even Parity
```

保证：

```text
1的个数为偶数
```

---

例如：

```text
10110001
```

共有：

```text
4个1
```

偶校验：

```text
校验位 = 0
```

---

# 11. UART发送流程

发送字符：

```c
printf("A");
```

流程：

```text
CPU
 ↓
UART TX寄存器
 ↓
UART发送器
 ↓
TX引脚
 ↓
RX引脚
 ↓
UART接收器
 ↓
UART RX寄存器
 ↓
CPU
```

---

# 12. UART硬件结构

UART内部通常包含：

```text
UART
│
├── TX Buffer
├── RX Buffer
├── Baud Generator
├── Control Register
└── Status Register
```

---

# 13. UART寄存器

常见寄存器：

### DR

Data Register

```text
发送和接收数据
```

---

### SR

Status Register

```text
状态寄存器
```

例如：

```text
TX完成
RX完成
错误标志
```

---

### CR

Control Register

```text
使能UART
配置波特率
配置中断
```

---

# 14. UART中断

CPU轮询：

```text
while(1)
{
    检查是否收到数据
}
```

效率低。

---

使用中断：

```text
收到数据
 ↓
UART产生中断
 ↓
CPU进入ISR
 ↓
读取数据
```

---

优点：

```text
CPU利用率高
实时性好
```

---

# 15. UART + DMA

高速通信时：

```text
UART
 ↓
DMA
 ↓
RAM
```

无需CPU逐字节搬运。

---

例如：

```text
串口接收1MB数据
```

CPU方式：

```text
接收一次
处理中断一次
```

非常耗费资源。

---

DMA方式：

```text
DMA自动搬运
```

CPU只处理结果。

---

# 16. RS232与TTL串口

很多初学者容易混淆。

---

## TTL串口

MCU常用：

```text
0V
3.3V
```

或：

```text
0V
5V
```

---

## RS232

PC传统串口：

```text
+12V
-12V
```

---

区别：

```text
TTL不能直接连接RS232
```

需要：

```text
MAX232
```

进行电平转换。

---

# 17. UART与USB区别

UART：

```text
简单
成本低
```

---

USB：

```text
速度快
协议复杂
```

---

对比：

| 项目   | UART | USB |
| ---- | ---- | --- |
| 线路   | 少    | 多   |
| 实现难度 | 低    | 高   |
| 速度   | 较低   | 高   |
| 成本   | 低    | 高   |

---

# 18. 嵌入式开发中的应用

最常见用途：

```text
调试日志输出
```

例如：

```c
printf("hello");
```

通过UART输出到串口终端。

---

常见场景：

```text
Bootloader调试
Linux控制台
GPS模块
4G模块
蓝牙模块
工业设备
传感器
```

---

# 19. Linux中的串口

设备文件：

```text
/dev/ttyS0
/dev/ttyS1
/dev/ttyUSB0
/dev/ttyUSB1
```

查看：

```bash
ls /dev/tty*
```

---

使用串口工具：

```bash
minicom
screen
picocom
```

---

# 20. 总结

## UART特点

```text
简单
可靠
成本低
应用广泛
```

---

## 核心参数

```text
波特率
数据位
校验位
停止位
```

最常见配置：

```text
115200 8N1
```

---

## 典型连接

```text
TX → RX
RX → TX
GND → GND
```

---

## 高级应用

```text
UART中断
UART DMA
RS232
Linux串口驱动
```

---

一句话总结：

```text
串口（UART）是一种利用TX/RX两根信号线进行异步串行通信的接口，是嵌入式系统中最常用、最基础的通信方式之一。
```
