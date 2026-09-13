# Embedding 向量与语义的关系

## 1. 什么是 Embedding

在大语言模型（LLM）中，计算机不能直接理解：

```text
我喜欢吃苹果
```

计算机最终处理的是数字。

因此，LLM 首先需要把文本转换成 Token，然后再把 Token 转换成向量：

```text
文本
 ↓
Tokenizer
 ↓
Token ID
 ↓
Embedding
 ↓
向量
 ↓
Transformer
```

例如：

```text
"我喜欢苹果"
```

经过 Tokenizer 后可能得到：

```text
["我", "喜欢", "苹果"]
```

再转换成 Token ID：

```text
[125, 893, 4217]
```

然后 Embedding 层将每一个 Token ID 映射成一个高维向量：

```text
125  → [ 0.12, -0.35,  0.87, ...]
893  → [-0.42,  0.71,  0.15, ...]
4217 → [ 0.63, -0.18,  0.52, ...]
```

所以：

> **Embedding 的本质，就是把离散的 Token ID 映射成连续的高维向量。**

---

# 2. 为什么需要 Embedding

Token ID 本身没有语义。

例如：

```text
苹果 → 4217
香蕉 → 8123
汽车 → 1921
```

这里：

```text
4217
8123
1921
```

只是编号。

不能认为：

```text
8123 比 4217 大
```

就说明香蕉和苹果有什么语义关系。

也不能认为：

```text
|4217 - 8123| < |4217 - 1921|
```

就说明苹果和香蕉更加相似。

Token ID 是：

```text
离散编号
```

而 Embedding 是：

```text
连续向量
```

真正可以表达语义关系的是 Embedding 向量空间。

---

# 3. Embedding 的数学形式

假设词表大小为：

```text
V = 50000
```

Embedding 维度为：

```text
d = 768
```

那么 Embedding 层可以表示为一个矩阵：

```text
E ∈ R^(50000 × 768)
```

也就是：

```text
E =
[
    e₀
    e₁
    e₂
    ...
    e₄₉₉₉₉
]
```

其中每一行都是一个 Token 的 Embedding：

```text
eᵢ ∈ R^768
```

例如：

```text
Token ID = 4217
```

那么：

```text
Embedding(4217) = E[4217]
```

得到：

```text
[0.12, -0.35, 0.87, ..., 0.21]
```

总共有 768 个数字。

---

# 4. Embedding 为什么能够表示语义

这是理解 LLM 的一个非常重要的问题。

Embedding 层一开始并不知道：

```text
苹果
香蕉
汽车
电脑
```

分别是什么意思。

刚开始 Embedding 通常是随机初始化的。

例如：

```text
苹果：

[0.17, -0.52, 0.31, ...]

香蕉：

[-0.28, 0.43, 0.11, ...]

汽车：

[0.62, -0.15, 0.73, ...]
```

此时这些向量没有明确的语义。

真正的语义是在：

```text
训练过程中逐渐形成的
```

---

# 5. Embedding 是如何学习到语义的

核心原因是：

> **模型不断根据上下文预测目标 Token，并通过反向传播修改 Embedding 参数。**

例如训练数据中出现：

```text
我喜欢吃苹果。
我喜欢吃香蕉。
我喜欢吃橘子。
```

模型发现：

```text
苹果
香蕉
橘子
```

经常出现在：

```text
我喜欢吃 ______
```

的位置。

于是模型会逐渐学习：

```text
苹果
香蕉
橘子
```

在语言中的使用方式非常相似。

Embedding 参数经过大量训练以后，这些 Token 的向量会逐渐形成某种结构。

例如可以抽象理解为：

```text
水果区域

        苹果
       /
      /
 香蕉 -------- 橘子


汽车区域

        汽车
       /
      /
 卡车 -------- 公交车
```

注意：

这只是帮助理解的二维示意图。

实际 Embedding 通常是几百维甚至上千维。

---

# 6. 语义不是“写死”在某一个维度里的

这是一个非常容易产生误解的地方。

不能简单理解为：

```text
第1维 = 是否是动物
第2维 = 是否是水果
第3维 = 是否是正面情绪
第4维 = 是否是男性
...
```

实际上通常不是这么简单。

Embedding 的每一个维度往往不是一个可以直接解释的人类语义概念。

更准确的理解是：

```text
语义
 ↓
分布在大量维度之间
 ↓
形成一个整体的几何结构
```

