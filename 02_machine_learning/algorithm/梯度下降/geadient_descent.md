# 梯度下降算法

## 1. 什么是梯度下降

梯度下降（Gradient Descent）是一种用于求解函数最小值的优化算法。

在机器学习和深度学习中，我们通常希望找到一组模型参数，使损失函数（Loss Function）尽可能小：

$$
\min_{\theta} L(\theta)
$$

其中：

* $\theta$：模型参数
* $L(\theta)$：损失函数
* $\min$：寻找最小值

因此，梯度下降的核心任务就是：

> 不断调整模型参数，让损失函数逐渐减小。

可以把训练过程理解为：

```text
模型参数
   ↓
计算 Loss
   ↓
计算梯度
   ↓
根据梯度调整参数
   ↓
Loss 变小
   ↓
重复
```

最终希望找到一个使 Loss 较小甚至达到最小值的参数。

---

# 2. 为什么叫“梯度下降”

“梯度下降”这个名字可以拆成两个部分：

```text
梯度
+
下降
```

## 2.1 梯度

梯度描述函数在当前位置变化最快的方向。

对于一个变量：

$$
L=f(w)
$$

梯度就是导数：

$$
\frac{dL}{dw}
$$

对于多个变量：

$$
L=f(w_1,w_2,\cdots,w_n)
$$

梯度为：

$$
\nabla L=
\begin{bmatrix}
\frac{\partial L}{\partial w_1}\\
\frac{\partial L}{\partial w_2}\\
\vdots\\
\frac{\partial L}{\partial w_n}
\end{bmatrix}
$$

也就是说：

> 梯度告诉我们函数增长最快的方向。

---

## 2.2 下降

我们在机器学习中通常希望：

$$
Loss\downarrow
$$

也就是希望 Loss 越来越小。

而梯度指向的是函数增长最快的方向，因此我们应该朝着梯度的反方向移动。

所以：

$$
\boxed{
\theta_{new}
=
\theta-\eta\nabla L
}
$$

这就是梯度下降最核心的公式。

---

# 3. 梯度下降的核心公式

梯度下降公式：

$$
\boxed{
\theta_{new}
=
\theta-\eta\nabla L(\theta)
}
$$

其中：

| 符号                 | 含义          |
| ------------------ | ----------- |
| $\theta$           | 当前模型参数      |
| $\theta_{new}$     | 更新后的参数      |
| $L(\theta)$        | 损失函数        |
| $\nabla L(\theta)$ | 损失函数关于参数的梯度 |
| $\eta$             | 学习率         |

这个公式可以直接理解成：

```text
新参数
=
旧参数
-
学习率 × 梯度
```

---

# 4. 为什么要减去梯度

这是梯度下降最重要的原理之一。

假设：

$$
L(w)=w^2
$$

它的图像是一个开口向上的抛物线：

```text
Loss
 ↑
 │        ╲       ╱
 │         ╲     ╱
 │          ╲   ╱
 │           ╲ ╱
 │            ●
 └────────────────→ w
              0
```

最小值位于：

$$
w=0
$$

---

## 4.1 当 w > 0

假设：

$$
w=5
$$

那么：

$$
L(w)=w^2=25
$$

求导：

$$
\frac{dL}{dw}=2w
$$

所以：

$$
\frac{dL}{dw}=10
$$

梯度：

$$
10>0
$$

说明当前位置右侧的函数正在上升。

为了让 Loss 下降，我们应该：

```text
向左移动
```

所以使用：

$$
w_{new}=w-\eta\frac{dL}{dw}
$$

---

## 4.2 当 w < 0

假设：

$$
w=-5
$$

那么：

$$
\frac{dL}{dw}=-10
$$

梯度是负数。

这意味着：

```text
应该向右移动
```

而公式：

$$
w_{new}
=
w-\eta(-10)
$$

实际上就是：

$$
w_{new}
=
w+10\eta
$$

所以参数会自动向右移动。

---

# 5. 梯度下降的直观理解

可以把 Loss 函数想象成一座山。

如果我们站在山坡上，希望找到最低的地方：

```text
                 山顶
                  /\
                 /  \
                /    \
               /      \
              /        \
             /          \
            /            \
           /              \
          /                \
         /                  \
        /                    \
       /                      \
      /                        \
     /                          \
    ↓                            \
  当前位置                         \
                                   \
                                    ●
                                  最低点
```

