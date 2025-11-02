# CareReader - AI助老读物应用

CareReader 是一款基于视觉语言模型 (VLM)、语音识别 (ASR) 与语音合成 (TTS) 技术的 AI 助老读物应用。通过拍照或上传图片，自动识别图中文字、简明化解释内容，并用语音进行朗读或回答老人语音提问，协助老年用户轻松理解信息。

## 功能特性

- **图片识别**：上传或拍摄文档图片，自动识别文字内容（**8秒内完成**）
- **智能解释**：将复杂内容转换为简单易懂的白话文（**适合老年人理解**）
- **语音朗读**：将识别结果转换为自然语音播放（**8种预置音色可选**）
- **语音提问**：通过语音提问，获得针对性解答（**实时响应**）
- **适老化设计**：大字体、高对比度、简单操作流程（**不超过3步**）

## 性能指标

| 功能 | 响应时间 | 状态 |
|------|----------|------|
| VLM图像识别 | 8-9秒 | ✓ 快速 |
| TTS语音合成(50字) | 1-2秒 | ✓ 快速 |
| 智能问答 | 1-2秒 | ✓ 实时 |
| **完整流程** | **13秒** | ✓ 优秀 |

## 技术架构

- **后端框架**：FastAPI - 高性能异步Web框架
- **前端界面**：Gradio - 快速构建交互式界面
- **视觉模型**：阿里云百炼 qwen-vl-plus - 视觉语言理解（**性能优异，响应快速**）
- **语音识别**：FunAudioLLM/SenseVoiceSmall (SiliconFlow) - 中文语音识别
- **语音合成**：FunAudioLLM/CosyVoice2-0.5B (SiliconFlow) - 自然语音合成
- **API提供商**：阿里云百炼（VLM）+ SiliconFlow（TTS/ASR）

## 项目结构

```
CareReader/
├── app/                      # 后端应用
│   ├── main.py              # FastAPI主入口
│   ├── config.py            # 配置管理
│   ├── routes/              # API路由
│   │   ├── vlm.py          # 视觉语言模型路由
│   │   ├── tts.py          # 语音合成路由
│   │   └── asr.py          # 语音识别路由
│   ├── services/            # 服务层
│   │   ├── vlm_service.py  # VLM服务
│   │   ├── tts_service.py  # TTS服务
│   │   └── asr_service.py  # ASR服务
│   └── utils/               # 工具函数
│       └── image_handler.py # 图片处理
├── ui/                       # 前端界面
│   └── app_gradio.py        # Gradio应用
├── requirements.txt          # Python依赖
├── Dockerfile               # Docker配置
├── .env.example             # 环境变量模板
└── README.md                # 项目说明

```

## 快速开始

### 前置要求

