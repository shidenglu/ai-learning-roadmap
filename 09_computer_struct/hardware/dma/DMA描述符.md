# DMA Descriptor 机制详解


# 1. 什么是 DMA Descriptor


DMA Descriptor（DMA描述符）是 DMA 控制器用于描述一次数据传输任务的数据结构。


简单理解：

> DMA Descriptor 就是一张“搬运任务清单”，告诉 DMA：数据在哪里、搬到哪里、搬多少、完成没有。


传统 DMA：

```
CPU

↓

配置DMA寄存器

↓

DMA传输

↓

完成
```


如果每次传输都需要 CPU 配置：

```
源地址

目的地址

长度

控制信息
```

那么 CPU 负担仍然很大。


因此引入：

```
DMA Descriptor
```


让 CPU：

```
提前准备任务列表

↓

DMA自动执行
```


---

# 2. 为什么需要 DMA Descriptor


## 2.1 普通DMA的问题


假设网卡发送数据：

```
Packet1

Packet2

Packet3

...

Packet1000
```


如果没有 Descriptor：

每发送一个包：

```
CPU

↓

设置源地址

↓

设置长度

↓

启动DMA

↓

等待完成
```


CPU需要频繁参与。


---

## 2.2 使用Descriptor后


CPU提前建立：

```
Descriptor Ring
```


例如：

```
+-------------+
| Descriptor0 |
+-------------+
| Descriptor1 |
+-------------+
| Descriptor2 |
+-------------+
| Descriptor3 |
+-------------+

```


每个Descriptor描述一个数据包：

```
地址

长度

状态

控制信息
```


DMA自动：

```
读取Descriptor

↓

搬运数据

↓

更新状态

↓

读取下一个Descriptor
```


CPU只需要：

```
初始化一次

处理完成事件
```


---

# 3. DMA Descriptor基本结构


一个典型Descriptor：

```
+----------------------+
| Buffer Address       |
+----------------------+
| Length               |
+----------------------+
| Control              |
+----------------------+
| Status               |
+----------------------+
| Next Descriptor Ptr  |
+----------------------+
```


包含：

| 字段 | 作用 |
|-|-|
| Buffer Address | 数据缓冲区地址 |
| Length | 数据长度 |
| Control | 控制信息 |
| Status | 状态信息 |
| Next Pointer | 下一个Descriptor地址 |


---

# 4. Descriptor字段详细说明


# 4.1 Buffer Address


表示：

```
实际数据存放地址
```


例如：

```
DMA Buffer:

0x80000000
```


Descriptor：

```
buffer_addr = 0x80000000
```


DMA读取：

```
Descriptor

↓

找到Buffer

↓

搬运数据
```


---

# 4.2 Length


表示：

```
需要传输的数据长度
```


例如：

```
Length = 1500
```


表示：

```
发送一个1500字节Ethernet Frame
```


---

# 4.3 Control


控制DMA行为。


例如：

```
OWN

INT

FIRST

LAST

CHAIN
```


常见含义：

| Bit | 含义 |
|-|-|
| OWN | DMA是否拥有该Descriptor |
| INT | 完成后是否产生中断 |
| FIRST | 数据包开始 |
| LAST | 数据包结束 |
| CHAIN | 是否链接下一个Descriptor |


---

# 4.4 Status


DMA运行后更新。


例如：

```
SUCCESS

ERROR

DONE
```


CPU通过Status判断：

```
DMA是否完成
```


---

# 4.5 Next Descriptor Pointer


指向：

```
下一个Descriptor
```


形成链表：

```
Descriptor0

    |

    ↓

Descriptor1

    |

    ↓

Descriptor2
```


---

# 5. Descriptor Ring（描述符环）


实际硬件中最常见：

```
Descriptor Ring
```


结构：

```
        +------------+
        | Descriptor0|
        +------------+
              |
              ↓

        +------------+
        | Descriptor1|
        +------------+
              |
              ↓

        +------------+
        | Descriptor2|
        +------------+

              |
              ↓

        +------------+
        | Descriptor3|
        +------------+

              |
              ↓

           回到0

```


形成循环队列。


---

# 6. 为什么使用Ring


## 6.1 连续处理数据


例如网络：

```
Packet1

Packet2

Packet3

Packet4
```


DMA：

```
Desc0

↓

Desc1

↓

Desc2

↓

Desc3

↓

Desc0
```


无需重新配置。


---

## 6.2 提高吞吐量


CPU：

```
一次提交多个任务
```


DMA：

```
连续执行
```


减少：

```
CPU-DMA交互次数
```


---

# 7. DMA Descriptor工作流程


以网卡发送为例。


## 第一步：申请Buffer


驱动申请：

```
TX Buffer
```


例如：

```
RAM:

0x80000000
```


---

## 第二步：填写Descriptor


CPU写：

```
Descriptor0:


Buffer Address:

0x80000000


Length:

1500


Control:

FIRST | LAST

```


---

## 第三步：交给DMA


