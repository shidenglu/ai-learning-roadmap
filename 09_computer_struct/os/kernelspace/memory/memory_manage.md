# OS 内存管理详解

> Memory Management in Operating Systems

---

# 1. 什么是 OS 内存管理

内存管理（Memory Management）是操作系统最核心的功能之一。

它主要负责：

* 管理物理内存
* 为进程分配和回收内存
* 建立虚拟地址与物理地址之间的映射
* 实现进程之间的内存隔离
* 管理内核使用的内存
* 管理页表
* 管理 TLB
* 实现虚拟内存
* 处理缺页异常
* 实现共享内存
* 管理内存保护
* 管理 DMA 等特殊内存区域

可以把 OS 的内存管理简单理解成：

```text
                 操作系统
                    │
          ┌─────────┴─────────┐
          │                   │
      虚拟内存管理         物理内存管理
          │                   │
     ┌────┼────┐         ┌────┼────┐
     │    │    │         │    │    │
    页表  TLB  缺页      分配  回收  区域
     │         │
     └────┬────┘
          │
      地址转换/保护
          │
       物理内存
```

---

# 2. 为什么需要内存管理

如果没有操作系统的内存管理，那么多个程序直接操作物理内存，会产生严重的问题。

例如：

```text
物理内存

0x00000000 ───────────────
             程序 A
             │
             │
0x00100000 ───────────────
             程序 B
             │
             │
0x00200000 ───────────────
```

如果程序 A 出现 bug：

```c
*p = 123;
```

而 `p` 恰好指向程序 B 的内存，那么 A 就可能修改 B 的数据。

因此操作系统需要解决几个核心问题：

```text
问题 1：程序应该使用什么地址？
问题 2：程序使用的地址如何找到真实内存？
问题 3：不同进程如何相互隔离？
问题 4：内存如何分配？
问题 5：内存如何回收？
问题 6：内存不足怎么办？
问题 7：内核如何使用内存？
```

这些问题共同构成了 OS 内存管理。

---

# 3. 内存管理的核心目标

OS 内存管理主要有以下几个目标。

## 3.1 内存分配

给进程分配内存：

```text
进程 A → 内存
进程 B → 内存
进程 C → 内存
```

---

## 3.2 内存回收

进程退出后：

```text
进程退出
   ↓
释放内存
   ↓
内存重新进入空闲内存池
```

---

## 3.3 地址转换

将：

```text
虚拟地址
```

转换成：

```text
物理地址
```

例如：

```text
虚拟地址
0x7FFFFFFF1234
       │
       ↓
     MMU
       │
       ↓
物理地址
0x123451234
```

---

## 3.4 内存保护

防止进程访问不属于自己的内存：

```text
进程 A

可以访问：
A 的代码
A 的数据
A 的堆
A 的栈

不能访问：

进程 B 的内存
内核受保护区域
不存在的地址
只读区域的写操作
```

---

## 3.5 内存共享

有时候不同进程需要访问同一块内存。

例如：

```text
进程 A
   │
   ├──────────┐
              ↓
          共享内存
              ↑
   ┌──────────┘
   │
进程 B
```

---

# 4. 计算机中的内存层次

现代计算机并不是只有一种内存。

典型结构：

```text
CPU
 │
 ├── 寄存器
 │
 ├── L1 Cache
 │
 ├── L2 Cache
 │
 ├── L3 Cache
 │
 ├── DRAM
 │
 └── Storage
       ├── SSD
       └── HDD
```

从速度来看：

```text
寄存器
  ↓
L1 Cache
  ↓
L2 Cache
  ↓
L3 Cache
  ↓
DRAM
  ↓
SSD
  ↓
HDD
```

越往下：

* 容量越来越大
* 速度越来越慢
* 单位成本越来越低

OS 内存管理主要关注：

```text
CPU 地址空间
        ↓
MMU
        ↓
DRAM / Physical Memory
```

同时还会和：

```text
磁盘
Swap
文件系统
DMA
设备
```

进行协作。

---

# 5. 地址空间

理解 OS 内存管理最重要的概念之一就是：

> 地址空间（Address Space）

一个程序看到的并不是整个物理内存，而是自己的地址空间。

例如：

```text
进程 A

0x00000000 ─────────────
             Code
0x00100000 ─────────────
             Data
             Heap
               ↓
               ↓

             空闲区域

               ↑
               ↑
             Stack
0x7FFFFFFF ─────────────
```

进程 B 也可以拥有类似的地址空间：

```text
进程 B

0x00000000 ─────────────
             Code
0x00100000 ─────────────
             Data
             Heap
             Stack
0x7FFFFFFF ─────────────
```

虽然两个进程使用相同的虚拟地址：

```text
进程 A：
0x10000000

进程 B：
0x10000000
```

但是它们可以映射到不同的物理地址。

---

# 6. 虚拟地址和物理地址

这是 OS 内存管理中最核心的概念之一。

## 6.1 虚拟地址

程序看到和使用的地址称为：

```text
Virtual Address
```

简称：

```text
VA
```

例如：

```c
int *p = malloc(1024);
```

程序获得的 `p` 通常是一个虚拟地址。

---

# 7. 物理地址

真正访问 DRAM 的地址称为：

```text
Physical Address
```

简称：

```text
PA
```

例如：

```text
虚拟地址：

0x00007F1234567000

↓

MMU

↓

物理地址：

0x0000001234567000
```

---

# 8. 为什么需要虚拟地址

如果所有程序都直接使用物理地址：

```text
程序 A → 物理地址
程序 B → 物理地址
程序 C → 物理地址
```

会产生很多问题。

例如：

```text
程序 A：

*p = 123;
```

可能覆盖：

```text
程序 B 的数据
```

而使用虚拟内存后：

```text
进程 A
虚拟地址 0x1000
       ↓
物理地址 0x5000


进程 B
虚拟地址 0x1000
       ↓
物理地址 0x9000
```

两个进程可以使用相同的虚拟地址。

但是最终访问的是不同的物理内存。

---

# 9. MMU

负责地址转换的硬件通常称为：

```text
MMU
Memory Management Unit
```

即：

> 内存管理单元

基本过程：

