# Tokenizer 原理详解：大模型文本处理的第一步

## 1. 什么是 Tokenizer

Tokenizer（分词器）是大模型处理文本的第一步。

其作用是：

> **将人类可读的文本转换成模型能够处理的 Token 序列。**

大模型本身无法直接理解：

```text
你好
Hello
123
😊
```

这些字符。

神经网络只能处理数字，因此需要先经过 Tokenizer 处理。

整体流程：

```text
用户输入文本
       │
       ▼
   Tokenizer
       │
       ▼
 Token序列
       │
       ▼
 Token ID序列
       │
       ▼
 Embedding
       │
       ▼
 Transformer
```

---

# 2. 为什么需要 Tokenizer

假设输入：

```text
我爱中国
```

计算机看到的是：

```text
25105
29233
20013
22269
```

（Unicode编码）

这些数字本身没有语义关系。

而模型需要的是：

```text
我
爱
中国
```

这样的语言单位。

因此需要：

```text
文本
↓
切分
↓
Token
↓
数字ID
```

这个过程由 Tokenizer 完成。

---

# 3. Tokenizer 的核心任务

Tokenizer主要完成两件事：

## 文本切分（Tokenization）

例如：

```text
我爱中国
```

切分后：

```text
我
爱
中国
```

---

## Token映射

建立词表（Vocabulary）：

```text
我       → 1001
爱       → 3021
中国     → 5088
```

得到：

```python
[1001,3021,5088]
```

最终送入神经网络。

---

# 4. Tokenizer 工作流程

完整流程：

```text
文本(Text)
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
Transformer
```

例如：

```text
我爱中国
```

处理过程：

```text
我爱中国
    ↓
["我","爱","中国"]
    ↓
[1001,3021,5088]
    ↓
Embedding
    ↓
Transformer
```

---

# 5. 最简单的 Tokenizer

按照字符切分：

```text
我爱中国
```

得到：

```text
我
爱
中
国
```

即：

```python
["我","爱","中","国"]
```

优点：

* 简单

缺点：

* Token数量太多
* 语义表达能力差

例如：

```text
中国
```

被拆成：

```text
中
国
```

会丢失整体语义。

---

# 6. 按单词切分

英文常用：

```text
I love China
```

切分：

```python
["I","love","China"]
```

优点：

* 保留完整语义

缺点：

```text
词表巨大
```

例如：

```text
run
running
runner
runs
```

都需要单独存储。

导致：

```text
Vocabulary爆炸
```

---

# 7. 子词（Subword）切分

现代大模型普遍采用：

```text
Subword Tokenization
```

即：

```text
介于字符和单词之间
```

例如：

```text
unbelievable
```

切分：

```text
un
believ
able
```

变成：

```python
["un","believ","able"]
```

优点：

* 词表小
* 泛化能力强
* 可以处理新词

因此成为主流方案。

---

# 8. Vocabulary（词表）

Tokenizer训练完成后生成：

```text
Vocabulary
```

即：

```text
Token → ID
```

映射表。

例如：

```text
Token        ID

中国         5088
美国         6721
日本         2388
北京         922
上海         1601
```

模型训练过程中：

实际处理的是：

```python
[5088,922]
```

而不是：

```text
中国 北京
```

---

# 9. 编码过程（Encode）

输入：

```text
中国是一个伟大的国家
```

Tokenizer：

```python
["中国","是","一个","伟大","的","国家"]
```

再映射：

```python
[5088,11,120,8756,7,992]
```

称为：

```text
Encoding
```

即：

```text
文本
↓
Token ID
```

---

# 10. 解码过程（Decode）

模型输出：

```python
[5088,11,120]
```

Tokenizer再转换：

```text
中国
是
一个
```

最终：

```text
中国是一个
```

称为：

```text
Decoding
```

即：

```text
Token ID
↓
文本
```

---

# 11. 特殊 Token

除了普通词汇外，还包含特殊Token。

---

## BOS

句子开始：

```text
<BOS>
```

例如：

```text
<BOS> 我爱中国
```

---

## EOS

句子结束：

```text
<EOS>
```

例如：

```text
我爱中国 <EOS>
```

---

## PAD

长度补齐：

```text
<PAD>
```

例如：

```text
我 爱 中国 PAD PAD PAD
```

---

## UNK

未知词：

```text
<UNK>
```

表示：

