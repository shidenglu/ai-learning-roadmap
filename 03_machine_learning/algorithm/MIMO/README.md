# 4T256R Massive MIMO 收发与解调全过程详解

# 1. 系统模型概述

假设：

```text
发射端(Tx) ：4根天线
接收端(Rx) ：256根天线

调制方式：QPSK
信道模型：Rayleigh
检测算法：ZF
```

系统框图：

```text
Bit
 ↓
QPSK
 ↓
4层空间流
 ↓
4T发射
 ↓
MIMO信道 H
 ↓
256R接收
 ↓
ZF检测
 ↓
QPSK解调
 ↓
Bit
```

---

# 2. 什么是4T256R

4T：

```text
4 Transmit Antennas
```

256R：

```text
256 Receive Antennas
```

示意图：

```text
Tx1 ─────────┐
Tx2 ─────────┼──► 256根接收天线
Tx3 ─────────┼──►
Tx4 ─────────┘
```

---

# 3. 比特产生

随机生成数据：

```python
bits = np.random.randint(
    0,
    2,
    (Nsym,4,2)
)
```

例如：

```text
Tx1 : 01
Tx2 : 10
Tx3 : 11
Tx4 : 00
```

---

# 4. QPSK调制

映射关系：

```text
00 → +1+j
01 → +1-j
10 → -1+j
11 → -1-j
```

归一化：

```math
s = \frac{I+jQ}{\sqrt{2}}
```

例如：

```text
00 → 0.707+0.707j
01 → 0.707-0.707j
10 → -0.707+0.707j
11 → -0.707-0.707j
```

---

# 5. 构造发送向量

某个时刻：

```math
x=
\begin{bmatrix}
x_1\\
x_2\\
x_3\\
x_4
\end{bmatrix}
```

维度：

```text
4×1
```

例如：

```math
x=
\begin{bmatrix}
0.707+0.707j\\
-0.707+0.707j\\
0.707-0.707j\\
-0.707-0.707j
\end{bmatrix}
```

---

# 6. MIMO信道矩阵

信道：

```math
H \in \mathbb{C}^{256\times4}
```

表示：

```text
256根接收天线
4根发送天线
```

结构：

```math
H=
\begin{bmatrix}
h_{11}&h_{12}&h_{13}&h_{14}\\
h_{21}&h_{22}&h_{23}&h_{24}\\
\vdots&\vdots&\vdots&\vdots\\
h_{256,1}&h_{256,2}&h_{256,3}&h_{256,4}
\end{bmatrix}
```

其中：

```math
h_{ij}
```

表示：

```text
Tx_j → Rx_i
```

的复数信道增益。

---

# 7. 瑞利衰落模型

仿真：

```python
H = (
    np.random.randn(256,4)
    +
    1j*np.random.randn(256,4)
)/np.sqrt(2)
```

数学表示：

```math
h_{ij}
=
\frac{1}{\sqrt{2}}
(
N(0,1)
+
jN(0,1)
)
```

---

# 8. 信号传播

接收信号：

```math
y = Hx
```

维度：

```text
(256×4)
×
(4×1)
=
(256×1)
```

得到：

```math
y=
\begin{bmatrix}
y_1\\
y_2\\
\vdots\\
y_{256}
\end{bmatrix}
```

---

# 9. 展开理解

第1根接收天线：

```math
y_1=
h_{11}x_1+
h_{12}x_2+
h_{13}x_3+
h_{14}x_4
```

第2根接收天线：

```math
y_2=
h_{21}x_1+
h_{22}x_2+
h_{23}x_3+
h_{24}x_4
```

......

第256根接收天线：

```math
y_{256}
=
h_{256,1}x_1+
h_{256,2}x_2+
h_{256,3}x_3+
h_{256,4}x_4
```

---

# 10. 添加噪声

真实系统：

```math
y = Hx+n
```

其中：