- Python 3.10+
- 阿里云百炼 API密钥（VLM）- [申请地址](https://bailian.console.aliyun.com/)
- SiliconFlow API密钥（TTS/ASR）- [申请地址](https://cloud.siliconflow.cn/)

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/your-username/CareReader.git
cd CareReader
```

2. **创建虚拟环境**

```bash
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 阿里云百炼 API Configuration (推荐用于VLM，速度快)
ALIYUN_API_KEY=your-aliyun-api-key-here
ALIYUN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1

# SiliconFlow API Configuration (用于TTS和ASR)
SILICONFLOW_API_KEY=your-siliconflow-api-key-here
SILICONFLOW_API_BASE=https://api.siliconflow.cn/v1

# Model Configuration
VLM_MODEL=qwen-vl-plus
VLM_PROVIDER=aliyun
TTS_MODEL=FunAudioLLM/CosyVoice2-0.5B
ASR_MODEL=FunAudioLLM/SenseVoiceSmall

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8080
```

**配置说明：**
- `VLM_PROVIDER`：可选 `aliyun`（推荐，速度快）或 `siliconflow`（准确率高）
- `ALIYUN_API_KEY`：从阿里云百炼获取，用于图像识别
- `SILICONFLOW_API_KEY`：从SiliconFlow获取，用于语音合成和识别

### 运行方式

#### 方式1：运行Gradio界面（推荐）

```bash
python ui/app_gradio.py
```

访问：`http://localhost:7860`

#### 方式2：运行FastAPI服务

```bash
python app/main.py
# 或
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

访问API文档：`http://localhost:8080/docs`

#### 方式3：使用Docker

```bash
# 构建镜像
docker build -t carereader .

# 运行容器（Gradio界面）
docker run -p 7860:7860 --env-file .env carereader

# 或运行API服务
docker run -p 8080:8080 --env-file .env carereader uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## 使用说明

### 1. 图片识别和解释

1. 在"图片识别"标签页上传或拍摄文档图片
2. 点击"开始识别和解释"按钮
3. 查看识别结果和简明解释
4. 点击播放按钮收听语音朗读

### 2. 语音提问

1. 先完成图片识别（提供上下文）
2. 切换到"语音提问"标签页
3. 点击麦克风录制您的问题
4. 点击"提交问题"获得解答
5. 收听语音回答

## API接口

### VLM接口

- `POST /vlm/analyze` - 分析图片内容
- `POST /vlm/analyze-upload` - 上传图片分析
- `POST /vlm/question` - 回答问题

### TTS接口

- `POST /tts/speak` - 文字转语音
- `POST /tts/speak-metadata` - 文字转语音（含元数据）

### ASR接口

- `POST /asr/transcribe` - 语音转文字
- `POST /asr/transcribe-upload` - 上传音频识别

详细API文档：启动服务后访问 `/docs`

## 配置说明

### 主要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `ALIYUN_API_KEY` | 阿里云百炼API密钥（VLM） | 必填 |
| `SILICONFLOW_API_KEY` | SiliconFlow API密钥（TTS/ASR） | 必填 |
| `VLM_PROVIDER` | VLM提供商 | `aliyun` |
| `VLM_MODEL` | 视觉语言模型 | `qwen-vl-plus` |
| `TTS_MODEL` | 语音合成模型 | `FunAudioLLM/CosyVoice2-0.5B` |
| `ASR_MODEL` | 语音识别模型 | `FunAudioLLM/SenseVoiceSmall` |
| `API_PORT` | API服务端口 | `8080` |

### 适老化配置

- 默认字体大小：18px
- 语速调整：0.8倍速（放慢）
- 高对比度界面
- 简化操作流程

## 性能优化

### VLM性能对比

通过使用阿里云百炼的 `qwen-vl-plus` 模型，相比SiliconFlow的 `Qwen3-VL-32B-Instruct`：

- **响应时间**：从32秒优化到8-9秒
- **性能提升**：**3.7倍快速**
- **识别准确率**：保持一致
- **成本**：更经济

### 完整流程性能

| 环节 | 耗时 | 占比 |
|------|------|------|
| 图片编码 | <0.1秒 | <1% |
| VLM图像识别 | 8-9秒 | 67% |
| TTS语音合成 | 2-3秒 | 23% |
| 智能问答 | 1-2秒 | 10% |
| **总计** | **13秒** | **100%** |

## 常见问题

### Q: 如何获取阿里云API密钥？

A: 访问 [阿里云百炼控制台](https://bailian.console.aliyun.com/) → API密钥管理 → 创建新密钥

### Q: 能否使用SiliconFlow进行VLM识别？

A: 可以！修改 `.env` 中的 `VLM_PROVIDER=siliconflow` 即可切换，但响应会较慢（32秒左右）

### Q: TTS音色如何选择？

A: 目前支持8种预置音色：
- **女声**：anna（沉稳）、bella（激情）、claire（温柔）、diana（欢快）
- **男声**：alex（沉稳）、benjamin（低沉）、charles（磁性）、david（欢快）

## 开发指南

### 添加新功能

1. 在 `app/services/` 中添加新的服务类
2. 在 `app/routes/` 中创建对应的路由
3. 在 `app/main.py` 中注册路由
4. 更新Gradio界面以支持新功能

### 测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest tests/
```

## 部署

### Hugging Face Spaces

1. 创建新的Gradio Space
2. 上传所有文件
3. 在Space设置中添加环境变量 `SILICONFLOW_API_KEY`
4. Space会自动部署并运行

### Docker部署

```bash
# 使用docker-compose
docker-compose up -d
```

### 云服务器部署

1. 安装依赖并配置环境
2. 使用systemd或supervisor管理进程
3. 配置Nginx反向代理
4. 启用HTTPS

## 注意事项

1. **API密钥安全**：不要将 `.env` 文件提交到Git仓库
2. **图片隐私**：图片仅用于临时推理，不会存储
3. **网络要求**：需要稳定的网络连接访问API服务
4. **浏览器兼容**：建议使用Chrome、Safari等现代浏览器

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 开源协议

本项目采用 MIT License 开源协议。详见 [LICENSE](LICENSE) 文件。

## 致谢

- 阿里云百炼提供的高效VLM服务
- SiliconFlow提供的优质TTS/ASR服务
- Qwen、FunAudioLLM等开源模型团队
- FastAPI和Gradio等优秀开源框架

---

**让AI技术更好地服务老年人，让信息获取更加便捷！**

