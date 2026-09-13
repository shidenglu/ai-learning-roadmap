# 大模型（Large Language Model，LLM）原理总结

## 1. 什么是大模型

大模型（Large Language Model，LLM）是一类基于深度学习技术构建的人工智能模型，其核心任务是：

> 根据已有内容预测下一个最可能出现的词（Token）。

例如：

输入：

```text
中国的首都是
```

模型预测：

```text
北京
```

虽然本质上只是不断预测下一个 Token，但当模型规模足够大、训练数据足够丰富时，就能够表现出：

* 对话能力
* 翻译能力
* 编程能力
* 推理能力
* 总结能力
* 知识问答能力

目前主流大模型包括：

* GPT系列
* Claude系列
* Gemini系列
* DeepSeek系列
* Llama系列
* Qwen系列

---

# 2. 大模型整体架构

大模型整体结构如下：

```text
海量文本数据
      │
      ▼
 Token编码
      │
      ▼
 Embedding层
      │
      ▼
 Transformer网络
      │
      ▼
 输出概率分布
      │
      ▼
 预测下一个Token
```

核心组成：

```text
LLM
├── Tokenizer
├── Embedding
├── Positional Encoding
├── Transformer
│   ├── Self-Attention
│   ├── Multi-Head Attention
│   ├── Feed Forward
│   └── LayerNorm
└── Output Layer
```

---

# 3. Token是什么

模型并不认识文字。

例如：

```text
我爱中国
```

首先被Tokenizer切分：

```text
我
爱
中国
```

或者：

```text
我
爱
中
国
```

然后转换成数字：

```text
我      → 1001
爱      → 3021
中国    → 5088
```

得到：

```python
[1001, 3021, 5088]
```

这些数字称为：

```text
Token ID
```

---

# 4. Embedding层

神经网络无法直接处理整数。

例如：

```python
[1001,3021,5088]
```

需要映射成向量：

```python
1001 → [0.23,0.18,-0.51,...]
3021 → [0.44,-0.12,0.88,...]
5088 → [0.77,0.52,0.11,...]
```

假设：

```text
Embedding Dimension = 4096
```

则：

```python
Token
↓
4096维向量
```

Embedding作用：

```text
把离散符号映射到连续向量空间
```

使模型能够学习语义关系。

例如：

```text
北京
上海
广州
```

向量距离较近。

```text
苹果（水果）
香蕉
橘子
```

向量距离较近。

---

# 5. 位置编码（Positional Encoding）

Transformer本身无法感知顺序。

例如：

```text
我爱你
```

与：

```text
你爱我
```

对于普通矩阵计算来说：

```text
Token集合一样
```

因此需要加入位置信息：

```text
我  Position=1
爱  Position=2
你  Position=3
```

最终输入：

```text
Embedding
+
Position Embedding
```

形成：

```text
最终输入向量
```

---

# 6. Transformer架构

Transformer是目前大模型的核心。

2017年Google论文：

《Attention Is All You Need》

提出了Transformer。

结构：

```text
Input
 │
 ▼
Self Attention
 │
 ▼
Feed Forward
 │
 ▼
Self Attention
 │
 ▼
Feed Forward
 │
 ▼
...
```

GPT通常包含：

```text
几十层 ~ 上百层 Transformer Block
```

例如：

```text
GPT-3
96层

GPT-4
上百层

DeepSeek-V3
数百层专家网络
```

---

# 7. Attention机制

这是Transformer最重要的创新。

## 为什么需要Attention

例如：

```text
小明把书放在桌子上，
然后他离开了房间。
```

这里：

```text
他
```

指代：

```text
小明
```

模型需要关注前面内容。

Attention就是：

```text
当前Token
应该关注哪些Token
```

---

# 8. Self-Attention计算过程

对于输入：

```text
X
```

生成：

```text
Q = Query
K = Key
V = Value
```

即：

```text
Q=XWQ
K=XWK
V=XWV
```

计算相关性：

```text
Score = Q × KT
```

得到：

```text
每个Token之间的关联程度
```

然后：

```text
Softmax
```

归一化：

```text
Attention Weight
```

最后：

```text
Output = Weight × V
```

公式：

```math
Attention(Q,K,V)
=
softmax(
QK^T / √dk
)V
```

---

# 9. Multi-Head Attention

单个Attention只能关注一种关系。

例如：

```text
北京是中国的首都
```

可能同时关注：

* 地理关系
* 国家关系
* 语法关系
* 上下文关系

因此设计：

```text
Multi Head Attention
```

多个头同时学习：

```text
Head1
Head2
Head3
...
HeadN
```

最后拼接：

```text
Concat
↓
Linear
```

得到最终结果。

---

# 10. Feed Forward网络

Attention之后：

```text
FFN
```

即：

```python
Linear
↓
GELU/ReLU
↓
Linear
```

作用：

```text
增加非线性表达能力
```

类似于：

```text
特征提取器
```

---

# 11. LayerNorm

深层网络训练时容易不稳定。

因此加入：

```text
LayerNorm
```

作用：

```text
标准化数据
```

使训练更加稳定。

---

# 12. 残差连接（Residual）

Transformer中大量使用：

```text
x
│
├──────┐
│      │
▼      │
Attention
│      │
└──+───┘
   │
   ▼
Output
```

即：