例如：

```text
e(苹果)
=
[
  0.21,
 -0.13,
  0.87,
  0.44,
  ...
]
```

我们通常无法说：

```text
第 137 维 = 水果属性
```

而应该观察：

```text
整个向量
```

与其他向量之间的关系。

---

# 7. Embedding 空间

假设 Embedding 只有 2 维：

```text
二维向量空间
```

可以画成：

```text
          ↑
          |
     苹果 ●
          |
     香蕉 ●
          |
----------+----------------→
          |
          |
        汽车 ●
          |
```

如果：

```text
苹果 ≈ 香蕉
```

那么它们在向量空间中可能比较接近。

而：

```text
苹果
```

和：

```text
汽车
```

可能距离比较远。

因此：

> **语义相似的 Token，经过训练后往往会在向量空间中呈现某种相似的几何关系。**

---

# 8. 什么叫“向量相似”

最常见的方法之一是：

```text
余弦相似度
```

两个向量：

```text
A
B
```

余弦相似度定义为：

```text
cos(A,B)
=
(A · B) / (||A|| ||B||)
```

其中：

```text
A · B
```

表示点积。

```text
||A||
```

表示向量的长度。

---

# 9. 为什么使用余弦相似度

假设：

```text
A = [1, 0]
B = [0.9, 0.1]
```

两个向量方向非常接近。

因此：

```text
cos(A,B) ≈ 1
```

说明它们比较相似。

如果：

```text
A = [1,0]

C = [-1,0]
```

那么：

```text
cos(A,C) = -1
```

说明两个向量方向完全相反。

如果：

```text
A = [1,0]

D = [0,1]
```

那么：

```text
cos(A,D) = 0
```

表示方向正交。

因此可以粗略理解：

```text
cos ≈ 1
    ↓
方向非常相似

cos ≈ 0
    ↓
方向差异较大

cos ≈ -1
    ↓
方向相反
```

---

# 10. 一个非常重要的理解

需要特别注意：

> **Embedding 向量之间的距离并不是人类预先定义好的语义距离，而是模型在训练过程中逐渐学习出来的统计结构。**

也就是说，并不是程序员告诉模型：

```text
苹果和香蕉相似
```

而是模型在大量文本中看到：

```text
苹果
香蕉
橘子
葡萄
水果
```

这些词之间存在大量共同的上下文关系。

于是训练过程逐渐把这种关系编码到了向量空间中。

---

# 11. 分布式表示

Embedding 的核心思想可以理解为：

```text
Distributed Representation
```

即：

> 一个概念的含义不是由一个数字表示，而是由大量维度共同表示。

例如：

```text
苹果
```

可能对应：

```text
[
  0.21,
 -0.42,
  0.73,
  0.15,
  ...
]
```

而：

```text
香蕉
```

可能对应：

```text
[
  0.18,
 -0.37,
  0.69,
  0.22,
  ...
]
```

虽然具体数字不同，但整体结构可能比较接近。

---

# 12. 为什么“上下文”如此重要

仅仅使用静态 Embedding 并不能完整表达一个词在不同上下文中的含义。

例如：

```text
苹果
```

可能表示：

```text
水果
```

也可能表示：

```text
苹果公司
```

例如：

```text
我今天吃了一个苹果。
```

这里：

```text
苹果
```

明显是水果。

但是：

```text
苹果发布了新款手机。
```

这里：

```text
苹果
```

明显指 Apple 公司。

因此：

> **真正复杂的语义不能只依靠最初的 Embedding。**

还需要 Transformer 根据上下文进一步处理。

---

# 13. Embedding 与 Transformer 的关系

LLM 中可以大致理解为：

```text
文本
 ↓
Tokenizer
 ↓
Token ID
 ↓
Embedding
 ↓
初始向量
 ↓
Transformer
 ↓
上下文相关表示
 ↓
输出
```

Embedding 负责：

```text
Token ID
 ↓
基础向量表示
```

Transformer 负责：

```text
根据上下文
 ↓
重新理解这些 Token
```

---

# 14. 一个例子

假设：

```text
苹果很好吃
```

Token：

```text
["苹果", "很", "好吃"]
```

Embedding：

```text
苹果 → e₁
很   → e₂
好吃 → e₃
```

此时：

```text
e₁
```

只是苹果这个 Token 的基础表示。

然后进入 Transformer。

