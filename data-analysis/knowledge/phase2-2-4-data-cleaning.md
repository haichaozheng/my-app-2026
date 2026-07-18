# 数据清洗方法论

> **引入时机**：W6 | **核心挑战**："数据有缺失值、异常值、格式混乱" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

真实世界的数据从来不干净。当你从AKShare获取A股数据时，会遇到停牌日数据缺失、复权因子不一致、财报日期错位等问题；当你爬取网页数据时，会遇到格式不统一、编码错误、HTML标签混入等问题。如果你不先做数据清洗，后续所有分析都建立在错误的数据基础上——垃圾进，垃圾出。

金融数据的清洗有其特殊性和专业性。停牌处理、复权计算、财报日期对齐这些操作，在通用数据清洗教程中找不到，但却是金融数据分析的必备技能。掌握这些方法论，你的分析结果才经得起推敲。

## 这个知识点的核心内容

### 缺失值处理策略

缺失值不是简单的"删除或填充"，需要根据缺失原因选择策略：

- **完全随机缺失（MCAR）**：缺失与任何变量无关 → 可安全删除
- **随机缺失（MAR）**：缺失与已观测变量有关 → 用已观测值建模填充
- **非随机缺失（MNAR）**：缺失与未观测值本身有关 → 需要领域知识处理

```python
# 检查缺失情况
df.isnull().sum()
df.isnull().mean()  # 缺失比例

# 删除策略
df.dropna()  # 删除任何含缺失值的行
df.dropna(subset=["close"])  # 只看close列

# 填充策略
df["close"].fillna(method="ffill")  # 前值填充（金融时序常用）
df["close"].interpolate(method="time")  # 时间插值
df["volume"].fillna(0)  # 成交量填0（停牌日）

# 分组填充
df["close"] = df.groupby("code")["close"].fillna(method="ffill")
```

### 异常值检测与处理

金融数据中的异常值有两类：数据错误和真实极端值。处理前必须先判断属于哪一类：

```python
# 统计方法检测
Q1 = df["return"].quantile(0.25)
Q3 = df["return"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df["return"] < lower) | (df["return"] > upper)]

# Z-Score方法
from scipy import stats
z_scores = stats.zscore(df["return"].dropna())
outliers = df[np.abs(z_scores) > 3]

# 涨跌停限制检测（A股±10%，ST股±5%）
suspicious = df[
    (df["return"].abs() > 0.11) & (~df["code"].str.startswith("ST"))
]
```

处理方式：确认是数据错误→修正或删除；确认是真实极端值→保留，但分析时注意其影响。

### 格式规范化

金融数据格式混乱是常态，常见问题：

```python
# 日期格式统一
df["date"] = pd.to_datetime(df["date"], format="mixed")

# 百分比字符串→数值
df["pe_ratio"] = df["pe_ratio"].str.rstrip("%").astype(float) / 100

# 货币格式→数值
df["amount"] = df["amount"].str.replace(",", "").str.replace("¥", "").astype(float)

# 股票代码统一为6位
df["code"] = df["code"].astype(str).str.zfill(6)

# 行业分类统一
industry_map = {"银行Ⅰ": "银行", "银行业": "银行", "BANK": "银行"}
df["industry"] = df["industry"].map(industry_map).fillna(df["industry"])
```

### 金融数据特有清洗

**停牌处理**：

```python
# 识别停牌日：成交量为0或数据缺失
df["is_suspended"] = df["volume"] == 0

# 停牌日收益率设为0（而非NaN）
df.loc[df["is_suspended"], "return"] = 0

# 停牌期间前值填充收盘价
df["close"] = df.groupby("code")["close"].fillna(method="ffill")
```

**复权处理**：

```python
# 后复权价格 = 原始价格 × 复权因子
# 前复权价格：当前价格不变，历史价格向下调整
# 计算收益率必须使用复权价格
df["adj_close"] = df["close"] * df["adj_factor"]
df["return"] = df.groupby("code")["adj_close"].pct_change()
```

**财报日期对齐**：