CPU修改：

```
OWN=1
```


表示：

```
DMA拥有该任务
```


---

## 第四步：DMA读取Descriptor


DMA：

```
读取Descriptor

↓

获取Buffer地址

↓

读取数据
```


---

## 第五步：发送数据


DMA：

```
RAM

↓

MAC

↓

PHY

↓

网络
```


---

## 第六步：DMA更新状态


完成：

```
OWN=0

DONE=1
```


---

## 第七步：产生中断


DMA：

```
IRQ
```


通知CPU：

```
发送完成
```


---

# 8. OWN位的重要性


OWN（Owner）表示：

> 当前Descriptor属于谁。


通常：

```
OWN=1

DMA拥有
```


表示：

```
CPU不能修改
```


---

```
OWN=0

CPU拥有
```


表示：

```
DMA已经完成
```


---

状态转换：

```
CPU

↓

填写Descriptor

↓

OWN=1

↓

DMA处理

↓

OWN=0

↓

CPU回收
```


---

# 9. RX Descriptor（接收）


网络接收：

```
网卡

↓

DMA

↓

RAM
```


流程：


CPU提前准备：

```
RX Descriptor
```


例如：

```
Buffer Address:

0x90000000
```


然后：

```
OWN=1
```


表示：

```
DMA可以写入
```


---

网卡收到数据：

```
Packet

↓

DMA

↓

Buffer
```


完成：

```
OWN=0

Length=实际长度
```


CPU读取：

```
Packet
```


---

# 10. TX Descriptor（发送）


发送：

```
RAM

↓

DMA

↓

网卡
```


流程：

CPU：

```
准备Packet

↓

填写TX Descriptor

↓

OWN=1
```


DMA：

```
读取Buffer

↓

发送
```


完成：

```
OWN=0
```


---

# 11. Scatter-Gather Descriptor


普通DMA：

```
一个Descriptor

对应一个连续Buffer
```


问题：

数据可能分散：

```
Header

0x1000


Payload

0x5000
```


不连续。


Scatter-Gather：

允许：

```
Descriptor0

↓

Header


Descriptor1

↓

Payload
```


DMA一次完成。


---

# 12. 网络中的Descriptor应用


以Ethernet MAC为例：


## TX方向


```
Application


↓

Socket


↓

TCP/IP


↓

TX Buffer


↓

TX Descriptor


↓

DMA


↓

MAC


↓

PHY
```


---

## RX方向


```
PHY


↓

MAC


↓

DMA


↓

RX Descriptor


↓

RX Buffer


↓

TCP/IP


↓

Application
```


---

# 13. DMA Descriptor与驱动


驱动主要负责：


## 初始化


创建：

```
Descriptor Ring
```


设置：

```
Descriptor地址

Buffer地址
```


---

## 发送


流程：

```
申请Buffer

↓

填TX Descriptor

↓

启动DMA
```


---

## 接收


流程：

```
检查RX Descriptor

↓

获取Packet

↓

交给协议栈

↓

重新挂载Buffer
```


---

# 14. Descriptor与Cache一致性


DMA访问：

```
RAM
```


CPU访问：

```
Cache
```


可能出现：

```
CPU看到旧Descriptor
```


因此：


发送前：

```
Cache Flush

CPU Cache

↓

RAM
```


接收后：

```
Cache Invalidate

RAM

↓

CPU Cache
```


---

# 15. Descriptor与MMU


DMA通常使用：

```
物理地址
```


而CPU使用：

```
虚拟地址
```


因此：

需要：

```
Virtual Address

↓

Physical Address
```


例如Linux：

```
dma_map_single()
```


完成地址转换。


---

# 16. DMA Descriptor优势


## 降低CPU负担


CPU：

```
一次配置

多个任务执行
```


---

## 提高吞吐量


适合：

- 网络
- SSD
- 视频
- 音频


---

## 支持流水线


DMA：

```
传输Packet1

同时CPU处理Packet0
```


实现：

```
并行处理
```


---

# 17. DMA Descriptor缺点


## 软件复杂


需要管理：

- Descriptor状态
- Ring空间
- Cache同步
- 内存一致性


---

## 调试困难


问题可能来自：

```
地址错误

OWN错误

Cache未同步

长度错误
```


---

# 18. 总结


DMA Descriptor本质：

> 使用内存中的数据结构描述DMA传输任务，让DMA能够自主完成数据搬运。


核心结构：

```
Descriptor

{

 Buffer Address

 Length

 Control

 Status

 Next Pointer

}

```


典型流程：

```
CPU创建Descriptor

↓

设置Buffer

↓

交给DMA

↓

DMA读取Descriptor

↓

搬运数据

↓

更新Status

↓

中断通知CPU
```


网络设备：

```
RX Descriptor

负责接收


TX Descriptor

负责发送
```


一句话总结：

> DMA负责搬数据，Descriptor负责告诉DMA怎么搬；Ring负责让DMA连续、高效地处理大量数据。