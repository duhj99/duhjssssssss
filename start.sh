#!/bin/bash

# 进入后端目录
cd backend

# 检查是否已安装依赖
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "安装依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 启动服务器
echo "启动批量工具箱服务器..."
python app.py