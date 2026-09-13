# BSP 中的 Timer 初始化

## 1. 作用

BSP 的 Timer 初始化负责在系统启动阶段配置硬件定时器，为 Kernel / RTOS 提供基础的时间基准。

```text
Clock
  ↓
Timer
  ↓
产生周期性 Tick / 中断
  ↓
Kernel / RTOS
```

---

## 2. BSP 主要负责的内容

BSP 通常负责：

- 获取 Timer 时钟源
- 配置 Timer 工作频率
- 配置计数模式
- 设置初始计数值 / 重载值
- 配置 Timer 中断
- 注册 Timer 中断处理函数
- 启动 Timer

---

## 3. Timer 初始化流程

```text
Timer Clock
    ↓
配置 Timer
    ↓
设置计数频率
    ↓
设置周期 / Reload Value
    ↓
配置 Timer Interrupt
    ↓
注册 ISR
    ↓
启动 Timer
```

---

## 4. Timer Tick

例如：

```text
Timer Clock = 1 MHz
Timer Period = 1 ms

1 MHz × 1 ms = 1000 个计数
```

Timer 每计数 1000 次产生一次中断：

```text
Timer
 │
 ├── 计数
 ├── 计数
 ├── 计数
 ↓
达到 Reload Value
 │
 ↓
Timer Interrupt
 │
 ↓
Kernel Tick
```

---

## 5. Timer 中断

Timer 到期后通常产生硬件中断：

```text
Timer
  ↓
IRQ
  ↓
GIC
  ↓
CPU
  ↓
Timer ISR
  ↓
Kernel / RTOS Tick
```

BSP 主要负责：

> **把 Timer 配置好，并让 Timer 中断能够正确到达 CPU。**

---

## 6. Timer 与 Clock 的关系

```text
Clock Source
     ↓
   PLL / Divider
     ↓
 Timer Clock
     ↓
 Timer Counter
     ↓
 Timer IRQ
```

因此 Timer 初始化通常依赖 BSP 的 Clock 初始化。

---

## 7. BSP 与 Kernel / RTOS 的边界

```text
BSP
 │
 ├── Timer 硬件初始化
 ├── Timer Clock 配置
 ├── Timer 周期配置
 ├── Timer IRQ 配置
 └── Timer 启动
          ↓
     Kernel / RTOS
          │
          ├── Tick 管理
          ├── 软件定时器
          ├── 任务延时
          └── 超时管理
```

BSP 负责 **硬件 Timer**，Kernel / RTOS 负责 **系统时间管理**。

---

## 8. 一句话总结

> **BSP Timer 初始化 = 配置 Timer 时钟、计数周期和中断，并启动硬件 Timer，为 Kernel / RTOS 提供基础时间 Tick。**