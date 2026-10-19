# Week 07 实验 — 弄懂 Streamlit，做出股价波动预测 APP

> **定位**：本周实验基础篇。第 1 节跟做 Streamlit 基础（六步长出迷你查看器），第 2 节取数与接大模型；最后的组装 APP + AI 辅助编程是**课后练习任务**，按升级篇 `week07-streamlit-app-advanced.md` 推进。
> **实验任务**：应用 Streamlit 和大模型做一个预测股价波动方向的 APP（课堂案例 `streamlit.ipynb` 为底稿）。
> **耗时**：课堂跟做约 70 分钟（分布三节课）+ 课后补齐约 2-3 小时。实验不需要课后提交报告，按文末六项自查留档备抽查。
> **前提**：已按 `weeks/week03/venv-setup.md` 建好 `.venv`。
> **与本周其他任务的关系**：本实验做的是**课堂股票案例**；个人 MVP（迁你自己的 W4/W6 成果）走 `lab.md` + `mvp-template/`，两条线不要混。

---

## 实验路线图

按本周三节课推进——每一节都是下一节的地基，**过了验收点再往下走**：


| 节     | 主题             | 你将学会                                      | 课堂     | 课后     | 主要素材                                                                                       |
| ----- | -------------- | ----------------------------------------- | ------ | ------ | ------------------------------------------------------------------------------------------ |
| 第 1 节 | Streamlit 基础六步 | 跑起来 / 展示 / 下拉选股票 + 联动                     | 跟做 25' | 补跑 30' | 本文档 + 官方 [main-concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) |
| 第 2 节 | 取数 + 接大模型      | 通用行情后复权收盘价 / 每日指标 / `.env` / 预测 prompt 与输出规范 | 演示     | 70'    | `streamlit.ipynb` 第 2 节                                                                    |
| 课后任务 | 组装 APP（升级篇）   | JSON 提取 / 按钮全链路 / **AI 辅助编程**             | —      | 60-90' | `week07-streamlit-app-advanced.md` + `cases/app.py`（对照）                                      |
| ★     | 进阶挑战           | 部署 / 加指标 / session_state / 缓存              | —      | 自选     | 升级篇文末                                                                                       |


**一句话心智模型（全程适用）**：Streamlit 应用 = 每次用户交互都从头到尾重跑一遍的 Python 脚本。`st.xxx` 负责输出，widget 返回值当普通变量用，**联动 = 用这个变量去筛选数据**。

**存档点**：每过一节就 `git commit` 一次（或另存副本）。下一节改崩了，随时退回存档——比从头重来省 20 分钟。

## 环境准备（一次性，10 分钟）

```bash
# 1. 激活虚拟环境（仓库根目录）
.venv\Scripts\activate          # Mac: source .venv/bin/activate

# 2. 安装依赖
pip install streamlit pandas tushare openai python-dotenv

# 3. 在 week07/ 下建实验工作目录，实验全程就一个文件 app.py
mkdir my-app && cd my-app
```

这一步也可以交给 AI 做。在仓库根目录打开 OpenCode/Cursor，输入（或按你自己的话改写）：

> 请帮我完成本周 Streamlit 实验的环境初始化：在 `data-analysis/weeks/week07/` 下新建目录 `my-app/`，里面只建一个文件 `app.py`，内容为最小 Streamlit 应用（`import streamlit as st` + `st.title("我的股票查看器")` + `st.write("Hello, Streamlit!")`）；再建一个 `.env` 模板文件，包含 `TUSHARE_TOKEN=` 和 `DEEPSEEK_API_KEY=` 两行占位（值留空，我自己填），并确认 `.env` 已被仓库的 `.gitignore` 忽略，不会被提交。做完告诉我怎么用 `streamlit run` 跑起来。

用 AI 的注意点（本周反复强调的规矩）：

- **验证再采信**：AI 说"已创建"不等于创建了——自己到文件管理器/资源管理器里看一眼 `my-app/app.py` 是否存在、内容对不对
- **密钥自己填**：`.env` 里的 token 和 key 永远自己手动填，**不要粘贴给 AI、不要发给同学**
- 这个提示词本身就是第 3 节「AI 辅助编程」的热身：**说清楚做什么、放哪里、约束是什么**，AI 才填得对

