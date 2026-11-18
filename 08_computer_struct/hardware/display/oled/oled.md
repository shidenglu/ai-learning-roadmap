# OLED（Organic Light Emitting Diode）有机发光二极管

## 1. 什么是 OLED

OLED（Organic Light Emitting Diode）即：

```text
有机发光二极管显示器
```

是一种**自发光显示技术**，每个像素都能独立发光，无需背光。

常见于：

```text
手机
智能手表
电视
车载显示屏
工业显示屏
```

---

# 2. OLED 基本结构

```text
OLED Panel
   │
   ├── 红色像素(R)
   ├── 绿色像素(G)
   └── 蓝色像素(B)
```

每个像素单独控制亮灭。

---

# 3. OLED 工作原理

```text
加电
  ↓
有机材料发光
  ↓
形成RGB颜色
  ↓
显示图像
```

与 LCD 不同：

```text
LCD 需要背光

OLED 自发光
```

---

# 4. OLED 显示流程

```text
Application
      │
      ▼
Frame Buffer
      │
      ▼
Display Controller
      │
      ▼
OLED Panel
```

控制器持续将图像数据刷新到 OLED 屏幕。

---

# 5. OLED 像素特点

### 显示白色

```text
R = ON
G = ON
B = ON
```

### 显示黑色

```text
R = OFF
G = OFF
B = OFF
```

因此：

```text
黑色区域几乎不耗电
```

---

# 6. 常见 OLED 接口

| 接口       | 应用场景      |
| -------- | --------- |
| I2C      | 小尺寸OLED模块 |
| SPI      | MCU显示模块   |
| MIPI DSI | 手机、平板     |
| eDP      | 高分辨率显示屏   |

---

# 7. OLED 常见参数

## 分辨率

```text
128×64
128×128
720P
1080P
2K
4K
```

### 刷新率

```text
60Hz
90Hz
120Hz
```

### 色深

```text
RGB565
RGB666
RGB888
```

---

# 8. OLED 优缺点

## 优点

```text
自发光

对比度高

响应速度快

视角大

屏幕更薄
```

## 缺点

```text
成本较高

寿命相对较短

长期显示可能烧屏
```

---

# 9. OLED 与 LCD 对比

| 项目   | OLED  | LCD  |
| ---- | ----- | ---- |
| 发光方式 | 自发光   | 背光   |
| 对比度  | 很高    | 一般   |
| 黑色显示 | 真黑    | 发灰   |
| 响应速度 | 快     | 较慢   |
| 厚度   | 薄     | 较厚   |
| 功耗   | 黑色功耗低 | 基本固定 |
| 成本   | 高     | 低    |

---

# 10. OLED 驱动层次

```text
Application
      │
      ▼
OLED Driver
      │
      ▼
Display Controller
      │
      ▼
OLED Panel
```

小尺寸 OLED 常见：

```text
MCU
 │
 ├── I2C
 └── SPI
      │
      ▼
OLED
```

---

# 11. 常见应用

| 场景   | 设备      |
| ---- | ------- |
| 手机   | AMOLED屏 |
| 智能手表 | OLED屏   |
| 电视   | OLED TV |
| 开发板  | OLED模块  |
| 工业设备 | 信息显示屏   |

---

# 12. 核心知识点

```text
OLED
 │
 ├── 自发光
 ├── RGB像素
 ├── 高对比度
 ├── 快速响应
 ├── 无背光
 ├── I2C/SPI
 ├── MIPI DSI
 └── Frame Buffer
```

---

# 13. 总结

OLED 是一种自发光显示技术，每个像素独立发光，无需背光。

核心显示链路：

```text
Application
     │
     ▼
Frame Buffer
     │
     ▼
Display Controller
     │
     ▼
OLED Panel
```

一句话总结：

> **OLED 是一种无需背光、像素自发光的显示技术，具有高对比度、响应速度快、视角大等优点，广泛应用于手机、手表和高端显示设备。**
