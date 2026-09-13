# 数值稳定性和权重初始化

## 1. 为什么要学习数值稳定性和权重初始化

随着神经网络层数不断增加，训练过程中会出现两个常见问题：

```text
梯度爆炸（Gradient Explosion）
梯度消失（Gradient Vanishing）
```

这两个问题会导致模型无法正常训练。

例如：

```text
输入层
 ↓
隐藏层1
 ↓
隐藏层2
 ↓
隐藏层3
 ↓
...
 ↓
输出层
```

当网络层数很多时，梯度在反向传播过程中不断相乘：

```text
梯度
 ↓
乘以W
 ↓
乘以W
 ↓
乘以W
 ↓
...
```

如果权重过大：

```text
梯度越来越大
```

产生：

```text
梯度爆炸
```

如果权重过小：

```text
梯度越来越小
```

产生：

```text
梯度消失
```

---

# 2. 梯度爆炸

## 现象

假设：

```math
W = 2
```

网络有10层：

```math
2^{10}=1024
```

网络有50层：

```math
2^{50}
=
1125899906842624
```

梯度迅速增大。

---

训练时表现：

```text
Loss = NaN
参数变成 Inf
训练直接崩溃
```

---

## 示例

```python
import torch

x = torch.tensor(2.0)

for i in range(20):
    x = x * 2

print(x)
```

输出：

```text
1048576
```

继续增加层数会越来越大。

---

# 3. 梯度消失

## 现象

假设：

```math
W=0.1
```

10层：

```math
0.1^{10}
=
0.0000000001
```

50层：

```math
0.1^{50}
≈0
```

---

训练时表现：

```text
Loss不下降
准确率不提高
参数几乎不更新
```

---

## 示例

```python
import torch

x = torch.tensor(1.0)

for i in range(20):
    x = x * 0.1

print(x)
```

输出：

```text
1e-20
```

接近于0。

---

# 4. 梯度爆炸和梯度消失的根源

考虑一个L层神经网络：

```math
y=f_L(...f_2(f_1(x)))
```

根据链式法则：

```math
\frac{\partial L}{\partial W}
=
\frac{\partial L}{\partial h_L}
\frac{\partial h_L}{\partial h_{L-1}}
...
\frac{\partial h_1}{\partial W}
```

实际上是很多项连乘：

```text
a × b × c × d × ...
```

---

如果：

```text
每项 > 1
```

则：

```text
指数增长
```

---

如果：

```text
每项 < 1
```

则：

```text
指数衰减
```

---

# 5. 数值稳定性

数值稳定性：

```text
训练过程中
数值不会无限变大
也不会无限变小
```

---

理想情况：

```text
激活值稳定
梯度稳定
Loss稳定
```

---

# 6. 权重初始化的重要性

如果全部初始化为0：

```python
W = 0
```

会发生：

```text
所有神经元完全相同
```

例如：

```text
神经元1
神经元2
神经元3
```

输出：

```text
完全一样
```

梯度：

```text
完全一样
```

训练后仍然一样。

---

称为：

```text
对称性问题
(Symmetry Problem)
```

---

因此：

```text
权重不能全部初始化为0
```

---

# 7. 随机初始化

最简单方法：

```python
nn.Linear(784,256)
```

PyTorch默认随机初始化。

---

例如：

```python
torch.randn(3,3)
```

输出：

```text
[[ 0.12 -0.23  0.56]
 [ 0.44 -0.08  0.31]
 [-0.66  0.19 -0.42]]
```

每个神经元不同。

---

# 8. Xavier初始化

## 提出者

```text
Xavier Glorot
```

因此也叫：

```text
Glorot Initialization
```

---

## 思想

希望：

```text
输入方差
≈
输出方差
```

保持一致。

---

对于：

```math
n_{in}
```

输入神经元数。

```math
n_{out}
```

输出神经元数。

---

权重服从：

```math
W \sim U\left(-\sqrt{\frac{6}{n_{in}+n_{out}}},\sqrt{\frac{6}{n_{in}+n_{out}}}\right)
```

---

PyTorch：

```python
nn.init.xavier_uniform_(layer.weight)
```

---

# 9. Xavier初始化示例

```python
import torch
from torch import nn

layer = nn.Linear(784,256)

nn.init.xavier_uniform_(
    layer.weight
)
```

---

# 10. Kaiming初始化

## 提出者

微软研究院：

```text
He Kaiming
何恺明
```

因此称：

```text
He Initialization
Kaiming Initialization
```

---

专门针对：

```text
ReLU
```

设计。

---

## 原理

ReLU会丢弃：

```text
约50%的神经元
```

因此需要更大的方差。

---

公式：

```math
Var(W)
=
\frac{2}{n_{in}}
```

---

PyTorch：

```python
nn.init.kaiming_uniform_(
    layer.weight
)
```

---

# 11. Kaiming初始化示例

```python
import torch
from torch import nn

layer = nn.Linear(784,256)

nn.init.kaiming_uniform_(
    layer.weight,
    nonlinearity='relu'
)
```

---

# 12. 常见初始化方法对比

| 方法 | 特点 | 适用 |
|--------|--------|--------|
| 全0初始化 | 不推荐 | 无 |
| 随机初始化 | 简单 | 小模型 |
| Xavier | 保持方差稳定 | Sigmoid/Tanh |
| Kaiming | 专为ReLU设计 | ReLU网络 |
| Orthogonal | 保持正交性 | RNN |
| Normal | 正态分布 | 通用 |

---

# 13. PyTorch中的初始化

## 默认初始化

```python
nn.Linear()
```

自动初始化。

---

## Xavier

```python
nn.init.xavier_uniform_()
```

```python
nn.init.xavier_normal_()
```

---

## Kaiming

```python
nn.init.kaiming_uniform_()
```

```python
nn.init.kaiming_normal_()
```

---

## 常量初始化

```python
nn.init.constant_(
    layer.weight,
    1
)
```

---

# 14. 实际工程经验

目前深度学习工程中：

```text
Sigmoid
↓
Xavier

Tanh
↓
Xavier

ReLU
↓
Kaiming

LeakyReLU
↓
Kaiming
```

最常见组合：

```python
Linear
↓
ReLU
↓
Kaiming
```

---

# 15. 数值稳定性的解决方案

## 梯度裁剪

限制梯度最大值：

```python
torch.nn.utils.clip_grad_norm_(
    model.parameters(),
    max_norm=1.0
)
```

---

## BatchNorm

保持数据分布稳定：

```python
nn.BatchNorm1d()
```

---

## Xavier初始化

防止梯度异常。

---

## Kaiming初始化

适配ReLU网络。

---

## 残差连接（ResNet）

缓解深层网络梯度消失。

---

# 16. 总结

## 梯度爆炸

```text
梯度越来越大
Loss=NaN
```

原因：

```text
权重过大
深层网络连乘
```

---

## 梯度消失

```text
梯度越来越小
参数不更新
```

原因：

```text
权重过小
Sigmoid饱和
深层网络连乘
```

---

## Xavier初始化

适用于：

```text
Sigmoid
Tanh
```

目标：

```text
输入方差≈输出方差
```

---

## Kaiming初始化

适用于：

```text
ReLU
LeakyReLU
```

目标：

```text
保持激活值稳定
```

---

## 一句话总结

> 数值稳定性研究的是深层网络训练过程中梯度爆炸和梯度消失问题，而权重初始化（Xavier、Kaiming）是解决这些问题最重要、最基础的方法之一，它能够让神经网络从训练开始就保持稳定的信号和梯度传播。