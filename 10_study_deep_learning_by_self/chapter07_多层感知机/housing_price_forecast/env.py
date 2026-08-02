# check_env.py

import sys

import torch
import torchvision
import numpy
import pandas
import sklearn
import matplotlib

print("=" * 50)

print("Python      :", sys.version)

print("Torch       :", torch.__version__)

print("TorchVision :", torchvision.__version__)

print("NumPy       :", numpy.__version__)

print("Pandas      :", pandas.__version__)

print("Sklearn     :", sklearn.__version__)

print("Matplotlib  :", matplotlib.__version__)

print("=" * 50)

print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))