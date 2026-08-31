# Pandas高级操作

> **引入时机**：W5 | **核心挑战**："数据量大、格式复杂，如何高效处理金融数据？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

当你开始做真实的金融数据分析项目时，Pandas基础操作（读取CSV、筛选行、选择列）远远不够。真实的金融数据是多年的、多标的、多频率的，你需要groupby做分组聚合、多级索引处理面板数据、时间序列操作计算收益率和均线、pivot_table做宽表长表转换。没有这些高级操作能力，你会在数据处理环节卡住，无法进入真正的分析阶段。

金融数据天然是时间序列+面板结构——多只股票、多个指标、跨越多年。Pandas的高级操作恰恰是为这类数据设计的。掌握这些操作，你处理多年A股数据就像处理单只股票一样轻松。

## 这个知识点的核心内容

### Groupby分组聚合

Groupby是数据分析中使用频率最高的操作之一，核心逻辑是"拆分-应用-合并"：

```python
import pandas as pd

# 按行业分组计算平均PE
df.groupby("industry")["PE"].mean()

# 多列聚合
df.groupby("industry").agg({
    "PE": ["mean", "median", "std"],
    "market_cap": "sum"
})

# 自定义聚合函数
df.groupby("industry")["revenue"].agg(
    growth_rate=lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]
)
```

常见陷阱：groupby后默认将分组列设为索引，如需保留为普通列使用 `as_index=False` 或 `.reset_index()`。

### 多级索引（MultiIndex）

金融面板数据天然适合多级索引——股票代码+日期、行业+公司+季度：

```python
# 构建多级索引
index = pd.MultiIndex.from_product(
    [["601398", "600036"], pd.date_range("2024-01-01", periods=5)],
    names=["stock", "date"]
)

# 多级索引的选择操作
df.loc[("601398", slice(None)), :]  # 选某只股票所有日期
df.xs("2024-01-02", level="date")  # 选某一天所有股票

# 多级索引的聚合
df.groupby(level="stock").mean()  # 按股票分组
```

关键操作：`stack()`/`unstack()` 在多级索引和列之间转换，`swaplevel()` 交换索引层级顺序。

### 时间序列操作

Pandas时间序列操作是金融数据分析的核心武器：

```python
# 日期解析与设置
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# 重采样：日频→月频
monthly = df.resample("M").last()  # 取月末值
monthly_return = df["close"].resample("M").last().pct_change()

# 滚动计算
df["MA20"] = df["close"].rolling(window=20).mean()
df["volatility"] = df["return"].rolling(window=20).std()
df["max_drawdown"] = df["close"].rolling(window=60).apply(
    lambda x: (x.iloc[-1] / x.max()) - 1
)

# 偏移操作
df["prev_close"] = df["close"].shift(1)
df["return"] = df["close"].pct_change()  # 等价于 (close - close.shift(1)) / close.shift(1)
df["lead_return"] = df["return"].shift(-1)  # 未来收益率
```

resample频率代码：`D`日、`W`周、`M`月末、`Q`季末、`Y`年末、`B`工作日。

### Pivot Table与宽长表转换

金融数据经常需要在宽表（每只股票一列）和长表（每行一个观测值）之间转换：

```python
# 长表→宽表
wide = df.pivot_table(
    values="close",
    index="date",
    columns="stock_code",
    aggfunc="last"
)

# 宽表→长表
long = wide.reset_index().melt(
    id_vars="date",
    var_name="stock_code",
    value_name="close"
)

# 带聚合的透视表
pd.pivot_table(
    df,
    values="return",
    index="industry",
    columns="year",
    aggfunc=["mean", "std"]
)
```

### 大数据集处理策略

当数据量超过内存时：

- **分块读取**：`pd.read_csv("file.csv", chunksize=10000)`
- **指定列类型**：`dtype={"stock_code": "category", "volume": "int32"}`，节省50%+内存
- **使用category类型**：低基数字符串列（如行业、交易所）
- **筛选后处理**：先筛选需要的行和列，再做复杂计算
- **使用eval**：`pd.eval()` 利用NumPy加速大表达式计算

