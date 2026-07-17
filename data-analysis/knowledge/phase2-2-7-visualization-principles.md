# 可视化设计原则

> **引入时机**：W7 | **核心挑战**："为什么我的图表没人能看懂？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

你花了一整天做出的图表，别人看了3秒就关掉了——这不是别人的问题，是你的图表设计有问题。在金融数据分析产品中，可视化是用户最直接接触的界面，图表设计质量直接决定产品的可用性。选择错误的图表类型、滥用颜色、忽略标注、信息过载，这些都是让图表从"传达信息"变成"制造困惑"的常见原因。

金融可视化有其特殊惯例：K线图的红涨绿跌（中国市场）、热力图的冷暖色、收益率的正负色。违反这些惯例不仅让专业用户困惑，还可能导致信息误读。掌握可视化设计原则，让你的图表从"能画出来"升级为"能传达洞察"。

## 这个知识点的核心内容

### 图表类型选择指南

不同类型的数据和问题对应不同的图表类型：

| 目的 | 推荐图表 | 金融场景示例 |
|------|----------|-------------|
| 趋势变化 | 折线图 | 股价走势、收益率曲线 |
| 对比差异 | 柱状图/条形图 | 各银行年度营收对比 |
| 占比构成 | 堆叠柱状图/饼图 | 资产配置比例 |
| 分布特征 | 直方图/箱线图 | 收益率分布对比 |
| 相关关系 | 散点图/热力图 | 股票相关矩阵 |
| 多维数据 | 平行坐标/雷达图 | 银行多维指标对比 |
| 时序OHLC | K线图 | 股票价格走势（开高低收） |
| 排名变化 | 斜率图/哑铃图 | 银行排名年度变化 |

选择原则：能用简单图表就不要用复杂图表。折线图能表达的信息，不要用雷达图。

### 常见可视化错误

**错误1：3D图表**
3D效果看似酷炫，实则严重干扰数据读取。角度倾斜导致长度对比失真，遮挡导致信息丢失。

**错误2：双Y轴滥用**
双Y轴容易产生虚假关联。左轴股价0-50，右轴成交量0-10亿，读者会误以为两者同步变化。

**错误3：饼图切片过多**
超过5个切片的饼图难以比较大小。改用柱状图更清晰。

**错误4：忽略零基线**
柱状图的Y轴不从0开始会夸大差异。股价折线图可以从非零开始（因为关注变化率），但柱状图必须从0开始。

**错误5：信息过载**
一张图里画20条折线、5个图例、3个注释——读者根本无法处理这么多信息。

### 色彩理论在金融可视化中的应用

色彩是可视化中最容易被滥用、也最有力量的元素：

**色相选择**：
- 类别数据：使用色相差异明显的调色板（如Tableau 10）
- 顺序数据：使用同一色相的深浅渐变
- 发散数据：使用冷暖对比色（如红-蓝，或中国市场的红-绿）

**金融场景色彩惯例**：
- 涨跌：中国市场红涨绿跌，国际市场绿涨红跌——产品面向中国用户请用红涨绿跌
- 热力图：正相关暖色（红），负相关冷色（蓝）
- 风险等级：低风险绿色，高风险红色

**色盲友好**：约8%男性有红绿色盲，避免仅用红绿区分，增加形状或纹理编码。

```python
import matplotlib.pyplot as plt

# 色盲友好调色板
cblind_colors = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7"]

# 发散色图
from matplotlib.colors import TwoSlopeNorm
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
plt.imshow(corr_matrix, cmap="RdBu_r", norm=norm)
```

### 金融图表惯例

金融领域有成熟的可视化惯例，遵循惯例降低用户的认知负担：

- **K线图**：红涨绿跌（中国市场），阳线实体填充，阴线实体空心或填绿
- **收益率图**：正收益红色，负收益绿色
- **热力图**：RdBu_r色图，0为白色，正负分别冷暖色
- **均线图**：短期均线（如5日）用实线，长期均线（如60日）用虚线
- **成交量柱状图**：放在K线下方，涨日红色柱，跌日绿色柱

