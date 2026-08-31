# 网卡（NIC）原理详解

# 1. 什么是网卡

网卡（Network Interface Card，NIC）是计算机连接网络的硬件设备。

作用：

```text
负责发送网络数据
负责接收网络数据
实现网络通信
```

例如：

```text
浏览网页
微信聊天
SSH登录
文件传输
视频会议
```

都需要网卡参与。

---

# 2. 网卡在计算机中的位置

```text
应用程序
    ↓
TCP/IP协议栈
    ↓
网卡驱动
    ↓
网卡(NIC)
    ↓
网线/WiFi
    ↓
交换机
    ↓
互联网
```

---

# 3. 网卡的主要功能

## 数据发送

```text
CPU
 ↓
网卡
 ↓
网络
```

---

## 数据接收

```text
网络
 ↓
网卡
 ↓
CPU
```

---

## MAC地址管理

每个网卡都有唯一标识：

```text
MAC Address
```

例如：

```text
00:11:22:33:44:55
```

---

## 数据校验

负责：

```text
CRC计算
错误检测
```

---

# 4. 网卡分类

## 有线网卡

通过网线连接：

```text
RJ45
```

例如：

```text
千兆网卡
万兆网卡
```

---

## 无线网卡

通过无线电通信：

```text
WiFi
```

例如：

```text
802.11ac
802.11ax
WiFi 6
WiFi 7
```

---

# 5. 网卡内部结构

典型结构：

```text
NIC
│
├── MAC模块
├── PHY模块
├── DMA引擎
├── RX Buffer
├── TX Buffer
├── 中断模块
└── PCIe接口
```

---

# 6. MAC层

MAC：

```text
Media Access Control
介质访问控制层
```

负责：

```text
以太网帧封装
MAC地址处理
CRC生成
```

例如：

```text
IP数据包
 ↓
MAC封装
 ↓
Ethernet Frame
```

---

# 7. PHY层

PHY：

```text
Physical Layer
物理层
```

作用：

```text
数字信号
↓
电信号
```

以及：

```text
电信号
↓
数字信号
```

---

# 8. MAC与PHY关系

```text
CPU
 ↓
MAC
 ↓
MII/RGMII/SGMII
 ↓
PHY
 ↓
网线
```

---

# 9. MAC地址

网卡出厂时拥有唯一地址：

例如：

```text
00:1A:2B:3C:4D:5E
```

共：

```text
48 bit
```

格式：

```text
XX:XX:XX:XX:XX:XX
```

---

# 10. 数据发送流程

例如：

```c
send(socket, buf, len);
```

流程：

```text
应用程序
 ↓
TCP
 ↓
IP
 ↓
Ethernet
 ↓
网卡驱动
 ↓
NIC
 ↓
网线
```

---

# 11. Ethernet Frame

网卡发送的基本单位：

```text
Ethernet Frame
```

格式：

```text
+--------+--------+------+------+
|Dst MAC |Src MAC |Type  |Data  |
+--------+--------+------+------+
```

---

# 12. 数据接收流程

```text
网线
 ↓
PHY
 ↓
MAC
 ↓
RX Buffer
 ↓
DMA
 ↓
DDR
 ↓
CPU
```

---

# 13. DMA在网卡中的作用

如果没有DMA：

```text
网卡
 ↓
CPU搬运
 ↓
内存
```

CPU负担巨大。

---

有DMA：

```text
网卡
 ↓
DMA
 ↓
DDR
```

CPU只负责处理结果。

---

# 14. RX Buffer

接收缓冲区：

```text
Network
 ↓
NIC
 ↓
RX Buffer
```

用于暂存收到的数据包。

---

# 15. TX Buffer

发送缓冲区：

```text
CPU
 ↓
TX Buffer
 ↓
NIC
 ↓
Network
```

用于暂存待发送数据。

---

# 16. 网卡中断

收到数据包：

```text
NIC
 ↓
Interrupt
 ↓
CPU
```

通知系统：