```python
# 高效读取大文件
dtypes = {
    "code": "category",
    "industry": "category",
    "close": "float32",
    "volume": "int32"
}
df = pd.read_csv("ashare_daily.csv", dtype=dtypes, parse_dates=["date"])

# 分块处理
results = []
for chunk in pd.read_csv("big_file.csv", chunksize=50000):
    results.append(chunk.groupby("code")["close"].mean())
final = pd.concat(results).groupby(level=0).mean()
```

## 关键细节与易错点

- **易错：rolling窗口默认包含NaN**。前19个MA20值为NaN，绘图和分析时需注意
- **易错：resample的"M"取月末最后一个交易日**。如果用`mean()`则取月内均值，逻辑完全不同
- **易错：groupby后忘记reset_index**。导致后续merge或选择操作出错
- **易错：pivot_table在有重复索引时报错**。需确认aggfunc参数是否正确
- **易错：shift的方向混淆**。shift(1)是向下移（取前一天的值），shift(-1)是向上移（取后一天的值）

## 金融数据分析示例

处理多年A股银行板块日线数据，计算月度收益率和滚动波动率：

```python
import akshare as ak
import pandas as pd

# 获取多只银行股数据
bank_codes = {
    "601398": "工商银行",
    "601939": "建设银行",
    "601288": "农业银行",
    "601988": "中国银行",
    "600036": "招商银行"
}

all_data = []
for code, name in bank_codes.items():
    df = ak.stock_zh_a_hist(
        symbol=code, period="daily",
        start_date="20200101", end_date="20241231"
    )
    df["code"] = code
    df["name"] = name
    df["date"] = pd.to_datetime(df["日期"])
    all_data.append(df[["date", "code", "name", "收盘", "成交量"]])

data = pd.concat(all_data, ignore_index=True)
data.rename(columns={"收盘": "close", "成交量": "volume"}, inplace=True)
data = data.set_index("date")

# 日收益率
data["daily_return"] = data.groupby("code")["close"].pct_change()

# 20日滚动波动率（年化）
data["rolling_vol"] = (
    data.groupby("code")["daily_return"]
    .rolling(window=20)
    .std()
    .reset_index(level=0, drop=True) * (252 ** 0.5)
)

# 月度收益率
monthly_close = data.groupby("code")["close"].resample("M").last()
monthly_return = monthly_close.groupby("code").pct_change()

# 行业横截面统计
cross_section = data.groupby(["date", "name"])["daily_return"].mean().unstack()
correlation = cross_section.corr()
print("银行股收益率相关矩阵：")
print(correlation)

# 年度表现汇总
annual_summary = (
    data.groupby([data.index.year, "name"])
    .agg(
        total_return=("daily_return", lambda x: (1 + x).prod() - 1),
        volatility=("daily_return", "std"),
        avg_volume=("volume", "mean")
    )
)
print("\n年度表现汇总：")
print(annual_summary)
```

## 拓展学习

- 《Python for Data Analysis》第2版——Wes McKinney（Pandas作者）亲著
- Pandas官方User Guide的时间序列章节——最权威的时间序列操作参考
- 《Effective Pandas》——Matt Harrison著，Pandas高效使用模式
- Vaex库：处理超大数据集（>1亿行）的Pandas替代方案
- Polars库：Rust实现的高性能DataFrame库，API与Pandas类似但速度快10倍+

## 参考链接

- https://pandas.pydata.org/docs/user_guide/timeseries.html — Pandas时间序列官方文档
- https://pandas.pydata.org/docs/user_guide/groupby.html — Pandas GroupBy官方文档
- https://pandas.pydata.org/docs/user_guide/reshaping.html — Pandas数据重塑（pivot/melt/stack）官方文档
- https://matplotlib.org/stable/gallery/index.html — Matplotlib图表画廊，配合Pandas可视化
