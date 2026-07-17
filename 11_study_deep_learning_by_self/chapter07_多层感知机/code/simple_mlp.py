import torch
from torch import nn
from d2l import torch as d2l

# ==========================
# 加载数据
# ==========================
batch_size = 256

train_iter, test_iter = d2l.load_data_fashion_mnist(
    batch_size
)

# ==========================
# 网络参数
# ==========================
num_inputs = 784
num_hiddens = 256
num_outputs = 10

# 第一层
W1 = nn.Parameter(
    torch.randn(num_inputs, num_hiddens) * 0.01
)

b1 = nn.Parameter(
    torch.zeros(num_hiddens)
)

# 第二层
W2 = nn.Parameter(
    torch.randn(num_hiddens, num_outputs) * 0.01
)

b2 = nn.Parameter(
    torch.zeros(num_outputs)
)

params = [W1, b1, W2, b2]

# ==========================
# ReLU
# ==========================
def relu(X):
    return torch.maximum(
        X,
        torch.zeros_like(X)
    )

# ==========================
# 前向传播
# ==========================
def net(X):

    # [256,1,28,28]
    X = X.reshape((-1, num_inputs))

    # [256,784]
    #      @
    # [784,256]
    #
    # =>
    # [256,256]
    H = relu(X @ W1 + b1)

    # [256,256]
    #      @
    # [256,10]
    #
    # =>
    # [256,10]
    return H @ W2 + b2

# ==========================
# 损失函数
# ==========================
loss = nn.CrossEntropyLoss()

# ==========================
# 优化器
# ==========================
lr = 0.1

updater = torch.optim.SGD(
    params,
    lr=lr
)

# ==========================
# 训练
# ==========================
def main():
    num_epochs = 10
    for epoch in range(num_epochs):
        train_loss = 0
        train_acc = 0
        train_num = 0

        for X, y in train_iter:

            y_hat = net(X)
            l = loss(y_hat, y)
            updater.zero_grad()
            l.backward()
            updater.step()
            train_loss += l.item() * y.shape[0]
            train_acc += (
                y_hat.argmax(dim=1) == y
            ).sum().item()
            train_num += y.shape[0]

        train_loss /= train_num
        train_acc /= train_num
        # ======================
        # 测试集
        # ======================
        test_acc = 0
        test_num = 0
        with torch.no_grad():
            for X, y in test_iter:
                y_hat = net(X)
                test_acc += (
                    y_hat.argmax(dim=1) == y
                ).sum().item()
                test_num += y.shape[0]

        test_acc /= test_num
        print(
            f"epoch={epoch+1:2d} "
            f"loss={train_loss:.4f} "
            f"train_acc={train_acc:.4f} "
            f"test_acc={test_acc:.4f}"
        )

if __name__ == "__main__":
    main()