```text
有新数据到了
```

---

# 17. 中断风暴问题

高流量场景：

```text
100万包/秒
```

如果每包一个中断：

```text
CPU被打爆
```

---

解决方案：

```text
NAPI
Polling
```

Linux广泛采用。

---

# 18. 网卡驱动

驱动负责：

```text
初始化网卡
配置DMA
处理中断
收发数据
```

Linux典型驱动：

```text
e1000
igb
ixgbe
r8169
```

---

# 19. Linux网络收包流程

```text
网线
 ↓
PHY
 ↓
MAC
 ↓
DMA
 ↓
Ring Buffer
 ↓
中断/NAPI
 ↓
netif_receive_skb()
 ↓
IP层
 ↓
TCP层
 ↓
Socket
 ↓
应用程序
```

---

# 20. Linux网络发包流程

```text
应用程序
 ↓
Socket
 ↓
TCP
 ↓
IP
 ↓
ARP
 ↓
网卡驱动
 ↓
DMA
 ↓
NIC
 ↓
网线
```

---

# 21. Ring Buffer

现代网卡大量使用环形缓冲区：

```text
+----+----+----+----+
|Pkt1|Pkt2|Pkt3|Pkt4|
+----+----+----+----+
```

特点：

```text
高性能
低锁竞争
适合DMA
```

---

# 22. 网卡与PCIe

PC中的网卡通常连接：

```text
PCIe
```

结构：

```text
CPU
 ↓
PCIe
 ↓
NIC
```

---

# 23. 网卡速度

常见规格：

```text
100 Mbps
1 Gbps
2.5 Gbps
10 Gbps
25 Gbps
40 Gbps
100 Gbps
```

数据中心：

```text
200G
400G
800G
```

也已广泛使用。

---

# 24. 校验和卸载

现代网卡支持：

```text
Checksum Offload
```

由网卡计算：

```text
IP Checksum
TCP Checksum
UDP Checksum
```

降低CPU负载。

---

# 25. TSO/GSO

大包分段卸载：

```text
TCP Segmentation Offload
```

例如：

```text
64KB数据
```

CPU不用拆：

```text
网卡自动拆分
```

---

# 26. RSS

Receive Side Scaling

作用：

```text
多核并行收包
```

例如：

```text
Queue0 → CPU0
Queue1 → CPU1
Queue2 → CPU2
Queue3 → CPU3
```

提高吞吐量。

---

# 27. SR-IOV

虚拟化常用：

```text
一个物理网卡
↓
多个虚拟网卡
```

提供给：

```text
多个虚拟机
```

使用。

---

# 28. 嵌入式系统中的网卡

常见：

```text
DM9000
RTL8211
LAN8720
DW GMAC
```

ARM SoC：

```text
CPU
 ↓
GMAC
 ↓
RGMII
 ↓
PHY
 ↓
RJ45
```

---

# 29. ARM SoC网络结构

```text
CPU
 │
AXI
 │
GMAC
 │
DMA
 │
PHY
 │
RJ45
```

其中：

```text
DMA
```

负责：

```text
DDR ↔ 网卡
```

高速搬运。

---

# 30. 总结

## 网卡是什么

```text
连接计算机与网络的设备
```

---

## 核心模块

```text
MAC
PHY
DMA
Buffer
Interrupt
```

---

## 发包流程

```text
CPU
 ↓
协议栈
 ↓
驱动
 ↓
网卡
 ↓
网络
```

---

## 收包流程

```text
网络
 ↓
网卡
 ↓
DMA
 ↓
内存
 ↓
CPU
```

---

## 对嵌入式/OS工程师最重要的知识链路

```text
网卡
 ↓
MAC
 ↓
PHY
 ↓
DMA
 ↓
中断
 ↓
NAPI
 ↓
Socket
 ↓
TCP/IP协议栈
```

掌握这条链路后，就能理解 Linux 网络驱动、lwIP、DPDK、ARM SoC GMAC 驱动以及高性能网络系统的工作原理。
