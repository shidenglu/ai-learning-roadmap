# 查看：

# 样本数量
# 特征数量
# 是否有缺失值
# 数据类型

import pandas as pd

# 读取预训练数据
df = pd.read_csv("train.csv")

# 查看数据基本信息

# 样本数量
print("样本数量:", df.shape[0])

# 特征数量
print("特征数量:", df.shape[1])

# 是否有缺失值
print("缺失值情况:")
print(df.isnull().sum())

# 数据类型
print("数据类型:")
print(df.dtypes)

print(df.head())
print(df.info())
print(df.describe())
print(df.shape)