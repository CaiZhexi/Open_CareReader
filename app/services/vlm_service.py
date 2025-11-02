"""
VLM (视觉语言模型) 服务
调用SiliconFlow的视觉语言模型API进行图文识别和理解
"""

import httpx
from typing import Optional, Dict, Any
from app.config import get_settings


class VLMService:
    """VLM服务类"""
    
    def __init__(self):
        self.settings = get_settings()
        
        # 根据provider选择API配置
        if self.settings.vlm_provider == "aliyun":
            self.api_url = f"{self.settings.aliyun_api_base}/chat/completions"
            self.api_key = self.settings.aliyun_api_key
        else:
            self.api_url = f"{self.settings.siliconflow_api_base}/chat/completions"
            self.api_key = self.settings.siliconflow_api_key
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def analyze_image(
        self, 
        image_url: str,
        prompt: Optional[str] = None,
        simplify: bool = True
    ) -> Dict[str, Any]:
        """
        分析图片内容
        
        Args:
            image_url: 图片URL或base64编码
            prompt: 自定义提示词
            simplify: 是否生成简明化说明
            
        Returns:
            分析结果
        """
        if prompt is None:
            if simplify:
                prompt = """请仔细分析这张图片中的所有文字内容，并完成以下任务：
1. 识别并提取图片中的所有文字
2. 用简单易懂的白话文解释这些内容的含义
3. 特别注意：请使用适合老年人理解的语言，避免使用专业术语
4. 如果有重要信息，请重点说明

请以清晰、友好的方式呈现结果。"""
            else:
                prompt = "请识别并提取这张图片中的所有文字内容。"
        
        payload = {
            "model": self.settings.vlm_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient(timeout=self.settings.api_timeout) as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            result = response.json()
            
            # 提取文本内容
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return {
                "success": True,
                "content": content,
                "model": self.settings.vlm_model,
                "raw_response": result
            }
    
    async def answer_question(
        self,
        question: str,
        context: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        回答用户问题
        
        Args:
            question: 用户问题
            context: 上下文信息
            image_url: 可选的图片URL
            
        Returns:
            回答结果
        """
        content = []
        
        # 构建消息内容
        if context:
            prompt_text = f"根据以下内容回答问题（请用简单易懂的话回答）：\n\n内容：{context}\n\n问题：{question}"
        else:
            prompt_text = f"请用简单易懂的话回答以下问题：{question}"
        
        content.append({"type": "text", "text": prompt_text})
        
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})
        
        payload = {
            "model": self.settings.vlm_model,
            "messages": [
                {
                    "role": "user",
                    "content": content if len(content) > 1 else prompt_text
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient(timeout=self.settings.api_timeout) as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            result = response.json()
            
            answer = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return {
                "success": True,
                "answer": answer,
                "model": self.settings.vlm_model,
                "raw_response": result
            }

