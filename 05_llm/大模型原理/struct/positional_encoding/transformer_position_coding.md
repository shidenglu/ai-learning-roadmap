# Transformer 位置编码演化详解

## 1. 为什么需要位置编码

Transformer 的核心是 Self-Attention：

```text
Attention(Q,K,V)
=
Softmax(QKᵀ/√d)
×V
```

Attention 本身只关注向量之间的关系，并不知道 Token 的先后顺序。

例如：

```text
我 爱 中国
```

和：

```text
中国 爱 我
```

经过 Embedding 后：

```text
[E我, E爱, E中国]
```

Attention 无法天然区分：

```text
谁在前
谁在后
```

因此 Transformer 必须额外引入位置信息。

---

# 位置编码的发展路线

```text
绝对位置编码（Sin/Cos）
        ↓
可学习位置编码（Learnable PE）
        ↓
相对位置编码（Relative PE）
        ↓
RoPE（Rotary Position Embedding）
        ↓
现代LLM主流方案
```

---

# 2. 第一代：绝对位置编码（Sin/Cos PE）

## 核心思想

直接告诉模型：

```text
我是第0个Token
我是第1个Token
我是第2个Token
```

即：

```text
Input
=
Token Embedding
+
Position Encoding
```

---

## 实现流程

输入：

```text
我 爱 中国
```

Token Embedding：

```text
我      -> E0
爱      -> E1
中国    -> E2
```

位置：

```text
0
1
2
```

位置编码：

```text
PE(0)
PE(1)
PE(2)
```

最终输入：

```text
X0 = E0 + PE(0)

X1 = E1 + PE(1)

X2 = E2 + PE(2)
```

---

## Sin/Cos公式

偶数维：

```text
PE(pos,2i)
=
sin(pos / 10000^(2i/d))
```

奇数维：

```text
PE(pos,2i+1)
=
cos(pos / 10000^(2i/d))
```

其中：

```text
pos : Token位置
i   : 维度索引
d   : Embedding维度
```

---

## 优点

无需训练：

```text
直接计算即可
```

支持长文本：

```text
训练512
推理4096
仍可计算
```

---

## 缺点

模型看到的是：

```text
位置0
位置1
位置2
```

而不是：

```text
距离1
距离2
距离3
```

无法天然表达相对位置关系。

---

# 3. 第二代：可学习位置编码（Learnable Position Embedding）

代表模型：

```text
BERT
GPT-2
```

---

## 核心思想

既然词向量可以学习：

```text
苹果 -> 向量
香蕉 -> 向量
```

那么位置向量也可以学习：

```text
位置0 -> 向量
位置1 -> 向量
位置2 -> 向量
```

---

## 实现

定义位置Embedding表：

```python
position_embedding =
nn.Embedding(
    max_len,
    hidden_size
)
```

例如：

```python
nn.Embedding(
    512,
    768
)
```

内部结构：

```text
Position Table

0 -> 向量A
1 -> 向量B
2 -> 向量C
...
511 -> 向量Z
```

---

## 输入方式

仍然是：

```text
Input
=
Token Embedding
+
Position Embedding
```

---

## 优点

表达能力更强。

位置向量能够根据训练数据自动优化。

---

## 缺点

假设训练时：

```text
最大长度=512
```

那么：

```text
位置513
```

没有对应参数。

因此：

```text
长文本外推能力差
```

---

# 4. 第三代：相对位置编码（Relative Position Encoding）

代表模型：

```text
Transformer-XL
T5
DeBERTa
```

---

## 核心思想

Attention 真正关心的不是：

```text
你在第100个位置
```

而是：

```text
你距离我有多远
```

例如：

```text
我 爱 中国
```

Attention 更关心：

```text
我 ←→ 爱

距离 = 1
```

而不是：

```text
位置0
位置1
```

---

## 实现方式

原始 Attention：

```text
score
=
QKᵀ
```

修改后：

```text
score
=
QKᵀ
+
RelativeBias
```

其中：

```text
RelativeBias
=
距离编码
```

例如：

```text
distance = -2
distance = -1
distance = 0
distance = 1
distance = 2
```

分别拥有不同参数。

---

## 示例

Attention矩阵：

```text
      我 爱 中

我     *
爱     *
中     *
```

加入距离信息后：

