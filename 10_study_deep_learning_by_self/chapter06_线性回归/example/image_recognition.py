import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


# ===============================
# 1. GPU设备选择
# ===============================
device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print("当前设备:", device)

# ===============================
# 2. 加载MNIST数据
# ===============================
# 功能：定义一组数据预处理操作，把原始图片转换成 PyTorch 可以训练的 Tensor 格式。
# Compose 把多个预处理步骤串起来，按顺序执行。
# 图片-》操作1-》操作2-》操作3-》tensor
# tensor 才是 pytorch 可以训练的结构
transform = transforms.Compose([
    transforms.ToTensor()
])


# 创建一个 MNIST 训练数据集对象。
# 去哪里找数据？加载训练集还是测试集？没有数据时是否自动下载？读取图片时如何预处理？
train_dataset = datasets.MNIST(
    root="./data",
    train=True,
    download=True,
    transform=transform
)

# 创建一个 MNIST 测试数据集对象。
# 去哪里找数据？加载训练集还是测试集？没有数据时是否自动下载？读取图片时如何预处理？
test_dataset = datasets.MNIST(
    root="./data",
    train=False,
    download=True,
    transform=transform
)

# 每次取出 256 张图片进行训练
# test_dataset 是一整本书，DataLoader 是把这本书按页码一页页拿出来给模型看。
batch_size = 256
train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True
)

# 每次取出 256 张图片进行测试
test_loader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False
)

# ===============================
# 3. 定义Softmax分类网络
# ===============================
# 定义一个神经网络类，继承 nn.Module ，表示这是一个PyTorch神经网络模型
class SoftmaxNet(nn.Module):
    def __init__(self):
        # 调用父类的初始化函数
        super().__init__()
        # 图片转换成1维向量
        self.flatten = nn.Flatten()
        # 对应数学 y = Wx + b
        self.linear = nn.Linear(
            28*28,
            10
        )

    # 前向传播
    # 输入一张图片，首先转换为一维向量
    # 然后计算出结果，返回
    def forward(self,x):
        x = self.flatten(x)
        logits = self.linear(x)
        return logits

# 创建网络会自动执行 __init__ 方法，初始化网络参数
net = SoftmaxNet()
# 选择设备
net = net.to(device)
print(net)

# ===============================
# 4. 损失函数
# ===============================
loss_fn = nn.CrossEntropyLoss()

# ===============================
# 5. 优化器
# ===============================
# 随机梯度下降的优化器
# net.parameters() 把网络里面所有需要训练的参数交给优化器
optimizer = torch.optim.SGD(
    net.parameters(),
    lr=0.1
)

# ===============================
# 6. 训练
# ===============================
epochs = 10

train_loss_history = []
train_acc_history = []

for epoch in range(epochs):
    net.train()
    total_loss = 0
    correct = 0
    total = 0

    for X,y in train_loader:
        # 数据放GPU
        X = X.to(device)
        y = y.to(device)

        # 前向传播，得到预测值
        logits = net(X)

        # 计算loss
        # 计算预测和实际的损失
        loss = loss_fn(
            logits,
            y
        )

        # 清梯度
        # PyTorch 默认会做梯度累加，第一次等于 0.1，第二次 0.2 + 0.1 = 0.3
        optimizer.zero_grad()

        # 反向传播
        # 计算模型里的每个参数的梯度
        loss.backward()

        # 更新参数
        optimizer.step()

        # 统计误差
        # 把当前 batch 的平均交叉熵损失取出来（Tensor转Python数字），累积到整个epoch的总损失中，用于后面统计训练误差。
        total_loss += loss.item()

        # 在所有标签中找出值最大对应的标签，即预测值
        pred = logits.argmax(
            dim=1
        )

        # 下面的 y 是真实值
        # 预测对一个就 ++
        correct += (
            pred == y
        ).sum().item()

        # 总共有多少样本
        total += y.size(0)

    epoch_loss = total_loss / len(train_loader)
    epoch_acc = correct / total

    train_loss_history.append(
        epoch_loss
    )

    train_acc_history.append(
        epoch_acc
    )

    print(
        f"Epoch:{epoch+1}, "
        f"Loss:{epoch_loss:.4f}, "
        f"Acc:{epoch_acc:.4f}"
    )



# ===============================
# 7. 测试
# ===============================
# 把神经网络切换到 评估模式（evaluation mode），即预测
net.eval()

correct = 0
total = 0

# torch.no_grad() 关闭梯度更新
with torch.no_grad():
    # 便利测试集
    for X,y in test_loader:
        # 选择执行的设备
        X = X.to(device)
        y = y.to(device)

        # 预测出结果 10*1 维度的向量
        logits = net(X)

        # 选择值最大的作为预测值
        pred = logits.argmax(
            dim=1
        )

        # 预测对了
        correct += (
            pred == y
        ).sum().item()

        # 总共预测了多少样本
        total += y.size(0)



print(
    "测试准确率:",
    correct / total
)



# ===============================
# 8. 显示训练曲线
# ===============================


plt.figure()

plt.plot(
    train_loss_history
)

plt.xlabel(
    "epoch"
)

plt.ylabel(
    "loss"
)

plt.title(
    "Training Loss"
)

plt.show()



# ===============================
# 9. 随机预测一个图片
# ===============================
# image 是一个 1*28*28 的张量，label 是一个数字
image,label = test_dataset[0]

# 绘制图片
# image.squeeze() 去掉维度为 1 的维度，得 28*28 图形
plt.imshow(
    image.squeeze(),
    cmap="gray"
)

# 显示真实标签
plt.title(
    f"label:{label}"
)

# 显示图像
plt.show()

# 增加 batch 维度，变成 1*1*28*28
# 网络训练时得输入时 batch*channel*height*width 的四维张量
image = image.unsqueeze(0)
image = image.to(device)

# torch.no_grad() 关闭梯度
with torch.no_grad():
    # 预测结果 10*1 维度的向量
    output = net(image)
    # 选取最大的那个值得小标作为输出
    prediction = output.argmax(
        dim=1
    )

print(
    "预测结果:",
    prediction.item()
)

# 绘制图片
# import matplotlib.pyplot as plt

# # 假设你已经成功加载了数据 (test_dataset)
# sample = test_dataset[0] 
# image_tensor = sample[0] # 取出图像部分
# label = sample[1]        # 取出标签部分

# # 2. 预处理：
# # image_tensor 是 (1, 28, 28) 的形状，包含一个通道维度
# # imshow 需要的是 (28, 28)
# # 使用 .squeeze() 去掉维度为 1 的那一维
# image_to_show = image_tensor.squeeze().numpy()

# # 3. 绘图
# plt.imshow(image_to_show, cmap='gray')
# plt.title(f"Label: {label}")
# plt.show()