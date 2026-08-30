import numpy as np
import matplotlib.pyplot as plt

attention = np.array([
    [0.8, 0.1, 0.05, 0.05],
    [0.2, 0.6, 0.1, 0.1],
    [0.1, 0.2, 0.6, 0.1],
    [0.05, 0.1, 0.15, 0.7]
])

plt.imshow(
    attention,
    cmap="viridis"
)

plt.colorbar()

plt.xlabel("Key")
plt.ylabel("Query")

plt.title("Attention Matrix")

plt.show()