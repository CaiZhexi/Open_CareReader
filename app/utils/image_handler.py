"""
图片处理工具
处理图片上传、格式转换和编码
"""

import base64
from io import BytesIO
from PIL import Image
from typing import Union


def image_to_base64(image: Union[str, bytes, Image.Image]) -> str:
    """
    将图片转换为base64编码
    
    Args:
        image: 图片路径、字节数据或PIL Image对象
        
    Returns:
        base64编码的字符串
    """
    if isinstance(image, str):
        # 文件路径
        with open(image, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    elif isinstance(image, bytes):
        # 字节数据
        return base64.b64encode(image).decode("utf-8")
    elif isinstance(image, Image.Image):
        # PIL Image对象
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    else:
        raise ValueError("不支持的图片类型")


def validate_image(image_data: bytes) -> bool:
    """
    验证图片数据是否有效
    
    Args:
        image_data: 图片字节数据
        
    Returns:
        是否为有效图片
    """
    try:
        img = Image.open(BytesIO(image_data))
        img.verify()
        return True
    except Exception:
        return False


def resize_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    """
    调整图片大小以优化API请求
    
    Args:
        image: PIL Image对象
        max_size: 最大尺寸
        
    Returns:
        调整后的图片
    """
    width, height = image.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    return image


def compress_image_to_base64(image_path: str, max_size: int = 1024, quality: int = 85) -> str:
    """
    压缩图片并转换为base64编码（优化API请求速度）
    
    Args:
        image_path: 图片路径
        max_size: 最大边长（像素）
        quality: JPEG质量（1-100）
        
    Returns:
        data URL格式的base64字符串
    """
    from io import BytesIO
    
    # 打开图片
    img = Image.open(image_path)
    
    # 转换为RGB（如果是RGBA）
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # 调整大小
    img = resize_image(img, max_size)
    
    # 压缩为JPEG
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=quality, optimize=True)
    
    # Base64编码
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/jpeg;base64,{img_base64}"

