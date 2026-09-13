import numpy as np
import matplotlib.pyplot as plt

# 模拟 CNN 输出
feature_maps = np.random.rand(4, 28, 28)

fig, axes = plt.subplots(1, 4, figsize=(12, 3))

for i in range(4):

    axes[i].imshow(
        feature_maps[i],
        cmap="gray"
    )

    axes[i].set_title(
        f"Feature {i}"
    )

    axes[i].axis("off")

plt.tight_layout()

plt.show()