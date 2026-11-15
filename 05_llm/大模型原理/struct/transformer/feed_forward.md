# Feed Forward Network（前馈神经网络）

## 1. 什么是 Feed Forward？

Feed Forward Network（FFN，前馈神经网络）是一种信息单向传播的神经网络结构。

在 Transformer 中，FFN 是一个重要组成部分，主要负责对每个 Token 的特征向量进行非线性变换，提取和增强特征表达能力。

它通常由两个全连接层（Linear）和一个激活函数（Activation Function）组成。

**核心作用：**

- 对 Token 的特征进行非线性变换。
- 提升模型的特征表达能力。
- 学习不同特征维度之间的组合关系。

## 2. FFN 在 Transformer 中的位置

Transformer 的一个 Encoder Layer 通常包含两个主要模块：

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
      Feed Forward Network
            |
            v
       Add & Norm
            |
            v
          Output
```

其中：

- Attention：负责学习不同 Token 之间的关联关系。
- FFN：负责对每个 Token 的特征进行独立的非线性变换。

Attention 主要处理 Token 之间的关系，FFN 主要处理 Token 内部的特征。

## 3. FFN 网络结构

标准 Transformer FFN 通常由两个线性层和一个激活函数组成。

```text
              Input
                |
                v
          Linear Layer 1
          (d_model → d_ff)
                |
                v
          Activation
             (ReLU)
                |
                v
          Linear Layer 2
          (d_ff → d_model)
                |
                v
              Output
```

假设：

- `d_model = 512`
- `d_ff = 2048`

那么 FFN 的维度变化为：

```text
Input:  [Batch, Seq_Len, 512]
                |
                v
Linear 1: [Batch, Seq_Len, 2048]
                |
                v
ReLU:     [Batch, Seq_Len, 2048]
                |
                v
Linear 2: [Batch, Seq_Len, 512]
                |
                v
Output:   [Batch, Seq_Len, 512]
```

可以看到，FFN 先将特征维度从 512 扩展到 2048，再压缩回 512。

这种结构也称为 Expansion（扩展）和 Projection（投影）。

## 4. FFN 数学原理

标准 FFN 的数学表达式：

\[
FFN(x)=W_2 \cdot \sigma(W_1x+b_1)+b_2
\]

其中：

| 符号 | 含义 |
|---|---|
| \(x\) | 输入特征向量 |
| \(W_1\) | 第一层权重矩阵 |
| \(b_1\) | 第一层偏置 |
| \(\sigma\) | 激活函数 |
| \(W_2\) | 第二层权重矩阵 |
| \(b_2\) | 第二层偏置 |

假设输入维度为 512，隐藏层维度为 2048：

\[
W_1 \in \mathbb{R}^{512 \times 2048}
\]

\[
W_2 \in \mathbb{R}^{2048 \times 512}
\]

这里采用行向量表示输入的数学约定。

### 4.1 第一层 Linear

输入向量：

\[
x \in \mathbb{R}^{512}
\]

经过第一层线性变换：

\[
h=xW_1+b_1
\]

得到：

\[
h \in \mathbb{R}^{2048}
\]

特征维度从 512 扩展到 2048。

### 4.2 激活函数

经过 ReLU 激活函数：

\[
a=ReLU(h)
\]

其中：

\[
ReLU(x)=\max(0,x)
\]

激活函数引入非线性，使网络能够学习更加复杂的特征关系。

### 4.3 第二层 Linear

经过第二层线性变换：

\[
y=aW_2+b_2
\]

得到：

\[
y \in \mathbb{R}^{512}
\]

最终将特征维度恢复到原始的 512。

## 5. 为什么需要扩展特征维度？

为什么 FFN 不直接使用：

```text
512 → 512
```

而是采用：

```text
512 → 2048 → 512
```

主要原因是增加隐藏层的特征表达能力。

第一层将输入特征映射到更高维度的空间，让模型可以学习更多特征组合。

激活函数进一步引入非线性。

第二层再将高维特征映射回原始维度。

可以理解为：

```text
原始特征
    |
    v
