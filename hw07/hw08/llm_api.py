"""
大模型API封装模块
读取环境变量密钥，内置约束Prompt，仅允许基于检索文档回答
"""
import os
import requests

# 读取环境变量，不硬编码密钥
API_KEY = os.getenv("LLM_API_KEY", "YOUR_API_KEY_PLACEHOLDER")
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 约束提示词：强制模型只能使用提供的文档内容作答
BASE_PROMPT = """
你是文档答疑助手，仅能依据【参考文档片段】回答用户问题。
规则：
1. 如果参考文档无相关信息，直接回复：未在上传资料中找到相关内容
2. 回答需标注引用的原文片段，保证有据可依
3. 禁止编造文档不存在的信息，杜绝幻觉
4. 回答简洁清晰，专业易懂

【参考文档片段】：
{context_text}

用户问题：
{user_question}
"""

def get_llm_answer(context_text: str, user_question: str) -> str:
    """
    调用大模型接口生成回答
    :param context_text: RAG检索到的原文片段
    :param user_question: 用户输入提问
    :return: AI生成回答文本
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {
            "role": "user",
            "content": BASE_PROMPT.format(context_text=context_text, user_question=user_question)
        }
    ]
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.1
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        resp_json = resp.json()
        if "choices" in resp_json and len(resp_json["choices"]) > 0:
            return resp_json["choices"][0]["message"]["content"].strip()
        else:
            return f"接口返回异常：{resp_json}"
    except Exception as e:
        return f"大模型调用失败：{str(e)}"


def get_doc_summary(full_text: str) -> str:
    """
    文档全文摘要接口
    """
    summary_prompt = f"请对下面文档内容生成精简总结，控制在300字以内：\n{full_text}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": summary_prompt}],
        "temperature": 0.2
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    res = resp.json()
    return res["choices"][0]["message"]["content"].strip()