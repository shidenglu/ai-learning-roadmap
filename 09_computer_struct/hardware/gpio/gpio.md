# GPIO（General Purpose Input Output）

## 1. 什么是 GPIO

GPIO（General Purpose Input Output）即：

```text
通用输入输出接口
```

GPIO 是 MCU、CPU、SoC 对外连接硬件设备最基础的接口。

例如：

```text
GPIO
 │
 ├── LED
 ├── 按键
 ├── 蜂鸣器
 ├── 继电器
 ├── 中断输入
 └── 外设控制信号
```

---

# 2. GPIO 的作用

GPIO 本质上就是一个可编程数字引脚。

可以配置为：

```text
输入(Input)
输出(Output)
```

例如：

```text
GPIO Output → 控制LED

GPIO Input  → 读取按键
```

---

# 3. GPIO 基本结构

```text
          CPU
           │
           ▼
      GPIO Controller
           │
      ┌────┴────┐
      ▼         ▼
   GPIO0      GPIO1
      │         │
     LED      KEY
```

软件通过 GPIO 控制器访问引脚状态。

---

# 4. GPIO 输入模式

配置为输入：

```c
gpio_direction_input(GPIO0);
```

此时 GPIO 用于读取外部信号。

例如：

```text
按键
 │
 ▼
GPIO
 │
 ▼
CPU
```

读取：

```c
value = gpio_get_value(GPIO0);
```

结果：

```text
0 → Low
1 → High
```

---

# 5. GPIO 输出模式

配置为输出：

```c
gpio_direction_output(GPIO0, 1);
```

此时 GPIO 可以输出电平。

例如：

```text
CPU
 │
 ▼
GPIO
 │
 ▼
LED
```

控制：

```c
gpio_set_value(GPIO0, 1);
```

LED 点亮。

---

# 6. GPIO 电平

通常：

```text
HIGH = 1

LOW  = 0
```

例如：

| 电压   | 状态   |
| ---- | ---- |
| 0V   | Low  |
| 3.3V | High |
| 5V   | High |

具体阈值由芯片决定。

---

# 7. GPIO 输入输出示意

## 输出

```text
GPIO = 1

CPU
 │
 ▼
GPIO ─────► LED

LED ON
```

## 输入

```text
Button
  │
  ▼
GPIO
  │
  ▼
CPU

读取按键状态
```

---

# 8. 上拉与下拉

输入引脚悬空时：

```text
电平不确定
```

因此需要：

```text
Pull-Up
Pull-Down
```

---

## 上拉

```text
VCC
 │
 R
 │
GPIO
 │
KEY
 │
GND
```

未按下：

```text
GPIO = 1
```

按下：

```text
GPIO = 0
```

---

## 下拉

```text
VCC
 │
KEY
 │
GPIO
 │
 R
 │
GND
```

未按下：

```text
GPIO = 0
```

按下：

```text
GPIO = 1
```

---

# 9. GPIO 中断

GPIO 不仅能轮询读取，还能产生中断。

例如：

```text
按键按下
   │
   ▼
GPIO检测到边沿
   │
   ▼
IRQ
   │
   ▼
CPU
```

中断服务函数：

```c
void gpio_isr(void)
{
    /* 按键处理 */
}
```

---

# 10. GPIO 复用（Mux）

现代 SoC 引脚通常支持多种功能。

例如：

```text
PIN0
 │
 ├── GPIO
 ├── UART_TX
 ├── SPI_MOSI
 └── I2C_SDA
```

因此初始化时需要配置：

```text
PinMux
```

例如：

```c
pinmux_set(PIN0, GPIO_FUNC);
```

---

# 11. GPIO 编号

常见编号方式：

```text
GPIOA_0
GPIOA_1
GPIOA_2
...
GPIOB_0
GPIOB_1
...
```

或者：

```text
GPIO0
GPIO1
GPIO2
...
```

---

# 12. GPIO 驱动层次

```text
Application
     │
     ▼
GPIO Driver
     │
     ▼
GPIO Controller
     │
     ▼
GPIO Pin
     │
     ▼
LED / KEY / Sensor
```

---

# 13. 常见 GPIO API

初始化：

```c
gpio_request(pin);
```

设置输入：

```c
gpio_direction_input(pin);
```

设置输出：

```c
gpio_direction_output(pin, value);
```

读取电平：

```c
gpio_get_value(pin);
```

设置电平：

```c
gpio_set_value(pin, value);
```

释放：

```c
gpio_free(pin);
```

---

# 14. GPIO 典型应用

| 应用   | GPIO作用   |
| ---- | -------- |
| LED  | 输出控制     |
| 按键   | 输入检测     |
| 蜂鸣器  | 输出控制     |
| 继电器  | 输出控制     |
| 中断信号 | IRQ输入    |
| 复位信号 | Reset控制  |
| 电源使能 | Enable控制 |

---

# 15. GPIO 核心知识点

```text
GPIO
 │
 ├── Input
 ├── Output
 ├── Pull-Up
 ├── Pull-Down
 ├── Interrupt
 └── PinMux
```

---

# 16. 总结

GPIO 是 MCU/CPU 最基础的硬件接口。

核心功能：

```text
输入(Input)
输出(Output)
```

常见用途：

```text
LED控制
按键检测
中断输入
复位控制
电源控制
外设控制
```

一句话总结：

> **GPIO 本质上是一个可编程数字引脚，可以读取外部电平，也可以输出高低电平控制外部设备，是所有嵌入式系统最基础的硬件接口。**
