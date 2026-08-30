import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt
# =========================
# 1. CNN 网络
# =========================
net = nn.Sequential(
    nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=2, stride=2),
    nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=2, stride=2),
    nn.Flatten(),
    nn.Linear(32 * 7 * 7, 10)
)
# =========================
# 2. 查看网络输出尺寸
# =========================
X = torch.randn(1, 1, 28, 28)
print("=" * 50)
print("CNN Network")
print("=" * 50)
for layer in net:
    X = layer(X)
    print(
        f"{layer.__class__.__name__:15s}",
        X.shape
    )
# =========================
# 3. 加载数据
# =========================
batch_size = 256
train_iter, test_iter = d2l.load_data_fashion_mnist(
    batch_size=batch_size
)
# =========================
# 4. 计算准确率
# =========================
def evaluate_accuracy(net, data_iter, device):
    net.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in data_iter:
            X = X.to(device)
            y = y.to(device)
            y_hat = net(X)
            pred = y_hat.argmax(dim=1)
            correct += (pred == y).sum().item()
            total += y.numel()
    return correct / total
# =========================
# 5. 训练
# =========================
def train(net, train_iter, test_iter, num_epochs, lr, device):
    net.to(device)
    loss = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        net.parameters(),
        lr=lr
    )

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    for epoch in range(num_epochs):
        net.train()
        total_loss = 0
        total_correct = 0
        total_num = 0

        for X, y in train_iter:
            X = X.to(device)
            y = y.to(device)
            optimizer.zero_grad()
            y_hat = net(X)
            l = loss(y_hat, y)
            l.backward()
            optimizer.step()
            total_loss += l.item() * X.shape[0]
            total_correct += (
                y_hat.argmax(dim=1) == y
            ).sum().item()
            total_num += X.shape[0]

        train_loss = total_loss / total_num
        train_acc = total_correct / total_num

        test_acc = evaluate_accuracy(
            net,
            test_iter,
            device
        )

        train_loss_list.append(train_loss)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)

        print(
            f"Epoch [{epoch + 1}/{num_epochs}] "
            f"Loss={train_loss:.4f} "
            f"TrainAcc={train_acc:.4f} "
            f"TestAcc={test_acc:.4f}"
        )

    # =========================
    # 6. 绘制训练曲线
    # =========================
    epochs = range(1, num_epochs + 1)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(
        epochs,
        train_loss_list
    )
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Loss")
    plt.grid(True)
    plt.subplot(1, 2, 2)
    plt.plot(
        epochs,
        train_acc_list,
        label="Train Acc"
    )
    plt.plot(
        epochs,
        test_acc_list,
        label="Test Acc"
    )
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# =========================
# 7. Main
# =========================
if __name__ == "__main__":
    lr = 0.1
    num_epochs = 10
    device = d2l.try_gpu()
    print("Training device:", device)
    train(
        net,
        train_iter,
        test_iter,
        num_epochs,
        lr,
        device
    )