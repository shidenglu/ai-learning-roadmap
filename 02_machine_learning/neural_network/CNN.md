# CNN（卷积神经网络）完整介绍

> CNN：**Convolutional Neural Network**
>
> 中文：**卷积神经网络**
>
> 简称：**CNN**

---

# 1. CNN 是什么

CNN（Convolutional Neural Network，卷积神经网络）是一类非常擅长处理**具有空间结构数据**的神经网络。

最典型的应用就是：

* 图像分类
* 图像识别
* 目标检测
* 图像分割
* 人脸识别
* OCR
* 图像生成
* 视频分析
* 医学图像分析
* 自动驾驶视觉

例如输入一张图片：

```text
        图片
         ↓
       CNN
         ↓
    特征提取
         ↓
    分类 / 检测
         ↓
       结果
```

例如：

```text
输入：

      🐱

       ↓

CNN

       ↓

猫：0.97
狗：0.02
鸟：0.01
```

CNN 的核心思想是：

> **通过卷积操作，让神经网络自动从输入数据中提取局部特征，并通过多层网络逐渐组合成更加复杂的特征。**

---

# 2. CNN 在机器学习中的位置

可以把整个 AI 体系简单理解为：

```text
人工智能 AI
│
└── 机器学习 Machine Learning
    │
    ├── 传统机器学习
    │   ├── 线性回归
    │   ├── 逻辑回归
    │   ├── 决策树
    │   ├── 随机森林
    │   └── SVM
    │
    └── 神经网络 Neural Network
        │
        ├── MLP
        ├── CNN
        ├── RNN
        ├── LSTM
        └── Transformer
```

所以：

```text
CNN
 ↓
Convolutional Neural Network
 ↓
卷积神经网络
 ↓
神经网络的一种
 ↓
机器学习的一种方法
```

---

# 3. 为什么需要 CNN

在 CNN 出现之前，可以直接使用全连接神经网络处理图片。

例如一张：

```text
28 × 28
```

的灰度图片：

```text
28 × 28 = 784
```

可以把图片拉平成：

```text
[784]
```

然后输入全连接层：

```text
784
 ↓
Linear
 ↓
100
 ↓
Linear
 ↓
10
```

但是这种方式存在很多问题。

---

# 4. 全连接处理图片的问题

## 4.1 参数数量巨大

假设输入图片：

```text
224 × 224 × 3
```

那么输入数据量：

$$
224\times224\times3=150528
$$

如果直接连接一个拥有 4096 个神经元的全连接层：

$$
150528\times4096
$$

参数数量超过：

```text
6 亿
```

参数量非常大。

---

# 5. 图片具有空间结构

图片并不是普通的一维数据。

例如：

```text
猫的眼睛
```

通常出现在：

```text
猫的头部
```

而头部又处于：

```text
猫的身体
```

附近。

也就是说：

> 图片中的像素之间具有很强的空间关系。

相邻像素通常具有比较强的关联。

例如：

```text
像素
 ↓
边缘
 ↓
纹理
 ↓
局部形状
 ↓
物体
```

CNN 正是利用了这种空间结构。

---

# 6. CNN 的核心思想

CNN 最重要的三个思想：

```text
局部连接
+
权重共享
+
层次化特征提取
```

---

# 7. 局部连接

假设输入图片：

```text
28 × 28
```

CNN 不会让一个神经元连接全部 784 个像素。

而是只看一个局部区域。

例如：

```text
3 × 3
```

也就是说：

```text
┌─────────────┐
│             │
│    ┌───┐    │
│    │3×3│    │
│    └───┘    │
│             │
└─────────────┘
```

这个 `3×3` 区域就是一个局部感受野。

---

# 8. 卷积

CNN 最核心的操作就是：

> **卷积（Convolution）**

假设输入：

```text
X
```

卷积核：

```text
K
```

通过卷积操作：

$$
Y=X*K
$$

得到：

```text
Y
```