Self-Attention 会让：

```text
苹果
```

与：

```text
好吃
```

产生关系。

于是模型能够进一步理解：

```text
苹果
+
好吃
```

更可能表示：

```text
水果
```

---

# 15. Context 如何改变语义

比较：

```text
句子 A：

我吃了一个苹果。
```

和：

```text
句子 B：

苹果发布了新款手机。
```

虽然两个句子都有：

```text
苹果
```

但是 Transformer 会根据不同上下文产生不同的上下文表示。

可以抽象表示为：

```text
Token Embedding

苹果
 ↓
e(苹果)
```

经过 Transformer：

```text
苹果 + 我 + 吃了
        ↓
上下文表示 h₁
```

另一个句子：

```text
苹果 + 发布 + 手机
        ↓
上下文表示 h₂
```

因此：

```text
h₁ ≠ h₂
```

这就是：

> **Contextual Representation（上下文相关表示）**

---

# 16. Embedding 和 Contextual Embedding 的区别

可以简单区分：

## 静态 Embedding

一个 Token 基本对应一个固定向量：

```text
苹果
 ↓
e(苹果)
```

无论出现在什么句子中，初始 Embedding 都一样。

---

## 上下文 Embedding

经过 Transformer 后：

```text
苹果 + 上下文
 ↓
h(苹果 | context)
```

不同上下文得到不同表示。

例如：

```text
我吃苹果

苹果
 ↓
h₁
```

和：

```text
苹果公司发布产品

苹果
 ↓
h₂
```

其中：

```text
h₁ ≠ h₂
```

---

# 17. 从“词向量”发展到“大模型表示”

早期 NLP 中，经常使用：

```text
Word2Vec
GloVe
FastText
```

它们主要解决：

```text
Token
 ↓
向量
```

的问题。

例如：

```text
king
queen
man
woman
```

可能在向量空间中形成一定关系。

经典的抽象关系是：

```text
king - man + woman ≈ queen
```

也就是：

```text
国王
-
男人
+
女人
≈
女王
```

这说明向量空间不仅可以表示“相似”，还可能学习到某些关系结构。

不过需要注意：

> 这种简单的线性关系并不是所有语义关系都成立，也不能把现代 LLM 的语义理解完全归结为这种向量运算。

---

# 18. 为什么向量能够表达“关系”

因为神经网络训练的目标不是让每个 Token 获得一个人类可解释的标签。

而是：

```text
让模型尽可能准确地预测训练数据
```

例如：

```text
我今天开了一辆 ______
```

模型应该预测：

```text
汽车
```

而不是：

```text
苹果
```

为了实现这个目标，模型必须学习：

```text
开
汽车
驾驶
道路
司机
方向盘
```

之间的统计关系。

这些关系会逐渐反映在模型参数和隐藏状态中。

因此：

```text
语言中的统计规律
        ↓
训练目标
        ↓
梯度下降
        ↓
调整参数
        ↓
Embedding / Transformer 参数
        ↓
形成向量空间结构
```

---

# 19. Embedding 并不是“语义数据库”

这是理解 LLM 时非常重要的一点。

不能简单认为：

```text
Embedding：

苹果 → 水果
香蕉 → 水果
汽车 → 交通工具
```

实际上 Embedding 并不是一个传统数据库。

它更像是：

```text
一个高维空间中的坐标系统
```

例如：

```text
苹果 → 某个位置
香蕉 → 某个位置
汽车 → 某个位置
飞机 → 某个位置
```

这些位置之间的相对关系携带了一部分信息。

---

# 20. 一个非常形象的比喻

可以把 Embedding 想象成一张“语义地图”。

例如现实世界的地图：

```text
北京
 ↓
上海
 ↓
广州
```

地图上的位置表示：

```text
地理关系
```

而 Embedding 空间：

```text
苹果
香蕉
橘子
汽车
飞机
电脑
```

位置之间的关系可以部分表示：

```text
语言关系
语义关系
使用关系
上下文关系
```

因此可以把 Embedding 理解成：

> **语言世界的一张高维地图。**

---

# 21. 为什么叫“高维空间”

假设：

```text
Embedding dimension = 3
```

那么：

```text
苹果 = [0.2, 0.7, 0.1]
```

可以画在三维空间。

但是现代模型通常可能使用：

```text
768
1024
2048
4096
...
```

甚至更高的维度。

