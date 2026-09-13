# LCD（Liquid Crystal Display）液晶显示器

## 1. 什么是 LCD

LCD（Liquid Crystal Display）即：

```text
液晶显示器
```

利用液晶分子控制光线透过率来显示图像。

常见于：

```text
手机
平板
显示器
电视
车载屏
工业控制屏
```

---

# 2. LCD 基本结构

```text
背光源
   │
   ▼
偏光片
   │
   ▼
液晶层
   │
   ▼
彩色滤光片(RGB)
   │
   ▼
偏光片
   │
   ▼
用户眼睛
```

LCD 本身不发光，需要背光源。

---

# 3. LCD 工作原理

液晶分子在电场作用下改变排列方向：

```text
加电
  ↓
液晶旋转
  ↓
改变光线通过量
  ↓
形成图像
```

通过控制每个像素亮度实现显示。

---

# 4. LCD 像素结构

一个像素通常由：

```text
R
G
B
```

三个子像素组成。

```text
┌─────┬─────┬─────┐
│  R  │  G  │  B  │
└─────┴─────┴─────┘
```

不同亮度组合形成各种颜色。

---

# 5. LCD 显示流程

```text
Application
      │
      ▼
Frame Buffer
      │
      ▼
LCD Controller
      │
      ▼
LCD Panel
```

显示控制器不断读取 Frame Buffer 并刷新屏幕。

---

# 6. 常见 LCD 接口

| 接口       | 应用场景   |
| -------- | ------ |
| MCU 8080 | 小尺寸屏   |
| RGB      | 开发板LCD |
| LVDS     | 工控屏    |
| MIPI DSI | 手机/平板  |
| HDMI     | 显示器/电视 |

---

# 7. LCD 常见参数

## 分辨率

```text
800×480
1280×720
1920×1080
3840×2160
```

---

## 刷新率

```text
60Hz
90Hz
120Hz
```

表示：

```text
每秒刷新次数
```

---

## 色深

| 格式     | 位数    |
| ------ | ----- |
| RGB565 | 16bit |
| RGB666 | 18bit |
| RGB888 | 24bit |

---

# 8. Frame Buffer

Frame Buffer 用于存放当前画面。

例如：

```text
1920×1080
RGB888
```

占用：

```text
1920 × 1080 × 3

≈ 6MB
```

---

# 9. LCD 驱动主要功能

```text
初始化LCD

配置时钟

配置分辨率

配置刷新率

刷新Frame Buffer

控制背光
```

---

# 10. LCD 与 OLED 对比

| 项目   | LCD | OLED  |
| ---- | --- | ----- |
| 发光方式 | 背光  | 自发光   |
| 厚度   | 较厚  | 较薄    |
| 对比度  | 一般  | 很高    |
| 功耗   | 较高  | 黑色功耗低 |
| 成本   | 较低  | 较高    |
| 烧屏   | 不易  | 可能存在  |

---

# 11. LCD 驱动层次

```text
Application
      │
      ▼
GUI
      │
      ▼
LCD Driver
      │
      ▼
LCD Controller
      │
      ▼
LCD Panel
```

---

# 12. 核心知识点

```text
LCD
 │
 ├── Backlight
 ├── Liquid Crystal
 ├── Pixel(RGB)
 ├── Resolution
 ├── Refresh Rate
 ├── Frame Buffer
 ├── RGB565/RGB888
 ├── LCD Controller
 └── MIPI/LVDS/RGB
```

---

# 13. 总结

LCD 是目前最常见的显示技术之一，通过液晶控制背光透过率形成图像。

核心显示链路：

```text
Application
     │
     ▼
Frame Buffer
     │
     ▼
LCD Controller
     │
     ▼
LCD Panel
     │
     ▼
Image
```

一句话总结：

> **LCD 是一种依靠液晶调节背光透过率进行显示的屏幕技术，其核心由背光、液晶层、像素阵列和显示控制器组成。**
