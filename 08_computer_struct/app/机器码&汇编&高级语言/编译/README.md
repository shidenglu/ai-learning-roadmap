# 编译（Compilation）

## 1. 编译阶段概述

编译（Compilation）是编译器将预处理后的 C/C++ 源代码转换成目标平台汇编代码的过程。

在整个构建流程中的位置：

```text
main.c
   │
   ▼
预处理
   │
   ▼
main.i
   │
   ▼
编译
   │
   ▼
main.s
   │
   ▼
汇编
   │
   ▼
main.o
```

对于 GCC：

```bash
gcc -S main.i -o main.s
```

生成：

```text
main.s
```

---

# 2. 编译阶段的输入与输出

## 输入

预处理后的源码：

```text
main.i
```

示例：

```c
int add(int a,int b)
{
    return a+b;
}

int main()
{
    int x = 10;

    int y = add(x,20);

    return y;
}
```

此时：

* 宏已经展开
* 头文件已经展开
* 条件编译已经处理

源码已经变成纯 C 代码。

---

## 输出

目标平台汇编代码：

```text
main.s
```

例如：

```asm
add:
    push rbp
    mov rbp,rsp

    mov eax,edi
    add eax,esi

    pop rbp
    ret
```

---

# 3. 编译器内部架构

编译阶段通常可以划分为：

```text
源代码
   │
   ▼
词法分析
   │
   ▼
语法分析
   │
   ▼
语义分析
   │
   ▼
中间表示(IR)
   │
   ▼
代码优化
   │
   ▼
目标代码生成
   │
   ▼
汇编代码
```

现代编译器：

* GCC
* LLVM
* ARMCC
* Clang

基本都采用类似架构。

---

# 4. 第一部分：词法分析（Lexical Analysis）

## 作用

将字符流转换成 Token（记号）。

源码：

```c
int a = 10;
```

编译器看到的是：

```text
i
n
t

a

=

1
0

;
```

词法分析后：

```text
TOKEN_INT
TOKEN_ID(a)
TOKEN_ASSIGN
TOKEN_NUMBER(10)
TOKEN_SEMICOLON
```

---

## 为什么需要词法分析

便于后续语法处理。

例如：

```c
a = b + c;
```

被拆分为：

```text
ID(a)
=
ID(b)
+
ID(c)
;
```

---

# 5. 第二部分：语法分析（Syntax Analysis）

## 作用

检查代码是否符合语言语法规则。

例如：

```c
int a = 10;
```

生成语法树：

```text
声明语句
├──类型 int
├──变量 a
└──初始值 10
```

---

## AST（抽象语法树）

例如：

```c
a = b + c;
```

构造：

```text
=
├── a
└── +
    ├── b
    └── c
```

称为：

```text
Abstract Syntax Tree
(AST)
```

---

## 语法错误示例

代码：

```c
int a = ;
```

编译器报错：

```text
expected expression before ';'
```

原因：

语法树无法构建。

---

# 6. 第三部分：语义分析（Semantic Analysis）

## 作用

检查代码逻辑是否合法。

---

## 类型检查

代码：

```c
int a;

a = "hello";
```

报错：

```text
incompatible types
```

---

## 变量检查

代码：

```c
a = 10;
```

报错：

```text
undeclared identifier 'a'
```

因为：

```text
变量未定义
```

---

## 函数检查

代码：

```c
result = add(1);
```

函数：

```c
int add(int a,int b);
```

报错：

```text
too few arguments
```

---

## 作用域检查

代码：

```c
{
    int a;
}

a = 10;
```

报错：

```text
a not declared
```

---

# 7. 第四部分：中间表示（IR）

## 什么是 IR

IR：

```text
Intermediate Representation
中间表示
```

是一种介于：

```text
高级语言
        ↓
IR
        ↓
汇编
```

之间的表示形式。

---

## 为什么需要 IR

因为：

```text
C
C++
Rust
Go
```

都可以转换成统一 IR。

然后：

```text
IR
 ↓
ARM

IR
 ↓
x86

IR
 ↓
RISC-V
```

这样可以复用大量编译器代码。

---

## LLVM IR 示例

源码：

```c
a = b + c;
```

IR：

```llvm
%1 = load i32, i32* %b

%2 = load i32, i32* %c

%3 = add i32 %1,%2

store i32 %3, i32* %a
```

---

# 8. 第五部分：代码优化（Optimization）

优化是编译器最复杂的部分之一。

---

## 常量折叠

源码：

```c
int a = 2 + 3;
```

优化后：

```c
int a = 5;
```

---

## 常量传播

源码：

```c
int x = 10;

int y = x + 1;
```

优化：

```c
int y = 11;
```

---

## 死代码删除

源码：

```c
if(0)
{
    func();
}
```

优化：

```text
整个代码块删除
```

---

## 公共子表达式消除

源码：

```c
a = b*c;

d = b*c;
```

优化：

```c
temp = b*c;

a = temp;

d = temp;
```

---

## 循环展开

源码：

```c
for(i=0;i<4;i++)
{
    sum += a[i];
}
```

优化：

```c
sum += a[0];
sum += a[1];
sum += a[2];
sum += a[3];
```

减少循环开销。

---

## 内联优化

源码：

```c
inline int add(int a,int b)
{
    return a+b;
}
```

调用：

```c
x = add(1,2);
```

优化：

```c
x = 1 + 2;
```

不再函数跳转。

---

# 9. 第六部分：目标代码生成（Code Generation）

## 作用

把 IR 转换成目标平台汇编代码。

---

## 示例

源码：

```c
a = b + c;
```

IR：

```text
t1 = load b

t2 = load c

t3 = add t1,t2

store t3 -> a
```

---

生成 ARM 汇编：

```asm
LDR r0,[b]

LDR r1,[c]

ADD r2,r0,r1

STR r2,[a]
```

---

生成 x86 汇编：

```asm
mov eax,[b]

add eax,[c]

mov [a],eax
```

---

## 为什么需要这一阶段

不同 CPU：

```text
ARM
x86
PowerPC
RISC-V
MIPS
```

指令集完全不同。

编译器需要针对目标架构生成对应汇编。

---

# 10. 编译阶段的主要输出

最终生成：

```text
main.s
```

内容包括：

```text
函数实现
汇编指令
标签
跳转
调用关系
```

例如：

```asm
main:
    push rbp

    mov rbp,rsp

    mov DWORD PTR [rbp-4],10

    leave

    ret
```

---

# 11. 编译阶段总结

编译阶段本质上是在完成：

```text
高级语言
     ↓
Token
     ↓
AST
     ↓
语义检查
     ↓
IR
     ↓
优化
     ↓
汇编代码
```

各步骤职责：

| 步骤   | 作用          |
| ---- | ----------- |
| 词法分析 | 代码拆分为 Token |
| 语法分析 | 构建 AST      |
| 语义分析 | 检查逻辑正确性     |
| IR生成 | 构建中间表示      |
| 优化   | 提高运行效率      |
| 代码生成 | 转换为汇编       |

最终得到：

```text
main.i
    ↓
编译器
    ↓
main.s
```

这就是编译阶段的核心工作。
