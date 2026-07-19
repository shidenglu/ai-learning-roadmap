import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt

# =========================
# 生成数据
# =========================
n_train, n_test = 20, 100
num_inputs = 200
batch_size = 5

true_w = torch.ones((num_inputs, 1)) * 0.01
true_b = 0.05

train_data = d2l.synthetic_data(
    true_w,
    true_b,
    n_train
)

test_data = d2l.synthetic_data(
    true_w,
    true_b,
    n_test
)

train_iter = d2l.load_array(
    train_data,
    batch_size
)

test_iter = d2l.load_array(
    test_data,
    batch_size,
    is_train=False
)

# =========================
# 初始化参数
# =========================
def init_params():
    w = torch.normal(
        0,
        1,
        size=(num_inputs, 1),
        requires_grad=True
    )

    b = torch.zeros(
        1,
        requires_grad=True
    )

    return w, b


# =========================
# L2正则项
# =========================
def l2_penalty(w):
    return torch.sum(w.pow(2)) / 2

# =========================
# 训练函数
# =========================
def train(lambd):
    w, b = init_params()
    net = lambda X: d2l.linreg(X, w, b)
    loss = d2l.squared_loss
    lr = 0.003
    num_epochs = 100
    train_losses = []
    test_losses = []
    epochs = []

    for epoch in range(num_epochs):
        for X, y in train_iter:
            l = loss(
                net(X),
                y
            ) + lambd * l2_penalty(w)

            l.sum().backward()

            d2l.sgd(
                [w, b],
                lr,
                batch_size
            )

            with torch.no_grad():
                w.grad.zero_()
                b.grad.zero_()

        if (epoch + 1) % 5 == 0:
            train_loss = d2l.evaluate_loss(
                net,
                train_iter,
                loss
            )

            test_loss = d2l.evaluate_loss(
                net,
                test_iter,
                loss
            )

            epochs.append(epoch + 1)
            train_losses.append(train_loss)
            test_losses.append(test_loss)

            print(
                f"epoch={epoch+1:3d} "
                f"train_loss={train_loss:.6f} "
                f"test_loss={test_loss:.6f}"
            )

    print(
        f"\nλ={lambd} 时 "
        f"w的L2范数 = {torch.norm(w).item():.6f}"
    )

    return epochs, train_losses, test_losses

# =========================
# 无权重衰减
# =========================
epochs1, train1, test1 = train(
    lambd=0
)

# =========================
# 有权重衰减
# =========================
epochs2, train2, test2 = train(
    lambd=3
)

# =========================
# 绘图
# =========================
plt.figure(figsize=(8, 5))

plt.plot(
    epochs1,
    train1,
    label="Train Loss (lambda=0)"
)

plt.plot(
    epochs1,
    test1,
    label="Test Loss (lambda=0)"
)

plt.plot(
    epochs2,
    train2,
    "--",
    label="Train Loss (lambda=3)"
)

plt.plot(
    epochs2,
    test2,
    "--",
    label="Test Loss (lambda=3)"
)

plt.yscale("log")

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title("Weight Decay (L2 Regularization)")

plt.legend()

plt.grid(True)

plt.show()