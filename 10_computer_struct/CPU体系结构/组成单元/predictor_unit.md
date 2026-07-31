# 分支预测单元（Branch Prediction Unit）详解

## 目录

- 什么是分支预测单元
- 为什么需要分支预测
- 分支指令带来的问题
- 分支预测的工作原理
- 静态分支预测
- 动态分支预测
- BTB（Branch Target Buffer）
- BHT（Branch History Table）
- 两位饱和计数器
- 现代CPU中的分支预测
- 分支预测失败的代价
- 分支预测与流水线
- ARM与x86中的分支预测
- 总结

---

# 1. 什么是分支预测单元

分支预测单元（Branch Prediction Unit，BPU）是现代CPU中的一个重要模块。

其作用是：

```text
提前猜测程序接下来会执行哪条指令
```

从而避免CPU流水线停顿。

---

CPU执行流程：

```text
取指(Fetch)
    ↓
译码(Decode)
    ↓
执行(Execute)
```

当遇到：

```c
if (a > b)
{
    ...
}
else
{
    ...
}
```

CPU必须决定：

```text
下一条指令在哪？
```

此时：

```text
分支预测单元
```

提前给出答案。

---

# 2. 为什么需要分支预测

现代CPU采用流水线技术。

例如：

```text
第1周期：取指

第2周期：译码

第3周期：执行
```

---

理想情况下：

```text
周期1：指令A(Fetch)

周期2：指令A(Decode)
       指令B(Fetch)

周期3：指令A(Execute)
       指令B(Decode)
       指令C(Fetch)
```

流水线始终满载。

---

但是遇到：

```asm
CMP X0,#0

BEQ LABEL
```

CPU不知道：

```text
是否跳转？
```

必须等待执行结果。

---

导致：

```text
流水线停顿
```

性能下降。

---

# 3. 分支指令带来的问题

例如：

```c
if (x > 0)
{
    y = 1;
}
else
{
    y = 2;
}
```

编译后：

```asm
CMP X0,#0

BLE ELSE

MOV X1,#1

B END

ELSE:
MOV X1,#2
```

---

CPU执行到：

```asm
BLE ELSE
```

时不知道：

```text
跳转？

还是继续向下执行？
```

---

于是：

```text
取指单元无法确定下一条指令地址
```

流水线可能空转。

---

# 4. 分支预测的工作原理

CPU采用：

```text
猜测
```

机制。

例如：

```asm
BEQ LABEL
```

CPU直接猜：

```text
大概率会跳转
```

然后：

```text
提前取 LABEL 地址的指令
```

---

如果猜对：

```text
流水线继续运行
```

没有损失。

---

如果猜错：

```text
清空流水线
重新取指
```

产生性能损失。

---

# 5. 静态分支预测

最简单的方法。

---

## 方法1

永远预测：

```text
不跳转
```

---

## 方法2

永远预测：

```text
跳转
```

---

## 方法3

根据方向预测

```text
向后跳转
预测跳转

向前跳转
预测不跳转
```

因为：

```text
循环通常向后跳转
```

例如：

```c
for(i=0;i<100;i++)
```

大部分时间都会继续循环。

---

# 6. 动态分支预测

现代CPU主要采用：

```text
动态预测
```

根据历史行为学习。

---

例如：

```c
for(i=0;i<1000;i++)
```

执行过程：

```text
T
T
T
T
T
T
...
N
```

T = Taken（跳转）

N = Not Taken（不跳转）

---

CPU发现：

```text
这条分支几乎总是跳转
```

以后直接预测：

```text
Taken
```

---

# 7. BHT（Branch History Table）

Branch History Table

分支历史表。

记录：

```text
过去是否跳转
```

---

例如：

| 分支地址 | 历史 |
|-----------|--------|
|0x1000|T|
|0x2000|N|
|0x3000|T|

---

下次执行：

```text
直接参考历史
```

进行预测。

---

# 8. BTB（Branch Target Buffer）

Branch Target Buffer

分支目标缓冲区。

---

不仅预测：

```text
是否跳转
```

还预测：

```text
跳到哪里
```

---

例如：

```asm
B LOOP
```

BTB记录：

```text
PC=0x1000

Target=0x2000
```

---

下次：

```text
直接从0x2000开始取指
```

