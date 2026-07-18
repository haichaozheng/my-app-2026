# EDA多视角分析

> **引入时机**：W6 | **核心挑战**："只看均值和分布不够，如何从多个角度发现规律？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

很多同学做EDA就是画个直方图、算个均值标准差，然后说"探索完了"。这不是EDA，这是走过场。真正的EDA是从多个视角审视数据，像侦探一样寻找线索、发现异常、形成假设。单一的视角会让你遗漏重要信息——分布正常不代表没有异常值，趋势向上不代表没有结构性变化。

在金融数据分析中，多视角EDA更是必不可少。股票数据需要从时间趋势、横截面对比、行业分布、异常事件等多个角度分析，否则你可能漏掉关键的行业轮动信号或个股异常。养成多视角EDA的习惯，你的分析深度会产生质的飞跃。

## 这个知识点的核心内容

### 五大EDA视角

系统性的EDA应从五个互补视角展开：

1. **分布视角**：数据的集中趋势、离散程度、偏态和峰态
   - 直方图、核密度图、QQ图
   - 关注：是否正态、是否有双峰、尾部有多厚

2. **相关视角**：变量之间的关联关系
   - 相关矩阵热力图、散点图矩阵
   - 关注：哪些变量强相关、相关关系是否稳定

3. **趋势视角**：随时间变化的规律
   - 折线图、滚动统计量、趋势分解
   - 关注：是否有趋势、是否有周期性、是否有结构断点

4. **比较视角**：分组之间的差异
   - 箱线图、分组柱状图、小提琴图
   - 关注：组间差异是否显著、组内方差是否一致

5. **异常视角**：偏离正常模式的观测值
   - 异常值标记、残差图、孤立点检测
   - 关注：异常是数据错误还是重要信号

### EDA检查清单

对每个数据集，系统性地走完以下清单：

- [ ] 数据概览：形状、列名、数据类型、缺失情况
- [ ] 单变量分布：每个数值列的均值/中位数/分位数/极值
- [ ] 双变量关系：关键变量间的散点图和相关系数
- [ ] 时间趋势：时间序列的走势、滚动统计、趋势分解
- [ ] 分组比较：按类别变量分组的统计差异
- [ ] 异常检测：离群值的位置和可能原因
- [ ] 缺失模式：缺失值是否集中出现在某些时间段或分组

### 从EDA到假设

EDA的目标不是产出图表，而是形成分析假设：

- 分布视角发现双峰 → 假设：数据包含两个子群体
- 相关视角发现某相关系数突然变化 → 假设：发生了结构性变化
- 趋势视角发现周期性 → 假设：存在季节性因素
- 比较视角发现组间差异 → 假设：分组变量有解释力
- 异常视角发现极端值聚集 → 假设：存在系统性风险事件

每个假设都应该可测试——后续用正式的统计方法验证。

### EDA的可视化最佳实践

- **一张图只传达一个信息**：不要把所有东西塞进一张图
- **标注关键发现**：用箭头、文字标注让读者一眼看到重点
- **用颜色有意义**：颜色编码表示分类，而非装饰
- **控制信息密度**：数据点太多时用采样或聚合
- **保持一致性**：同一报告中相同含义使用相同颜色和符号

### 自动化EDA工具

当数据维度较多时，可以用自动化工具快速生成概览：

```python
# ydata-profiling：一键生成EDA报告
from ydata_profiling import ProfileReport
profile = ProfileReport(df, title="A股银行板块EDA报告")
profile.to_file("eda_report.html")

# 自定义快速EDA函数
def quick_eda(df, date_col="date", group_col="code", value_cols=None):
    if value_cols is None:
        value_cols = df.select_dtypes(include="number").columns.tolist()

    print(f"数据形状: {df.shape}")
    print(f"时间范围: {df[date_col].min()} ~ {df[date_col].max()}")
    print(f"分组数量: {df[group_col].nunique()}")
    print(f"\n数值列统计:")
    print(df[value_cols].describe())
    print(f"\n缺失值比例:")
    print(df[value_cols].isnull().mean())
```