卷积核会在输入图片上滑动。

---

# 9. 卷积核

卷积核也叫：

* Kernel
* Filter
* 卷积滤波器

例如：

```text
3 × 3
```

卷积核：

```text
┌───┬───┬───┐
│ w1│ w2│ w3│
├───┼───┼───┤
│ w4│ w5│ w6│
├───┼───┼───┤
│ w7│ w8│ w9│
└───┴───┴───┘
```

这些 `w` 都是神经网络需要学习的参数。

---

# 10. 卷积是怎么计算的

假设输入局部区域：

```text
1 2 3
4 5 6
7 8 9
```

卷积核：

```text
1 0 -1
1 0 -1
1 0 -1
```

进行逐元素相乘：

```text
1×1 + 2×0 + 3×(-1)
+
4×1 + 5×0 + 6×(-1)
+
7×1 + 8×0 + 9×(-1)
```

最终得到一个数字。

也就是：

$$
1-3+4-6+7-9=-6
$$

这个数字就是当前位置的输出。

然后卷积核向右移动，再计算一次。

---

# 11. 卷积核在图片上滑动

假设：

```text
输入图片
```

卷积核：

```text
3×3
```

那么：

```text
①

┌───────────────┐
│███            │
│███            │
│███            │
│               │
└───────────────┘


②

┌───────────────┐
│  ███          │
│  ███          │
│  ███          │
│               │
└───────────────┘


③

┌───────────────┐
│    ███        │
│    ███        │
│    ███        │
│               │
└───────────────┘
```

卷积核不断移动。

每个位置得到一个数字。

最终形成：

```text
特征图 Feature Map
```

---

# 12. 特征图 Feature Map

卷积之后得到的结果叫：

```text
Feature Map
特征图
```

例如：

```text
输入图片
   ↓
卷积核
   ↓
特征图
```

特征图中的某些位置数值较大，意味着：

> 这个位置可能存在卷积核比较关注的特征。

例如某个卷积核学会检测：

```text
横向边缘
```

那么：

```text
横向边缘
   ↓
卷积
   ↓
对应位置响应较强
```

---

# 13. 卷积核为什么能够提取特征

关键在于：

> **卷积核中的参数是通过训练学习出来的。**

例如训练之前：

```text
卷积核：

0.12  -0.32  0.51
0.21   0.08 -0.11
...
```

这些数字没有明确意义。

经过大量训练以后：

```text
卷积核
 ↓
自动学习
 ↓
可能对某种边缘产生强响应
```

网络会自动学习：

```text
边缘
 ↓
纹理
 ↓
形状
 ↓
物体局部
 ↓
完整物体
```

这就是 CNN 的核心能力之一。

---

# 14. stride：步幅

`stride` 表示：

> **卷积核每次移动多少个像素。**

例如：

```python
nn.Conv2d(
    1,
    96,
    kernel_size=11,
    stride=4
)
```

表示：

```text
卷积核每次向右移动 4 个像素
```

并且：

```text
每向下移动一行
也移动 4 个像素
```

所以二维卷积中的：

```text
stride = 4
```

意味着：

```text
向右：跳 4
向下：跳 4
```

---

# 15. stride = 1

```text
stride = 1
```

卷积核：

```text
向右移动 1
向下移动 1
```

例如：

```text
███
███
███

↓

 ███
 ███
 ███

↓

  ███
  ███
  ███
```

---

# 16. stride = 2

```text
stride = 2
```

表示：

```text
向右跳 2
向下跳 2
```

这样通常会让输出特征图变小。

---

# 17. padding：填充

`padding` 表示：

> **在输入数据边缘增加额外的数据。**

例如：

```text
padding = 1
```

原始：

```text
1 2 3
4 5 6
7 8 9
```

填充后：

```text
0 0 0 0 0
0 1 2 3 0
0 4 5 6 0
0 7 8 9 0
0 0 0 0 0
```

---

# 18. 为什么需要 padding

