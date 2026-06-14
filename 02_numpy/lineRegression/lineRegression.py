import numpy as np

X = np.array([
    [50,1],
    [60,1],
    [70,1],
    [80,1],
    [90,1]
])

y = np.array([
    [100],
    [120],
    [140],
    [160],
    [180]
])

theta = np.linalg.inv(
    X.T @ X
) @ X.T @ y

w = theta[0,0]
b = theta[1,0]

print("w =", w)
print("b =", b)