import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

import torch
from torch import nn
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader


def main():

    # ==========================================
    # GPU
    # ==========================================

    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    print("Device:", device)

    # ==========================================
    # 读取数据
    # ==========================================

    train_df = pd.read_csv("train.csv")

    print("原始数据维度:", train_df.shape)

    # ==========================================
    # 删除ID
    # ==========================================

    train_df = train_df.drop(columns=["Id"])

    # ==========================================
    # 标签
    # ==========================================

    y = train_df["SalePrice"]

    # ==========================================
    # 特征
    # ==========================================

    X = train_df.drop(columns=["SalePrice"])

    # ==========================================
    # One-Hot编码
    # ==========================================

    X = pd.get_dummies(X)

    print("编码后维度:", X.shape)

    # ==========================================
    # 缺失值处理
    # ==========================================

    imputer = SimpleImputer(strategy="median")

    X = imputer.fit_transform(X)

    # ==========================================
    # 标准化
    # ==========================================

    scaler = StandardScaler()

    X = scaler.fit_transform(X)

    # ==========================================
    # 数据集划分
    # ==========================================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # ==========================================
    # Tensor
    # ==========================================

    X_train = torch.tensor(
        X_train,
        dtype=torch.float32
    )

    X_test = torch.tensor(
        X_test,
        dtype=torch.float32
    )

    y_train = torch.tensor(
        y_train.values,
        dtype=torch.float32
    ).reshape(-1, 1)

    y_test = torch.tensor(
        y_test.values,
        dtype=torch.float32
    ).reshape(-1, 1)

    # ==========================================
    # DataLoader
    # ==========================================

    batch_size = 64

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=batch_size,
        shuffle=True,
        num_workers=0
    )

    # ==========================================
    # 网络
    # ==========================================

    input_dim = X_train.shape[1]

    model = nn.Sequential(
        nn.Linear(input_dim, 256),
        nn.ReLU(),

        nn.Linear(256, 128),
        nn.ReLU(),

        nn.Linear(128, 64),
        nn.ReLU(),

        nn.Linear(64, 1)
    ).to(device)

    # ==========================================
    # Loss
    # ==========================================

    criterion = nn.MSELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    # ==========================================
    # Train
    # ==========================================

    epochs = 100

    for epoch in range(epochs):

        model.train()

        total_loss = 0

        for X_batch, y_batch in train_loader:

            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            pred = model(X_batch)

            loss = criterion(
                pred,
                y_batch
            )

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        if (epoch + 1) % 10 == 0:

            print(
                f"Epoch {epoch+1:3d}"
                f" Loss={total_loss:.4f}"
            )

    # ==========================================
    # Test
    # ==========================================

    model.eval()

    with torch.no_grad():

        pred = model(
            X_test.to(device)
        )

        mse = criterion(
            pred,
            y_test.to(device)
        )

        rmse = torch.sqrt(mse)

    print("\nTest RMSE =", rmse.item())

    # ==========================================
    # Predict
    # ==========================================

    sample = X_test[0].reshape(1, -1)

    with torch.no_grad():

        price = model(
            sample.to(device)
        )

    print("\n真实房价:", y_test[0].item())
    print("预测房价:", price.item())


if __name__ == "__main__":
    main()