如果没有 padding：

```text
输入：
28 × 28

kernel：
3 × 3

stride：
1
```

输出：

$$
28-3+1=26
$$

变成：

```text
26 × 26
```

如果网络很深：

```text
28
 ↓
26
 ↓
24
 ↓
22
 ↓
...
```

图片会越来越小。

所以可以使用 padding。

---

# 19. stride、padding、kernel 对输出尺寸的影响

卷积输出尺寸：

$$
H_{out}
=
\left\lfloor
\frac{H_{in}+2P-K}{S}
\right\rfloor+1
$$

宽度同理：

$$
W_{out}
=
\left\lfloor
\frac{W_{in}+2P-K}{S}
\right\rfloor+1
$$

其中：

```text
H_in   输入高度
W_in   输入宽度
K      kernel size
P      padding
S      stride
```

---

# 20. 一个例子

输入：

```text
224 × 224
```

卷积：

```text
kernel = 11
stride = 4
padding = 1
```

那么：

$$
H_{out}
=
\left\lfloor
\frac{224+2-11}{4}
\right\rfloor+1
$$

得到：

```text
54
```

所以：

```text
224 × 224
      ↓
Conv2d
      ↓
54 × 54
```

---

# 21. 通道 Channel

图片通常有通道。

灰度图：

```text
1 channel
```

RGB 图片：

```text
3 channels

R
G
B
```

所以 RGB 图片：

```text
224 × 224 × 3
```

在 PyTorch 中通常表示：

```text
[batch, channel, height, width]
```

例如：

```text
[32, 3, 224, 224]
```

表示：

```text
32 张图片
3 个通道
224 高
224 宽
```

---

# 22. Conv2d 的参数

例如：

```python
nn.Conv2d(
    256,
    384,
    kernel_size=3,
    padding=1
)
```

四个重要参数：

```text
256
 ↓
输入通道数

384
 ↓
输出通道数

3
 ↓
卷积核大小 3×3

1
 ↓
padding
```

---

# 23. 输出通道是什么意思

例如：

```python
nn.Conv2d(
    256,
    384,
    kernel_size=3
)
```

表示：

```text
输入：
256 个通道

       ↓

384 个卷积核

       ↓

输出：
384 个通道
```

所以：

$$
\boxed{输出通道数=卷积核数量}
$$

---

# 24. 为什么有 384 个输出通道

因为可以有：

```text
卷积核1
卷积核2
卷积核3
...
卷积核384
```

每个卷积核都可以学习不同的特征。

例如：

```text
卷积核1 → 横向边缘
卷积核2 → 纵向边缘
卷积核3 → 斜向边缘
卷积核4 → 某种纹理
...
卷积核384 → 其他特征
```

训练过程中，这些特征并不是人工指定的，而是模型自动学习的。

---

# 25. 多通道卷积

假设输入：

```text
256 个通道
```

使用：

```text
1 个输出卷积核
```

这个卷积核实际上需要覆盖所有输入通道。

因此它的形状是：

```text
256 × 3 × 3
```

而不是：

```text
3 × 3
```

---

# 26. 一个输出通道怎么产生

输入：

```text
256 channels
```

一个卷积核：

```text
256 × 3 × 3
```

分别对 256 个通道进行卷积：

```text
Channel 1
    ↓
卷积

Channel 2
    ↓
卷积

...

Channel 256
    ↓
卷积
```

然后把结果相加：

```text
256 个特征图
      ↓
    相加
      ↓
一个输出特征图
```

因此：

```text
一个卷积核
      ↓
一个输出通道
```

---

# 27. 384 个输出通道

如果：

```text
输入通道 = 256
输出通道 = 384
kernel = 3×3
```

那么：

```text
卷积核1：
256 × 3 × 3

卷积核2：
256 × 3 × 3

...

卷积核384：
256 × 3 × 3
```

最终得到：

```text
384 个输出特征图
```

所以：