```math
Output = F(x) + x
```

作用：

```text
防止梯度消失
```

提高深层训练效果。

---

# 13. 训练过程

训练目标：

```text
预测下一个Token
```

例如：

输入：

```text
我爱中国
```

训练样本：

```text
输入      标签

我         爱
我爱       中国
我爱中国   <EOS>
```

模型不断学习：

```text
前文
→
下一个词
```

---

# 14. 损失函数

使用：

```text
Cross Entropy
```

交叉熵损失。

例如：

真实：

```text
北京
```

模型预测：

```text
北京 0.8
上海 0.1
广州 0.1
```

损失较小。

如果：

```text
北京 0.1
上海 0.7
广州 0.2
```

损失较大。

---

# 15. 反向传播

训练流程：

```text
Forward
 ↓
Loss
 ↓
Backward
 ↓
Gradient
 ↓
Optimizer
 ↓
Update Weight
```

优化器常用：

```text
AdamW
```

---

# 16. 预训练（Pretraining）

训练数据：

```text
互联网文本
书籍
论文
代码
百科
新闻
论坛
```

规模：

```text
TB级
PB级
```

目标：

```text
学习世界知识
学习语言规律
学习推理模式
```

预训练成本：

```text
数千~数万GPU
持续数月
```

---

# 17. 指令微调（SFT）

预训练后模型只会：

```text
补全文本
```

例如：

```text
用户：
1+1=

模型：
2
3
4
5
...
```

因此进行：

```text
Supervised Fine-Tuning
```

使用：

```text
问题
↓
标准答案
```

进行训练。

使模型学会：

```text
问答
翻译
代码生成
总结
```

---

# 18. RLHF

RLHF：

```text
Reinforcement Learning
from Human Feedback
```

即：

```text
人类反馈强化学习
```

流程：

```text
模型回答
      ↓
人工评分
      ↓
奖励模型
      ↓
强化学习优化
```

作用：

```text
更符合人类偏好
```

例如：

* 更礼貌
* 更安全
* 更有帮助

---

# 19. 推理阶段（Inference）

训练完成后进入推理阶段。

输入：

```text
请介绍Transformer
```

流程：

```text
Tokenize
 ↓
Embedding
 ↓
Transformer
 ↓
概率分布
 ↓
选择下一个Token
 ↓
生成文本
```

不断循环：

```text
Token
→
Token
→
Token
→
...
```

直到：

```text
<EOS>
```

结束。

---

# 20. 大模型为什么需要大量显存

参数规模：

```text
7B  = 70亿参数
13B = 130亿参数
70B = 700亿参数
```

例如：

```text
70B模型
```

FP16存储：

```text
70 × 10^9 × 2 Byte
≈ 140GB
```

因此需要：

```text
多张GPU
```

共同运行。

---

# 21. 涌现能力（Emergent Ability）

当模型规模增大后出现：

```text
推理
数学
编程
规划
工具调用
```

能力突然增强。

这种现象称：

```text
Emergent Ability
```

即：

```text
涌现能力
```

---

# 22. RAG技术

RAG：

```text
Retrieval Augmented Generation
```

即：

```text
检索增强生成
```

流程：

```text
用户问题
     ↓
知识库检索
     ↓
相关文档
     ↓
送入LLM
     ↓
生成答案
```

解决：

```text
知识过时
幻觉问题
```

---

# 23. Agent技术

Agent：

```text
大模型 + 工具
```

例如：

```text
LLM
├── 搜索引擎
├── Python
├── 数据库
├── 文件系统
└── API
```

工作流程：

```text
思考
 ↓
调用工具
 ↓
获取结果
 ↓
继续思考
 ↓
输出答案
```

这也是当前AI发展的重要方向。

---

# 24. 当前主流大模型技术栈

```text
Tokenizer
    ↓
Embedding
    ↓
Positional Encoding
    ↓
Transformer
    ↓
Self Attention
    ↓
Feed Forward
    ↓
Cross Entropy
    ↓
Backpropagation
    ↓
AdamW
    ↓
Pretraining
    ↓
SFT
    ↓
RLHF
    ↓
Inference
```

---

# 25. 一张图看懂大模型

```text
海量数据
    │
    ▼
Tokenizer
    │
    ▼
Embedding
    │
    ▼
Transformer
 ┌──────────────┐
 │ SelfAttention│
 │ MultiHead    │
 │ FFN          │
 │ LayerNorm    │
 └──────────────┘
    │
    ▼
概率分布
    │
    ▼
预测下一个Token
    │
    ▼
生成文本
    │
    ▼
SFT
    │
    ▼
RLHF
    │
    ▼
ChatGPT / DeepSeek / Claude
```

# 总结

大模型的本质可以浓缩为一句话：

> **利用Transformer网络，通过海量数据训练，学习“下一个Token预测”任务，从而获得语言理解、知识记忆、推理、编程和对话能力。**

核心公式：

```math
输入Token
↓
Embedding
↓
Transformer(Self-Attention)
↓
概率分布
↓
预测下一个Token
↓
循环生成文本
```

理解大模型时，重点掌握以下五个核心知识：

1. Token与Embedding
2. Transformer结构
3. Self-Attention机制
4. 预训练与微调
5. 推理生成过程

掌握这五部分，就掌握了现代大模型的核心原理。