梯度告诉我们：

> 当前坡度最陡的上坡方向。

但是我们的目标是下山。

所以：

> 沿着梯度的反方向走。

每走一步：

```text
当前位置
   ↓
计算梯度
   ↓
向梯度反方向走
   ↓
新的位置
   ↓
重新计算梯度
   ↓
继续走
```

这就是梯度下降。

---

# 6. 一个完整的数学例子

假设：

$$
L(w)=w^2
$$

求导：

$$
\frac{dL}{dw}=2w
$$

假设初始：

$$
w=5
$$

学习率：

$$
\eta=0.1
$$

---

## 第一次更新

当前：

$$
w=5
$$

梯度：

$$
\frac{dL}{dw}=10
$$

更新：

$$
w=5-0.1\times10
$$

得到：

$$
w=4
$$

Loss：

$$
L=4^2=16
$$

---

## 第二次更新

当前：

$$
w=4
$$

梯度：

$$
\frac{dL}{dw}=8
$$

更新：

$$
w=4-0.1\times8
$$

得到：

$$
w=3.2
$$

Loss：

$$
L=3.2^2=10.24
$$

---

## 第三次更新

当前：

$$
w=3.2
$$

梯度：

$$
\frac{dL}{dw}=6.4
$$

更新：

$$
w=3.2-0.1\times6.4
$$

得到：

$$
w=2.56
$$

Loss：

$$
L=2.56^2=6.5536
$$

---

## 不断重复

参数变化：

```text
5
↓
4
↓
3.2
↓
2.56
↓
2.048
↓
1.6384
↓
...
↓
0
```

Loss：

```text
25
↓
16
↓
10.24
↓
6.5536
↓
4.1943
↓
...
↓
0
```

最终：

$$
w\rightarrow0
$$

同时：

$$
L\rightarrow0
$$

---

# 7. 梯度下降实际上是在“迭代”

梯度下降不是一次就找到答案。

它是一个不断重复的过程：

$$
\theta_0
\rightarrow
\theta_1
\rightarrow
\theta_2
\rightarrow
\theta_3
\rightarrow
\cdots
$$

每一次：

$$
\theta_{t+1}
=
\theta_t-\eta\nabla L(\theta_t)
$$

其中：

* $t$：当前迭代次数
* $\theta_t$：当前参数
* $\theta_{t+1}$：下一次参数
* $\nabla L(\theta_t)$：当前位置的梯度

---

# 8. 学习率

梯度下降中非常重要的一个参数就是：

$$
\eta
$$

它叫：

> 学习率（Learning Rate）

学习率决定：

> 每一次参数更新走多远。

梯度下降：

$$
\theta_{new}
=
\theta-\eta\nabla L
$$

其中：

```text
η
↓
控制步子大小
```

---

# 9. 学习率太小

假设：

$$
\eta=0.000001
$$

每次只移动非常小的一步。

```text
起点
 ↓
·
 ↓
·
 ↓
·
 ↓
·
 ↓
·
 ↓
最小值
```

优点：

* 更新比较平稳
* 不容易一下跨过最小值

缺点：

* 收敛速度非常慢
* 训练需要大量迭代

---

# 10. 学习率太大

假设：

$$
\eta=10
$$

每次移动非常远。

可能出现：

```text
       ●
      / \
     /   \
    /     \
   /       \
 ●           ●
```

参数可能不断跨过最小值：

```text
左边
  ↓
  ●
     ↓
       ●
   ↓
 ●
       ↓
         ●
```

甚至可能导致：

```text
Loss
 ↑
 │       /
 │      /
 │    /
 │  /
 │ /
 └────────→
```

Loss 不下降，反而越来越大。

因此：

> 学习率过大会导致训练不稳定甚至发散。

---

# 11. 合适的学习率

理想情况：

```text
Loss
 ↑
 │\
 │ \
 │  \
 │   \
 │    \
 │     \____
 │          \____
 └────────────────→ 迭代次数
```

Loss 稳定下降并逐渐趋于稳定。

---

# 12. 梯度下降与神经网络

在神经网络中，我们通常有很多参数：

```text
W1
b1
W2
b2
W3
b3
...
```

这些参数共同决定模型的预测结果。

例如：

```text
输入 X
   ↓
神经网络
   ↓
预测值 y_hat
   ↓
Loss
```