$$
\boxed{
Conv2d(256,384,3)
}
$$

就是：

```text
256 输入通道
        ↓
384 个卷积核
        ↓
384 输出通道
```

---

# 28. ReLU

CNN 中通常会在卷积后使用激活函数。

最常见：

```python
nn.ReLU()
```

ReLU：

$$
ReLU(x)=\max(0,x)
$$

例如：

```text
输入：

-3
-1
 0
 2
 5

↓

ReLU

0
0
0
2
5
```

---

# 29. 为什么使用 ReLU

如果没有激活函数：

```text
Linear
 ↓
Linear
 ↓
Linear
```

多个线性变换最终仍然可以表示成一个线性变换。

加入：

```text
ReLU
```

之后：

```text
卷积
 ↓
ReLU
 ↓
卷积
 ↓
ReLU
```

网络就可以学习更加复杂的非线性关系。

---

# 30. 池化 Pooling

CNN 中还有一个非常重要的操作：

```text
Pooling
```

常见：

```text
Max Pooling
Average Pooling
```

PyTorch：

```python
nn.MaxPool2d(
    kernel_size=3,
    stride=2
)
```

---

# 31. 最大池化

例如：

```text
1 5
3 2
```

最大池化：

```text
max(1,5,3,2)
```

得到：

```text
5
```

所以：

```text
┌───┬───┐
│ 1 │ 5 │
├───┼───┤
│ 3 │ 2 │
└───┴───┘

       ↓

       5
```

---

# 32. 池化的作用

池化主要可以：

```text
降低特征图尺寸
降低计算量
扩大后续网络的感受野
增强一定程度的平移鲁棒性
```

例如：

```text
224 × 224
    ↓
112 × 112
    ↓
56 × 56
    ↓
28 × 28
```

---

# 33. Flatten

卷积层输出通常是：

```text
[batch, channel, height, width]
```

例如：

```text
[128, 256, 5, 5]
```

全连接层通常需要：

```text
[batch, features]
```

所以需要：

```python
nn.Flatten()
```

将：

```text
[128, 256, 5, 5]
```

变成：

```text
[128, 6400]
```

因为：

$$
256\times5\times5=6400
$$

注意：

> `Flatten()` 不会改变数据，只是改变张量的形状。

---

# 34. Dropout

Dropout 是一种常见的正则化方法。

例如：

```python
nn.Dropout(0.5)
```

训练过程中：

```text
50%的神经元
随机暂时关闭
```

例如：

```text
原来：

● ● ● ● ● ● ● ●

Dropout：

● ○ ● ○ ○ ● ● ○
```

其中：

```text
● → 保留
○ → 暂时关闭
```

目的是：

> **降低模型对某几个神经元的过度依赖，减轻过拟合。**

注意：

```text
训练阶段：
Dropout 开启

测试阶段：
Dropout 关闭
```

所以：

```python
net.train()
```

会启用 Dropout。

而：

```python
net.eval()
```

会关闭 Dropout。

---

# 35. CNN 的典型结构

一个经典 CNN 可以理解为：

```text
输入图片
   ↓
卷积
   ↓
激活函数
   ↓
池化
   ↓
卷积
   ↓
激活函数
   ↓
池化
   ↓
Flatten
   ↓
全连接层
   ↓
分类结果
```

---

# 36. CNN 的层次化特征

CNN 很重要的一个思想：

> **越浅的网络学习越简单的特征，越深的网络学习越复杂的特征。**

例如：

```text
输入图片
   ↓
第一层卷积
   ↓
边缘
   ↓
第二层卷积
   ↓
纹理
   ↓
第三层卷积
   ↓
局部形状
   ↓
更深层
   ↓
物体结构
   ↓
最终分类
```

可以理解为：

```text
像素
 ↓
边缘
 ↓
纹理
 ↓
形状
 ↓
局部结构
 ↓
完整对象
```

---

# 37. 感受野 Receptive Field