```text
CPU
 │
 │ Virtual Address
 ↓
MMU
 │
 │ 查询页表
 ↓
Physical Address
 │
 ↓
Cache / DRAM
```

MMU 同时还负责很多内存保护功能。

例如：

```text
Read
Write
Execute
User
Kernel
```

---

# 10. 虚拟地址转换

假设系统使用分页机制。

虚拟地址：

```text
Virtual Address

┌──────────────┬──────────────┐
│ Virtual Page │ Page Offset  │
│    Number    │              │
└──────────────┴──────────────┘
```

其中：

```text
Virtual Page Number
```

表示：

> 虚拟页编号

而：

```text
Page Offset
```

表示：

> 页内偏移

---

# 11. 分页机制

现代操作系统最常见的内存管理机制之一就是：

> Paging

即：

> 分页

核心思想：

将虚拟地址空间划分成固定大小的：

```text
Page
```

将物理内存划分成固定大小的：

```text
Page Frame
```

例如：

```text
虚拟地址空间

Page 0
Page 1
Page 2
Page 3
Page 4
...
```

物理内存：

```text
Frame 0
Frame 1
Frame 2
Frame 3
Frame 4
...
```

然后建立：

```text
Page → Frame
```

的映射。

---

# 12. Page 和 Page Frame

虚拟内存：

```text
Page
```

物理内存：

```text
Page Frame
```

例如页面大小为：

```text
4 KB
```

那么：

```text
Virtual Page 0 → Physical Frame 10
Virtual Page 1 → Physical Frame 3
Virtual Page 2 → Physical Frame 20
Virtual Page 3 → Physical Frame 8
```

于是：

```text
虚拟空间：

Page 0
Page 1
Page 2
Page 3

       │
       │ Page Table
       ↓

物理内存：

Frame 10
Frame 3
Frame 20
Frame 8
```

---

# 13. 页表

负责记录：

```text
Virtual Page
```

和：

```text
Physical Frame
```

之间关系的数据结构叫：

> Page Table

即：

> 页表

例如：

```text
虚拟页       物理页框

Page 0   →   Frame 5
Page 1   →   Frame 8
Page 2   →   Frame 2
Page 3   →   Frame 9
```

---

# 14. 页表项 PTE

页表中的每一项通常称为：

```text
PTE
Page Table Entry
```

页表项不仅保存物理页框地址，还保存各种权限和状态。

典型信息：

```text
Physical Frame Number
Read
Write
Execute
User
Present
Accessed
Dirty
```

例如：

```text
PTE

┌──────────────────────────────┐
│ Physical Frame Number        │
├──────────────────────────────┤
│ Present                      │
│ Read                         │
│ Write                        │
│ Execute                      │
│ User                         │
│ Accessed                     │
│ Dirty                        │
└──────────────────────────────┘
```

---

# 15. 地址转换过程

假设：

```text
Page Size = 4 KB
```

CPU 产生：

```text
VA = 0x12345678
```

那么可以拆成：

```text
Virtual Page Number
+
Page Offset
```

MMU：

```text
VA
 │
 ↓
提取 VPN
 │
 ↓
查询 Page Table
 │
 ↓
得到 Physical Frame
 │
 ↓
加上 Page Offset
 │
 ↓
PA
```

公式：

```text
Physical Address
=
Physical Frame Base
+
Page Offset
```

---

# 16. TLB

如果每次地址转换都访问页表：

```text
CPU
 ↓
Page Table
 ↓
DRAM
```

会非常慢。

因此 CPU 通常提供：

> TLB

全称：

```text
Translation Lookaside Buffer
```

即：

> 地址转换旁路缓冲器

可以把 TLB 理解成：

> 页表映射的高速缓存。

---

# 17. TLB 工作流程

访问虚拟地址：

```text
CPU
 │
 │ VA
 ↓
TLB
 │
 ├── Hit ─────→ 得到 PA
 │
 └── Miss
       ↓
     Page Table
       ↓
     得到 PTE
       ↓
     更新 TLB
       ↓
     得到 PA
```

所以：

```text
TLB Hit
```

通常可以快速完成地址转换。

---

# 18. TLB 和 Cache 的区别

TLB 和 Cache 都是高速缓存，但是缓存的东西不同。

| 项目   | TLB                          | Cache  |
| ---- | ---------------------------- | ------ |
| 全称   | Translation Lookaside Buffer | Cache  |
| 缓存内容 | 地址转换关系                       | 数据/指令  |
| 作用   | VA → PA                      | 缓存数据   |
| 服务对象 | MMU                          | CPU    |
| 主要目的 | 加速地址转换                       | 加速数据访问 |

可以理解成：

```text
TLB：

VA → PA

Cache：

PA → Data
```

实际现代 CPU 的缓存体系更加复杂，但这个理解非常适合入门。

---

# 19. 多级页表

如果一个进程拥有非常大的虚拟地址空间，直接建立完整页表会非常浪费内存。

因此现代 CPU 通常使用：

> 多级页表

例如：

```text
Virtual Address

┌──────┬──────┬──────┬──────┐
│ L0   │ L1   │ L2   │ L3   │
└──────┴──────┴──────┴──────┘
   │
   ↓
L0 Table
   │
   ↓
L1 Table
   │
   ↓
L2 Table
   │
   ↓
L3 Table
   │
   ↓
Page
```

---

# 20. 为什么需要多级页表

假设虚拟地址空间非常大：

```text
64-bit Virtual Address
```

如果给整个地址空间的每个 Page 都建立 PTE：

```text
页表规模可能非常巨大
```

但是一个普通程序实际上只使用一小部分地址空间。

因此多级页表可以做到：

> 用到哪个区域，就创建哪个区域对应的页表。

例如：

```text
整个虚拟地址空间

┌──────────────────────────────┐
│                              │
│      未使用                   │
│                              │
├──────────────────────────────┤
│      Code                    │
├──────────────────────────────┤
│      Data                    │
├──────────────────────────────┤
│      Heap                    │
├──────────────────────────────┤
│      未使用                   │
├──────────────────────────────┤
│      Stack                   │
└──────────────────────────────┘
```

没有使用的区域不需要建立完整的底层页表。

---

