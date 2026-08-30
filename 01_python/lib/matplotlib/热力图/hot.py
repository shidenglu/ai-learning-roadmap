import numpy as np
import matplotlib.pyplot as plt

matrix = np.random.rand(10, 10)

plt.imshow(
    matrix,
    cmap="hot"
)

plt.colorbar()

plt.title("Heatmap")

plt.show()