CNN 中有一个重要概念：

> **感受野（Receptive Field）**

表示：

> 一个神经元在输入图片上能够“看到”的区域。

例如：

```text
第一层：

一个神经元
 ↓
看到 3×3 区域
```

经过多层卷积：

```text
第一层
 ↓
第二层
 ↓
第三层
```

深层神经元可以间接看到输入图片中更大的区域。

因此：

```text
浅层：
局部信息

深层：
更大范围的信息
```

---

# 38. CNN 为什么具有一定的平移鲁棒性

假设图片中的猫：

```text
猫在左边
```

经过卷积：

```text
检测猫的某些局部特征
```

如果猫移动到：

```text
猫在右边
```

卷积核仍然会在整张图片上滑动。

因此相同的卷积核仍然可能检测到相同特征。

这就是 CNN 对空间位置变化具有一定鲁棒性的原因之一。

---

# 39. 参数共享

CNN 的另一个核心思想：

> **同一个卷积核在整张图片上重复使用。**

例如：

```text
卷积核：

[ a b c
  d e f
  g h i ]
```

它可以扫描：

```text
左上
 ↓
中间
 ↓
右边
 ↓
下一行
 ↓
...
```

始终使用同一组：

```text
a,b,c,d,e,f,g,h,i
```

这些参数不会因为位置不同而改变。

这叫：

> **参数共享（Parameter Sharing）**

---

# 40. CNN 为什么参数量比全连接少

假设：

```text
224 × 224 × 3
```

直接全连接：

```text
150528 × 4096
```

参数巨大。

而卷积：

```text
3 × 3
```

假设：

```text
输入通道 = 3
输出通道 = 64
```

参数：

$$
3\times3\times3\times64
$$

只有：

```text
1728
```

再加上 bias：

```text
1792
```

相比数亿参数小得多。

---

# 41. 卷积层参数数量

对于：

```python
nn.Conv2d(
    C_in,
    C_out,
    kernel_size=K
)
```

参数数量：

$$
C_{out}\times C_{in}\times K\times K
$$

如果有 bias：

$$
C_{out}
$$

因此：

$$
Parameters=
C_{out}C_{in}K^2+C_{out}
$$

---

# 42. 例如 AlexNet 第一层

```python
nn.Conv2d(
    1,
    96,
    kernel_size=11,
    stride=4
)
```

参数：

$$
96\times1\times11\times11
$$

得到：

```text
11616
```

加上 96 个 bias：

```text
11712
```

---

# 43. LeNet

LeNet 是非常经典的 CNN。

经典结构：

```text
输入
 ↓
卷积
 ↓
池化
 ↓
卷积
 ↓
池化
 ↓
全连接
 ↓
全连接
 ↓
输出
```

可以表示为：

```text
28×28
 ↓
Conv
 ↓
Pool
 ↓
Conv
 ↓
Pool
 ↓
Flatten
 ↓
Linear
 ↓
Linear
 ↓
10类
```

LeNet 是现代 CNN 的重要基础。

---

# 44. AlexNet

AlexNet 是 CNN 发展历史上非常重要的网络。

典型结构：

```text
输入
 ↓
Conv
 ↓
ReLU
 ↓
MaxPool
 ↓
Conv
 ↓
ReLU
 ↓
MaxPool
 ↓
Conv
 ↓
ReLU
 ↓
Conv
 ↓
ReLU
 ↓
Conv
 ↓
ReLU
 ↓
MaxPool
 ↓
Flatten
 ↓
Linear
 ↓
Dropout
 ↓
Linear
 ↓
Dropout
 ↓
Linear
```

---

# 45. PyTorch 中的 AlexNet 示例

