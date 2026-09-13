# 导入库
# 逻辑回归代码 根据二维坐标判断属于类别0，还是类别1

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# 构造数据集
# 特征

X = torch.tensor([
    [1.0, 1.0],
    [2.0, 1.0],
    [2.0, 2.0],
    [3.0, 2.0],

    [4.0, 5.0],
    [5.0, 4.0],
    [5.0, 5.0],
    [6.0, 5.0]
])

# 标签

y = torch.tensor([
    [0.0],
    [0.0],
    [0.0],
    [0.0],

    [1.0],
    [1.0],
    [1.0],
    [1.0]
])

print(X.shape)
print(y.shape)

# 画出数据

plt.figure(figsize=(5,5))

for i in range(len(X)):

    if y[i] == 0:
        plt.scatter(
            X[i][0],
            X[i][1],
            marker="o"
        )
    else:
        plt.scatter(
            X[i][0],
            X[i][1],
            marker="x"
        )

plt.grid()
plt.show()

# 定义逻辑回归模型

class LogisticRegression(nn.Module):

    def __init__(self):

        super().__init__()

        self.linear = nn.Linear(
            in_features=2,
            out_features=1
        )

    def forward(self, x):

        z = self.linear(x)

        p = torch.sigmoid(z)

        return p

# 创建模型

model = LogisticRegression()

print(model)

# 损失函数

criterion = nn.BCELoss()

# 优化器

optimizer = optim.SGD(
    model.parameters(),
    lr=0.1
)

# 参看初始参数

for name, param in model.named_parameters():

    print(name)

    print(param.data)

# 训练

epochs = 100

loss_history = []

for epoch in range(epochs):

    # Forward

    outputs = model(X)

    loss = criterion(
        outputs,
        y
    )

    # Backward

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    loss_history.append(
        loss.item()
    )

    if epoch % 10 == 0:

        print(
            f"Epoch={epoch:03d} "
            f"Loss={loss.item():.4f}"
        )

# 观察LOSS下降

plt.figure(figsize=(8,4))

plt.plot(loss_history)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title("Training Loss")

plt.grid()

plt.show()

# 查看训练后的参数

for name, param in model.named_parameters():

    print(name)

    print(param.data)

# 预测

test = torch.tensor([
    [4.0, 4.0]
])

prob = model(test)

print(prob)

# 转换成类别

pred = (prob > 0.5).float()

print(pred)