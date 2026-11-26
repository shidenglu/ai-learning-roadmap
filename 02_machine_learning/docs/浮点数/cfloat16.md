# CFLOAT16（半精度复数浮点数）

## 1. CFLOAT16 是什么

CFLOAT16（Complex Float16）是一种半精度复数浮点数类型，由两个 FLOAT16 组成，分别表示复数的实部和虚部。

复数表示：

\[
z=a+bi
\]

- `a`：实部（Real）
- `b`：虚部（Imaginary）
- `i`：虚数单位，满足 \(i^2=-1\)

## 2. 数据结构

CFLOAT16 通常由两个 IEEE 754 FP16 数值组成：

| 字段 | 数据类型 | 位数 |
|---|---|---:|
| 实部 Real | FLOAT16 | 16 bit |
| 虚部 Imaginary | FLOAT16 | 16 bit |
| 合计 | CFLOAT16 | 32 bit |

```text
+------------------+------------------+
| Real (FLOAT16)   | Imag (FLOAT16)   |
|     16 bit       |     16 bit       |
+------------------+------------------+
              32 bit
```

单个 CFLOAT16 元素通常占用 4 字节。

## 3. 数值示例

表示复数：

\[
z=1.5+2.5i
\]

存储方式：

```text
Real      = FLOAT16(1.5)
Imaginary = FLOAT16(2.5)
```

两个 FP16 组合后，表示一个复数。

## 4. 常见复数浮点类型

| 类型 | 实部 | 虚部 | 总位数 |
|---|---|---|---:|
| CFLOAT16 | FP16 | FP16 | 32 bit |
| CFLOAT32 | FP32 | FP32 | 64 bit |
| CFLOAT64 | FP64 | FP64 | 128 bit |

## 5. 应用场景

CFLOAT16 常用于需要复数运算且希望降低存储开销的场景：

- FFT / IFFT
- OFDM 数字通信
- 信道估计（CE）
- 复数神经网络
- GPU 低精度复数计算

例如 OFDM 频域子载波：

\[
X_k=1.2+0.8i
\]

可以使用 CFLOAT16 存储实部和虚部。

## 6. PyTorch 示例

PyTorch 使用 `torch.complex32`（别名 `torch.chalf`）表示半精度复数：

```python
import torch

real = torch.tensor([1.5], dtype=torch.float16)
imag = torch.tensor([2.5], dtype=torch.float16)

z = torch.complex(real, imag)

print(z)
print(z.dtype)
print(z.element_size())
```

注意：不同框架对 CFLOAT16 的命名和运算支持可能不同。

## 7. 总结

1. CFLOAT16 是半精度复数浮点数。
2. 由两个 FLOAT16 组成，分别表示实部和虚部。
3. 单个元素通常占用 32 bit（4 字节）。
4. 常用于 FFT、OFDM 和复数信号处理。
5. 相比 CFLOAT32，存储空间减少一半，但数值精度降低。

**核心：CFLOAT16 = FP16 实部 + FP16 虚部。**