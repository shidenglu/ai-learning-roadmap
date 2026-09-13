# NumPy 学习指南

> 面向机器学习与深度学习的 NumPy 入门教程

---

# 目录

* 什么是 NumPy
* ndarray
* shape
* dtype
* 创建数组
* 索引(Index)
* 切片(Slice)
* reshape
* concatenate
* 统计函数
* 广播机制(Broadcast)
* 矩阵运算
* NumPy 在线性回归中的应用
* NumPy 学习路线

---

# 1. 什么是 NumPy

## 1.1 NumPy简介

NumPy（Numerical Python）是 Python 中最重要的科学计算库。

官方定义：

```text
NumPy is the fundamental package for scientific computing with Python.
```

简单理解：

```text
Python负责流程控制

NumPy负责数学计算
```

---

## 1.2 为什么需要 NumPy

普通 Python：

```python
a = [1,2,3]
b = [4,5,6]

c = []

for i in range(len(a)):
    c.append(a[i] + b[i])

print(c)
```

NumPy：

```python
import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])

c = a + b

print(c)
```

优点：

* 速度快
* 内存占用少
* 支持矩阵运算
* 支持向量化计算
* 机器学习基础库

---

# 2. ndarray

## 2.1 什么是 ndarray

NumPy 的核心数据结构：

```python
import numpy as np

a = np.array([1,2,3])

print(type(a))
```

输出：

```python
<class 'numpy.ndarray'>
```

---

含义：

```text
nd = N Dimension
array = 数组
```

即：

```text
N维数组
```

---

## 2.2 一维数组

```python
a = np.array([1,2,3,4])

print(a)
```

输出：

```python
[1 2 3 4]
```

---

## 2.3 二维数组

```python
A = np.array([
    [1,2],
    [3,4]
])

print(A)
```

输出：

```python
[[1 2]
 [3 4]]
```

数学表示：

```text
|1 2|
|3 4|
```

---

## 2.4 三维数组

```python
A = np.zeros((2,3,4))

print(A.shape)
```

输出：

```python
(2,3,4)
```

表示：

```text
2个矩阵
每个矩阵3行
每行4列
```

---

# 3. shape

shape 表示数组形状。

---

## 一维数组

```python
a = np.array([1,2,3,4])

print(a.shape)
```

输出：

```python
(4,)
```

表示：

```text
4个元素
```

---

## 二维数组

```python
A = np.array([
    [1,2,3],
    [4,5,6]
])

print(A.shape)
```

输出：

```python
(2,3)
```

表示：

```text
2行3列
```

---

## 三维数组

```python
A = np.zeros((2,3,4))

print(A.shape)
```

输出：

```python
(2,3,4)
```

---

# 4. dtype

dtype 表示元素数据类型。

---

查看类型：

```python
a = np.array([1,2,3])

print(a.dtype)
```

输出：

```python
int64
```

---

浮点类型：

```python
a = np.array([1.1,2.2,3.3])

print(a.dtype)
```

输出：

```python
float64
```

---

指定类型：

```python
a = np.array(
    [1,2,3],
    dtype=np.float32
)

print(a.dtype)
```

输出：

```python
float32
```

---

机器学习中最常见：

```python
float32
```

---

# 5. 创建数组

## array

```python
a = np.array([1,2,3])
```

---

## zeros

```python
A = np.zeros((2,3))

print(A)
```

输出：

```python
[[0. 0. 0.]
 [0. 0. 0.]]
```

---

## ones

```python
A = np.ones((2,3))

print(A)
```

输出：

```python
[[1. 1. 1.]
 [1. 1. 1.]]
```

---

## eye

单位矩阵：

```python
A = np.eye(3)

print(A)
```

输出：

```python
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```

---

## arange

```python
a = np.arange(0,10,2)

print(a)
```

输出：

```python
[0 2 4 6 8]
```

---

## linspace

```python
a = np.linspace(0,1,5)

print(a)
```

输出：

```python
[0.   0.25 0.5  0.75 1.  ]
```

---

# 6. 索引(Index)

## 一维索引

```python
a = np.array([10,20,30])

print(a[0])
```

输出：

```python
10
```

---

## 二维索引

```python
A = np.array([
    [1,2,3],
    [4,5,6]
])

print(A[0,1])
```

输出：

```python
2
```

---

# 7. 切片(Slice)

## 一维切片

```python
a = np.array([10,20,30,40,50])

print(a[1:4])
```

输出：

```python
[20 30 40]
```

---

## 取第一行

```python
print(A[0,:])
```

---

## 取第一列

```python
print(A[:,0])
```

---

## 取第二列

```python
print(A[:,1])
```

机器学习中：

```python
X[:,0]
```

表示：

```text
取第一个特征
```

---

# 8. reshape

改变数组形状。

