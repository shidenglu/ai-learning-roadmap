import torch
from d2l import torch as d2l
import matplotlib.pyplot as plt


# ============================
# 1. 加载数据
# ============================

batch_size = 256

# Windows环境建议num_workers=0
train_iter, test_iter = d2l.load_data_fashion_mnist(
    batch_size
)


# ============================
# 2. 定义模型参数
# ============================

num_inputs = 784
num_outputs = 10


# W: [784,10]
W = torch.normal(
    0,
    0.01,
    size=(num_inputs, num_outputs),
    requires_grad=True
)

# b: [10]
b = torch.zeros(
    num_outputs,
    requires_grad=True
)



# ============================
# 3. softmax函数
# ============================

def softmax(X):

    # 防止exp溢出
    X_max = X.max(
        dim=1,
        keepdim=True
    ).values


    X_exp = torch.exp(
        X - X_max
    )


    partition = X_exp.sum(
        dim=1,
        keepdim=True
    )


    return X_exp / partition



# ============================
# 4. 网络
# ============================

def net(X):

    X = X.reshape(
        (-1, W.shape[0])
    )


    return softmax(
        torch.matmul(X, W) + b
    )



# ============================
# 5. 交叉熵损失
# ============================

def cross_entropy(y_hat, y):

    return -torch.log(
        y_hat[
            torch.arange(len(y_hat)),
            y
        ]
    )



# ============================
# 6. 计算准确率
# ============================

def accuracy(y_hat, y):

    if len(y_hat.shape) > 1:

        y_hat = y_hat.argmax(
            dim=1
        )


    return (
        y_hat == y
    ).sum().item()



# ============================
# 7. 累加器
# ============================

class Accumulator:

    def __init__(self, n):

        self.data = [
            0.0
        ] * n


    def add(self, *args):

        self.data = [
            a + float(b)
            for a, b in zip(
                self.data,
                args
            )
        ]


    def reset(self):

        self.data = [
            0.0
        ] * len(self.data)


    def __getitem__(self, idx):

        return self.data[idx]



# ============================
# 8. 测试准确率
# ============================

def evaluate_accuracy(net, data_iter):

    metric = Accumulator(2)

    with torch.no_grad():

        for X, y in data_iter:

            metric.add(
                accuracy(net(X), y),
                y.numel()
            )


    return metric[0] / metric[1]



# ============================
# 9. Windows版绘图类
# ============================

class Animator:


    def __init__(
            self,
            xlabel=None,
            ylabel=None,
            legend=None,
            xlim=None,
            ylim=None
    ):

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend = legend

        self.X = []
        self.Y = []


        self.fig, self.ax = plt.subplots(
            figsize=(6,4)
        )


        self.xlim = xlim
        self.ylim = ylim



    def add(self, x, y):


        if not isinstance(
                y,
                (list,tuple)
        ):
            y = [y]


        if len(self.Y)==0:

            self.Y = [
                []
                for _ in range(len(y))
            ]


        for i,value in enumerate(y):

            self.Y[i].append(value)


        self.X.append(x)



        self.ax.clear()



        for i,data in enumerate(self.Y):

            self.ax.plot(
                range(
                    1,
                    len(data)+1
                ),
                data,
                label=self.legend[i]
            )


        self.ax.set_xlabel(
            self.xlabel
        )

        self.ax.set_ylabel(
            self.ylabel
        )


        if self.xlim:

            self.ax.set_xlim(
                self.xlim
            )


        if self.ylim:

            self.ax.set_ylim(
                self.ylim
            )


        self.ax.legend()


        # Windows实时刷新
        plt.pause(0.1)



# ============================
# 10. 一个epoch训练
# ============================

def train_epoch_ch3(
        net,
        train_iter,
        loss,
        updater):


    metric = Accumulator(3)


    for X,y in train_iter:


        y_hat = net(X)


        l = loss(
            y_hat,
            y
        )


        l.sum().backward()


        updater(
            X.shape[0]
        )


        metric.add(
            float(l.sum()),
            accuracy(
                y_hat,
                y
            ),
            y.numel()
        )


    return (
        metric[0]/metric[2],
        metric[1]/metric[2]
    )



# ============================
# 11. 训练函数
# ============================

def train_ch3(
        net,
        train_iter,
        test_iter,
        loss,
        num_epochs,
        updater):


    animator = Animator(
        xlabel="epoch",
        ylabel="value",
        xlim=[1,num_epochs],
        ylim=[0.3,1],
        legend=[
            "train loss",
            "train acc",
            "test acc"
        ]
    )


    for epoch in range(num_epochs):


        train_metrics = train_epoch_ch3(
            net,
            train_iter,
            loss,
            updater
        )


        test_acc = evaluate_accuracy(
            net,
            test_iter
        )


        animator.add(
            epoch+1,
            train_metrics+(test_acc,)
        )


        print(
            f"epoch {epoch+1}: ",
            f"loss={train_metrics[0]:.3f}, ",
            f"train acc={train_metrics[1]:.3f}, ",
            f"test acc={test_acc:.3f}"
        )



    # 保存图片
    plt.savefig(
        "softmax_training.png",
        dpi=300
    )



# ============================
# 12. SGD优化器
# ============================

lr = 0.1


def updater(batch_size):

    d2l.sgd(
        [W,b],
        lr,
        batch_size
    )



# ============================
# 13. 主函数
# ============================

def main():


    num_epochs = 10


    train_ch3(
        net,
        train_iter,
        test_iter,
        cross_entropy,
        num_epochs,
        updater
    )


    plt.show()



if __name__ == "__main__":

    main()