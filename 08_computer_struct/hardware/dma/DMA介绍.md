# DMA（Direct Memory Access，直接内存访问）详解


# 1. 什么是 DMA

DMA（Direct Memory Access，直接内存访问）是一种：

> **允许外设在不经过 CPU 参与的情况下，直接访问内存的数据传输技术。**

传统数据传输：

```
外设

↓

CPU

↓

内存
```

DMA 数据传输：

```
外设

↓

DMA控制器

↓

内存
```

DMA 的核心思想：

```
让 CPU 负责控制

让 DMA 负责搬运数据
```

---

# 2. 为什么需要 DMA


## 2.1 没有 DMA 的数据传输


假设网卡收到一个数据包。


传统方式：

```
网卡收到数据

↓

产生中断

↓

CPU响应

↓

CPU读取网卡数据

↓

CPU写入内存

↓

处理完成
```


CPU参与每一次数据搬运。


例如：

网卡：

```
1Gbps

10Gbps

100Gbps
```


大量数据传输会导致：

```
CPU负载增加

效率降低
```

---

# 3. DMA解决的问题


DMA出现后：

```
网卡

↓

DMA控制器

↓

内存Buffer
```


过程：

```
CPU配置DMA

↓

DMA自动搬运数据

↓

完成后通知CPU
```


CPU只参与：

```
开始配置

↓

结束处理
```


中间的数据移动：

```
DMA完成
```

---

# 4. DMA系统组成


一个完整DMA系统包括：


```
             CPU

              |

              |
          配置DMA

              |

        DMA Controller

          /          \

         /            \

      外设            内存

      UART            RAM

      ETH             DDR

      SD              SRAM

```


主要组成：

| 部件 | 作用 |
|-|-|
| CPU | 配置DMA、处理结果 |
| DMA控制器 | 控制数据搬运 |
| 外设 | 数据来源或目的 |
| 内存 | 数据存储区域 |
| 总线 | 数据传输通道 |

---

# 5. DMA工作流程


一次DMA传输通常包含以下步骤：

---

## 第一步：CPU配置DMA


CPU设置：

```
源地址

目的地址

传输长度

方向

模式
```


例如：

内存：

```
0x80000000
```


外设：

```
UART FIFO
```


配置：

```
source = UART

destination = RAM

length = 1024 bytes
```

---

## 第二步：启动DMA


CPU发送：

```
DMA Start
```


DMA控制器开始工作。


---

## 第三步：DMA搬运数据


DMA控制：

```
读取数据

↓

写入目标地址
```


期间：

```
CPU可以继续运行
```

---

## 第四步：DMA完成通知


完成后：

DMA产生：

```
DMA interrupt
```


通知CPU：

```
数据已经准备完成
```

---

# 6. DMA传输方向


## 6.1 外设到内存（Peripheral → Memory）


例如：

网卡接收数据：

```
Ethernet

↓

DMA

↓

RAM Buffer
```


应用：

- 网络接收
- ADC采样
- 摄像头采集


---

## 6.2 内存到外设（Memory → Peripheral）


例如：

发送网络数据：

```
RAM Buffer

↓

DMA

↓

Ethernet
```


应用：

- 网络发送
- UART发送
- 音频播放


---

## 6.3 内存到内存（Memory → Memory）


例如：

复制大块数据：

```
RAM

↓

DMA

↓

RAM
```


应用：

- 图像复制
- 数据搬移


---

# 7. DMA与CPU对比


| 项目 | CPU搬运 | DMA搬运 |
|-|-|-|
| 数据路径 | 外设→CPU→内存 | 外设→内存 |
| CPU参与 | 高 | 低 |
| 效率 | 低 | 高 |
| 适合数据量 | 小 | 大 |
| 实时性 | 较差 | 好 |


---

# 8. DMA控制器内部结构


典型DMA控制器：

```
+----------------+

| DMA Controller |

+----------------+

       |

       |

+------+------+

|             |

Channel0   Channel1

Channel2   Channel3

```


每个Channel通常包含：

```
Source Address

Destination Address

Transfer Count

Control Register

Status Register
```

---

# 9. DMA寄存器模型


典型DMA寄存器：

## 9.1 源地址寄存器


Source Address：

保存：

```
数据来源地址
```


例如：

```
UART FIFO地址
```

---

## 9.2 目的地址寄存器


Destination Address：

保存：

```
数据写入地址
```


例如：

```
RAM Buffer
```

---

## 9.3 数据长度寄存器


Transfer Count：

表示：

```
需要搬运多少数据
```


例如：

```
4096 Bytes
```

---

## 9.4 控制寄存器


Control：

包含：

```
启动

方向

中断使能

传输模式
```

---

## 9.5 状态寄存器


Status：

表示：

```
空闲

运行

完成

错误
```

---

# 10. DMA传输模式


## 10.1 单次传输模式


一次DMA：

```
配置

↓

传输固定长度

↓

结束
```


适合：

```
一次性数据
```

---

## 10.2 循环模式


DMA完成后：

```
自动重新开始
```


应用：

- 音频
- ADC采样
- 网络接收


