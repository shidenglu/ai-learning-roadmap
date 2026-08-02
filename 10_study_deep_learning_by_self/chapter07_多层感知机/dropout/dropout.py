import torch
from torch import nn
from d2l import torch as d2l

# ==========================
# 网络参数
# ==========================
num_inputs = 784
num_outputs = 10

num_hiddens1 = 256
num_hiddens2 = 256

dropout1 = 0.2
dropout2 = 0.5

# ==========================
# 定义MLP
# ==========================
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(
                num_inputs,
                num_hiddens1
            ),

            nn.ReLU(),
            nn.Dropout(dropout1),
            nn.Linear(
                num_hiddens1,
                num_hiddens2
            ),

            nn.ReLU(),
            nn.Dropout(dropout2),
            nn.Linear(
                num_hiddens2,
                num_outputs
            )
        )

    def forward(self, X):
        return self.net(X)

# 创建模型
net = Net()

# ==========================
# 计算准确率
# ==========================
def accuracy(y_hat, y):
    if len(y_hat.shape) > 1:
        y_hat = y_hat.argmax(dim=1)
    return float(
        (y_hat == y).sum()
    )

# ==========================
# 测试集准确率
# ==========================
def evaluate_accuracy(net, data_iter):
    net.eval()
    metric_correct = 0
    metric_total = 0

    with torch.no_grad():
        for X, y in data_iter:
            y_hat = net(X)
            metric_correct += accuracy(
                y_hat,
                y
            )
            metric_total += y.numel()

    return metric_correct / metric_total


# ==========================
# 单轮训练
# ==========================

def train_epoch(net,
                train_iter,
                loss,
                optimizer):
    net.train()
    total_loss = 0
    total_correct = 0
    total_num = 0

    for X, y in train_iter:
        y_hat = net(X)
        l = loss(
            y_hat,
            y
        )

        optimizer.zero_grad()
        l.mean().backward()
        optimizer.step()
        total_loss += l.sum().item()
        total_correct += accuracy(
            y_hat,
            y
        )
        total_num += y.numel()

    train_loss = total_loss / total_num
    train_acc = total_correct / total_num

    return train_loss, train_acc

# ==========================
# 损失函数
# ==========================
loss = nn.CrossEntropyLoss(
    reduction='none'
)

# ==========================
# 优化器
# ==========================
lr = 0.5
optimizer = torch.optim.SGD(
    net.parameters(),
    lr=lr
)

# ==========================
# 训练
# ==========================
batch_size = 256
num_epochs = 10
def main():
    # 数据集
    train_iter, test_iter = d2l.load_data_fashion_mnist(
        batch_size
    )

    loss = nn.CrossEntropyLoss(
        reduction='none'
    )

    optimizer = torch.optim.SGD(
        net.parameters(),
        lr=0.5
    )

    for epoch in range(num_epochs):
        train_loss, train_acc = train_epoch(
            net,
            train_iter,
            loss,
            optimizer
        )

        test_acc = evaluate_accuracy(
            net,
            test_iter
        )

        print(
            f"epoch {epoch+1}, "
            f"loss={train_loss:.4f}, "
            f"train_acc={train_acc:.4f}, "
            f"test_acc={test_acc:.4f}"
        )

if __name__ == '__main__':
    main()