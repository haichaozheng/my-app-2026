import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="我的数据产品", layout="wide")

DATA_FILE = Path("data") / "sample.csv"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


st.title("数据分析产品 · 最小骨架")

if not DATA_FILE.exists():
    st.warning("把项目 CSV 放到 data/ 目录后即可运行（文件名见上方 DATA_FILE）")
    st.stop()

df = load_data(DATA_FILE)

with st.sidebar:
    st.header("筛选")
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    x_col = st.selectbox("X 轴", df.columns.tolist())
    y_col = st.selectbox("Y 轴", num_cols or df.columns.tolist())

st.subheader("数据概览")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("核心图表")
if x_col in num_cols and y_col in num_cols:
    fig = px.scatter(df, x=x_col, y=y_col)
else:
    fig = px.bar(df.head(50), x=x_col, y=y_col)
st.plotly_chart(fig, use_container_width=True)

st.subheader("关键发现")
st.markdown("在此替换为你 W5/W6 已设计好的洞察与图表设计说明。")
