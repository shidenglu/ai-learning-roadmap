# Attention：有无 Attention 的 Softmax 数值对比

## 1. 核心问题

Attention 的作用可以简单理解为：

> **让当前 Token 根据上下文，从其他 Token 中获取有用信息，从而形成更准确的上下文表示。**

最终预测流程：

```text
Token
  ↓
Attention
  ↓
Context-aware Hidden State
  ↓
Linear
  ↓
Logits
  ↓
Softmax
  ↓
下一个 Token 的概率
```

---

## 2. 示例句子

假设输入：

```text
小明昨天在商店买了一部新手机，回到家以后发现手机的屏幕已经出现了裂痕
```

当前正在预测：

```text
裂痕
```

为了方便演示，假设每个 Token 只有 **2 维向量**。

---

# 3. 没有 Attention

没有 Attention 时，可以构造一个最简单的对比模型：

> 当前 Token 只能使用自己的表示，不读取其他 Token 的上下文。

假设：

```text
裂痕 = [1.0, 0.0]
```

经过 Linear：

```text
Logits：

严重    1.2
轻微    1.0
正常    0.8
漂亮    0.7
```

经过 Softmax：

```text
严重    31.7%
轻微    25.9%
正常    21.2%
漂亮    21.2%
```

模型无法充分利用：

```text
手机
屏幕
发现
出现
```

这些上下文信息。

---

# 4. 有 Attention

有 Attention 后，“裂痕”可以查看前面的 Token。

假设 Attention 得到：

```text
Token       Attention Weight

小明             0.03
昨天             0.01
在               0.01
商店             0.02
买               0.03
了               0.01
一部             0.01
新               0.02
手机             0.25
回到             0.01
家               0.01
以后             0.01
发现             0.12
手机             0.20
的               0.01
屏幕             0.35
已经             0.03
出现             0.07
了               0.01
裂痕             0.01
```

可以看到，“裂痕”重点关注：

```text
手机
屏幕
发现
出现
```

---

# 5. Attention 如何融合信息

假设：

```text
V手机 = [1.0, 0.8]
V屏幕 = [0.9, 1.0]
V发现 = [0.2, 0.5]
V出现 = [0.3, 0.4]
```

那么：

```text
Attention Output
=
0.25 × V手机
+ 0.20 × V手机
+ 0.35 × V屏幕
+ 0.12 × V发现
+ 0.07 × V出现
+ ...
```

得到：

```text
Attention Output ≈ [0.81, 0.798]
```

于是：

```text
原始表示：

裂痕
↓
[1.0, 0.0]


Attention 后：

裂痕
↓
[0.81, 0.798]
```

也就是说：

> **Attention 将上下文信息融合到了“裂痕”的表示中。**

---

# 6. 最终 Softmax

Attention 后：

```text
Hidden State = [0.81, 0.798]
```

经过输出 Linear：

```text
Logits：

严重    4.014
轻微   -2.007
正常    0.565
漂亮   -0.565
```

Softmax：

```text
严重    ≈ 96.0%
轻微    ≈  0.2%
正常    ≈  3.0%
漂亮    ≈  0.8%
```

最终模型明显更倾向于：

```text
严重
```

---

# 7. 两种模型对比

## 没有 Attention

```text
裂痕
 ↓
[1.0, 0.0]
 ↓
Linear
 ↓
[1.2, 1.0, 0.8, 0.7]
 ↓
Softmax
 ↓
[31.7%, 25.9%, 21.2%, 21.2%]
```

## 有 Attention

```text
裂痕
 ↓
查看上下文
 ↓
手机、屏幕、发现、出现
 ↓
信息融合
 ↓
[0.81, 0.798]
 ↓
Linear
 ↓
[4.014, -2.007, 0.565, -0.565]
 ↓
Softmax
 ↓
[96.0%, 0.2%, 3.0%, 0.8%]
```

---

# 8. 为什么 Softmax 结果会不同？

关键不是 Softmax 本身。

Softmax 只是把 Logits 转换成概率。

真正发生变化的是：

```text
上下文
  ↓
Attention
  ↓
Hidden State 改变
  ↓
Linear
  ↓
Logits 改变
  ↓
Softmax
  ↓
概率改变
```

因此：

```text
Attention
    ↓
改变 Hidden State
    ↓
改变 Logits
    ↓
改变 Softmax
    ↓
改变预测结果
```

---

# 9. Attention 的本质

可以把 Attention 理解成：

> **当前 Token 主动去上下文中“找信息”，然后把找到的信息融合到自己的向量中。**

例如：

```text
裂痕
 ↓
“我需要什么信息？”
 ↓
找到：
  手机
  屏幕
  出现
  发现
 ↓
融合这些信息
 ↓
得到新的“裂痕”表示
```

所以 Attention 的核心不是：

```text
简单地看其他 Token
```

而是：

```text
找到相关 Token
      ↓
按照相关程度分配权重
      ↓
提取它们的 Value
      ↓
加权融合
      ↓
得到新的上下文表示
```

---

# 10. 一句话总结

```text
没有 Attention：

Token → 自己的表示 → 预测


有 Attention：

Token
 ↓
查看上下文
 ↓
提取相关信息
 ↓
融合上下文
 ↓
新的 Hidden State
 ↓
预测
```

**Attention 的本质：让 Token 从“孤立的词向量”变成“结合上下文后的动态表示”。**

> 注：上面的数值是为了演示 Attention 原理而人为构造的教学数据，不代表真实训练好的 LLM 的实际输出。
