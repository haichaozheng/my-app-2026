# Streamlit/Gradio

> **引入时机**：W7 | **核心挑战**："用什么框架做数据分析产品原型？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

你现在有了数据分析的代码，但它们散落在Jupyter Notebook里——只有你自己能用。要让其他人（用户、评审、投资人）使用你的分析成果，你需要把它变成一个Web应用。Streamlit和Gradio是两个专门为数据科学和AI应用设计的Python Web框架，让你不需要前端知识就能快速搭建可交互的数据产品原型。

对于金融数据分析产品来说，选择合适的框架至关重要。如果你做的是仪表板类应用（图表+筛选+对比），Streamlit是最佳选择；如果你做的是AI交互类应用（输入文本→返回分析结果），Gradio更合适。掌握这两个框架，你就能在1-2天内把Notebook变成可分享的产品原型。

## 这个知识点的核心内容

### Streamlit与Gradio对比

| 维度 | Streamlit | Gradio |
|------|-----------|--------|
| 核心场景 | 数据仪表板、分析报告 | AI模型演示、交互式工具 |
| 布局灵活性 | 高（多列、侧边栏、Tab） | 中（行列布局） |
| 图表支持 | 原生Plotly/Matplotlib/Altair | 主要支持Matplotlib/Plotly |
| AI交互 | 支持chat组件 | 原生chat、audio、image组件 |
| 定制UI | 中等 | 较低 |
| 学习曲线 | 低 | 极低 |
| 部署 | Streamlit Cloud免费 | Hugging Face Spaces免费 |
| 热重载 | 支持 | 支持 |

选择指南：
- 做仪表板/数据分析产品 → **Streamlit**
- 做AI聊天/模型演示 → **Gradio**
- 不确定 → 先用Streamlit，更灵活

### Streamlit基础应用结构

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# === 页面配置（必须在最前面）===
st.set_page_config(
    page_title="银行股分析仪表板",
    page_icon="🏦",
    layout="wide"
)

# === 侧边栏：控制区 ===
with st.sidebar:
    st.header("参数设置")
    stock_code = st.selectbox("选择股票", ["601398", "600036", "601166"])
    start_date = st.date_input("开始日期")
    end_date = st.date_input("结束日期")
    show_ma = st.checkbox("显示均线", value=True)
    ma_windows = st.multiselect("均线周期", [5, 10, 20, 60], default=[5, 20])

# === 主区域：展示区 ===
st.title("🏦 银行股分析仪表板")

# 指标卡片
col1, col2, col3, col4 = st.columns(4)
col1.metric("当前价格", "5.42", "+0.08 (+1.5%)")
col2.metric("PE(TTM)", "5.2", "-0.3")
col3.metric("PB", "0.61", "+0.02")
col4.metric("股息率", "5.8%", "+0.1%")

# K线图
st.subheader("价格走势")
fig = go.Figure()  # ... 绑图逻辑
st.plotly_chart(fig, use_container_width=True)

# 数据表格
st.subheader("近期数据")
st.dataframe(df.tail(20), use_container_width=True, hide_index=True)
```

### Streamlit布局组件

```python
# Tab布局
tab1, tab2, tab3 = st.tabs(["K线图", "基本面", "AI分析"])
with tab1:
    st.plotly_chart(kline_fig)
with tab2:
    st.dataframe(fundamental_df)
with tab3:
    st.chat_message("assistant").write("分析结果...")

# 列布局
col1, col2 = st.columns([2, 1])  # 2:1宽度比
with col1:
    st.plotly_chart(main_chart)
with col2:
    st.write("关键指标")
    st.json({"PE": 5.2, "PB": 0.6})

# Expander折叠
with st.expander("查看原始数据"):
    st.dataframe(raw_df)

# Container容器
placeholder = st.empty()
placeholder.line_chart(new_data)  # 动态更新
```

### Streamlit数据缓存

缓存是Streamlit性能的关键：

```python
# 缓存数据获取（避免每次交互重新获取）
@st.cache_data(ttl=3600)  # 缓存1小时
def get_stock_data(code, start, end):
    import akshare as ak
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                            start_date=start, end_date=end, adjust="hfq")
    return df

