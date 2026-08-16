# 将数据划分训练集和测试集
from sklearn.model_selection import train_test_split
import pandas as pd

# 读取预训练数据
df = pd.read_csv("train.csv")

X = df[["age","salary"]]
y = df["label"]

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(X)
print(y)