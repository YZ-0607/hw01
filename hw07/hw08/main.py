"""
Web主界面入口 Streamlit
整合OCR、RAG、大模型全套AI能力，持续交互页面
"""
import streamlit as st
from PIL import Image
import PyPDF2
from ocr_core import image_to_text
from rag_core import init_vector_store, add_text_to_store, search_top_k, clear_all_store
from llm_api import get_llm_answer, get_doc_summary

# 页面基础配置
st.set_page_config(page_title="多模态文档智能助手", layout="wide")
st.title("📚 多模态文档智能AI助手（OCR+RAG+大模型）")

# 初始化向量库
if "init_flag" not in st.session_state:
    init_vector_store()
    st.session_state["init_flag"] = True

# 侧边栏功能区
with st.sidebar:
    st.header("功能面板")
    upload_file = st.file_uploader("上传PDF / 图片(jpg/png)", type=["pdf", "png", "jpg", "jpeg"])
    clear_btn = st.button("清空全部知识库")
    if clear_btn:
        clear_all_store()
        st.success("知识库已清空！")

# 文件解析逻辑
full_doc_text = ""
if upload_file is not None:
    file_name = upload_file.name
    st.subheader(f"已上传文件：{file_name}")
    if file_name.endswith(".pdf"):
        # PDF解析
        pdf_reader = PyPDF2.PdfReader(upload_file)
        all_pages_text = ""
        for page in pdf_reader.pages:
            page_txt = page.extract_text()
            if page_txt:
                all_pages_text += page_txt + "\n"
        full_doc_text = all_pages_text
        st.text_area("PDF提取预览", full_doc_text, height=200)
    else:
        # 图片OCR视觉AI处理
        img = Image.open(upload_file)
        st.image(img, width=400)
        ocr_result = image_to_text(img)
        full_doc_text = ocr_result
        st.text_area("OCR识别文字预览", full_doc_text, height=200)

    # 存入向量知识库
    if st.button("加入AI知识库"):
        if full_doc_text.strip() != "":
            add_text_to_store(full_doc_text)
            st.success("✅ 文件已存入向量知识库，可提问！")
        else:
            st.warning("未识别到有效文本，无法入库")

# 文档一键摘要
if full_doc_text.strip():
    if st.button("生成文档AI摘要"):
        with st.spinner("大模型正在总结文档..."):
            summary = get_doc_summary(full_doc_text)
            st.subheader("📄 文档摘要")
            st.write(summary)

# 对话问答区域
st.divider()
st.subheader("💬 基于私有知识库提问")
user_query = st.text_input("输入你的问题：")
if user_query:
    with st.spinner("AI检索知识库并生成回答..."):
        ref_context = search_top_k(user_query, top_k=3)
        answer = get_llm_answer(ref_context, user_query)
    st.subheader("AI回答")
    st.write(answer)
    with st.expander("查看检索到的原文参考片段"):
        st.write(ref_context if ref_context else "知识库暂无内容，请先上传文件")