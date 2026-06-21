import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs

# 1. 数据
X, y = make_blobs(n_samples=100, centers=2, random_state=6)

# 2. 模型
model = svm.SVC(kernel="linear", C=1.0)
model.fit(X, y)

# 3. 画图
plt.scatter(X[:,0], X[:,1], c=y)

# 支持向量
plt.scatter(model.support_vectors_[:,0],
            model.support_vectors_[:,1],
            s=100, facecolors='none', edgecolors='r')

# 分割线
w = model.coef_[0]
b = model.intercept_[0]

xx = np.linspace(min(X[:,0]), max(X[:,0]), 100)
yy = -(w[0]*xx + b) / w[1]

plt.plot(xx, yy, 'k-')

plt.title("SVM Demo with Support Vectors")
plt.show()