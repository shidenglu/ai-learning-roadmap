# Multi-Head Attention：为什么不同 Head 能学习不同关系

## 1. 一个容易产生的误解

容易认为 Multi-Head Attention 是：

```text
4096维
  ↓
简单切成32份
  ↓
每份128维
  ↓
32个Head
```

**这是不准确的。**

真实的 Multi-Head Attention 中：

> **每个 Head 都可以看到完整的输入 X，然后通过自己独立的 WQ、WK、WV 进行投影。**

---

## 2. 每个 Head 如何得到 Q/K/V

假设：

```text
hidden_size = 4096
num_heads   = 32
head_dim    = 128
```

输入：

```text
X = [Token数量, 4096]
```

对于第一个 Head：

```text
Q₁ = X × WQ₁
K₁ = X × WK₁
V₁ = X × WV₁
```

第二个 Head：

```text
Q₂ = X × WQ₂
K₂ = X × WK₂
V₂ = X × WV₂
```

其中：

```text
WQ₁ ≠ WQ₂
WK₁ ≠ WK₂
WV₁ ≠ WV₂
```

所以：

```text
                    X
              [Token,4096]
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Head1       Head2       Head3 ...
        │           │           │
   WQ₁/WK₁/WV₁ WQ₂/WK₂/WV₂ WQ₃/WK₃/WV₃
        │           │           │
        ↓           ↓           ↓
     128维        128维        128维
```

---

## 3. 为什么不同 Head 会得到不同关系？

因为每个 Head 有**独立的参数**。

例如同一个 Token：

```text
它
```

Head 1 可能学习：

```text
它 → 苹果
```

Head 2 可能学习：

```text
它 → 小明
```

Head 3 可能学习：

```text
它 → 吃
```

它们看到的是同一个 `X`，但是：

```text
WQ₁、WK₁
WQ₂、WK₂
WQ₃、WK₃
```

不同，所以计算出来的：

```text
Q₁K₁ᵀ
Q₂K₂ᵀ
Q₃K₃ᵀ
```

也不同。

因此得到不同的 Attention 权重。

---

## 4. 一个简单例子

句子：

```text
小明给小红一本书，因为她很喜欢。
```

当前 Token：

```text
她
```

不同 Head 可能学习出不同的关注模式：

```text
Head 1：

小明   小红   书
 0.2    0.7   0.1

→ 更关注人物之间的关系


Head 2：

小明   小红   书
 0.6    0.1   0.3

→ 可能关注另一种句法关系
```

注意：

> **并不是人为规定 Head 1 负责指代、Head 2 负责语法。**

这些关系是模型训练过程中自己学出来的。

---

## 5. `head_dim` 的真正含义

```text
head_dim = hidden_size / num_heads
```

例如：

```text
hidden_size = 4096
num_heads   = 32

head_dim = 4096 / 32 = 128
```

这里的 `128` 表示：

> **每个 Head 最终使用 128 维的 Q/K/V 表示进行 Attention 计算。**

不是：

```text
Head1 → 原始 X 的第1~128维
Head2 → 原始 X 的第129~256维
```

而是：

```text
完整 X
  ↓
不同 Head 的投影矩阵
  ↓
不同的128维表示
```

---

## 6. Multi-Head Attention 的核心流程

```text
                 X
           [Token,4096]
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
     Head1     Head2     Head3 ...
       ↓         ↓         ↓
    Q₁K₁V₁     Q₂K₂V₂     Q₃K₃V₃
       ↓         ↓         ↓
  Attention  Attention  Attention
       ↓         ↓         ↓
      信息1      信息2      信息3
       └─────────┼─────────┘
                 ↓
                拼接
                 ↓
              Linear
                 ↓
          新的 Hidden State
```

---

## 7. 最核心的理解

### 错误理解

```text
4096维
 ↓
硬切成32份
 ↓
每个Head负责一部分维度
```

### 正确理解

```text
完整 X
 ↓
每个 Head 使用不同的 WQ/WK/WV
 ↓
投影成自己的 128维 Q/K/V
 ↓
独立计算 Attention
 ↓
学习不同的 Token 关系
 ↓
最后把多个 Head 的信息拼起来
```

因此：

> **Multi-Head Attention 的“多头”并不是简单地把特征维度切开，而是让多个独立的投影空间从不同角度观察同一组 Token。**

这也是不同 Head 能够学习不同关系的根本原因。
