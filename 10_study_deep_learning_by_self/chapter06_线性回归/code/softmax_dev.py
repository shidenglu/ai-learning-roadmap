import torch
from torch import nn
from d2l import torch as d2l

batch_size = 256
train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)

# 网络
net = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 10)
)

# 初始化权重
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.normal_(m.weight, std=0.01)

net.apply(init_weights)

# 损失函数
loss = nn.CrossEntropyLoss()

# 优化器
trainer = torch.optim.SGD(net.parameters(), lr=0.1)

# 训练轮数
num_epochs = 10

# 训练
for epoch in range(num_epochs):

    net.train()

    train_loss = 0
    train_acc = 0
    train_num = 0

    for X, y in train_iter:

        # 前向传播
        y_hat = net(X)

        # 计算损失
        l = loss(y_hat, y)

        # 梯度清零
        trainer.zero_grad()

        # 反向传播
        l.backward()

        # 更新参数
        trainer.step()

        train_loss += l.item() * y.shape[0]

        train_acc += (y_hat.argmax(dim=1) == y).sum().item()

        train_num += y.shape[0]

    train_loss /= train_num
    train_acc /= train_num

    # 测试集评估
    net.eval()

    test_acc = 0
    test_num = 0

    with torch.no_grad():

        for X, y in test_iter:

            y_hat = net(X)

            test_acc += (y_hat.argmax(dim=1) == y).sum().item()

            test_num += y.shape[0]

    test_acc /= test_num

    print(
        f"epoch {epoch+1:2d} | "
        f"train_loss={train_loss:.4f} | "
        f"train_acc={train_acc:.4f} | "
        f"test_acc={test_acc:.4f}"
    )