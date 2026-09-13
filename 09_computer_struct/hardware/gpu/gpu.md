# GPU（Graphics Processing Unit）图形处理器

## 1. 什么是 GPU

GPU（Graphics Processing Unit）即：

```text
图形处理器
```

最初用于图形渲染，如今广泛应用于：

```text
图形渲染
人工智能
深度学习
科学计算
视频编解码
```

---

# 2. GPU 的位置

```text
          CPU
           │
      PCIe Bus
           │
           ▼
          GPU
           │
           ▼
        VRAM
```

CPU 负责逻辑控制：

```text
流程控制
系统管理
任务调度
```

GPU 负责：

```text
大规模并行计算
```

---

# 3. GPU 与 CPU 对比

| 项目   | CPU     | GPU      |
| ---- | ------- | -------- |
| 核心数量 | 少（数十个）  | 多（数千个）   |
| 单核性能 | 强       | 较弱       |
| 并行能力 | 一般      | 极强       |
| 擅长任务 | 逻辑控制    | 大规模计算    |
| 应用   | OS、应用程序 | 图形、AI、计算 |

---

# 4. GPU 为什么快

CPU：

```text
4~64个强核心
```

GPU：

```text
数千个计算核心
```

例如：

```text
CPU
 ├── Core0
 ├── Core1
 └── Core2

GPU
 ├── Core0
 ├── Core1
 ├── Core2
 ...
 └── Core5000+
```

因此特别适合：

```text
矩阵运算
向量运算
并行计算
```

---

# 5. GPU 基本结构

```text
GPU
 │
 ├── Compute Units
 ├── Shader Cores
 ├── Cache
 ├── Memory Controller
 └── VRAM
```

核心组件：

```text
计算核心
缓存
显存控制器
显存(VRAM)
```

---

# 6. GPU 显存（VRAM）

GPU 拥有独立显存：

```text
GPU
 │
 ▼
VRAM
```

常见：

```text
8GB
12GB
16GB
24GB
32GB+
```

作用：

```text
存储图像

存储模型参数

存储训练数据
```

---

# 7. GPU 在图形中的作用

显示流程：

```text
Application
      │
      ▼
CPU
      │
      ▼
GPU
      │
      ▼
Frame Buffer
      │
      ▼
Display
```

GPU 负责：

```text
几何计算
纹理处理
光照计算
图像渲染
```

---

# 8. GPU 在 AI 中的作用

深度学习本质大量使用：

```text
矩阵乘法
卷积运算
向量计算
```

例如：

```text
Y = W × X + B
```

GPU 可以同时执行大量计算。

```text
Tensor
   │
   ▼
GPU
   │
   ▼
并行计算
```

因此训练速度远高于 CPU。

---

# 9. CUDA

CUDA 是 NVIDIA 的 GPU 计算平台。

```text
PyTorch
    │
    ▼
CUDA
    │
    ▼
GPU
```

常见代码：

```python
device = "cuda"
```

表示：

```text
使用 GPU 计算
```

---

# 10. GPU 驱动层次

```text
Application
      │
      ▼
CUDA/OpenCL
      │
      ▼
GPU Driver
      │
      ▼
GPU Hardware
      │
      ▼
VRAM
```

---

# 11. 常见 GPU 厂商

| 厂商     | 产品            |
| ------ | ------------- |
| NVIDIA | RTX、A100、H100 |
| AMD    | Radeon、MI系列   |
| Intel  | Arc、集成GPU     |

---

# 12. GPU 在 AI 系统中的位置

```text
Dataset
    │
    ▼
CPU
    │
    ▼
GPU
    │
    ▼
Model Training
    │
    ▼
Weights
```

训练过程中：

```text
数据加载 → CPU

模型计算 → GPU

结果保存 → SSD
```

---

# 13. 核心知识点

```text
GPU
 │
 ├── Parallel Computing
 ├── CUDA
 ├── VRAM
 ├── Tensor
 ├── Matrix Multiplication
 ├── Deep Learning
 ├── Rendering
 └── PCIe
```

---

# 14. 总结

GPU 是专门面向并行计算设计的处理器。

核心结构：

```text
CPU
 │
 ▼
PCIe
 │
 ▼
GPU
 │
 ▼
VRAM
```

核心优势：

```text
核心数量多
并行能力强
矩阵运算快
适合AI训练
```

一句话总结：

> **GPU 是一种拥有大量计算核心的并行处理器，最初用于图形渲染，如今已成为深度学习、人工智能和高性能计算的核心硬件。**