```text
词表中不存在
```

---

# 12. 主流 Tokenizer 算法

现代大模型主要使用以下算法。

---

## WordPiece

Google提出。

典型模型：

```text
BERT
```

示例：

```text
playing
```

切分：

```text
play
##ing
```

---

## BPE

Byte Pair Encoding

GPT系列最常使用。

核心思想：

```text
频繁出现的字符组合
↓
合并
```

例如：

```text
l
o
w
```

逐渐学习：

```text
low
```

作为一个Token。

---

## SentencePiece

Google提出。

特点：

```text
直接处理原始文本
```

无需预分词。

典型模型：

```text
Llama
T5
ALBERT
```

---

## Unigram

SentencePiece中的另一种实现。

思想：

```text
从大量候选Token中
寻找最优组合
```

---

# 13. GPT为什么使用BPE

因为BPE兼顾：

```text
词表大小
训练效率
泛化能力
```

例如：

```text
ChatGPT
GPT-2
GPT-3
GPT-4
```

均采用：

```text
BPE变种
```

Tokenizer。

---

# 14. 中文 Tokenizer 的特点

中文没有天然空格。

例如：

```text
我爱北京天安门
```

Tokenizer需要自动判断：

方案1：

```text
我
爱
北京
天安门
```

方案2：

```text
我
爱
北
京
天
安
门
```

现代模型通常采用：

```text
BPE
SentencePiece
```

自动学习最优切分方式。

---

# 15. Tokenizer 为什么影响模型性能

Tokenizer直接决定：

```text
文本如何表示
```

例如：

```text
中国
```

如果拆成：

```text
中
国
```

模型需要：

```text
两次Attention
```

才能理解。

如果直接：

```text
中国
```

作为一个Token：

```text
一次Attention
```

即可。

因此：

```text
优秀Tokenizer
=
更高效率
=
更强性能
```

---

# 16. Tokenizer 与上下文长度

假设：

```text
Context Length = 128K Tokens
```

如果Tokenizer切分效率高：

```text
1 Token ≈ 1~2汉字
```

则：

```text
可容纳更多文本
```

如果切分效率低：

```text
1 Token ≈ 0.5汉字
```

则：

```text
有效上下文减少
```

因此Tokenizer会直接影响：

* 上下文容量
* 推理速度
* 显存占用
* API费用

---

# 17. HuggingFace 示例

加载Tokenizer：

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "bert-base-chinese"
)
```

编码：

```python
text = "我爱中国"

ids = tokenizer.encode(text)

print(ids)
```

输出：

```python
[101,2769,4263,704,1744,102]
```

解码：

```python
print(
    tokenizer.decode(ids)
)
```

输出：

```text
我爱中国
```

---

# 18. Tokenizer 在大模型中的位置

整体架构：

```text
用户输入
    │
    ▼
Tokenizer
    │
    ▼
Token ID
    │
    ▼
Embedding
    │
    ▼
Transformer
    │
    ▼
输出Token ID
    │
    ▼
Tokenizer Decode
    │
    ▼
最终文本
```

Tokenizer是：

```text
人类语言
与
神经网络
之间的翻译器
```

---

# 19. 一张图看懂 Tokenizer

```text
输入文本

"我爱中国"

     │
     ▼

Tokenizer

     │
     ▼

["我","爱","中国"]

     │
     ▼

[1001,3021,5088]

     │
     ▼

Embedding

     │
     ▼

Transformer

     │
     ▼

[1001,3021,5088,999]

     │
     ▼

Decode

     │
     ▼

"我爱中国。"
```

---

# 总结

Tokenizer 是大模型处理文本的第一步。

核心职责：

```text
文本
↓
Token
↓
Token ID
```

以及：

```text
Token ID
↓
文本
```

关键知识点：

1. Tokenizer负责文本切分和编号映射。
2. 模型处理的是Token ID，而不是文字。
3. Vocabulary保存Token与ID的映射关系。
4. 主流算法包括BPE、WordPiece、SentencePiece。
5. GPT系列主要使用BPE。
6. Tokenizer质量会影响模型性能和上下文长度。
7. Tokenizer是连接自然语言和神经网络的桥梁。

一句话理解：

> **Tokenizer 是大模型的“语言翻译器”，负责把人类语言转换为模型能够理解的 Token 和数字 ID，再把模型输出重新转换成人类可读的文本。**
