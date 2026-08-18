# Token 详解：大模型中的最小语言单元

## 1. 什么是 Token

在大模型（LLM）中，**Token（词元）** 是模型能够处理的最小语言单位。

可以理解为：

> **Token 是大模型阅读、理解和生成文本时使用的基本单位。**

注意：

```text
Token ≠ 字符
Token ≠ 单词
Token ≠ 汉字
```

它是一种介于字符和单词之间的表示方式。

例如：

```text
Hello World
```

可能被分成：

```text
Hello
World
```

两个 Token。

而：

```text
中华人民共和国
```

可能被分成：

```text
中华
人民
共和国
```

三个 Token。

也可能被分成：

```text
中
华
人
民
共
和
国
```

七个 Token。

具体如何切分取决于 Tokenizer。

---

# 2. 为什么需要 Token

计算机无法直接理解：

```text
你好
Hello
123
😊
```

这些文本。

神经网络只能处理数字。

因此需要：

```text
文本
↓
Token
↓
数字ID
↓
神经网络
```

例如：

```text
我爱中国
```

经过切分：

```text
我
爱
中国
```

再映射为：

```python
[1001, 3021, 5088]
```

模型实际处理的是：

```python
1001
3021
5088
```

而不是文字本身。

---

# 3. Token 的工作流程

完整流程：

```text
用户输入
    │
    ▼
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
    │
    ▼
输出Token
    │
    ▼
文本(Text)
```

例如：

```text
我爱中国
```

经过处理：

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

# 4. Token 与字符的区别

例如：

```text
Hello
```

字符数：

```text
5
```

但 Token 数：

```text
1
```

因为：

```text
Hello
```

可能作为一个完整单词存在于词表中。

---

再例如：

```text
unbelievable
```

可能被拆成：

```text
un
believ
able
```

即：

```text
3 Tokens
```

而字符数：

```text
10+
```

---

# 5. Token 与单词的区别

例如：

```text
playing
```

可能被拆成：

```text
play
ing
```

即：

```text
2 Tokens
```

虽然只有：

```text
1 个单词
```

因此：

```text
Word ≠ Token
```

---

# 6. 中文 Token 示例

中文切分方式与英文不同。

例如：

```text
我爱北京天安门
```

可能被切分：

```text
我
爱
北京
天安门
```

或者：

```text
我
爱
北
京
天
安
门
```

不同模型采用不同策略。

---

# 7. Tokenizer 是什么

Tokenizer（分词器）负责：

```text
文本
↓
Token
```

以及：

```text
Token
↓
数字ID
```

例如：

```text
中国是一个伟大的国家
```

Tokenizer：

```text
中国
是
一个
伟大
的
国家
```

然后转换：

```python
[5088, 11, 120, 8756, 7, 992]
```

---

# 8. Token ID

每个 Token 都对应一个编号。

例如：

```text
Token        ID

中国         5088
美国         6721
日本         2388
```

形成：

```text
Vocabulary（词表）
```

例如：

```text
中国 → 5088
美国 → 6721
北京 → 922
上海 → 1601
```

模型训练过程中：

实际上学习的是：

```text
ID 与 ID 之间的关系
```

---

# 9. Vocabulary（词表）

词表是：

```text
所有 Token 的集合
```

例如：

```text
词表大小

50,000
100,000
200,000
```

现代大模型常见：

```text
32K
50K
100K
200K+
```

例如：

```text
GPT系列
≈100K+
```

```text
Llama系列
≈128K+
```

---

# 10. 特殊 Token

除了普通文字外，还有特殊 Token。

---

## BOS

Beginning Of Sentence

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

End Of Sentence

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

Padding

用于补齐长度：

```text
<PAD>
```

例如：

```text
我 爱 中国 PAD PAD PAD
```

---

## UNK

Unknown

未知词：

```text
<UNK>
```

表示：

```text
词表中不存在
```

---

# 11. Token 与 Embedding 的关系

模型无法直接处理：

```python
[1001,3021,5088]
```

需要映射：

```python
1001
↓
[0.23,0.66,-0.12,...]
```

这一步叫：

```text
Embedding
```

因此：

```text
Token
↓
Token ID
↓
Embedding Vector
```

例如：

```text
中国
↓
5088
↓
4096维向量
```

---

# 12. Token 数量为什么重要

大模型计费通常按照：

```text
Token数量
```

计算。

例如：

```text
输入：
1000 Tokens

输出：
500 Tokens
```

总消耗：

```text
1500 Tokens
```

---

# 13. 上下文窗口（Context Window）

模型一次能够处理的最大 Token 数量。

例如：

```text
4K Tokens
8K Tokens
32K Tokens
128K Tokens
1M Tokens
```

假设：

```text
128K Tokens
```

表示：

```text
一次最多读取约12~20万汉字
```

（实际取决于文本内容）

---

# 14. 大模型如何预测 Token

例如：

输入：

```text
中国的首都是
```

模型内部：

```text
中国的首都是
↓
Token化
↓
Transformer
↓
概率分布
```

输出：

```text
北京      95%
上海       2%
广州       1%
深圳       1%
其他       1%
```

选择：

```text
北京
```

作为下一个 Token。

然后继续：

```text
中国的首都是北京
```

再次预测。

循环执行：

```text
Token
↓
Token
↓
Token
↓
...
```

最终生成完整回答。

---

# 15. Token 在大模型中的地位

可以把大模型比作人类：

```text
人类
↓
认识文字
↓
理解句子
↓
理解文章
```

对应：

```text
LLM
↓
Token
↓
句子
↓
段落
↓
知识
```

因此：

```text
Token
```

就是：

```text
大模型世界里的“文字积木”
```

所有能力：

```text
聊天
翻译
编程
推理
问答
```

最终都建立在：

```text
Token处理
```

之上。

---

# 16. 一张图看懂 Token

```text
用户输入：
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

[4096维向量]

        │
        ▼

Transformer

        │
        ▼

预测下一个Token

        │
        ▼

"。"
```

---

# 总结

Token 是大模型处理文本时的最小单位。

核心流程：

```text
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
Transformer
↓
预测下一个Token
↓
生成文本
```

关键结论：

1. Token 是大模型的基础输入单位。
2. Token 不等于字符，也不等于单词。
3. Token 经过 Tokenizer 转换为数字 ID。
4. Token ID 再转换为向量（Embedding）。
5. Transformer 处理的是向量而不是文字。
6. 大模型本质上是在不断预测下一个 Token。
7. 上下文长度、推理速度、API费用都与 Token 数量直接相关。

一句话理解：

> **Token 就是大模型眼中的“文字积木”，所有语言理解和生成能力，最终都建立在 Token 的表示与预测之上。**
