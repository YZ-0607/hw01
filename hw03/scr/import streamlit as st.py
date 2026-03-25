import streamlit as st
import face_recognition
import numpy as np
from PIL import Image
import os

# -------------------------- 页面配置 --------------------------
st.set_page_config(
    page_title="人脸识别系统",
    page_icon="👤",
    layout="centered"
)
st.title("👤 人脸识别检测系统")
st.markdown("基于 face_recognition + Streamlit 实现的人脸检测与识别")

# -------------------------- 加载已知人脸库 --------------------------
# 创建已知人脸文件夹
KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# 缓存加载已知人脸，避免重复加载
@st.cache_resource
def load_known_faces():
    known_encodings = []
    known_names = []
    
    # 遍历人脸库图片
    for img_name in os.listdir(KNOWN_FACES_DIR):
        if img_name.endswith(("jpg", "jpeg", "png")):
            img_path = os.path.join(KNOWN_FACES_DIR, img_name)
            img = face_recognition.load_image_file(img_path)
            # 提取128维人脸特征编码
            face_enc = face_recognition.face_encodings(img)[0]
            
            # 文件名作为人名（如: zhangsan.jpg → zhangsan）
            name = os.path.splitext(img_name)[0]
            known_encodings.append(face_enc)
            known_names.append(name)
    
    return known_encodings, known_names

known_face_encodings, known_face_names = load_known_faces()

# -------------------------- 功能函数 --------------------------
def detect_faces(image):
    """人脸检测：返回人脸位置坐标"""
    face_locations = face_recognition.face_locations(image)
    return face_locations

def recognize_faces(image):
    """人脸识别：检测 + 特征比对 + 返回结果"""
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:
        # 与已知人脸库比对
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "未知人脸"
        
        # 取距离最小的匹配结果
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_idx = np.argmin(face_distances)
            if matches[best_match_idx]:
                name = known_face_names[best_match_idx]
        
        face_names.append(name)
    
    return face_locations, face_names

# -------------------------- 界面交互逻辑 --------------------------
# 选项卡：人脸检测 / 人脸识别
tab1, tab2 = st.tabs(["📷 人脸检测", "🔍 人脸识别"])

# 选项1：仅人脸检测
with tab1:
    st.subheader("人脸位置检测")
    uploaded_img = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"], key="detect")
    
    if uploaded_img is not None:
        img = Image.open(uploaded_img)
        img_np = np.array(img)
        
        # 检测人脸
        locations = detect_faces(img_np)
        st.success(f"检测到 {len(locations)} 张人脸")
        
        # 展示原图
        st.image(img, caption="上传图片", use_column_width=True)
        
        # 绘制人脸框
        img_draw = img.copy()
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img_draw)
        for top, right, bottom, left in locations:
            draw.rectangle([(left, top), (right, bottom)], outline="red", width=3)
        
        st.image(img_draw, caption="人脸检测结果", use_column_width=True)

# 选项2：人脸识别（带比对）
with tab2:
    st.subheader("人脸身份识别")
    st.info(f"已加载 {len(known_face_names)} 个已知人脸")
    uploaded_img2 = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"], key="recog")
    
    if uploaded_img2 is not None:
        img = Image.open(uploaded_img2)
        img_np = np.array(img)
        
        # 识别人脸
        locations, names = recognize_faces(img_np)
        
        # 绘制结果
        img_draw = img.copy()
        draw = ImageDraw.Draw(img_draw)
        for (top, right, bottom, left), name in zip(locations, names):
            # 画框
            draw.rectangle([(left, top), (right, bottom)], outline="blue", width=3)
            # 写名字
            draw.text((left, top-15), name, fill="blue")
        
        # 展示结果
        st.image(img_draw, caption="识别结果", use_column_width=True)
        
        # 输出文字结果
        st.markdown("### 识别结果")
        for i, name in enumerate(names):
            st.write(f"第 {i+1} 张人脸：**{name}**")