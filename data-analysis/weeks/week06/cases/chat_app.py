"""
学校大模型网关聊天 APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对应 notebook: ../llm_api.ipynb；测试脚本: swufe_llm_test.py
功能：侧栏选择模型（DeepSeek / GLM / Qwen）→ 多轮对话，流式输出

运行：streamlit run chat_app.py
前提：.env 中配置 SwufeModel_API_KEY（参考 .env.example）
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

CASES_DIR = Path(__file__).resolve().parent
# 优先读本目录 .env，再读仓库根目录 .env（默认不覆盖已加载的值）
load_dotenv(CASES_DIR / ".env")
load_dotenv(CASES_DIR.parents[3] / ".env")

BASE_URL = "http://llm.swufe.edu.cn/v1"

# 网关上现有的模型（模型名区分大小写，须完整复制）
MODELS = {
    "deepseek-ai/DeepSeek-V4-Flash-0731": "DeepSeek 文本对话",
    "ZhipuAI/GLM-5.2": "智谱 GLM 文本对话",
    "Qwen/Qwen3.8-Flash-Next": "通义 Qwen 文本对话",
    "Qwen/Qwen3-VL-32B": "通义 Qwen 多模态（支持图片输入，本网页只发文本）",
}
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731"


def get_api_key() -> str | None:
    """优先读 st.secrets（Streamlit Cloud），回退到环境变量（本地 .env）"""
    try:
        return st.secrets["SwufeModel_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.getenv("SwufeModel_API_KEY")


def stream_reply(model: str, messages: list[dict]):
    """流式调用模型，逐块产出回复文本（st.write_stream 需要生成器）"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    chunks = client.chat.completions.create(model=model, messages=messages, stream=True)
    for chunk in chunks:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# ══════════════════════════════════════════════════════
# Streamlit UI
# ══════════════════════════════════════════════════════

st.set_page_config(page_title="西财大模型聊天", page_icon="💬", layout="centered")
st.title("💬 西财大模型聊天")

API_KEY = get_api_key()
if not API_KEY:
    st.error("请在 .env 或 Streamlit Cloud Secrets 中配置 SwufeModel_API_KEY（参考 .env.example）")
    st.stop()

# ── 侧栏：选模型 + 系统提示词 + 清空 ──
with st.sidebar:
    st.header("设置")
    model = st.selectbox(
        "选择模型",
        list(MODELS),
        format_func=lambda m: f"{m}（{MODELS[m]}）",
    )
    system_prompt = st.text_input("系统提示词", value="你是人工智能助手")
    st.caption("切换模型不会清空对话：同一段历史发给不同模型，可以直接对比回答。")
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()

# ── 会话历史（存 session_state，rerun 后仍在） ──
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 输入 → 流式回复 ──
if prompt := st.chat_input("输入你的问题…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(
                stream_reply(
                    model,
                    [{"role": "system", "content": system_prompt}]
                    + st.session_state.messages,
                )
            )
        except Exception as e:
            reply = None
            st.error(f"调用失败：{e}")

    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
