# CE（Channel Estimation，信道估计）代码仿真

## 1. 实验目的

通过 Python + NumPy 模拟 OFDM 系统中的信道估计（CE）过程，理解接收端如何利用已知导频（Pilot）估计无线信道特性。

本实验主要实现：

1. 生成 OFDM 频域数据。
2. 插入已知导频（Pilot）。
3. 通过 IFFT 将频域信号转换为时域信号。
4. 模拟无线多径信道和噪声。
5. 通过 FFT 将时域信号转换为频域信号。
6. 利用 Pilot 进行 LS 信道估计。
7. 通过插值获得其他子载波的信道响应。
8. 利用估计的信道进行均衡。
9. 对比真实信道和估计信道。

## 2. 实验原理

### 2.1 无线信道模型

无线信号在传输过程中，会受到多径传播、信号衰落和噪声等因素影响。

接收信号可以表示为：

\[
Y(k)=H(k)X(k)+N(k)
\]

其中：

| 符号 | 含义 |
|---|---|
| \(X(k)\) | 发送信号 |
| \(H(k)\) | 信道频率响应 |
| \(Y(k)\) | 接收信号 |
| \(N(k)\) | 加性噪声 |

接收端需要估计 \(H(k)\)，才能对接收信号进行补偿。

### 2.2 Pilot（导频信号）

Pilot 是发送端预先定义的已知参考信号，接收端提前知道其内容。

发送端发送 Pilot：

\[
X_p(k)
\]

经过无线信道后：

\[
Y_p(k)=H(k)X_p(k)+N(k)
\]

接收端利用已知的发送 Pilot 和接收到的 Pilot，估计信道响应。

### 2.3 LS 信道估计

LS（Least Squares，最小二乘）是一种常见的信道估计算法。

\[
\hat H_{LS}(k)=\frac{Y_p(k)}{X_p(k)}
\]

其中：

- \(X_p(k)\)：发送端已知的导频。
- \(Y_p(k)\)：接收端收到的导频。
- \(\hat H_{LS}(k)\)：估计得到的信道响应。

### 2.4 信道均衡

得到信道估计结果后，可以利用信道均衡恢复原始数据。

本实验使用 ZF（Zero Forcing，迫零）均衡：

\[
\hat X(k)=\frac{Y(k)}{\hat H(k)}
\]

其中：

- \(Y(k)\)：接收信号。
- \(\hat H(k)\)：估计的信道响应。
- \(\hat X(k)\)：均衡后的信号。

## 3. 实验流程

整个 OFDM 信道估计过程分为发送端和接收端。

### 3.1 发送端

```text
        生成 QPSK 数据
              |
              v
        插入已知 Pilot
              |
              v
             IFFT
              |
              v
          添加 CP
              |
              v
         无线信道传输
```

### 3.2 接收端

```text
         接收无线信号
              |
              v
           去除 CP
              |
              v
             FFT
              |
              v
         提取 Pilot
              |
              v
          信道估计 CE
              |
              v
           信道插值
              |
              v
          信道均衡
              |
              v
           QAM 解调
              |
              v
          恢复原始数据
```

### 3.3 具体处理步骤

| 步骤 | 处理模块 | 主要功能 |
|---|---|---|
| 1 | QPSK | 生成频域调制数据 |
| 2 | Pilot | 插入已知导频 |
| 3 | IFFT | 频域转换为时域 |
| 4 | CP | 添加循环前缀 |
| 5 | Channel | 模拟无线信道 |
| 6 | FFT | 时域转换为频域 |
| 7 | CE | 利用导频估计信道 |
| 8 | Interpolation | 插值获得完整信道响应 |
| 9 | Equalization | 补偿信道造成的影响 |

## 4. Python 仿真环境

安装依赖：

```bash
pip install numpy matplotlib
```

项目结构：

```text
CE_Demo/
│
├── ce_demo.py
└── requirements.txt
```

requirements.txt：

```text
numpy
matplotlib
```

## 5. 完整 Python 代码

文件：`ce_demo.py`

