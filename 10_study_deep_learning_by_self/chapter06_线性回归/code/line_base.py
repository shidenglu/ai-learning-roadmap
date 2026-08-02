# matplotlib inline
import random
import torch
from d2l import torch as d2l

# 生成真实的数据集
# y 是真实的标签，X是特征，w是权重，b是偏差，噪声服从均值为0、标准差为0.01的正态分布
def synthetic_data(w, b, num_examples):  #@save
    """生成y=Xw+b+噪声"""
    X = torch.normal(0, 1, (num_examples, len(w))) # 生成符合标准正态分布（均值为 0，方差为 1）的随机数。
    y = torch.matmul(X, w) + b # 生成的矩阵形状（Shape）是 (num_examples, len(w))
    y += torch.normal(0, 0.01, y.shape) # 生成符合均值为 0，标准差为 0.01 的正态分布的随机数，并将其加到 y 上
    return X, y.reshape((-1, 1)) # 将特征矩阵 X 和标签列向量 y 作为结果返回。

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 1000)

print('features:', features[0],'\nlabel:', labels[0])

d2l.set_figsize()
d2l.plt.scatter(features[:, (1)].detach().numpy(), labels.detach().numpy(), 1);
d2l.plt.show()

# 读取数据集
# 
def data_iter(batch_size, features, labels):
    num_examples = len(features) # 计算数据集里一共有多少条数据（样本总数）
    indices = list(range(num_examples)) # 生成一个从 $0$ 到 num_examples - 1 的连续整数列表，作为数据的下标（索引）。比如有 5 个样本，indices 就是 [0, 1, 2, 3, 4]。
    # 这些样本是随机读取的，没有特定的顺序
    random.shuffle(indices) # random.shuffle(indices)：把刚才生成的索引列表原地随机打乱。比如原本是 [0, 1, 2, 3, 4]，打乱后可能变成 [3, 0, 4, 1, 2]
    for i in range(0, num_examples, batch_size): # 假设共有 1000 个样本，batch_size 是 10。那么 i 的取值依次是：0, 10, 20, 30, ...，每次直接跳过一个批次的大小。
        batch_indices = torch.tensor(
            indices[i: min(i + batch_size, num_examples)])
        yield features[batch_indices], labels[batch_indices] # 每次选 batch_size 个样本，返回它们的特征和标签

batch_size = 10

for X, y in data_iter(batch_size, features, labels):
    print(X, '\n', y)
    break

# 初始化模型参数 requires_grad=True 需求求导更新
w = torch.normal(0, 0.01, size=(2,1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# 定义模型
def linreg(X, w, b):  #@save
    """线性回归模型"""
    return torch.matmul(X, w) + b

# 定义损失函数
def squared_loss(y_hat, y):  #@save
    """均方损失"""
    return (y_hat - y.reshape(y_hat.shape)) ** 2 / 2

# 定义优化算法
def sgd(params, lr, batch_size):  #@save
    """小批量随机梯度下降"""
    with torch.no_grad():
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_()

# 学习率
lr = 0.03

# 模型参数
num_epochs = 3
net = linreg
loss = squared_loss

# 循环3次，使用小批量随机梯度下降来优化模型参数
for epoch in range(num_epochs):
    for X, y in data_iter(batch_size, features, labels):
        l = loss(net(X, w, b), y)  # X和y的小批量损失
        # 因为l形状是(batch_size,1)，而不是一个标量。l中的所有元素被加到一起，
        # 并以此计算关于[w,b]的梯度
        l.sum().backward()
        # l.sum()：把这批样本的所有损失加起来，变成一个标量（单个数字）。
        # 因为 PyTorch 的自动求导机制 .backward() 默认只能对标量进行。
        # .backward()：反向传播（Backward Propagation）。PyTorch 开始大显身手，
        # 自动计算出总损失关于参数 $w$ 和 $b$ 的梯度（偏导数）。这个梯度代表了参数调整的方向，
        # 会被偷偷存放在 w.grad 和 b.grad 中。
        sgd([w, b], lr, batch_size)  # 使用参数的梯度更新参数
    with torch.no_grad():
        train_l = loss(net(features, w, b), labels)
        print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')

print(f'w的估计误差: {true_w - w.reshape(true_w.shape)}')
print(f'b的估计误差: {true_b - b}')