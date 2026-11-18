# Attention 基础（注意力机制）

## 1. Attention 是什么？

Attention（注意力机制）是一种让神经网络根据当前任务需求，动态关注输入信息中重要部分的机制。

在传统神经网络中，模型通常按照固定方式处理输入数据，而 Attention 可以根据不同的输入内容，为不同的信息分配不同的权重。

**核心思想：重点关注重要信息，降低无关信息的影响。**

例如，在机器翻译任务中：

输入：

```text
I love deep learning
```

当模型需要翻译 `learning` 时，可以重点关注 `deep`，同时参考其他单词，从而更好地理解当前单词的语义。

## 2. 为什么需要 Attention？

在 Attention 出现之前，序列任务通常使用 RNN、LSTM 等循环神经网络。

传统 Seq2Seq 模型存在一个问题：

Encoder 将整个输入序列压缩成一个固定长度的上下文向量，再交给 Decoder 生成输出。

这种方式存在以下不足：

1. 输入序列较长时，固定长度向量难以保留全部信息。
2. 早期输入的信息容易在传递过程中丢失。
3. Decoder 无法直接访问 Encoder 的所有隐藏状态。
4. 模型难以针对当前生成内容动态选择相关信息。

Attention 通过建立输入与输出之间的动态关联，改善了这些问题。

## 3. Attention 的核心思想

Attention 的计算可以抽象为三个步骤：

1. 计算相关性（Score）：判断当前查询与输入信息之间的相关程度。
2. 计算权重（Weight）：将相关性分数转换为概率分布。
3. 加权求和（Weighted Sum）：根据权重对输入信息进行加权求和。

整体流程：

```text
       Query（查询）
            |
            v
     计算相关性 Score
            |
            v
       Softmax归一化
            |
            v
      Attention Weight
            |
            v
     对 Value 加权求和
            |
            v
      Attention Output
```

## 4. Q、K、V 基本概念

Attention 的核心组成是 Q、K、V。

| 名称 | 英文 | 含义 |
|---|---|---|
| Q | Query | 查询，表示当前需要寻找什么信息 |
| K | Key | 键，用于描述输入信息的特征 |
| V | Value | 值，表示真正需要提取的信息 |

可以将其理解为数据库查询：

- Query：我要查询什么？
- Key：每条数据有什么特征？
- Value：查询命中后，真正返回什么内容？

例如：

```text
Query：我想了解苹果的营养价值

Key：
    苹果的营养成分
    苹果的种植方法
    手机的发展历史

Value：
    营养成分对应的信息
    种植方法对应的信息
    手机历史对应的信息
```

Query 与 Key 计算相关性，得到权重，再利用权重对 Value 进行加权求和。

**注意：Q、K、V 是 Attention 的计算角色，不一定是三个完全不同的数据源。**

## 5. Attention 数学计算

以 Scaled Dot-Product Attention（缩放点积注意力）为例。

### 5.1 计算相关性分数

使用 Query 和 Key 进行点积：

\[
Score = QK^T
\]

其中：

- Q：查询矩阵
- K：键矩阵
- \(K^T\)：Key 的转置矩阵

点积越大，通常表示 Query 与 Key 越相关。

### 5.2 缩放处理

为了避免点积结果过大，对 Score 进行缩放：

\[
Score_{scaled} = \frac{QK^T}{\sqrt{d_k}}
\]

其中：

- \(d_k\)：Key 向量的维度。
- \(\sqrt{d_k}\)：缩放因子。

缩放的目的是控制数值大小，避免 Softmax 进入梯度过小的区域。

### 5.3 Softmax 归一化

将相关性分数转换为注意力权重：

\[
Attention\ Weight =
Softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)
\]

Softmax 计算公式：

\[
Softmax(x_i)=\frac{e^{x_i}}{\sum_j e^{x_j}}
\]

其结果满足：

- 每个权重都在 0 到 1 之间。
- 所有权重之和等于 1。

### 5.4 加权求和

使用 Attention Weight 对 Value 进行加权求和：

\[
Output = Attention\ Weight \cdot V
\]

最终得到 Attention 输出。

### 5.5 完整公式

\[
\boxed{
Attention(Q,K,V)=
Softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
}
\]

这就是 Transformer 中经典的 Scaled Dot-Product Attention 公式。

## 6. Attention 计算实例

假设有三个 Value 向量：

```text
V1 = [1, 0]
V2 = [0, 1]
V3 = [1, 1]
```

经过 Query 和 Key 的相关性计算及 Softmax，得到：

```text
Attention Weight：

W = [0.2, 0.3, 0.5]
```

最终输出：

\[
Output = 0.2V_1+0.3V_2+0.5V_3
\]

