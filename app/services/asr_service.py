"""
ASR (语音识别) 服务
调用SiliconFlow的ASR API将语音转换为文字
"""

import httpx
from typing import Dict, Any, Union
from app.config import get_settings


class ASRService:
    """ASR服务类"""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_url = f"{self.settings.siliconflow_api_base}/audio/transcriptions"
        self.headers = {
            "Authorization": f"Bearer {self.settings.siliconflow_api_key}"
        }
    
    async def speech_to_text(
        self,
        audio_file: Union[bytes, str],
        language: str = "zh"
    ) -> Dict[str, Any]:
        """
        将语音转换为文字
        
        Args:
            audio_file: 音频文件路径或字节数据
            language: 语言代码（默认中文）
            
        Returns:
            识别结果
        """
        # 准备文件数据
        if isinstance(audio_file, bytes):
            files = {"file": ("audio.wav", audio_file, "audio/wav")}
        else:
            files = {"file": open(audio_file, "rb")}
        
        data = {
            "model": self.settings.asr_model,
            "language": language
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.settings.api_timeout) as client:
                response = await client.post(
                    self.api_url,
                    data=data,
                    files=files,
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                
                # 提取识别的文本
                text = result.get("text", "")
                
                return {
                    "success": True,
                    "text": text,
                    "model": self.settings.asr_model,
                    "language": language,
                    "raw_response": result
                }
        finally:
            # 如果是文件对象，确保关闭
            if isinstance(audio_file, str) and "file" in files:
                files["file"].close()
    
    async def transcribe_with_timestamps(
        self,
        audio_file: Union[bytes, str],
        language: str = "zh"
    ) -> Dict[str, Any]:
        """
        将语音转换为文字并返回时间戳信息
        
        Args:
            audio_file: 音频文件路径或字节数据
            language: 语言代码
            
        Returns:
            包含时间戳的识别结果
        """
        result = await self.speech_to_text(audio_file, language)
        
        # 这里可以根据API实际返回的格式提取时间戳信息
        # 当前版本先返回基本结果
        return result

