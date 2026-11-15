# Normalization（归一化）

## 1. 什么是 Normalization？

Normalization（归一化）是一种用于调整数据分布的技术，主要目的是让神经网络的训练过程更加稳定。

在 Transformer 中，Normalization 通常指 Layer Normalization（LayerNorm）。

它的主要作用是：

- 调整特征的数值分布。
- 稳定网络训练过程。
- 改善梯度传播。
- 减少不同层之间特征数值变化带来的影响。

简单理解：

**Normalization 通过对神经网络中的特征进行标准化处理，让特征保持相对稳定的数值分布。**

## 2. Norm 在 Transformer 中的位置

Transformer 的 Encoder Layer 通常包含 Attention、FFN 和 Norm。

以经典 Post-LN 结构为例：

```text
             Input
               |
               v
       Multi-Head Attention
               |
               v
          Add & Norm
               |
               v
        Feed Forward
               |
               v
          Add & Norm
               |
               v
             Output
```

其中：

- Attention：负责 Token 之间的信息交互。
- FFN：负责 Token 特征的非线性变换。
- Norm：负责调整特征分布，稳定训练。

注意：不同 Transformer 架构的 Norm 位置可能不同，常见的还有 Pre-LN。

## 3. LayerNorm 的基本原理

LayerNorm（层归一化）是 Transformer 中最常见的归一化方式之一。

它的核心思想是：

**针对每个 Token 的特征维度，计算均值和方差，再对特征进行标准化。**

假设一个 Token 的特征向量为：

\[
X=[x_1,x_2,x_3,x_4]
\]

### 3.1 计算均值

首先计算当前 Token 所有特征的平均值：

\[
\mu=\frac{1}{N}\sum_{i=1}^{N}x_i
\]

其中：

- N：特征维度。
- \(x_i\)：第 i 个特征值。
- \(\mu\)：特征均值。

### 3.2 计算方差

计算每个特征与均值之间的偏差平方，再求平均：

\[
\sigma^2=
\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2
\]

### 3.3 标准化

使用均值和方差对特征进行标准化：

\[
\hat{x}_i=
\frac{x_i-\mu}{\sqrt{\sigma^2+\epsilon}}
\]

其中：

- \(\hat{x}_i\)：标准化后的特征。
- \(\epsilon\)：防止分母为零的极小常数。

经过这一步，特征的均值接近 0，方差接近 1。

### 3.4 缩放和偏移

LayerNorm 还包含两个可学习参数：

- \(\gamma\)：缩放参数。
- \(\beta\)：偏移参数。

最终计算：

\[
y_i=\gamma_i\hat{x}_i+\beta_i
\]

完整公式：

\[
\boxed{
LayerNorm(x)=
\gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta
}
\]

其中 \(\gamma\) 和 \(\beta\) 可以通过反向传播进行训练。

这样做可以让模型在标准化之后，仍然具有调整特征分布的能力。

## 4. LayerNorm 维度计算

假设 Transformer 输入：

\[
X\in\mathbb{R}^{Batch\times Seq\_Len\times d_{model}}
\]

例如：

\[
X\in\mathbb{R}^{2\times4\times512}
\]

表示：

- Batch = 2
- Token 数量 = 4
- 每个 Token 的特征维度 = 512

LayerNorm 通常设置：

```python
nn.LayerNorm(512)
```

它会对每个 Token 的 512 个特征分别计算均值和方差。

例如：

```text
Batch 1:

Token 1 → 对 512 个特征进行 Norm
Token 2 → 对 512 个特征进行 Norm
Token 3 → 对 512 个特征进行 Norm
Token 4 → 对 512 个特征进行 Norm

Batch 2:

Token 1 → 对 512 个特征进行 Norm
Token 2 → 对 512 个特征进行 Norm
Token 3 → 对 512 个特征进行 Norm
Token 4 → 对 512 个特征进行 Norm
```

注意：

**LayerNorm 不会改变输入张量的形状，只会调整特征数值。**

输入：

\[
[2,4,512]
\]

输出：

\[
[2,4,512]
\]

## 5. PyTorch 实现 LayerNorm

使用 PyTorch 可以直接调用：

```python
import torch
import torch.nn as nn

# 创建 LayerNorm
norm = nn.LayerNorm(512)

# 输入数据
x = torch.randn(2, 4, 512)

# 前向传播
y = norm(x)

print("Input shape:", x.shape)
print("Output shape:", y.shape)
```

输出：

```text
Input shape: torch.Size([2, 4, 512])
Output shape: torch.Size([2, 4, 512])
```

### 5.1 手动实现 LayerNorm

下面使用 PyTorch 基础运算实现 LayerNorm：

```python
import torch
import torch.nn as nn

class LayerNorm(nn.Module):

    def __init__(self, dim, eps=1e-5):
        super().__init__()

        self.gamma = nn.Parameter(torch.ones(dim))
        self.beta = nn.Parameter(torch.zeros(dim))

        self.eps = eps

    def forward(self, x):

        # 计算均值
        mean = x.mean(dim=-1, keepdim=True)

        # 计算方差
        var = x.var(
            dim=-1,
            unbiased=False,
            keepdim=True
        )

        # 标准化
        x_norm = (x - mean) / torch.sqrt(var + self.eps)

        # 缩放和偏移
        return self.gamma * x_norm + self.beta


# 测试
x = torch.randn(2, 4, 512)

norm = LayerNorm(512)

y = norm(x)

print(y.shape)
```

