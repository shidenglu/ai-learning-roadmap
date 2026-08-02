# 检擦 torch 是否可以使用 GPU
import torch
a = torch.ones((3,1))
a = a.cuda(0)
b = torch.ones((3,1))
b = b.cuda(0)
a + b