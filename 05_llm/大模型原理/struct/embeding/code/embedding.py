"""
============================================================
Embedding 语义向量实验
============================================================

目标：

    King - Man + Woman ≈ Queen

模拟过程：

    Token
      ↓
    Token ID
      ↓
    Embedding
      ↓
    训练
      ↓
    学习语义空间
      ↓
    King - Man + Woman
      ↓
    找最相似的词
      ↓
    Queen

这是一个教学性质的简化版 Word2Vec / Embedding 实验。

依赖：

    pip install torch matplotlib

============================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt


# ============================================================
# 1. 设置随机种子
# ============================================================

torch.manual_seed(42)


# ============================================================
# 2. 构造一个简单语料
# ============================================================
#
# 我们希望模型能够学习到：
#
#     King  <-> Man
#     Queen <-> Woman
#
# 并且：
#
#     King 和 Queen
#     Man 和 Woman
#
# 具有对应关系。
#
# 这里使用一些非常简单的句子。
#
# ============================================================

sentences = [
    ["king", "man", "royal"],
    ["king", "man", "male"],
    ["king", "man", "prince"],
    ["king", "royal", "male"],
    ["king", "royal", "prince"],

    ["queen", "woman", "royal"],
    ["queen", "woman", "female"],
    ["queen", "woman", "princess"],
    ["queen", "royal", "female"],
    ["queen", "royal", "princess"],

    ["man", "male", "father"],
    ["man", "male", "boy"],
    ["man", "father", "boy"],

    ["woman", "female", "mother"],
    ["woman", "female", "girl"],
    ["woman", "mother", "girl"],

    ["prince", "man", "male"],
    ["prince", "royal", "king"],

    ["princess", "woman", "female"],
    ["princess", "royal", "queen"],

    ["father", "man", "male"],
    ["mother", "woman", "female"],

    ["boy", "man", "male"],
    ["girl", "woman", "female"],
]


# ============================================================
# 3. 创建词表
# ============================================================

vocab = sorted(
    set(
        word
        for sentence in sentences
        for word in sentence
    )
)

word2id = {
    word: i
    for i, word in enumerate(vocab)
}

id2word = {
    i: word
    for word, i in word2id.items()
}

vocab_size = len(vocab)


print("=" * 60)
print("词表")
print("=" * 60)

for word, idx in word2id.items():
    print(f"{idx:2d} -> {word}")

print()
print("词表大小:", vocab_size)


# ============================================================
# 4. 构造 Skip-Gram 训练数据
# ============================================================
#
# Skip-Gram：
#
#     中心词 -> 上下文词
#
# 例如：
#
#     king man royal
#
# 可以产生：
#
#     king -> man
#     king -> royal
#     man  -> king
#     man  -> royal
#     royal -> king
#     royal -> man
#
# window_size = 1
# 表示只看相邻词。
#
# ============================================================

window_size = 1

training_data = []

for sentence in sentences:

    for center_index in range(len(sentence)):

        center_word = sentence[center_index]

        start = max(
            0,
            center_index - window_size
        )

        end = min(
            len(sentence),
            center_index + window_size + 1
        )

        for context_index in range(start, end):

            if context_index == center_index:
                continue

            context_word = sentence[context_index]

            training_data.append(
                (
                    word2id[center_word],
                    word2id[context_word]
                )
            )


print()
print("=" * 60)
print("训练样本数量")
print("=" * 60)

print(len(training_data))


# ============================================================
# 5. 定义 Skip-Gram 模型
# ============================================================
#
# 模型非常简单：
#
#             Token ID
#                ↓
#          Embedding Layer
#                ↓
#            Linear Layer
#                ↓
#          预测上下文词
#
# ============================================================

class SkipGram(nn.Module):

    def __init__(
        self,
        vocab_size,
        embedding_dim
    ):
        super().__init__()

        # Embedding矩阵：
        #
        # vocab_size × embedding_dim
        #
        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim
        )

        # 根据Embedding预测上下文词
        self.linear = nn.Linear(
            embedding_dim,
            vocab_size
        )

    def forward(self, x):

        # Token ID
        #
        # 例如：
        #
        # [king, man, woman]
        #
        # ↓
        #
        # [0, 1, 2]
        #
        embedding = self.embedding(x)

        # Embedding
        #
        # ↓
        #
        # Linear
        #
        output = self.linear(embedding)

        return output


# ============================================================
# 6. 创建模型
# ============================================================

embedding_dim = 20

model = SkipGram(
    vocab_size=vocab_size,
    embedding_dim=embedding_dim
)


# ============================================================
# 7. 查看训练前的Embedding
# ============================================================

print()
print("=" * 60)
print("训练前 Embedding")
print("=" * 60)

before_embedding = model.embedding.weight.detach().clone()

for word in [
    "king",
    "queen",
    "man",
    "woman"
]:

    idx = word2id[word]

    vector = before_embedding[idx]

    print(
        f"{word:6s}: "
        f"{vector[:5].numpy()}"
    )


# ============================================================
# 8. 损失函数和优化器
# ============================================================

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)


# ============================================================
# 9. 开始训练
# ============================================================

epochs = 1000

print()
print("=" * 60)
print("开始训练")
print("=" * 60)

for epoch in range(epochs):

    total_loss = 0.0

    # 打乱训练数据
    indices = torch.randperm(
        len(training_data)
    )

    for index in indices:

        center_id, context_id = training_data[index]

        center = torch.tensor(
            [center_id],
            dtype=torch.long
        )

        target = torch.tensor(
            [context_id],
            dtype=torch.long
        )

        # ----------------------------------------------------
        # 前向传播
        # ----------------------------------------------------

        output = model(center)

        # ----------------------------------------------------
        # 计算Loss
        # ----------------------------------------------------

        loss = criterion(
            output,
            target
        )

        # ----------------------------------------------------
        # 清空梯度
        # ----------------------------------------------------

        optimizer.zero_grad()

        # ----------------------------------------------------
        # 反向传播
        # ----------------------------------------------------

        loss.backward()

        # ----------------------------------------------------
        # 更新参数
        # ----------------------------------------------------

        optimizer.step()

        total_loss += loss.item()

    if epoch % 100 == 0:

        print(
            f"Epoch {epoch:4d} | "
            f"Loss = {total_loss:.4f}"
        )


# ============================================================
# 10. 取出训练后的Embedding
# ============================================================

embedding = model.embedding.weight.detach()


print()
print("=" * 60)
print("训练后 Embedding")
print("=" * 60)

for word in [
    "king",
    "queen",
    "man",
    "woman"
]:

    idx = word2id[word]

    vector = embedding[idx]

    print(
        f"{word:6s}: "
        f"{vector[:5].numpy()}"
    )


# ============================================================
# 11. 计算向量之间的余弦相似度
# ============================================================
#
# cosine similarity：
#
#        A · B
# -------------------
#   ||A|| × ||B||
#
# 越接近1：
#
#     越相似
#
# 越接近0：
#
#     越不相关
#
# ============================================================

def similarity(word1, word2):

    id1 = word2id[word1]
    id2 = word2id[word2]

    v1 = embedding[id1]
    v2 = embedding[id2]

    return F.cosine_similarity(
        v1.unsqueeze(0),
        v2.unsqueeze(0)
    ).item()


print()
print("=" * 60)
print("词向量相似度")
print("=" * 60)

pairs = [
    ("king", "queen"),
    ("man", "woman"),
    ("king", "man"),
    ("queen", "woman"),
    ("king", "girl"),
    ("man", "girl"),
]

for word1, word2 in pairs:

    sim = similarity(
        word1,
        word2
    )

    print(
        f"{word1:6s} <-> "
        f"{word2:6s} : "
        f"{sim:.4f}"
    )


# ============================================================
# 12. 最重要的部分
#
#     King - Man + Woman
#
# ============================================================

king_vector = embedding[
    word2id["king"]
]

man_vector = embedding[
    word2id["man"]
]

woman_vector = embedding[
    word2id["woman"]
]


# ============================================================
# 计算：
#
#     King - Man + Woman
#
# ============================================================

result_vector = (
    king_vector
    - man_vector
    + woman_vector
)


# ============================================================
# 13. 在整个词表中寻找最相似的词
# ============================================================

similarities = F.cosine_similarity(
    result_vector.unsqueeze(0),
    embedding
)


# 从大到小排序
sorted_indices = torch.argsort(
    similarities,
    descending=True
)


print()
print("=" * 60)
print("King - Man + Woman")
print("=" * 60)

print()
print(
    "我们希望得到："
)

print(
    "King - Man + Woman ≈ Queen"
)

print()
print("计算结果：")
print()


# ============================================================
# 14. 输出最接近的词
# ============================================================

for rank, idx in enumerate(
    sorted_indices[:10]
):

    word = id2word[idx.item()]

    score = similarities[
        idx
    ].item()

    print(
        f"{rank + 1:2d}. "
        f"{word:10s} "
        f"similarity = {score:.4f}"
    )


# ============================================================
# 15. 单独查看 Queen 的相似度
# ============================================================

queen_id = word2id["queen"]

queen_similarity = similarities[
    queen_id
].item()


print()
print("=" * 60)
print("最终结果")
print("=" * 60)

print()

print(
    f"King - Man + Woman"
)

print(
    f"Queen similarity = "
    f"{queen_similarity:.4f}"
)


# ============================================================
# 16. 分析向量关系
# ============================================================
#
# 计算：
#
#     King - Man
#
# 和：
#
#     Queen - Woman
#
# 如果两者接近，说明模型学习到了：
#
#     Man -> King
#
#     Woman -> Queen
#
# 这种对应关系。
#
# ============================================================

king_man = (
    king_vector
    - man_vector
)

queen_woman = (
    embedding[word2id["queen"]]
    - woman_vector
)


relation_similarity = F.cosine_similarity(
    king_man.unsqueeze(0),
    queen_woman.unsqueeze(0)
).item()


print()
print("=" * 60)
print("语义关系")
print("=" * 60)

print()
print(
    "King - Man"
)

print(
    "≈"
)

print(
    "Queen - Woman"
)

print()

print(
    "关系向量余弦相似度 = "
    f"{relation_similarity:.4f}"
)


# ============================================================
# 17. 可视化Embedding
# ============================================================
#
# Embedding实际上是20维。
#
# 为了方便观察：
#
#     使用PCA
#
# 把20维压缩到2维。
#
# ============================================================

def pca_2d(matrix):

    # 去中心化
    matrix = matrix - matrix.mean(
        dim=0,
        keepdim=True
    )

    # SVD
    U, S, V = torch.pca_lowrank(
        matrix,
        q=2
    )

    # 投影到二维
    result = matrix @ V[:, :2]

    return result


embedding_2d = pca_2d(
    embedding
)


# ============================================================
# 18. 绘制Embedding空间
# ============================================================

plt.figure(
    figsize=(10, 8)
)

for i, word in id2word.items():

    x = embedding_2d[i, 0].item()
    y = embedding_2d[i, 1].item()

    plt.scatter(
        x,
        y
    )

    plt.text(
        x + 0.02,
        y + 0.02,
        word,
        fontsize=12
    )


plt.title(
    "Learned Word Embedding"
)

plt.xlabel(
    "PCA Dimension 1"
)

plt.ylabel(
    "PCA Dimension 2"
)

plt.grid(
    True,
    alpha=0.3
)

plt.show()


# ============================================================
# 19. 最终总结
# ============================================================
#
# 整个过程实际上就是：
#
#
# Token
#   ↓
# Token ID
#   ↓
# Embedding Lookup
#   ↓
# 向量
#   ↓
# Neural Network
#   ↓
# Loss
#   ↓
# Backpropagation
#   ↓
# 更新Embedding
#
#
# 训练很多次以后：
#
#     King
#     Queen
#     Man
#     Woman
#
# 在向量空间中形成某种结构。
#
#
# 最后：
#
#     King - Man + Woman
#
# 得到一个新的向量。
#
# 再在整个词表中寻找：
#
#     cosine_similarity(result, word)
#
# 最大的词。
#
# 如果训练得好：
#
#     Queen
#
# 就会排在非常靠前的位置。
#
#
# 注意：
#
#     "King - Man + Woman = Queen"
#
# 并不是Embedding层被人为规定的公式。
#
# 而是：
#
#     训练数据
#          ↓
#     梯度下降
#          ↓
#     Embedding参数不断更新
#          ↓
#     语义关系逐渐形成
#
# ============================================================
