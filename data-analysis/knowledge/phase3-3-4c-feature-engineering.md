# 特征工程与因子构建

> **引入时机**：W13 | **核心挑战**：ML模型效果不好，可能不是模型问题而是特征问题 | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

在机器学习的实际项目中，有一个被反复验证的经验法则：特征工程对模型效果的影响往往大于模型选择和超参数调优的总和。当你发现模型的预测效果不理想时，第一反应不应该是换一个更复杂的模型，而应该检查你的特征是否足够好。在金融领域，这尤为明显——一个好的因子（特征）可以持续产生alpha，而再复杂的模型在垃圾特征上也只能产出垃圾结果。

金融特征工程有其独特的专业性。你需要理解金融逻辑才能构建有意义的特征——5日均线与20日均线的交叉、布林带宽度、RSI超买超卖、换手率变化率，这些都不是靠自动化工具能生成的。特征工程是金融领域知识和ML技术能力交汇的核心环节，也是让你的产品区别于通用分析工具的关键。

在PBL项目中，特征工程的能力直接决定了你产品的预测功能是否可靠。一个能构建专业金融因子的产品，比一个只喂原始价格数据的黑盒模型，更容易获得用户信任和监管认可。

## 这个知识点的核心内容

### 特征工程概述

特征工程是将原始数据转化为更有效表达的过程，包含以下环节：

- **特征构造**：从原始数据创建新特征，如从价格序列计算技术指标
- **特征变换**：对特征进行数学变换，如对数变换、标准化、分箱
- **特征选择**：从众多特征中筛选最有价值的子集
- **特征降维**：将高维特征空间投影到低维空间，保留主要信息

在金融领域，特征工程的核心是因子构建——基于金融逻辑和统计规律，从市场数据中提取能预测未来收益或风险的变量。

### 金融特征构造

**技术指标类特征**：

- **动量因子**：N日收益率（5日、20日、60日）、价格与均线偏离度
- **波动率因子**：N日历史波动率、ATR（Average True Range）、布林带宽度
- **成交量因子**：换手率、量价背离度、成交量变化率
- **趋势强度**：ADX、MACD信号、均线多头/空头排列

**基本面因子**：

- **估值因子**：P/E、P/B、PS、EV/EBITDA及其行业分位数
- **质量因子**：ROE、ROA、毛利率稳定性、应计利润
- **成长因子**：营收增长率、净利润增长率、预期调整幅度
- **财务健康**：Altman Z-score、利息覆盖率、资产负债率

**另类特征**：

- **情绪因子**：新闻情感得分、社交媒体讨论热度、搜索指数变化
- **资金流向**：北向资金净流入、融资余额变化、大宗交易折价率
- **宏观特征**：利率变化、PMI、M2增速、期限利差

### 特征变换

对构造好的特征进行变换以改善模型表现：

- **标准化（Z-score）**：(x - μ) / σ，使不同量纲的特征可比
- **秩变换（Rank）**：将值替换为排序位置，对异常值和分布形状鲁棒
- **对数变换**：log(x)，压缩右偏分布（如成交量、市值）
- **分箱/离散化**：将连续值分为若干区间，捕捉非线性关系
- **行业中性化**：减去行业均值，去除行业效应，使因子跨行业可比

### 特征选择

从大量候选特征中筛选最有价值的子集：

- **过滤法**：基于统计指标（相关系数、互信息、方差）筛选，速度快但不考虑特征组合
- **包装法**：逐步选择（前向/后向），考虑特征组合但计算量大
- **嵌入法**：利用模型自身的特征重要性（Lasso系数、树模型feature_importance）
- **金融特征选择原则**：优先选择有金融逻辑支撑的特征，而非纯粹统计显著的；避免多重共线性；关注因子衰减（过去有效的因子未来可能失效）

### 降维方法

当特征维度过高时需要降维：

- **PCA（主成分分析）**：线性降维，找到方差最大的方向。金融中常用于提取市场因子、行业因子
- **因子分析**：假设观测变量由少数隐因子驱动，比PCA更有统计模型基础
- **自编码器**：神经网络实现的非线性降维，适合复杂模式

## 关键细节与易错点

### 未来函数（Look-ahead Bias）

特征工程中最致命的错误。使用未来才能获取的信息构造特征，导致模型在回测中表现极好但在实盘中失效。常见例子：用全量数据计算标准化参数（应只用训练集）、使用当期财务数据预测当期收益（财务数据有发布延迟）。

