"""
股价波动预测 APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对应 notebook: weeks/week07/streamlit.ipynb
功能：输入股票代码 → tushare 取近5日指标 → DeepSeek 7步预测 → 概率图示 + 分析原因

运行：streamlit run app.py
前提：.env 中配置 TUSHARE_TOKEN 和 DEEPSEEK_API_KEY
"""

import os
import re
import json

import pandas as pd
import plotly.express as px
import streamlit as st
import tushare as ts
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # 本地读 .env（云端无此文件，静默跳过）


def get_secret(key: str) -> str:
    """优先读 st.secrets（Streamlit Cloud），回退到环境变量（本地 .env）"""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)


TUSHARE_TOKEN = get_secret("TUSHARE_TOKEN")
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")

# ── 预设股票列表（侧栏 selectbox 用） ──
STOCKS = {
    "000001.SZ": "平安银行",
    "600519.SH": "贵州茅台",
    "000858.SZ": "五粮液",
    "002594.SZ": "比亚迪",
    "688012.SH": "中微公司",
    "688825.SH": "长鑫科技",
    "688836.SH": "宇树科技",
}


# ── 对应 notebook「获取多天的指标数据」 ──
# 循环取数 + 容错跳过是接 API 的通用套路
@st.cache_data(ttl=3600)
def fetch_daily_basic(ts_code: str, days: int = 5) -> pd.DataFrame:
    """从 tushare 取近 days 天的每日指标（换手率/量比/PE/PB）"""
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()

    today = pd.Timestamp.now()
    result = pd.DataFrame()

    for i in range(days * 2):  # 多取几天，容错非交易日
        target_date = today - pd.Timedelta(days=i)
        trade_date = target_date.strftime("%Y%m%d")

        try:
            daily_data = pro.daily_basic(
                ts_code=ts_code,
                trade_date=trade_date,
                fields="ts_code,trade_date,turnover_rate,volume_ratio,pe,pb",
            )
            if daily_data is not None and not daily_data.empty:
                if not daily_data.isna().all().all():
                    result = pd.concat([result, daily_data], ignore_index=True)
        except Exception:
            continue

        if len(result) >= days:
            break

    return result.head(days)


# ── 对应 notebook「chat with AI」 ──
# DeepSeek 兼容 OpenAI 接口：换厂商只需改 base_url、模型名和 API Key 环境变量
def llm_chat(prompt: str) -> str:
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=DEEPSEEK_API_KEY,
    )
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


# ── 对应 notebook「构造预测prompt，并预测」 ──
# 7步指令：重述问题 → 正反理由及强度 → 聚合 → 初始概率 → 反思 → 最终JSON
def build_prompt(firm_name: str, df: pd.DataFrame) -> str:
    question = (
        f"will future price of this stock {firm_name} "
        "moves up or down in the subsequent fifth trading day?"
    )
    resolution_criteria = (
        "预测的判断标准：股票价格在随后的第五个交易日是否高于或低于当前价格。"
    )
    materials = str(df.to_dict(orient="records"))

    return f"""
    You are an expert in future event prediction.
        - Question:{question}
        - Resolution Criteria:{resolution_criteria}

    We have retrieved the following Materials for this question (Special Note: Some indicators in the materials may be percentages (%) and not decimals):
        - Materials: {materials}

    Solve the problem(question) step by step as required by the intructions.

    Instructions:
       1. Given the above question, rephrase and expand it to help you do better answering. Maintain all information in the original question.
    {{ Insert rephrased and expanded question. }}
       2. Based on the materials provided, extract and provide a few reasons why the answer might be in each option (i.e., stock price moves up or moves down). Rate the strength of each reason for each option.
    {{ Insert your thoughts }}
       3. Based on the materials provided, extract and provide a few reasons why the answer might be not in each option (i.e., stock price moves up or moves down). Rate the strength of each reason for each option.
    {{ Insert your thoughts }}
       4. Aggregate your considerations. Think like a superforecaster (e.g. Nate Silver).
    {{ Insert your aggregated considerations }}
       5. Output an initial probability (prediction) given steps 1-4.
    {{ Insert initial probability,  do not ouput initial probability in JSON format}}
       6. Reflect, and evaluate whether your calculated probability is excessively confident or not confident enough. Also, consider anything else that might affect the forecast that you did not before consider (e.g. base rate of the event).
    {{ Insert your thoughts }}
       7. Output your final probability prediction (the sum of up and down probabilities must equal to 1).
    {{ Insert your answer, your final prediction must be in JSON format with keys: up and down }}
      8. 回答问题用中文。
"""


