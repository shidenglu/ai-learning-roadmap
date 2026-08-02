# 正规方程
import numpy as np

X = np.array([
    [1,1],
    [2,1],
    [3,1]
])

y = np.array([
    [3],
    [6],
    [9]
])

theta = np.linalg.inv(
    X.T @ X
) @ X.T @ y

print(theta)

# 提取 w 和 b
w = theta[0,0]
b = theta[1,0]

print(w)
print(b)