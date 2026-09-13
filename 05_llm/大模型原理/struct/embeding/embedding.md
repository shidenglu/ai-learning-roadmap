# Embedding层详解：从Token ID到语义向量

## 1. 什么是 Embedding

Embedding（嵌入层）是大模型中负责将 **Token ID 转换为向量（Vector）** 的模块。

其作用是：

> **把离散的Token ID映射到连续的高维向量空间中，让神经网络能够处理语言信息。**

整体流程：

```text id="emb001"
文本
 ↓
Tokenizer
 ↓
Token
 ↓
Token ID
 ↓
Embedding
 ↓
向量(Vector)
 ↓
Transformer
```

例如：

```text id="emb002"
我爱中国
```

经过 Tokenizer：

```python id="emb003"
[1001, 3021, 5088]
```

经过 Embedding：

```python id="emb004"
[
 [0.23,0.51,...],
 [0.91,0.11,...],
 [0.43,0.72,...]
]
```

此时模型处理的已经不是文字，而是向量。

---

# 2. 为什么需要 Embedding

神经网络只能处理：

```text id="emb005"
数字
向量
矩阵
张量
```

无法直接处理：

```text id="emb006"
中国
北京
人工智能
```

即使转换成：

```python id="emb007"
[5088]
```

也没有意义。

因为：

```text id="emb008"
5088
```

只是编号，不代表语义。

例如：

```text id="emb009"
中国 → 5088
美国 → 6721
北京 → 922
```

数字之间：

```text id="emb010"
5088 和 6721
```

没有任何数学意义。

因此需要：

```text id="emb011"
Token ID
↓
Embedding
↓
语义向量
```

---

# 3. Embedding 的本质

Embedding 本质上是：

> **一个巨大的查找表（Lookup Table）。**

例如：

```text id="emb012"
词表大小 = 5

Embedding维度 = 4
```

Embedding矩阵：

```python id="emb013"
[
 [0.1,0.2,0.3,0.4],  # Token 0
 [0.5,0.6,0.7,0.8],  # Token 1
 [0.9,1.0,1.1,1.2],  # Token 2
 [1.3,1.4,1.5,1.6],  # Token 3
 [1.7,1.8,1.9,2.0]   # Token 4
]
```

形状：

```text id="emb014"
(5,4)
```

即：

```text id="emb015"
5个Token

每个Token
↓
4维向量
```

---

# 4. Embedding 的查表过程

假设：

```python id="emb016"
token_ids = [0,2,4]
```

查表：

```python id="emb017"
embedding[token_ids]
```

得到：

```python id="emb018"
[
 [0.1,0.2,0.3,0.4],
 [0.9,1.0,1.1,1.2],
 [1.7,1.8,1.9,2.0]
]
```

即：

```text id="emb019"
0 → 第一行
2 → 第三行
4 → 第五行
```

所以：

```text id="emb020"
Embedding
=
查表操作
```

---

# 5. 一个简单例子

词表：

```text id="emb021"
我      → 0
爱      → 1
中国    → 2
```

Embedding矩阵：

```python id="emb022"
[
 [0.1,0.2,0.3],
 [0.4,0.5,0.6],
 [0.7,0.8,0.9]
]
```

输入：

```python id="emb023"
[0,1,2]
```

输出：

```python id="emb024"
[
 [0.1,0.2,0.3],
 [0.4,0.5,0.6],
 [0.7,0.8,0.9]
]
```

即：

```text id="emb025"
我
↓
[0.1,0.2,0.3]

爱
↓
[0.4,0.5,0.6]

中国
↓
[0.7,0.8,0.9]
```

---

# 6. Embedding 维度

Embedding维度表示：

```text id="emb026"
每个Token用多少数字表示
```

例如：

```text id="emb027"
128维
256维
768维
1024维
4096维
8192维
```

---

典型模型：

| 模型         | Embedding维度 |
| ---------- | ----------- |
| BERT Base  | 768         |
| BERT Large | 1024        |
| GPT-2      | 768~1600    |
| Llama2 7B  | 4096        |
| GPT-3      | 12288       |

---

例如：

```text id="emb028"
中国
```

可能表示为：

```python id="emb029"
[
 0.32,
-0.71,
 1.24,
 ...
]
```

长度：

```text id="emb030"
4096维
```

---

# 7. Embedding 为什么能表达语义

训练开始时：

```text id="emb031"
Embedding
随机初始化
```

例如：

```python id="emb032"
中国
↓
[0.12,-0.33,0.55]

美国
↓
[-0.71,0.18,0.09]
```

