"""
TTS路由
处理文字转语音相关的API请求
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional

from app.services.tts_service import TTSService


router = APIRouter(prefix="/tts", tags=["TTS"])
tts_service = TTSService()


class TTSRequest(BaseModel):
    """TTS请求模型"""
    text: str
    voice: str = "S1"


@router.post("/speak")
async def text_to_speech(request: TTSRequest):
    """
    将文字转换为语音
    
    接收文字，返回音频数据
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="文字内容不能为空")
        
        # 调用TTS服务
        audio_data = await tts_service.text_to_speech(
            text=request.text,
            voice=request.voice
        )
        
        # 返回音频数据
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音合成失败: {str(e)}")


@router.post("/speak-metadata")
async def text_to_speech_with_metadata(request: TTSRequest):
    """
    将文字转换为语音并返回元数据
    
    返回包含音频数据和元信息的JSON响应
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="文字内容不能为空")
        
        # 调用TTS服务
        result = await tts_service.text_to_speech_with_metadata(
            text=request.text,
            voice=request.voice
        )
        
        # 将音频数据转换为base64
        import base64
        result["audio_base64"] = base64.b64encode(result["audio_data"]).decode("utf-8")
        del result["audio_data"]
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音合成失败: {str(e)}")


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "TTS"}

