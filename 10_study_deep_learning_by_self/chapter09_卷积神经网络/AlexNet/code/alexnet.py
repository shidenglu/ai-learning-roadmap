import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt

net = nn.Sequential(
    # 这里使用一个11*11的更大窗口来捕捉对象。
    # 同时，步幅为4，以减少输出的高度和宽度。
    # 另外，输出通道的数目远大于LeNet
    nn.Conv2d(1, 96, kernel_size=11, stride=4, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    # 减小卷积窗口，使用填充为2来使得输入与输出的高和宽一致，且增大输出通道数
    nn.Conv2d(96, 256, kernel_size=5, padding=2), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    # 使用三个连续的卷积层和较小的卷积窗口。
    # 除了最后的卷积层，输出通道的数量进一步增加。
    # 在前两个卷积层之后，汇聚层不用于减少输入的高度和宽度
    nn.Conv2d(256, 384, kernel_size=3, padding=1), nn.ReLU(),
    nn.Conv2d(384, 384, kernel_size=3, padding=1), nn.ReLU(),
    nn.Conv2d(384, 256, kernel_size=3, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    # nn.Flatten 把数据平摊为一个一维的张量
    nn.Flatten(),
    # 这里，全连接层的输出数量是LeNet中的好几倍。使用dropout层来减轻过拟合
    nn.Linear(6400, 4096), nn.ReLU(),
    # 训练时，随机把 50% 的神经元输出“暂时关掉”，让网络不要过度依赖某几个神经元。
    nn.Dropout(0.5),
    nn.Linear(4096, 4096), nn.ReLU(),
    nn.Dropout(0.5),
    # 最后是输出层。由于这里使用Fashion-MNIST，所以用类别数为10，而非论文中的1000
    nn.Linear(4096, 10)
)

# ==========================
# 加载 Fashion-MNIST 数据
# ==========================
# 由于AlexNet中全连接层的输入个数远大于LeNet，所以这里需要将图像放大到224*224像素
batch_size = 128
train_iter, test_iter = d2l.load_data_fashion_mnist(
    batch_size=batch_size,
    resize=224
)

def evaluate_accuracy_gpu(net, data_iter, device=None):
    if isinstance(net, nn.Module):
        # Set the model to evaluation mode
        net.eval()
        if device is None:
            device = next(net.parameters()).device

    correct = 0
    total = 0

    # 只做推理，不用计算梯度
    with torch.no_grad():
        for X, y in data_iter:
            # 把 X 和 y 都放到指定的设备上
            # 有的模型可能有多个输入，因此需要判断X是否是列表
            # X = [Tensor, Tensor, Tensor]
            if isinstance(X, list):
                X = [x.to(device) for x in X]
            else:
                X = X.to(device)
            y = y.to(device)

            # 计算预测结果
            pred = net(X).argmax(dim=1)
            # 统计预测正确的数量和总样本数
            correct += (pred == y).sum().item()
            total += y.numel()
    # 计算并返回准确率
    return correct / total

def train_ch6(
        net,
        train_iter,
        test_iter,
        num_epochs,
        lr,
        device):
    # Initialize the weights of the network using Xavier initialization
    # 如果当前这一层是 Linear 或者 Conv2d，就给它初始化权重。
    # Conv2d       → 初始化 ✓
    # ReLU         → 不处理
    # MaxPool2d    → 不处理
    # Conv2d       → 初始化 ✓
    # Linear       → 初始化 ✓
    # Dropout      → 不处理
    # Linear       → 初始化 ✓
    def init_weights(m):
        if isinstance(
                m,
                (nn.Linear, nn.Conv2d)):
            nn.init.xavier_uniform_(m.weight)

    # 把 init_weights 这个函数应用到 net 的每一层
    net.apply(init_weights)

    # Print the device being used for training
    net.to(device)

    # Define the optimizer and loss function
    optimizer = torch.optim.SGD(
        net.parameters(),
        lr=lr
    )
    loss = nn.CrossEntropyLoss()

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    print("training on", device)

    for epoch in range(num_epochs):
        # Set the model to training mode
        net.train()
        total_loss = 0
        total_correct = 0
        total_num = 0

        for X, y in train_iter:
            # Move the data to the specified device (GPU or CPU)
            X = X.to(device)
            y = y.to(device)
            # Compute the predictions and loss
            # 把上一轮训练留下来的梯度清零。 有些场景会做梯度累加，这里不需要，所以要清零。
            optimizer.zero_grad()
            # Compute the predictions and loss
            y_hat = net(X)
            # Compute the loss using the predictions and true labels
            l = loss(y_hat, y)
            # Compute the gradients and update the parameters
            # 反向传播计算梯度
            l.backward()
            # Update the parameters using the optimizer
            # 这里的 optimizer.step() 做了两件事：
            # 1. 根据计算得到的梯度更新模型参数
            # 2. 把梯度清零，以便下一轮训练使用
            optimizer.step()
            # 统计训练损失和准确率
            # 这里的 total_loss 是一个累加值，表示当前 epoch 的总损失。
            # 由于每个 batch 的大小可能不同，所以要乘以当前 batch 的样本数 X.shape[0]，这样才能得到总损失。
            # 例如，如果当前 batch 的大小是 128，那么 total_loss 就会加上 128 个样本的损失。
            total_loss += l.item() * X.shape[0]
            total_correct += (
                y_hat.argmax(dim=1) == y
            ).sum().item()

            total_num += X.shape[0]

        train_loss = total_loss / total_num
        train_acc = total_correct / total_num

        test_acc = evaluate_accuracy_gpu(
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

    print(
        f"\nFinal: "
        f"Loss={train_loss:.4f} "
        f"TrainAcc={train_acc:.4f} "
        f"TestAcc={test_acc:.4f}"
    )

    epochs = range(1, num_epochs + 1)

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10, 6)
    )

    axes[0].plot(
        epochs,
        train_loss_list,
        linewidth=2
    )

    axes[0].set_title("Training Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].grid(True)

    axes[1].plot(
        epochs,
        train_acc_list,
        label="Train Acc",
        linewidth=2
    )

    axes[1].plot(
        epochs,
        test_acc_list,
        label="Test Acc",
        linewidth=2
    )

    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # ==========================
    # 查看网络结构
    # ==========================
    X = torch.randn(1, 1, 224, 224)
    for layer in net:
        X = layer(X)
        print(layer.__class__.__name__, "output shape:", X.shape)

    # ==========================
    # 训练模型
    # ==========================
    lr = 0.01
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
