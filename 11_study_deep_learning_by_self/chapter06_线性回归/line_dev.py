import numpy as np
import torch
from torch.utils import data
from d2l import torch as d2l

# 定义真实的权重和偏置
true_w = torch.tensor([2, -3.4])
true_b = 4.2
# 输入参数：传入了刚才定义的真实权重 true_w、真实偏置 true_b，以及希望生成的样本数量 1000。
# 底层逻辑：这个函数在幕后做两件事：随机生成一个形状为 (1000, 2) 的特征矩阵 features（服从正态分布）。
# 根据公式 $y = X \mathbf{w} + b$ 计算出对应的标签，并在标签中加入了一点点随机噪声（模拟现实世界中数据的误差），最终得到 labels。
# 输出结果：features: 形状为 (1000, 2) 的张量，代表 1000 个样本，每个样本有 2 个特征。labels: 形状为 (1000, 1) 的张量，代表这 1000 个样本对应的真实标签（目标值）。
features, labels = d2l.synthetic_data(true_w, true_b, 1000)

# data_arrays: 接收一个元组，通常包含特征和标签，即 (features, labels)。
# batch_size: 每个小批次包含的样本数量。
# is_train=True: 一个布尔值。如果是训练阶段（True），我们希望打乱数据的顺序（Shuffle），以保证模型训练的随机性，防止模型产生依赖读取顺序的偏见。
#@save: 这是《动手学深度学习》书中的特殊标记，意思是这个函数被保存在 d2l 模块中，以后可以直接通过 d2l.load_array 调用。
def load_array(data_arrays, batch_size, is_train=True):  #@save
    """构造一个PyTorch数据迭代器"""
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)

batch_size = 10
data_iter = load_array((features, labels), batch_size)

next(iter(data_iter))

# nn是神经网络的缩写
from torch import nn

# 搭建神经网络模型
# nn: PyTorch 的神经网络（Neural Network）模块，里面包含了构建模型所需的所有“积木”。
# nn.Sequential: 像一个传送带（容器）。你把网络层按顺序放进去，数据就会按照这个顺序一层层传过去。
# nn.Linear(2, 1): 定义了一个全连接层（线性层）。
# 输入维度是 2：因为我们前面的特征 features 每个样本有 2 个特征。
# 输出维度是 1：因为我们预测的标签 labels 只有一个值（房价、考试分数等）。它内部自动创建了两个变量：权重 $w$（形状是 1行2列）和偏置 $b$（标量）。
net = nn.Sequential(nn.Linear(2, 1))

# 初始化网络参数（赋初值）
# net[0]: 因为模型是用 Sequential 包裹的，net[0] 表示取出传送带上的第一层（也就是那个 nn.Linear(2, 1)）。
# .weight.data.normal_(0, 0.01): 将权重 $w$ 的值，使用正态分布（高斯分布）进行覆盖。均值为 0，标准差为 0.01。
# .bias.data.fill_(0): 将偏置 $b$ 的值全部清零（填入 0）。
net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)

# 定义损失函数
# nn.MSELoss(): 均方误差损失函数（Mean Squared Error Loss）。它会计算预测值和真实值之间的差异，并将差异平方后取平均，作为模型的损失。
loss = nn.MSELoss()

# 定义优化算法
# torch.optim.SGD: 随机梯度下降优化器（Stochastic Gradient Descent）。它会根据计算出的梯度，调整模型的参数（权重和偏置），以最小化损失函数。
# net.parameters(): 获取模型中所有需要优化的参数（权重和偏置）。
trainer = torch.optim.SGD(net.parameters(), lr=0.03)

# 训练模型
num_epochs = 3
for epoch in range(num_epochs):
    for X, y in data_iter:
        # 计算损失
        l = loss(net(X) ,y)
        # 反向传播和优化
        trainer.zero_grad()
        l.backward()
        # 更新参数
        trainer.step()
    # 计算训练误差
    l = loss(net(features), labels)
    print(f'epoch {epoch + 1}, loss {l:f}')

w = net[0].weight.data
print('w的估计误差：', true_w - w.reshape(true_w.shape))
b = net[0].bias.data
print('b的估计误差：', true_b - b)