没有任何意义。

---

经过训练后：

```text id="emb033"
语义相近
↓
向量接近
```

例如：

```text id="emb034"
中国
美国
日本
法国
```

都会位于：

```text id="emb035"
国家区域
```

附近。

---

而：

```text id="emb036"
苹果
香蕉
橘子
```

位于：

```text id="emb037"
水果区域
```

附近。

---

# 8. 向量空间示意图

二维示意：

```text id="emb038"
            苹果

              ●

 香蕉 ●

                      中国

                      ●

                  美国 ●

            日本 ●
```

实际情况：

```text id="emb039"
不是二维

而是几千维
```

---

# 9. Word2Vec 与 Embedding

Embedding思想最早来自：

```text id="emb040"
Word2Vec
```

经典例子：

```text id="emb041"
国王
男人
女人
王后
```

向量满足：

```text id="emb042"
King - Man + Woman
≈ Queen
```

即：

```math id="emb043"
v(King)-v(Man)+v(Woman)
≈
v(Queen)
```

说明向量中已经编码了语义信息。

---

# 10. PyTorch中的Embedding

定义：

```python id="emb044"
import torch
import torch.nn as nn

embedding = nn.Embedding(
    num_embeddings=10000,
    embedding_dim=256
)
```

表示：

```text id="emb045"
词表大小 = 10000

每个Token
↓
256维向量
```

---

输入：

```python id="emb046"
ids = torch.tensor(
    [1,5,10]
)
```

输出：

```python id="emb047"
vectors = embedding(ids)
```

形状：

```python id="emb048"
torch.Size([3,256])
```

---

# 11. 大模型中的Embedding矩阵

假设：

```text id="emb049"
Vocabulary = 100000

Embedding = 4096
```

则：

```text id="emb050"
Embedding Matrix

100000 × 4096
```

参数量：

```math id="emb051"
100000 × 4096
=
409,600,000
```

约：

```text id="emb052"
4亿参数
```

仅Embedding层就可能占据大量参数。

---

# 12. Position Embedding

除了Token Embedding：

```text id="emb053"
中国
```

还需要：

```text id="emb054"
位置信息
```

例如：

```text id="emb055"
我爱中国
```

与：

```text id="emb056"
中国爱我
```

Token一样。

顺序不同。

因此需要：

```text id="emb057"
Position Embedding
```

最终输入：

```text id="emb058"
Token Embedding
+
Position Embedding
```

---

# 13. Transformer输入

Transformer真正看到的是：

```text id="emb059"
Embedding向量
```

而不是：

```text id="emb060"
Token ID
```

流程：

```text id="emb061"
Token ID
    ↓
Embedding
    ↓
Position Embedding
    ↓
Transformer
    ↓
Self-Attention
```

---

# 14. Embedding 在训练中如何更新

训练过程中：

```text id="emb062"
Forward
 ↓
Loss
 ↓
Backward
 ↓
Gradient
 ↓
Update
```

Embedding矩阵也会参与更新。

因此：

```text id="emb063"
中国
```

对应向量会越来越合理。

---

# 15. Embedding 的意义

Embedding完成了：

```text id="emb064"
离散空间
↓
连续空间
```

转换。

即：

```text id="emb065"
Token ID
↓
Vector
```

这样：

```text id="emb066"
Attention
FFN
Transformer
```

才能进行矩阵运算。

---

# 16. 一张图看懂 Embedding

```text id="emb067"
文本

"我爱中国"

     │
     ▼

Tokenizer

     │
     ▼

[1001,3021,5088]

     │
     ▼

Embedding

     │
     ▼

[
 [0.12,0.55,...],
 [0.91,0.11,...],
 [0.43,0.72,...]
]

     │
     ▼

Position Embedding

     │
     ▼

Transformer
```

---

# 17. 总结

Embedding层是大模型中连接 Tokenizer 和 Transformer 的桥梁。

核心职责：

```text id="emb068"
Token ID
↓
高维向量
```

关键知识点：

1. Embedding本质是一个查找表（Lookup Table）。
2. Token ID本身没有语义，Embedding赋予语义表示。
3. 语义相近的Token，其Embedding向量往往更接近。
4. Embedding矩阵是可训练参数。
5. Embedding输出会与Position Embedding相加后送入Transformer。
6. 大模型处理的是向量，而不是文字。

一句话理解：

> **Embedding层就是大模型的“语言数字化转换器”，负责把Token ID映射成具有语义信息的高维向量，从而让Transformer能够理解和处理语言。**
