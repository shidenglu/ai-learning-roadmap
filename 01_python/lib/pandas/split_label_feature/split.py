# 特征(X)
# ↓
# 模型

# 标签(y)
# ↓
# 监督信号

import pandas as pd

# 读取预训练数据
df = pd.read_csv("train.csv")

X = df[["age", "salary"]]

y = df["label"]

print(X)
print(y)