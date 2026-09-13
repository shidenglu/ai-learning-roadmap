import numpy as np
import matplotlib.pyplot as plt

# 固定随机种子
np.random.seed(0)

# x
x = np.arange(1, 11)

# 噪声
noise = np.random.normal(0, 1, len(x))

# y = 2x + 1 + noise
y = 2 * x + 1 + noise

print("x =", x)
print("y =", y)

plt.scatter(x, y)
plt.grid()
plt.show()

n = len(x)

sum_x = np.sum(x)
sum_y = np.sum(y)
sum_x2 = np.sum(x**2)
sum_xy = np.sum(x*y)

a = (n*sum_xy - sum_x*sum_y) / \
    (n*sum_x2 - sum_x**2)

b = (sum_y - a*sum_x) / n

print("斜率 a =", a)
print("截距 b =", b)

y_hat = a*x + b

error = y - y_hat

print(error)

sse = np.sum(error**2)

print("SSE =", sse)

mse = np.mean(error**2)

print("MSE =", mse)

plt.figure(figsize=(8,5))

plt.scatter(x, y, label="data")

plt.plot(
    x,
    y_hat,
    linewidth=2,
    label="least squares"
)

plt.legend()
plt.grid()

plt.show()