# Cache（缓存）原理详解

## 目录

- 什么是Cache
- 为什么需要Cache
- CPU与内存速度鸿沟
- Cache的基本工作原理
- 局部性原理
- Cache层次结构
- Cache Line
- Cache映射方式
- Cache读写过程
- Cache命中与未命中
- Cache替换算法
- Cache写策略
- 多核CPU中的Cache一致性
- Cache与虚拟内存
- Cache性能分析
- Cache在现代CPU中的作用
- 总结

---

# 1. 什么是Cache

Cache（缓存）是一种：

```text
容量较小
速度极快
位于CPU附近
```

的存储器。

---

其作用：

```text
把CPU即将访问的数据
提前保存起来
```

从而减少访问内存的时间。

---

一句话理解：

```text
Cache = CPU的数据高速缓存区
```

---

# 2. 为什么需要Cache

CPU速度越来越快：

```text
CPU主频：
3GHz ~ 6GHz
```

即：

```text
1个时钟周期
≈ 0.2ns ~ 0.3ns
```

---

而内存速度：

```text
DDR5
≈ 50ns ~ 100ns
```

---

对比：

| 设备 | 访问时间 |
|--------|--------|
| Register | 1 Cycle |
| L1 Cache | 1~4 Cycles |
| L2 Cache | 10~15 Cycles |
| L3 Cache | 30~60 Cycles |
| DRAM | 100~300 Cycles |

---

如果没有Cache：

```text
CPU大部分时间都在等待内存
```

---

# 3. CPU与内存速度鸿沟

```text
CPU
 ↓
每秒几十亿次运算

RAM
 ↓
远远跟不上
```

---

称为：

```text
Memory Wall
（内存墙）
```

---

解决办法：

```text
增加Cache
```

---

# 4. Cache基本工作原理

例如：

程序访问：

```c
a[0]
a[1]
a[2]
a[3]
```

---

第一次：

```text
CPU
 ↓
Cache Miss
 ↓
内存
 ↓
读取数据
```

---

同时：

```text
把附近的数据
一起放进Cache
```

---

之后：

```text
a[1]
a[2]
a[3]
```

直接从Cache读取。

---

# 5. 局部性原理

Cache能够工作的核心原因：

```text
程序访问具有局部性
```

---

## 时间局部性

刚访问的数据：

```text
未来大概率再次访问
```

例如：

```c
for(i=0;i<100;i++)
{
    sum += x;
}
```

变量：

```text
x
```

会不断被访问。

---

## 空间局部性

访问：

```text
a[0]
```

大概率接着访问：

```text
a[1]
a[2]
a[3]
```

---

因此：

```text
Cache一次加载一大片数据
```

---

# 6. Cache层次结构

现代CPU：

```text
CPU Core
  ↓
L1 Cache
  ↓
L2 Cache
  ↓
L3 Cache
  ↓
Memory
```

---

## L1 Cache

特点：

```text
最快
最小
```

通常：

```text
32KB ~ 128KB
```

---

## L2 Cache

特点：

```text
稍慢
稍大
```

通常：

```text
512KB ~ 4MB
```

---

## L3 Cache

特点：

```text
多个核心共享
```

通常：

```text
16MB ~ 256MB
```

---

# 7. Cache Line

Cache并不是按字节存储。

而是：

```text
Cache Line
```

作为最小单位。

---

典型大小：

```text
64 Bytes
```

---

例如：

访问：

```text
0x1000
```

实际上加载：

```text
0x1000 ~ 0x103F
```

共：

```text
64字节
```

---

# 8. Cache映射方式

## 直接映射

```text
一个内存块
只能放一个位置
```

优点：

```text
简单
```

缺点：

```text
冲突多
```

---

## 全相联映射

```text
可放任意位置
```

优点：

```text
命中率高
```

缺点：

```text
硬件复杂
```

---

## 组相联映射

现代CPU最常用。

例如：

```text
8-way Set Associative
```

---

# 9. Cache读过程

CPU访问：

```text
addr = 0x1000
```

---

步骤：

```text
CPU
 ↓
查L1
 ↓
命中？
```

---

如果：