我们希望：

$$
Loss\rightarrow最小
$$

因此需要计算：

$$
\frac{\partial L}{\partial W_1}
$$

$$
\frac{\partial L}{\partial b_1}
$$

$$
\frac{\partial L}{\partial W_2}
$$

$$
\frac{\partial L}{\partial b_2}
$$

等等。

然后更新参数：

$$
W_1
=
W_1
-
\eta
\frac{\partial L}{\partial W_1}
$$

$$
W_2
=
W_2
-
\eta
\frac{\partial L}{\partial W_2}
$$

---

# 13. 神经网络中的完整训练流程

一个神经网络训练过程：

```text
                输入数据
                   │
                   ↓
              Forward
                   │
                   ↓
                y_hat
                   │
                   ↓
               Loss(y_hat,y)
                   │
                   ↓
              Backward
                   │
                   ↓
              计算梯度
                   │
                   ↓
           Gradient Descent
                   │
                   ↓
              更新参数
                   │
                   ↓
              下一批数据
```

完整过程：

```text
1. 取一个 Batch

2. 前向传播

3. 得到预测值

4. 计算 Loss

5. 反向传播

6. 计算梯度

7. 根据梯度更新参数

8. 下一个 Batch

9. 重复
```

---

# 14. 梯度下降和反向传播的区别

这两个概念非常容易混淆。

## 14.1 反向传播

反向传播（Backpropagation）的作用是：

> 计算 Loss 对网络参数的梯度。

例如：

$$
\frac{\partial L}{\partial W_1}
$$

$$
\frac{\partial L}{\partial W_2}
$$

$$
\frac{\partial L}{\partial b_1}
$$

---

## 14.2 梯度下降

梯度下降的作用是：

> 根据计算出来的梯度更新参数。

例如：

$$
W_1
=
W_1
-
\eta
\frac{\partial L}{\partial W_1}
$$

所以：

```text
反向传播
    ↓
计算梯度
    ↓
梯度下降
    ↓
更新参数
```

二者不是同一个东西。

---

# 15. PyTorch 中对应的代码

例如：

```python
optimizer.zero_grad()

y_hat = net(X)

l = loss(y_hat, y)

l.backward()

optimizer.step()
```

对应关系：

```text
optimizer.zero_grad()
        ↓
清除旧梯度

y_hat = net(X)
        ↓
前向传播

l = loss(y_hat, y)
        ↓
计算 Loss

l.backward()
        ↓
反向传播
计算梯度

optimizer.step()
        ↓
根据梯度更新参数
```

---

# 16. `l.backward()` 做了什么

例如：

```python
l = loss(y_hat, y)

l.backward()
```

`backward()` 会根据计算图计算：

$$
\frac{\partial L}{\partial \theta}
$$

并把梯度保存到对应参数的：

```python
parameter.grad
```

中。

例如：

```python
print(net[0].weight.grad)
```

可以查看第一个卷积层权重的梯度。

---

# 17. `optimizer.step()` 做了什么

例如：

```python
optimizer.step()
```

如果使用 SGD：

```python
optimizer = torch.optim.SGD(
    net.parameters(),
    lr=0.01
)
```

那么它本质上执行类似：

$$
W
\leftarrow
W-\eta\frac{\partial L}{\partial W}
$$

也就是：

```text
旧参数
   ↓
读取参数梯度
   ↓
乘以学习率
   ↓
减去更新量
   ↓
得到新参数
```

---

# 18. 为什么要 `zero_grad()`

PyTorch 默认会进行梯度累加。

例如：

```python
l.backward()
```

之后：

```text
W.grad
```

里面已经有梯度。

如果下一次再：

```python
l.backward()
```

梯度可能会累加到原来的梯度上。

因此通常训练一个 Batch 前：

```python
optimizer.zero_grad()
```

清除之前的梯度。

标准流程：

```python
optimizer.zero_grad()

y_hat = net(X)

l = loss(y_hat, y)

l.backward()

optimizer.step()
```

可以理解成：

```text
清空旧梯度
    ↓
前向传播
    ↓
计算 Loss
    ↓
反向传播计算新梯度
    ↓
更新参数
```

---

# 19. 梯度下降中的 Batch

深度学习通常不会一次把整个数据集全部送进模型。

例如：

```text
训练集：

60000 张图片
```

设置：

```python
batch_size = 128
```