# 21. 缺页异常

如果 CPU 访问一个虚拟地址，但是：

```text
Page Table
```

发现页面不存在：

```text
Present = 0
```

就可能产生：

> Page Fault

即：

> 缺页异常

流程：

```text
CPU 访问 VA
      ↓
TLB Miss
      ↓
查询 Page Table
      ↓
发现 Page 不存在
      ↓
Page Fault
      ↓
CPU 进入异常处理
      ↓
OS Kernel
      ↓
判断原因
```

---

# 22. 缺页异常不一定意味着错误

很多人第一次接触 Page Fault 时容易认为：

> Page Fault = 程序出错

实际上不是。

Page Fault 可能是正常的内存管理机制。

例如：

```text
程序第一次访问某个页面
        ↓
页面还没有真正分配物理内存
        ↓
触发 Page Fault
        ↓
OS 分配物理页
        ↓
建立页表映射
        ↓
重新执行指令
```

这种情况属于正常的：

> Demand Paging

---

# 23. Demand Paging

Demand Paging：

> 按需分页

核心思想：

```text
程序声明/使用大量虚拟内存
             ↓
并不立即分配所有物理内存
             ↓
真正访问时
             ↓
触发 Page Fault
             ↓
再分配物理页面
```

例如：

```c
malloc(1GB);
```

并不一定意味着：

```text
立即占用 1GB 物理内存
```

具体行为取决于操作系统、分配器和内存提交策略。

真正访问页面时才可能触发实际物理页分配。

---

# 24. Copy-on-Write

另一个非常重要的机制：

> Copy-on-Write

简称：

```text
COW
```

即：

> 写时复制

典型场景：

```text
fork()
```

父进程：

```text
Page A
```

子进程：

```text
Page A
```

最开始两个进程可以共享同一个物理页面：

```text
Process A
   │
   │
   ├──────────┐
              ↓
          Physical Page
              ↑
   ┌──────────┘
   │
Process B
```

如果两个进程都只是读取：

```text
共享
```

如果某个进程执行：

```text
write
```

那么触发：

```text
Page Fault
     ↓
分配新的 Physical Page
     ↓
复制数据
     ↓
修改页表
     ↓
继续执行
```

---

# 25. 虚拟内存

虚拟内存的核心思想：

> 给进程提供一个独立、连续、巨大的虚拟地址空间，而不要求这些地址全部对应连续的物理内存。

例如：

```text
虚拟地址：

0x10000000
0x10001000
0x10002000
0x10003000

       ↓

物理地址：

0x50000000
0x72000000
0x12000000
0x90000000
```

物理内存可以是：

```text
离散的
```

但是从程序角度看：

```text
虚拟地址空间是连续的
```

---

# 26. 虚拟内存带来的好处

## 26.1 进程隔离

```text
Process A
   ↓
VA
   ↓
PA A


Process B
   ↓
VA
   ↓
PA B
```

---

## 26.2 内存保护

例如：

```text
Code：

R-X

Data：

RW-

Stack：

RW-
```

可以禁止：

```text
向代码区域写数据
```

也可以禁止：

```text
执行数据区域
```

这就是：

> W^X / NX 等内存保护思想的基础之一。

---

## 26.3 程序不需要关心物理内存位置

程序只需要使用：

```text
Virtual Address
```

不需要知道：

```text
Physical Address
```

---

## 26.4 支持共享内存

多个虚拟地址可以映射到同一个物理页面：

```text
Process A VA
       │
       ↓
   Physical Page
       ↑
       │
Process B VA
```

---

# 27. 内存保护

内存管理不仅仅负责：

> 地址转换

还负责：

> 访问权限控制。

常见权限：

```text
R = Read
W = Write
X = Execute
```

例如：

```text
代码段：

R-X

数据段：

RW-

只读数据：

R--

```

如果程序尝试：

```text
向 R-- 区域写数据
```

CPU 可以触发异常。

---

# 28. User 和 Kernel 权限

现代 CPU 通常区分：

```text
User Mode
```

和：

```text
Kernel Mode
```

例如：

```text
User Application
       │
       │ syscall
       ↓
Kernel
       │
       ↓
Hardware
```

用户程序不能随便访问：

```text
Kernel Memory
```

否则会破坏操作系统。

---

# 29. 用户空间和内核空间

典型操作系统会将地址空间划分成：

```text
虚拟地址空间

高地址
┌──────────────────────┐
│ Kernel Space         │
├──────────────────────┤
│                      │
│                      │
│ User Space           │
│                      │
└──────────────────────┘
低地址
```

用户程序通常运行在：

```text
User Space
```

操作系统内核运行在：

```text
Kernel Space
```

---

# 30. 用户空间典型布局

典型进程可以理解为：

```text
高地址

┌──────────────────────┐
│ Stack                │
│        ↓             │
├──────────────────────┤
│                      │
│      mmap 区域       │
│                      │
├──────────────────────┤
│        ↑             │
│ Heap                 │
├──────────────────────┤
│ Data / BSS           │
├──────────────────────┤
│ Code / Text          │
└──────────────────────┘

低地址
```

其中：

```text
Code
Data
BSS
Heap
mmap
Stack
```

是理解进程内存布局的重要概念。

---

# 31. Code / Text Segment

代码段保存：

```text
机器指令
```

例如：

```c
int add(int a, int b)
{
    return a + b;
}
```

编译后会生成机器指令。

通常：

```text
Text Segment

权限：

R-X
```

即：

```text
可读
可执行
不可写
```

---

# 32. Data Segment

Data Segment 保存：

> 已初始化的全局变量和静态变量。

例如：

```c
int global = 100;
```

通常属于：

```text
Data Segment
```

---

# 33. BSS Segment

BSS 通常保存：

> 未初始化或者初始化为 0 的全局变量和静态变量。

例如：

```c
int global;
static int value;
```

程序加载时，BSS 通常不需要在可执行文件中保存大量实际数据。

只需要记录：

```text
BSS Size
```

然后 OS/Loader 在内存中创建对应区域并初始化为 0。

---

# 34. Heap

Heap：

> 堆

主要用于动态内存分配。

例如：

```c
malloc()
calloc()
realloc()
free()
```

