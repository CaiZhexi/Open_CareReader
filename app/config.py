"""
配置中心
统一管理所有配置项和环境变量
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # API配置
    siliconflow_api_key: str
    siliconflow_api_base: str = "https://api.siliconflow.cn/v1"
    
    # 阿里云百炼API配置
    aliyun_api_key: str = ""
    aliyun_api_base: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    # 模型配置
    vlm_model: str = "qwen-vl-plus"
    vlm_provider: str = "aliyun"  # 可选: aliyun 或 siliconflow
    tts_model: str = "IndexTeam/IndexTTS-2"
    asr_model: str = "FunAudioLLM/SenseVoiceSmall"
    
    # 服务器配置
    api_host: str = "0.0.0.0"
    api_port: int = 8080
    
    # 超时配置
    api_timeout: int = 180  # 增加到180秒以适应VLM处理时间
    
    # 适老化配置
    default_font_size: int = 18
    default_speech_rate: float = 0.8  # 语速放慢
    default_voice: str = "zh-CN-XiaoxiaoNeural"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（单例模式）"""
    return Settings()