摆好窗口：左边编辑器，右边浏览器（终端跑起来后自动弹出）。

**密钥配置（第 2 节起用到）**：把 `my-app/` 下的 `.env` 填成真实密钥（上一步走 AI 路径的同学：占位文件已建好，直接填值；手动路径的同学：新建 `.env`；**此文件永不提交、不发群里**）：

```
TUSHARE_TOKEN=你的tushare token
DEEPSEEK_API_KEY=你的 DeepSeek key
```

- tushare token：两种来源二选一
  - **课程公用 token（本学期可用）**：`TUSHARE_TOKEN=5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521`——全班共用，**积分在 2000 左右，同时调用可能触发频次限制**；遇到限频报错（提示积分/次数不足）就换个时段再试，或用自己的 token
  - 自己注册：tushare.pro 注册获取（推荐：免受全班并发限频影响）
- DeepSeek key：platform.deepseek.com 获取

**tushare 基本用法**（三行，对应 `streamlit.ipynb` 第 2 节）：

```python
import tushare as ts

ts.set_token(token=TUSHARE_TOKEN)   # 每次会话设置一次
pro = ts.pro_api()                  # 拿到 pro 接口对象，之后用它取数
```

> `set_token` 只认 token 字符串本身（从 `.env` 读出来再传进去，别把整行 `TUSHARE_TOKEN=xxx` 填进去）；报"积分不足/没有权限"就是 token 权限问题，不是代码问题。

---



# 第 1 节实验 · Streamlit 基础（课堂跟做 25 分钟，课后补齐约 30 分钟）



## 步骤 0 | 先弄懂它是什么（2 分钟）

