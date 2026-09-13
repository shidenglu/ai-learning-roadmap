# 数据转 tensor
import pandas as pd
import torch

df = pd.read_csv("train.csv")

# 特征
X = df[["age", "salary"]]

# 标签
y = df["label"]

# Pandas -> NumPy -> Tensor
X = torch.tensor(
    X.to_numpy(),
    dtype=torch.float32
)

y = torch.tensor(
    y.to_numpy(),
    dtype=torch.float32
)

print("X:")
print(X)

print("X shape:")
print(X.shape)

print("y:")
print(y)

print("y shape:")
print(y.shape)