示意：

```text
Heap

       ↑
       │
       │ 增长
       │
┌───────────────┐
│               │
│     Heap      │
│               │
└───────────────┘
```

注意：

> 用户程序的 `malloc()` 并不等于直接调用内核的物理页分配器。

通常存在多层：

```text
malloc
  ↓
用户态内存分配器
  ↓
系统调用
  ↓
Kernel Memory Manager
  ↓
Physical Page
```

---

# 35. Stack

Stack：

> 栈

用于保存函数调用相关的数据。

例如：

```c
void foo()
{
    int a;
    int b;

    bar();
}
```

栈可能保存：

```text
局部变量
返回地址
保存的寄存器
函数调用信息
```

典型结构：

```text
高地址

┌───────────────┐
│ foo Stack     │
├───────────────┤
│ bar Stack     │
├───────────────┤
│ main Stack    │
└───────────────┘

低地址
```

具体栈增长方向由体系结构和 ABI 决定，常见架构通常向低地址增长。

---

# 36. 内核内存管理

OS 自己也需要内存。

例如：

```text
进程控制块 PCB
页表
内核线程
驱动
网络协议栈
文件系统
缓存
内核对象
```

所以内核需要自己的内存管理系统。

可以简单理解为：

```text
                 Kernel
                   │
          ┌────────┴────────┐
          │                 │
     Virtual Memory    Physical Memory
          │                 │
          │                 │
       Page Table      Page Allocator
                              │
                        Slab / SLUB
```

---

# 37. 物理内存管理

内核首先需要管理：

> Physical Memory

例如机器拥有：

```text
16 GB RAM
```

OS 需要知道：

```text
哪些物理页面正在使用
哪些页面空闲
哪些页面属于内核
哪些页面属于用户进程
哪些页面用于 DMA
哪些页面被缓存
```

---

# 38. Bitmap 管理物理页面

一种简单的物理内存管理方法：

> Bitmap

例如：

```text
Page 0  → 0
Page 1  → 1
Page 2  → 0
Page 3  → 1
Page 4  → 0
```

可以定义：

```text
0 = Free
1 = Used
```

那么：

```text
Bitmap:

0 1 0 1 0 0 1 0
```

就可以表示物理页面使用情况。

---

# 39. Free List

另一种常见方式：

> 空闲链表

例如：

```text
Free Page
   ↓
Page 3
   ↓
Page 8
   ↓
Page 10
   ↓
Page 15
```

申请页面：

```text
pop()
```

释放页面：

```text
push()
```

---

# 40. Buddy System

Linux 等操作系统中常见：

> Buddy Allocator

即：

> 伙伴系统

核心思想：

将内存按照：

```text
2^n
```

大小进行管理。

例如：

```text
Order 0 → 1 Page
Order 1 → 2 Pages
Order 2 → 4 Pages
Order 3 → 8 Pages
Order 4 → 16 Pages
```

例如需要：

```text
4 Pages
```

可以申请：

```text
Order 2
```

---

# 41. 为什么需要 Buddy System

因为操作系统经常需要：

```text
申请不同大小的连续物理内存
```

伙伴系统可以比较高效地：

```text
分裂
合并
```

例如：

```text
64 Pages
```

分裂：

```text
64
 ↓
32 + 32
 ↓
16 + 16 + 32
 ↓
...
```

释放后，如果两个伙伴都空闲：

```text
16 + 16
   ↓
32
```

继续：

```text
32 + 32
   ↓
64
```

这样可以减少外部碎片。

---

# 42. Slab / SLUB

Buddy System 更适合：

> 页面级别的物理内存管理。

但是内核中经常需要申请：

```text
几十字节
几百字节
几 KB
```

如果每次都按照 Page 分配，会产生很大浪费。

所以内核通常使用：

> Slab / SLUB

这种对象分配器。

例如：

```text
Page
 │
 ├── Object
 ├── Object
 ├── Object
 ├── Object
 └── Object
```

适合频繁创建和销毁固定大小的内核对象。

---

# 43. Buddy 和 SLUB 的关系

可以理解为：

```text
                Kernel Memory
                     │
          ┌──────────┴──────────┐
          │                     │
      Page Allocator       Object Allocator
          │                     │
        Buddy                  SLUB
          │                     │
          └──────────┬──────────┘
                     ↓
               Physical Memory
```

简单来说：

```text
Buddy
→ 管 Page

SLUB
→ 管 Object
```

---

# 44. `malloc()` 到物理内存发生了什么

例如：

```c
void *p = malloc(100);
```

并不是简单：

```text
malloc
 ↓
物理地址
```

更合理的理解是：

```text
Application
     │
     ↓
malloc()
     │
     ↓
User Allocator
     │
     ↓
系统调用
     │
     ↓
Kernel Virtual Memory
     │
     ↓
Physical Page
     │
     ↓
DRAM
```

其中可能涉及：

```text
brk/sbrk
mmap
Page Fault
Page Allocator
```

具体路径取决于分配大小、分配器实现以及操作系统。

---

# 45. 内存碎片

内存管理中的一个重要问题：

> Fragmentation

主要有：

```text
Internal Fragmentation
内部碎片

External Fragmentation
外部碎片
```

---

# 46. 内部碎片

内部碎片：

> 分配给程序的内存大于实际需要的内存。

例如：

```text
需要：

100 bytes

但是分配粒度：

128 bytes
```

那么：

```text
浪费：

28 bytes
```

这就是内部碎片。

---

# 47. 外部碎片

例如：

```text
Free  Free  Used  Free  Used  Free
```

总空闲内存可能很多。

但是：

```text
没有足够大的连续区域
```

于是无法满足：

```text
连续大块内存分配
```

这就是外部碎片。

分页机制能够显著降低连续物理内存分配带来的外部碎片问题。

---

# 48. 页面回收

当系统内存不足时：

```text
Free Memory ↓
```

OS 需要回收内存。

可能回收：

```text
Page Cache
匿名页面
文件映射页面
其他可回收内存
```

---

# 49. Swap

Swap：

> 交换空间

可以将某些内存页面暂时放到磁盘：

```text
RAM
 │
 │ Page
 ↓
Swap
 │
 │
 ↓
Disk
```

