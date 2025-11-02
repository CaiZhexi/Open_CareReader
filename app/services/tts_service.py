"""
TTS (文字转语音) 服务
调用SiliconFlow的TTS API将文字转换为语音
"""

import httpx
from typing import Dict, Any
from app.config import get_settings


class TTSService:
    """TTS服务类"""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_url = f"{self.settings.siliconflow_api_base}/audio/speech"
        self.headers = {
            "Authorization": f"Bearer {self.settings.siliconflow_api_key}",
            "Content-Type": "application/json"
        }
    
    async def text_to_speech(
        self,
        text: str,
        voice: str = "claire"  # claire是温柔女声，适合老年人
    ) -> bytes:
        """
        将文字转换为语音
        
        Args:
            text: 要转换的文字
            voice: 说话人音色（默认claire-温柔女声）
                  可选：alex, benjamin, charles, david（男声）
                       anna, bella, claire, diana（女声）
            
        Returns:
            音频数据（字节）
        """
        # CosyVoice2-0.5B使用系统预置音色格式：model:voice
        voice_id = f"{self.settings.tts_model}:{voice}"
        
        payload = {
            "model": self.settings.tts_model,
            "input": text,  # 直接使用文本，不需要特殊格式
            "voice": voice_id,  # 使用系统预置音色
            "response_format": "mp3"
        }
        
        async with httpx.AsyncClient(timeout=self.settings.api_timeout) as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            # 检查响应是否为音频数据
            content_type = response.headers.get("content-type", "")
            
            if "audio" in content_type or "octet-stream" in content_type:
                # 直接返回音频字节
                return response.content
            else:
                # 可能是JSON响应，需要进一步处理
                result = response.json()
                # 根据API实际响应格式调整
                if "audio" in result:
                    import base64
                    return base64.b64decode(result["audio"])
                else:
                    raise ValueError(f"未知的响应格式: {result}")
    
    async def text_to_speech_with_metadata(
        self,
        text: str,
        voice: str = "S1"
    ) -> Dict[str, Any]:
        """
        将文字转换为语音并返回元数据
        
        Args:
            text: 要转换的文字
            voice: 说话人标识
            
        Returns:
            包含音频数据和元数据的字典
        """
        audio_data = await self.text_to_speech(text, voice)
        
        return {
            "success": True,
            "audio_data": audio_data,
            "text": text,
            "voice": voice,
            "model": self.settings.tts_model,
            "audio_length": len(audio_data)
        }

