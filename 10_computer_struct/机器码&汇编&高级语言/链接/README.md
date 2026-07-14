# 链接（Linking） 

# 1. 链接阶段概述

链接（Linking）是编译流程中的最后一个阶段。

它的作用是：

```text
将多个目标文件(.o)

以及库文件(.a/.so)

组合成一个完整的可执行文件
```

即：

```text
目标文件
      ↓
链接器
      ↓
可执行文件
```

---

# 2. 链接阶段在编译流程中的位置

完整流程：

```text
main.c
  ↓
预处理
  ↓
main.i
  ↓
编译
  ↓
main.s
  ↓
汇编
  ↓
main.o
  ↓
链接
  ↓
main.elf / main.exe
```

---

# 3. 链接阶段输入与输出

## 3.1 输入

链接阶段输入：

### 目标文件

```text
main.o
uart.o
timer.o
```

这些文件由汇编阶段生成。

---

### 静态库

```text
libxxx.a
```

例如：

```text
libc.a
libm.a
```

特点：

```text
编译时复制进入程序
```

---

### 动态库

```text
libxxx.so
```

例如：

```text
libc.so
```

特点：

```text
运行时加载
```

---

### 链接脚本

嵌入式：

```text
xxx.ld
```

Linux：

```text
默认链接脚本
```

用于描述：

* 内存布局
* 段地址
* 程序入口

---

# 4. 输出文件

链接完成后生成：

## Linux

```text
a.out
```

或者：

```text
app
```

---

## Windows

```text
.exe
```

---

## 嵌入式

通常：

```text
firmware.elf
```

然后转换：

```text
firmware.bin
```

用于烧录。

---

# 5. 为什么需要链接

一个大型工程：

```text
main.c

uart.c

gpio.c

timer.c
```

每个文件单独编译：

```text
main.o

uart.o

gpio.o

timer.o
```

但是：

main.o里面：

```c
uart_init();
```

不知道：

```text
uart_init()
在哪里实现
```

所以需要：

```text
链接器(Linker)

寻找定义

建立关系

生成最终程序
```

---

# 6. 链接器（Linker）

负责链接工作的程序：

```text
Linker
```

常见：

| 工具     | 说明       |
| ------ | -------- |
| GNU ld | GNU工具链   |
| gold   | GNU高速链接器 |
| lld    | LLVM链接器  |
| ar     | 静态库管理    |

---

# 7. 链接阶段主要工作

链接器主要完成：

```text
1. 符号解析(Symbol Resolution)

2. 地址分配(Address Allocation)

3. 重定位(Relocation)

4. 段合并(Section Merging)

5. 生成ELF
```

---

# 8. 第一部分：符号解析（Symbol Resolution）

## 8.1 什么是符号

程序中的：

* 函数名
* 全局变量名

称为：

```text
Symbol
```

例如：

```c
int add(int a,int b)
{
    return a+b;
}
```

产生符号：

```text
add
```

---

# 9. 符号引用与定义

假设：

main.c：

```c
extern int add(int,int);


int main()
{
    int x;

    x = add(1,2);

}
```

编译：

```text
main.o
```

里面：

```text
需要:

add
```

---

add.c：

```c
int add(int a,int b)
{
    return a+b;
}
```

生成：

```text
add.o
```

里面：

```text
提供:

add
```

---

链接器：

找到：

```text
main.o

需要add


add.o

提供add
```

建立关系：

```text
main.o
      ↓
add.o
```

---

# 10. 符号表（Symbol Table）

目标文件中包含：

```text
Symbol Table
```

例如：

```text
Name        Type

main        FUNC

add         FUNC

count       OBJECT
```

---

查看：

```bash
nm main.o
```

输出：

```text
U add
```

表示：

```text
Undefined

未定义
```

---

add.o：

```bash
nm add.o
```

输出：

```text
T add
```

表示：

```text
Text段定义
```

---

# 11. 第二部分：地址分配（Address Allocation）

每个目标文件：

都有自己的地址空间。

例如：

main.o:

```text
.text

0x0000
```

add.o:

```text
.text

0x0000
```

---

但是最终程序：

必须统一：

```text
.text

0x10000

.data

0x20000

.bss

0x30000
```

---

链接器负责：

```text
重新安排所有地址
```

---

# 12. 程序段布局

最终ELF：

