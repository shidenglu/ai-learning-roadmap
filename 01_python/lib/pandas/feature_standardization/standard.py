# 特征标准化

import pandas as pd

df = pd.DataFrame({
    "age":[20,25,30],
    "salary":[5000,6000,7000]
})

# 尺度差异太大。会影响梯度下降。
# 结果
# 均值≈0
# 方差≈1
df = (
    df - df.mean()
) / df.std()

print(df)