# C/C++ 编译过程之预处理（Preprocessing）

# 1. 什么是预处理

预处理（Preprocessing）是编译器处理源代码的第一步。

作用：

```text
处理以 # 开头的预处理指令
```

例如：

```c
#include
#define
#ifdef
#ifndef
#if
#error
#pragma
```

预处理完成后：

```text
源文件(.c)
↓
预处理器(cpp)
↓
展开后的源码(.i)
```

---

# 2. 编译四阶段

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
main.elf
```

对应 GCC：

```bash
gcc -E main.c -o main.i
gcc -S main.i -o main.s
gcc -c main.s -o main.o
gcc main.o -o main.exe
```

---

# 3. 预处理器做什么

主要完成：

| 功能    | 指令         |
| ----- | ---------- |
| 头文件展开 | #include   |
| 宏替换   | #define    |
| 条件编译  | #if #ifdef |
| 删除注释  | // /* */   |
| 特殊宏替换 | **FILE**   |
| 编译控制  | #pragma    |

---

# 4. #include 展开

源代码：

```c
#include <stdio.h>

int main()
{
    printf("hello");
}
```

预处理后：

```c
// stdio.h 内容

typedef struct FILE FILE;

int printf(const char*,...);

...

int main()
{
    printf("hello");
}
```

实际上：

```text
把头文件内容复制进来
```

---

# 5. 宏替换

代码：

```c
#define MAX 100

int a = MAX;
```

预处理后：

```c
int a = 100;
```

---

# 6. 带参数宏

代码：

```c
#define ADD(a,b) ((a)+(b))

int x = ADD(3,5);
```

展开：

```c
int x = ((3)+(5));
```

---

# 7. 条件编译

代码：

```c
#define DEBUG

#ifdef DEBUG

printf("debug\n");

#endif
```

展开后：

```c
printf("debug\n");
```

如果：

```c
#undef DEBUG
```

则：

```c
/* 删除 */
```

不会出现在最终源码。

---

# 8. 删除注释

源码：

```c
int a = 10; // variable
```

预处理：

```c
int a = 10;
```

---

# 9. 特殊宏

## **FILE**

```c
printf("%s\n",__FILE__);
```

展开：

```c
printf("%s\n","main.c");
```

---

## **LINE**

```c
printf("%d\n",__LINE__);
```

展开：

```c
printf("%d\n",25);
```

---

## **DATE**

```c
printf("%s\n",__DATE__);
```

展开：

```c
printf("%s\n","Jul 15 2026");
```

---

## **TIME**

```c
printf("%s\n",__TIME__);
```

展开：

```c
printf("%s\n","23:58:00");
```

---

# 10. 头文件保护

代码：

```c
#ifndef UART_H

#define UART_H

...

#endif
```

作用：

```text
避免头文件重复包含
```

例如：

```text
main.c
↓
a.h
↓
uart.h
↓
b.h
↓
uart.h
```

第二次包含：

```text
直接跳过
```

避免重复定义错误。

---

# 11. #pragma

例如：

```c
#pragma pack(1)
```

作用：

```text
改变结构体对齐方式
```

例如：

```c
struct Test
{
    char a;
    int b;
};
```

默认：

```text
sizeof = 8
```

使用：

```c
#pragma pack(1)
```

后：

```text
sizeof = 5
```

---

# 12. 查看预处理结果

源文件：

```c
#include <stdio.h>

#define MAX 100

int main()
{
    int a = MAX;

    printf("%d\n",a);
}
```

执行：

```bash
gcc -E main.c -o main.i
```

生成：

```text
main.i
```

查看：

```bash
cat main.i
```

可以看到：

* stdio.h 已展开
* MAX 已替换
* 注释已删除

---

# 13. 为什么需要预处理

主要原因：

## 代码复用

```c
#include "uart.h"
```

不用复制代码。

---

## 配置管理

```c
#define DEBUG
```

切换调试版本。

---

## 跨平台

```c
#ifdef WINDOWS

...

#else

...

#endif
```

支持多个平台。

---

## 自动生成代码

宏：

```c
#define REG(addr) (*(volatile int*)(addr))
```

生成寄存器访问代码。

---

# 14. 嵌入式开发中的典型应用

## 寄存器定义

```c
#define UART0_BASE 0x40000000

#define UART_DR \
    (*(volatile unsigned int*)\
    (UART0_BASE+0x00))
```

使用：

```c
UART_DR = 0x55;
```

预处理后：

```c
(*(volatile unsigned int*)
(0x40000000))
=
0x55;
```

---

## 调试日志

```c
#ifdef DEBUG

printf("error\n");

#endif
```

Release版本：

```text
直接删除
```

零运行开销。

---

# 15. 总结

预处理器本质上是：

```text
文本替换器
```

它不理解：

* 变量
* 函数
* 类型

只负责：

```text
头文件展开

宏替换

条件编译

删除注释
```

最终生成：

```text
.c
↓
.i
↓
.s
↓
.o
↓
.elf
```

预处理阶段最核心的内容：

```c
#include
#define
#ifdef
#ifndef
#pragma
```

掌握这几个指令，就掌握了绝大部分工程项目中的预处理机制。