当再次访问：

```text
Page Fault
     ↓
从 Swap 读取
     ↓
重新放入 RAM
```

这会带来较高的性能开销。

因此：

> Swap 是内存管理中的一种扩展机制，而不是速度等价于 RAM 的“第二内存”。

---

# 50. Page Cache

操作系统会利用空闲内存缓存文件数据：

```text
Application
     ↓
File
     ↓
Page Cache
     ↓
Disk
```

读取文件时：

```text
Application
     ↓
Page Cache Hit
     ↓
直接读取 RAM
```

比直接访问磁盘快很多。

---

# 51. Anonymous Memory

匿名内存：

> Anonymous Memory

指没有直接对应文件的内存。

例如：

```text
malloc()
```

产生的很多用户空间内存通常属于匿名内存。

典型：

```text
Heap
Stack
Anonymous mmap
```

---

# 52. File-backed Memory

文件映射内存：

```text
File
  │
  ↓
mmap()
  │
  ↓
Virtual Memory
```

例如：

```c
mmap()
```

可以将文件映射到进程虚拟地址空间。

这样程序可以通过：

```c
*p
```

直接访问文件对应的数据区域。

---

# 53. Shared Memory

共享内存是进程间通信的重要方式。

例如：

```text
Process A
Virtual Page A
       │
       ↓
Physical Page
       ↑
       │
Virtual Page B
Process B
```

两个进程可以通过映射到同一个物理页面来共享数据。

优点：

```text
数据不需要频繁复制
```

因此共享内存通常具有很高的性能。

---

# 54. 内存映射

现代操作系统中：

```text
Virtual Memory
```

和：

```text
Physical Memory
```

不是简单的一一对应关系。

可以建立：

```text
VA → PA
```

也可以：

```text
VA → File
```

甚至：

```text
VA → Shared Physical Page
```

因此虚拟内存实际上是一种非常强大的抽象。

---

# 55. Huge Page

普通页面：

```text
4 KB
```

当内存很大时：

```text
Page 数量非常多
```

页表会变得庞大。

因此现代系统支持：

> Huge Page

例如：

```text
2 MB
1 GB
```

具体大小取决于 CPU 架构和 OS 配置。

优势：

```text
Page 数量减少
↓
页表减少
↓
TLB 覆盖范围增加
↓
降低 TLB Miss
```

---

# 56. TLB Reach

TLB Reach：

> TLB 能够覆盖的虚拟内存范围。

例如：

```text
TLB Entries = 1024
Page Size = 4 KB
```

那么理论覆盖：

```text
1024 × 4 KB
=
4 MB
```

如果使用：

```text
2 MB Huge Page
```

则：

```text
1024 × 2 MB
=
2 GB
```

因此 Huge Page 对大内存、高性能计算等场景很重要。

---

# 57. NUMA

大型服务器通常采用：

> NUMA

全称：

```text
Non-Uniform Memory Access
```

即：

> 非统一内存访问

结构可以理解为：

```text
CPU 0 ─── Memory 0

CPU 1 ─── Memory 1

CPU 2 ─── Memory 2
```

CPU 0 访问：

```text
Memory 0
```

通常比访问：

```text
Memory 1
```

更快。

因此 OS 内存管理不仅要考虑：

```text
有没有内存
```

还需要考虑：

```text
内存在哪里
```

---

# 58. DMA 与内存管理

设备进行 DMA 时：

```text
Device
   │
   │ DMA
   ↓
Memory
```

设备可以直接读写内存。

因此 OS 必须考虑：

```text
物理地址
DMA 地址
IOMMU
Cache Coherency
内存对齐
内存连续性
DMA Buffer
```

---

# 59. IOMMU

IOMMU：

> Input-Output Memory Management Unit

可以理解为：

> 给设备提供类似 MMU 的地址转换和保护能力。

传统情况下：

```text
CPU
 ↓
MMU
 ↓
Physical Memory
```

有 IOMMU：

```text
CPU
 ↓
MMU
 ↓
Memory

Device
 ↓
IOMMU
 ↓
Memory
```

IOMMU 可以实现：

```text
DMA 地址转换
DMA 内存隔离
设备访问控制
```

---

# 60. Cache Coherency 与内存管理

现代多核 CPU：

```text
CPU 0
 └── Cache

CPU 1
 └── Cache
```

多个 CPU 可能缓存同一块内存。

因此需要保证：

```text
Cache
```

和：

```text
Memory
```

之间的一致性。

这就是：

> Cache Coherency

对于操作系统、驱动、DMA 等系统软件来说，这是理解内存系统非常重要的一部分。

---

# 61. 内存屏障

多核系统中：

```text
CPU 0
CPU 1
```

可能存在：

```text
乱序执行
Store Buffer
Cache
```

因此操作系统和驱动经常需要使用：

> Memory Barrier

例如：

```text
Load Barrier
Store Barrier
Full Barrier
```

不同 CPU 架构提供不同的内存模型和屏障指令。

---

# 62. 进程创建与内存

当执行：

```c
fork();
```

操作系统通常不会立即把父进程所有内存完整复制一份。

而是使用：

```text
Copy-on-Write
```

大致：

```text
Parent
   │
   ├──────────┐
              ↓
          Physical Page
              ↑
   ┌──────────┘
   │
Child
```

只有写入时：

```text
Page Fault
   ↓
Copy Page
   ↓
建立独立映射
```

这样可以大幅降低进程创建成本。

---

# 63. 程序加载与内存管理

执行：

```bash
./app
```

大致过程：

```text
Shell
 ↓
execve()
 ↓
Kernel
 ↓
读取 ELF
 ↓
创建进程地址空间
 ↓
建立代码/数据映射
 ↓
建立 Stack
 ↓
建立 Heap 初始区域
 ↓
建立动态链接相关映射
 ↓
设置页表
 ↓
返回用户态
 ↓
开始执行
```

这里：

```text
ELF
虚拟内存
页表
物理内存
```

是紧密关联的。

---

# 64. ELF 与内存映射

ELF 文件通常包含：

```text
.text
.rodata
.data
.bss
```

加载器会根据：

