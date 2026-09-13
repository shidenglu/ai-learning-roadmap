import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

train_loss = [
    1.20, 0.90, 0.70, 0.55, 0.45,
    0.38, 0.32, 0.28, 0.25, 0.22
]

val_loss = [
    1.30, 1.00, 0.82, 0.70, 0.63,
    0.60, 0.61, 0.64, 0.68, 0.72
]

plt.plot(
    epochs,
    train_loss,
    label="Train Loss"
)

plt.plot(
    epochs,
    val_loss,
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title("Training and Validation Loss")

plt.legend()
plt.grid()

plt.show()