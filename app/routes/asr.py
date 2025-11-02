"""
ASR路由
处理语音识别相关的API请求
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import base64

from app.services.asr_service import ASRService


router = APIRouter(prefix="/asr", tags=["ASR"])
asr_service = ASRService()


class ASRRequest(BaseModel):
    """ASR请求模型"""
    audio_base64: str
    language: str = "zh"


@router.post("/transcribe")
async def speech_to_text(request: ASRRequest):
    """
    将语音转换为文字
    
    接收base64编码的音频，返回识别结果
    """
    try:
        # 解码音频数据
        audio_data = base64.b64decode(request.audio_base64)
        
        # 调用ASR服务
        result = await asr_service.speech_to_text(
            audio_file=audio_data,
            language=request.language
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音识别失败: {str(e)}")


@router.post("/transcribe-upload")
async def transcribe_uploaded_audio(
    file: UploadFile = File(...),
    language: str = Form("zh")
):
    """
    识别上传的音频文件
    
    接收文件上传，返回识别结果
    """
    try:
        # 读取文件内容
        audio_data = await file.read()
        
        # 验证文件大小（限制为10MB）
        if len(audio_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="音频文件过大，请限制在10MB以内")
        
        # 调用ASR服务
        result = await asr_service.speech_to_text(
            audio_file=audio_data,
            language=language
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音识别失败: {str(e)}")


@router.post("/transcribe-timestamps")
async def transcribe_with_timestamps(request: ASRRequest):
    """
    将语音转换为文字并返回时间戳
    
    接收base64编码的音频，返回带时间戳的识别结果
    """
    try:
        # 解码音频数据
        audio_data = base64.b64decode(request.audio_base64)
        
        # 调用ASR服务
        result = await asr_service.transcribe_with_timestamps(
            audio_file=audio_data,
            language=request.language
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音识别失败: {str(e)}")


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "ASR"}

