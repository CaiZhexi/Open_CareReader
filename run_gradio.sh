#!/bin/bash

# CareReader Gradio启动脚本

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3.10 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "检查并安装依赖..."
pip install -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "错误：未找到.env文件"
    echo "请复制.env.example为.env并配置API密钥"
    exit 1
fi

# 启动Gradio应用
echo "启动CareReader Gradio界面..."
python ui/app_gradio.py

