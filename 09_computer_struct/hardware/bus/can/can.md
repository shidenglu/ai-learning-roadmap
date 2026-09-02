# CAN 总线

## 1. 什么是 CAN

CAN（Controller Area Network）是一种**多主机、广播式、差分通信**总线，主要用于汽车和工业控制系统中的设备通信。

典型通信对象：

```text
        CAN Bus
══════════════════════════════════
    │          │          │
    ▼          ▼          ▼
  ECU        ABS        仪表
    │          │          │
 发动机      制动系统    Dashboard
```

CAN 的核心特点：

> **多个节点共享一条总线，通过消息 ID 区分数据，而不是通过设备地址通信。**

---

# 2. CAN 的基本结构

```text
        Node A
          │
          │
          ├──────────── CANH
          │
          ├──────────── CANL
          │
        Node B
          │
        Node C
          │
        Node D
```

CAN 使用两根差分信号线：

```text
CANH
CANL
```

---

# 3. CAN 通信节点

一个 CAN 节点通常包含：

```text
Application
     │
     ▼
CAN Driver
     │
     ▼
CAN Controller
     │
     ▼
CAN Transceiver
     │
     ▼
CANH / CANL
```

例如汽车 ECU：

```text
CPU
 │
 ▼
CAN Controller
 │
 ▼
CAN Transceiver
 │
 ├── CANH
 └── CANL
```

---

# 4. CAN 为什么使用差分信号

CAN 使用：

```text
CANH
CANL
```

传输差分信号：

```text
Vdiff = CANH - CANL
```

接收器主要判断两根线之间的电压差，因此具有较强的抗干扰能力。

```text
CANH ────────────────
CANL ────────────────
        ↓
     差分信号
```

---

# 5. CAN 总线拓扑

典型结构：

```text
        Node A
          │
          │
══════════╪════════════════════════
          │
        Node B
          │
          │
        Node C
          │
          │
        Node D
```

所有节点共享：

```text
CANH
CANL
```

因此 CAN 是一种**共享总线**。

---

# 6. CAN 的终端电阻

CAN 总线两端通常需要：

```text
120Ω
```

终端电阻。

```text
120Ω                         120Ω
 │                            │
CANH ──────────────────────────
CANL ──────────────────────────
 │                            │
Node A                     Node D
```

两个终端电阻用于：

```text
减少信号反射
改善信号完整性
```

---

# 7. CAN 的核心：消息 ID

CAN 与 I2C 最大的区别之一：

```text
I2C → 设备地址

CAN → 消息 ID
```

例如：

```text
ID = 0x100
Data = Engine Speed
```

另一个：

```text
ID = 0x200
Data = Vehicle Speed
```

因此：

```text
CAN Bus
   │
   ├── ID 0x100 → 发动机转速
   ├── ID 0x200 → 车速
   ├── ID 0x300 → 温度
   └── ID 0x400 → 制动状态
```

---

# 8. CAN 是广播通信

一个节点发送：

```text
Node A
  │
  │ ID = 0x100
  ▼
CAN Bus
```

所有节点都可以看到这个消息：

```text
             CAN Bus
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
      ECU      ABS      仪表
```

节点根据：

```text
Message ID
```

决定是否接收。

---

# 9. CAN 数据帧

典型 CAN 数据帧：

```text
┌─────┬──────┬──────┬──────┬──────┐
│ SOF │ ID   │ Ctrl │ Data │ CRC  │
└─────┴──────┴──────┴──────┴──────┘
```

主要字段：

```text
SOF
 ↓
ID
 ↓
控制字段
 ↓
Data
 ↓
CRC
 ↓
ACK
 ↓
EOF
```

---

# 10. CAN 数据长度

经典 CAN：

```text
Data = 0 ~ 8 Byte
```

CAN FD：

```text
Data 最大可达到 64 Byte
```

因此 CAN FD 比经典 CAN 更适合传输较大的数据。

---

# 11. CAN 的优先级

CAN 使用消息 ID 决定仲裁优先级。

通常：

```text
ID 越小
   ↓
优先级越高
```

例如：

```text
Node A → ID = 0x100
Node B → ID = 0x200
```

同时发送时：

```text
0x100 获得总线
0x200 等待
```

