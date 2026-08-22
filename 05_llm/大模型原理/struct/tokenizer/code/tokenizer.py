# -*- coding: utf-8 -*-
class MiniTokenizer:
    def __init__(self):
        # 词表
        self.vocab = {
            "中国": 0,
            "北京": 1,
            "上海": 2,
            "人工智能": 3,
            "大模型": 4,
            "学习": 5,
            "深度学习": 6,
            "神经网络": 7,
            "是": 8,
            "一个": 9,
            "重要": 10,
            "领域": 11,
            "我": 12,
            "爱": 13,
            "<UNK>": 999
        }

    def tokenize(self, text):
        tokens = []
        i = 0
        while i < len(text):
            matched = False
            # 最长匹配（4字→3字→2字）
            for length in [4,3,2]:
                if i + length <= len(text):
                    word = text[i:i+length]
                    if word in self.vocab:
                        tokens.append(word)
                        i += length
                        matched = True
                        break
            if matched:
                continue

            # 单字处理
            char = text[i]
            if char.strip():
                tokens.append(char)
            i += 1
        return tokens

    def encode(self, text):
        tokens = self.tokenize(text)
        ids = [
            self.vocab.get(
                token,
                self.vocab["<UNK>"]
            )
            for token in tokens
        ]
        return tokens, ids


tokenizer = MiniTokenizer()

text = """
人工智能是一个重要领域，
深度学习和神经网络推动了大模型的发展。
我爱中国，北京是中国的首都。
"""

tokens, ids = tokenizer.encode(text)

print("原文:")
print(text)

print("\nToken:")
print(tokens)

print("\nToken ID:")
print(ids)

# 统计使用了多少 token
print("\nToken数量:")
print(len(tokens))

# 显示映射关系
for token, id_ in zip(tokens, ids):
    print(f"{token:<10} -> {id_}")