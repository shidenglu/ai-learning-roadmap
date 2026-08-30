# Matplotlib 常用 API 速查表

> 本文整理 Matplotlib 在机器学习、深度学习、PyTorch、D2L 学习过程中最常用的 API。
>
> 重点包含：**方法、功能描述、常用入参个数、入参及含义**。

| 方法 | 功能描述 | 常用入参个数 | 入参及含义 |
|---|---|---:|---|
| `plt.figure()` | 创建一个新的 Figure 画布 | 5 | `num`：画布编号/名称；`figsize`：画布大小 `(宽, 高)`；`dpi`：分辨率；`facecolor`：背景色；`edgecolor`：边框颜色 |
| `plt.subplots()` | 创建 Figure 和一个或多个 Axes 子图 | 7 | `nrows`：行数；`ncols`：列数；`figsize`：画布大小；`dpi`：分辨率；`sharex`：是否共享 X 轴；`sharey`：是否共享 Y 轴；`squeeze`：是否压缩 Axes 数组维度 |
| `plt.plot()` | 绘制折线图、曲线图 | 10 | `x`：X 轴数据；`y`：Y 轴数据；`fmt`：线型简写；`color`：颜色；`linewidth`：线宽；`linestyle`：线型；`marker`：数据点样式；`markersize`：数据点大小；`label`：图例名称；`alpha`：透明度 |
| `plt.scatter()` | 绘制散点图 | 8 | `x`：X 坐标；`y`：Y 坐标；`s`：点大小；`c`：点颜色；`marker`：点形状；`alpha`：透明度；`label`：图例名称；`edgecolors`：边缘颜色 |
| `plt.bar()` | 绘制垂直柱状图 | 8 | `x`：柱子位置/类别；`height`：柱子高度；`width`：柱子宽度；`bottom`：柱子起始高度；`align`：对齐方式；`color`：颜色；`alpha`：透明度；`label`：图例名称 |
| `plt.barh()` | 绘制水平柱状图 | 7 | `y`：Y 轴位置/类别；`width`：柱子宽度；`height`：柱子高度；`left`：X 方向起始位置；`align`：对齐方式；`color`：颜色；`label`：图例名称 |
| `plt.hist()` | 绘制直方图，观察数据分布 | 7 | `x`：输入数据；`bins`：分组数量；`range`：数据范围；`density`：是否归一化；`cumulative`：是否绘制累积分布；`alpha`：透明度；`label`：图例名称 |
| `plt.imshow()` | 显示图片或二维矩阵 | 6 | `X`：图片/二维矩阵；`cmap`：颜色映射；`vmin`：颜色映射最小值；`vmax`：颜色映射最大值；`aspect`：宽高比例；`interpolation`：插值方式 |
| `plt.colorbar()` | 添加颜色条，表示颜色与数值之间的对应关系 | 5 | `mappable`：对应的图像对象；`ax`：所属 Axes；`orientation`：方向；`fraction`：颜色条尺寸比例；`pad`：与主图距离 |
| `plt.title()` | 设置当前图像标题 | 4 | `label`：标题文字；`fontsize`：字体大小；`loc`：标题位置；`pad`：标题与图像距离 |
| `plt.xlabel()` | 设置 X 轴名称 | 3 | `xlabel`：X 轴文字；`fontsize`：字体大小；`labelpad`：文字与坐标轴距离 |
| `plt.ylabel()` | 设置 Y 轴名称 | 3 | `ylabel`：Y 轴文字；`fontsize`：字体大小；`labelpad`：文字与坐标轴距离 |
| `plt.xlim()` | 设置 X 轴显示范围 | 2 | `left`：X 轴最小值；`right`：X 轴最大值 |
| `plt.ylim()` | 设置 Y 轴显示范围 | 2 | `bottom`：Y 轴最小值；`top`：Y 轴最大值 |
| `plt.xticks()` | 设置 X 轴刻度位置和标签 | 3 | `ticks`：刻度位置；`labels`：刻度文字；`rotation`：文字旋转角度 |
| `plt.yticks()` | 设置 Y 轴刻度位置和标签 | 3 | `ticks`：刻度位置；`labels`：刻度文字；`rotation`：文字旋转角度 |
| `plt.legend()` | 显示图例 | 4 | `loc`：图例位置；`fontsize`：字体大小；`title`：图例标题；`frameon`：是否显示边框 |
| `plt.grid()` | 显示或设置坐标网格 | 5 | `visible`：是否显示；`axis`：作用于 X/Y/both；`which`：主/次刻度；`linestyle`：线型；`alpha`：透明度 |
| `plt.savefig()` | 将当前图像保存到文件 | 7 | `fname`：文件名/路径；`dpi`：分辨率；`format`：文件格式；`bbox_inches`：边界处理；`transparent`：是否透明背景；`facecolor`：背景色；`pad_inches`：边距 |
| `plt.show()` | 显示图像 | 1 | `block`：是否阻塞程序执行 |
| `plt.clf()` | 清空当前 Figure | 0 | 无参数；清空当前画布中的所有绘图内容 |
| `plt.close()` | 关闭 Figure 或图像窗口 | 1 | `fig`：要关闭的 Figure；可以是对象、编号、名称或 `"all"` |
| `plt.ion()` | 开启交互式绘图模式 | 0 | 无参数 |
| `plt.ioff()` | 关闭交互式绘图模式 | 0 | 无参数 |
| `plt.pause()` | 暂停程序并刷新图像，常用于动态绘图 | 1 | `interval`：暂停时间，单位为秒 |
| `plt.tight_layout()` | 自动调整子图布局，避免标题、坐标轴等重叠 | 3 | `pad`：边缘间距；`w_pad`：子图水平间距；`h_pad`：子图垂直间距 |
| `ax.plot()` | 在指定 Axes 中绘制折线图 | 10 | `x`：X 数据；`y`：Y 数据；`fmt`：线型简写；`color`：颜色；`linewidth`：线宽；`linestyle`：线型；`marker`：数据点；`markersize`：点大小；`label`：图例；`alpha`：透明度 |
| `ax.scatter()` | 在指定 Axes 中绘制散点图 | 8 | `x`：X 坐标；`y`：Y 坐标；`s`：点大小；`c`：颜色；`marker`：点形状；`alpha`：透明度；`label`：图例；`edgecolors`：边缘颜色 |
| `ax.imshow()` | 在指定 Axes 中显示图片或二维矩阵 | 6 | `X`：图片/矩阵；`cmap`：颜色映射；`vmin`：最小值；`vmax`：最大值；`aspect`：宽高比例；`interpolation`：插值方式 |
| `ax.set_title()` | 设置指定 Axes 的标题 | 4 | `label`：标题；`fontsize`：字体大小；`loc`：位置；`pad`：间距 |
| `ax.set_xlabel()` | 设置指定 Axes 的 X 轴名称 | 3 | `xlabel`：X 轴文字；`fontsize`：字体大小；`labelpad`：间距 |
| `ax.set_ylabel()` | 设置指定 Axes 的 Y 轴名称 | 3 | `ylabel`：Y 轴文字；`fontsize`：字体大小；`labelpad`：间距 |
| `ax.set_xlim()` | 设置指定 Axes 的 X 轴范围 | 2 | `left`：最小值；`right`：最大值 |
| `ax.set_ylim()` | 设置指定 Axes 的 Y 轴范围 | 2 | `bottom`：最小值；`top`：最大值 |
| `ax.legend()` | 显示指定 Axes 的图例 | 4 | `loc`：图例位置；`fontsize`：字体大小；`title`：图例标题；`frameon`：是否显示边框 |
| `ax.grid()` | 设置指定 Axes 的网格 | 5 | `visible`：是否显示；`axis`：X/Y/both；`which`：主/次刻度；`linestyle`：线型；`alpha`：透明度 |