特征扩展
    |
    v
非线性特征变换
    |
    v
特征融合
    |
    v
输出特征
```

注意：扩展维度并不意味着一定产生更多有用信息，而是提供更大的可学习表示空间。

## 6. FFN 如何处理多个 Token？

假设输入句子包含 3 个 Token：

```text
Token 1: I
Token 2: like
Token 3: AI
```

Embedding 和 Attention 处理后，得到：

\[
X \in \mathbb{R}^{3 \times 512}
\]

FFN 对每一个 Token 独立执行相同的网络计算：

```text
Token 1 ──> FFN ──> Output 1

Token 2 ──> FFN ──> Output 2

Token 3 ──> FFN ──> Output 3
```

数学表达式：

\[
Y=FFN(X)
\]

对于每个 Token：

\[
Y_i=FFN(X_i)
\]

这里有两个重要特点：

1. 所有 Token 共享同一组 FFN 权重参数。
2. 不同 Token 之间不会在 FFN 内部直接进行信息交互。

因此，FFN 通常不会改变 Token 数量，只改变每个 Token 的特征表示。

## 7. PyTorch 代码实现

```python
import torch
import torch.nn as nn

class FeedForward(nn.Module):

    def __init__(self, d_model, d_ff):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

    def forward(self, x):
        return self.net(x)


# 参数配置
d_model = 512
d_ff = 2048

# 创建 FFN
ffn = FeedForward(d_model, d_ff)

# 输入：Batch=2，Token数量=3，特征维度=512
x = torch.randn(2, 3, 512)

# 前向传播
y = ffn(x)

print("Input shape:", x.shape)
print("Output shape:", y.shape)
```

输出：

```text
Input shape:  torch.Size([2, 3, 512])
Output shape: torch.Size([2, 3, 512])
```

可以看到：

- Batch 数量保持不变。
- Token 数量保持不变。
- 特征维度经过扩展后又恢复到原始维度。

## 8. FFN 与 Attention 的区别

| 对比项目 | Attention | FFN |
|---|---|---|
| 核心作用 | 学习 Token 之间的关系 | 学习 Token 特征变换 |
| 输入 | 多个 Token | 多个 Token |
| 信息交互 | Token 之间交互 | Token 独立计算 |
| 参数 | Q、K、V 等投影矩阵 | 两个 Linear 层 |
| 主要计算 | 注意力加权 | 线性变换与激活 |
| 输出维度 | 通常为 d_model | 通常为 d_model |

两者相互配合：

- Attention 负责从其他 Token 获取相关信息。
- FFN 负责进一步处理融合后的特征。

## 9. FFN 的其他形式

标准 Transformer FFN 使用 ReLU，但现代 Transformer 也使用其他激活函数。

例如：

### GELU

\[
GELU(x)=x\Phi(x)
\]

GPT、BERT 等模型的不同版本中都可以看到 GELU 的应用。

### SwiGLU

SwiGLU 是一种门控前馈网络结构，常用于现代大语言模型。

其基本形式：

\[
SwiGLU(x)=
(SiLU(xW_1)\odot xW_2)W_3
\]

其中：

- SiLU：激活函数。
- \(\odot\)：逐元素乘法。
- \(W_1,W_2,W_3\)：可学习权重矩阵。

与标准 FFN 相比，SwiGLU 引入门控机制，可以增强特征变换能力。

## 10. 总结

Feed Forward Network 是 Transformer 中负责特征非线性变换的重要模块。

核心结构：

```text
Input
  |
  v
Linear (d_model → d_ff)
  |
  v
Activation
  |
  v
Linear (d_ff → d_model)
  |
  v
Output
```

核心特点：

1. 两个全连接层组成。
2. 中间通过激活函数引入非线性。
3. 先扩展特征维度，再恢复原始维度。
4. 所有 Token 共享 FFN 参数。
5. 每个 Token 独立执行 FFN 计算。

**一句话总结：Attention 负责 Token 之间的信息交互，FFN 负责 Token 内部的特征加工，两者共同构成 Transformer 的核心计算模块。**
