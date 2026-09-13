import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

fig, ax = plt.subplots()

ax.plot(x, y)

ax.set_xlabel("X")
ax.set_ylabel("Y")

ax.set_title("y = x²")

ax.grid()

plt.show()