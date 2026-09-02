# Timer（定时器）

## 1. 什么是 Timer

Timer（定时器）是 MCU、CPU、SoC 内部的一种硬件模块，用于：

```text
计时
延时
周期触发
测量时间
产生PWM
```

Timer 本质上是一个：

```text
硬件计数器(Counter)
```

---

# 2. Timer 基本结构

```text
Clock
  │
  ▼
Prescaler
  │
  ▼
Counter
  │
  ▼
Compare/Overflow
  │
  ▼
Interrupt
```

---

# 3. 工作原理

时钟不断驱动计数器递增：

```text
0
1
2
3
4
...
```

达到设定值后：

```text
触发中断
产生事件
重新计数
```

---

# 4. Timer 核心组成

| 模块               | 作用    |
| ---------------- | ----- |
| Clock            | 时钟源   |
| Prescaler        | 分频器   |
| Counter          | 计数器   |
| Compare Register | 比较寄存器 |
| Interrupt        | 定时中断  |

---

# 5. 定时中断

例如：

```text
每 1ms 触发一次
```

流程：

```text
Timer
  │
  ▼
计数到设定值
  │
  ▼
IRQ
  │
  ▼
CPU
```

代码示例：

```c
void timer_isr(void)
{
    /* 周期任务 */
}
```

---

# 6. 延时功能

Timer 常用于实现：

```text
1ms
10ms
100ms
1s
```

等精确定时。

例如：

```c
delay_ms(100);
```

---

# 7. PWM 输出

Timer 可以产生 PWM 波形：

```text
 ┌───┐     ┌───┐
 │   │     │   │
 │   │     │   │
─┘   └─────┘   └────
```

应用：

```text
LED调光
电机控制
蜂鸣器
风扇控制
```

---

# 8. 输入捕获（Input Capture）

用于测量外部信号时间。

例如：

```text
测量脉宽

测量频率

测量周期
```

```text
外部信号
    │
    ▼
Timer Capture
    │
    ▼
记录计数值
```

---

# 9. 看门狗定时器（Watchdog）

特殊 Timer：

```text
系统正常
    ↓
定期喂狗

长时间未喂狗
    ↓
系统复位
```

用于提高系统可靠性。

---

# 10. Timer 驱动层次

```text
Application
      │
      ▼
Timer Driver
      │
      ▼
Timer Controller
      │
      ▼
Clock Source
```

---

# 11. 常见应用

| 场景        | 用途            |
| --------- | ------------- |
| 操作系统 Tick | 系统时钟          |
| 延时函数      | delay_ms      |
| LED闪烁     | 周期控制          |
| PWM       | 调光/调速         |
| 电机控制      | PWM输出         |
| 频率测量      | Input Capture |
| 看门狗       | 系统保护          |

---

# 12. 常见 API

启动：

```c
timer_start();
```

停止：

```c
timer_stop();
```

设置周期：

```c
timer_set_period(1000);
```

注册中断：

```c
timer_register_isr();
```

---

# 13. 核心知识点

```text
Timer
 │
 ├── Clock
 ├── Prescaler
 ├── Counter
 ├── Interrupt
 ├── Delay
 ├── PWM
 ├── Capture
 └── Watchdog
```

---

# 14. 总结

Timer 是嵌入式系统中最重要的硬件模块之一，本质是一个由时钟驱动的计数器。

核心流程：

```text
Clock
  │
  ▼
Counter
  │
  ▼
Overflow/Compare
  │
  ▼
Interrupt/PWM/Event
```

一句话总结：

> **Timer 是一种基于硬件计数器实现时间管理的模块，可用于定时中断、延时、PWM 输出、频率测量以及系统时钟等功能。**
