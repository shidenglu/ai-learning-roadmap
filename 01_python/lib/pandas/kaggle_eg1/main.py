import pandas as pd
import torch
from sklearn.model_selection import train_test_split

# ============================================================
# 1. 读取数据
# ============================================================
df = pd.read_csv("train.csv")
print("=" * 60)
print("原始数据")
print("=" * 60)
print(df)
# ============================================================
# 2. 查看数据基本信息
# ============================================================
print("\n" + "=" * 60)
print("前5行")
print("=" * 60)
print(df.head())
print("\n" + "=" * 60)
print("数据基本信息")
print("=" * 60)
df.info()
print("\n" + "=" * 60)
print("统计信息")
print("=" * 60)
print(df.describe())
# ============================================================
# 3. 查看缺失值
# ============================================================
print("\n" + "=" * 60)
print("缺失值统计")
print("=" * 60)
print(df.isnull().sum())
# ============================================================
# 4. 删除无用列
# ============================================================
print("\n" + "=" * 60)
print("删除 Id")
print("=" * 60)
df = df.drop(columns=["Id"])
print(df)
# ============================================================
# 5. 处理数值特征缺失值
# ============================================================
print("\n" + "=" * 60)
print("处理缺失值")
print("=" * 60)
# Age 使用平均值填充
df["Age"] = df["Age"].fillna(
    df["Age"].mean()
)

# Salary 使用平均值填充
df["Salary"] = df["Salary"].fillna(
    df["Salary"].mean()
)

print(df)
print("\n处理之后的缺失值：")
print(df.isnull().sum())
# ============================================================
# 6. 类别特征 One-Hot 编码
# ============================================================
print("\n" + "=" * 60)
print("One-Hot 编码")
print("=" * 60)

df = pd.get_dummies(
    df,
    columns=["Gender", "City"],
    dtype=int
)

print(df)
# ============================================================
# 7. 分离特征 X 和标签 y
# ============================================================
print("\n" + "=" * 60)
print("分离 X 和 y")
print("=" * 60)

X = df.drop(columns=["Buy"])

y = df["Buy"]

print("X:")
print(X)
print("\ny:")
print(y)
# ============================================================
# 8. 查看 X 和 y 的形状
# ============================================================
print("\n" + "=" * 60)
print("数据形状")
print("=" * 60)
print("X shape:", X.shape)
print("y shape:", y.shape)
# ============================================================
# 9. 划分训练集和测试集
# ============================================================
print("\n" + "=" * 60)
print("划分训练集和测试集")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("X_train:")
print(X_train)
print("\nX_test:")
print(X_test)
print("\ny_train:")
print(y_train)
print("\ny_test:")
print(y_test)
# ============================================================
# 10. Pandas -> NumPy
# ============================================================
print("\n" + "=" * 60)
print("Pandas -> NumPy")
print("=" * 60)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()

y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

print("X_train type:", type(X_train))
print("y_train type:", type(y_train))
# ============================================================
# 11. NumPy -> PyTorch Tensor
# ============================================================
print("\n" + "=" * 60)
print("NumPy -> PyTorch Tensor")
print("=" * 60)

X_train = torch.tensor(
    X_train,
    dtype=torch.float32
)

X_test = torch.tensor(
    X_test,
    dtype=torch.float32
)

y_train = torch.tensor(
    y_train,
    dtype=torch.float32
)

y_test = torch.tensor(
    y_test,
    dtype=torch.float32
)
# ============================================================
# 12. 查看最终结果
# ============================================================
print("X_train:")
print(X_train)
print("\nX_train shape:")
print(X_train.shape)
print("\ny_train:")
print(y_train)
print("\ny_train shape:")
print(y_train.shape)