```math
n
=
\begin{bmatrix}
n_1\\
n_2\\
\vdots\\
n_{256}
\end{bmatrix}
```

表示AWGN噪声。

---

# 11. 接收端问题

已知：

```math
y
```

和

```math
H
```

求：

```math
x
```

即：

```text
恢复4路发送数据
```

---

# 12. ZF检测

求伪逆：

\begin{aligned} y &= Hx \ x &= (H^H H)^{-1}H^H y \end{aligned}

对应权矩阵：

```math
W=(H^H H)^{-1}H^H
```

维度分析：

```math
H
=
256\times4
```

则：

```math
H^H
=
4\times256
```

所以：

```math
H^H H
=
4\times4
```

最终：

```math
W
=
4\times256
```

---

# 13. 恢复发送信号

```math
\hat{x}=Wy
```

维度：

```text
(4×256)
×
(256×1)
=
(4×1)
```

结果：

```math
\hat{x}
=
\begin{bmatrix}
\hat{x}_1\\
\hat{x}_2\\
\hat{x}_3\\
\hat{x}_4
\end{bmatrix}
```

---

# 14. 为什么256根天线效果好

核心量：

```math
H^H H
```

当：

```text
Nr >> Nt
```

即：

```text
256 >> 4
```

时：

```math
\frac{1}{256}H^H H
\approx I
```

即：

```math
H^H H
\approx
256I
```

因此：

```math
W
\approx
\frac{1}{256}H^H
```

检测变得非常简单。

---

# 15. Massive MIMO本质

随着接收天线增加：

```text
4R
8R
16R
32R
64R
128R
256R
```

会出现：

```text
信道向量逐渐正交
```

即：

```math
h_i^H h_j
\rightarrow 0
```

其中：

```math
i \ne j
```

因此：

```text
不同空间流互不干扰
```

---

# 16. QPSK解调

检测后：

```math
\hat{x}
=
0.81+0.65j
```

判断：

```text
实部 > 0
虚部 > 0
```

得到：

```text
00
```

例如：

```math
-0.9+0.7j
```

得到：

```text
10
```

规则：

```text
Re > 0 → 0
Re < 0 → 1

Im > 0 → 0
Im < 0 → 1
```

---

# 17. BER计算

发送：

```text
1000000 bits
```

恢复：

```text
999995 bits正确
```

错误：

```text
5 bits
```

则：

```math
BER
=
\frac{5}{1000000}
=
5\times10^{-6}
```

---

# 18. 与5G基站的对应关系

真实5G：

```text
UE:
4T4R

gNB:
256T256R
```

流程：

```text
Bit
 ↓
LDPC
 ↓
QAM
 ↓
Layer Mapping
 ↓
Precoding
 ↓
OFDM
 ↓
DMRS/SRS
 ↓
无线信道
 ↓
Channel Estimation
 ↓
MMSE
 ↓
LLR
 ↓
LDPC Decode
 ↓
Bit
```

---

# 19. SRS与信道估计

实际系统并不知道：

```math
H
```

需要发送：

```text
SRS
```

导频：

```math
X_{SRS}
```

接收：

```math
Y_{SRS}
=
HX_{SRS}
\;+\;
N
```

估计：

```math
\hat H
=
Y_{SRS}
X_{SRS}^{-1}
```

得到：

```math
256×4
```

的信道矩阵。

---

# 20. 总结

4T256R Massive MIMO 的核心数学模型只有一句：

```math
y = Hx+n
```

发送端：

```text
Bit
→ QPSK
→ 4层空间流
```

接收端：

```text
256根天线
↓
获得256路观测
↓
ZF/MMSE
↓
恢复4层数据
↓
QPSK解调
↓
Bit
```

由于：

```text
256 >> 4
```

因此：

```text
空间流容易分离
干扰容易消除
BER极低
```

这就是 Massive MIMO 能够支撑 5G 高容量、高频谱效率的根本原因。