### 信息密度与可读性的平衡

- **数据墨水比**（Tufte）：最大化数据墨水，最小化非数据墨水
- 去掉不必要的网格线、边框、背景色
- 标注只标注关键信息，不要标注每个数据点
- 多图表时用子图而非叠在一起
- 合理使用缩放和聚焦：全局视图展示趋势，局部放大展示细节

## 关键细节与易错点

- **易错：折线图时间轴不连续**。节假日没有交易数据，但X轴不应该留空，需明确标注或跳过
- **易错：K线图用错复权类型**。前复权适合看历史走势，后复权适合算真实收益
- **易错：热力图色标不对称**。相关系数范围[-1,1]，色标中心必须设为0
- **易错：忽略图表尺寸和字体**。报告中图表太小看不清，演示中字体太小读不出
- **易错：用折线图画分类数据**。分类变量之间没有连续性，应使用柱状图

## 金融数据分析示例

正确选择图表类型展示银行板块分析结果：

```python
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 获取数据
codes = {
    "601398": "工商银行", "601939": "建设银行",
    "600036": "招商银行", "601166": "兴业银行",
    "601328": "交通银行", "600000": "浦发银行"
}

all_data = []
for code, name in codes.items():
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                            start_date="20230101", end_date="20241231", adjust="hfq")
    df["code"] = code
    df["name"] = name
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
data["date"] = pd.to_datetime(data["日期"])
data.rename(columns={"收盘": "close", "成交量": "volume"}, inplace=True)
data["return"] = data.groupby("code")["close"].pct_change()

# === 图1：折线图 - 趋势 ===
fig, ax = plt.subplots(figsize=(12, 5))
for name, group in data.groupby("name"):
    group.set_index("date")["close"].plot(ax=ax, label=name, linewidth=1)
ax.set_title("银行股价格走势（2023-2024）")
ax.set_ylabel("前复权收盘价")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, alpha=0.3)

# === 图2：热力图 - 相关 ===
returns_wide = data.pivot_table(values="return", index="date", columns="name")
corr = returns_wide.corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f",
            vmin=-1, vmax=1, square=True, ax=ax)
ax.set_title("银行股日收益率相关矩阵")

# === 图3：箱线图 - 分布对比 ===
fig, ax = plt.subplots(figsize=(10, 5))
returns_list = [data[data["name"] == name]["return"].dropna().values for name in data["name"].unique()]
bp = ax.boxplot(returns_list, labels=data["name"].unique(), patch_artist=True)
colors = ["#E74C3C" if np.median(v) >= 0 else "#27AE60" for v in returns_list]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax.set_title("各银行日收益率分布对比")
ax.set_ylabel("日收益率")
ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)

# === 图4：柱状图 - 年度对比 ===
data["year"] = data["date"].dt.year
annual_ret = data.groupby(["year", "name"])["return"].apply(
    lambda x: (1 + x).prod() - 1
).unstack()
fig, ax = plt.subplots(figsize=(10, 5))
annual_ret.plot(kind="bar", ax=ax, color=sns.color_palette("Set2", len(codes)))
ax.set_title("各银行年度收益率对比")
ax.set_ylabel("年度收益率")
ax.legend(fontsize=7, loc="upper left")
ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
plt.xticks(rotation=0)
```

## 拓展学习

- 《The Visual Display of Quantitative Information》——Edward Tufte的可视化圣经
- 《Storytelling with Data》——Cole Nussbaumer Knaflic，数据可视化叙事经典
- 《Fundamentals of Data Visualization》——Claus Wilke，开源可视化设计教材
- ColorBrewer——专业的地图和数据色彩方案工具
- Financial Visualization with Matplotlib——专门针对金融图表的教程

## 参考链接

- https://clauswilke.com/dataviz/ — 《Fundamentals of Data Visualization》在线版
- https://www.storytellingwithdata.com/ — Storytelling with Data博客和资源
- https://colorbrewer2.org/ — ColorBrewer色彩方案选择器
- https://r-graph-gallery.com/ — R图表画廊（设计思路跨语言通用）
