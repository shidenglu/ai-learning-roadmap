# 计算 MSE
import numpy as np

y = np.array([100,120,140])

y_hat = np.array([90,110,150])

mse = np.mean((y - y_hat)**2)

print(mse)