这里：

- `dim=-1`：表示对最后一个维度进行归一化。
- `keepdim=True`：保留维度，方便广播计算。
- `gamma`：可学习缩放参数。
- `beta`：可学习偏移参数。

## 6. BatchNorm 和 LayerNorm 的区别

Normalization 有多种实现方式，其中常见的是 BatchNorm 和 LayerNorm。

### 6.1 BatchNorm

BatchNorm（批归一化）主要针对一个 Batch 中同一特征维度的数据计算均值和方差。

例如输入：

\[
X\in\mathbb{R}^{Batch\times Channel\times H\times W}
\]

BatchNorm 通常针对每个 Channel，在 Batch、H、W 这些维度上计算统计量。

常用于 CNN 等网络结构。

### 6.2 LayerNorm

LayerNorm 通常针对每个样本或 Token 的特征维度独立计算均值和方差。

在 Transformer 中：

\[
X\in\mathbb{R}^{Batch\times Seq\_Len\times d_{model}}
\]

LayerNorm 对最后一个特征维度进行归一化。

### 6.3 两者对比

| 对比项目 | BatchNorm | LayerNorm |
|---|---|---|
| 归一化维度 | Batch 等统计维度 | 特征维度 |
| 是否依赖 Batch 大小 | 是 | 否 |
| 是否使用运行均值 | 通常使用 | 不需要 |
| 常见应用 | CNN | Transformer |
| 输入输出形状 | 不变 | 不变 |

## 7. RMSNorm

RMSNorm（Root Mean Square Normalization）是一种简化的归一化方法。

它与 LayerNorm 的主要区别是：

**RMSNorm 不计算均值，只计算特征的均方根。**

计算公式：

\[
RMS(x)=
\sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2+\epsilon}
\]

归一化：

\[
\boxed{
RMSNorm(x)=
\gamma\frac{x}{RMS(x)}
}
\]

其中：

- N：特征维度。
- \(\gamma\)：可学习缩放参数。
- \(\epsilon\)：数值稳定项。

RMSNorm 不包含 LayerNorm 中的均值减法和偏移参数 \(\beta\)。

### LayerNorm 与 RMSNorm 对比

| 对比项目 | LayerNorm | RMSNorm |
|---|---|---|
| 计算均值 | 是 | 否 |
| 计算方差 | 是 | 否 |
| 计算均方根 | 否 | 是 |
| 缩放参数 | 有 | 有 |
| 偏移参数 | 通常有 | 通常没有 |
| 计算复杂度 | 相对较高 | 相对较低 |

RMSNorm 被许多现代大语言模型采用，例如 LLaMA 系列。

## 8. Pre-LN 和 Post-LN

除了归一化方式，Transformer 中 Norm 的位置也很重要。

### 8.1 Post-LN

经典 Transformer 采用 Post-LN 结构：

\[
Y=LayerNorm(X+Attention(X))
\]

\[
Z=LayerNorm(Y+FFN(Y))
\]

结构：

```text
Input
  |
  v
Attention
  |
  v
Add Residual
  |
  v
LayerNorm
  |
  v
FFN
  |
  v
Add Residual
  |
  v
LayerNorm
  |
  v
Output
```

### 8.2 Pre-LN

Pre-LN 将 Norm 放在 Attention 和 FFN 之前：

\[
Y=X+Attention(LayerNorm(X))
\]

\[
Z=Y+FFN(LayerNorm(Y))
\]

结构：

```text
Input
  |
  +----------------------+
  |                      |
  v                      |
LayerNorm                |
  |                      |
  v                      |
Attention                |
  |                      |
  +------ Add <----------+
           |
           v
           Y
           |
           +----------------------+
           |                      |
           v                      |
       LayerNorm                  |
           |                      |
           v                      |
          FFN                     |
           |                      |
           +------ Add <----------+
                      |
                      v
                    Output
```

### 8.3 Pre-LN 和 Post-LN 对比

| 对比项目 | Pre-LN | Post-LN |
|---|---|---|
| Norm 位置 | 子层之前 | 残差相加之后 |
| 残差路径 | 更直接 | 经过 Norm |
| 深层训练 | 通常更稳定 | 可能更难训练 |
| 常见应用 | 现代 Transformer | 原始 Transformer |

## 9. Norm 在 Transformer 中的作用总结

Transformer 中的 Attention 和 FFN 都包含大量线性变换。

随着网络层数增加，特征数值可能发生较大变化。

Norm 主要用于稳定特征分布，改善训练过程。

它的作用可以概括为：

1. 对特征进行标准化。
2. 通过可学习参数调整特征分布。
3. 改善深层网络的训练稳定性。
4. 配合残差连接，帮助构建深层 Transformer。

## 10. 总结

Normalization 是 Transformer 中重要的基础模块。

常见类型：

| 类型 | 核心特点 |
|---|---|
| BatchNorm | 对 Batch 等维度进行统计归一化 |
| LayerNorm | 对单个 Token 的特征维度进行归一化 |
| RMSNorm | 使用均方根进行归一化，不减均值 |

核心公式：

**LayerNorm：**

\[
y=\gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta
\]

**RMSNorm：**

\[
y=\gamma\frac{x}{\sqrt{\frac{1}{N}\sum x_i^2+\epsilon}}
\]

一句话总结：

**Norm 负责调整神经网络中的特征分布，让模型训练更加稳定；Attention 负责信息交互，FFN 负责特征变换，Residual 负责提供直接的信息传递路径。**
