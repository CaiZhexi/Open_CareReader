"""
VLM路由
处理图像识别和问答相关的API请求
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import base64

from app.services.vlm_service import VLMService
from app.utils.image_handler import validate_image


router = APIRouter(prefix="/vlm", tags=["VLM"])
vlm_service = VLMService()


class AnalyzeImageRequest(BaseModel):
    """图片分析请求模型"""
    image_base64: str
    prompt: Optional[str] = None
    simplify: bool = True


class QuestionRequest(BaseModel):
    """问答请求模型"""
    question: str
    context: Optional[str] = None
    image_base64: Optional[str] = None


@router.post("/analyze")
async def analyze_image(request: AnalyzeImageRequest):
    """
    分析图片内容
    
    接收base64编码的图片，返回识别和解释结果
    """
    try:
        # 验证图片数据
        image_data = base64.b64decode(request.image_base64)
        if not validate_image(image_data):
            raise HTTPException(status_code=400, detail="无效的图片数据")
        
        # 构造图片URL（data URL格式）
        image_url = f"data:image/jpeg;base64,{request.image_base64}"
        
        # 调用VLM服务
        result = await vlm_service.analyze_image(
            image_url=image_url,
            prompt=request.prompt,
            simplify=request.simplify
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.post("/analyze-upload")
async def analyze_uploaded_image(
    file: UploadFile = File(...),
    prompt: Optional[str] = Form(None),
    simplify: bool = Form(True)
):
    """
    分析上传的图片文件
    
    接收文件上传，返回识别和解释结果
    """
    try:
        # 读取文件内容
        image_data = await file.read()
        
        # 验证图片
        if not validate_image(image_data):
            raise HTTPException(status_code=400, detail="无效的图片文件")
        
        # 转换为base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        # 调用VLM服务
        result = await vlm_service.analyze_image(
            image_url=image_url,
            prompt=prompt,
            simplify=simplify
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.post("/question")
async def answer_question(request: QuestionRequest):
    """
    回答用户问题
    
    基于上下文或图片内容回答问题
    """
    try:
        # 构造图片URL（如果提供）
        image_url = None
        if request.image_base64:
            image_url = f"data:image/jpeg;base64,{request.image_base64}"
        
        # 调用VLM服务
        result = await vlm_service.answer_question(
            question=request.question,
            context=request.context,
            image_url=image_url
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回答失败: {str(e)}")


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "VLM"}

