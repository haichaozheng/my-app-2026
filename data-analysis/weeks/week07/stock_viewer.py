"""
股票数据查看器 — Week07 第 1 节实验最终版
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对应实验文档: weeks/week07/week07-streamlit-app.md（第 1 节实验）
六步生长的最终结果：下拉选股票 + 滑块选窗口 + 联动图表 + 指标卡
它就是第 3 节股价预测 APP（cases/app.py）的骨架

运行：streamlit run stock_viewer.py
依赖：streamlit、pandas（无需 API Key，数据为教学演示）
"""

import pandas as pd
import streamlit as st

# ── 步骤 2：演示数据（第 2 节课会换成 tushare 真数据） ──
prices = pd.DataFrame(
    {
        "平安银行": [11.20, 11.35, 11.28, 11.50, 11.42, 11.25, 11.48, 11.36, 11.53, 11.58],
        "贵州茅台": [1520, 1540, 1505, 1555, 1528, 1570, 1552, 1595, 1540, 1605],
        "比亚迪": [238, 251, 232, 246, 270, 254, 228, 258, 241, 265],
        "宁德时代": [246, 232, 259, 218, 255, 268, 240, 275, 249, 262],
    },
    index=pd.date_range("2026-09-28", periods=10, freq="B"),  # B=工作日
)

# ── 步骤 5：预设股票（与 cases/app.py 的侧栏同构） ──
STOCKS = {
    "000001.SZ": "平安银行",
    "600519.SH": "贵州茅台",
    "002594.SZ": "比亚迪",
    "300750.SZ": "宁德时代",
}

# ── 页面骨架 ──
st.title("我的股票查看器")
st.caption("教学演示数据，非真实行情；第 2 节课换成 tushare 取的真数据")

# ── 控件（加餐版：搬进侧栏，预览第 3 节 APP 的布局） ──
with st.sidebar:
    stock_options = [f"{code} {name}" for code, name in STOCKS.items()]
    selected = st.selectbox("选择股票", stock_options)
    lookback = st.slider("显示最近 N 个交易日", min_value=3, max_value=10, value=5)

code, name = selected.split()

# ── 主区域：表格 + 联动图表 + 指标卡 ──
st.subheader("近 10 个交易日收盘价")
st.dataframe(prices)

one = prices[name]  # 选中的那一列（Series）
st.subheader(f"{name}（{code}）· 最近 {lookback} 个交易日")
st.line_chart(one.tail(lookback))

latest, prev = one.iloc[-1], one.iloc[-2]
st.metric("最新收盘价", f"{latest:.2f}", delta=f"{latest - prev:+.2f}")

st.write(f"你选择了：{name}（{code}）")
# 🔍 rerun 证据：每次换股票/拖滑块，这个时间戳都会变——整脚本重跑了
st.caption(f"⏱ 本页面渲染于 {pd.Timestamp.now()}")
