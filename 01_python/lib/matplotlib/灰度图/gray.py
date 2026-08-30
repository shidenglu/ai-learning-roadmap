import numpy as np
import matplotlib.pyplot as plt

image = np.random.rand(28, 28)

plt.imshow(
    image,
    cmap="gray"
)

plt.title("MNIST")

plt.axis("off")

plt.show()