例如：

```
Buffer:

[0][1][2][3]


DMA:

0→1→2→3→0→1...
```

---

## 10.3 Scatter-Gather DMA


散列表DMA。


可以：

```
多个不连续Buffer

↓

一次DMA完成
```


例如：

网络协议：

```
Header Buffer

+

Payload Buffer

↓

一次发送
```


---

# 11. DMA与Cache问题


DMA最大的难点之一：

> CPU Cache一致性。


例如：

CPU：

```
Cache中有旧数据
```


DMA：

```
直接修改RAM
```


结果：

```
CPU读取Cache

得到旧数据
```

---

# 12. Cache一致性处理


## 方法1：Cache Flush


DMA发送前：

```
CPU Cache

↓

写回RAM
```


保证：

```
DMA读取最新数据
```


---

## 方法2：Cache Invalidate


DMA接收后：

```
清除Cache

↓

重新读取RAM
```


保证：

```
CPU看到DMA数据
```

---

# 13. DMA与MMU


现代系统：

```
CPU

↓

MMU

↓

虚拟地址

↓

物理地址

↓

RAM
```


但是DMA通常访问：

```
物理地址
```


因此：

DMA需要：

```
虚拟地址转换

或

固定物理内存
```

---

# 14. DMA Buffer设计


常见设计：

```
          RAM


+----------------+

| DMA Buffer     |

+----------------+

| Application    |

+----------------+

```


要求：

## 地址连续

DMA通常需要：

```
连续物理地址
```


---

## 地址对齐


例如：

```
64 Bytes

128 Bytes
```

提高访问效率。


---

# 15. DMA与中断结合


典型流程：

```
CPU

配置DMA

  |

  ↓

DMA搬数据

  |

  ↓

完成

  |

  ↓

DMA Interrupt

  |

  ↓

CPU处理
```


这是：

```
DMA + Interrupt
```

经典硬件设计。

---

# 16. 网络中的DMA


以网卡为例：

## 接收


```
网卡收到Packet

↓

DMA

↓

RX Ring Buffer

↓

CPU读取

↓

协议栈处理
```


---

## 发送


```
应用数据

↓

TX Buffer

↓

DMA

↓

网卡

↓

发送
```


---

# 17. DMA Ring Buffer


网络设备常用：

```
Descriptor Ring
```


结构：

```
+-------+
|Desc 0 |
+-------+
|Desc 1 |
+-------+
|Desc 2 |
+-------+
|Desc 3 |
+-------+
```


每个Descriptor描述：

```
Buffer地址

长度

状态
```

---

# 18. DMA在嵌入式系统中的应用


常见场景：

| 外设 | DMA应用 |
|-|-|
| UART | 高速串口收发 |
| SPI | Flash读写 |
| I2C | 数据传输 |
| ADC | 连续采样 |
| DAC | 音频输出 |
| Ethernet | 网络通信 |
| Camera | 图像采集 |
| SD Card | 文件读写 |


---

# 19. DMA与操作系统关系


操作系统通常提供：

```
DMA驱动
```

负责：

- DMA初始化
- Buffer管理
- 中断处理
- Cache同步


例如Linux：

```
DMA API
```


包括：

```
dma_alloc_coherent()

dma_map_single()

dma_unmap_single()
```

---

# 20. DMA与驱动开发


驱动流程：


```
设备初始化

↓

申请DMA Buffer

↓

配置DMA寄存器

↓

启动DMA

↓

等待中断

↓

处理数据

↓

释放资源
```


---

# 21. DMA优点


## 高吞吐

减少CPU搬运：

```
CPU计算

+

DMA搬运
```


并行工作。


---

## 降低CPU负载


CPU：

```
不用复制大量数据
```


---

## 提高实时性


适合：

- 网络
- 音频
- 视频
- 工业控制


---

# 22. DMA缺点


## 需要硬件支持


必须：

```
DMA Controller
```


---

## 软件复杂度增加


需要处理：

- 地址
- Cache
- 中断
- 同步


---

## 安全问题


DMA可以直接访问内存。


如果控制错误：

可能：

```
覆盖内存

破坏数据
```

因此现代系统引入：

```
IOMMU
```

限制DMA访问范围。

---

# 23. DMA与IOMMU


传统：

```
DMA

↓

物理内存
```


IOMMU：

```
DMA

↓

IOMMU

↓

允许访问区域

↓

内存
```


作用：

- 隔离设备
- 提高安全性
- 虚拟化支持


---

# 24. 总结


DMA的核心思想：

```
让专用硬件负责数据搬运

释放CPU
```


传统方式：

```
外设

↓

CPU

↓

内存
```


DMA方式：

```
外设

↓

DMA

↓

内存
```


关键流程：

```
CPU配置DMA

↓

DMA搬运数据

↓

产生中断

↓

CPU处理结果
```


核心价值：

```
提高数据传输效率

降低CPU负载

提高系统实时性
```


一句话总结：

> DMA就是让外设绕过CPU，直接和内存交换数据的一种高速数据传输机制，是现代嵌入式系统、网络设备和操作系统中的核心硬件技术。