那么训练时：

```text
128张
 ↓
计算 Loss
 ↓
计算梯度
 ↓
更新一次参数

128张
 ↓
计算 Loss
 ↓
计算梯度
 ↓
更新一次参数

128张
 ↓
...
```

因此：

> 一个 Batch 通常对应一次参数更新。

---

# 20. Batch Size 与参数更新

假设训练集：

$$
N=10000
$$

Batch Size：

$$
B=100
$$

那么一个 Epoch 大约有：

$$
\frac{10000}{100}=100
$$

个 Batch。

因此：

```text
1 Epoch
=
100 个 Batch
=
约 100 次参数更新
```

注意：

> Batch Size 是一次计算多少个样本，而不是更新多少轮梯度。

---

# 21. Epoch、Batch、Iteration

三个概念需要区分。

## Epoch

整个训练数据集完整训练一次：

```text
60000 张训练图片
全部训练一遍
=
1 Epoch
```

## Batch

一次送入模型的数据：

```text
batch_size = 128

一次训练：
128 张图片
```

## Iteration

处理一个 Batch 通常称为一次 Iteration。

例如：

```text
60000 张图片
batch_size = 128

≈ 469 个 Batch

≈ 469 次 Iteration

≈ 469 次参数更新
```

所以：

```text
Epoch
 └── Batch
      └── Iteration
           └── 梯度计算
                ↓
              参数更新
```

---

# 22. 梯度下降的三种常见形式

根据每次计算梯度使用的数据量不同，可以把梯度下降分成三种常见形式：

```text
Batch Gradient Descent
Mini-Batch Gradient Descent
Stochastic Gradient Descent
```

---

# 23. 批量梯度下降

Batch Gradient Descent：

> 每次使用整个训练集计算梯度。

例如：

```text
训练集
60000 张图片
     ↓
全部进入网络
     ↓
计算 Loss
     ↓
计算梯度
     ↓
更新一次参数
```

优点：

* 梯度比较稳定
* 计算方向比较准确

缺点：

* 数据量很大时计算非常慢
* 内存消耗大
* 参数更新次数少

---

# 24. 随机梯度下降

Stochastic Gradient Descent，简称：

> SGD

理论上的随机梯度下降：

```text
一次只使用一个样本

1张图片
 ↓
计算 Loss
 ↓
计算梯度
 ↓
更新参数

下一张图片
 ↓
计算 Loss
 ↓
计算梯度
 ↓
更新参数
```

优点：

* 更新非常频繁
* 单次计算量小

缺点：

* 梯度波动比较大
* Loss 曲线可能不稳定

---

# 25. Mini-Batch Gradient Descent

深度学习中最常见的是：

> Mini-Batch Gradient Descent

也就是每次使用一小批数据。

例如：

```text
batch_size = 128
```

那么：

```text
128个样本
 ↓
计算梯度
 ↓
更新参数
```

然后：

```text
下一批128个样本
 ↓
计算梯度
 ↓
更新参数
```

这就是现代深度学习最常见的训练方式。

---

# 26. 三种梯度下降的区别

| 方法            | 每次使用的数据 | 参数更新 |
| ------------- | ------: | ---: |
| Batch GD      |   整个数据集 |    少 |
| SGD           |    1个样本 | 非常频繁 |
| Mini-Batch GD |   一小批样本 |   常见 |

实际深度学习中通常使用：

```text
Mini-Batch
```

例如：

```python
batch_size = 128
```

---

# 27. 梯度下降在 CNN 中的过程

以 CNN 为例：

```text
输入图片
   ↓
卷积层
   ↓
ReLU
   ↓
池化
   ↓
卷积层
   ↓
全连接层
   ↓
预测结果
   ↓
Cross Entropy Loss
```

假设 CNN 中存在：

```text
Conv1.weight
Conv1.bias

Conv2.weight
Conv2.bias

Linear.weight
Linear.bias
```

Loss 计算完成以后：

```text
Loss
 ↓
反向传播
 ↓
计算：

∂L/∂Conv1.weight
∂L/∂Conv1.bias

∂L/∂Conv2.weight
∂L/∂Conv2.bias

∂L/∂Linear.weight
∂L/∂Linear.bias
```

然后：

```text
梯度下降
 ↓
更新所有参数
```

例如：

