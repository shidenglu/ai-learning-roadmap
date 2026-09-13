# 安装 miniconda

Miniconda 是一个轻量级的 Python 环境和包管理工具。

# 通过 miniconda 创建一个 python 环境

conda create -n -y d2l-zh python=3.8 pip

# 安装需要的包

pip install -y jupyter d2l torch torchvision

# 下载代码并执行

wget https://zh-v2.d2l.ai/d2l-zh.zip
unzip d2l-zh.zip
jupyter notebook