因此无法直接画出来。

我们实际上处理的是：

```text
R^d
```

例如：

```text
R^4096
```

即：

```text
4096维向量空间
```

---

# 22. 为什么维度越高就越能表达语义？

不能简单认为：

```text
维度越高
=
语义一定越丰富
```

更准确的理解是：

```text
更高维空间
 ↓
提供更多自由度
 ↓
可以编码更加复杂的表示
```

但是最终效果还取决于：

```text
模型结构
训练数据
训练目标
参数量
训练方法
优化过程
```

---

# 23. Token Embedding 的 PyTorch 实现

可以用一个非常简单的例子理解。

```python
import torch
import torch.nn as nn

# 假设词表中有 10 个 Token
vocab_size = 10

# 每个 Token 使用 4 维向量表示
embedding_dim = 4

embedding = nn.Embedding(
    num_embeddings=vocab_size,
    embedding_dim=embedding_dim
)

# Token ID
tokens = torch.tensor([1, 3, 5])

# 查表
vectors = embedding(tokens)

print(vectors)
print(vectors.shape)
```

输出形状：

```text
torch.Size([3, 4])
```

因为：

```text
3 个 Token
×
4 维 Embedding
```

所以：

```text
[
    [....],
    [....],
    [....]
]
```

---

# 24. Embedding 本质上就是查表

这一点非常重要。

假设：

```text
Embedding 矩阵：

E =
[
    e₀
    e₁
    e₂
    e₃
    e₄
]
```

输入：

```text
Token ID = 3
```

实际上就是：

```text
E[3]
```

也就是取第 3 行。

因此：

```text
Token ID
   ↓
Embedding Matrix 查表
   ↓
Vector
```

Embedding 层并不是一个神秘的“语义转换器”。

它本质上就是一个：

```text
可训练的查表矩阵
```

---

# 25. Embedding 矩阵如何被训练

假设：

```text
E ∈ R^(V × d)
```

例如：

```text
V = 50000
d = 768
```

那么参数数量：

```text
50000 × 768
=
38,400,000
```

也就是大约：

```text
3840 万个参数
```

训练过程中：

```text
前向传播
 ↓
计算 Loss
 ↓
反向传播
 ↓
计算梯度
 ↓
更新 Embedding
```

例如：

```text
E[4217]
```

对应“苹果”。

如果当前模型因为“苹果”这个 Token 的表示不够好而产生预测误差，那么反向传播会影响相关参数。

经过海量训练：

```text
E[4217]
```

会逐渐形成适合模型任务的表示。

---

# 26. 为什么相似语义会逐渐靠近

假设：

```text
苹果
香蕉
橘子
```

经常出现在类似上下文：

```text
吃苹果
吃香蕉
吃橘子

买苹果
买香蕉
买橘子

水果包括苹果
水果包括香蕉
水果包括橘子
```

那么模型需要用类似的方式处理它们。

于是训练过程中：

```text
苹果
香蕉
橘子
```

的表示可能逐渐形成相似结构。

可以抽象为：

```text
              水果
               ●
              /|\
             / | \
            /  |  \
        苹果  香蕉  橘子
```

而：

```text
汽车
飞机
火车
```

可能形成另外一个区域：

```text
            交通工具
                ●
              / | \
             /  |  \
           汽车 飞机 火车
```

---

# 27. 但是“靠近”不是绝对的

需要注意：

```text
语义相似
```

和：

```text
向量距离近
```

之间不是简单的一一对应关系。

Embedding 表示的是模型为了完成训练任务而形成的内部表示。

因此：

```text
向量空间
```

受到：

```text
训练数据
训练目标
模型结构
Tokenizer
上下文
参数更新方式
```

等多种因素影响。

所以不能简单说：

```text
距离近 = 人类认为完全相同
```

更准确地说：

> **向量空间中的几何关系是模型从训练数据中学习出来的表示结构。**

---

# 28. Embedding 与“知识”的关系

Embedding 可以携带大量信息，但不要把它理解成：

```text
Embedding = 知识库
```

例如模型知道：

```text
巴黎是法国首都
```

并不意味着 Embedding 中存在一条明确的数据：

```text
巴黎 → 法国首都
```

更接近实际的情况是：

```text
大量 Token
+
大量 Transformer 参数
+
大量上下文交互
+
训练过程中形成的参数结构
```

共同构成模型的知识表示。

---

