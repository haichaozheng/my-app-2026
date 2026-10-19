"""
进度条效果演示 — Week07 加餐配套
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
运行：streamlit run progress_demo.py
对照页面上下两段，直观感受"有进度条"和"没进度条"的差别
"""

import time

import streamlit as st

st.title("进度条效果演示")

st.subheader("① 有进度条：知道它在干活")
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
    time.sleep(0.03)  # 模拟耗时，共约 3 秒
st.success("完成！")

st.subheader("② 没有进度条：同样的 3 秒，页面死寂")
time.sleep(3)
st.success("也完成了——但你刚才是不是以为卡死了？")
