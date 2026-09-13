# 磁盘（Disk）原理详解

# 1. 什么是磁盘

磁盘（Disk）是一种用于长期存储数据的设备。

特点：

```text
断电不丢失
容量大
价格低
长期保存数据
```

例如：

```text
Windows系统
Linux系统
照片
视频
数据库
程序文件
```

最终都存储在磁盘中。

---

# 2. 为什么需要磁盘

CPU和内存虽然速度快，但存在问题：

```text
断电后数据丢失
容量有限
成本较高
```

例如：

```text
CPU Cache
L1 Cache
L2 Cache
DDR内存
```

都属于易失性存储器。

因此需要：

```text
磁盘
SSD
```

保存长期数据。

---

# 3. 存储层次结构

计算机中的存储系统通常如下：

```text
CPU寄存器
    ↓
L1 Cache
    ↓
L2 Cache
    ↓
L3 Cache
    ↓
DDR内存
    ↓
SSD/HDD
```

速度：

```text
快
↓
慢
```

容量：

```text
小
↓
大
```

---

# 4. 磁盘分类

现代计算机中的磁盘主要有两类：

```text
HDD
SSD
```

---

# 5. HDD（机械硬盘）

全称：

```text
Hard Disk Drive
```

内部结构：

```text
磁头
盘片
电机
控制器
```

示意图：

```text
       磁头
         ▼

 ┌─────────────┐
 │             │
 │    盘片      │
 │             │
 └─────────────┘

      ↑
     电机
```

通过盘片旋转实现数据读写。

---

# 6. HDD工作原理

机械硬盘内部盘片高速旋转：

例如：

```text
5400 RPM
7200 RPM
10000 RPM
```

RPM：

```text
Revolutions Per Minute
每分钟转数
```

---

读取过程：

```text
CPU
 ↓
磁盘控制器
 ↓
磁头移动
 ↓
找到目标位置
 ↓
读取数据
 ↓
返回内存
```

---

# 7. HDD中的盘片

盘片表面覆盖磁性材料。

数据以磁信号形式保存。

例如：

```text
N极
S极
```

表示：

```text
0
1
```

---

# 8. 磁道（Track）

盘片被划分为多个同心圆。

```text
 ┌─────────┐
 │ ○ ○ ○ ○ │
 │ ○ ○ ○ ○ │
 │ ○ ○ ○ ○ │
 └─────────┘
```

这些圆环称为：

```text
Track
磁道
```

---

# 9. 扇区（Sector）

磁道继续划分：

```text
Track
 ├─Sector
 ├─Sector
 ├─Sector
 └─Sector
```

扇区是磁盘最小物理存储单位。

常见大小：

```text
512 Byte
4 KB
```

---

# 10. 柱面（Cylinder）

多个盘片相同半径位置形成：

```text
Cylinder
柱面
```

示意：

```text
盘片1
盘片2
盘片3
```

相同磁道位置：

```text
Track 10
Track 10
Track 10
```

组成一个柱面。

---

# 11. HDD访问时间

读取数据需要：

## 寻道时间

磁头移动：

```text
Track A
↓
Track B
```

耗时：

```text
Seek Time
```

---

## 旋转延迟

等待目标扇区转到磁头下方：

```text
Rotational Latency
```

---

## 传输时间

读取数据：

```text
Transfer Time
```

---

总时间：

```text
访问时间

=
寻道时间
+
旋转延迟
+
传输时间
```

---

# 12. HDD优缺点

优点：

```text
容量大
价格低
寿命长
```

缺点：

```text
速度慢
有噪音
怕震动
```

---

# 13. SSD（固态硬盘）

全称：

```text
Solid State Drive
```

内部没有机械结构。

采用：

```text
NAND Flash
```

存储数据。

---

# 14. SSD内部结构

```text
SSD
│
├── Flash Controller
├── Cache
└── NAND Flash
```

---

# 15. SSD工作原理

数据保存在：

```text
Flash Cell
```

中。

利用电子存储电荷。

表示：

```text
0
1
```

---

# 16. SSD的组织结构

```text
SSD
│
├── Channel
│
├── Die
│
├── Plane
│
├── Block
│
└── Page
```

---

最小读写单位：

```text
Page
```

通常：

```text
4KB
8KB
16KB
```

---

擦除单位：

```text
Block
```

例如：

```text
256 Page
```

组成一个Block。

---

# 17. SSD为什么快

因为：

```text
没有磁头
没有盘片
没有寻道
```

访问过程：

```text
控制器
↓
Flash
↓
返回数据
```

速度远高于机械硬盘。

---

# 18. HDD与SSD对比

| 项目      | HDD | SSD   |
| ------- | --- | ----- |
| 存储介质    | 磁盘  | Flash |
| 是否有机械结构 | 有   | 无     |
| 速度      | 慢   | 快     |
| 噪音      | 有   | 无     |
| 功耗      | 较高  | 较低    |
| 容量价格比   | 高   | 较低    |

---

# 19. 磁盘接口

## SATA

传统接口：

```text
SATA III
6Gbps
```

理论速度：

```text
600MB/s
```

---

## NVMe

现代高速接口：

```text
PCIe
```

之上运行。

例如：

```text
PCIe 4.0 x4
```

带宽：

```text
约8GB/s
```

---

# 20. 文件如何存储

例如：

```text
hello.txt
```

内容：

```text
hello world
```

文件系统会将其拆分：

```text
Block1
Block2
Block3
```

存放到磁盘不同位置。

---

# 21. 文件系统

常见文件系统：

```text
FAT32
NTFS
EXT4
XFS
Btrfs
```

作用：

```text
管理文件
管理目录
管理空闲空间
```

---

# 22. 磁盘与操作系统

程序读取文件：

```c
fopen("test.txt");
```

流程：

```text
应用程序
 ↓
文件系统
 ↓
块设备驱动
 ↓
磁盘驱动
 ↓
SSD/HDD
```

---

# 23. DMA与磁盘

现代磁盘读写通常采用DMA。

例如：

```text
SSD
 ↓
DMA
 ↓
DDR
```

CPU只负责发起请求。

无需逐字节搬运数据。

---

# 24. Linux中的磁盘

查看磁盘：

```bash
lsblk
```

例如：

```text
sda
sdb
nvme0n1
```

---

查看分区：

```bash
fdisk -l
```

---

查看挂载：

```bash
mount
```

---

# 25. 磁盘性能指标

## IOPS

```text
Input Output Operations Per Second
```

每秒读写次数。

---

## Throughput

```text
MB/s
GB/s
```

吞吐量。

---

## Latency

```text
响应延迟
```

---

# 26. 总结

## HDD

```text
磁头
盘片
磁道
扇区
柱面
```

特点：

```text
容量大
价格低
速度慢
```

---

## SSD

```text
Flash
Controller
Page
Block
```

特点：

```text
速度快
无噪音
低功耗
```

---

## 数据访问路径

```text
CPU
 ↓
Cache
 ↓
DDR
 ↓
SSD/HDD
```

---

## 对操作系统工程师最重要的知识

```text
磁盘
 ↓
文件系统
 ↓
块设备驱动
 ↓
DMA
 ↓
页缓存(Page Cache)
 ↓
虚拟内存
```

理解这条链路之后，就能深入理解 Linux、Windows 等操作系统是如何管理和访问磁盘数据的。
