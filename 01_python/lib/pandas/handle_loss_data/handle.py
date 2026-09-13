# 真实数据经常有缺失值。

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "age":[20,25,np.nan,22],
    "salary":[5000,6000,7000,np.nan]
})

print(df)

# 擦看缺失值
print(df.isnull().sum())

# 使用均值填充
df["age"] = df["age"].fillna(
    df["age"].mean()
)

df["salary"] = df["salary"].fillna(
    df["salary"].mean()
)

print(df)