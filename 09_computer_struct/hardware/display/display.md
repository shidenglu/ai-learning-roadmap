# Display（显示子系统）简介

## 1. 什么是 Display

Display（显示）是指将 CPU、GPU 或 SoC 产生的图像数据显示到屏幕上的系统。

常见显示设备：

```text
LCD
OLED
AMOLED
HDMI 显示器
DP 显示器
TV
```

---

# 2. Display 系统结构

```text
Application
      │
      ▼
 Graphics/UI
      │
      ▼
Display Driver
      │
      ▼
Display Controller
      │
      ▼
Display Interface
      │
      ▼
Panel(Screen)
```

---

# 3. Display 数据流

显示本质上是把内存中的图像数据刷新到屏幕。

```text
Frame Buffer
      │
      ▼
Display Controller
      │
      ▼
LCD/OLED
```

例如：

```text
内存
 │
 ▼
RGB数据
 │
 ▼
屏幕显示图像
```

---

# 4. Display Controller（显示控制器）

显示控制器负责：

```text
读取Frame Buffer
生成时序信号
控制刷新率
输出显示数据
```

例如：

```text
DDR
 │
 ▼
Display Controller
 │
 ▼
LCD
```

---

# 5. Frame Buffer

Frame Buffer（帧缓冲区）用于保存当前显示画面。

例如：

```text
1920 × 1080
RGB888
```

占用内存：

```text
1920 × 1080 × 3

≈ 6MB
```

---

# 6. 常见显示接口

| 接口          | 用途        |
| ----------- | --------- |
| RGB         | MCU/LCD直连 |
| LVDS        | 工业显示器     |
| MIPI DSI    | 手机、平板     |
| HDMI        | 显示器、电视    |
| DisplayPort | PC显示器     |
| eDP         | 笔记本屏幕     |

---

# 7. 刷新率（Refresh Rate）

表示屏幕每秒刷新次数。

常见：

```text
60Hz
90Hz
120Hz
144Hz
```

例如：

```text
60Hz
```

表示：

```text
每秒刷新60次画面
```

---

# 8. 分辨率（Resolution）

表示屏幕像素数量。

常见：

| 分辨率       | 像素    |
| --------- | ----- |
| 800×480   | WVGA  |
| 1280×720  | 720P  |
| 1920×1080 | 1080P |
| 2560×1440 | 2K    |
| 3840×2160 | 4K    |

---

# 9. 显示驱动主要功能

```text
初始化屏幕

配置时钟

配置分辨率

配置刷新率

管理Frame Buffer

控制背光
```

---

# 10. Display 驱动层次

```text
Application
      │
      ▼
GUI Framework
      │
      ▼
Display Driver
      │
      ▼
Display Controller
      │
      ▼
LCD / OLED Panel
```

---

# 11. 常见应用场景

| 场景    | 显示设备     |
| ----- | -------- |
| 手机    | OLED     |
| 平板    | LCD/OLED |
| 开发板   | LCD      |
| 工控机   | LCD      |
| PC显示器 | HDMI/DP  |
| 电视    | HDMI     |

---

# 12. 核心知识点

```text
Display
   │
   ├── Resolution
   ├── Refresh Rate
   ├── Frame Buffer
   ├── Display Controller
   ├── LCD/OLED
   ├── HDMI
   ├── MIPI DSI
   └── LVDS
```

---

# 13. 总结

Display 子系统负责将内存中的图像数据显示到屏幕。

核心数据路径：

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
Display Interface
     │
     ▼
LCD / OLED
```

一句话总结：

> **Display 是连接软件图形界面与物理屏幕的桥梁，其核心任务是将 Frame Buffer 中的图像数据按照指定时序持续刷新到显示设备上。**