# 29. Embedding 与 Transformer 参数的区别

可以粗略划分：

```text
Embedding
    ↓
提供 Token 的初始表示

Transformer
    ↓
处理 Token 之间的关系

Attention
    ↓
根据上下文建立动态关系

MLP
    ↓
进行非线性特征变换

最终隐藏状态
    ↓
形成更加丰富的上下文表示
```

所以：

```text
Embedding
```

只是整个 LLM 表示系统的起点。

---

# 30. Self-Attention 为什么能够进一步理解语义

假设：

```text
我把苹果放进冰箱，因为它坏了。
```

这里：

```text
它
```

到底指：

```text
苹果
```

还是：

```text
冰箱
```

模型需要结合上下文。

Self-Attention 可以让：

```text
它
```

关注：

```text
苹果
```

和：

```text
冰箱
```

等其他 Token。

于是形成：

```text
它
 ↓
Attention
 ↓
苹果
```

从而得到更加准确的上下文表示。

---

# 31. Embedding 和 Attention 的核心区别

可以用一句话理解：

```text
Embedding：
Token 本身是什么？

Attention：
Token 在当前句子中和谁有什么关系？
```

例如：

```text
苹果
```

Embedding 提供：

```text
苹果的基础表示
```

Attention 提供：

```text
当前语境下苹果和其他 Token 的关系
```

---

# 32. 从 Token 到语义的完整过程

现在把整个过程串起来：

```text
自然语言
    │
    ▼
"我喜欢吃苹果"
    │
    ▼
Tokenizer
    │
    ▼
Token
    │
    ▼
Token ID
    │
    ▼
Embedding
    │
    ▼
初始向量
    │
    ▼
Positional Information
    │
    ▼
Transformer
    │
    ├── Self-Attention
    │
    ├── MLP
    │
    ├── LayerNorm
    │
    └── Residual
    │
    ▼
上下文相关表示
    │
    ▼
Language Model Head
    │
    ▼
Logits
    │
    ▼
概率
    │
    ▼
预测下一个 Token
```

---

# 33. 为什么 Embedding 是 LLM 的基础

LLM 面对的是：

```text
离散语言
```

例如：

```text
苹果
汽车
人工智能
Linux
CPU
```

而神经网络擅长处理的是：

```text
连续数值
```

因此需要：

```text
离散 Token
     ↓
连续向量
```

Embedding 正好完成了这个桥梁。

所以：

> **Embedding 是自然语言进入神经网络数值计算世界的第一座桥梁。**

---

# 34. 从“编号”到“空间”

可以把 Tokenizer 和 Embedding 对比起来：

```text
Tokenizer：

苹果
 ↓
4217
```

Tokenizer 解决：

```text
文字如何编号？
```

而 Embedding：

```text
4217
 ↓
[0.12, -0.35, 0.87, ...]
```

解决：

```text
这个编号如何变成神经网络可以处理的表示？
```

因此：

```text
Tokenizer
=
建立离散符号系统

Embedding
=
建立连续向量表示空间
```

---

# 35. Token ID 没有语义，Embedding 才开始产生表示结构

例如：

```text
苹果 → 4217
```

这里：

```text
4217
```

没有语义。

而：

```text
4217
 ↓
Embedding
 ↓
[0.12, -0.35, 0.87, ...]
```

这个向量才进入了模型的表示空间。

经过训练：

```text
苹果
香蕉
橘子
```

可能形成一定的空间关系。

因此可以理解为：

```text
Token ID
    ↓
只是地址
    ↓
Embedding Matrix
    ↓
取出向量
    ↓
进入语义表示空间
```

---

# 36. 一个非常重要的误区

不能认为：

```text
Embedding 向量
=
这个词的完整语义
```

这是不准确的。

更准确的是：

```text
Embedding
=
Token 的初始表示
```

真正复杂的语义表示来自：

```text
Embedding
+
位置编码
+
Self-Attention
+
MLP
+
多层 Transformer
```

最终：

```text
Token
 ↓
Contextual Representation
```

才是更加丰富的上下文语义表示。

---

# 37. 为什么 LLM 能理解长句子

例如：

```text
虽然今天下着很大的雨，但是我还是开车去了公司，因为下午有一个非常重要的会议。
```

这里存在：

```text
时间关系
因果关系
转折关系
人物行为
事件关系
```

单独的 Token Embedding 很难表达完整关系。

