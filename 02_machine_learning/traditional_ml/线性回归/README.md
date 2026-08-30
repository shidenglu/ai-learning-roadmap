# 线性回归（Linear Regression）学习笔记

## 1. 概述

线性回归（Linear Regression）是一种用于**回归问题**的基础机器学习模型，用来预测连续数值。

其核心思想是：

> 假设输入特征与输出之间存在线性关系，用一条直线（或超平面）去拟合数据。

---

## 2. 模型定义

### 2.1 一元线性回归

当只有一个特征时：

\[
y = wx + b
\]

其中：

- \( x \)：输入特征
- \( w \)：权重（斜率）
- \( b \)：偏置（截距）
- \( y \)：预测值

---

### 2.2 多元线性回归

当有多个特征时：

\[
y = w_1x_1 + w_2x_2 + ... + w_nx_n + b
\]

向量形式：

\[
y = Xw + b
\]

---

## 3. 目标函数

线性回归的目标是：

> 找到一组参数 \( w, b \)，使预测值与真实值误差最小。

---

## 4. 损失函数（Loss Function）

常用均方误差（MSE）：

\[
L = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
\]

其中：

- \( y_i \)：真实值
- \( \hat{y}_i \)：预测值

---

## 5. 为什么使用 MSE

使用均方误差的原因：

- 避免正负误差抵消
- 强化大误差惩罚
- 数学性质良好（可导、凸函数）

---

## 6. 参数求解方法

### 6.1 解析解（最小二乘法）

\[
w = (X^T X)^{-1} X^T y
\]

优点：
- 直接计算
- 不需要迭代

缺点：
- 计算复杂度高
- 不适用于大规模数据

---

### 6.2 梯度下降法（Gradient Descent）

参数更新：

\[
w := w - \eta \frac{\partial L}{\partial w}
\]

\[
b := b - \eta \frac{\partial L}{\partial b}
\]

其中：

- \( \eta \)：学习率

---

## 7. 梯度推导

损失函数：

\[
L = \frac{1}{n} \sum (Xw + b - y)^2
\]

梯度：

\[
\frac{\partial L}{\partial w} = \frac{2}{n} X^T (Xw + b - y)
\]

\[
\frac{\partial L}{\partial b} = \frac{2}{n} \sum (Xw + b - y)
\]

---

## 8. 训练流程

1. 初始化参数 \( w, b \)
2. 前向计算预测值
3. 计算损失函数
4. 计算梯度
5. 更新参数
6. 重复直到收敛

---

## 9. NumPy 实现

```python
import numpy as np

# 数据
X = np.array([[1], [2], [3], [4]])
y = np.array([[2], [4], [6], [8]])

# 参数初始化
w = np.random.randn(1, 1)
b = np.zeros((1, 1))

lr = 0.01
epochs = 1000
n = len(X)

# 训练
for epoch in range(epochs):
    y_pred = X @ w + b
    
    loss = np.mean((y_pred - y) ** 2)

    dw = (2/n) * X.T @ (y_pred - y)
    db = (2/n) * np.sum(y_pred - y)

    w -= lr * dw
    b -= lr * db

print("w:", w)
print("b:", b)