```python
net = nn.Sequential(

    nn.Conv2d(
        1,
        96,
        kernel_size=11,
        stride=4,
        padding=1
    ),

    nn.ReLU(),

    nn.MaxPool2d(
        kernel_size=3,
        stride=2
    ),

    nn.Conv2d(
        96,
        256,
        kernel_size=5,
        padding=2
    ),

    nn.ReLU(),

    nn.MaxPool2d(
        kernel_size=3,
        stride=2
    ),

    nn.Conv2d(
        256,
        384,
        kernel_size=3,
        padding=1
    ),

    nn.ReLU(),

    nn.Conv2d(
        384,
        384,
        kernel_size=3,
        padding=1
    ),

    nn.ReLU(),

    nn.Conv2d(
        384,
        256,
        kernel_size=3,
        padding=1
    ),

    nn.ReLU(),

    nn.MaxPool2d(
        kernel_size=3,
        stride=2
    ),

    nn.Flatten(),

    nn.Linear(
        6400,
        4096
    ),

    nn.ReLU(),

    nn.Dropout(0.5),

    nn.Linear(
        4096,
        4096
    ),

    nn.ReLU(),

    nn.Dropout(0.5),

    nn.Linear(
        4096,
        10
    )
)
```

---

# 46. AlexNet 的数据尺寸变化

输入：

```text
[1, 1, 224, 224]
```

经过第一层：

```text
Conv2d
 ↓
[1, 96, 54, 54]
```

经过池化：

```text
[1, 96, 26, 26]
```

第二层卷积：

```text
[1, 256, 26, 26]
```

第二次池化：

```text
[1, 256, 12, 12]
```

后面的卷积：

```text
[1, 384, 12, 12]

[1, 384, 12, 12]

[1, 256, 12, 12]
```

最后池化：

```text
[1, 256, 5, 5]
```

Flatten：

```text
[1, 6400]
```

因为：

$$
256\times5\times5=6400
$$

然后：

```text
Linear
 ↓
[1, 4096]
```

最后：

```text
Linear
 ↓
[1, 10]
```

---

# 47. 为什么最后是 10

如果使用 MNIST：

```text
0
1
2
3
4
5
6
7
8
9
```

一共：

```text
10 个类别
```

所以：

```python
nn.Linear(
    4096,
    10
)
```

输出：

```text
[batch_size, 10]
```

例如：

```text
[128, 10]
```

表示：

```text
128 张图片
每张图片对应 10 个类别的预测分数
```

---

# 48. 分类结果怎么得到

例如网络输出：

```text
[
    1.2,
    0.3,
    5.8,
    0.2,
    1.1,
    0.4,
    0.1,
    0.5,
    0.2,
    0.8
]
```

最大值：

```text
5.8
```

对应：

```text
类别 2
```

因此：

```python
y_hat.argmax(dim=1)
```

可以得到预测类别。

---

# 49. CrossEntropyLoss

分类任务通常使用：

```python
loss = nn.CrossEntropyLoss()
```

模型输出：

```text
y_hat
[batch_size, 10]
```

标签：

```text
y
[batch_size]
```

例如：

```text
y_hat：

[1.2, 0.3, 5.8, ...]
```

真实标签：

```text
2
```

CrossEntropyLoss 会根据：

```text
模型对类别2的预测
```

计算损失。

---

# 50. CNN 的训练过程

CNN 和普通神经网络的训练过程本质上是一样的：

```text
输入图片
   ↓
前向传播
   ↓
得到预测结果
   ↓
计算 Loss
   ↓
反向传播
   ↓
计算梯度
   ↓
更新参数
```

代码：

```python
optimizer.zero_grad()

y_hat = net(X)

l = loss(y_hat, y)

l.backward()

optimizer.step()
```

---

# 51. `zero_grad()`

```python
optimizer.zero_grad()
```

作用：

> 清除上一轮留下的梯度。

因为 PyTorch 默认会累加梯度。

---

# 52. `backward()`

```python
l.backward()
```

作用：

> 根据 Loss 计算网络中所有参数的梯度。

例如：

$$
\frac{\partial L}{\partial W}
$$

得到：

```text
卷积核梯度
全连接层权重梯度
bias 梯度
...
```

