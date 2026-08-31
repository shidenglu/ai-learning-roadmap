# UART 总线

## 1. 什么是 UART

UART（Universal Asynchronous Receiver/Transmitter）是一种**异步、串行、全双工**通信接口。

常用于：

```text
MCU ↔ PC
MCU ↔ GPS
MCU ↔ 蓝牙模块
MCU ↔ WiFi模块
MCU ↔ 调试串口
```

---

## 2. UART 基本结构

最典型的 UART 是点对点通信：

```text
      Device A              Device B
     ┌────────┐            ┌────────┐
     │  UART  │            │  UART  │
     └───┬────┘            └───┬────┘
         │                     │
        TX ──────────────────► RX
        RX ◄────────────────── TX
        GND ───────────────── GND
```

主要信号：

```text
TX   → 发送数据
RX   → 接收数据
GND  → 参考地
```

---

## 3. UART 为什么不需要时钟线

UART 是**异步通信**。

发送端和接收端提前约定：

```text
Baud Rate
Data Bits
Parity
Stop Bits
```

例如：

```text
115200
8 Data Bits
No Parity
1 Stop Bit
```

因此不需要单独的：

```text
CLK
```

---

## 4. UART 数据帧

UART 一帧典型结构：

```text
      Start     Data       Parity    Stop
        │         │           │        │
        ▼         ▼           ▼        ▼
       ┌──┬────────────────┬──────┬────┐
       │0 │  8 Data Bits   │  P   │ 1  │
       └──┴────────────────┴──────┴────┘
```

典型配置：

```text
8N1
```

表示：

```text
8 → 8个数据位
N → No Parity，无校验
1 → 1个停止位
```

---

## 5. UART 空闲状态

UART 总线空闲时通常为：

```text
TX = HIGH
```

发送数据时：

```text
IDLE
  │
  ▼
START BIT = 0
  │
  ▼
DATA
  │
  ▼
PARITY（可选）
  │
  ▼
STOP BIT = 1
  │
  ▼
IDLE
```

---

## 6. UART 数据传输

例如发送：

```text
0x55
```

二进制：

```text
01010101
```

一帧：

```text
Start
  ↓
01010101
  ↓
Stop
```

UART 通常按照：

```text
LSB → MSB
```

顺序发送数据位。

---

## 7. 波特率

Baud Rate 表示通信符号速率。

常见配置：

```text
9600
19200
38400
57600
115200
921600
```

例如：

```text
115200 baud
```

表示每秒大约传输：

```text
115200 个符号
```

对于普通 UART 二进制传输，通常可近似理解为：

```text
115200 bit/s
```

但实际有效数据吞吐量还要考虑：

```text
Start Bit
Data Bit
Parity
Stop Bit
```

---

## 8. UART 全双工

UART 可以同时发送和接收：

```text
Device A                    Device B

TX ───────────────────────► RX
RX ◄─────────────────────── TX

       同时发送和接收
```

因此 UART 是：

> **全双工通信。**

---

## 9. UART 常见配置

| 参数        | 常见值    |
| --------- | ------ |
| Baud Rate | 115200 |
| Data Bits | 8      |
| Parity    | None   |
| Stop Bits | 1      |
| 流控        | None   |

最常见配置：

```text
115200 8N1
```

---

## 10. UART 硬件流控

UART 可以使用额外信号实现流控：

```text
RTS
CTS
```

例如：

```text
Device A                  Device B

TX ─────────────────────► RX
RX ◄───────────────────── TX

RTS ────────────────────► CTS
CTS ◄───────────────────── RTS
```

作用：

```text
控制发送速度
防止接收端来不及处理数据
```

---

## 11. UART 与 RS-232 / RS-485 的关系

UART 是一种：

> **串行数据收发接口/控制器。**

RS-232、RS-485 是不同的：

> **物理层电气标准。**

可以理解为：

```text
UART
 │
 ▼
数据格式 / 收发控制
 │
 ▼
物理层收发器
 │
 ├── RS-232
 ├── RS-485
 └── TTL/CMOS UART
```

所以：

```text
UART ≠ RS-232
UART ≠ RS-485
```

---

## 12. UART 与 I2C、SPI、CAN 对比

| 项目   | UART   | I2C        | SPI               | CAN        |
| ---- | ------ | ---------- | ----------------- | ---------- |
| 同步方式 | 异步     | 同步         | 同步                | 同步         |
| 全双工  | 是      | 否          | 是                 | 否          |
| 典型信号 | TX/RX  | SDA/SCL    | MOSI/MISO/SCLK/CS | CANH/CANL  |
| 多设备  | 通常点对点  | 支持         | 支持                | 支持         |
| 地址   | 无      | 有          | CS                | Message ID |
| 抗干扰  | 一般     | 一般         | 一般                | 强          |
| 典型应用 | 调试/GPS | Sensor/RTC | Flash/LCD         | 汽车/工业      |

---

## 13. UART 驱动层次

```text
Application
     │
     ▼
UART Driver
     │
     ▼
UART Controller
     │
     ▼
UART Transceiver / GPIO
     │
     ▼
TX / RX
```

发送数据：

```c
uart_write("hello");
```

底层通常：

```text
检查 TX FIFO
      ↓
写 UART TX Register
      ↓
UART Controller
      ↓
TX Pin
```

接收：

```text
RX Pin
  ↓
UART Controller
  ↓
RX FIFO
  ↓
UART Driver
  ↓
Application
```

---

## 14. UART 常见工作方式

### 轮询

```text
CPU
 │
 └── 一直检查 UART 状态
          ↓
       RX/TX Ready
```

### 中断

```text
UART
 │
 └── IRQ
      ↓
     CPU
      ↓
 UART ISR
```

### DMA

```text
UART
 │
 ▼
DMA
 │
 ▼
Memory
```

适合大量数据传输。

---

## 15. UART 核心知识点

```text
TX / RX
   ↓
异步通信
   ↓
Baud Rate
   ↓
Start Bit
   ↓
Data Bits
   ↓
Parity
   ↓
Stop Bit
   ↓
FIFO
   ↓
Polling / Interrupt / DMA
```

一句话总结：

> **UART 是一种不需要独立时钟线，通过双方约定波特率和数据帧格式进行串行、异步、全双工通信的接口，最常用于调试、模块通信和设备间数据传输。**
