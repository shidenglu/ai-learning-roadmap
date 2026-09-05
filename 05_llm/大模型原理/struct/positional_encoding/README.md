# Positional Encoding（位置编码）

## 1. 为什么需要 Positional Encoding

Transformer 的 Self-Attention 本质上是一种并行计算机制：

```text
我 爱 中国
中国 爱 我
```

对于 Attention 来说，仅看到 Token 向量时：

```text
我
爱
中国
```

并不知道它们出现的先后顺序。

因此：

```text
我爱中国
中国爱我
```

如果不引入位置信息，模型可能认为它们是相同的输入。

---

## 2. Positional Encoding 的作用

Positional Encoding（位置编码）的作用是：

> 为每个 Token 注入位置信息，让 Transformer 感知序列顺序。

即：

```text
Token Embedding
       +
Positional Encoding
       ↓
最终输入向量
```

例如：

```text
句子：

我 爱 中国

位置：

0  1  2
```

经过位置编码后：

```text
我     + PE(0)
爱     + PE(1)
中国   + PE(2)
```

这样模型就能区分：

```text
我 爱 中国
```

和

```text
中国 爱 我
```

---

## 3. Transformer中的输入

输入到 Transformer 的实际上是：

```text
Input Embedding
=
Token Embedding
+
Positional Encoding
```

数学表示：

```text
X = E + P
```

其中：

```text
E : Token Embedding
P : Position Encoding
X : Transformer输入
```

---

## 4. 经典 Sin/Cos 位置编码

论文《Attention Is All You Need》采用：

```text
sin()
cos()
```

构造位置向量。

公式：

```text
PE(pos,2i)
=
sin(pos / 10000^(2i/d))
```

```text
PE(pos,2i+1)
=
cos(pos / 10000^(2i/d))
```

其中：

```text
pos : 位置编号
i   : 维度索引
d   : Embedding维度
```

---

## 5. 示例

假设：

```text
Embedding维度 = 4
```

则：

```text
位置0

[
 sin(0)
 cos(0)
 sin(0)
 cos(0)
]

=
[
 0
 1
 0
 1
]
```

位置1：

```text
[
 sin(1)
 cos(1)
 sin(0.01)
 cos(0.01)
]
```

位置2：

```text
[
 sin(2)
 cos(2)
 sin(0.02)
 cos(0.02)
]
```

不同位置会得到不同向量。

---

## 6. 为什么使用 Sin/Cos

优点：

### 唯一性

不同位置：

```text
PE(0) ≠ PE(1) ≠ PE(2)
```

模型能够区分位置。

### 可扩展

训练：

```text
长度 = 512
```

推理：

```text
长度 = 2048
```

仍然可以计算新的位置编码。

### 表达相对距离

模型能够学习：

```text
位置5
位置6
```

之间的关系。

---

## 7. 可学习位置编码

现代大模型更多采用：

```text
Learnable Position Embedding
```

即：

```text
Position ID
      ↓
Embedding
      ↓
Position Vector
```

类似：

```python
nn.Embedding(max_len, d_model)
```

例如：

```text
位置0 → 向量A
位置1 → 向量B
位置2 → 向量C
```

这些向量由训练自动学习得到。

---

## 8. RoPE（Rotary Position Embedding）

当前主流大模型：

```text
LLaMA
Qwen
DeepSeek
ChatGPT系列
```

普遍采用：

```text
RoPE
(Rotary Position Embedding)
```

核心思想：

```text
不直接加位置向量
```

而是：

```text
对Q/K进行旋转变换
```

使 Attention 天然感知位置关系。

优点：

```text
✓ 长文本效果更好
✓ 相对位置表达更强
✓ 外推能力更好
✓ 已成为主流方案
```

---

## 9. 位置编码的发展

```text
RNN
 ↓
天然具有顺序

Transformer
 ↓
需要位置编码

Sin/Cos PE
 ↓
Learnable PE
 ↓
Relative PE
 ↓
RoPE
 ↓
现代LLM主流方案
```

---

## 10. 总结

Positional Encoding 的本质是：

> 给 Token 注入位置信息，使 Transformer 能够理解序列顺序。

整体流程：

```text
文本
 ↓
Tokenizer
 ↓
Token ID
 ↓
Token Embedding
 ↓
Positional Encoding
 ↓
Embedding + Position
 ↓
Transformer
 ↓
Attention计算
 ↓
输出
```

一句话概括：

> Transformer 天生不理解顺序，Positional Encoding 负责告诉模型“谁在前、谁在后”，从而让模型能够理解语言中的时序和语法结构。