# 缓存计算结果
@st.cache_data
def calculate_indicators(df, windows):
    for w in windows:
        df[f"MA{w}"] = df["close"].rolling(w).mean()
    return df

# 缓存全局资源（如数据库连接）
@st.cache_resource
def get_database_connection():
    import sqlite3
    return sqlite3.connect("stocks.db")
```

### Gradio基础应用结构

```python
import gradio as gr

def analyze_stock(stock_code, analysis_type):
    # 分析逻辑
    return result_text, result_chart

with gr.Blocks(title="银行股AI分析助手") as demo:
    gr.Markdown("# 🏦 银行股AI分析助手")

    with gr.Row():
        stock_input = gr.Dropdown(
            choices=["601398", "600036", "601166"],
            label="选择股票"
        )
        analysis_type = gr.Radio(
            choices=["技术分析", "基本面分析", "综合分析"],
            label="分析类型"
        )

    analyze_btn = gr.Button("开始分析", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(label="分析结论", lines=5)
        output_chart = gr.Plot(label="分析图表")

    analyze_btn.click(
        fn=analyze_stock,
        inputs=[stock_input, analysis_type],
        outputs=[output_text, output_chart]
    )

demo.launch()
```

### Gradio Chat组件

```python
def chat_respond(message, history):
    prompt = f"你是一个金融分析助手。用户问题：{message}"
    response = call_llm_api(prompt)
    return response

demo = gr.ChatInterface(
    fn=chat_respond,
    title="银行股AI分析助手",
    description="输入关于银行股的问题，AI将给出分析",
    examples=["工商银行值得买入吗？", "银行板块近期走势如何？"]
)
demo.launch()
```

### 图表集成

在Streamlit中集成Plotly图表的最佳实践：

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_kline_with_volume(df):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.03, row_heights=[0.7, 0.3]
    )

    fig.add_trace(go.Candlestick(
        x=df["date"], open=df["open"], high=df["high"],
        low=df["low"], close=df["close"],
        increasing_line_color="red", decreasing_line_color="green",
        increasing_fillcolor="red", decreasing_fillcolor="green"
    ), row=1, col=1)

    colors = ["red" if c >= o else "green" for c, o in zip(df["close"], df["open"])]
    fig.add_trace(go.Bar(x=df["date"], y=df["volume"], marker_color=colors),
                  row=2, col=1)

    fig.update_layout(
        height=500, xaxis_rangeslider_visible=False,
        margin=dict(l=50, r=50, t=30, b=30)
    )
    return fig

fig = create_kline_with_volume(df)
st.plotly_chart(fig, use_container_width=True)
```

## 关键细节与易错点

- **易错：Streamlit每次交互都重新运行整个脚本**。必须用@st.cache_data缓存耗时操作，否则每次点按钮都重新获取数据
- **易错：st.set_page_config不在脚本最开头**。这个调用必须是第一个Streamlit命令
- **易错：Gradio的fn返回值类型与outputs不匹配**。返回PIL Image对应gr.Image，返回plotly fig对应gr.Plot
- **易错：Streamlit中直接print()看不到输出**。用st.write()或st.text()替代
- **易错：忘记在plotly图表中设置use_container_width=True**。图表不会自适应容器宽度

## 金融数据分析示例

用Streamlit构建完整的银行股分析仪表板：

```python
import streamlit as st
import akshare as ak
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="银行股仪表板", page_icon="🏦", layout="wide")

BANK_CODES = {
    "601398": "工商银行", "601939": "建设银行",
    "601288": "农业银行", "601988": "中国银行",
    "600036": "招商银行", "601166": "兴业银行"
}

@st.cache_data(ttl=3600)
def get_stock_data(code):
    df = ak.stock_zh_a_hist(
        symbol=code, period="daily",
        start_date="20240101", end_date="20241231", adjust="hfq"
    )
    df["日期"] = pd.to_datetime(df["日期"])
    df["收益率"] = df["收盘"].pct_change()
    return df

# 侧边栏
with st.sidebar:
    st.header("⚙️ 参数设置")
    selected = st.selectbox("选择股票", list(BANK_CODES.keys()),
                            format_func=lambda x: f"{x} {BANK_CODES[x]}")
    start = st.date_input("开始日期", value=pd.Timestamp("2024-01-01"))
    end = st.date_input("结束日期", value=pd.Timestamp("2024-12-31"))
    show_ma = st.checkbox("显示均线", value=True)
    ma_list = st.multiselect("均线周期", [5, 10, 20, 60], default=[5, 20])
    compare = st.multiselect("对比股票", list(BANK_CODES.keys()),
                             format_func=lambda x: BANK_CODES[x])

# 获取数据
df = get_stock_data(selected)
mask = (df["日期"].dt.date >= start) & (df["日期"].dt.date <= end)
df_filtered = df[mask]

name = BANK_CODES[selected]
st.title(f"🏦 {name} 分析仪表板")

# 指标卡片
latest = df_filtered.iloc[-1]
prev = df_filtered.iloc[-2]
change = latest["收盘"] - prev["收盘"]
change_pct = change / prev["收盘"] * 100

col1, col2, col3 = st.columns(3)
col1.metric("收盘价", f"{latest['收盘']:.2f}",
            f"{change:+.2f} ({change_pct:+.2f}%)")
col2.metric("成交量", f"{latest['成交量']:,.0f}")
col3.metric("最高/最低", f"{latest['最高']:.2f} / {latest['最低']:.2f}")

# Tab布局
tab1, tab2, tab3 = st.tabs(["📈 K线图", "📊 对比分析", "📋 数据表"])

with tab1:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03, row_heights=[0.7, 0.3])
    fig.add_trace(go.Candlestick(
        x=df_filtered["日期"], open=df_filtered["开盘"],
        high=df_filtered["最高"], low=df_filtered["最低"],
        close=df_filtered["收盘"],
        increasing_line_color="red", decreasing_line_color="green",
        increasing_fillcolor="red", decreasing_fillcolor="green"
    ), row=1, col=1)

    if show_ma:
        for w in ma_list:
            ma = df_filtered["收盘"].rolling(w).mean()
            fig.add_trace(go.Scatter(
                x=df_filtered["日期"], y=ma, mode="lines",
                name=f"MA{w}", line=dict(width=1)
            ), row=1, col=1)

    colors = ["red" if c >= o else "green"
              for c, o in zip(df_filtered["收盘"], df_filtered["开盘"])]
    fig.add_trace(go.Bar(
        x=df_filtered["日期"], y=df_filtered["成交量"],
        marker_color=colors, name="成交量"
    ), row=2, col=1)

    fig.update_layout(height=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    if compare:
        compare_fig = go.Figure()
        for code in [selected] + compare:
            cdf = get_stock_data(code)
            compare_fig.add_trace(go.Scatter(
                x=cdf["日期"], y=cdf["收盘"],
                mode="lines", name=BANK_CODES[code]
            ))
        compare_fig.update_layout(title="价格走势对比", height=500)
        st.plotly_chart(compare_fig, use_container_width=True)
    else:
        st.info("请在侧边栏选择对比股票")

with tab3:
    st.dataframe(df_filtered, use_container_width=True, hide_index=True,
                 column_config={"收益率": st.column_config.ProgressColumn(
                     format="%.2f%", min_value=-0.1, max_value=0.1)})
```

## 拓展学习

- Streamlit官方文档——最权威的参考，包含所有组件和API
- Gradio官方文档——完整的组件库和示例
- Streamlit Gallery——真实应用案例库，获取灵感
- 30 Days of Streamlit——系统的Streamlit学习路径
- Streamlit高级主题：Session State和Callback——理解Streamlit的运行机制

## 参考链接

- https://docs.streamlit.io/ — Streamlit官方文档
- https://www.gradio.app/docs — Gradio官方文档
- https://streamlit.io/gallery — Streamlit应用画廊
- https://30days.streamlit.app/ — 30天学Streamlit教程
