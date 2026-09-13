import matplotlib.pyplot as plt

x1 = [1, 2, 1.5, 2.5, 3]
y1 = [1, 1.5, 2, 2.5, 3]

x2 = [6, 7, 7.5, 8, 9]
y2 = [6, 7, 8, 7.5, 9]

plt.scatter(x1, y1, label="Class 0")
plt.scatter(x2, y2, label="Class 1")

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")

plt.title("Dataset Distribution")

plt.legend()
plt.grid()

plt.show()