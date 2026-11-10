
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

# ZF 均衡，避免除数过小
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