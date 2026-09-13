import numpy as np
import matplotlib.pyplot as plt

weights = np.random.randn(10000)

plt.hist(
    weights,
    bins=50
)

plt.xlabel("Weight")
plt.ylabel("Frequency")

plt.title("Weight Distribution")

plt.grid()

plt.show()