```python
import numpy as np
import matplotlib.pyplot as plt


# ==================================================
# 1. OFDM 参数配置
# ==================================================

N = 64                 # OFDM 子载波数量
CP = 8                 # 循环前缀长度
PILOT_INTERVAL = 4     # 每隔 4 个子载波插入一个 Pilot
SNR_DB = 25            # 信噪比


# ==================================================
# 2. 生成 OFDM 频域数据
# ==================================================

np.random.seed(42)

# 生成 QPSK 数据
data = (
    (2 * np.random.randint(0, 2, N) - 1)
    + 1j * (2 * np.random.randint(0, 2, N) - 1)
) / np.sqrt(2)

# Pilot 位置
pilot_idx = np.arange(0, N, PILOT_INTERVAL)

# 数据位置
data_idx = np.setdiff1d(np.arange(N), pilot_idx)

# 频域发送信号
X = np.zeros(N, dtype=complex)

# 插入数据
X[data_idx] = data[data_idx]

# 插入已知 Pilot
X[pilot_idx] = 1 + 0j


# ==================================================
# 3. IFFT：频域转换为时域
# ==================================================

tx_time = np.fft.ifft(X)

# 添加循环前缀 CP
tx_cp = np.concatenate((tx_time[-CP:], tx_time))


# ==================================================
# 4. 模拟无线信道
# ==================================================

# 多径信道冲激响应
h = np.zeros(6, dtype=complex)

h[0] = 1.0
h[2] = 0.35 * np.exp(1j * 0.6)
h[5] = 0.20 * np.exp(-1j * 0.8)

# 真实信道频率响应
H_true = np.fft.fft(h, N)

# 信号经过多径信道
rx_full = np.convolve(tx_cp, h)

# 去掉循环前缀对应的时域部分
rx_time = rx_full[CP:CP + N]

# 添加 AWGN 高斯白噪声
signal_power = np.mean(np.abs(rx_time) ** 2)
noise_power = signal_power / (10 ** (SNR_DB / 10))

noise = np.sqrt(noise_power / 2) * (
    np.random.randn(N) + 1j * np.random.randn(N)
)

rx_time = rx_time + noise


# ==================================================
# 5. FFT：时域转换为频域
# ==================================================

Y = np.fft.fft(rx_time)


# ==================================================
# 6. CE：LS 信道估计
# ==================================================

# 提取接收到的 Pilot
Y_pilot = Y[pilot_idx]

# 提取发送端已知的 Pilot
X_pilot = X[pilot_idx]

# LS 信道估计
H_pilot_est = Y_pilot / X_pilot


# ==================================================
# 7. 信道插值
# ==================================================

# 对实部和虚部分别进行线性插值
H_est = (
    np.interp(np.arange(N), pilot_idx, H_pilot_est.real)
    + 1j * np.interp(
        np.arange(N), pilot_idx, H_pilot_est.imag
    )
)


# ==================================================
# 8. 信道均衡
# ==================================================

# ZF 均衡
Y_equalized = Y[data_idx] / (
    H_est[data_idx] + 1e-10
)

# 原始数据
X_original = X[data_idx]


# ==================================================
# 9. 计算信道估计误差
# ==================================================

mse = np.mean(np.abs(H_true - H_est) ** 2)

print("=" * 45)
print("OFDM Channel Estimation Demo")
print("=" * 45)

print(f"子载波数量: {N}")
print(f"Pilot 数量: {len(pilot_idx)}")
print(f"数据数量: {len(data_idx)}")
print(f"信噪比 SNR: {SNR_DB} dB")
print(f"信道估计 MSE: {mse:.6f}")


# ==================================================
# 10. 绘制仿真结果
# ==================================================

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# 图 1：真实信道与估计信道的幅度
axes[0, 0].plot(
    np.abs(H_true),
    label="True Channel",
    linewidth=2
)

axes[0, 0].plot(
    np.abs(H_est),
    "--",
    label="Estimated Channel",
    linewidth=2
)

axes[0, 0].scatter(
    pilot_idx,
    np.abs(H_pilot_est),
    marker="o",
    label="Pilot Estimation"
)

axes[0, 0].set_title("Channel Magnitude")
axes[0, 0].set_xlabel("Subcarrier")
axes[0, 0].set_ylabel("Magnitude")
axes[0, 0].legend()
axes[0, 0].grid()


# 图 2：真实信道与估计信道的相位
axes[0, 1].plot(
    np.unwrap(np.angle(H_true)),
    label="True Channel"
)

axes[0, 1].plot(
    np.unwrap(np.angle(H_est)),
    "--",
    label="Estimated Channel"
)

axes[0, 1].set_title("Channel Phase")
axes[0, 1].set_xlabel("Subcarrier")
axes[0, 1].set_ylabel("Phase (rad)")
axes[0, 1].legend()
axes[0, 1].grid()


# 图 3：均衡前的星座图
axes[1, 0].scatter(
    Y[data_idx].real,
    Y[data_idx].imag,
    label="Before Equalization"
)

axes[1, 0].set_title("Before Equalization")
axes[1, 0].set_xlabel("In-phase")
axes[1, 0].set_ylabel("Quadrature")
axes[1, 0].grid()
axes[1, 0].axis("equal")


# 图 4：均衡后的星座图
axes[1, 1].scatter(
    Y_equalized.real,
    Y_equalized.imag,
    label="Equalized"
)

axes[1, 1].scatter(
    X_original.real,
    X_original.imag,
    marker="x",
    label="Original Data"
)

axes[1, 1].set_title("After Equalization")
axes[1, 1].set_xlabel("In-phase")
axes[1, 1].set_ylabel("Quadrature")
axes[1, 1].legend()
axes[1, 1].grid()
axes[1, 1].axis("equal")


plt.tight_layout()
plt.show()
```

## 6. 关键代码解析

### 6.1 生成 Pilot

