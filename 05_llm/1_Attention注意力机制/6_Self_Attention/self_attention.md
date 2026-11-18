# Self-Attention（自注意力机制）简介

## 1. 什么是Self-Attention

Self-Attention（自注意力机制）是一种用于建模序列内部元素之间关系的算法。

核心思想：

```text
序列中的每个Token
都去关注（Attention）
序列中的其它Token
从而获得上下文信息
```

例如：

```text
我 爱 深度 学习
```

计算：

```text
"学习"
会关注：

我
爱
深度
学习
```

从而理解：

```text
学习 ← 深度学习
```

而不是单独理解"学习"两个字。

---

## 2. 为什么需要Self-Attention

传统RNN：

```text
Token1 → Token2 → Token3 → Token4
```

缺点：

- 串行计算
- 长距离依赖困难
- 梯度消失

例如：

```text
小明住在北京，
他喜欢吃烤鸭。
```

RNN需要经过很多步才能知道：

```text
他 = 小明
```

---

Self-Attention：

```text
每个Token直接关注所有Token
```

```text
       他
      ↗↑↖
小明 北京 喜欢 烤鸭
```

一次计算即可建立关系。

---

## 3. Self-Attention输入

假设句子：

```text
I love AI
```

经过Tokenizer：

```text
[I, love, AI]
```

Embedding后：

```text
X =
[
 x1
 x2
 x3
]
```

维度：

```text
(seq_len, d_model)

(3, 512)
```

例如：

```text
3个Token

每个Token 512维
```

---

## 4. Q、K、V的产生

输入：

```text
X
```

通过三个线性层：

```text
Q = XWQ

K = XWK

V = XWV
```

得到：

```text
Query
Key
Value
```

---

含义：

```text
Q：我想找什么

K：我有什么特征

V：我的内容
```

---

## 5. Attention计算过程

### Step1

计算相关性

```text
Q × Kᵀ
```

公式：

```text
Score = QKᵀ
```

得到：

```text
每个Token之间的相似度
```

---

### Step2

缩放

公式：

```text
Score = QKᵀ / √dk
```

其中：

```text
dk = Key维度
```

目的：

```text
避免数值过大
```

---

### Step3

Softmax归一化

```text
Attention Weight
=
Softmax(Score)
```

得到：

```text
每个Token的重要程度
```

例如：

```text
[0.1 0.8 0.1]
```

表示：

```text
重点关注第二个Token
```

---

### Step4

加权求和

```text
Output
=
AttentionWeight × V
```

得到最终输出：

```text
Context Vector
```

---

## 6. 完整公式

Transformer核心公式：



---

## 7. 计算示例

假设：

```text
Token1 = 我
Token2 = 爱
Token3 = AI
```

计算：

```text
"AI"
```

对应Q：

```text
Q_AI
```

与所有K计算：

```text
Q_AI · K_我

Q_AI · K_爱

Q_AI · K_AI
```

得到：

```text
[1.2, 3.5, 2.1]
```

Softmax：

```text
[0.07, 0.73, 0.20]
```

说明：

```text
AI最关注"爱"
```

最终：

```text
Output_AI
=
0.07V我
+
0.73V爱
+
0.20VAI
```

---

## 8. 矩阵形式

输入：

```text
X
```

生成：

```text
Q
K
V
```

然后：

```text
QKᵀ
   ↓
Scale
   ↓
Softmax
   ↓
Attention Matrix
   ↓
乘V
   ↓
Output
```

流程：

```text
X
│
├──WQ──►Q
├──WK──►K
└──WV──►V

QKᵀ
 ↓
Softmax
 ↓
Attention
 ↓
×V
 ↓
Output
```

---

## 9. Self-Attention的优势

### 长距离依赖

```text
小明住北京，
他喜欢烤鸭。
```

直接建立：

```text
他 ↔ 小明
```

关系。

---

### 并行计算

RNN：

```text
串行
```

Transformer：

```text
并行
```

GPU利用率极高。

---

### 全局感知

每个Token：

```text
关注整个句子
```

而不是局部窗口。

---

## 10. 缺点

Attention矩阵大小：

```text
N × N
```

复杂度：

```text
O(N²)
```

例如：

```text
10000 Token

Attention矩阵

10000 × 10000
```

显存消耗巨大。

因此后来出现：

```text
FlashAttention
Sparse Attention
Linear Attention
Grouped Query Attention
```

等优化方案。

---

## 11. Self-Attention在Transformer中的位置

```text
Input
  ↓
Embedding
  ↓
Self-Attention
  ↓
Add & Norm
  ↓
Feed Forward
  ↓
Add & Norm
  ↓
Output
```

---

## 12. 总结

```text
Self-Attention核心作用：

让每个Token
关注序列中的所有Token

实现：
    全局建模
    长距离依赖
    并行计算

核心公式：

Attention(Q,K,V)
=
Softmax(QKᵀ/√dk)V

流程：

X
 ↓
Q K V
 ↓
QKᵀ
 ↓
Softmax
 ↓
Attention Weight
 ↓
V加权求和
 ↓
Output
```

Self-Attention 是 Transformer、BERT、GPT、LLaMA、Qwen、DeepSeek 等大语言模型最核心的计算模块。