```text
Program Header
```

将需要的内容映射到虚拟地址空间。

例如：

```text
ELF

.text
  ↓
Virtual Memory
  ↓
R-X

.rodata
  ↓
Virtual Memory
  ↓
R--

.data
  ↓
Virtual Memory
  ↓
RW-

.bss
  ↓
Virtual Memory
  ↓
RW-
```

---

# 65. 地址空间与页表的关系

可以把整个关系总结成：

```text
Process
   │
   ↓
Virtual Address Space
   │
   ↓
Page Table
   │
   ↓
Virtual Page → Physical Frame
   │
   ↓
MMU
   │
   ↓
Physical Memory
```

---

# 66. 一个完整的内存访问过程

假设程序执行：

```c
x = *p;
```

其中：

```text
p = Virtual Address
```

那么大致过程：

```text
CPU 执行 Load
      ↓
产生 Virtual Address
      ↓
检查 TLB
      ↓
      ├── TLB Hit
      │      ↓
      │   得到 Physical Address
      │
      └── TLB Miss
             ↓
          查询 Page Table
             ↓
             ├── Page Present
             │       ↓
             │    更新 TLB
             │       ↓
             │    得到 PA
             │
             └── Page Not Present
                     ↓
                 Page Fault
                     ↓
                   Kernel
                     ↓
                分配/加载页面
                     ↓
                  更新页表
                     ↓
                  返回执行
      ↓
Physical Address
      ↓
Cache
      ↓
DRAM
      ↓
返回数据
      ↓
CPU
```

这是理解现代虚拟内存系统最重要的一条主线。

---

# 67. 内存管理的层次结构

从应用程序一直到底层硬件，可以形成：

```text
┌──────────────────────────────┐
│ Application                  │
├──────────────────────────────┤
│ malloc / mmap / free         │
├──────────────────────────────┤
│ User Memory Allocator        │
├──────────────────────────────┤
│ System Call                  │
├──────────────────────────────┤
│ Kernel Virtual Memory        │
├──────────────────────────────┤
│ Page Fault Handler           │
├──────────────────────────────┤
│ Page Table Management        │
├──────────────────────────────┤
│ Physical Page Allocator      │
├──────────────────────────────┤
│ Buddy / SLUB                 │
├──────────────────────────────┤
│ MMU / TLB                    │
├──────────────────────────────┤
│ Cache                        │
├──────────────────────────────┤
│ DRAM                         │
└──────────────────────────────┘
```

---

# 68. OS 内存管理核心数据结构

一个操作系统的内存管理通常会涉及大量数据结构。

典型包括：

```text
Page
Page Table
PTE
VMA
Address Space
Free List
Buddy
Slab / SLUB
Page Cache
Swap
Memory Region
```

在 Linux 中还会看到：

```text
struct page
struct mm_struct
struct vm_area_struct
pgd
p4d
pud
pmd
pte
```

等概念。

---

# 69. `mm_struct`

以 Linux 为例：

```text
mm_struct
```

可以理解为：

> 一个进程的用户态地址空间描述信息。

其中包含很多重要信息，例如：

```text
页表
VMA
地址空间范围
代码区域
数据区域
堆
栈
mmap 区域
```

可以粗略理解：

```text
Process
   │
   ↓
mm_struct
   │
   ├── Page Table
   ├── VMA
   ├── Heap
   ├── Stack
   ├── Code
   └── Data
```

---

# 70. VMA

Linux 中：

```text
vm_area_struct
```

简称：

```text
VMA
```

表示：

> 一段具有相同属性的连续虚拟地址区域。

例如：

```text
0x400000 ─────────────
           Code
           R-X
0x500000 ─────────────

0x600000 ─────────────
           Data
           RW-
0x700000 ─────────────

0x800000 ─────────────
           Heap
           RW-
```

每一段都可以由 VMA 描述。

---

# 71. VMA 和 Page Table 的区别

这是一个非常容易混淆的问题。

VMA：

> 描述虚拟地址区域的属性和范围。

Page Table：

> 描述虚拟地址如何映射到物理地址。

例如：

```text
VMA

0x10000000 ~ 0x20000000
权限：RW
```

表示：

```text
这一段虚拟地址可以读写
```

而页表描述：

```text
0x10000000 → Physical Page A
0x10001000 → Physical Page B
0x10002000 → Physical Page C
```

所以：

```text
VMA
↓
描述“这是什么区域、有什么权限”

Page Table
↓
描述“它现在映射到了哪里”
```

---

# 72. 内核虚拟地址

内核也可能使用虚拟地址。

例如：

```text
Kernel Virtual Address
        ↓
      MMU
        ↓
Physical Address
```

这样内核同样可以获得：

```text
地址隔离
权限保护
方便的地址空间管理
```

---

# 73. 内核直接映射

许多现代操作系统会建立某种：

> Direct Mapping

例如：

```text
Kernel Virtual Address
        │
        │ 固定偏移
        ↓
Physical Address
```

可以理解成：

```text
VA = PA + Offset
```

实际实现依架构和操作系统而不同。

这种机制让内核能够比较方便地访问大量物理内存。

---

# 74. 内存管理与上下文切换

进程 A：

```text
Page Table A
```

进程 B：

```text
Page Table B
```

当 CPU 从 A 切换到 B：

```text
Context Switch
      ↓
切换地址空间
      ↓
使用 Page Table B
```

于是：

```text
同一个虚拟地址
```

在不同进程中：

```text
可能映射到不同物理地址
```

这就是进程隔离的重要基础。

---

# 75. ASID / PCID

如果每次进程切换都完全清空 TLB：

```text
Context Switch
      ↓
Flush TLB
```

会产生性能损失。

因此一些 CPU 支持：

```text
ASID
```

或：

```text
PCID
```

用于给不同地址空间打标签。

例如：

```text
TLB Entry

┌─────────────────────┐
│ ASID                │
│ Virtual Page        │
│ Physical Frame      │
└─────────────────────┘
```

这样可以减少频繁刷新 TLB 的需求。

---

# 76. 内存管理与 CPU 架构

OS 内存管理高度依赖 CPU 架构。

例如：

```text
ARM64
x86-64
RISC-V
```