这就是 CAN 的：

```text
Bit-wise Arbitration
按位仲裁
```

---

# 12. CAN 多主机

CAN 不需要固定的 Master。

任何节点都可以发起通信：

```text
Node A ──┐
Node B ──┼── CAN Bus
Node C ──┤
Node D ──┘
```

例如：

```text
ECU → 发送发动机转速

ABS → 发送轮速

仪表 → 发送仪表状态
```

因此 CAN 是：

> **Multi-Master 多主机总线。**

---

# 13. CAN ACK

发送节点发送数据后：

```text
发送节点
    │
    ▼
CAN Bus
    │
    ▼
其他节点
```

如果至少有一个节点正确接收到帧：

```text
ACK
```

发送节点可以知道：

```text
有人正确接收了这个消息
```

---

# 14. CAN 错误检测

CAN 具有较强的错误检测能力：

```text
CRC
ACK
Bit Monitoring
Bit Stuffing
Frame Check
```

出现错误时：

```text
检测错误
   ↓
发送 Error Frame
   ↓
当前消息重新发送
```

---

# 15. CAN 的典型应用

## 汽车

```text
Engine ECU
Transmission ECU
ABS
ESP
Airbag
Dashboard
```

例如：

```text
发动机 ECU
     │
     │ Engine RPM
     ▼
   CAN Bus
     │
     ▼
   Dashboard
```

---

## 工业控制

```text
PLC
 │
 ├── Motor Controller
 ├── Sensor
 ├── Servo
 └── IO Module
```

---

# 16. CAN 与 I2C 对比

| 项目     | CAN       | I2C     |
| ------ | --------- | ------- |
| 通信方式   | 广播        | 主从      |
| 主机     | 多主        | 主/从     |
| 线路     | CANH/CANL | SDA/SCL |
| 信号     | 差分        | 单端      |
| 设备识别   | 消息 ID     | 设备地址    |
| 抗干扰    | 强         | 一般      |
| 典型应用   | 汽车/工业     | 芯片内部外设  |
| 通信距离   | 较远        | 较短      |
| 数据量    | CAN 0~8B  | 取决于协议   |
| CAN FD | 最大64B     | -       |

---

# 17. CAN 与 UART 对比

| 项目   | CAN   | UART    |
| ---- | ----- | ------- |
| 通信方式 | 多主广播  | 点对点     |
| 信号   | 差分    | 单端      |
| 节点数量 | 多节点   | 通常两个    |
| 仲裁   | 有     | 无       |
| CRC  | 硬件支持  | 通常没有    |
| 抗干扰  | 强     | 较弱      |
| 典型应用 | 汽车/工业 | 调试/模块通信 |

---

# 18. CAN 驱动层次

```text
Application
     │
     ▼
CAN Protocol / Driver
     │
     ▼
CAN Controller
     │
     ▼
CAN Transceiver
     │
     ▼
CANH / CANL
     │
     ▼
CAN Bus
```

例如发送：

```c
can_send(0x100, data, 8);
```

最终完成：

```text
Message ID
     ↓
Data
     ↓
CAN Controller
     ↓
Transceiver
     ↓
CANH/CANL
     ↓
CAN Bus
```

---

# 19. CAN 核心知识点

学习 CAN 重点掌握：

```text
CANH / CANL
     ↓
差分通信
     ↓
Multi-Master
     ↓
Broadcast
     ↓
Message ID
     ↓
Bit-wise Arbitration
     ↓
CAN Frame
     ↓
ACK
     ↓
CRC / Error Detection
     ↓
CAN FD
```

---

# 20. 总结

CAN 是一种：

```text
多主机
广播式
差分
高可靠
实时
```

的通信总线。

最核心的理解：

```text
              CAN BUS
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
      ECU       ABS      Dashboard
       │         │         │
       └─────────┼─────────┘
                 │
              CANH/CANL
```

与 I2C 的关键区别：

```text
I2C：
设备地址 → 找设备

CAN：
消息 ID → 找数据
```

一句话总结：

> **CAN 通过 CANH/CANL 两根差分线连接多个节点，各节点通过消息 ID 进行广播通信，并通过优先级仲裁和完善的错误检测机制实现可靠的实时通信。**
