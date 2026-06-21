# 逻辑回归（Logistic Regression）原理详解

---

# 1. 什么是逻辑回归

逻辑回归（Logistic Regression）是机器学习中最经典的分类算法之一。

虽然名字叫：

```text
Logistic Regression
```

但是它实际上解决的是：

```text
分类问题（Classification）
```

而不是回归问题。

例如：

| 场景     | 输入    | 输出          |
| ------ | ----- | ----------- |
| 垃圾邮件识别 | 邮件内容  | 垃圾邮件 / 正常邮件 |
| 银行贷款审批 | 收入、年龄 | 通过 / 拒绝     |
| 人脸识别   | 图片特征  | 是本人 / 不是本人  |
| 故障检测   | 传感器数据 | 正常 / 异常     |

---

# 2. 为什么需要逻辑回归

假设有如下数据：

| 学习时间(h) | 是否通过考试 |
| ------- | ------ |
| 1       | 0      |
| 2       | 0      |
| 3       | 0      |
| 4       | 1      |
| 5       | 1      |
| 6       | 1      |

其中：

```text
0 -> 不通过
1 -> 通过
```

目标：

```text
根据学习时间
预测是否通过考试
```

---

## 使用线性回归会发生什么

线性回归模型：

```math
y = wx + b
```

假设训练后得到：

```math
y = 0.3x - 0.5
```

则：

```text
x = 1

y = -0.2
```

出现问题：

```text
概率不可能小于0
```

再例如：

```text
x = 6

y = 1.3
```

出现问题：

```text
概率不可能大于1
```

因此：

```text
线性回归不适合分类问题
```

---

# 3. 逻辑回归核心思想

逻辑回归实际上分为两步：

```text
输入特征
    ↓

线性变换

z = wx+b

    ↓

Sigmoid函数

    ↓

输出概率
```

---

# 4. 第一部分：线性变换

对于一个样本：

```text
x1
x2
x3
...
xn
```

首先计算：

```math
z=w_1x_1+w_2x_2+\cdots+w_nx_n+b
```

写成矩阵形式：

```math
z=W^TX+b
```

其中：

```text
W
权重参数

X
输入特征

b
偏置
```

---

# 5. 第二部分：Sigmoid函数

线性变换后：

```math
z∈(-∞,+∞)
```

范围太大。

因此引入：

```math
\sigma(z)=\frac{1}{1+e^{-z}}
```

Sigmoid函数。

---

## Sigmoid特点

输入：

```text
(-∞,+∞)
```

输出：

```text
(0,1)
```

刚好满足概率要求。

---

## 举例

### z=0

```math
\sigma(0)=0.5
```

表示：

```text
50%概率
```

---

### z=5

```math
\sigma(5)=0.993
```

表示：

```text
99.3%概率属于类别1
```

---

### z=-5

```math
\sigma(-5)=0.0067
```

表示：

```text
几乎属于类别0
```

---

# 6. 分类决策

模型输出：

```math
p=\sigma(z)
```

例如：

```text
p = 0.91
```

说明：

```text
91%概率属于类别1
```

---

通常使用阈值：

```text
0.5
```

规则：

```text
p > 0.5

类别1
```

```text
p < 0.5

类别0
```

---

# 7. Forward过程

Forward（前向传播）流程：

```text
输入特征
    ↓

线性计算

z=wx+b

    ↓

Sigmoid

p=σ(z)

    ↓

输出概率
```

例如：

```text
学习时间=5h
```

计算：

```math
z=2.1
```

经过Sigmoid：

```math
p=0.89
```

输出：

```text
89%概率通过考试
```

---

# 8. 为什么需要Loss

预测值：

```text
0.89
```

真实值：

```text
1
```

预测正确。

---

预测值：

```text
0.02
```

真实值：

```text
1
```

预测错误。

---

需要一个函数衡量：

```text
预测有多差
```

这就是：

```text
Loss Function
```

---

# 9. 交叉熵损失（Cross Entropy）

逻辑回归最经典损失：

```math
L=-[y\log(p)+(1-y)\log(1-p)]
```

其中：

```text
y
真实标签

p
预测概率
```

---

## 情况1

真实：

```text
y=1
```

预测：

```text
p=0.99
```

Loss：

```text
接近0
```

很好。

---

## 情况2

真实：

```text
y=1
```

预测：

```text
p=0.01
```

Loss：

```text
非常大
```

很差。

---

# 10. Backward过程

有了Loss以后：

```text
Loss
    ↓

求梯度

∂Loss/∂W

    ↓

更新参数
```

---

## 梯度含义

梯度表示：

```text
参数变化一点点

Loss变化多少
```

例如：

```math
\frac{\partial L}{\partial W}
```

如果：

```text
梯度 > 0
```

说明：

```text
W应该减小
```

---

如果：

```text
梯度 < 0
```

说明：

```text
W应该增大
```

---

# 11. 参数更新

采用梯度下降：

```math
W=W-\eta\frac{\partial L}{\partial W}
```

其中：

```text
η
Learning Rate
学习率
```

例如：

```text
W=5

Gradient=0.3

η=0.1
```

更新：

```math
W=5-0.1×0.3
```

得到：

```text
W=4.97
```

---

# 12. 整个训练过程

完整流程：

```text
训练样本
    ↓

Forward

z=wx+b

    ↓

Sigmoid

    ↓

Prediction

    ↓

Loss

    ↓

Backward

    ↓

Gradient

    ↓

Optimizer

    ↓

Update Weight

    ↓

下一轮训练
```

---

# 13. 从神经网络角度看逻辑回归

逻辑回归实际上就是：

```text
没有隐藏层的神经网络
```

结构：

```text
Input
  ↓
Output
```

---

神经网络：

```text
Input
  ↓

Hidden Layer

  ↓

Output
```

---

因此：

```text
逻辑回归
=
最简单神经网络
```

---

# 14. 与深度学习的关系

现代AI模型：

```text
CNN
ResNet
YOLO
Transformer
LLM
```

虽然结构不同。

但训练过程完全一致：

```text
Forward
    ↓

Loss
    ↓

Backward
    ↓

Optimizer
    ↓

Update
```

逻辑回归是理解这一切的起点。

---

# 15. 嵌入式工程师如何理解

如果把逻辑回归看成一个系统：

```text
输入
    ↓

运算模块

z=wx+b

    ↓

非线性模块

Sigmoid

    ↓

输出概率

    ↓

误差反馈

Loss

    ↓

参数修正

Gradient Descent
```

本质上就是一个：

```text
带反馈闭环的自适应系统
```

这与通信系统中的：

```text
信道估计
均衡器
PLL
LMS自适应滤波
```

在思想上非常接近。

区别只是：

```text
传统DSP
人工设计参数

AI
自动学习参数
```

---

# 总结

逻辑回归核心只有四步：

```text
1. Linear

z=wx+b

2. Sigmoid

得到概率

3. CrossEntropy

计算误差

4. Gradient Descent

更新参数
```

理解了这四步，就理解了现代深度学习训练框架的核心思想。
