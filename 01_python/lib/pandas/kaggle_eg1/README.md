# 原始数据
Age  Salary  Gender  City       Buy
20   5000    M       Beijing     0
25   6000    F       Shanghai    1
30   7000    M       Beijing     1

# 经过Pandas
                    原始 CSV
                       │
                       ↓
                pd.read_csv()
                       │
                       ↓
                  DataFrame
                       │
            ┌──────────┴──────────┐
            ↓                     ↓
        查看数据                缺失值
      head/info              isnull()
                                  │
                                  ↓
                               fillna()
                                  │
                                  ↓
                             完整数据
                                  │
                                  ↓
                               drop()
                                  │
                                  ↓
                          删除无用的 Id
                                  │
                                  ↓
                         get_dummies()
                                  │
                                  ↓
                         类别 → 数字
                                  │
                                  ↓
                         X              y
                         │              │
                         ↓              ↓
                   train_test_split()
                         │
                  ┌──────┴──────┐
                  ↓             ↓
               train          test
                  │
                  ↓
              to_numpy()
                  │
                  ↓
                NumPy
                  │
                  ↓
             torch.tensor()
                  │
                  ↓
              Tensor
                  │
                  ↓
             神经网络