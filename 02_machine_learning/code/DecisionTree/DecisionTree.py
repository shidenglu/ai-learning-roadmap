import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

# ==========================================
# 1. 准备数据
# ==========================================
# 我们使用经典的鸢尾花(Iris)数据集，包含3种花，4个特征（花萼/花瓣的长宽）
iris = load_iris()
X = iris.data
y = iris.target

# 将数据分为训练集（80%）和测试集（20%）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 2. 训练决策树模型
# ==========================================
# 为了防止树长得太深导致“过拟合”，我们限制最大深度为 3 层
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# 查看在测试集上的准确率
score = model.score(X_test, y_test)
print(f"模型在测试集上的准确率: {score:.2%}")

# ==========================================
# 3. 决策树可视化（画出这棵树）
# ==========================================
plt.figure(figsize=(12, 8), dpi=100)

# 使用 plot_tree 函数绘制树状图
plot_tree(model, 
          feature_names=iris.feature_names,  # 传入特征名称，方便阅读
          class_names=iris.target_names,    # 传入类别名称（山鸢尾/变色鸢尾/维吉尼亚鸢尾）
          filled=True,                      # 填充颜色（颜色越深代表纯度越高）
          rounded=True,                     # 圆角边框
          fontsize=10)                      # 字体大小

plt.title("Decision Tree Visualization (Iris Dataset)", fontsize=14)
plt.show()