```python
# 问题：不同公司Q3财报披露日期不同（10月-11月）
# 解决：统一对齐到报告期而非披露期
financial["report_period"] = pd.to_datetime(financial["report_date"])
financial["disclosure_date"] = pd.to_datetime(financial["disclosure_date"])

# 按报告期聚合
quarterly = financial.groupby(["code", "report_period"]).last()
```

### 数据质量检查清单

完成清洗后，用此清单验证：

- [ ] 缺失值比例是否在可接受范围（<5%为佳）
- [ ] 数值列是否有非数值混入
- [ ] 日期列是否全部为有效日期
- [ ] 收益率是否在合理范围（A股日收益率绝对值通常<10%）
- [ ] 停牌日是否已正确处理
- [ ] 复权价格是否正确（复权后历史价格应连续无跳空）
- [ ] 分组操作是否正确（groupby后未跨股票计算）

## 关键细节与易错点

- **易错：直接删除所有缺失值**。金融时序数据删除一天会导致整个时间链断裂，应优先填充
- **易错：用均值填充收益率缺失值**。收益率缺失通常意味着停牌，应填0而非均值
- **易错：用未复权价格计算收益率**。除权除息日会产生虚假的暴跌信号
- **易错：跨股票groupby时未按股票分组**。导致用A股票的收盘价填充B股票的缺失值
- **易错：异常值一律删除**。金融数据中的极端值往往最有信息量（如暴跌日、财报超预期日）

## 金融数据分析示例

清洗A股银行板块数据，处理停牌和异常值：

```python
import akshare as ak
import pandas as pd
import numpy as np

# 获取原始数据
codes = ["601398", "600036", "601166"]
all_data = []
for code in codes:
    df = ak.stock_zh_a_hist(
        symbol=code, period="daily",
        start_date="20200101", end_date="20241231",
        adjust="hfq"  # 前复权
    )
    df["code"] = code
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
data["date"] = pd.to_datetime(data["日期"])
data.rename(columns={"收盘": "close", "成交量": "volume", "最高": "high", "最低": "low"}, inplace=True)

# Step 1: 检查缺失值
print("缺失值统计：")
print(data[["close", "volume", "high", "low"]].isnull().sum())

# Step 2: 识别并处理停牌
data["is_suspended"] = data["volume"] == 0
print(f"\n停牌日数量：{data['is_suspended'].sum()}")

# 停牌日：前值填充收盘价，收益率设为0
data = data.sort_values(["code", "date"])
data["close"] = data.groupby("code")["close"].fillna(method="ffill")

# Step 3: 计算收益率
data["return"] = data.groupby("code")["close"].pct_change()
data.loc[data["is_suspended"], "return"] = 0

# Step 4: 异常值检测
print("\n收益率统计：")
print(data["return"].describe())

# 检测超出涨跌停限制的异常值
extreme = data[data["return"].abs() > 0.11]
print(f"\n超出涨跌限制的记录：{len(extreme)}条")
if len(extreme) > 0:
    print(extreme[["code", "date", "close", "return"]])

# Step 5: 格式规范化
data["code"] = data["code"].astype(str).str.zfill(6)

# Step 6: 最终质量检查
print(f"\n数据范围：{data['date'].min()} 至 {data['date'].max()}")
print(f"股票数量：{data['code'].nunique()}")
print(f"缺失值比例：{data.isnull().mean().max():.2%}")
```

## 拓展学习

- 《Python for Finance》数据清洗章节——金融数据清洗的专业方法
- great_expectations库——数据质量自动化测试框架
- pandas-profiling库——一键生成数据质量报告
- 《Doing Data Science》——从实践角度理解数据清洗的重要性
- Data Linting概念——像代码lint一样自动检测数据问题

## 参考链接

- https://pandas.pydata.org/docs/user_guide/missing_data.html — Pandas缺失值处理官方文档
- https://docs.greatexpectations.io/docs/ — Great Expectations数据质量测试框架
- https://ydata-profiling.ydata.ai/ — Pandas Profiling自动数据报告工具
- https://scikit-learn.org/stable/modules/impute.html — Scikit-learn缺失值填充方法