```python
a = np.array([
    1,2,3,4,5,6
])

b = a.reshape(2,3)

print(b)
```

输出：

```python
[[1 2 3]
 [4 5 6]]
```

---

自动计算维度：

```python
b = a.reshape(-1,2)

print(b)
```

输出：

```python
[[1 2]
 [3 4]
 [5 6]]
```

---

机器学习中常见：

```python
X = X.reshape(-1,1)
```

---

# 9. concatenate

数组拼接。

---

## 按行拼接

```python
A = np.array([[1,2]])
B = np.array([[3,4]])

C = np.concatenate(
    [A,B],
    axis=0
)

print(C)
```

输出：

```python
[[1 2]
 [3 4]]
```

---

## 按列拼接

```python
A = np.array([
    [1],
    [2]
])

B = np.array([
    [3],
    [4]
])

C = np.concatenate(
    [A,B],
    axis=1
)

print(C)
```

输出：

```python
[[1 3]
 [2 4]]
```

---

# 10. 统计函数

## mean

平均值：

```python
np.mean(a)
```

---

按列平均：

```python
np.mean(A,axis=0)
```

---

按行平均：

```python
np.mean(A,axis=1)
```

---

## sum

```python
np.sum(a)
```

---

## max

```python
np.max(a)
```

---

## min

```python
np.min(a)
```

---

## std

标准差：

```python
np.std(a)
```

---

# 11. 广播机制(Broadcast)

广播是 NumPy 最强大的功能之一。

---

## 标量广播

```python
a = np.array([1,2,3])

print(a + 10)
```

输出：

```python
[11 12 13]
```

实际等价：

```python
[1,2,3]
+
[10,10,10]
```

---

## 行广播

```python
A = np.array([
    [1,2,3],
    [4,5,6]
])

b = np.array([10,20,30])

print(A+b)
```

输出：

```python
[[11 22 33]
 [14 25 36]]
```

---

广播规则：

从右向左比较维度：

```text
相等
或者
其中一个为1
```

即可广播。

---

机器学习中：

```python
Y = X @ W + b
```

其中：

```python
+b
```

就是广播机制。

---

# 12. NumPy矩阵运算

## 转置

```python
A.T
```

---

## 点积

```python
np.dot(a,b)
```

---

## 矩阵乘法

```python
A @ B
```

---

## 求逆矩阵

```python
np.linalg.inv(A)
```

---

验证：

```python
A @ np.linalg.inv(A)
```

结果：

```python
单位矩阵
```

---

## 行列式

```python
np.linalg.det(A)
```

---

# 13. NumPy 在线性回归中的应用

## 构造数据集

```python
X = np.array([
    [50],
    [60],
    [70]
])

y = np.array([
    [100],
    [120],
    [140]
])
```

---

## 建立模型

```text
y = wx + b
```

---

计算预测值：

```python
w = 2
b = 0

y_hat = w * X + b
```

---

## 计算误差

```python
error = y - y_hat
```

---

## 计算MSE

```python
mse = np.mean(
    (y-y_hat)**2
)
```

---

# 14. NumPy实现线性回归

```python
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
```

输出：

```python
[[3.]
 [0.]]
```

即：

```text
w = 3
b = 0
```

---

# 15. 推荐学习顺序

```text
ndarray
 ↓
shape
 ↓
dtype
 ↓
索引
 ↓
切片
 ↓
reshape
 ↓
concatenate
 ↓
广播机制
 ↓
矩阵乘法
 ↓
转置
 ↓
逆矩阵
 ↓
统计函数
 ↓
线性回归
 ↓
梯度下降
 ↓
神经网络
```

---

# 16. NumPy核心API速查表

| 分类   | API           |
| ---- | ------------- |
| 创建数组 | array         |
| 全0矩阵 | zeros         |
| 全1矩阵 | ones          |
| 单位矩阵 | eye           |
| 等差数组 | arange        |
| 等分数组 | linspace      |
| 查看形状 | shape         |
| 修改形状 | reshape       |
| 数据类型 | dtype         |
| 拼接   | concatenate   |
| 平均值  | mean          |
| 求和   | sum           |
| 最大值  | max           |
| 最小值  | min           |
| 标准差  | std           |
| 转置   | T             |
| 点积   | dot           |
| 矩阵乘法 | @             |
| 求逆   | np.linalg.inv |
| 行列式  | np.linalg.det |

---

# 总结

NumPy 是：

```text
Python中的矩阵计算引擎
```

对于机器学习而言：

```text
数据 = ndarray

模型 = 矩阵

训练 = 矩阵运算

梯度 = 矩阵求导

神经网络 = 大规模矩阵乘法
```

掌握 NumPy 后，可以无缝进入：

```text
线性回归
↓
逻辑回归
↓
梯度下降
↓
神经网络
↓
PyTorch
↓
Transformer
↓
大语言模型
```
