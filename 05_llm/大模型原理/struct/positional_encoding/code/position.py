import numpy as np


# ============================================================
# 1. 模拟 Token Embedding
# ============================================================

embedding = {
    "我": np.array([1.0, 0.0]),
    "爱": np.array([0.0, 1.0]),
    "你": np.array([1.0, 1.0]),
}


# ============================================================
# 2. 两个 Token 完全一样，只是顺序不同
# ============================================================

sentence1 = ["我", "爱", "你"]
sentence2 = ["你", "爱", "我"]


# ============================================================
# 3. 不使用位置编码
# ============================================================

def encode_without_position(sentence):
    vectors = []

    for token in sentence:
        vectors.append(embedding[token])

    return np.array(vectors)


# ============================================================
# 4. 使用简单的位置编码
# ============================================================

position_embedding = {
    0: np.array([0.0, 0.0]),
    1: np.array([0.0, 1.0]),
    2: np.array([1.0, 0.0]),
}


def encode_with_position(sentence):
    vectors = []

    for position, token in enumerate(sentence):

        token_vector = embedding[token]

        position_vector = position_embedding[position]

        # Token Embedding + Position Embedding
        vector = token_vector + position_vector

        vectors.append(vector)

    return np.array(vectors)


# ============================================================
# 5. 打印结果
# ============================================================

print("=" * 60)
print("不使用位置编码")
print("=" * 60)

x1 = encode_without_position(sentence1)
x2 = encode_without_position(sentence2)

print("句子1：", sentence1)
print(x1)

print()

print("句子2：", sentence2)
print(x2)


# ============================================================
# 6. 看看整个序列的信息是否一样
# ============================================================

print()
print("不使用位置编码：")

sum1 = x1.sum(axis=0)
sum2 = x2.sum(axis=0)

print("句子1所有 Token 的向量和：", sum1)
print("句子2所有 Token 的向量和：", sum2)

print("是否相同：", np.allclose(sum1, sum2))


# ============================================================
# 7. 加入位置编码
# ============================================================

print()
print("=" * 60)
print("加入位置编码")
print("=" * 60)

x1_pos = encode_with_position(sentence1)
x2_pos = encode_with_position(sentence2)

print("句子1：", sentence1)
print(x1_pos)

print()

print("句子2：", sentence2)
print(x2_pos)


# ============================================================
# 8. 再次比较
# ============================================================

print()
print("加入位置编码以后：")

sum1_pos = x1_pos.sum(axis=0)
sum2_pos = x2_pos.sum(axis=0)

print("句子1所有 Token 的向量和：", sum1_pos)
print("句子2所有 Token 的向量和：", sum2_pos)

print("是否相同：", np.allclose(sum1_pos, sum2_pos))


# ============================================================
# 9. 单独观察“我”
# ============================================================

print()
print("=" * 60)
print("观察同一个 Token：我")
print("=" * 60)

print()

print("句子1：我 爱 你")

print("我的位置：0")
print("我 + position0：",
      embedding["我"] + position_embedding[0])

print()

print("句子2：你 爱 我")

print("我的位置：2")
print("我 + position2：",
      embedding["我"] + position_embedding[2])