import matplotlib.pyplot as plt
import numpy as np

plt.ion()

losses = []

for epoch in range(20):

    loss = np.exp(-epoch / 5)

    losses.append(loss)

    plt.clf()

    plt.plot(
        range(1, epoch + 2),
        losses
    )

    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    plt.title("Training")

    plt.grid()

    plt.pause(0.2)

plt.ioff()

plt.show()