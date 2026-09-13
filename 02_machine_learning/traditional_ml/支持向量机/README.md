# 支持向量机（Support Vector Machine, SVM）完整学习笔记

## 1. SVM 是什么？

支持向量机（SVM）是一种经典的**监督学习算法**，既可以用于：

- 分类（最常见）
- 回归（SVR）

其核心思想是：

> 在特征空间中找到一个“间隔最大”的超平面，将不同类别的数据分开。

---

## 2. 核心思想（一句话理解）

SVM 不只是“找一条分割线”，而是：

> 找到一个**间隔最大（Margin 最大）**的分割超平面。

---

## 3. 几何直觉

在二维空间中：

- 一条直线可以分开两类数据
- SVM 选择的是：**离两类数据最近点最远的那条线**

这些“离边界最近的点”叫：

> 👉 支持向量（Support Vectors）

---

## 4. 超平面表示

### 4.1 线性分类函数

\[
f(x) = w^T x + b
\]

分类规则：

- f(x) ≥ 0 → 正类
- f(x) < 0 → 负类

---

## 5. 间隔（Margin）

SVM 的关键目标：

> 最大化分类间隔

间隔定义为：

\[
Margin = \frac{2}{||w||}
\]

因此：

> 最大化间隔 ⇔ 最小化 ||w||

---

## 6. 优化目标（硬间隔 SVM）

当数据线性可分：

### 目标函数：

\[
\min \frac{1}{2} ||w||^2
\]

### 约束条件：

\[
y_i (w^T x_i + b) \ge 1
\]

其中：

- \( y_i \in \{+1, -1\} \)

---

## 7. 软间隔 SVM（现实情况）

现实数据通常不可完全线性分割，因此引入：

> 松弛变量（Slack Variable）ξ

### 目标函数：

\[
\min \frac{1}{2} ||w||^2 + C \sum \xi_i
\]

### 约束：

\[
y_i (w^T x_i + b) \ge 1 - \xi_i
\]

---

## 8. 参数 C 的意义

C 控制：

- 大 C → 更严格分类（容易过拟合）
- 小 C → 更宽松间隔（更泛化）

---

## 9. 支持向量（最关键概念）

只有少量样本真正影响模型：

> 👉 离分界面最近的点

这些点决定：

- 超平面位置
- 分类边界

其余数据点“几乎不起作用”

---

## 10. 对偶问题（核心数学技巧）

SVM 可以转化为对偶问题：

\[
\max \sum \alpha_i - \frac{1}{2} \sum \alpha_i \alpha_j y_i y_j (x_i \cdot x_j)
\]

约束：

- α_i ≥ 0
- Σ α_i y_i = 0

---

## 11. 核函数（Kernel Trick）

当数据**非线性可分**时：

> 把数据映射到高维空间，使其线性可分

但不直接计算高维映射，而是使用核函数：

---

### 常见核函数

#### 1. 线性核

\[
K(x, x') = x^T x'
\]

---

#### 2. 多项式核

\[
K(x, x') = (x^T x' + c)^d
\]

---

#### 3. RBF 高斯核（最常用）

\[
K(x, x') = exp(-\gamma ||x - x'||^2)
\]

---

## 12. SVM 训练流程

1. 输入数据
2. 选择核函数
3. 构建优化问题
4. 求解 α（拉格朗日乘子）
5. 得到支持向量
6. 构建分类函数

---

## 13. Python 实现（sklearn）

```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 数据
X, y = datasets.load_iris(return_X_y=True)

# 切分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# SVM 模型
model = SVC(kernel='rbf', C=1.0, gamma='scale')

# 训练
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))