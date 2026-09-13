# 将数据转换为numpy
import pandas as pd
from sklearn.model_selection import train_test_split

# 读取预训练数据
df = pd.read_csv("train.csv")

X = df[["age","salary"]].values

print(type(X))