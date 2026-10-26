import streamlit as st

from dotenv import load_dotenv
import os

# 读取 my-app/.env 中的密钥（该文件已加入 .gitignore，不会进 git）
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")

import tushare as ts

ts.set_token(token=TUSHARE_TOKEN)

# bar = ts.pro_bar(
#     ts_code="000001.SZ",
#     adj="hfq",              # 后复权：分红除权不产生价格跳空，走势连续可比
#     start_date="20100901",
#     end_date="20261021",    # 换成最近一个交易日
# )
# bar = bar.sort_values("trade_date")   # 返回按日期倒序，画图前要排成 旧 → 新

# st.subheader("后复权收盘价走势")
# st.line_chart(bar.set_index("trade_date")["close"])

pro = ts.pro_api()
# df = pro.daily_basic(
#     ts_code="000001.SZ",
#     trade_date="20261020",   # 换成最近一个交易日
#     fields="ts_code,trade_date,turnover_rate,volume_ratio,pe,pb",
# )

import pandas as pd

df = pd.DataFrame()
today = pd.Timestamp.now()
for i in range(10):  # 多倒推几天，容错非交易日
    trade_date = (today - pd.Timedelta(days=i)).strftime("%Y%m%d")
    try:
        daily = pro.daily_basic(
            ts_code="000001.SZ", trade_date=trade_date,
            fields="ts_code,trade_date,turnover_rate,volume_ratio,pe,pb",
        )
        if not daily.empty:
            df = pd.concat([df, daily], ignore_index=True)
    except Exception:
        continue
    if len(df) >= 5:
        break

st.subheader("每日指标数据")
st.dataframe(df)


from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    st.warning("未设置 DEEPSEEK_API_KEY：请在 my-app/.env 文件中添加一行 `DEEPSEEK_API_KEY=你的密钥`，保存后刷新页面。")
    st.stop()

def llm_chat(prompt):
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

# prompt = "给我写一个计算机和数据分析方面笑话，要求是短小精悍，风趣幽默，让人捧腹大笑。"
# response = llm_chat(prompt)
# st.subheader("AI 笑话")
# st.write(response)

firm_name = "平安银行"
question = f"will future price of this stock {firm_name} moves up or down in the subsequent fifth trading day?"
resolution_criteria = "预测的判断标准：股票价格在随后的第五个交易日是否高于或低于当前价格。"
materials = str(df.to_dict(orient="records"))

prompt = f"""
You are an expert in future event prediction.
    - Question:{question}
    - Resolution Criteria:{resolution_criteria}
    - Materials: {materials}

    Solve the problem step by step as required by the instructions.

    Instructions:
       1. 重述并扩展问题……
       （中间各步：正反理由及强度 → 聚合 → 初始概率 → 反思，完整版见 notebook）
       7. Output your final probability prediction (the sum of up and down probabilities must equal to 1).
       {{ Insert your answer, your final prediction must be in JSON format with keys: up and down }}
       8. 回答问题用中文。
"""

answer = llm_chat(prompt)

# 显示到页面上（给用户看 AI 的完整分析；print 只到终端）
st.subheader("AI 预测（原始回复）")
st.write(answer)  

