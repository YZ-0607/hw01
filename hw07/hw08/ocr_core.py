"""
计算机视觉AI模块：PP-OCRv4本地图像文字识别
预训练模型离线推理，无需云端图片上传
"""
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

# 初始化OCR模型，只使用中文，关闭日志冗余输出
ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)

def image_to_text(pil_img: Image.Image) -> str:
    """
    输入PIL图像，返回识别拼接后的完整文本
    :param pil_img: 上传图片对象
    :return: 图片提取纯文本
    """
    # PIL转numpy数组适配OCR输入
    img_array = np.array(pil_img)
    result = ocr.ocr(img_array, cls=True)
    text_lines = []
    for page in result:
        if page is None:
            continue
        for line_info in page:
            text_content = line_info[1][0]
            text_lines.append(text_content)
    full_text = "\n".join(text_lines)
    return full_text.strip()