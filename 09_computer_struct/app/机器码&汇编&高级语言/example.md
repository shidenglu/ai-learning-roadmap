# 如何阅读汇编代码：从高级语言到CPU指令

# 1. 为什么需要学习看汇编

高级语言：

```c
int c = a + b;
```

表达的是：

```text
程序员的意图
```

而汇编：

```asm
ADD r0,r1,r2
```

表达的是：

```text
CPU真正执行的动作
```

学习汇编的目的不是为了手写大量汇编，而是为了理解：

* 编译器生成了什么代码
* CPU如何执行程序
* 为什么某段代码性能高/低
* 调试优化后的程序
* 分析OS Kernel、驱动、基带算法性能

---

# 2. 一个简单C程序示例

下面代码包含：

* 函数调用
* 局部变量
* 加法运算
* 条件判断

```c
#include <stdio.h>


int add(int a, int b)
{
    return a + b;
}


int main()
{
    int x = 10;
    int y = 20;

    int result = add(x, y);

    if(result > 20)
    {
        result++;
    }

    printf("%d\n", result);

    return 0;
}
```

---

# 3. 程序执行逻辑

先不用看汇编。

程序逻辑：

```text
main()

 |
 |
定义x

x = 10


定义y

y = 20


调用add()

 |
 |
a=10

b=20


返回30


判断:

30 > 20?


成立


result++

31


打印31
```

---

# 4. 编译生成汇编

例如：

ARM Cortex-A64：

编译：

```bash
gcc -S test.c
```

生成：

```text
test.s
```

---

# 5. add函数对应汇编

C代码：

```c
int add(int a,int b)
{
    return a+b;
}
```

对应ARM64汇编：

```asm
add:

    add w0,w0,w1

    ret
```

---

# 6. 如何理解add汇编

## C代码

```c
return a+b;
```

实际上：

```text
a
 |
寄存器w0


b
 |
寄存器w1


相加


结果
 |
寄存器w0
```

---

对应：

```asm
add w0,w0,w1
```

格式：

```text
ADD 目标寄存器, 输入1, 输入2
```

所以：

```asm
add w0,w0,w1
```

等价：

```c
w0 = w0 + w1;
```

---

# 7. main函数汇编

C代码：

```c
int x=10;

int y=20;
```

汇编：

```asm
mov w0,#10

str w0,[sp,#28]


mov w0,#20

str w0,[sp,#24]
```

---

# 8. 分析变量存储

C语言：

```c
int x=10;
```

编译器可能：

放在栈：

```
Stack

+---------+
|   x     |  <- sp+28
+---------+
|   y     |  <- sp+24
+---------+
```

汇编：

```asm
str w0,[sp,#28]
```

含义：

store register

即：

```text
寄存器w0

      ↓

内存地址 sp+28
```

---

# 9. 函数调用分析

C语言：

```c
result = add(x,y);
```

汇编：

```asm
ldr w0,[sp,#28]

ldr w1,[sp,#24]


bl add
```

逐条解释：

---

## 第1行

```asm
ldr w0,[sp,#28]
```

含义：

load register

从：

```text
栈中的x
```

读取：

```text
w0=10
```

---

## 第2行

```asm
ldr w1,[sp,#24]
```

读取：

```text
w1=20
```

---

## 第3行

```asm
bl add
```

Branch Link

作用：

```text
跳转到add函数

同时保存返回地址
```

对应：

```c
add(x,y)
```

---

# 10. 条件判断如何实现

C代码：

```c
if(result>20)
{
    result++;
}
```

CPU没有：

```text
if
```

这种指令。

CPU只有：

* 比较
* 跳转

---

汇编：

```asm
cmp w0,#20

ble end


add w0,w0,#1


end:
```

---

# 11. 对应关系

C：

```c
if(result>20)
```

汇编：

```asm
cmp w0,#20
```

比较：

```text
result - 20
```

---

C：

```c
{
result++;
}
```

汇编：

```asm
add w0,w0,#1
```

---

C：

```c
}
```

汇编：

```asm
end:
```

---

# 12. 汇编阅读核心方法

不要逐字翻译。

按照：

```text
变量
 ↓
寄存器
 ↓
内存
 ↓
指令
 ↓
控制流程
```

分析。

---

# 13. 常见汇编指令对应C语言

| C语言    | ARM汇编        |
| ------ | ------------ |
| a=b    | mov          |
| a=b+c  | add          |
| a=b-c  | sub          |
| a=b*c  | mul          |
| a=b    | ldr          |
| b=a    | str          |
| if     | cmp + branch |
| while  | branch       |
| 函数调用   | bl           |
| return | ret          |

---

# 14. CPU执行角度重新理解程序

C代码：

```c
int c=a+b;
```

程序员看到：

```text
数学计算
```

CPU看到：

```text
读取a

↓

读取b

↓

ALU执行ADD

↓

保存结果c
```

---

# 15. 为什么优化需要看汇编

例如：

C代码：

```c
for(i=0;i<100;i++)
{
    sum+=a[i];
}
```

编译器可能生成：

```asm
loop:

ldr w1,[x0]

add w2,w2,w1

add x0,x0,#4

subs w3,w3,#1

bne loop
```

看到：

每次循环：

* load
* add
* 地址增加
* 判断跳转

可以发现性能瓶颈：

* 内存访问
* 分支
* cache miss

---

# 16. ARM寄存器快速认识

## 通用寄存器

ARM64：

```
x0-x30
```

其中：

| 寄存器   | 用途            |
| ----- | ------------- |
| x0-x7 | 函数参数          |
| x0    | 返回值           |
| sp    | 栈指针           |
| x29   | frame pointer |
| x30   | 返回地址          |

---

# 17. 函数调用约定

C：

```c
add(10,20)
```

实际上：

```
参数1
 |
x0


参数2
 |
x1


调用


bl add


返回值

x0
```

这叫：

```text
ABI(Application Binary Interface)
```

---

# 18. 看汇编的三个层次

## 第一层：看功能

例如：

```asm
add w0,w1,w2
```

知道：

```text
加法
```

---

## 第二层：看数据流

例如：

```asm
ldr w0,[sp,#20]

add w0,w0,#1
```

知道：

```text
从内存取变量

加1

保存结果
```

---

## 第三层：看性能

例如：

```asm
ldr

ldr

mul

str
```

分析：

* cache
* pipeline
* memory latency

---

# 19. 推荐学习路线

## 第一步

掌握：

```
C变量

↓

寄存器

↓

内存
```

---

## 第二步

掌握：

```
函数调用

↓

栈帧

↓

返回地址
```

---

## 第三步

掌握：

```
循环

↓

分支

↓

流水线
```

---

## 第四步

结合：

```
编译优化

↓

-O2/-O3

↓

性能分析
```

---

# 总结

高级语言：

```c
result=a+b;
```

告诉编译器：

```text
我要什么
```

汇编：

```asm
ldr w0,[x]
ldr w1,[y]
add w0,w0,w1
str w0,[result]
```

告诉CPU：

```text
具体怎么做
```

阅读汇编的核心：

```text
C变量
  ↓
寄存器
  ↓
内存
  ↓
指令
  ↓
CPU执行
```

对于嵌入式、OS Kernel、基带芯片开发：

真正重要的是理解：

```
C代码
 ↓
编译器
 ↓
汇编
 ↓
CPU流水线
 ↓
硬件执行
```

这条完整链路。