无需等待计算结果。

---

# 9. 两位饱和计数器

现代CPU经典算法。

---

状态：

```text
00 强不跳转

01 弱不跳转

10 弱跳转

11 强跳转
```

---

状态机：

```text
          Taken
      ┌─────────────┐
      ▼             │

00 ←→ 01 ←→ 10 ←→ 11

      ▲             │
      └─────────────┘

        Not Taken
```

---

特点：

```text
偶尔一次错误
不会立刻改变预测
```

提高稳定性。

---

# 10. 现代CPU中的分支预测

现代CPU采用：

```text
多级预测器
```

例如：

```text
BHT

BTB

Global History

Local History

TAGE Predictor

Neural Predictor
```

共同工作。

---

预测准确率通常：

```text
95%~99%以上
```

---

# 11. 分支预测失败的代价

假设：

```text
20级流水线
```

预测错误：

```text
流水线全部清空
```

---

需要：

```text
重新取指

重新译码

重新执行
```

---

损失：

```text
10~30个CPU周期
```

甚至更多。

---

因此：

```text
预测失败
=
严重性能损失
```

---

# 12. 分支预测与流水线

无预测：

```text
CMP
↓
等待结果
↓
决定跳转
↓
继续执行
```

---

有预测：

```text
CMP
↓
预测结果
↓
提前取指
↓
流水线不停顿
```

---

因此：

```text
分支预测
=
提高流水线利用率
```

---

# 13. ARM中的分支预测

AArch64处理器：

```text
Cortex-A53

Cortex-A72

Cortex-A76

Neoverse
```

都拥有：

```text
BPU
```

---

工作流程：

```text
PC
↓
BTB查询
↓
预测跳转地址
↓
Fetch
```

---

# 14. x86中的分支预测

Intel Core

AMD Zen

都拥有极其复杂的预测器。

例如：

```text
BTB

L0 BTB

L1 BTB

L2 BTB

TAGE Predictor
```

---

预测准确率：

```text
接近99%
```

---

因此：

```text
现代CPU每秒可执行数十亿条指令
```

而不会频繁停顿。

---

# 15. 分支预测失败示例

代码：

```c
if(rand()%2)
{
    ...
}
```

结果：

```text
跳转概率≈50%
```

---

CPU无法学习规律。

预测准确率：

```text
≈50%
```

---

导致：

```text
频繁刷流水线
```

性能下降。

---

# 16. 操作系统中的体现

操作系统代码：

```c
if(likely(ptr != NULL))
{
    ...
}
```

Linux内核常见：

```c
likely()

unlikely()
```

---

作用：

```text
帮助CPU提高预测准确率
```

例如：

```c
if (likely(success))
```

表示：

```text
大概率进入该分支
```

---

# 17. 分支预测单元在CPU中的位置

```text
                    Program Counter
                           │
                           ▼
                ┌─────────────────┐
                │ Branch Predictor│
                └───────┬─────────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼

       Predict Taken         Predict Not Taken

             │
             ▼

          Fetch Unit
             │
             ▼

          Decoder
             │
             ▼

         Execute Unit
```

---

# 18. 总结

## 分支预测单元的核心作用

```text
预测程序下一步执行路径
```

---

## 工作流程

```text
分支指令
      ↓
Branch Predictor
      ↓
预测结果
      ↓
提前取指
      ↓
继续流水线执行
```

---

## 关键组成

| 模块 | 作用 |
|--------|--------|
| BHT | 记录历史行为 |
| BTB | 记录目标地址 |
| Predictor | 预测是否跳转 |
| Global History | 全局历史记录 |
| Local History | 局部历史记录 |

---

## 一句话理解

```text
分支预测单元（BPU）
是CPU中的“预言家”。

它根据历史执行情况，
提前猜测程序下一步会走哪条路径，
从而让流水线持续满载运行，
大幅提高CPU性能。
```

---

## CPU执行流程中的位置

```text
PC
 ↓
Branch Predictor
 ↓
Fetch
 ↓
Decode
 ↓
Execute
 ↓
Write Back
```

现代高性能CPU（ARM Cortex-A、Apple M系列、Intel Core、AMD Zen）都高度依赖分支预测技术，其准确率往往超过95%，是CPU性能提升的重要来源之一。