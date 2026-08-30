import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5]

loss = [1.0, 0.8, 0.6, 0.4, 0.3]

plt.plot(epochs, loss)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title("Training Loss")

plt.grid()

plt.savefig(
    "training_loss.png",
    dpi=300
)

plt.show()