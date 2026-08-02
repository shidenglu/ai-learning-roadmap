import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# ======================
# XOR数据
# ======================
X = torch.tensor([
    [0., 0.],
    [0., 1.],
    [1., 0.],
    [1., 1.]
])

y = torch.tensor([
    [0.],
    [1.],
    [1.],
    [0.]
])

# ======================
# MLP模型
# ======================
class XORNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(2, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)


model = XORNet()
# ======================
# 损失函数
# ======================
criterion = nn.BCELoss()

# ======================
# 优化器
# ======================
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.1
)

# ======================
# 训练
# ======================
loss_history = []
epochs = 5000
for epoch in range(epochs):
    y_hat = model(X)
    loss = criterion(
        y_hat,
        y
    )

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    loss_history.append(
        loss.item()
    )

    if epoch % 500 == 0:
        print(
            f"epoch={epoch:4d} "
            f"loss={loss.item():.6f}"
        )

# ======================
# 测试
# ======================

print("\n预测结果")
with torch.no_grad():
    pred = model(X)
    print(pred)

# ======================
# 画Loss曲线
# ======================

plt.figure(figsize=(8,5))

plt.plot(loss_history)

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.title("MLP Learning XOR")

plt.grid()

plt.show()