\[
Output =
0.2[1,0]+0.3[0,1]+0.5[1,1]
\]

\[
\boxed{Output=[0.7,0.8]}
\]

可以看到，权重越大，对最终输出的贡献越大。

## 7. Python 实现 Attention

下面使用 NumPy 实现一个简单的 Scaled Dot-Product Attention。

### 7.1 完整代码

```python
import numpy as np


def softmax(x):
    """Softmax 归一化"""
    x = x - np.max(x, axis=-1, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def scaled_dot_product_attention(Q, K, V):
    """
    Scaled Dot-Product Attention

    Q: Query
    K: Key
    V: Value
    """

    # 获取 Key 的维度
    d_k = K.shape[-1]

    # 1. 计算相关性
    score = np.matmul(Q, K.T)

    # 2. 缩放
    score = score / np.sqrt(d_k)

    # 3. Softmax 计算注意力权重
    attention_weights = softmax(score)

    # 4. 加权求和
    output = np.matmul(attention_weights, V)

    return output, attention_weights


if __name__ == "__main__":

    # 构造 Q、K、V
    Q = np.array([
        [1.0, 0.0]
    ])

    K = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0]
    ])

    V = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0]
    ])

    output, weights = scaled_dot_product_attention(Q, K, V)

    print("Attention Weight:")
    print(weights)

    print("Attention Output:")
    print(output)
```

### 7.2 输出结果

```text
Attention Weight:
[[0.4011 0.1978 0.4011]]

Attention Output:
[[0.8022 0.5989]]
```

### 7.3 代码流程

| 步骤 | 操作 | NumPy API | 功能 |
|---|---|---|---|
| 1 | 计算相关性 | `np.matmul()` | Q 与 K 转置进行矩阵乘法 |
| 2 | 缩放 | `/ np.sqrt()` | 控制分数大小 |
| 3 | 权重归一化 | `softmax()` | 将分数转换为注意力权重 |
| 4 | 加权求和 | `np.matmul()` | 权重与 V 相乘 |

## 8. Attention 的常见类型

Attention 根据计算方式和应用场景，可以分为不同类型。

| 类型 | 中文名称 | 核心特点 |
|---|---|---|
| Additive Attention | 加性注意力 | 使用神经网络计算相关性 |
| Dot-Product Attention | 点积注意力 | 使用 Q 和 K 点积计算相关性 |
| Scaled Dot-Product Attention | 缩放点积注意力 | 点积后增加缩放因子 |
| Self-Attention | 自注意力 | Q、K、V 来自同一序列 |
| Cross-Attention | 交叉注意力 | Q 与 K、V 来自不同序列 |
| Multi-Head Attention | 多头注意力 | 并行计算多个注意力头 |

## 9. Attention 与 Transformer 的关系

Attention 是 Transformer 的核心组成部分。

Transformer 使用 Attention 建立序列中不同位置之间的关联。

其核心结构可以抽象为：

```text
输入序列
   |
   v
Embedding
   |
   v
Positional Encoding
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
输出
```

其中：

- Attention：负责计算不同位置之间的信息关联。
- Multi-Head Attention：从多个不同的表示空间提取信息。
- Feed Forward Network：对每个位置的特征进行非线性变换。
- Positional Encoding：提供序列位置信息。

## 10. Attention 学习路线

建议按照以下顺序深入学习：

| 顺序 | 知识点 | 学习重点 |
|---|---|---|
| 1 | Attention 基础 | Q、K、V 和基本计算流程 |
| 2 | Seq2Seq | 理解传统 Encoder-Decoder 架构 |
| 3 | Additive Attention | 理解加性注意力 |
| 4 | Dot-Product Attention | 理解点积注意力 |
| 5 | Scaled Dot-Product Attention | 理解缩放点积注意力 |
| 6 | Self-Attention | 理解序列内部的信息交互 |
| 7 | Multi-Head Attention | 理解多头并行注意力 |
| 8 | Causal Attention | 理解自回归生成中的掩码 |
| 9 | Cross-Attention | 理解不同序列之间的信息交互 |

## 11. 总结

Attention 的本质是根据 Query 与 Key 的相关性计算权重，再使用这些权重对 Value 进行加权求和。

核心流程：

```text
Q、K、V 输入
     |
     v
Q 与 K 计算相关性
     |
     v
缩放处理
     |
     v
Softmax 归一化
     |
     v
得到 Attention Weight
     |
     v
Attention Weight 与 V 相乘
     |
     v
得到 Attention Output
```

核心公式：

\[
\boxed{
Attention(Q,K,V)=
Softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
}
\]

**核心结论：Attention 通过动态计算权重，让模型能够根据当前任务关注输入序列中更重要的信息，是 Transformer 和现代 LLM 的重要基础。**