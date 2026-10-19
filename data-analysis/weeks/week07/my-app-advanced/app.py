"""
股价波动预测 APP（进阶版）— Week07 升级篇配套成品
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对应实验文档: weeks/week07/week07-streamlit-app-advanced.md
结构 = 文档四步：
  步骤 1  extract_json 提取概率（契约在 prompt，兜底在代码）
  步骤 2  侧栏 + 按钮 + 全链路编排骨架（fetch_daily_basic / llm_chat / build_prompt 为基础篇旧零件）
  步骤 3  AI 按"保留函数不动，只写 UI 编排"的约束组装
  步骤 4  验收清单全覆盖：换股票复跑 / 未点击引导 / 失败不崩
进阶挑战已内置：@st.cache_data 缓存（挑战 5）、plotly 概率条形图
（对照成品：weeks/week07/cases/app.py）

运行：streamlit run app.py
前提：.env 中配置 TUSHARE_TOKEN 和 DEEPSEEK_API_KEY
"""

import json
import os
import re

import pandas as pd
import plotly.express as px
import streamlit as st
import tushare as ts
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # 本地读 .env（云端无此文件，静默跳过）

TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ── 预设股票列表（侧栏 selectbox 用；与 prices/名称对齐） ──
STOCKS = {
    "000001.SZ": "平安银行",
    "600519.SH": "贵州茅台",
    "002594.SZ": "比亚迪",
    "300750.SZ": "宁德时代",
}


# ══════════════════════════════════════════════════════
# 旧零件（基础篇已跑通，组装时保留不动）
# ══════════════════════════════════════════════════════

# ── 基础篇 2.2：每日指标（预测的原材料）──
# 进阶挑战 5：@st.cache_data 缓存——同一股票 1 小时内重复查询不重复取数，省 API 次数
@st.cache_data(ttl=3600)
def fetch_daily_basic(ts_code: str, days: int = 5) -> pd.DataFrame:
    """从 tushare 取近 days 天的每日指标（换手率/量比/PE/PB），循环取数 + 容错跳过"""
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()

    today = pd.Timestamp.now()
    result = pd.DataFrame()

    for i in range(days * 2):  # 多倒推几天，容错非交易日
        trade_date = (today - pd.Timedelta(days=i)).strftime("%Y%m%d")
        try:
            daily = pro.daily_basic(
                ts_code=ts_code,
                trade_date=trade_date,
                fields="ts_code,trade_date,turnover_rate,volume_ratio,pe,pb",
            )
            if not daily.empty:
                result = pd.concat([result, daily], ignore_index=True)
        except Exception:
            continue
        if len(result) >= days:
            break

    return result.head(days)


# ── 基础篇 2.3：大模型对话（先 hello 再谈业务的就是它）──
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


# ── 基础篇 2.4：预测 prompt（三要素 + 输出规范）──
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


# ── 升级篇步骤 1：提取 JSON（契约在 prompt，兜底在代码）──
def extract_json(response: str) -> dict:
    """正则从长文本中抠出 JSON；抠不到明确报错，别让下游拿着 None 崩得更远"""
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if not match:
        raise ValueError("未在响应中找到 JSON 数据")
    return json.loads(match.group())


# ══════════════════════════════════════════════════════
# UI 编排（升级篇步骤 2 的骨架 + 步骤 3 AI 填充）
# ══════════════════════════════════════════════════════

st.set_page_config(page_title="股价波动预测（进阶版）", layout="wide")
st.title("股价波动预测 APP（进阶版）")
st.caption("升级篇配套成品 · 侧栏选股票 → 点按钮 → 自动取数 → AI 预测 → 概率展示")

# ── 验收点：密钥缺失要有合理表现，不崩 ──
if not TUSHARE_TOKEN:
    st.error("请在 my-app-advanced/.env 中配置 TUSHARE_TOKEN（公用 token 见实验文档 2.1）")
    st.stop()
if not DEEPSEEK_API_KEY:
    st.error("请在 my-app-advanced/.env 中配置 DEEPSEEK_API_KEY")
    st.stop()

# ── 骨架 ①：侧栏放选择和触发 ──
with st.sidebar:
    st.header("选择股票")

    stock_options = [f"{code} {name}" for code, name in STOCKS.items()]
    selected = st.selectbox("预设股票", stock_options)
    code, name = selected.split()

    st.divider()
    # ── 骨架 ②：按钮触发（贵的操作让用户主动触发） ──
    predict_btn = st.button("🔮 开始预测", type="primary")

# ── 验收点：按钮没点时页面不报错，给引导 ──
if not predict_btn:
    st.info("👈 在左侧选择股票后点击「开始预测」")
    st.stop()

# ── 骨架 ③：取数（失败不崩） ──
with st.spinner(f"正在获取 {name}（{code}）近 5 日指标…"):
    df = fetch_daily_basic(code, days=5)

if df.empty:
    st.warning("未取到数据：可能是非交易日、该股票暂无 daily_basic 数据，或 token 限频。稍后重试或换个时段。")
    st.stop()

st.subheader("① 近 5 日指标（预测的原材料）")
st.dataframe(df, width="stretch")
st.caption("字段：turnover_rate 换手率 · volume_ratio 量比 · pe 市盈率 · pb 市净率")

# ── 骨架 ④⑤：预测（spinner 等待反馈，不是死寂） ──
with st.spinner("AI 正在分析，请稍候（约 10-30 秒）…"):
    prompt = build_prompt(name, df)
    answer = llm_chat(prompt)

# ── 骨架 ⑥ + 验收点：提取失败不崩，展示原始回复供检查 ──
try:
    prediction = extract_json(answer)
except (ValueError, json.JSONDecodeError):
    st.error("未能从 AI 回复中提取概率 JSON，下方为完整回复供检查（重跑一次通常即可）。")
    with st.expander("AI 完整回复", expanded=True):
        st.markdown(answer)
    st.stop()

# 契约在 prompt（with keys: up and down），兜底在代码（get 默认 0）
up_prob = prediction.get("up", 0)
down_prob = prediction.get("down", 0)

if up_prob + down_prob == 0:
    st.error(f"概率提取异常（up/down 均为 0），原始 keys：{list(prediction.keys())}")
    st.stop()

# ── 概率展示：指标卡 + plotly 条形图 ──
st.subheader("② 预测概率")

col1, col2 = st.columns(2)
with col1:
    st.metric("上涨概率 (up)", f"{up_prob:.1%}")
with col2:
    st.metric("下跌概率 (down)", f"{down_prob:.1%}")

prob_df = pd.DataFrame(
    {"方向": ["上涨 (up)", "下跌 (down)"], "概率": [up_prob, down_prob]}
)
fig = px.bar(
    prob_df,
    x="概率",
    y="方向",
    orientation="h",
    text=prob_df["概率"].apply(lambda v: f"{v:.1%}"),
    color="方向",
    color_discrete_map={"上涨 (up)": "#22c55e", "下跌 (down)": "#ef4444"},
    range_x=[0, 1],
    title=f"{name} 未来第五个交易日涨跌概率",
)
fig.update_traces(textposition="outside", showlegend=False)
fig.update_layout(yaxis_title="", xaxis_title="概率", xaxis_tickformat=".0%", height=280)
st.plotly_chart(fig, use_container_width=True)

# ── 骨架 ⑦：过程折叠，结论突出 ──
st.subheader("③ AI 完整分析")
with st.expander("展开完整分析过程", expanded=True):
    st.markdown(answer)
