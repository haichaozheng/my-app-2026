# 交互式可视化工具

> **引入时机**：W7 | **核心挑战**："静态图表不够，用户需要交互探索数据" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

你的产品用户不想只看一张固定的图表——他们想放大某个时间段、悬浮查看具体数值、点击某只股票看详情、筛选特定行业。静态的matplotlib图表无法满足这些需求。交互式可视化让你的数据产品从"报告"变成"工具"，用户可以按照自己的方式探索数据，发现他们关心的洞察。

金融数据分析产品尤其需要交互性。K线图需要悬浮显示OHLC数据，相关矩阵需要点击查看详情，时间序列需要缩放查看不同粒度。掌握Plotly、Pyecharts等交互式可视化工具，是你构建可用数据产品的关键能力。

## 这个知识点的核心内容

### 交互式可视化工具对比

| 特性 | Plotly | Pyecharts | ECharts(原生) |
|------|--------|-----------|---------------|
| 语言 | Python原生 | Python封装 | JavaScript |
| 学习曲线 | 低 | 中 | 高 |
| 定制灵活性 | 高 | 中 | 最高 |
| 金融图表 | 内置K线图 | 内置K线图 | 需自行配置 |
| 与Streamlit集成 | 极佳 | 需转换 | 需组件 |
| 导出格式 | HTML/图片 | HTML/图片 | HTML/图片 |
| 社区生态 | 最活跃 | 中文友好 | 最成熟 |

选择建议：
- **快速原型**：Plotly，API简洁、与Streamlit无缝集成
- **中文生态**：Pyecharts，文档和示例丰富
- **深度定制**：ECharts原生，灵活度最高但需要JS知识

### Plotly核心功能

Plotly Express是快速绑图的入口，Graph Objects是精细控制的工具：

```python
import plotly.express as px
import plotly.graph_objects as go

# Plotly Express：快速绑图
fig = px.line(df, x="date", y="close", color="name",
              title="银行股价格走势",
              hover_data={"close": ":.2f", "volume": ":,.0f"})
fig.show()

# Graph Objects：精细控制
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["date"], y=df["close"],
    mode="lines",
    name="收盘价",
    hovertemplate="日期: %{x}<br>收盘: %{y:.2f}<extra></extra>"
))

# 布局控制
fig.update_layout(
    title="银行股价格走势",
    xaxis_title="日期",
    yaxis_title="价格",
    hovermode="x unified",  # 同一X位置所有trace同时显示
    xaxis_rangeslider_visible=True,  # 范围选择器
)
```

### 交互功能设计

核心交互功能及其适用场景：

**悬浮提示（Hover）**：
```python
fig.update_traces(
    hovertemplate="<b>%{text}</b><br>日期: %{x}<br>收盘: %{y:.2f}<extra></extra>",
    text=df["name"]
)
```

**缩放与平移（Zoom/Pan）**：
```python
fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True),
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1月", step="month", stepmode="backward"),
                dict(count=3, label="3月", step="month", stepmode="backward"),
                dict(count=1, label="1年", step="year", stepmode="backward"),
                dict(label="全部", step="all")
            ]
        )
    )
)
```

**筛选与过滤**：
```python
fig = px.scatter(df, x="PE", y="ROE", color="industry",
                 size="market_cap", hover_name="name",
                 animation_frame="year")  # 动画按年份播放
```

**点击联动**：
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.03, row_heights=[0.7, 0.3])

# K线图
fig.add_trace(go.Candlestick(
    x=df["date"], open=df["open"], high=df["high"],
    low=df["low"], close=df["close"], name="K线"
), row=1, col=1)

# 成交量
fig.add_trace(go.Bar(
    x=df["date"], y=df["volume"], name="成交量",
    marker_color=np.where(df["close"] >= df["open"], "red", "green")
), row=2, col=1)
```

### K线图实现

金融数据产品最常见的交互图表：

```python
import plotly.graph_objects as go
import akshare as ak

df = ak.stock_zh_a_hist(symbol="601398", period="daily",
                         start_date="20240101", end_date="20241231", adjust="hfq")

fig = go.Figure(data=[go.Candlestick(
    x=df["日期"],
    open=df["开盘"],
    high=df["最高"],
    low=df["最低"],
    close=df["收盘"],
    increasing_line_color="red",     # 中国市场：红涨
    decreasing_line_color="green",   # 绿跌
    increasing_fillcolor="red",
    decreasing_fillcolor="green"
)])

fig.update_layout(
    title="工商银行K线图（前复权）",
    yaxis_title="价格",
    xaxis_rangeslider_visible=True,
    xaxis_rangebreaks=[dict(bounds=["sat", "mon"])],  # 隐藏周末
)

# 添加均线
for window, color in [(5, "blue"), (20, "orange"), (60, "purple")]:
    ma = df["收盘"].rolling(window).mean()
    fig.add_trace(go.Scatter(
        x=df["日期"], y=ma, mode="lines",
        name=f"MA{window}", line=dict(color=color, width=1)
    ))

fig.show()
```

### 嵌入应用

将交互图表嵌入Streamlit应用：

```python
import streamlit as st
import plotly.graph_objects as go

st.title("银行股分析仪表板")

