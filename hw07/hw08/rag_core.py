"""
RAG向量检索核心模块
文本切割、向量化、FAISS本地向量库存储、相似度召回
使用预训练嵌入模型 all-MiniLM-L6-v2
"""
import faiss
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
import os

# 向量库持久化文件
INDEX_PATH = "faiss_index.index"
TEXT_STORE_PATH = "text_store.pkl"

# 加载开源预训练向量嵌入AI模型
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=60,
    separators=["\n\n", "\n", "。", "，", " "]
)

# 全局向量库与文本存储
index = None
text_list = []

def init_vector_store():
    """初始化/加载本地向量库，不存在则新建"""
    global index, text_list
    if os.path.exists(INDEX_PATH) and os.path.exists(TEXT_STORE_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(TEXT_STORE_PATH, "rb") as f:
            text_list = pickle.load(f)
    else:
        dim = embed_model.get_sentence_embedding_dimension()
        index = faiss.IndexFlatL2(dim)
        text_list = []

def add_text_to_store(raw_text: str):
    """
    新增文档文本至向量库
    :param raw_text: PDF/OCR提取完整文本
    """
    global index, text_list
    chunks = text_splitter.split_text(raw_text)
    if len(chunks) == 0:
        return
    embeddings = embed_model.encode(chunks)
    index.add(np.array(embeddings).astype("float32"))
    text_list.extend(chunks)
    # 持久化保存
    faiss.write_index(index, INDEX_PATH)
    with open(TEXT_STORE_PATH, "wb") as f:
        pickle.dump(text_list, f)

def search_top_k(query: str, top_k=3) -> str:
    """
    用户问题向量化检索，返回拼接参考文本
    """
    global index, text_list
    if index is None or index.ntotal == 0:
        return ""
    query_emb = embed_model.encode([query])
    _, idx_array = index.search(np.array(query_emb).astype("float32"), top_k)
    res_text = ""
    for idx in idx_array[0]:
        if 0 <= idx < len(text_list):
            res_text += f"【片段】{text_list[idx]}\n\n"
    return res_text

def clear_all_store():
    """清空全部知识库向量数据"""
    global index, text_list
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(TEXT_STORE_PATH):
        os.remove(TEXT_STORE_PATH)
    init_vector_store()