# ── 对应 notebook「从返回的response中提取json数据」 ──
# 程序化消费 AI 输出的第一步：用正则从长文本中抠出 JSON
def extract_json(response: str) -> dict:
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if not match:
        raise ValueError("未在响应中找到 JSON 数据")
    return json.loads(match.group())


# ══════════════════════════════════════════════════════
# Streamlit UI
# ══════════════════════════════════════════════════════

st.set_page_config(page_title="股价波动预测", layout="wide")
st.title("股价波动预测 APP")

# 检查密钥
if not TUSHARE_TOKEN:
    st.error("请在 .env 或 Streamlit Cloud Secrets 中配置 TUSHARE_TOKEN（参考 .env.example）")
    st.stop()
if not DEEPSEEK_API_KEY:
    st.error("请在 .env 或 Streamlit Cloud Secrets 中配置 DEEPSEEK_API_KEY（参考 .env.example）")
    st.stop()

# ── 侧栏：选股票 + 触发预测 ──
with st.sidebar:
    st.header("选择股票")

    # 预设列表 + 自由输入
    stock_options = [f"{code} {name}" for code, name in STOCKS.items()]
    selected = st.selectbox("预设股票", stock_options)

    # 从预设中拆出 ts_code 和 firm_name
    preset_ts_code = selected.split()[0]
    preset_name = STOCKS.get(preset_ts_code, "")

    # 自由输入（覆盖预设）
    custom_input = st.text_input(
        "或输入其他 ts_code（如 300750.SZ）",
        placeholder=f"留空则用预设：{preset_ts_code}",
    )

    if custom_input.strip():
        ts_code = custom_input.strip()
        firm_name = custom_input.strip()
    else:
        ts_code = preset_ts_code
        firm_name = preset_name

    st.divider()
    predict_btn = st.button("🔮 开始预测", type="primary")

# ── 主区域：预测流程 ──
if predict_btn:
    # ① 取数
    with st.spinner(f"正在获取 {firm_name}（{ts_code}）近5日指标…"):
        df = fetch_daily_basic(ts_code, days=5)

    if df.empty:
        st.warning("未取到数据，可能是非交易日或该股票尚无 daily_basic 数据。")
        st.stop()

    st.subheader("① 近5日指标数据")
    st.dataframe(df, width="stretch")
    st.caption("字段：turnover_rate 换手率 · volume_ratio 量比 · pe 市盈率 · pb 市净率")

    # ② 调用 LLM 预测
    with st.spinner("AI 正在分析，请稍候（7步推理约需 10-30 秒）…"):
        prompt = build_prompt(firm_name, df)
        answer = llm_chat(prompt)

    try:
        prediction = extract_json(answer)
    except ValueError:
        st.error("未能从 AI 回复中提取概率 JSON，下方为完整回复供检查。")
        st.text(answer)
        st.stop()

    up_prob = prediction.get("up", 0)
    down_prob = prediction.get("down", 0)

    # ── 概率图示：plotly 横向条形图 ──
    st.subheader("② 预测概率")

    prob_df = pd.DataFrame(
        {
            "方向": ["上涨 (up)", "下跌 (down)"],
            "概率": [up_prob, down_prob],
        }
    )

    color_map = {"上涨 (up)": "#22c55e", "下跌 (down)": "#ef4444"}

    fig = px.bar(
        prob_df,
        x="概率",
        y="方向",
        orientation="h",
        text=prob_df["概率"].apply(lambda v: f"{v:.1%}"),
        color="方向",
        color_discrete_map=color_map,
        range_x=[0, 1],
        title=f"{firm_name} 未来第五个交易日涨跌概率",
    )
    fig.update_traces(textposition="outside", showlegend=False)
    fig.update_layout(
        yaxis_title="",
        xaxis_title="概率",
        xaxis_tickformat=".0%",
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 结论
    if up_prob > down_prob:
        conclusion = f"倾向上涨（{up_prob:.1%}）"
        st.metric("结论", conclusion)
    else:
        conclusion = f"倾向下跌（{down_prob:.1%}）"
        st.metric("结论", conclusion)

    # ③ 分析原因
    st.subheader("③ 分析原因")
    with st.expander("展开 AI 完整分析过程（7步推理）", expanded=True):
        st.markdown(answer)

else:
    st.info("👈 在左侧选择股票后点击「开始预测」")
