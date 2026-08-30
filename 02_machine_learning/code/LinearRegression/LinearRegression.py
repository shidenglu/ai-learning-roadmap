import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 训练数据
X = np.array([
    [50],
    [60],
    [70],
    [80],
    [90]
])

y = np.array([
    150,
    180,
    210,
    240,
    270
])

# 创建模型
model = LinearRegression()

# 训练
model.fit(X, y)

# 输出模型参数
print("权重 w =", model.coef_[0])
print("偏置 b =", model.intercept_)

# 预测
area = np.array([[75]])

price = model.predict(area)

print("75㎡预测房价 =", price[0])

# 绘图
plt.scatter(X, y, label="Train Data")
plt.plot(X, model.predict(X), label="Regression Line")

plt.xlabel("Area")
plt.ylabel("Price")
plt.legend()

plt.show()