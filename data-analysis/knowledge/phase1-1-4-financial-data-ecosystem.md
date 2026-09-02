# 金融数据生态与获取

> **引入时机**：W2 | **核心挑战**：金融数据在哪里？怎么获取？有哪些API和数据源？ | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

每个金融数据分析项目的起点都是数据。没有数据，再好的分析思路也只是纸上谈兵。但很多同学在项目初期面对一个尴尬的局面：知道想做什么分析，却不知道去哪里获取数据。比如你想做"A股行业轮动分析"，需要行业分类、成分股列表、历史行情、财务数据——这些数据分散在不同的数据源中，格式各异，获取方式也不同。

金融数据生态是复杂且分层的：有免费的也有付费的，有实时延迟的也有历史回放的，有结构化API也有需要爬取的网页。了解这个生态的全貌，你才能根据项目需求选择最合适的数据源，避免"用大炮打蚊子"（付费获取本可免费得到的数据）或"缘木求鱼"（在不合适的数据源找特定数据）。

更重要的是，数据获取不是一次性事件，而是贯穿项目始终的基础工作。项目初期你可能只需要日线行情，但后期可能需要财务报表、宏观数据、另类数据等。对数据生态有整体认知，你在项目推进过程中就能从容应对各种数据需求，而不是每次都从零开始搜索。

## 这个知识点的核心内容

### 金融数据类型

金融数据可以按照内容和结构分为以下几类：

**市场数据（Market Data）**：反映证券交易价格和成交量的数据，是最基础也是最常用的数据类型。
- 行情数据：开盘价、最高价、最低价、收盘价、成交量、成交额（OHLCV）
- 盘口数据：买卖五档价格和挂单量（Level 1/Level 2）
- 分钟/日/周/月K线：不同时间粒度的聚合行情
- 指数数据：上证指数、沪深300、中证500等市场指数

**基本面数据（Fundamental Data）**：反映公司经营状况和财务健康的数据。
- 财务报表：资产负债表、利润表、现金流量表（季报/年报）
- 财务指标：PE、PB、ROE、毛利率、资产负债率等
- 分红送转：分红方案、除权除息日
- 股东数据：十大股东、股东人数变化

**另类数据（Alternative Data）**：非传统金融数据，用于获取增量信息。
- 新闻舆情：财经新闻、社交媒体情绪
- 卫星数据：停车场密度、航运轨迹
- 供应链数据：上下游企业关联
- 网络数据：搜索指数、App活跃度

**宏观数据（Macro Data）**：反映经济整体运行状况的数据。
- GDP、CPI、PPI、PMI等经济指标
- 货币政策：利率、M2、社融
- 进出口、固定资产投资等

### 数据源层级

金融数据源按照获取难度和成本可以分为以下层级：

| 层级 | 数据源 | 特点 | 适用场景 |
|------|--------|------|----------|
| 免费API | AKShare、Tushare（基础接口）、yfinance | 零成本，数据量有限制，可能有延迟 | 学习项目、原型验证 |
| 开源数据库 | TuShare Pro（积分制）、BaoStock | 需注册，数据较全，有一定限制 | 中等规模分析项目 |
| 付费数据 | Wind、Choice、聚源 | 成本高，数据全，质量有保障 | 专业量化研究 |
| 网页爬取 | 东方财富、新浪财经、同花顺、贝壳/链家、巨潮资讯 | 免费但不稳定，需注意合规 | 补充特定数据（详见 `phase1-1-4b-web-data-collection.md`） |

对于本课程的项目，免费和开源数据库完全够用。推荐优先使用AKShare和Tushare Pro。

### 关键API详解

**AKShare**（推荐首选）

AKShare是一个开源的金融数据接口库，特点是接口丰富、无需注册、完全免费。覆盖A股、港股、期货、基金、宏观经济等数据。

```python
import akshare as ak

df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20250101",
    end_date="20251231",
    adjust="qfq"
)
print(df.head())
print(df.columns)
```

AKShare常用接口：
- `stock_zh_a_hist`：A股历史行情
- `index_stock_cons_csindex`：指数成分股
- `stock_board_industry_name_em`：行业板块列表
- `stock_financial_report_sina`：财务报表
- `macro_china_gdp`：宏观数据

注意事项：AKShare接口更新频繁，部分接口可能调整。建议使用`ak.__version__`检查版本，及时更新。

**Tushare Pro**

Tushare Pro采用积分制，注册后获取基础积分，可满足大部分数据需求。数据质量较高，接口设计规范。

```python
import tushare as ts

pro = ts.pro_api("your_token")

df = pro.daily(
    ts_code="000001.SZ",
    start_date="20250101",
    end_date="20251231"
)
print(df.head())

df_financial = pro.income(
    ts_code="000001.SZ",
    period="20251231"
)
print(df_financial.head())
```

Tushare Pro常用接口：
- `daily`：日线行情
- `income`/`balancesheet`/`cashflow`：三大财务报表
- `index_daily`：指数日线行情
- `index_weight`：指数成分权重

注意事项：需要注册获取token，有调用频率限制（每分钟200次），部分高级接口需要更多积分。

**yfinance**（主要用于美股和港股）

```python
import yfinance as yf

data = yf.download("AAPL", start="2025-01-01", end="2025-12-31")
print(data.head())
```

注意：yfinance主要用于国际市场，A股数据覆盖有限且可能有延迟，A股项目不建议作为主要数据源。

### 数据格式与存储

获取的金融数据通常有以下格式：

