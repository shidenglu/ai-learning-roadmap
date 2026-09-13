import matplotlib.pyplot as plt

# Epoch
epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Loss
loss = [
    1.20,
    0.95,
    0.78,
    0.62,
    0.51,
    0.43,
    0.37,
    0.32,
    0.28,
    0.25
]

plt.plot(epochs, loss)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")

plt.grid()

plt.show()