---

# 53. `optimizer.step()`

```python
optimizer.step()
```

根据梯度更新参数。

以 SGD 为例：

$$
W=W-\eta\frac{\partial L}{\partial W}
$$

其中：

```text
W
↓
模型参数

η
↓
学习率

∂L/∂W
↓
梯度
```

---

# 54. CNN 为什么可以自动学习卷积核

这是 CNN 非常核心的地方。

卷积核不是人工设计好的。

例如：

```text
训练开始：

卷积核
 ↓
随机初始化
```

然后：

```text
输入图片
 ↓
卷积
 ↓
预测
 ↓
Loss
 ↓
反向传播
 ↓
计算卷积核梯度
 ↓
更新卷积核
```

重复：

```text
很多 Batch
×
很多 Epoch
```

最终：

```text
卷积核
 ↓
逐渐学会检测有意义的特征
```

---

# 55. CNN 中哪些是参数

例如：

```python
nn.Conv2d(
    256,
    384,
    3
)
```

其中：

```text
卷积核权重
```

是参数。

而：

```text
kernel_size = 3
stride = 1
padding = 1
```

这些是：

> **超参数**

不是训练出来的。

---

# 56. 参数和超参数的区别

## 参数

训练过程中自动学习：

```text
Weight
Bias
```

## 超参数

训练前人为设置：

```text
Learning Rate
Batch Size
Kernel Size
Stride
Padding
Epoch
Dropout
```

---

# 57. CNN 的完整数据流

以图像分类为例：

```text
图片
 ↓
像素
 ↓
卷积
 ↓
局部特征
 ↓
ReLU
 ↓
非线性
 ↓
Pooling
 ↓
降低空间尺寸
 ↓
卷积
 ↓
更复杂特征
 ↓
ReLU
 ↓
Pooling
 ↓
...
 ↓
Flatten
 ↓
全连接层
 ↓
分类
 ↓
Loss
 ↓
反向传播
 ↓
更新卷积核
 ↓
下一轮训练
```

---

# 58. CNN 与普通全连接网络的区别

| 对比   | 全连接神经网络        | CNN                          |
| ---- | -------------- | ---------------------------- |
| 英文   | Neural Network | Convolutional Neural Network |
| 连接方式 | 全连接            | 局部连接                         |
| 参数   | 多              | 相对少                          |
| 参数共享 | 没有             | 有                            |
| 空间结构 | 利用较少           | 利用充分                         |
| 图像处理 | 可以             | 非常适合                         |
| 核心操作 | 矩阵乘法           | 卷积                           |
| 典型结构 | MLP            | LeNet、AlexNet、ResNet         |

---

# 59. CNN、RNN、LSTM 的关系

它们都属于神经网络。

```text
Neural Network
│
├── MLP
│
├── CNN
│
├── RNN
│   ├── LSTM
│   └── GRU
│
└── Transformer
```

主要区别在于：

```text
CNN
 ↓
擅长空间结构
 ↓
图像

RNN
 ↓
擅长序列结构
 ↓
文本、时间序列

LSTM
 ↓
RNN 的改进结构
 ↓
解决长期依赖问题

Transformer
 ↓
基于 Attention
 ↓
现代大模型的重要基础
```

---

# 60. CNN 的典型网络发展

CNN 的发展可以大致理解为：

```text
LeNet
  ↓
AlexNet
  ↓
VGG
  ↓
GoogLeNet
  ↓
ResNet
  ↓
更现代的 CNN
```

---

# 61. LeNet

特点：

```text
卷积
+
池化
+
全连接
```

主要证明：

> CNN 可以有效进行图像识别。

---

# 62. AlexNet

AlexNet 的重要贡献包括：

```text
更深的网络
ReLU
Dropout
GPU训练
数据增强
```

它推动了深度学习在计算机视觉中的大发展。

---

# 63. VGG

VGG 的核心思想：

