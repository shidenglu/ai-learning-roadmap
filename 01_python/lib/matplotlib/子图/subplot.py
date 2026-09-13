import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5]

loss = [1.0, 0.8, 0.6, 0.45, 0.35]

accuracy = [0.50, 0.62, 0.72, 0.82, 0.88]

learning_rate = [
    0.01,
    0.01,
    0.005,
    0.005,
    0.001
]

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Loss
axes[0].plot(epochs, loss)
axes[0].set_title("Loss")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Loss")

# Accuracy
axes[1].plot(epochs, accuracy)
axes[1].set_title("Accuracy")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Accuracy")

# Learning Rate
axes[2].plot(epochs, learning_rate)
axes[2].set_title("Learning Rate")
axes[2].set_xlabel("Epoch")
axes[2].set_ylabel("LR")

plt.tight_layout()

plt.show()