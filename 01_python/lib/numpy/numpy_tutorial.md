# NumPy 完整学习指南

# 1. 什么是 NumPy

NumPy（Numerical Python）是 Python 中用于科学计算和数据分析的基础库。

官方网站：

https://numpy.org

NumPy 提供了：

* 高性能多维数组（ndarray）
* 数学运算函数
* 线性代数运算
* 随机数生成
* FFT变换
* 广播机制（Broadcasting）

几乎所有机器学习框架都建立在 NumPy 的思想之上：

* Scikit-Learn
* Pandas
* TensorFlow
* PyTorch

---

# 2. 为什么需要 NumPy

Python列表：

```python
a = [1, 2, 3]
b = [4, 5, 6]

print(a + b)
```

结果：

```python
[1,2,3,4,5,6]
```

并不是数学加法。

NumPy：

```python
import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])

print(a + b)
```

结果：

```python
[5 7 9]
```

真正实现向量运算。

---

# 3. ndarray

NumPy最核心的数据结构：

```python
numpy.ndarray
```

全称：

```text
N-dimensional Array
N维数组
```

---

# 4. 创建数组

## 一维数组

```python
import numpy as np

a = np.array([1,2,3,4])
```

输出：

```python
[1 2 3 4]
```

---

## 二维数组

```python
a = np.array([
    [1,2,3],
    [4,5,6]
])
```

输出：

```python
[[1 2 3]
 [4 5 6]]
```

---

## 三维数组

```python
a = np.array([
    [
        [1,2],
        [3,4]
    ],
    [
        [5,6],
        [7,8]
    ]
])
```

---

# 5. ndarray属性

```python
a = np.array([
    [1,2,3],
    [4,5,6]
])
```

---

## shape

查看维度

```python
a.shape
```

结果：

```python
(2,3)
```

表示：

```text
2行3列
```

---

## ndim

查看维度数

```python
a.ndim
```

结果：

```python
2
```

---

## size

元素总数

```python
a.size
```

结果：

```python
6
```

---

## dtype

数据类型

```python
a.dtype
```

结果：

```python
int64
```

---

# 6. 常用数组创建

## zeros

全0数组

```python
np.zeros((3,4))
```

结果：

```python
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
```

---

## ones

全1数组

```python
np.ones((2,3))
```

---

## full

指定值

```python
np.full((2,3),5)
```

结果：

```python
[[5 5 5]
 [5 5 5]]
```

---

## eye

单位矩阵

```python
np.eye(3)
```

结果：

```python
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```

---

# 7. 序列生成

## arange

类似range

```python
np.arange(0,10)
```

结果：

```python
[0 1 2 3 4 5 6 7 8 9]
```

---

## linspace

线性均匀采样

```python
np.linspace(0,1,5)
```

结果：

```python
[0.   0.25 0.5  0.75 1.  ]
```

---

# 8. 索引与切片

## 一维

```python
a = np.array([10,20,30,40])

a[0]
```

结果：

```python
10
```

---

## 切片

```python
a[1:3]
```

结果：

```python
[20 30]
```

---

## 二维

```python
a = np.array([
    [1,2,3],
    [4,5,6]
])
```

获取：

```python
a[0,1]
```

结果：

```python
2
```

---

# 9. 数组变形

## reshape

```python
a = np.arange(12)

a.reshape(3,4)
```

结果：

```python
[[0 1 2 3]
 [4 5 6 7]
 [8 9 10 11]]
```

---

## flatten

拉平

```python
a.flatten()
```

结果：

```python
[0 1 2 3 4 5]
```

---

# 10. 数学运算

```python
a = np.array([1,2,3])
b = np.array([4,5,6])
```

加法：

```python
a + b
```

结果：

```python
[5 7 9]
```

减法：

```python
a - b
```

乘法：

```python
a * b
```

除法：

```python
a / b
```

平方：

```python
a ** 2
```

---

# 11. 聚合运算

```python
a = np.array([1,2,3,4,5])
```

求和：

```python
np.sum(a)
```

平均值：

```python
np.mean(a)
```

最大值：

```python
np.max(a)
```

最小值：

```python
np.min(a)
```

标准差：

```python
np.std(a)
```

方差：

```python
np.var(a)
```

---

# 12. 矩阵运算

## 转置

```python
A.T
```

---

## 矩阵乘法

```python
A @ B
```

或者

```python
np.matmul(A,B)
```

---

# 13. 线性代数

## 求逆矩阵

```python
np.linalg.inv(A)
```

---

## 行列式

```python
np.linalg.det(A)
```

---

## 特征值

```python
np.linalg.eig(A)
```

---

## 解线性方程

```python
Ax=b
```

```python
x = np.linalg.solve(A,b)
```

---

# 14. 广播机制（Broadcast）

NumPy最重要的特性之一。

```python
a = np.array([
    [1,2,3],
    [4,5,6]
])

b = np.array([10,20,30])

a + b
```

结果：

```python
[[11 22 33]
 [14 25 36]]
```

NumPy自动扩展：

```text
[10 20 30]
↓
[[10 20 30]
 [10 20 30]]
```

这就是广播。

---

# 15. 随机数模块

## 随机数

```python
np.random.rand(3,4)
```

范围：

```text
0~1
```

---

## 正态分布

```python
np.random.randn(1000)
```

---

## 随机整数

```python
np.random.randint(
    0,
    10,
    size=(3,4)
)
```

---

# 16. FFT

快速傅里叶变换

```python
x_fft = np.fft.fft(x)
```

频率轴：

```python
f = np.fft.fftfreq(N,Ts)
```

通信系统中：

* OFDM
* 雷达
* 声纳
* SRS分析

都会用到。

---

# 17. NumPy 与机器学习

机器学习中的数据：

```python
X.shape = (样本数, 特征数)
```

例如：

```python
X = np.array([
    [170,70],
    [180,80],
    [160,60]
])
```

表示：

```text
3个样本
2个特征
```

---

线性回归：

```python
y = X @ w + b
```

逻辑回归：

```python
z = X @ w + b

p = sigmoid(z)
```

神经网络：

```python
z = X @ W + b
```

本质都是矩阵运算。

---

# 18. NumPy学习路线

第一阶段：

* ndarray
* shape
* dtype
* 索引切片

第二阶段：

* reshape
* 广播机制
* 聚合运算

第三阶段：

* 矩阵乘法
* 线性代数
* FFT

第四阶段：

* 机器学习中的矩阵表示
* 数据预处理
* 特征工程

掌握 NumPy 后，再学习：

```text
Pandas
↓
Matplotlib
↓
Scikit-Learn
↓
PyTorch
↓
深度学习
```

会非常顺畅。
