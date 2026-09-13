import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt

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

params = [
    W1,
    b1,
    W2,
    b2
]

# ==========================
# 激活函数 ReLU
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
    # [batch,1,28,28]
    #
    # 转换
    #
    # [batch,784]
    X = X.reshape(
        (-1,num_inputs)
    )

    # 隐藏层
    H = relu(
        X @ W1 + b1
    )

    # 输出层
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
# 测试准确率
# ==========================
def evaluate_accuracy():
    correct = 0
    total = 0
    with torch.no_grad():
        for X,y in test_iter:
            y_hat = net(X)
            correct += (
                y_hat.argmax(dim=1)==y
            ).sum().item()
            total += y.shape[0]
    return correct / total

# ==========================
# 保存训练数据
# ==========================
loss_history = []
train_acc_history = []
test_acc_history = []

# ==========================
# 保存训练曲线
# ==========================
def update_plot(epoch,num_epochs):
    plt.figure(
        figsize=(10,5)
    )

    # loss
    plt.subplot(
        1,
        2,
        1
    )

    plt.plot(
        loss_history,
        marker="o"
    )

    plt.xlabel(
        "epoch"
    )

    plt.ylabel(
        "loss"
    )

    plt.title(
        f"Loss Epoch {epoch}/{num_epochs}"
    )

    plt.grid()

    # accuracy
    plt.subplot(
        1,
        2,
        2
    )

    plt.plot(
        train_acc_history,
        label="train acc",
        marker="o"
    )

    plt.plot(
        test_acc_history,
        label="test acc",
        marker="s"
    )

    plt.xlabel(
        "epoch"
    )

    plt.ylabel(
        "accuracy"
    )

    plt.title(
        "Accuracy"
    )

    plt.legend()

    plt.grid()

    # 保存图片
    plt.savefig(
        "training_progress.png",
        dpi=200
    )

    plt.close()

# ==========================
# 训练
# ==========================

def main():
    num_epochs = 10
    for epoch in range(num_epochs):
        train_loss = 0
        train_acc = 0
        train_num = 0

        for X,y in train_iter:
            # forward
            y_hat = net(X)

            # loss
            l = loss(
                y_hat,
                y
            )

            # 清空梯度
            updater.zero_grad()

            # backward
            l.backward()

            # 更新参数
            updater.step()

            train_loss += (
                l.item()
                *
                y.shape[0]
            )

            train_acc += (
                y_hat.argmax(dim=1)==y
            ).sum().item()

            train_num += y.shape[0]

        train_loss /= train_num
        train_acc /= train_num
        test_acc = evaluate_accuracy()

        # 保存
        loss_history.append(
            train_loss
        )

        train_acc_history.append(
            train_acc
        )

        test_acc_history.append(
            test_acc
        )

        print(
            f"epoch={epoch+1:2d} "
            f"loss={train_loss:.4f} "
            f"train_acc={train_acc:.4f} "
            f"test_acc={test_acc:.4f}"
        )

        # 每个epoch更新图片
        update_plot(
            epoch+1,
            num_epochs
        )

        img_path = r".\\training_progress.png"
        img = plt.imread(
            img_path
        )

        plt.figure(
            figsize=(6,6)
        )

        plt.imshow(
            img
        )

        plt.axis("off")

        plt.show(block=False)

        plt.pause(3)

        plt.close()

# ==========================
# 显示预测
# ==========================
def show_prediction():
    classes = [
        't-shirt',
        'trouser',
        'pullover',
        'dress',
        'coat',
        'sandal',
        'shirt',
        'sneaker',
        'bag',
        'ankle boot'
    ]

    X,y = next(iter(test_iter))

    y_hat = net(X)

    plt.figure(
        figsize=(10,5)
    )

    for i in range(10):
        plt.subplot(
            2,
            5,
            i+1
        )

        plt.imshow(
            X[i].reshape(28,28),
            cmap="gray"
        )

        pred = y_hat[i].argmax().item()

        plt.title(
            f"P:{classes[pred]}\nT:{classes[y[i]]}",
            fontsize=8
        )

        plt.axis("off")

    plt.show()

# ==========================
# 主程序
# ==========================
if __name__ == "__main__":

    main()

    show_prediction()