例如：

```text
雨
会议
公司
开车
```

各自只有基础向量。

但是经过 Transformer：

```text
雨
 ↕
但是
 ↕
开车
 ↕
公司
 ↕
因为
 ↕
会议
```

不同 Token 之间可以通过 Attention 建立关系。

所以：

```text
Embedding
```

是起点。

而：

```text
Transformer
```

负责把这些基础表示组合成复杂的上下文表示。

---

# 38. 可以把语义理解成三层

学习 LLM 时，可以把“语义”粗略分成三个层次。

## 第一层：Token 级表示

```text
苹果
 ↓
Embedding
```

回答：

```text
这个 Token 的基础表示是什么？
```

---

## 第二层：上下文级表示

```text
苹果 + 吃 + 水果
 ↓
Transformer
```

回答：

```text
这个 Token 在当前句子中是什么意思？
```

---

## 第三层：整体语义表示

```text
整句话
 ↓
多层 Transformer
 ↓
复杂隐藏状态
```

回答：

```text
整个句子表达了什么？
```

---

# 39. Embedding 的本质可以概括成一句话

如果只记住一句话：

> **Embedding 是一个可训练的向量映射，它把离散 Token 映射到高维连续空间，而模型通过大量训练，使这个空间逐渐形成能够反映语言统计规律、语义相似性以及其他关系的结构。**

---

# 40. 最终理解图

把整个过程浓缩成一张图：

```text
                    自然语言
                       │
                       ▼
              ┌────────────────┐
              │    Tokenizer   │
              └────────────────┘
                       │
                       ▼
                    Token ID
                       │
                       ▼
              ┌────────────────┐
              │   Embedding    │
              │    Matrix      │
              └────────────────┘
                       │
                       ▼
                初始 Token 向量
                       │
                       ▼
              ┌────────────────┐
              │   Transformer  │
              │                │
              │ Self-Attention │
              │      +         │
              │      MLP       │
              └────────────────┘
                       │
                       ▼
              上下文相关向量
                       │
                       ▼
                  语义表示
                       │
                       ▼
                Language Model
                       │
                       ▼
                下一个 Token
```

---

# 41. 最核心的知识点总结

| 概念                   | 作用                       |
| -------------------- | ------------------------ |
| Token                | 文本被切分后的离散单位              |
| Token ID             | Token 的整数编号              |
| Embedding            | Token ID → 向量            |
| Embedding Matrix     | 保存所有 Token 向量的矩阵         |
| 向量空间                 | 表示 Token 之间关系的高维空间       |
| 余弦相似度                | 衡量两个向量方向的相似程度            |
| Context              | Token 所处的上下文             |
| Self-Attention       | 建立 Token 与 Token 之间的动态关系 |
| Transformer          | 对 Token 表示进行多层上下文建模      |
| Contextual Embedding | 融合上下文之后的 Token 表示        |

---

# 42. 最终建立正确的 LLM 心智模型

学习 LLM 时，建议把下面这条链路牢牢记住：

```text
文字
 ↓
Tokenizer
 ↓
Token
 ↓
Token ID
 ↓
Embedding
 ↓
向量
 ↓
Transformer
 ↓
Attention
 ↓
上下文关系
 ↓
高维隐藏表示
 ↓
Logits
 ↓
概率分布
 ↓
下一个 Token
```

其中最关键的理解是：

```text
Token ID
```

只是编号；

```text
Embedding
```

把编号变成向量；

```text
训练
```

让这些向量逐渐形成结构；

```text
Transformer
```

进一步根据上下文建立动态语义关系。

所以并不是：

```text
Embedding 本身知道“苹果是什么”
```

而是：

```text
大量训练数据
        ↓
模型训练
        ↓
Embedding + Transformer 参数发生变化
        ↓
向量空间形成结构
        ↓
模型能够利用这些结构处理语言
```

最终可以把 Embedding 理解成：

> **LLM 中连接“离散语言符号”和“连续神经网络表示”的桥梁，也是整个语义表示空间的起点。**

而从这里继续往下学习，下一步最值得搞清楚的是：

```text
Embedding
    ↓
Position Embedding / RoPE
    ↓
Q、K、V
    ↓
Self-Attention
    ↓
为什么 Attention 能理解上下文
    ↓
Transformer Block
```

这条链路搞懂以后，Transformer 的底层原理就会开始真正串起来。