- **DataFrame格式**：API直接返回Pandas DataFrame，最方便后续处理
- **CSV文件**：适合持久化存储和跨项目共享
- **JSON格式**：部分API返回JSON，需要用`pd.json_normalize()`转换
- **数据库存储**：对于大量历史数据，推荐存入SQLite或DuckDB

```python
import pandas as pd
import duckdb

df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20200101", adjust="qfq")
df.to_csv("data/000001_daily.csv", index=False)

df_from_csv = pd.read_csv("data/000001_daily.csv", parse_dates=["日期"])

con = duckdb.connect("data/stocks.duckdb")
con.execute("CREATE TABLE IF NOT EXISTS daily AS SELECT * FROM df")
con.close()
```

## 关键细节与易错点

### 复权方式选择

A股数据有前复权（qfq）和后复权（hfq）两种复权方式，选择不当会导致分析结果错误：
- **前复权**：以最新价格为基准向前调整，保证最新价格是真实价格，适合技术分析
- **后复权**：以最早价格为基准向后调整，保证历史价格连续，适合计算长期收益率
- **不复权**：原始价格，存在跳空，一般不用于分析

常见错误：计算长期收益率时使用前复权数据——前复权价格会因除权除息而回溯调整，导致历史收益率计算失真。计算长期收益应使用后复权数据。

### API限流与反爬

免费数据源都有调用频率限制：
- AKShare：虽然无官方限制，但频繁请求可能被封IP，建议请求间隔0.5-1秒
- Tushare Pro：每分钟200次，超出会返回错误
- 批量获取时务必添加`time.sleep()`，避免触发限流

```python
import time

for code in stock_list:
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20250101", adjust="qfq")
        all_data[code] = df
        time.sleep(1)
    except Exception as e:
        print(f"获取{code}失败: {e}")
        time.sleep(3)
```

### 数据对齐问题

不同数据源的时间戳格式可能不一致：
- AKShare返回"日期"列，格式为字符串"2025-01-01"
- Tushare Pro返回"trade_date"列，格式为字符串"20250101"
- 合并多个数据源时，必须统一时间格式后再合并

```python
df_akshare["日期"] = pd.to_datetime(df_akshare["日期"])
df_tushare["trade_date"] = pd.to_datetime(df_tushare["trade_date"], format="%Y%m%d")
merged = pd.merge(df_akshare, df_tushare, left_on="日期", right_on="trade_date")
```

### 行业分类标准不统一

A股有多种行业分类体系，它们之间不可直接对应：
- 申万行业分类：31个一级行业，投资研究最常用
- 证监会行业分类：监管用途，分类较粗
- 中证行业分类：中证指数公司制定
- 申万分类会定期调整（如2021版vs2014版），注意数据使用的版本

### 缺失值和数据异常

金融数据中常见的缺失和异常：
- 新股上市初期数据不全
- 停牌期间无交易数据（需要填充或标记）
- 财务数据有季节性（季报披露时间差）
- ST股票价格涨跌幅限制为5%而非10%
- 退市股票数据需要特殊处理

## 金融数据分析示例

**场景**：你需要为"A股行业轮动分析仪表板"项目获取完整的数据集，包括行业分类、成分股、历史行情和基本面数据。

```python
import akshare as ak
import pandas as pd
import time

industries = ak.stock_board_industry_name_em()
print(f"共{len(industries)}个行业板块")
print(industries.head())

industry_name = "银行"
bank_stocks = ak.stock_board_industry_cons_em(symbol=industry_name)
print(f"银行板块共{len(bank_stocks)}只股票")
print(bank_stocks[["代码", "名称"]].head())

all_daily = {}
for idx, row in bank_stocks.iterrows():
    code = row["代码"]
    name = row["名称"]
    try:
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date="20240101",
            adjust="qfq"
        )
        all_daily[code] = df
        print(f"已获取 {name}({code})，共{len(df)}条")
        time.sleep(1)
    except Exception as e:
        print(f"获取 {name}({code}) 失败: {e}")
        time.sleep(3)

combined = pd.concat(all_daily.values(), keys=all_daily.keys(), names=["股票代码"])
combined.to_csv("data/bank_stocks_daily.csv")

summary = pd.DataFrame({
    "股票代码": list(all_daily.keys()),
    "数据条数": [len(df) for df in all_daily.values()],
    "起始日期": [df["日期"].min() for df in all_daily.values()],
    "结束日期": [df["日期"].max() for df in all_daily.values()]
})
print(summary)
print(f"\n数据获取完成：成功{len(all_daily)}/{len(bank_stocks)}只")
```

## 拢展学习

- **AKShare官方文档**：https://akshare.akfamily.xyz/ 完整的接口文档和更新日志，是使用AKShare的必备参考
- **Tushare Pro官方文档**：https://tushare.pro/document/2 详细接口说明、积分规则和示例代码
- **《Python金融大数据分析》**：Hilpisch著，系统介绍金融数据获取、处理和分析的完整流程
- **QuantLib文档**：https://www.quantlib.org/ 金融计算库，适合进阶的金融数据分析和建模
- **金融数据获取对比表**：网上有多篇对比AKShare、Tushare、BaoStar等数据源的评测文章，可以帮助你根据项目需求选择

## 参考链接

- https://akshare.akfamily.xyz/ - AKShare官方文档
- https://tushare.pro/document/2 - Tushare Pro官方文档
- https://github.com/ranaroussi/yfinance - yfinance GitHub仓库
- https://www.baostock.com/ - BaoStock免费证券数据
- https://pypi.org/project/akshare/ - AKShare PyPI页面，可查看最新版本
