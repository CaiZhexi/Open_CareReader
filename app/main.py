"""
CareReader - FastAPI主入口
AI助老读物应用后端服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routes import vlm, tts, asr


# 创建FastAPI应用
app = FastAPI(
    title="CareReader API",
    description="基于VLM、ASR和TTS技术的AI助老读物应用",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(vlm.router)
app.include_router(tts.router)
app.include_router(asr.router)


@app.get("/")
async def root():
    """API根路径"""
    return {
        "name": "CareReader API",
        "version": "0.1.0",
        "description": "AI助老读物应用",
        "endpoints": {
            "docs": "/docs",
            "vlm": "/vlm",
            "tts": "/tts",
            "asr": "/asr"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    settings = get_settings()
    return {
        "status": "ok",
        "version": "0.1.0",
        "models": {
            "vlm": settings.vlm_model,
            "tts": settings.tts_model,
            "asr": settings.asr_model
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "message": "服务器内部错误"
        }
    )


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

