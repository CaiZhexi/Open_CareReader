"""
CareReader Gradio前端界面
提供简洁易用、适老化设计的操作界面
"""

import gradio as gr
import base64
import asyncio
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.vlm_service import VLMService
from app.services.tts_service import TTSService
from app.services.asr_service import ASRService


# 初始化服务
vlm_service = VLMService()
tts_service = TTSService()
asr_service = ASRService()

# 全局变量存储当前分析结果
current_context = {"text": "", "image_base64": ""}


async def analyze_image_async(image):
    """分析图片（异步）"""
    if image is None:
        return "请先上传图片", None
    
    try:
        # 将图片转换为base64
        from PIL import Image
        import io
        
        # 如果是PIL Image对象
        if isinstance(image, Image.Image):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        else:
            # 如果是numpy数组或其他格式
            img = Image.fromarray(image)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # 构造图片URL
        image_url = f"data:image/png;base64,{image_base64}"
        
        # 调用VLM服务
        result = await vlm_service.analyze_image(
            image_url=image_url,
            simplify=True
        )
        
        content = result.get("content", "")
        
        # 保存到全局变量
        current_context["text"] = content
        current_context["image_base64"] = image_base64
        
        # 生成语音
        audio_data = await tts_service.text_to_speech(content)
        
        # 保存音频文件
        audio_path = "/tmp/carereader_speech.mp3"
        with open(audio_path, "wb") as f:
            f.write(audio_data)
        
        return content, audio_path
    
    except Exception as e:
        return f"分析失败: {str(e)}", None


def analyze_image(image):
    """分析图片（同步包装）"""
    return asyncio.run(analyze_image_async(image))


async def answer_question_async(audio):
    """回答语音问题（异步）"""
    if audio is None:
        return "请先录制语音提问", None
    
    try:
        # 读取音频文件
        with open(audio, "rb") as f:
            audio_data = f.read()
        
        # 调用ASR服务识别语音
        asr_result = await asr_service.speech_to_text(audio_data)
        question = asr_result.get("text", "")
        
        if not question:
            return "未识别到语音内容，请重新录制", None
        
        # 构造图片URL（如果有）
        image_url = None
        if current_context["image_base64"]:
            image_url = f"data:image/png;base64,{current_context['image_base64']}"
        
        # 调用VLM服务回答问题
        answer_result = await vlm_service.answer_question(
            question=question,
            context=current_context["text"],
            image_url=image_url
        )
        
        answer = answer_result.get("answer", "")
        response_text = f"您的问题：{question}\n\n回答：{answer}"
        
        # 生成语音回答
        audio_data = await tts_service.text_to_speech(answer)
        
        # 保存音频文件
        audio_path = "/tmp/carereader_answer.mp3"
        with open(audio_path, "wb") as f:
            f.write(audio_data)
        
        return response_text, audio_path
    
    except Exception as e:
        return f"回答失败: {str(e)}", None


def answer_question(audio):
    """回答语音问题（同步包装）"""
    return asyncio.run(answer_question_async(audio))


# 创建Gradio界面
with gr.Blocks(
    title="CareReader - AI助老读物",
    theme=gr.themes.Soft(
        primary_hue="blue",
        font=gr.themes.GoogleFont("Noto Sans SC")
    ),
    css="""
        .large-text { font-size: 20px !important; }
        .extra-large-text { font-size: 24px !important; }
        .main-button { height: 80px !important; font-size: 20px !important; }
    """
) as demo:
    
    gr.Markdown(
        """
        # CareReader - AI助老读物助手
        
        简单三步，轻松理解文档内容：
        1. 上传或拍摄文档图片
        2. 查看简明解释和听取语音朗读
        3. 有疑问？点击语音提问
        """,
        elem_classes=["extra-large-text"]
    )
    
    with gr.Tab("图片识别", elem_id="tab1"):
        gr.Markdown("### 第一步：上传图片", elem_classes=["large-text"])
        
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    label="上传或拍摄图片",
                    type="pil",
                    height=400
                )
                analyze_btn = gr.Button(
                    "开始识别和解释",
                    variant="primary",
                    elem_classes=["main-button"]
                )
            
            with gr.Column(scale=1):
                text_output = gr.Textbox(
                    label="识别结果和简明解释",
                    lines=15,
                    elem_classes=["large-text"]
                )
                audio_output = gr.Audio(
                    label="语音朗读",
                    type="filepath"
                )
        
        analyze_btn.click(
            fn=analyze_image,
            inputs=[image_input],
            outputs=[text_output, audio_output]
        )
    
    with gr.Tab("语音提问", elem_id="tab2"):
        gr.Markdown("### 有疑问？语音提问", elem_classes=["large-text"])
        gr.Markdown("先识别图片，然后录制您的问题，我会为您解答", elem_classes=["large-text"])
        
        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    label="录制您的问题",
                    type="filepath",
                    sources=["microphone"]
                )
                ask_btn = gr.Button(
                    "提交问题",
                    variant="primary",
                    elem_classes=["main-button"]
                )
            
            with gr.Column(scale=1):
                answer_output = gr.Textbox(
                    label="回答",
                    lines=15,
                    elem_classes=["large-text"]
                )
                answer_audio = gr.Audio(
                    label="语音回答",
                    type="filepath"
                )
        
        ask_btn.click(
            fn=answer_question,
            inputs=[audio_input],
            outputs=[answer_output, answer_audio]
        )
    
    gr.Markdown(
        """
        ---
        **使用提示**：
        - 确保图片清晰、文字可见
        - 语音提问时请说清楚、放慢语速
        - 点击播放按钮收听语音解释
        """,
        elem_classes=["large-text"]
    )


if __name__ == "__main__":
    import os
    # 禁用代理以避免网络超时
    os.environ['NO_PROXY'] = '*'
    os.environ['no_proxy'] = '*'
    
    demo.queue()  # 启用队列以提高稳定性
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=False,
        quiet=False,
        debug=False
    )

