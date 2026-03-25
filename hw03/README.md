# 人脸识别作业 hw03
基于 face_recognition + Streamlit 实现的人脸检测与识别系统

## 环境配置
1. 安装 Python 3.11
2. 安装依赖：
pip install -r requirements.txt

## 运行方式
streamlit run src/face_app.py

## 功能说明
1. 人脸检测：检测图片中的所有人脸并框选
2. 人脸识别：与已知人脸库比对，输出姓名
3. 提取 128 维人脸特征，基于 dlib 实现