都支持：

```text
MMU
Page Table
TLB
Memory Protection
```

但是具体实现不同。

---

# 77. ARM64 中的内存管理

在 AArch64 中，常见概念包括：

```text
TTBR0_EL1
TTBR1_EL1
TCR_EL1
MAIR_EL1
SCTLR_EL1
```

例如：

```text
TTBR0_EL1
```

通常与某个地址空间的页表基地址相关。

```text
TTBR1_EL1
```

通常用于另一个地址空间区域。

具体地址空间划分由：

```text
TCR_EL1
```

等寄存器配置。

---

# 78. ARM64 页表层级

AArch64 常见页表层级：

```text
L0
 ↓
L1
 ↓
L2
 ↓
L3
 ↓
Page
```

典型：

```text
VA
 │
 ↓
L0
 │
 ↓
L1
 │
 ↓
L2
 │
 ↓
L3
 │
 ↓
Physical Page
```

不同配置下页表级数和地址位划分会有所不同。

---

# 79. x86-64 页表

x86-64 常见页表层级：

```text
PML4
 ↓
PDPT
 ↓
PD
 ↓
PT
 ↓
Page
```

较新的 x86-64 系统还支持：

```text
5-Level Paging
```

因此实际页表层级取决于 CPU 能力和 OS 配置。

---

# 80. OS 内存管理最核心的几个概念

如果刚开始学习 OS 内存管理，不需要一开始把所有东西都学完。

建议先抓住这几个核心概念：

```text
1. Virtual Address
2. Physical Address
3. MMU
4. Page
5. Page Frame
6. Page Table
7. PTE
8. TLB
9. Page Fault
10. Virtual Memory
11. Memory Protection
12. Process Address Space
13. Physical Page Allocator
14. Buddy
15. SLAB / SLUB
16. mmap
17. malloc
18. Copy-on-Write
19. Page Cache
20. Swap
```

---

# 81. 从一个 `malloc()` 理解整个内存管理

例如：

```c
int *p = malloc(4096);
*p = 100;
```

可以从 CPU 到 OS 完整理解。

第一步：

```text
malloc(4096)
```

用户态内存分配器负责：

```text
找到合适的虚拟地址区域
```

得到：

```text
VA
```

然后程序执行：

```c
*p = 100;
```

CPU 发起 Store：

```text
CPU
 ↓
VA
 ↓
TLB
```

如果 TLB Miss：

```text
Page Table
```

如果发现页面不存在：

```text
Page Fault
```

进入：

```text
Kernel
```

内核：

```text
分配 Physical Page
```

可能通过：

```text
Buddy
```

获得物理页面。

然后：

```text
建立：

VA → PA
```

修改：

```text
Page Table
```

返回用户态。

CPU 再次执行：

```text
*p = 100
```

最终：

```text
VA
 ↓
TLB
 ↓
PA
 ↓
Cache
 ↓
DRAM
```

完成数据写入。

这就是：

> 一个简单的用户态内存访问背后的完整 OS 内存管理过程。

---

# 82. 内存管理整体架构

最终可以把整个 OS 内存管理理解成下面这张图：

```text
                         Application
                              │
               ┌──────────────┴──────────────┐
               │                             │
             malloc                         mmap
               │                             │
               └──────────────┬──────────────┘
                              ↓
                     Virtual Address
                              │
                              ↓
                            MMU
                              │
                         ┌────┴────┐
                         │         │
                       TLB       Page Table
                         │         │
                         └────┬────┘
                              ↓
                      Physical Address
                              │
                 ┌────────────┼────────────┐
                 │            │            │
               Cache       Page Cache     DMA
                 │                         │
                 └────────────┬────────────┘
                              ↓
                           DRAM
                              │
                              ↓
                     Physical Page Manager
                              │
                 ┌────────────┼────────────┐
                 │                         │
               Buddy                      SLUB
                 │                         │
                 └────────────┬────────────┘
                              ↓
                       Physical Memory
```

---

# 83. 内存管理可以分成哪几个模块

如果从 OS 内核设计角度划分，可以将内存管理拆成：

```text
OS Memory Management
│
├── 1. Physical Memory Management
│      ├── Page
│      ├── Free List
│      ├── Bitmap
│      ├── Buddy
│      └── NUMA
│
├── 2. Virtual Memory Management
│      ├── Virtual Address Space
│      ├── VMA
│      ├── mmap
│      └── brk
│
├── 3. Page Table Management
│      ├── Page Table
│      ├── PTE
│      ├── Multi-Level Page Table
│      └── TLB
│
├── 4. Page Fault
│      ├── Demand Paging
│      ├── Copy-on-Write
│      └── File Mapping
│
├── 5. Kernel Memory Management
│      ├── kmalloc
│      ├── vmalloc
│      ├── Slab
│      └── SLUB
│
├── 6. Memory Reclaim
│      ├── Page Cache
│      ├── LRU
│      ├── Swap
│      └── Reclaim
│
└── 7. Memory Protection
       ├── User / Kernel
       ├── R/W/X
       ├── NX
       └── Isolation
```

---

# 84. 推荐的学习顺序

如果想系统学习 OS 内存管理，推荐按照下面顺序：

```text
第一阶段：基本概念

物理地址
虚拟地址
地址空间
进程内存布局


        ↓


第二阶段：分页

Page
Page Frame
Page Table
PTE
多级页表


        ↓


第三阶段：硬件

MMU
TLB
Cache
Memory Protection


        ↓


第四阶段：虚拟内存

Page Fault
Demand Paging
Copy-on-Write
mmap


        ↓


第五阶段：物理内存管理

Page Allocator
Free List
Bitmap
Buddy


        ↓


第六阶段：内核内存

kmalloc
vmalloc
Slab
SLUB


        ↓


第七阶段：高级内存

Page Cache
Swap
LRU
NUMA
Huge Page
IOMMU
DMA
Memory Barrier


        ↓


第八阶段：Linux 源码

mm/
mm/memory.c
mm/mmap.c
mm/page_alloc.c
mm/slub.c
mm/vmscan.c
```

---

# 85. 最终总结

OS 内存管理可以用一句话概括：