```python
pilot_idx = np.arange(0, N, PILOT_INTERVAL)

data_idx = np.setdiff1d(np.arange(N), pilot_idx)

X = np.zeros(N, dtype=complex)

X[data_idx] = data[data_idx]

X[pilot_idx] = 1 + 0j
```

每隔 4 个子载波插入一个 Pilot。

本实验将 Pilot 设置为：

\[
X_p(k)=1+0j
\]

因此，发送端和接收端都知道 Pilot 的具体值。

### 6.2 模拟无线信道

```python
h = np.zeros(6, dtype=complex)

h[0] = 1.0
h[2] = 0.35 * np.exp(1j * 0.6)
h[5] = 0.20 * np.exp(-1j * 0.8)
```

这里模拟一个三径无线信道。

| 路径 | 延迟 | 幅度 | 相位 |
|---|---:|---:|---:|
| 路径 1 | 0 | 1.0 | 0 |
| 路径 2 | 2 | 0.35 | 0.6 rad |
| 路径 3 | 5 | 0.20 | -0.8 rad |

不同路径的信号经过不同延迟、幅度和相位变化后，在接收端叠加。

通过：

```python
H_true = np.fft.fft(h, N)
```

可以得到真实信道的频率响应。

### 6.3 LS 信道估计

```python
Y_pilot = Y[pilot_idx]

X_pilot = X[pilot_idx]

H_pilot_est = Y_pilot / X_pilot
```

这是整个 CE 的核心。

假设：

```text
发送 Pilot = 1 + 0j

接收 Pilot = 0.8 + 0.2j
```

那么：

\[
\hat H=\frac{0.8+0.2j}{1}=0.8+0.2j
\]

说明信道对信号造成了幅度和相位变化。

### 6.4 信道插值

```python
H_est = (
    np.interp(np.arange(N), pilot_idx, H_pilot_est.real)
    + 1j * np.interp(
        np.arange(N), pilot_idx, H_pilot_est.imag
    )
)
```

Pilot 只分布在部分子载波上，因此无法直接得到所有子载波的信道响应。

这里分别对信道响应的实部和虚部进行线性插值，获得完整的信道估计结果。

### 6.5 信道均衡

```python
Y_equalized = Y[data_idx] / (
    H_est[data_idx] + 1e-10
)
```

利用估计的信道响应对接收数据进行补偿。

其中 `1e-10` 用于避免分母为零。

## 7. 仿真结果分析

程序运行后会输出四张图。

### 7.1 信道幅度对比

对比真实信道和估计信道的幅度。

- True Channel：真实信道幅度。
- Estimated Channel：估计信道幅度。
- Pilot Estimation：导频位置的估计结果。

两条曲线越接近，说明信道估计效果越好。

### 7.2 信道相位对比

对比真实信道和估计信道的相位。

信道不仅会改变信号幅度，还会引起相位变化。

### 7.3 均衡前星座图

无线信号经过信道后，QPSK 星座点会发生旋转、缩放和偏移。

接收端直接使用原始数据进行解调，可能产生错误。

### 7.4 均衡后星座图

利用 CE 得到的信道响应进行均衡后，接收星座点会重新靠近原始 QPSK 星座点。

说明信道均衡能够补偿信道造成的影响。

## 8. 信道估计误差 MSE

MSE（Mean Squared Error，均方误差）用于衡量估计信道与真实信道之间的差异。

计算公式：

\[
MSE=\frac{1}{N}\sum_{k=0}^{N-1}
|H(k)-\hat H(k)|^2
\]

其中：

- \(H(k)\)：真实信道响应。
- \(\hat H(k)\)：估计信道响应。
- \(N\)：子载波数量。

MSE 越小，表示信道估计越准确。

## 9. 实验总结

本实验模拟了 OFDM 系统中完整的信道估计过程。

| 模块 | 作用 |
|---|---|
| QPSK | 生成调制数据 |
| Pilot | 提供已知参考信号 |
| IFFT | 频域转换为时域 |
| Channel | 模拟无线信道 |
| FFT | 时域转换为频域 |
| CE | 利用 Pilot 估计信道 |
| Interpolation | 推算其他子载波的信道 |
| Equalization | 补偿信道影响 |

核心处理关系：

\[
\boxed{
\text{Pilot}
\rightarrow
\text{CE}
\rightarrow
\hat H
\rightarrow
\text{Equalization}
}
\]

**核心理解：Pilot 是已知的参考信号，CE 利用 Pilot 估计无线信道，信道均衡再利用估计结果恢复原始数据。**

## 10. 实验扩展

当前实验使用 LS 算法进行信道估计，可以进一步扩展：

1. **LS 与 MMSE 对比**：比较不同算法的信道估计精度。
2. **SNR 仿真**：改变信噪比，观察 MSE 的变化。
3. **Pilot 密度实验**：改变导频间隔，观察估计效果。
4. **多径信道实验**：增加多径数量和传播延迟。
5. **MIMO 信道估计**：扩展到多天线通信系统。

这些实验可以进一步帮助理解 LTE、5G NR 中的信道估计技术。