# 侧边栏选择
stock = st.sidebar.selectbox("选择股票", ["601398", "600036", "601166"])
start_date = st.sidebar.date_input("开始日期", value=pd.Timestamp("2024-01-01"))
end_date = st.sidebar.date_input("结束日期", value=pd.Timestamp("2024-12-31"))

# 获取数据并绑图
df = get_stock_data(stock, start_date, end_date)
fig = create_kline_chart(df)

# 直接渲染Plotly图表
st.plotly_chart(fig, use_container_width=True)

# 或者导出HTML
html = fig.to_html(include_plotlyjs="cdn")
st.components.v1.html(html, height=600)
```

## 关键细节与易错点

- **易错：Plotly默认K线图是绿涨红跌**。中国市场需要手动设置increasing/decreasing的颜色
- **易错：hover_data格式不对**。Plotly的hovertemplate使用%{x}、%{y}占位符，注意extra标签
- **易错：数据量大时交互卡顿**。超过10万点的散点图应考虑聚合或WebGL渲染
- **易错：Pyecharts图表在Streamlit中显示不正常**。需要使用st.components.v1.html()渲染
- **易错：导出图片需要kaleido**。Plotly导出静态图片需安装kaleido库

## 金融数据分析示例

构建交互式银行股分析仪表板：

```python
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import akshare as ak
import pandas as pd
import numpy as np

# 获取多只银行股数据
codes = {"601398": "工商银行", "600036": "招商银行", "601166": "兴业银行"}
all_data = {}
for code, name in codes.items():
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                            start_date="20240101", end_date="20241231", adjust="hfq")
    df["return"] = df["收盘"].pct_change()
    df["MA5"] = df["收盘"].rolling(5).mean()
    df["MA20"] = df["收盘"].rolling(20).mean()
    all_data[name] = df

# === 交互K线图 + 成交量 ===
fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True,
    vertical_spacing=0.03, row_heights=[0.7, 0.3],
    subplot_titles=("工商银行K线图", "成交量")
)

icbc = all_data["工商银行"]

fig.add_trace(go.Candlestick(
    x=icbc["日期"], open=icbc["开盘"], high=icbc["最高"],
    low=icbc["最低"], close=icbc["收盘"],
    increasing_line_color="red", decreasing_line_color="green",
    increasing_fillcolor="red", decreasing_fillcolor="green",
    name="K线"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=icbc["日期"], y=icbc["MA5"],
    mode="lines", name="MA5", line=dict(color="blue", width=1)
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=icbc["日期"], y=icbc["MA20"],
    mode="lines", name="MA20", line=dict(color="orange", width=1)
), row=1, col=1)

colors = np.where(icbc["收盘"] >= icbc["开盘"], "red", "green")
fig.add_trace(go.Bar(
    x=icbc["日期"], y=icbc["成交量"],
    marker_color=colors, name="成交量", showlegend=False
), row=2, col=1)

fig.update_layout(
    height=600,
    xaxis_rangeslider_visible=False,
    hovermode="x unified",
    xaxis_rangebreaks=[dict(bounds=["sat", "mon"])],
)

# === 交互散点图：PE vs ROE ===
# 假设有基本面数据
pe_roe_data = pd.DataFrame({
    "name": ["工商银行", "招商银行", "兴业银行", "建设银行", "农业银行"],
    "PE": [5.2, 6.1, 4.8, 5.0, 5.1],
    "ROE": [11.5, 15.2, 10.8, 11.2, 11.0],
    "market_cap": [20000, 8000, 3000, 18000, 12000],
    "PB": [0.6, 0.9, 0.5, 0.6, 0.6]
})

fig2 = px.scatter(
    pe_roe_data, x="PE", y="ROE", size="market_cap", color="PB",
    hover_name="name",
    title="银行股估值与盈利能力",
    labels={"PE": "市盈率", "ROE": "净资产收益率(%)", "PB": "市净率"},
    color_continuous_scale="RdYlGn"
)
fig2.update_layout(coloraxis_colorbar=dict(title="PB"))

# === 相关矩阵热力图 ===
returns_df = pd.DataFrame({name: df.set_index("日期")["return"] for name, df in all_data.items()})
corr = returns_df.corr()

fig3 = go.Figure(go.Heatmap(
    z=corr.values, x=corr.columns, y=corr.index,
    colorscale="RdBu_r", zmid=0, zmin=-1, zmax=1,
    text=corr.values.round(2), texttemplate="%{text}",
    hovertemplate="%{x} vs %{y}: %{z:.3f}<extra></extra>"
))
fig3.update_layout(title="银行股收益率相关性")
```

## 拓展学习

- Plotly官方教程——最系统的Plotly学习资源
- Pyecharts官方文档——中文最友好的交互图表库
- ECharts官网Examples——最丰富的图表示例库
- Dash by Plotly——构建完整数据应用的框架
- 《Interactive Data Visualization for the Web》——D3.js背后的可视化理论

## 参考链接

- https://plotly.com/python/ — Plotly Python官方文档
- https://pyecharts.org/ — Pyecharts官方文档
- https://echarts.apache.org/examples/ — Apache ECharts图表示例
- https://dash.plotly.com/ — Dash框架文档，构建交互式数据应用