```text
Hit
```

直接返回。

---

否则：

```text
L2
 ↓
L3
 ↓
Memory
```

---

# 10. Cache命中与未命中

## Cache Hit

```text
数据在Cache中
```

访问：

```text
几Cycle
```

---

## Cache Miss

```text
数据不在Cache中
```

访问：

```text
几十到几百Cycle
```

---

命中率：

```text
Hit Rate
=
Hit / Total
```

---

例如：

```text
99%
```

说明性能很好。

---

# 11. Cache替换算法

Cache满了怎么办？

---

常见算法：

## LRU

Least Recently Used

```text
淘汰最久没使用的数据
```

---

## FIFO

```text
先进先出
```

---

## Random

```text
随机淘汰
```

---

现代CPU通常：

```text
Pseudo-LRU
```

---

# 12. Cache写策略

## Write Through

```text
写Cache

同时写内存
```

---

优点：

```text
一致性好
```

缺点：

```text
慢
```

---

## Write Back

```text
先写Cache
```

以后再写内存。

---

优点：

```text
快
```

现代CPU主要采用：

```text
Write Back
```

---

# 13. 多核CPU中的Cache一致性

两个CPU核：

```text
Core0

Core1
```

都有自己的L1 Cache。

---

问题：

```text
Core0修改变量x

Core1不知道
```

---

导致：

```text
数据不一致
```

---

# 14. MESI协议

解决一致性问题。

状态：

| 状态 | 含义 |
|--------|--------|
| M | Modified |
| E | Exclusive |
| S | Shared |
| I | Invalid |

---

例如：

```text
Core0修改数据
```

其它Core：

```text
对应Cache Line失效
```

---

# 15. Cache与虚拟内存

CPU访问：

```text
虚拟地址
```

---

过程：

```text
CPU
 ↓
TLB
 ↓
物理地址
 ↓
Cache
 ↓
Memory
```

---

# 16. Cache性能分析

例如：

```c
for(i=0;i<1000000;i++)
{
    sum += a[i];
}
```

---

连续访问：

```text
Cache友好
```

命中率高。

---

而：

```c
for(i=0;i<1000000;i+=1024)
{
    sum += a[i];
}
```

---

跳跃访问：

```text
Cache Miss增加
```

性能下降。

---

# 17. Cache在现代CPU中的作用

现代CPU性能提升：

```text
高频率
乱序执行
分支预测
Cache
```

---

其中：

```text
Cache
```

通常贡献巨大。

---

没有Cache：

```text
CPU性能可能下降几十倍
```

甚至更多。

---

# 18. Cache与CPU内部结构关系

```text
             CPU Core
                 │
 ┌───────────────┼───────────────┐
 │               │               │

Register       ALU            LSU
 │                               │
 └───────────────┬───────────────┘
                 │
              L1 Cache
                 │
              L2 Cache
                 │
              L3 Cache
                 │
               DRAM
```

---

# 19. 总结

## Cache核心作用

```text
缩短CPU访问数据的时间
```

---

## Cache层次

```text
Register
 ↓
L1
 ↓
L2
 ↓
L3
 ↓
Memory
```

---

## Cache核心思想

```text
利用程序局部性

把未来可能访问的数据
提前放到高速缓存中
```

---

## 关键概念

| 名称 | 含义 |
|--------|--------|
| Cache Line | 缓存块 |
| Hit | 命中 |
| Miss | 未命中 |
| LRU | 替换算法 |
| MESI | 一致性协议 |
| Write Back | 回写策略 |

---

## 一句话理解

```text
Cache（缓存）

是CPU和内存之间的高速缓冲区。

它利用程序访问的局部性原理，
将热点数据提前保存到更快的存储中，
从而避免CPU频繁等待内存，提高系统整体性能。
```

---

## CPU访问数据完整流程

```text
程序
 ↓
寄存器(Register)
 ↓
L1 Cache
 ↓
L2 Cache
 ↓
L3 Cache
 ↓
主存(DRAM)
```

现代CPU之所以能够达到每秒数十亿次运算，Cache系统功不可没，它是CPU架构中最重要的性能加速技术之一。