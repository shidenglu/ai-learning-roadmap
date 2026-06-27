# 二维矩阵
import numpy as np

A = np.array([
    [1, 2],
    [3, 4]
])

print(A)

# 矩阵乘法
A = np.array([
    [1,2],
    [3,4]
])

B = np.array([
    [5,6],
    [7,8]
])

C = A @ B

print(C)

# 转置矩阵
A = np.array([
    [1,2,3],
    [4,5,6]
])

print(A.T)

# 求逆
A = np.array([
    [1,2],
    [3,4]
])

A_inv = np.linalg.inv(A)

print(A_inv)