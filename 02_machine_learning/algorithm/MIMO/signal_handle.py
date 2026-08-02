import numpy as np

# ==========================================
# 参数
# ==========================================

Nt = 4
Nr = 256

Nsym = 10000

SNR_dB = 10

# ==========================================
# QPSK
# ==========================================

bits = np.random.randint(
    0,
    2,
    (Nsym, Nt, 2)
)

symbols = (
    (2 * bits[...,0] - 1)
    +
    1j * (2 * bits[...,1] - 1)
) / np.sqrt(2)

# ==========================================
# Rayleigh Channel
# ==========================================

H = (
    np.random.randn(Nsym, Nr, Nt)
    +
    1j * np.random.randn(Nsym, Nr, Nt)
) / np.sqrt(2)

# ==========================================
# 发射
# ==========================================

y = np.zeros(
    (Nsym, Nr),
    dtype=complex
)

for k in range(Nsym):

    y[k] = H[k] @ symbols[k]

# ==========================================
# AWGN
# ==========================================

signal_power = np.mean(np.abs(y)**2)

noise_power = signal_power / (
    10**(SNR_dB/10)
)

noise = (
    np.random.randn(*y.shape)
    +
    1j*np.random.randn(*y.shape)
) * np.sqrt(noise_power/2)

y += noise

# ==========================================
# ZF检测
# ==========================================

x_hat = np.zeros(
    (Nsym, Nt),
    dtype=complex
)

for k in range(Nsym):

    W = np.linalg.pinv(H[k])

    x_hat[k] = W @ y[k]

# ==========================================
# 解调
# ==========================================

bits_hat = np.zeros_like(bits)

bits_hat[...,0] = np.real(x_hat) > 0
bits_hat[...,1] = np.imag(x_hat) > 0

BER = np.mean(bits != bits_hat)

print("BER =", BER)