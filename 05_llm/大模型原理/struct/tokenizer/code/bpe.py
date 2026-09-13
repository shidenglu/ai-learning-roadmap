from collections import Counter

class SimpleBPE:
    def __init__(self, num_merges=20):
        self.num_merges = num_merges
        self.merges = []

    # --------------------------------
    # 将单词拆成字符
    # --------------------------------
    def get_vocab(self, corpus):
        vocab = []
        for word in corpus:
            chars = list(word)
            vocab.append(chars)
        return vocab

    # --------------------------------
    # 统计相邻字符对频率
    # --------------------------------
    def get_pair_stats(self, vocab):
        pairs = Counter()
        for word in vocab:
            for i in range(len(word)-1):
                pair = (
                    word[i],
                    word[i+1]
                )
                pairs[pair] += 1
        return pairs

    # --------------------------------
    # 执行一次merge
    # --------------------------------
    def merge_pair(
        self,
        pair,
        vocab
    ):

        merged_vocab = []
        bigram = "".join(pair)
        for word in vocab:
            new_word = []
            i = 0
            while i < len(word):
                if (
                    i < len(word)-1
                    and word[i] == pair[0]
                    and word[i+1] == pair[1]
                ):
                    new_word.append(
                        bigram
                    )
                    i += 2
                else:
                    new_word.append(
                        word[i]
                    )
                    i += 1

            merged_vocab.append(
                new_word
            )
        return merged_vocab
    # --------------------------------
    # 训练
    # --------------------------------
    def train(self, corpus):
        vocab = self.get_vocab(corpus)
        print("初始状态\n")
        for w in vocab:
            print(w)
        print("\n开始训练...\n")
        for step in range(self.num_merges):
            pairs = self.get_pair_stats(vocab)
            if not pairs:
                break
            best_pair = max(
                pairs,
                key=pairs.get
            )

            print(
                f"Step {step+1}: "
                f"Merge {best_pair} "
                f"Freq={pairs[best_pair]}"
            )

            self.merges.append(
                best_pair
            )

            vocab = self.merge_pair(
                best_pair,
                vocab
            )
        self.vocab = vocab

    # --------------------------------
    # Tokenize
    # --------------------------------
    def tokenize(self, word):
        tokens = list(word)
        for pair in self.merges:
            merged = "".join(pair)
            i = 0
            new_tokens = []
            while i < len(tokens):
                if (
                    i < len(tokens)-1
                    and tokens[i] == pair[0]
                    and tokens[i+1] == pair[1]
                ):
                    new_tokens.append(
                        merged
                    )
                    i += 2
                else:
                    new_tokens.append(
                        tokens[i]
                    )
                    i += 1
            tokens = new_tokens
        return tokens

# 测试
corpus = [
    "low",
    "lower",
    "lowest",
    "low",
    "low"
]

bpe = SimpleBPE(
    num_merges=10
)

bpe.train(corpus)

# 最终能学习到如下 token
# low
# er
# est