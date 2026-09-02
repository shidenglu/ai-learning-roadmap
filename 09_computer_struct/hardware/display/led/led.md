# LED（Light Emitting Diode）发光二极管

## 1. 什么是 LED

LED（Light Emitting Diode）即：

```text
发光二极管
```

是一种能够将电能转换为光能的半导体器件。

常用于：

```text
指示灯
状态灯
数码管
背光源
照明设备
显示屏
```

---

# 2. LED 基本结构

```text
      Anode(+)
          │
          ▼
      LED芯片
          │
          ▼
     Cathode(-)
```

当电流流过 LED 时：

```text
电流
  ↓
电子跃迁
  ↓
释放光子
  ↓
发光
```

---

# 3. LED 电路连接

最常见接法：

```text
VCC
 │
 R
 │
LED
 │
GPIO
 │
GND
```

其中：

```text
R
```

为限流电阻，用于保护 LED。

---

# 4. LED 工作原理

GPIO 输出高低电平控制 LED。

### 点亮

```text
GPIO = 0

VCC
 │
 R
 │
LED
 │
GPIO
 │
GND
```

形成电流回路：

```text
LED ON
```

---

### 熄灭

```text
GPIO = 1
```

无电流流过：

```text
LED OFF
```

---

# 5. LED 常见颜色

| 颜色 | 典型用途  |
| -- | ----- |
| 红色 | 电源指示  |
| 绿色 | 正常运行  |
| 黄色 | 告警状态  |
| 蓝色 | 工作状态  |
| 白色 | 照明/背光 |

---

# 6. LED 驱动方式

## GPIO 直接驱动

```c
gpio_set_value(LED_GPIO, 1);
```

适用于：

```text
状态灯
指示灯
```

---

## PWM 驱动

通过 PWM 调节占空比：

```text
占空比增大
      ↓
亮度提高
```

例如：

```text
10% → 较暗

50% → 中等亮度

100% → 最亮
```

---

# 7. LED 闪烁控制

常见实现：

```c
while (1)
{
    led_on();
    delay_ms(500);

    led_off();
    delay_ms(500);
}
```

效果：

```text
亮0.5秒
灭0.5秒
循环
```

---

# 8. LED 驱动层次

```text
Application
      │
      ▼
LED Driver
      │
      ▼
GPIO/PWM Driver
      │
      ▼
LED
```

---

# 9. 常见应用

| 场景   | 用途   |
| ---- | ---- |
| 开发板  | 状态指示 |
| 路由器  | 网络状态 |
| 工控设备 | 告警指示 |
| 汽车   | 仪表灯  |
| 显示屏  | 像素显示 |
| 手机   | 闪光灯  |

---

# 10. 核心知识点

```text
LED
 │
 ├── 发光二极管
 ├── 正向导通
 ├── 限流电阻
 ├── GPIO控制
 ├── PWM调光
 ├── 状态指示
 └── 背光显示
```

---

# 11. 总结

LED 是嵌入式系统中最常见的输出设备之一。

典型控制链路：

```text
Application
     │
     ▼
LED Driver
     │
     ▼
GPIO / PWM
     │
     ▼
LED
```

一句话总结：

> **LED 是一种通过电流驱动发光的半导体器件，在嵌入式系统中通常由 GPIO 或 PWM 控制，用于状态指示、照明和显示。**
