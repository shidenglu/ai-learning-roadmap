import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageDraw

# ==========================
# AlexNet
# ==========================
net = nn.Sequential(
    nn.Conv2d(1, 96, kernel_size=11, stride=4, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    nn.Conv2d(96, 256, kernel_size=5, padding=2), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    nn.Conv2d(256, 384, kernel_size=3, padding=1), nn.ReLU(),
    nn.Conv2d(384, 384, kernel_size=3, padding=1), nn.ReLU(),
    nn.Conv2d(384, 256, kernel_size=3, padding=1), nn.ReLU(),
    nn.MaxPool2d(kernel_size=3, stride=2),
    nn.Flatten(),
    nn.Linear(6400, 4096), nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(4096, 4096), nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(4096, 10)
)

# ==========================
# MNIST 数据
# ==========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

train_dataset = datasets.MNIST(
    root="./data",
    train=True,
    transform=transform,
    download=True
)

test_dataset = datasets.MNIST(
    root="./data",
    train=False,
    transform=transform,
    download=True
)

batch_size = 128
train_iter = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True
)

test_iter = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False
)
# ==========================
# Accuracy
# ==========================
def evaluate_accuracy_gpu(net, data_iter, device=None):
    net.eval()
    if device is None:
        device = next(net.parameters()).device
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in data_iter:
            X = X.to(device)
            y = y.to(device)
            pred = net(X).argmax(dim=1)
            correct += (pred == y).sum().item()
            total += y.numel()

    return correct / total
# ==========================
# Training
# ==========================
def train_ch6(net, train_iter, test_iter, num_epochs, lr, device):
    def init_weights(m):
        if isinstance(
                m,
                (nn.Linear, nn.Conv2d)):

            nn.init.xavier_uniform_(
                m.weight
            )

    net.apply(init_weights)
    net.to(device)
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
            total_loss += (
                l.item() * X.shape[0]
            )
            total_correct += (
                y_hat.argmax(dim=1) == y
            ).sum().item()
            total_num += X.shape[0]
        train_loss = (
            total_loss / total_num
        )

        train_acc = (
            total_correct / total_num
        )

        test_acc = evaluate_accuracy_gpu(
            net,
            test_iter,
            device
        )

        train_loss_list.append(
            train_loss
        )

        train_acc_list.append(
            train_acc
        )

        test_acc_list.append(
            test_acc
        )

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

    # ==========================
    # 最后绘制训练曲线
    # ==========================
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

    axes[0].set_title(
        "Training Loss"
    )

    axes[0].set_xlabel(
        "Epoch"
    )

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

    axes[1].set_title(
        "Accuracy"
    )

    axes[1].set_xlabel(
        "Epoch"
    )

    axes[1].legend()

    axes[1].grid(True)

    plt.tight_layout()

    plt.show()


# ==========================
# 手写数字识别
# ==========================
def draw_digit(net, device):
    window = tk.Tk()
    window.title(
        "MNIST Handwritten Digit Recognition"
    )

    window.geometry(
        "500x600"
    )

    canvas_size = 600
    canvas = tk.Canvas(
        window,
        width=canvas_size,
        height=canvas_size,
        bg="black"
    )

    canvas.pack(
        pady=20
    )
    image = Image.new(
        "L",
        (canvas_size, canvas_size),
        0
    )
    draw = ImageDraw.Draw(image)
    # ==========================
    # 鼠标绘制
    # ==========================
    def paint(event):
        x = event.x
        y = event.y
        radius = 10
        canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="white",
            outline="white"
        )
        draw.ellipse(
            [
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ],
            fill=255
        )
    canvas.bind(
        "<B1-Motion>",
        paint
    )
    # ==========================
    # 清空
    # ==========================
    def clear():
        canvas.delete(
            "all"
        )
        draw.rectangle(
            [
                0,
                0,
                canvas_size,
                canvas_size
            ],
            fill=0
        )
        result_label.config(
            text="Prediction: "
        )
    # ==========================
    # 预测
    # ==========================
    def predict():
        img = image.resize(
            (224, 224)
        )
        tensor = torch.tensor(
            list(img.getdata()),
            dtype=torch.float32
        )
        tensor = tensor.reshape(
            1,
            1,
            224,
            224
        )
        tensor = tensor / 255.0
        tensor = tensor.to(
            device
        )
        net.eval()
        with torch.no_grad():
            output = net(tensor)
            prediction = output.argmax(
                dim=1
            ).item()
            probability = torch.softmax(
                output,
                dim=1
            )
            confidence = probability[
                0,
                prediction
            ].item()
        result_label.config(
            text=(
                f"Prediction: {prediction}\n"
                f"Confidence: {confidence:.2%}"
            )
        )
    # ==========================
    # 按钮
    # ==========================
    button_frame = tk.Frame(
        window
    )
    button_frame.pack(
        pady=10
    )
    predict_button = tk.Button(
        button_frame,
        text="Predict",
        font=("Arial", 14),
        width=10,
        command=predict
    )
    predict_button.pack(
        side=tk.LEFT,
        padx=10
    )
    clear_button = tk.Button(
        button_frame,
        text="Clear",
        font=("Arial", 14),
        width=10,
        command=clear
    )
    clear_button.pack(
        side=tk.LEFT,
        padx=10
    )
    result_label = tk.Label(
        window,
        text="Prediction: ",
        font=("Arial", 20)
    )
    result_label.pack(
        pady=20
    )
    window.mainloop()
# ==========================
# Main
# ==========================
if __name__ == "__main__":
    # 查看网络结构
    X = torch.randn(1, 1, 224, 224)
    for layer in net:
        X = layer(X)
        print(layer.__class__.__name__, "output shape:", X.shape)

    # ==========================
    # 训练
    # ==========================
    lr = 0.01
    num_epochs = 10
    device = (
        torch.device("cuda")
        if torch.cuda.is_available()
        else torch.device("cpu")
    )
    
    train_ch6(net, train_iter, test_iter, num_epochs, lr, device)
    # ==========================
    # 手写数字预测
    # ==========================
    draw_digit(
        net,
        device
    )