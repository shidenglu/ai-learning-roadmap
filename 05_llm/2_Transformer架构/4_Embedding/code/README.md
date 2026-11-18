1. 构造语料
   ↓
   king / queen / man / woman 等词组成训练句子

2. 建立词表
   ↓
   word → Token ID
   king → 0
   man  → 1
   ...

3. 构造训练数据
   ↓
   使用 Skip-Gram：
   中心词 → 上下文词

4. 创建 Embedding
   ↓
   Token ID → Embedding向量
   初始向量是随机的

5. 模型训练
   ↓
   Embedding → Linear → 预测上下文词
   ↓
   计算 Loss
   ↓
   反向传播
   ↓
   更新 Embedding

6. 得到训练后的词向量
   ↓
   king、man、woman、queen
   都变成具有语义关系的向量

7. 执行向量运算
   ↓
   King - Man + Woman
   ↓
   得到一个新的向量

8. 相似度搜索
   ↓
   新向量与所有词向量计算余弦相似度
   ↓
   找最接近的词
   ↓
   Queen