## 关键细节与易错点

- **误区：EDA就是画画图**。EDA的核心是"探索"和"发现"，画图只是手段，形成假设才是目的
- **误区：EDA做一次就够了**。随着分析的深入，应该反复回到EDA，用新的视角审视数据
- **易错：只看全局统计忽略分组**。全局均值可能掩盖组间巨大差异
- **易错：相关系数低就认为变量无关**。非线性关系无法被皮尔逊相关系数捕获
- **易错：发现异常值就删除**。金融数据中异常值往往是最有价值的信号

## 金融数据分析示例

对A股银行板块进行完整的多视角EDA：

```python
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 获取数据
codes = {
    "601398": "工商银行", "601939": "建设银行",
    "601288": "农业银行", "601988": "中国银行",
    "600036": "招商银行", "601166": "兴业银行",
    "600000": "浦发银行", "601328": "交通银行"
}

all_data = []
for code, name in codes.items():
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                            start_date="20200101", end_date="20241231", adjust="hfq")
    df["code"] = code
    df["name"] = name
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
data["date"] = pd.to_datetime(data["日期"])
data.rename(columns={"收盘": "close", "成交量": "volume"}, inplace=True)
data["return"] = data.groupby("code")["close"].pct_change()

# === 视角1：分布 ===
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
data["return"].dropna().hist(bins=100, ax=axes[0])
axes[0].set_title("日收益率分布")
axes[0].axvline(0, color="red", linestyle="--")

# 按银行分组的收益率分布
for name in data["name"].unique():
    subset = data[data["name"] == name]["return"].dropna()
    sns.kdeplot(subset, ax=axes[1], label=name)
axes[1].set_title("各银行日收益率核密度")
axes[1].legend(fontsize=7)

# === 视角2：相关 ===
returns_wide = data.pivot_table(values="return", index="date", columns="name")
corr = returns_wide.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("银行股收益率相关矩阵")

# === 视角3：趋势 ===
fig, ax = plt.subplots(figsize=(14, 5))
for name in data["name"].unique():
    subset = data[data["name"] == name].set_index("date")["close"]
    subset.plot(ax=ax, label=name)
ax.set_title("银行股价格走势（前复权）")
ax.legend(fontsize=7)

# 滚动波动率
data["rolling_vol"] = data.groupby("code")["return"].transform(
    lambda x: x.rolling(20).std() * np.sqrt(252)
)

# === 视角4：比较 ===
plt.figure(figsize=(10, 5))
data.boxplot(column="return", by="name", figsize=(10, 5))
plt.title("各银行日收益率分布对比")
plt.suptitle("")

# 年度收益率对比
annual = data.copy()
annual["year"] = annual["date"].dt.year
annual_ret = annual.groupby(["year", "name"])["return"].apply(
    lambda x: (1 + x).prod() - 1
).unstack()
annual_ret.plot(kind="bar", figsize=(12, 5))
plt.title("各银行年度收益率对比")

# === 视角5：异常 ===
extreme_days = data[data["return"].abs() > 0.05]
print(f"单日涨跌超5%的天数：{len(extreme_days)}")
print(extreme_days[["date", "name", "return"]].sort_values("return"))
```

## 拓展学习

- 《Exploratory Data Analysis》——John Tukey（EDA提出者）的经典著作
- 《R for Data Science》EDA章节——Hadley Wickham的EDA方法论
- ydata-profiling库——自动化EDA报告生成
- seaborn官方Gallery——统计可视化最佳实践
- 《The Visual Display of Quantitative Information》——Tufte的数据可视化经典

## 参考链接

- https://www.kaggle.com/learn — EDA完整指南和Notebook
- https://seaborn.pydata.org/examples/index.html — Seaborn图表画廊
- https://ydata-profiling.ydata.ai/ — ydata-profiling自动化EDA工具
- https://www.amazon.com/Exploratory-Data-Analysis-John-Tukey/dp/0201076160 — Tukey的EDA经典著作