> **操作系统通过虚拟内存、页表、MMU、TLB 和物理内存分配器，把进程看到的虚拟地址空间安全、高效地映射到真实物理内存。**

整个体系可以浓缩成：

```text
                  Process
                     │
                     ↓
              Virtual Address
                     │
                     ↓
                    MMU
                     │
              ┌──────┴──────┐
              ↓             ↓
             TLB         Page Table
              │             │
              └──────┬──────┘
                     ↓
             Physical Address
                     │
                     ↓
               Physical Page
                     │
              ┌──────┴──────┐
              ↓             ↓
            Buddy          SLUB
              │             │
              └──────┬──────┘
                     ↓
                    RAM
```

从操作系统角度：

```text
进程
 ↓
虚拟地址空间
 ↓
VMA
 ↓
页表
 ↓
虚拟页 → 物理页框
 ↓
MMU / TLB
 ↓
物理内存
```

从硬件角度：

```text
CPU
 ↓
Virtual Address
 ↓
TLB
 ↓
Page Table
 ↓
Physical Address
 ↓
Cache
 ↓
DRAM
```

从内核角度：

```text
Virtual Memory
      │
      ├── mmap / brk
      │
      ↓
Page Fault
      │
      ↓
Physical Page Allocator
      │
      ├── Buddy
      │
      ↓
Physical Page
      │
      ↓
SLUB / Kernel Objects
```

所以，学习 OS 内存管理时，最重要的不是死记各种 API，而是建立下面这条完整的因果链：

```text
为什么需要虚拟地址
        ↓
为什么需要分页
        ↓
虚拟地址如何转换成物理地址
        ↓
页表是什么
        ↓
为什么需要多级页表
        ↓
为什么需要 TLB
        ↓
Page Fault 是怎么产生的
        ↓
OS 如何处理 Page Fault
        ↓
物理页面从哪里来
        ↓
Buddy 如何管理物理页面
        ↓
内核如何管理小对象
        ↓
进程如何实现内存隔离
        ↓
进程之间如何共享内存
        ↓
内存不足时如何回收
        ↓
Swap / Page Cache / NUMA / Huge Page
        ↓
最终形成完整的 OS Memory Management
```

---

# 86. 一张图记住 OS 内存管理

```text
                         ┌─────────────────┐
                         │   Application   │
                         └────────┬────────┘
                                  │
                         malloc / mmap
                                  │
                                  ↓
                       ┌──────────────────┐
                       │ Virtual Address  │
                       └────────┬─────────┘
                                │
                                ↓
                         ┌──────────────┐
                         │     TLB      │
                         └──────┬───────┘
                                │
                       Hit ─────┤
                                │ Miss
                                ↓
                       ┌────────────────┐
                       │   Page Table   │
                       └───────┬────────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                 Present             Not Present
                     │                   │
                     │              Page Fault
                     │                   │
                     │                   ↓
                     │                Kernel
                     │                   │
                     │          ┌────────┴────────┐
                     │          │                 │
                     │       File/Swap        Allocate
                     │          │                 │
                     │          └────────┬────────┘
                     │                   │
                     └──────────┬────────┘
                                ↓
                       ┌──────────────────┐
                       │ Physical Address │
                       └────────┬─────────┘
                                │
                                ↓
                         ┌──────────────┐
                         │    Cache     │
                         └──────┬───────┘
                                │
                                ↓
                         ┌──────────────┐
                         │     DRAM     │
                         └──────────────┘
```

**最终需要建立的核心认识：**

```text
虚拟地址 ≠ 物理地址

页表：
负责建立 VA → PA 映射

MMU：
负责执行地址转换

TLB：
缓存 VA → PA 映射

Page Fault：
处理页面不存在/权限等异常情况

Buddy：
管理物理页面

SLUB：
管理内核小对象

VMA：
描述进程虚拟地址区域

Virtual Memory：
给进程提供独立、连续、受保护的地址空间

Memory Management：
就是把这些机制组合起来，
统一管理 CPU、进程、虚拟地址、物理内存和各种内存资源。
```

# 87. 核心术语速查表

| 术语         | 全称                           | 含义            |
| ---------- | ---------------------------- | ------------- |
| MM         | Memory Management            | 内存管理          |
| VA         | Virtual Address              | 虚拟地址          |
| PA         | Physical Address             | 物理地址          |
| MMU        | Memory Management Unit       | 内存管理单元        |
| Page       | Memory Page                  | 虚拟页           |
| Frame      | Page Frame                   | 物理页框          |
| PT         | Page Table                   | 页表            |
| PTE        | Page Table Entry             | 页表项           |
| TLB        | Translation Lookaside Buffer | 地址转换缓存        |
| PF         | Page Fault                   | 缺页异常          |
| VMA        | Virtual Memory Area          | 虚拟内存区域        |
| COW        | Copy-on-Write                | 写时复制          |
| DMA        | Direct Memory Access         | 直接内存访问        |
| IOMMU      | I/O Memory Management Unit   | I/O 内存管理单元    |
| NUMA       | Non-Uniform Memory Access    | 非统一内存访问       |
| Slab       | Slab Allocator               | 内核对象分配器       |
| SLUB       | Unqueued Slab Allocator      | Linux 常用对象分配器 |
| Buddy      | Buddy System                 | 伙伴内存分配系统      |
| Swap       | Swap Space                   | 交换空间          |
| Huge Page  | Huge Page                    | 大页            |
| Page Cache | Page Cache                   | 文件页缓存         |

---

# 88. 最重要的一句话

如果只记住整个文档中的一句话，可以记住：

> **OS 内存管理的本质，就是利用虚拟地址空间 + 页表 + MMU/TLB + 物理内存分配与回收机制，为每个进程提供一个独立、安全、高效的内存环境。**

而整个学习主线就是：

```text
进程
 ↓
虚拟地址空间
 ↓
分页
 ↓
页表
 ↓
MMU
 ↓
TLB
 ↓
物理内存
 ↓
Buddy
 ↓
SLUB
 ↓
Page Fault
 ↓
内存回收
 ↓
Swap / Page Cache / NUMA / Huge Page / DMA
```

这条主线基本就是**现代操作系统内存管理的骨架**。
