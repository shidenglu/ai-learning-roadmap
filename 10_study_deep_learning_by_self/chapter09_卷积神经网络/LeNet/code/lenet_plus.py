import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt

# ==========================
# LeNet 网络结构
# ==========================
net = nn.Sequential(
    nn.Conv2d(1, 6, kernel_size=5, padding=2),
    nn.Sigmoid(),
    nn.AvgPool2d(kernel_size=2, stride=2),
    nn.Conv2d(6, 16, kernel_size=5),
    nn.Sigmoid(),
    nn.AvgPool2d(kernel_size=2, stride=2),
    nn.Flatten(),
    nn.Linear(16 * 5 * 5, 120),
    nn.Sigmoid(),
    nn.Linear(120, 84),
    nn.Sigmoid(),
    nn.Linear(84, 10)
)

# ==========================
# 查看网络结构
# ==========================
X = torch.rand(size=(1, 1, 28, 28))
print("=" * 50)
print("LeNet Shape")
print("=" * 50)
for layer in net:
    X = layer(X)
    print(
        f"{layer.__class__.__name__}",
        X.shape
    )

# ==========================
# 加载 Fashion-MNIST 数据
# ==========================
batch_size = 256

train_iter, test_iter = d2l.load_data_fashion_mnist(
    batch_size=batch_size
)

# ==========================
# Accuracy
# ==========================
def accuracy(y_hat, y):
    if len(y_hat.shape) > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp = y_hat.type(y.dtype) == y
    return float(
        cmp.type(y.dtype).sum()
    )

# ==========================
# GPU Accuracy
# ==========================
def evaluate_accuracy_gpu(
        net,
        data_iter,
        device=None):

    if isinstance(net, nn.Module):
        net.eval()
        if device is None:
            device = next(
                net.parameters()
            ).device
    metric = [0, 0]
    with torch.no_grad():
        for X, y in data_iter:
            X = X.to(device)
            y = y.to(device)
            metric[0] += accuracy(
                net(X),
                y
            )
            metric[1] += y.numel()
    return metric[0] / metric[1]

# ==========================
# Train
# ==========================
def train_ch6(
        net,
        train_iter,
        test_iter,
        num_epochs,
        lr,
        device):

    # ==========================
    # Xavier 初始化
    # ==========================
    def init_weights(m):
        if isinstance(
                m,
                (nn.Linear, nn.Conv2d)
        ):
            nn.init.xavier_uniform_(
                m.weight
            )
    net.apply(init_weights)
    print("\nTraining on:", device)
    # ==========================
    # 将网络移动到 GPU / CPU
    # ==========================
    net.to(device)
    # ==========================
    # 优化器
    # ==========================
    optimizer = torch.optim.SGD(
        net.parameters(),
        lr=lr
    )
    # ==========================
    # 损失函数
    # ==========================
    loss = nn.CrossEntropyLoss()
    # ==========================
    # 保存训练数据
    #
    # 注意：
    # 这里不再实时绘图
    # ==========================
    train_loss_list = []
    train_acc_list = []
    test_acc_list = []
    # ==========================
    # 开始训练
    # ==========================
    for epoch in range(num_epochs):
        net.train()
        total_loss = 0
        total_correct = 0
        total_num = 0
        # ==========================
        # 一个 Epoch 的训练
        # ==========================
        for X, y in train_iter:
            # --------------------------
            # 数据移动到 GPU
            # --------------------------
            X = X.to(device)
            y = y.to(device)
            # --------------------------
            # 梯度清零
            # --------------------------
            optimizer.zero_grad()
            # --------------------------
            # 前向传播
            # --------------------------
            y_hat = net(X)
            # --------------------------
            # 计算 Loss
            # --------------------------
            l = loss(
                y_hat,
                y
            )
            # --------------------------
            # 反向传播
            # --------------------------
            l.backward()
            # --------------------------
            # 更新参数
            # --------------------------
            optimizer.step()
            # --------------------------
            # 累加 Loss
            # --------------------------
            total_loss += (
                l.item() * X.shape[0]
            )
            # --------------------------
            # 累加预测正确数量
            # --------------------------
            total_correct += accuracy(
                y_hat,
                y
            )
            # --------------------------
            # 累加样本数量
            # --------------------------
            total_num += X.shape[0]
        # ==========================
        # 计算平均 Loss
        # ==========================
        train_loss = (
            total_loss / total_num
        )
        # ==========================
        # 计算训练集准确率
        # ==========================
        train_acc = (
            total_correct / total_num
        )
        # ==========================
        # 测试集准确率
        # ==========================
        test_acc = evaluate_accuracy_gpu(
            net,
            test_iter,
            device
        )
        # ==========================
        # 保存数据
        # ==========================
        train_loss_list.append(
            train_loss
        )
        train_acc_list.append(
            train_acc
        )
        test_acc_list.append(
            test_acc
        )
        # ==========================
        # 控制台打印
        # ==========================
        print(
            f"Epoch [{epoch + 1:2d}/{num_epochs}] "
            f"Loss={train_loss:.4f} "
            f"TrainAcc={train_acc:.4f} "
            f"TestAcc={test_acc:.4f}"
        )

    # ==================================================
    # 所有 Epoch 训练完成
    # ==================================================
    print("\nTraining finished!")
    # ==================================================
    # 最后统一绘图
    # ==================================================
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10, 6)
    )
    # ==========================
    # 第一张图：Training Loss
    # ==========================
    axes[0].plot(
        range(1, num_epochs + 1),
        train_loss_list,
        linewidth=2
    )
    axes[0].set_title(
        "Training Loss"
    )
    axes[0].set_xlabel(
        "Epoch"
    )
    axes[0].set_ylabel(
        "Loss"
    )
    axes[0].grid(True)
    # ==========================
    # 第二张图：Accuracy
    # ==========================
    axes[1].plot(
        range(1, num_epochs + 1),
        train_acc_list,
        label="Train Acc",
        linewidth=2
    )
    axes[1].plot(
        range(1, num_epochs + 1),
        test_acc_list,
        label="Test Acc",
        linewidth=2
    )
    axes[1].set_title(
        "Training / Test Accuracy"
    )
    axes[1].set_xlabel(
        "Epoch"
    )
    axes[1].set_ylabel(
        "Accuracy"
    )
    axes[1].legend()
    axes[1].grid(True)
    # ==========================
    # 自动调整布局
    # ==========================
    plt.tight_layout()
    # ==========================
    # 最后显示一次
    # ==========================
    plt.show()

# ==========================
# Main
# ==========================
if __name__ == "__main__":
    lr = 0.9
    num_epochs = 10
    device = d2l.try_gpu()
    train_ch6(
        net,
        train_iter,
        test_iter,
        num_epochs,
        lr,
        device
    )