先看 [Streamlit 官网](https://streamlit.io/) 首页怎么介绍自己：

> **A faster way to build and share data apps**
> Turn your data scripts into shareable web apps in minutes.
> All in pure Python. No front‑end experience required.
>
> （一种更快构建和分享数据应用的方式：几分钟内把你的数据脚本变成可分享的网页应用。全部用纯 Python，无需任何前端经验。）

三句话对应你现在的处境：`streamlit.ipynb` 是数据脚本，本周把它变成别人浏览器能打开的 APP——不用学 HTML/CSS/JS，你已会的 pandas 就是全部前置。

笔记本 ↔ Streamlit 对照表：


| 在 notebook 里          | 在 Streamlit 里                                   |
| --------------------- | ----------------------------------------------- |
| 格子输出（最后一个表达式 / print） | `st.write` / `st.dataframe` / `st.line_chart` … |
| 你赋值的变量                | widget 的返回值（`selectbox` / `slider` …）           |
| 手动「Restart & Run All」 | 用户一动控件，自动全部重跑                                   |
| 别人跑不起你的 notebook      | 别人浏览器直接打开                                       |


只记一个动作公式：`st.xxx` **负责输出，widget 返回值当普通变量用，联动 = 用这个变量去筛选数据**。

## 六步跟做

每步节奏：**猜 → 做 → 观察 → 检查**（课堂由教师停问；课后自问自答）。

### 步骤 1 | 先跑起来（2 分钟）

猜一猜：一个最小的 Streamlit 应用要几行代码？

`app.py` 写成：

```python
import streamlit as st

st.title("我的股票查看器")
st.write("Hello, Streamlit!")
```

终端（在 `my-app/` 目录下，**不是** `python app.py`）：

```bash
streamlit run app.py
```

👀 **观察**：浏览器打开 `http://localhost:8501`。改一个字 → 保存 → 页面右上角点 **Always rerun**，之后每次保存自动刷新。

✅ **检查**：这和 notebook 有什么区别？
答：就是普通 `.py` 文件；运行命令是 `streamlit run`；输出不在终端里，在别人的浏览器里——这就是「店面」和「实验室」的区别。

### 步骤 2 | 数据上屏（3 分钟）

猜一猜：DataFrame 放到网页上要写多少前端代码？

> 提示：下面用的是**模拟假数据**（手工填的收盘价，不是真实行情）——先把"数据怎么上屏"跑通，第 2 节再换成 tushare 的真数据。

继续加：

```python
import pandas as pd

prices = pd.DataFrame(
    {
        "平安银行": [11.20, 11.35, 11.28, 11.50, 11.42, 11.25, 11.48, 11.36, 11.53, 11.58],
        "贵州茅台": [1520, 1540, 1505, 1555, 1528, 1570, 1552, 1595, 1540, 1605],
        "比亚迪": [238, 251, 232, 246, 270, 254, 228, 258, 241, 265],
        "宁德时代": [246, 232, 259, 218, 255, 268, 240, 275, 249, 262],
    },
    index=pd.date_range("2026-09-28", periods=10, freq="B"),  # B=工作日
)

st.subheader("近 10 个交易日收盘价")
st.dataframe(prices)
st.caption("教学演示数据，非真实行情；第 2 节换成 tushare 取的真数据")
```

👀 **观察**：网页上出现表格，可排序、可滚动、可全屏。

✅ **检查**：`st.dataframe` 和在 notebook 里敲 `df` 有何异同？
答：同一个 pandas 对象，展示的地方从格子变成网页。`prices` 只是普通变量，`st.xxx` **才是「放到页面上」的动作**。

📎 30 秒加餐：把 `st.dataframe` 换成 `st.table` 试试——静态表（不可排序）。快速原型用前者。

### 步骤 3 | 一行出图（3 分钟）

继续加：

```python
st.subheader("价格走势")
st.line_chart(prices)
```

👀 **观察**：一行代码，四条折线图。

✅ **检查**：这张图在 W6 用 matplotlib 要写几行？
答：Streamlit 内置图表胜在快，适合原型；要完全复刻你 W6 的图表设计（配色/标注/交互），第 3 节换成 plotly（`st.plotly_chart`）。

### 步骤 4 | 用户开口说话：滑块 + 看见 rerun（4 分钟）★机制核心

继续加：

```python
lookback = st.slider("显示最近 N 个交易日", min_value=3, max_value=10, value=5)
st.line_chart(prices.tail(lookback))

# 🔍 rerun 证据：每次交互后，这个时间戳都会变
st.caption(f"⏱ 本页面渲染于 {pd.Timestamp.now()}")
```

👀 **观察**：拖动滑块，图表「自己」变了。**盯着时间戳**——每拖一下都变。

✅ **检查（本节课最重要的一问）**：图表为什么会跟着滑块变？
答：不是「图表监听了滑块」，而是**你每动一下控件，整个脚本从头到尾重跑了一遍**，`lookback` 拿到了新值。理解了它，第 3 节「按钮触发预测」和 `st.session_state`（跨重跑记住状态）都是同一件事的延伸。

### 步骤 5 | 下拉列表选股票（5 分钟）★第 3 节 APP 的骨架

继续加：

```python
STOCKS = {
    "000001.SZ": "平安银行",
    "600519.SH": "贵州茅台",
    "002594.SZ": "比亚迪",
    "300750.SZ": "宁德时代",
}

stock_options = [f"{code} {name}" for code, name in STOCKS.items()]
selected = st.selectbox("选择股票", stock_options)

code, name = selected.split()
st.write(f"你选择了：{name}（{code}）")
```

👀 **观察**：下拉列表出现，选项是「代码 + 名称」；换一个选项，时间戳又变了（又是 rerun）。

✅ **检查**：`selectbox` 和 `slider` 有何异同？
答：选项离散、从给定列表里挑；返回值是字符串，**当普通变量用**——套路完全一样。

📎 记住这段代码：第 3 节股价预测 APP 的侧栏（`cases/app.py`）用的就是它。

### 步骤 6 | 选项联动：合成迷你 APP（5 分钟）

继续加：

```python
one = prices[name]  # 选中的那一列（Series）

st.subheader(f"{name} · 最近 {lookback} 个交易日")
st.line_chart(one.tail(lookback))

latest, prev = one.iloc[-1], one.iloc[-2]
st.metric("最新收盘价", f"{latest:.2f}", delta=f"{latest - prev:+.2f}")
```

👀 **观察**：换股票 → 图表和指标联动；拖滑块 → 窗口变长变短。**一个能交互的迷你产品成型了。**

📎 `st.metric` **是什么**：**指标卡**——金融 APP 里最常见的那种"大数字 + 涨跌标记"展示（想想股票软件首页的个股报价卡）。三个参数：

```python
st.metric(label="最新收盘价", value=f"{latest:.2f}", delta=f"{latest - prev:+.2f}")
#        ↑ 卡片标题              ↑ 主数值(大字)         ↑ 变化量(小字+箭头)
```

- `delta > 0` 自动显示绿色 **▲ 向上箭头**；`delta < 0` 自动显示红色 **▼ 向下箭头**（A 股习惯红涨绿跌，可加 `delta_color="inverse"` 反转）
- `f"{latest - prev:+.2f}"` 里的 `+` 是格式化语法：强制带正负号（`+0.13` 而不是 `0.13`），`: -2f` 保留两位小数——没有它，涨跌方向就看不出来
- 为什么自己算 `latest - prev` 而不让 Streamlit 算？**指标卡只管展示，算什么、和谁比（环比/同比/对比基准）由你决定**——这是"展示"和"分析"的分工

✅ **检查**：所谓「联动」在代码上是什么？
答：没有任何魔法——就是**用 widget 的返回值（**`name`**、**`lookback`**）去筛选数据（**`prices[name]`**、**`.tail(lookback)`**）**。你在 notebook 里用代码过滤，在网页上用户用点击过滤。

### 收束（2 分钟）

一句话（跟读）：**Streamlit = 把 notebook 的格子变成网页的元件。**

快问快答（课堂随机点名 / 课后自测）：

1. 产品为什么必须是 `.py` 而不是 notebook？——`streamlit run` 只认脚本；产品要一个入口。
2. 用户改了下拉选项后，哪些代码执行了？——整个脚本，从头到尾。
3. 用户选的值去哪了？——widget 的返回值，是个普通变量。
4. 想跨 rerun 记住点东西怎么办？——`st.session_state`（本周知道有它即可）。

**✅ 第 1 节过关验收**：`app.py` 能换股票、换窗口，图表联动；能不看书说出那句话心智模型。

**💣 常见坑**：


| 症状                             | 原因 / 解法                                              |
| ------------------------------ | ---------------------------------------------------- |
| `streamlit: command not found` | venv 没激活，或漏了 `pip install streamlit`                 |
| 页面不自动刷新                        | 右上角菜单点 **Always rerun**                              |
| 改了代码页面没变                       | 文件没保存；或终端跑的不是这个文件（看终端打印的路径）                          |
| `python app.py` 没反应            | 运行命令是 `streamlit run app.py`                         |
| 把代码敲进了 notebook                | 应用是 `.py`；notebook 是实验室，产品是店面                        |
| 端口被占用                          | `streamlit run app.py --server.port 8502`            |
| `KeyError: '宁德时代'`             | 步骤 6 的 `name` 来自 `STOCKS`，但 `prices` 里没有这一列——两边股票要对齐 |


**💾 存档点 1**：commit。跟丢的同学：直接取 `weeks/week07/stock_viewer.py`（本节最终版），`streamlit run` 先跑起来，再回头对照看每一块是哪一步加的。

### 加餐（时间富余再做）

**进度条**（第 3 节「AI 分析中…」会用到）：

```python
import time

bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
    time.sleep(0.01)
```

这段代码在做什么：

- `st.progress(0)` 先在页面上放一个 **0% 的进度条**；`bar.progress(i + 1)` 不断**更新同一个进度条**的百分比——注意不是新增 100 个条，而是原地刷新（`bar` 是个可更新的占位对象）
- `time.sleep(0.01)` 只是**模拟耗时的计算**——让进度条肉眼可见地"长大"（全程约 1 秒）。真实场景里这里放的是你真正的耗时操作（取数、调大模型）

**🏃 先体验再看代码（2 分钟）**：光看代码想象不出效果——把下面完整的对照实验敲进 `progress_demo.py` 跑一遍：

```python
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
```

运行 `streamlit run progress_demo.py`，页面上下两段就是**同一份耗时的两种待遇**：① 的蓝条从 0% 平滑涨到 100%（约 3 秒）；② 死寂 3 秒后突然蹦出"也完成了"。盯着 ② 感受一下"是不是卡死了？"的怀疑——**这就是进度条存在的理由**。

它解决什么问题：第 3 节点「开始预测」后，取数 + 大模型推理要 10-30 秒，页面一动不动用户会以为卡死了。进度条（或 `st.spinner` 转圈）告诉用户"在干活，请等"——**长计算不给反馈 = 用户关闭页面**，这是产品意识和实验室脚本的最大区别之一。

📎 注意加餐里 `st.progress` 和第 3 节实际用的 `st.spinner`（"AI 正在分析…"转圈）是同-purpose 的两种选择：进度条适合**知道进度百分比**的循环任务；spinner 适合**不知道要多久**的一次性等待（比如调一次 API）。

**控件搬进侧栏**（预览第 3 节 APP 的样子）：

```python
with st.sidebar:
    lookback = st.slider("显示最近 N 个交易日", min_value=3, max_value=10, value=5)
    selected = st.selectbox("选择股票", stock_options)
```

把原来两处控件包进 `with st.sidebar:`，其余代码不动——控件就到了页面左侧。

---



# 第 2 节实验 · 换真数据 + 接大模型（课后约 70 分钟）

对应 `streamlit.ipynb`「获取股票的每日指标」「获取多天的指标数据」「chat with AI」「构造预测prompt，并预测」。本周用 tushare 的两个接口，**分工不同**：


| 接口                     | 文档                                                                                     | 用途                           | 取法         |
| ---------------------- | -------------------------------------------------------------------------------------- | ---------------------------- | ---------- |
| 通用行情 `ts.pro_bar`      | [https://tushare.pro/document/2?doc_id=109](https://tushare.pro/document/2?doc_id=109) | **行情展示**：后复权收盘价画走势图          | 一次取一段日期区间  |
| 每日指标 `pro.daily_basic` | [https://tushare.pro/document/2?doc_id=32](https://tushare.pro/document/2?doc_id=32)   | **预测原材料**：换手率/量比/PE/PB 喂给大模型 | 按单日取，循环拼多天 |


**🎯 目标**：把演示数据换成 tushare 真实数据（行情用后复权收盘价、预测用每日指标），并让大模型基于指标给出涨跌概率——APP 的"原材料"和"大脑"。

## 2.1 通用行情接口：后复权收盘价（15 分钟，行情展示用）

**读密钥 + 设 token**（密钥永不硬编码；`set_token` 每次会话设一次，之后 `pro_bar` 和 `daily_basic` 都能用）：

```python
from dotenv import load_dotenv
import os

load_dotenv(override=True)
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")

import tushare as ts

ts.set_token(token=TUSHARE_TOKEN)
```

> **课堂快速通道**：还没来得及注册 tushare 的同学，可以直接把课程公用 token 拷进 `my-app/.env` 的 `TUSHARE_TOKEN=` 后面：
> `5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521`
> （全班共用，积分约 2000，**同时调用可能限频**；报"积分/次数不足"就换个时段再试，或注册自己的 token。）

**一次取一段日期**（注意与 2.2 的按单日取对照——`pro_bar` 直接给区间）：

```python
bar = ts.pro_bar(
    ts_code="000001.SZ",
    adj="hfq",              # 后复权：分红除权不产生价格跳空，走势连续可比
    start_date="20260901",
    end_date="20261016",    # 换成最近一个交易日
)
bar = bar.sort_values("trade_date")   # 返回按日期倒序，画图前要排成 旧 → 新
```

把第 1 节的 `st.line_chart(prices...)` 换成：

```python
st.subheader("后复权收盘价走势")
st.line_chart(bar.set_index("trade_date")["close"])
```

✅ **检查**：为什么画图用后复权（`adj="hfq"`）而不是原始价？
答：分红、送股会在原始价上制造"假跳空"（价格突然掉一截但不是下跌）；后复权把它修回去，走势才连续可比——展示行情的标准做法。

**✅ 过关验收**：网页上的折线图变成真实后复权收盘价；换一只 `ts_code` 再跑，曲线跟着变。

**💣 常见坑**：图是"倒着"的（新 → 旧）→ 忘了 `sort_values("trade_date")`；报"积分不足"→ 见环境准备里公用 token 的限频说明；`OSError: ERROR.`**（就这两个词，看不出原因）**→ 九成是 token 没配好：`.env` 里 `TUSHARE_TOKEN=` 后面是空的、多了空格引号，或文件不在运行目录。tushare 会把真实报错（如"您的token不对"）**藏在终端的 print 里**、最后只抛这个笼统的 ERROR——先去终端往上翻找那行小字，再检查 `.env`。

## 2.2 每日指标：预测的原材料（25 分钟）

接口文档：[https://tushare.pro/document/2?doc_id=32](https://tushare.pro/document/2?doc_id=32)

**单日取数**（先在 notebook 里试，再搬进 `app.py`）：

```python
pro = ts.pro_api()
df = pro.daily_basic(
    ts_code="000001.SZ",
    trade_date="20261016",   # 换成最近一个交易日
    fields="ts_code,trade_date,turnover_rate,volume_ratio,pe,pb",
)
```

**倒推取 5 天**——`Timestamp`/`Timedelta` 正好接 W6；**"循环取数 + 容错跳过"是接 API 的通用套路**（非交易日没数据，跳过继续）：

```python
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
```

**🔍 逐行拆解（别跳过——这里的每一招 W4/W5/W6 都见过）**：


| 代码                             | 在做什么                              | 接哪周的旧知识                      |
| ------------------------------ | --------------------------------- | ---------------------------- |
| `df = pd.DataFrame()`          | 造一个**空表**当收集容器                    | W5 建空 DataFrame              |
| `today - pd.Timedelta(days=i)` | 日期减法：今天往前推 i 天                    | W6 的 `Timestamp`/`Timedelta` |
| `.strftime("%Y%m%d")`          | 日期 → `20261016` 格式字符串（API 只认这个格式） | W6 的日期格式化                    |
| `pd.concat([df, daily])`       | **数据拼接**：把新取的一行"接"到表尾，像接水管        | W4 翻页采集时的累积套路                |
| `ignore_index=True`            | 拼接后重排行号（0,1,2,…），不保留两段各自的旧索引      | W4/W5 用过                     |
| `if len(df) >= 5: break`       | **够 5 天就停**——不多取、不浪费 API 次数       | —                            |


**📎 数据拼接值得单独说**（`pd.concat` 是本周之后反复要用的积木）：

- `pd.concat([表1, 表2])` 默认**竖着接**（一行行摞起来，`axis=0`）——适合"多次取数、越接越长"；横着接用 `axis=1`（并排加列）
- 常见变体：`pd.concat([df1, df2], ignore_index=True)` 忽略旧索引；去重加 `df.drop_duplicates()`
- 动手试（30 秒）：在 notebook 里造两张小表 concat 起来，`ignore_index` 分别用 True/False 各跑一次，**对比行号列的区别**——看一眼胜过背十遍
- 生活类比：循环取数 = 拿着桶一趟趟去井里打水；`pd.concat` = 每趟倒进同一个大缸；`break` = 缸满了就收工

**✅ 检查**：为什么循环 10 次却只要 5 天数据？
答：周末和节假日没有交易数据（`daily.empty` 为真，跳过）；倒推 10 个自然日最多能覆盖 5-6 个交易日。这也是为什么有 `if len(df) >= 5: break`——取够了立刻停，**省 API 调用次数**（公用 token 有频次限制，每一句都在省着用）。

用 `st.dataframe(df)` 把 5 日指标也展示到网页上（`prices[name]` 那套演示数据可以删了——行情图已由 2.1 的后复权收盘价接管）。

**✅ 过关验收**：网页表格里出现 5 行真实数据，列是 `ts_code, trade_date, turnover_rate, volume_ratio, pe, pb`；换一只 `ts_code` 再跑，数据跟着变。

**💣 常见坑**：取到 0 行 → `trade_date` 是非交易日/未来日期，或 token 积分不够该接口（看报错）；`None` 密钥 → `.env` 没写对（等号两边别加空格），或文件不在运行目录；**全班同时用公用 token 报频次限制** → 换时段再试，或改用自己的 token。

✅ **检查**：为什么行情图和预测用两个接口？
答：`pro_bar` 给的是**价格**（展示用，后复权保证连续）；`daily_basic` 给的是**估值/交易指标**（PE、换手率等，信息量大，适合当预测的 materials）。各取所长。

## 2.3 跑通大模型对话（10 分钟）

**先 hello 再谈业务**：

```python
from openai import OpenAI

def llm_chat(prompt):
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content
```

**显示到页面上**（`print` 只会打到终端；这是产品——用 `st.write` 让浏览器里的用户看到）：

```python
st.subheader("打招呼测试")
st.write(llm_chat("hello"))
```

👀 **观察**：浏览器页面上出现大模型的回复（约等几秒）。第一次连通的"魔法时刻"——你的网页会"说话"了。

✅ **检查**：`print` 和 `st.write` 的区别？
答：`print` 输出到**终端**（只有跑程序的你看得见）；`st.write` 输出到**网页**（打开页面的用户都看得见）。本周主题就是从实验室走向店面——从现在起，给用户看的输出都用 `st.xxx`。

> 报错排查：`api_key=None`/401 → `DEEPSEEK_API_KEY` 没在 `.env` 里填或没保存；超时 → 网络问题重试。

> 换厂商（豆包等兼容 OpenAI 接口的服务）只需改 `base_url`、模型名和 `.env` 里的 key 名。



## 2.4 构造预测 prompt（25 分钟）

三要素：**问题**（第五个交易日涨还是跌）+ **判断标准** + **materials**（你的数据）：

```python
firm_name = "平安银行"
question = f"will future price of this stock {firm_name} moves up or down in the subsequent fifth trading day?"
resolution_criteria = "预测的判断标准：股票价格在随后的第五个交易日是否高于或低于当前价格。"
materials = str(df.to_dict(orient="records"))
```

**然后是输出规范**——你要的不只是"一段分析文字"，而是**程序能解析的固定格式**。三要素之后在 prompt 里追加（完整版从 `streamlit.ipynb`「构造预测prompt，并预测」或 `cases/app.py` 的 `build_prompt()` 复制，不要凭记忆默写）：

```python
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
```

输出规范拆开看就是三条，每条都有明确用途：

| 规范（写在 prompt 里） | 用途（写在代码里） |
|---|---|
| `in JSON format with keys: up and down` | 3.1 才能放心用 `prediction['up']` 取值 |
| `the sum of up and down probabilities must equal to 1` | 验收时检查 `up + down ≈ 1`，概率不合法一眼识破 |
| `回答问题用中文` | 用户（中文读者）能直接看懂分析过程 |

**⚠️ key 由谁定？由你在 prompt 里定。** 后面 3.1 要用 `prediction['up']` / `prediction['down']` 取值——**key 必须不多不少正好是 `up` 和 `down`**，否则 `KeyError`。这是"程序化消费 AI 输出"的第一课：

- prompt 里**没写死 key** → 模型可能给你 `{"上涨": ..., "下跌": ...}` 或 `{"upward": ..., "downward": ...}`，`prediction['up']` 直接崩
- 契约写了**但没兜底** → 模型偶尔不守约，所以 3.1 的 `extract_json` 之后还要 try/except + `prediction.get("up", 0)`
- 📎 同思想第 3 节还会遇到：让 AI 组装代码时"保留我的函数不动"也是在定契约

**指令完整版从** `streamlit.ipynb`**「构造预测prompt，并预测」一节复制**（或从 `cases/app.py` 的 `build_prompt()` 复制），不要自己凭记忆默写。

**🔍 逐个拆解 `materials = str(df.to_dict(orient="records"))`**——这行是把你的数据"翻译"给大模型的关键一步，从里往外读：

```python
df.to_dict(orient="records")   # ① DataFrame → list[dict]，每一行变成一个字典
str(...)                       # ② Python 对象 → 字符串
```

**① `df.to_dict(orient="records")`**——DataFrame 变成"一行一个字典"的列表：

```python
# 假设 df 长这样（2 行 × 3 列）:
#    ts_code    trade_date   pe
# 0  000001.SZ  20261016    6.85
# 1  000001.SZ  20261015    6.90

df.to_dict(orient="records")
# 变成:
# [{'ts_code': '000001.SZ', 'trade_date': '20261016', 'pe': 6.85},
#  {'ts_code': '000001.SZ', 'trade_date': '20261015', 'pe': 6.90}]
```

- `orient` 参数决定"变什么形状"：`"records"` = **每行一个字典**（最常用于喂给大模型/写 JSON）；对比 `"list"` = 每列一个列表。**为什么要 records？** 因为"一条记录 = 一个字典"的形状，和人类阅读表格的方式一致，大模型最容易看懂
- 动手试（30 秒）：在 notebook 里对你自己的 `df` 跑一遍 `df.to_dict(orient="records")`，肉眼对比原表格——确认每一行去哪了

**② `str(...)`**——为什么还要转字符串？

- prompt 是一个**纯文本**（f-string），`{materials}` 塞进去时 Python 会自动调 `str()`——所以这一步严格说可省，但**显式写出来是在提醒自己：从这里开始，结构化数据变成了文本的一部分**
- 这一步就是"数据 → 大模型"的**翻译边界**：DataFrame（机器友好的表格）→ 字符串（语言模型唯一能读的东西）

✅ **检查**：为什么不让大模型直接读 DataFrame？
答：大模型没有"表格"这个器官——它的输入只能是文本。`to_dict(orient="records")` 把表格变成"一行一个字典"的文本，是最保真、最不易歧义的翻译方式（对比 `print(df)` 会丢列名对齐，转 markdown 表格又多此一举）。**给 AI 喂数据 = 选一种它读得懂的格式**——这个思想在以后每次"程序 × 大模型"的场合都会复用。

```python
answer = llm_chat(prompt)

# 显示到页面上（给用户看 AI 的完整分析；print 只到终端）
st.subheader("AI 预测（原始回复）")
st.write(answer)   # 肉眼检查：末尾应有 {"up": 0.xx, "down": 0.xx}
```

**✅ 过关验收**：`answer` 末尾有形如 `{"up": 0.35, "down": 0.65}` 的 JSON；`up + down ≈ 1`。

**💾 存档点 2**：取数 → 预测全链已在脚本里跑通。commit。

---



# 课后练习任务 · 组装 APP + AI 辅助编程

基础篇到此为止：你的页面已能展示真实行情图 + 5 日指标表 + AI 预测回复。**最后一步——把这些零件组装成完整产品（侧栏选股票 → 点按钮 → 自动取数 → AI 预测 → 概率展示），并全程用 AI 辅助编程完成主体代码**——按升级版实验文档 `week07-streamlit-app-advanced.md` 推进：

1. **提取 JSON**：正则从 AI 长回复中抠出 `{"up": ..., "down": ...}`，指标卡上屏
2. **手写骨架**（约 20 行，必须自己写）：侧栏 + 按钮 + 全链路编排
3. **AI 组装**：把零件 + 骨架交给 Cursor/OpenCode——你当架构师，AI 当施工队
4. **验收 AI 产出**：换股票复跑、失败不崩、**找出必须手改的 1-2 处**（评分点）

对照成品：`weeks/week07/cases/app.py`。进阶挑战（部署上线 / 加指标 / session_state / 缓存）也在升级版文档里。

**💾 存档点 3**：这就是你的实验成品。commit。

---

## 实验报告（不需要课后提交）

本实验**不交报告**——按下面六项自查留档，教师按需抽查（运行演示 + 口头问答，问的就是这几项）：

1. **实验目标与完成度**：基础篇两节 + 升级篇课后任务，各过了验收点没有，每段一句话说它给了你什么
2. **关键过程截图**：各段过关验收点 1-2 张（迷你查看器联动 / 真数据表 + 预测 JSON / 完整 APP 换股票复跑）
3. **踩坑记录**（1-3 条）：什么坑、报错长什么样
4. **解决经验**：问了 AI、互助小组还是课程群？具体怎么解决的
5. **AI 辅助编程记录**（升级篇）：你给 AI 的关键提示词、AI 哪里写错了/不符合预期、**你手改了哪 1-2 处、为什么**
6. **一句话反思**：用你自己的话说"Streamlit 是什么"（不超过两句）

⚠️ 不交报告 ≠ 没有验收：**APP 必须可运行**（自检达标线见下），课堂/课随时可能被邀请演示。

## 自检（达标线）

- [ ] APP 能在浏览器打开，换股票后预测结果跟着变
- [ ] 密钥在 `.env` 里，代码和截图里都看不到明文 key
- [ ] 我能指着代码说出"联动"是哪几行实现的（用"widget 返回值筛选数据"的语言）
- [ ] AI 生成的代码里，我手改过的地方我能讲清为什么
- [ ] 六项自查留档齐全，截图对得上验收点



## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

预计卡点集中在：`.env` 配置、tushare 取到 0 行（基础篇对应小节）、JSON 提取失败（升级篇步骤 1）——先回对应位置看 💣 常见坑。