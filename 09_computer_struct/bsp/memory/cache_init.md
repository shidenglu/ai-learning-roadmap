# BSP 中的 Cache 初始化

## 1. 作用

BSP 的 Cache 初始化负责在系统启动阶段完成 CPU Cache 的基础配置，使 CPU 能够正常、高效地访问内存。

```text
CPU
 │
 ├── I-Cache ──→ 指令
 │
 └── D-Cache ──→ 数据
        │
        ↓
       DDR
```

---

## 2. BSP 主要负责的内容

BSP 通常负责：

- Cache 状态检查
- Cache 参数获取
- 必要的 Cache Invalidate
- I-Cache 初始化与开启
- D-Cache 初始化与开启
- 配合 MMU 设置内存 Cache 属性
- Cache 开启前后的必要同步

---

## 3. I-Cache 与 D-Cache

| Cache | 作用 |
|---|---|
| I-Cache | 缓存 CPU 执行的指令 |
| D-Cache | 缓存 CPU 访问的数据 |

```text
             CPU
              │
       ┌──────┴──────┐
       ↓             ↓
    I-Cache        D-Cache
       │             │
     指令            数据
```

---

## 4. Cache 初始化流程

```text
CPU Reset
   ↓
CPU 基础初始化
   ↓
检查 Cache 状态
   ↓
必要时 Invalidate Cache
   ↓
配置 MMU / Memory Attribute
   ↓
开启 I-Cache
   ↓
开启 D-Cache
   ↓
进入 Kernel / RTOS
```

---

## 5. Cache 与 MMU

Cache 属性通常需要与 MMU 的内存属性配合。

```text
MMU
 │
 ├── Normal Memory
 │      └── Cacheable
 │           └── DDR / RAM
 │
 └── Device Memory
        └── Non-cacheable
             └── UART / GIC / 外设寄存器
```

典型配置：

| 内存区域 | 典型属性 |
|---|---|
| DDR / RAM | Normal + Cacheable |
| UART | Device + Non-cacheable |
| GIC | Device + Non-cacheable |
| DMA Buffer | 根据平台 DMA 一致性方案配置 |

---

## 6. Cache Invalidate

BSP 在开启 Cache 前，可能需要将 Cache 中已有内容失效：

```text
Cache Invalidate
       ↓
Cache 内容失效
       ↓
重新从内存获取数据
       ↓
开启 Cache
```

是否需要 Invalidate，以及具体操作方式，取决于 CPU 架构和启动环境。

---

## 7. ARM64 常见寄存器

| 寄存器 | 作用 |
|---|---|
| `SCTLR_EL1` | 控制 MMU、I-Cache、D-Cache |
| `CTR_EL0` | Cache 基本信息 |
| `CCSIDR_EL1` | Cache 大小、组数、路数 |
| `CSSELR_EL1` | 选择 Cache Level |

`SCTLR_EL1` 中常见控制位：

```text
M → MMU Enable
C → D-Cache Enable
I → I-Cache Enable
```

---

## 8. BSP 与 Kernel / RTOS 的边界

```text
BSP
 │
 ├── Cache 基础配置
 ├── Cache 状态初始化
 ├── I/D-Cache 开启
 └── 启动阶段必要的 Invalidate
              ↓
        Kernel / RTOS
              │
              ├── Cache 运行时管理
              ├── Clean / Flush
              ├── Invalidate
              ├── DMA Cache 一致性
              └── 多核 Cache 管理
```

BSP 主要负责：

> **建立系统启动所需要的 Cache 基础运行环境。**

而系统运行期间的 Cache 管理由 Kernel、RTOS 或驱动负责。

---

## 9. 一句话总结

> **BSP Cache 初始化 = Cache 基础配置 + 必要的 Invalidate + I/D-Cache 开启 + 配合 MMU 设置内存属性，为 Kernel/RTOS 提供 Cache 基础运行环境。**