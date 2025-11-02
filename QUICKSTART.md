# CareReader 快速入门指南

## 5分钟快速启动

### 方法1: 使用自动化脚本（推荐）

```bash
# 1. 进入项目目录
cd CareReader

# 2. 运行初始化脚本
python setup.py

# 3. 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate  # Windows

# 4. 启动Gradio界面
./run_gradio.sh  # Mac/Linux
# 或
python ui/app_gradio.py  # Windows
```

### 方法2: 手动配置

```bash
# 1. 创建虚拟环境
python3.10 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置API密钥
cp .env.example .env
# 编辑.env文件，填入你的API密钥

# 4. 启动应用
python ui/app_gradio.py
```

### 方法3: 使用Docker

```bash
# 1. 创建.env文件
cp .env.example .env
# 编辑.env文件，填入你的API密钥

# 2. 启动服务
docker-compose up gradio
```

## 使用教程

### 1. 图片识别

1. 打开浏览器访问 http://localhost:7860
2. 在"图片识别"标签页点击上传图片
3. 点击"开始识别和解释"按钮
4. 查看识别结果和简明解释
5. 点击播放按钮收听语音

### 2. 语音提问

1. 先完成图片识别（提供上下文）
2. 切换到"语音提问"标签页
3. 点击麦克风录制问题
4. 点击"提交问题"按钮
5. 查看和收听答案

## 常见问题

### Q: 提示API密钥错误？
A: 检查.env文件中的SILICONFLOW_API_KEY是否正确配置

### Q: 安装依赖失败？
A: 确保Python版本为3.10+，尝试升级pip：`pip install --upgrade pip`

### Q: 语音录制不工作？
A: 检查浏览器权限，确保允许麦克风访问

### Q: 图片识别很慢？
A: 这取决于网络速度和API响应时间，正常情况下3-5秒

## 端口说明

- Gradio界面：7860
- FastAPI服务：8080

## 获取API密钥

访问 [SiliconFlow](https://cloud.siliconflow.cn/) 注册账号并获取API密钥

## 技术支持

遇到问题？查看完整文档：README.md

