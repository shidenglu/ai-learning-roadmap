# 线性代数核心笔记 (Linear Algebra Cheat Sheet)

线性代数是现代应用数学、数据科学和机器学习的基石。它主要研究**向量空间**和**线性映射**。

---

## 1. 核心对象：向量与矩阵 (Vectors and Matrices)

### 向量 (Vector)
向量可以看作是空间中的一个点或一条有向线段。在 $n$ 维实数空间 $\mathbb{R}^n$ 中，向量通常表示为列向量：

$$x = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}$$

### 矩阵 (Matrix)
矩阵是一个由数字排成的矩形阵列，可以看作是**线性变换的载体**。一个 $m \times n$ 的矩阵 $A$ 有 $m$ 行 $n$ 列：

$$A = \begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{bmatrix}$$

---

## 2. 矩阵运算与线性方程组

### 矩阵乘法 (Matrix Multiplication)
设 $A$ 是 $m \times n$ 矩阵，$B$ 是 $n \times p$ 矩阵，则它们的乘积 $C = AB$ 是一个 $m \times p$ 矩阵，其中每个元素定义为：

$$c_{ij} = \sum_{k=1}^n a_{ik}b_{kj}$$

> ⚠️ **注意**：矩阵乘法**不满足交换律**，即 $AB \neq BA$（通常情况下）。

### 线性方程组 (Linear Systems)
任何线性方程组都可以紧凑地表示为矩阵乘法形式：

$$Ax = b$$

其中 $A$ 为系数矩阵，$x$ 为未知数向量，$b$ 为常数向量。解法通常使用**高斯消元法（Gaussian Elimination）**将矩阵化为行阶梯形（REF）。

---

## 3. 矩阵的特征性质

### 行列式 (Determinant)
行列式 $\det(A)$ 或 $|A|$ 是一个将方阵映射到标量的函数。
* 地理意义：代表变换后的**空间体积缩放比例**。
* 若 $\det(A) = 0$，说明矩阵将空间压缩到了更低的维度（不可逆）。

### 逆矩阵 (Inverse Matrix)
对于方阵 $A$，如果存在矩阵 $A^{-1}$ 使得：

$$AA^{-1} = A^{-1}A = I$$

（其中 $I$ 是单位矩阵），则称 $A$ 是**可逆的（Collectible/Non-singular）**。
> **充要条件**：$\det(A) \neq 0$。

### 秩 (Rank)
矩阵的秩 $\text{rank}(A)$ 是指矩阵中**线性无关的行或列的最大数量**。它代表了矩阵能够张成的空间的最高维度。

---

## 4. 空间与基底 (Spaces and Bases)

* **张成空间 (Span)**：一组向量通过线性组合所能到达的所有点的集合。
* **线性相关与无关 (Linear Independence)**：
  如果存在不全为 0 的系数使得 $\sum c_i v_i = 0$，则这组向量**线性相关**；否则**线性无关**。
* **基底 (Basis)**：向量空间中一组**线性无关**且能**张成该空间**的向量集合。

---

## 5. 特征值与特征向量 (Eigenvalues and Eigenvectors)

对于一个方阵 $A$，如果存在一个非零向量 $v$ 和标量 $\lambda$，满足：

$$Av = \lambda v$$

* $v$ 称为 **特征向量 (Eigenvector)**：在矩阵变换下，其**方向保持不变**，只有拉伸或缩放。
* $\lambda$ 称为 **特征值 (Eigenvalue)**：对应方向的**缩放倍数**。

### 特征方程 (Characteristic Equation)
求解特征值需要解以下方程：

$$\det(A - \lambda I) = 0$$

---

## 6. 重要矩阵分解 (Matrix Decompositions)

| 分解类型 | 公式 | 适用条件 | 应用场景 |
| :--- | :--- | :--- | :--- |
| **特征分解 (Eigendecomposition)** | $A = Q \Lambda Q^{-1}$ | 方阵，且有 $n$ 个线性无关特征向量 | 矩阵幂运算、马尔可夫链 |
| **奇异值分解 (SVD)** | $A = U \Sigma V^T$ | 任意 $m \times n$ 矩阵 | PCA降维、图像压缩、推荐系统 |
| **LU分解** | $A = LU$ | 方阵（通常需要行列变换） | 求解线性方程组、计算机数值计算 |