```text
+----------------+
| ELF Header     |
+----------------+
| .text          |
| 程序代码       |
+----------------+
| .rodata        |
| 常量           |
+----------------+
| .data          |
| 初始化变量     |
+----------------+
| .bss           |
| 未初始化变量   |
+----------------+
| Heap           |
+----------------+
| Stack          |
+----------------+
```

---

# 13. 第三部分：重定位（Relocation）

## 13.1 为什么需要重定位

编译时：

```asm
call add
```

但是：

```text
add地址未知
```

因为：

可能来自：

* 其他.o
* 静态库
* 动态库

---

链接后：

例如：

```text
add地址:

0x10400
```

修改：

```asm
call 0x10400
```

---

# 14. 重定位表（Relocation Table）

目标文件中保存：

```text
Relocation Section
```

记录：

```text
需要修改的位置

修改方式

目标符号
```

例如：

```text
offset:

0x20

symbol:

add
```

---

# 15. 第四部分：段合并（Section Merge）

多个.o：

```text
main.o

.text

.data


uart.o

.text

.data
```

链接：

合并：

```text
最终:

.text

main代码

uart代码


.data

所有变量
```

---

# 16. 静态链接（Static Linking）

## 原理

把库代码复制到最终程序。

例如：

```text
main.o
+
libc.a
↓
app
```

---

## 特点

优点：

* 不依赖外部库
* 运行稳定
* 启动快

缺点：

* 文件大
* 内存浪费

---

# 17. 动态链接（Dynamic Linking）

## 原理

程序运行时加载库。

例如：

```text
app
↓
libc.so
```

---

## 特点

优点：

* 文件小
* 多程序共享库
* 节省内存

缺点：

* 依赖运行环境
* 加载稍慢

---

# 18. 嵌入式中的链接

嵌入式链接与PC最大区别：

需要控制：

```text
代码放哪里

数据放哪里

RAM使用多少

Flash使用多少
```

---

# 19. 链接脚本（Linker Script）

文件：

```text
xxx.ld
```

例如：

```ld
MEMORY
{
 FLASH : ORIGIN = 0x08000000
 RAM   : ORIGIN = 0x20000000
}


SECTIONS
{

.text :
{
    *(.text)
}


.data :
{
    *(.data)
}

}
```

---

作用：

指定：

```text
.text → Flash

.data → RAM

.bss → RAM
```

---

# 20. ARM启动过程中的链接

典型：

源码：

```text
start.S

main.c

uart.c
```

生成：

```text
start.o

main.o

uart.o
```

链接：

```text
linker

+

xxx.ld
```

生成：

```text
firmware.elf
```

转换：

```text
objcopy

↓

firmware.bin
```

烧录：

```text
Flash
```

---

# 21. ELF文件中的关键内容

链接生成：

```text
firmware.elf
```

包含：

## Program Header

描述：

```text
加载信息
```

---

## Section Header

描述：

```text
代码段
数据段
符号
```

---

## Symbol Table

保存：

```text
函数地址

变量地址
```

---

## Relocation

保存：

```text
地址修正信息
```

---

# 22. 查看链接结果

## 查看ELF信息

```bash
readelf -h firmware.elf
```

---

## 查看段信息

```bash
readelf -S firmware.elf
```

---

## 查看符号

```bash
nm firmware.elf
```

---

## 查看内存布局

```bash
objdump -h firmware.elf
```

---

# 23. 链接阶段总结

链接器完成：

```text
.o文件
      ↓
符号解析
      ↓
地址分配
      ↓
重定位
      ↓
段合并
      ↓
生成ELF
```

核心任务：

| 功能    | 作用        |
| ----- | --------- |
| 符号解析  | 找到函数和变量定义 |
| 地址分配  | 确定最终运行地址  |
| 重定位   | 修正跳转和访问地址 |
| 段合并   | 组合代码和数据   |
| 生成ELF | 产生最终程序    |

---

# 24. 四阶段最终总结

```text
.c
↓
预处理
↓
.i
↓
编译
↓
.s
↓
汇编
↓
.o
↓
链接
↓
.elf
```

其中：

* **预处理**：处理源码文本
* **编译**：理解代码并生成汇编
* **汇编**：生成机器指令
* **链接**：组织整个程序，让所有模块成为一个完整系统

对于嵌入式系统：

```text
链接阶段 = 决定程序最终如何放入CPU内存
```

因此：

* Linker Script
* ELF
* Symbol
* Relocation

是理解 BootLoader、RTOS、Linux Kernel 构建流程的核心。