---

# Matplotlib 深度学习高频 API 分类

| 功能模块 | 核心 API | 深度学习用途 |
|---|---|---|
| 创建画布 | `figure()` | 创建绘图窗口 |
| 创建子图 | `subplots()` | 同时显示 Loss、Accuracy 等 |
| 折线图 | `plot()` | Loss、Accuracy、Learning Rate |
| 散点图 | `scatter()` | 数据集、特征、Embedding 分布 |
| 柱状图 | `bar()` | 模型性能、类别数量对比 |
| 直方图 | `hist()` | 数据、权重、梯度、激活值分布 |
| 图像显示 | `imshow()` | MNIST、CNN Feature Map |
| 热力图 | `imshow()` | Attention、矩阵、特征图 |
| 颜色条 | `colorbar()` | 显示热力图数值范围 |
| 图例 | `legend()` | 区分 Train / Validation |
| 标题 | `title()` | 说明图像内容 |
| X 轴 | `xlabel()` | Epoch、Feature 等 |
| Y 轴 | `ylabel()` | Loss、Accuracy 等 |
| 坐标范围 | `xlim()` / `ylim()` | 控制显示区域 |
| 坐标刻度 | `xticks()` / `yticks()` | 控制坐标刻度 |
| 网格 | `grid()` | 辅助观察数据 |
| 保存 | `savefig()` | 保存训练结果 |
| 显示 | `show()` | 显示图像 |
| 清空 | `clf()` | 动态绘图时清除旧图 |
| 关闭 | `close()` | 关闭图像窗口 |
| 交互模式 | `ion()` | 开启动态绘图 |
| 动态刷新 | `pause()` | 实时刷新训练曲线 |
| 关闭交互 | `ioff()` | 关闭动态绘图 |
| 自动布局 | `tight_layout()` | 防止多个子图重叠 |

---

# 深度学习最需要掌握的 API

如果目标是学习 PyTorch、CNN、Transformer、D2L，而不是成为专业的数据可视化工程师，那么优先掌握下面这些：

```text
第一优先级：

plot()
imshow()
subplots()
scatter()
hist()

第二优先级：

legend()
title()
xlabel()
ylabel()
grid()
colorbar()

第三优先级：

xlim()
ylim()
xticks()
yticks()
savefig()
tight_layout()

动态绘图：

ion()
pause()
ioff()
clf()
close()