```text
      我 爱 中

我   *+b0
爱   *+b1
中   *+b2
```

---

## 优点

模型直接学习：

```text
距离1
距离2
距离3
```

更符合语言规律。

---

## 缺点

实现复杂。

Attention额外引入距离参数和计算开销。

---

# 5. 第四代：RoPE（Rotary Position Embedding）

代表模型：

```text
LLaMA
Qwen
DeepSeek
Gemma
Mistral
ChatGPT系列架构
```

现代LLM主流方案。

---

## 核心思想

前面三代：

```text
Embedding
+
Position
```

RoPE：

```text
不再把位置加到Embedding
```

而是：

```text
直接修改Q和K
```

---

# 6. RoPE实现原理

Transformer中：

```text
X
 ↓
Wq
 ↓
Q

X
 ↓
Wk
 ↓
K
```

RoPE加入后：

```text
Q
 ↓
Rotate
 ↓
Q'

K
 ↓
Rotate
 ↓
K'
```

然后：

```text
Attention
=
Q'K'ᵀ
```

---

## 二维理解

假设：

```text
Q

[
x
y
]
```

位置：

```text
pos
```

对应旋转角度：

```text
θ
```

构造旋转矩阵：

```text
R(θ)

[
 cosθ  -sinθ
 sinθ   cosθ
]
```

计算：

```text
Q'
=
R(θ)
×
Q
```

---

## 图形理解

位置0：

```text
→
```

位置1：

```text
↗
```

位置2：

```text
↑
```

位置3：

```text
↖
```

位置不同：

```text
旋转角度不同
```

---

# 7. RoPE的关键优势

RoPE后的Attention：

```text
score
=
(RiQ)
(RjK)ᵀ
```

数学展开后会自然出现：

```text
(i-j)
```

即：

```text
相对距离
```

因此：

```text
Attention天然感知距离
```

---

## RoPE同时拥有

### 绝对位置

```text
第10个Token
```

由旋转角度体现。

---

### 相对位置

```text
距离=5
```

由：

```text
(i-j)
```

自动体现。

---

### 长文本外推能力

训练：

```text
4K
```

推理：

```text
32K
64K
128K
```

仍可使用。

因为：

```text
角度可持续计算
```

无需新增参数。

---

# 8. LLaMA/Qwen中的RoPE

实际流程：

```text
Token
 ↓
Embedding
 ↓
Q/K/V
 ↓
RoPE(Q)
RoPE(K)
 ↓
Attention
 ↓
FFN
 ↓
Output
```

伪代码：

```python
q = Wq(x)
k = Wk(x)

q = apply_rope(q)
k = apply_rope(k)

attn = softmax(
    q @ k.T
)
```

---

# 9. 四代位置编码对比

| 方案           | 加入位置方式         | 是否训练 | 长文本能力 | 主流程度       |
| ------------ | -------------- | ---- | ----- | ---------- |
| Sin/Cos PE   | Embedding相加    | 否    | 好     | 已较少使用      |
| Learnable PE | Embedding相加    | 是    | 差     | BERT/GPT-2 |
| Relative PE  | Attention Bias | 是    | 较好    | 部分模型       |
| RoPE         | Q/K旋转          | 否    | 极好    | 当前主流       |

---

# 10. 演化总结

位置编码的发展本质上是在不断回答同一个问题：

> 如何让 Attention 更自然地理解 Token 之间的位置关系。

演化过程：

```text
第一代
绝对位置
↓
告诉模型：
我是第几个Token

第二代
可学习位置
↓
让模型自己学习位置表示

第三代
相对位置
↓
让模型关注距离关系

第四代
RoPE
↓
把位置信息直接编码到Q/K中
↓
同时获得
绝对位置
+
相对位置
+
长文本外推能力
```

---

# 11. 一句话总结

```text
Sin/Cos PE
=
把位置加到输入上

Learnable PE
=
把位置作为可训练参数

Relative PE
=
把距离加入Attention

RoPE
=
把位置旋转进Q/K
```

现代大模型（LLaMA、Qwen、DeepSeek 等）几乎全部采用 RoPE，因为它同时兼顾：

```text
位置表达能力
+
相对距离建模
+
长文本扩展能力
+
计算效率
```

因此已经成为当前 Transformer 位置编码的主流实现方案。