### 特征泄漏（Data Leakage）

与未来函数相关，训练阶段使用了测试阶段才能获得的信息。例如：在全部数据上做PCA后再划分训练/测试集，测试集的信息泄漏到了PCA变换中。正确做法：在训练集上拟合变换，再将变换应用到测试集。

### 忽视特征的时间对齐

金融数据的发布频率不同（日线、月报、季报），特征与标签的时间对齐至关重要。用Q3财报数据预测Q3股价收益就是错误的——Q3财报在Q3结束后才发布。必须确保特征时刻早于标签时刻。

### 过度特征工程

构造太多特征（几百甚至上千个）会导致维度灾难和过拟合。特征数量应该与样本量匹配，通常样本量应为特征数的10倍以上。在金融数据量有限的情况下，少而精的特征优于多而杂的特征。

### 忽视因子衰减

金融因子的有效性会随时间衰减——当太多人使用同一因子时，其超额收益会消失。需要定期监控因子表现，及时淘汰失效因子、挖掘新因子。

### 直接使用价格而非收益率

价格序列是非平稳的，直接用价格作为特征几乎必然导致虚假回归。应该使用收益率、变化率或相对指标作为特征。

## 金融数据分析示例

**场景**：为一组A股股票构建ML预测特征，目标是预测未来5日收益。

**技术指标特征**：

```python
import pandas as pd
import numpy as np

def compute_features(df):
    df = df.copy()

    df["return_5d"] = df["close"].pct_change(5)
    df["return_20d"] = df["close"].pct_change(20)
    df["volatility_20d"] = df["return_5d"].rolling(20).std()

    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["price_vs_ma5"] = df["close"] / df["ma5"] - 1
    df["price_vs_ma20"] = df["close"] / df["ma20"] - 1

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    df["turnover_rate"] = df["volume"] / df["total_shares"] * 100
    df["volume_change"] = df["volume"].pct_change(5)

    df["bollinger_width"] = (
        df["close"].rolling(20).std() * 2
    ) / df["ma20"]

    return df

df_features = compute_features(df)
```

**基本面特征**：

```python
df["pe_ratio"] = df["market_cap"] / df["net_income"]
df["pb_ratio"] = df["market_cap"] / df["book_value"]
df["roe"] = df["net_income"] / df["book_value"]

pe_group = df.groupby("industry")["pe_ratio"]
df["pe_industry_rank"] = pe_group.rank(pct=True)

df["debt_ratio"] = df["total_debt"] / df["total_assets"]
df["interest_coverage"] = df["ebit"] / df["interest_expense"]
```

**特征选择**：

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import mutual_info_regression

feature_cols = ["return_5d", "return_20d", "volatility_20d",
                "price_vs_ma5", "price_vs_ma20", "rsi_14",
                "turnover_rate", "volume_change", "bollinger_width",
                "pe_industry_rank", "roe", "debt_ratio"]

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(df[feature_cols], df["target_return_5d"])

importance = pd.Series(rf.feature_importances_, index=feature_cols)
print(importance.sort_values(ascending=False))

selected = importance[importance > 0.05].index.tolist()
```

**标准化与行业中性化**：

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df[feature_cols] = scaler.fit_transform(df[feature_cols])

for col in feature_cols:
    industry_mean = df.groupby("industry")[col].transform("mean")
    df[f"{col}_neutral"] = df[col] - industry_mean
```

## 拓展学习

- **WorldQuant Alpha101**：101个量化因子的经典论文，展示了因子构建的系统性方法
- **因子投资方法论**：因子有效性检验（IC/IR分析）、因子组合优化、因子择时
- **自动特征工程**：Featuretools、tsfresh等库，从时间序列中自动提取大量特征
- **NLP特征工程**：从金融新闻和研报中提取文本特征，构建情绪因子
- **另类数据**：卫星图像、信用卡消费数据、App使用数据等非传统数据源的特征构建

## 参考链接

- https://arxiv.org/abs/2009.11389 - WorldQuant Alpha101因子论文
- https://featuretools.alteryx.com/ - Featuretools自动特征工程
- https://tsfresh.readthedocs.io/ - tsfresh时间序列特征提取库
- https://platform.worldquantbrain.com/ - WorldQuant Brain量化因子研究平台
- https://www.factorwar.com/ - 因子战争博客，中文因子投资深度分析