> **使用很多连续的小卷积核。**

例如：

```text
3×3
3×3
3×3
```

而不是大量使用：

```text
11×11
7×7
```

结构更加规整。

---

# 64. GoogLeNet

GoogLeNet 引入：

> **Inception 模块**

一个模块中同时使用不同尺寸的卷积：

```text
1×1
3×3
5×5
Pooling
```

然后组合起来。

思想是：

> 同时从不同尺度提取特征。

---

# 65. ResNet

ResNet 最大的特点：

> **残差连接（Residual Connection）**

普通：

```text
X
 ↓
网络
 ↓
Y
```

ResNet：

```text
        ┌──────────────┐
        │              │
X ──────┼→ 网络 →      + → Y
        │              │
        └──────────────┘
```

数学形式：

$$
Y=F(X)+X
$$

这样可以帮助训练非常深的网络。

---

# 66. CNN 的优点

CNN 主要优点：

### 1. 参数共享

减少参数。

### 2. 局部连接

适合图像空间结构。

### 3. 自动特征提取

不需要人工设计大量特征。

### 4. 层次化学习

可以：

```text
边缘
 ↓
纹理
 ↓
形状
 ↓
对象
```

### 5. 对图像非常有效

因此 CNN 长期以来都是计算机视觉的重要基础。

---

# 67. CNN 的缺点

CNN 也存在一些问题。

### 1. 对全局关系建模能力有限

卷积主要关注局部区域。

需要很多层才能逐渐获得较大的感受野。

### 2. 网络可能很大

例如 AlexNet 的全连接层参数非常多。

### 3. 对数据要求较高

训练大型 CNN 通常需要大量数据和计算资源。

### 4. 长距离依赖不如 Transformer

对于：

```text
自然语言
长序列
全局关系
```

Transformer 通常更加适合。

---

# 68. CNN 中最重要的几个概念

学习 CNN 时，建议重点掌握：

```text
1. Convolution
   卷积

2. Kernel
   卷积核

3. Feature Map
   特征图

4. Channel
   通道

5. Stride
   步幅

6. Padding
   填充

7. Pooling
   池化

8. ReLU
   激活函数

9. Flatten
   展平

10. Dropout
    正则化

11. Receptive Field
    感受野

12. Parameter Sharing
    参数共享
```

---

# 69. CNN 最核心的理解

如果只记住 CNN 的本质，可以记住下面这句话：

> **CNN 使用可学习的卷积核，在输入数据的局部区域上滑动，通过参数共享的方式提取空间特征，并通过多层网络逐渐从低级特征学习到高级特征。**

也就是：

```text
图片
 ↓
卷积核扫描
 ↓
局部特征
 ↓
边缘
 ↓
纹理
 ↓
形状
 ↓
复杂结构
 ↓
物体
 ↓
分类
```

---

# 70. 最终总结

CNN：

```text
Convolutional Neural Network
```

中文：

```text
卷积神经网络
```

属于：

```text
Machine Learning
        ↓
Neural Network
        ↓
CNN
```

CNN 最核心的思想：

```text
局部连接
+
参数共享
+
层次化特征提取
```

核心计算：

```text
输入
 ↓
卷积
 ↓
ReLU
 ↓
池化
 ↓
卷积
 ↓
ReLU
 ↓
池化
 ↓
...
 ↓
Flatten
 ↓
Linear
 ↓
分类
```

其中：

```text
Conv2d
↓
提取特征

ReLU
↓
增加非线性

MaxPool
↓
降低空间尺寸

Flatten
↓
把多维特征转换成一维特征

Linear
↓
进行最终分类

Dropout
↓
减轻过拟合
```

最重要的一点：

> **CNN 并不是人为告诉计算机“什么是边缘、什么是纹理、什么是眼睛”。而是通过反向传播，让卷积核自己从大量训练数据中学习这些特征。**

这也是 CNN 从传统图像处理方法走向深度学习方法的关键。