$$
W_{conv1}
\leftarrow
W_{conv1}
-
\eta
\frac{\partial L}
{\partial W_{conv1}}
$$

---

# 28. 梯度下降并不直接修改输入数据

梯度下降主要更新：

```text
模型参数
```

而不是：

```text
输入图片
```

例如：

```text
输入图片 X
     ↓
   CNN
     ↓
参数 W
     ↓
预测
     ↓
Loss
```

训练过程中：

```text
X
```

通常不被梯度下降更新。

真正被更新的是：

```text
W
b
```

也就是：

```text
卷积核参数
全连接层参数
偏置参数
...
```

---

# 29. 梯度下降到底在优化什么

神经网络训练的核心目标可以写成：

$$
\boxed{
\min_{\theta}L(\theta)
}
$$

其中：

$$
\theta
=
\{W_1,b_1,W_2,b_2,\cdots\}
$$

也就是说：

> 梯度下降实际上是在寻找一组最合适的网络参数。

例如：

```text
初始参数
    ↓
随机初始化
    ↓
计算 Loss
    ↓
计算梯度
    ↓
更新参数
    ↓
Loss 下降
    ↓
继续更新
    ↓
Loss 继续下降
    ↓
...
    ↓
找到较好的参数
```

---

# 30. 局部最小值

梯度下降并不保证一定找到整个函数的全局最小值。

例如：

```text
Loss
 ↑
 │       ╱╲
 │      /  \
 │  ╱╲ /    ╲
 │ /  ╲      \
 │●    ╲      ●
 └────────────────→ 参数
```

可能存在：

```text
局部最小值
```

和：

```text
全局最小值
```

梯度下降可能在某个局部区域停止。

---

# 31. 鞍点

高维函数中还可能出现：

> 鞍点（Saddle Point）

例如：

```text
        ↗
       /
──────●──────
     /
    ↘
```

某些方向上函数在下降，而另外一些方向上函数在上升。

此时梯度可能非常小：

$$
\nabla L\approx0
$$

导致参数更新速度变慢。

---

# 32. 梯度消失

如果梯度非常小：

$$
|\nabla L|\approx0
$$

那么：

$$
\theta_{new}
=
\theta-\eta\nabla L
$$

参数变化也会非常小。

表现为：

```text
梯度
 ↓
越来越小
 ↓
参数几乎不更新
 ↓
Loss 学不动
```

这叫：

> 梯度消失（Gradient Vanishing）。

---

# 33. 梯度爆炸

如果梯度非常大：

$$
|\nabla L|\gg1
$$

那么参数更新：

$$
\eta\nabla L
$$

可能非常大。

表现为：

```text
参数
 ↓
大幅变化
 ↓
Loss变大
 ↓
梯度更大
 ↓
参数变化更大
 ↓
训练发散
```

这叫：

> 梯度爆炸（Gradient Explosion）。

---

# 34. 梯度下降的完整逻辑

把整个过程串起来：

```text
                    模型参数
                       │
                       ↓
                    前向传播
                       │
                       ↓
                    预测结果
                       │
                       ↓
                     Loss
                       │
                       ↓
                  反向传播
                       │
                       ↓
                     梯度
                       │
                       ↓
                 梯度下降更新
                       │
                       ↓
                   新模型参数
                       │
                       ↓
                   下一次训练
```

核心公式：

$$
\boxed{
\theta_{t+1}
=
\theta_t
-
\eta\nabla L(\theta_t)
}
$$

---

# 35. 最核心的理解

如果只记住梯度下降的核心思想，可以记住下面这句话：

> **梯度告诉我们 Loss 增长最快的方向，梯度下降则沿着梯度的反方向调整模型参数，使 Loss 尽可能下降。**

可以进一步记成：

```text
梯度
↓
告诉我往哪里 Loss 增长最快

梯度的反方向
↓
告诉我往哪里 Loss 下降最快

学习率
↓
告诉我走多远

参数更新
↓
真正改变模型
```

最终形成：

$$
\boxed{
参数
\rightarrow
Loss
\rightarrow
梯度
\rightarrow
反方向
\rightarrow
参数更新
\rightarrow
Loss下降
}
$$

---

# 36. 一句话总结

梯度下降算法本质上就是：

$$
\boxed{
新参数
=
旧参数
-
学习率
\times
Loss对参数的梯度
}
$$

它是现代机器学习和深度学习中最核心的参数优化思想之一。
