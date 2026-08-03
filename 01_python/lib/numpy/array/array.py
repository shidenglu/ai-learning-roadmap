# 一维数组
import numpy as np

a = np.array([1, 2, 3, 4])

print(a)

print(type(a))

# 数据计算
a = np.array([1,2,3])

b = np.array([4,5,6])

print(a+b)
print(a-b)
print(a*2)

# 求均值
a = np.array([10,20,30,40])

print(np.mean(a))

# 求和
a = np.array([1,2,3,4])

print(np.sum(a))

# 求最大值
a = np.array([5,8,3,9])

print(np.max(a))

# 生成训练数据
X = np.array([
    [50],
    [60],
    [70],
    [80],
    [90]
])

y = np.array([
    100,
    120,
    140,
    160,
    180
])

print(X)
print(y)

# 计算预测值
X = np.array([50,60,70])

w = 2
b = 0

y_hat = w * X + b

print(y_hat)

# 计算误差
y = np.array([100,120,140])

y_hat = np.array([90,110,150])

error = y - y_hat

print(error)