import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# =========================
# 1. 加载数据
# =========================
data = load_breast_cancer()

X = data.data
y = data.target

print("数据维度:", X.shape)
print("类别:", np.unique(y))

# =========================
# 2. 切分训练集/测试集
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# 3. 建立随机森林模型
# =========================
model = RandomForestClassifier(
    n_estimators=100,   # 100棵树
    max_depth=10,
    random_state=42
)

# =========================
# 4. 训练模型
# =========================
model.fit(X_train, y_train)

# =========================
# 5. 预测
# =========================
y_pred = model.predict(X_test)

# =========================
# 6. 评估
# =========================
acc = accuracy_score(y_test, y_pred)

print("\n准确率:", acc)

print("\n混淆矩阵:")
print(confusion_matrix(y_test, y_pred))

print("\n分类报告:")
print(classification_report(y_test, y_pred))

# =========================
# 7. 特征重要性
# =========================
importances = model.feature_importances_

# 排序输出Top10
indices = np.argsort(importances)[::-1]

print("\nTop10重要特征:")
for i in range(10):
    idx = indices[i]
    print(f"{data.feature_names[idx]}: {importances[idx]:.4f}")