import numpy as np
import matplotlib.pyplot as plt

# 模拟一张 28×28 图片
image = np.random.rand(28, 28)

plt.imshow(image)

plt.title("MNIST Image")

plt.show()