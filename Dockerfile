# CareReader Dockerfile
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/
COPY ui/ ./ui/

# 创建必要的目录
RUN mkdir -p /tmp

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 8080
EXPOSE 7860

# 启动命令（可以选择启动API或Gradio）
# 默认启动Gradio界面
CMD ["python", "ui/app_gradio.py"]

# 如果要启动API服务，使用以下命令：
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

