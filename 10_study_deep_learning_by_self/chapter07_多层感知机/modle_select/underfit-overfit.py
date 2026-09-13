import math
import numpy as np
import torch
from torch import nn
from d2l import torch as d2l

# 定义真实的函数
max_degree = 20  # 多项式的最大阶数
true_w = np.zeros(max_degree)  # 分配大量的空间
# [5, 1.2, -3.4, 5.6, 0, 0, 0, ... ,0]
# y=5+1.2x−3.4x2+5.6x3
true_w[0:4] = np.array([5, 1.2, -3.4, 5.6])

n_train, n_test = 100, 100  # 训练和测试数据集大小

# 生成输入特征
# 200*1 200 个样本 每个一个特征
features = np.random.normal(size=(n_train + n_test, 1))
# 打乱顺序
np.random.shuffle(features)
# 生成多项式
# 维度 200*20
poly_features = np.power(features, np.arange(max_degree).reshape(1, -1))
# 除阶乘
for i in range(max_degree):
    poly_features[:, i] /= math.gamma(i + 1)  # gamma(n)=(n-1)!
# labels的维度:(n_train+n_test,)
# 计算标签
# 实际上是计算 y=w0​+w1​x+w2​2!x2​+w3​3!x3​
labels = np.dot(poly_features, true_w)
# 加入噪声
labels += np.random.normal(scale=0.1, size=labels.shape)

# NumPy ndarray转换为tensor
true_w, features, poly_features, labels = [torch.tensor(x, dtype=
    torch.float32) for x in [true_w, features, poly_features, labels]]

# features 样本 输入 x
# poly_features 查看前两个样本的20阶特征 y=1​+​x+​2!x2​+​3!x3​ 中 每个元素的值 一组 20 个
# labels 和 前置参数相乘后的结果 标签
features[:2], poly_features[:2, :], labels[:2]

# 计算整个数据集的损失
def evaluate_loss(net, data_iter, loss):  #@save
    """评估给定数据集上模型的损失"""
    metric = d2l.Accumulator(2)  # 损失的总和,样本数量
    for X, y in data_iter:
        out = net(X)
        y = y.reshape(out.shape)
        l = loss(out, y)
        metric.add(l.sum(), l.numel())
    return metric[0] / metric[1]

# 训练一个 epoch
def train_epoch(net, train_iter, loss, trainer):
    # 切换到训练模式
    net.train()
    total_loss = 0
    total_num = 0

    for X, y in train_iter:
        trainer.zero_grad()
        y_hat = net(X)
        l = loss(y_hat, y)
        l.mean().backward()
        trainer.step()
        total_loss += l.sum().item()
        total_num += y.numel()
    return total_loss / total_num

def train(train_features, test_features, train_labels, test_labels,
          num_epochs=400):
    # 损失函数 均方误差
    loss = nn.MSELoss(reduction='none')
    # 输入维度 n 阶模型就是100*n
    input_shape = train_features.shape[-1]
    # 不设置偏置，因为我们已经在多项式中实现了它
    # 创建模型
    net = nn.Sequential(nn.Linear(input_shape, 1, bias=False))
    # 每次训练多少
    batch_size = min(10, train_labels.shape[0])
    # train_features 维度 100*n
    # train_labels.reshape(-1,1) 维度 100 * 1
    train_iter = d2l.load_array((train_features, train_labels.reshape(-1,1)),
                                batch_size)
    test_iter = d2l.load_array((test_features, test_labels.reshape(-1,1)),
                               batch_size, is_train=False)
    # 优化器
    trainer = torch.optim.SGD(net.parameters(), lr=0.01)
    # animator = d2l.Animator(xlabel='epoch', ylabel='loss', yscale='log',
    #                         xlim=[1, num_epochs], ylim=[1e-3, 1e2],
    #                         legend=['train', 'test'])
    for epoch in range(num_epochs):
        train_epoch(net, train_iter, loss, trainer)
        # if epoch == 0 or (epoch + 1) % 20 == 0:
        #     animator.add(epoch + 1, (evaluate_loss(net, train_iter, loss),
        #                              evaluate_loss(net, test_iter, loss)))
    print('weight:', net[0].weight.data.numpy())

# 从多项式特征中选择前4个维度，即1,x,x^2/2!,x^3/3!
train(poly_features[:n_train, :4], poly_features[n_train:, :4],
      labels[:n_train], labels[n_train:])

# 从多项式特征中选择前2个维度，即1和x
train(poly_features[:n_train, :2], poly_features[n_train:, :2],
      labels[:n_train], labels[n_train:])

# 从多项式特征中选取所有维度
train(poly_features[:n_train, :], poly_features[n_train:, :],
      labels[:n_train], labels[n_train:], num_epochs=1500)