# 模型初始化（Model Initialization）详解

## 1. 什么是模型初始化

模型初始化（Model Initialization）是指：

> 在模型开始训练之前，为模型中的参数（权重 Weight 和偏置 Bias）赋予初始值的过程。

例如：

```python
import torch.nn as nn

model = nn.Linear(3, 1)
```

当执行这行代码时：

```python
nn.Linear(3, 1)
```

PyTorch 会自动生成：

```text
W = [[0.12, -0.31, 0.56]]
b = [0.08]
```

这些随机生成的参数就是模型的初始参数。

---

## 2. 为什么需要初始化

训练神经网络的过程本质上是：

```text
不断修改参数
↓
让损失函数越来越小
↓
找到最优参数
```

例如：

```text
真实关系：

y = 2x + 3
```

模型一开始并不知道：

```text
w = 2
b = 3
```

因此需要先随机给一个值：

```text
w = 0.4
b = -0.8
```

然后通过梯度下降不断更新：

```text
w = 0.4
↓
0.9
↓
1.5
↓
1.9
↓
2.0
```

最终逼近真实值。

---

# 3. 模型训练流程

完整流程如下：

```text
创建模型
    ↓
参数初始化
    ↓
输入数据
    ↓
前向传播
    ↓
计算损失
    ↓
反向传播
    ↓
更新参数
    ↓
重复迭代
```

其中：

```text
参数初始化
```

就是整个训练流程的起点。

---

# 4. 模型里有哪些参数需要初始化

以全连接层为例：

```python
nn.Linear(784, 10)
```

内部包含：

```text
Weight
Bias
```

数学表达式：

y = Wx + b

其中：

```text
W：权重矩阵
b：偏置向量
```

例如：

```text
输入层: 784
输出层: 10
```

则：

```text
W.shape = (10, 784)

b.shape = (10,)
```

需要初始化的就是：

```text
W
b
```

---

# 5. 最简单的初始化方式

## 全零初始化

```python
nn.init.zeros_(layer.weight)
nn.init.zeros_(layer.bias)
```

结果：

```text
W =

[0 0 0]
[0 0 0]
[0 0 0]
```

---

## 为什么不能全部初始化为 0

假设：

```text
输入层 2 个神经元

隐藏层 3 个神经元
```

权重：

```text
W =
[0 0]
[0 0]
[0 0]
```

前向传播：

```text
输出全部相同
```

反向传播：

```text
梯度全部相同
```

更新后：

```text
参数仍然完全相同
```

导致：

```text
所有神经元学到一样的东西
```

这叫：

```text
对称性问题（Symmetry Problem）
```

因此：

```text
不能全部初始化为0
```

---

# 6. 随机初始化

最常见的方法：

```python
nn.init.normal_(layer.weight)
```

例如：

```text
0.15
-0.33
0.41
0.06
```

每个神经元的参数都不同。

这样：

```text
神经元学习不同特征
```

网络才有表达能力。

---

# 7. 正态分布初始化

## 定义

从高斯分布中随机采样：

```text
N(μ, σ²)
```

例如：

```python
nn.init.normal_(
    layer.weight,
    mean=0,
    std=0.01
)
```

生成：

```text
0.005
-0.008
0.011
0.003
```

图像：

```text
            *
         * * *
      * * * * *
    * * * * * * *
      * * * * *
         * * *
            *
```

大多数值接近：

```text
0
```

---

# 8. 均匀分布初始化

## 定义

在指定区间内均匀随机取值。

```python
nn.init.uniform_(
    layer.weight,
    a=-0.1,
    b=0.1
)
```

例如：

```text
0.03
-0.08
0.06
0.01
```

分布：

```text
-0.1 ---------------- 0.1
```

任何位置出现概率相同。

---

# 9. Xavier 初始化

## 为什么出现 Xavier

深层网络中：

```text
输入
 ↓
隐藏层1
 ↓
隐藏层2
 ↓
隐藏层3
 ↓
...
```

如果权重太大：

```text
信号越来越大
```

产生：

```text
梯度爆炸
```

如果权重太小：

```text
信号越来越小
```

产生：

```text
梯度消失
```

---

## Xavier思想

保持：

```text
每层输入方差
≈
每层输出方差
```

---

公式：

[
Var(W)=\frac{2}{n_{in}+n_{out}}
]

其中：

```text
n_in  输入神经元数

n_out 输出神经元数
```

---

PyTorch实现：

```python
nn.init.xavier_uniform_(layer.weight)
```

或者：

```python
nn.init.xavier_normal_(layer.weight)
```

---

## 适用于

```text
Sigmoid

Tanh
```

激活函数。

---

# 10. He初始化

## 背景

ReLU 出现后：

```text
Xavier 不再最优
```

因为：

```text
ReLU会把负数变成0
```

导致：

```text
方差减半
```

---

## He初始化公式

$Var(W)=\frac{2}{n_{in}}$

---

PyTorch：

```python
nn.init.kaiming_normal_(layer.weight)
```

或者：

```python
nn.init.kaiming_uniform_(layer.weight)
```

---

## 适用于

```text
ReLU

LeakyReLU

GELU
```

现代神经网络最常用。

---

# 11. 不同初始化方法比较

| 方法          | 是否推荐  | 适用场景         |
| ----------- | ----- | ------------ |
| 全零初始化       | ❌     | 几乎不用         |
| 随机初始化       | ⭐     | 小模型          |
| 正态分布        | ⭐⭐    | 一般情况         |
| 均匀分布        | ⭐⭐    | 一般情况         |
| Xavier      | ⭐⭐⭐⭐  | Sigmoid/Tanh |
| He(Kaiming) | ⭐⭐⭐⭐⭐ | ReLU网络       |

---

# 12. PyTorch查看初始化结果

```python
import torch
from torch import nn

layer = nn.Linear(4, 3)

print(layer.weight)
print(layer.bias)
```

输出：

```text
Parameter containing:
tensor([[ 0.25, -0.43, 0.17, 0.28],
        [-0.34, 0.11, 0.39,-0.07],
        [ 0.16, 0.44,-0.28, 0.05]])
```

---

# 13. 自定义初始化

```python
def init_weights(m):

    if type(m) == nn.Linear:

        nn.init.xavier_uniform_(m.weight)

        nn.init.zeros_(m.bias)

model.apply(init_weights)
```

执行后：

```text
所有 Linear 层
↓
使用 Xavier 初始化
↓
Bias = 0
```

---

# 14. 实际项目推荐

## 线性回归

```python
nn.init.normal_(weight, std=0.01)
```

---

## MLP

```python
nn.init.kaiming_normal_(weight)
```

---

## CNN

```python
nn.init.kaiming_normal_(weight)
```

---

## ResNet

```python
nn.init.kaiming_normal_(weight)
```

---

## Transformer

```python
nn.init.xavier_uniform_(weight)
```

---

# 15. 总结

模型初始化的本质：

```text
给模型参数一个合理的起点
```

训练过程：

```text
随机初始化参数
        ↓
前向传播
        ↓
计算损失
        ↓
反向传播
        ↓
更新参数
        ↓
不断逼近最优解
```

常见初始化方案：

```text
全零初始化        ❌

随机初始化        ⭐

Xavier初始化     ⭐⭐⭐⭐

He初始化         ⭐⭐⭐⭐⭐
```

对于现代深度学习：

```text
ReLU网络
    ↓
He(Kaiming)初始化
```

几乎已经成为默认选择。
