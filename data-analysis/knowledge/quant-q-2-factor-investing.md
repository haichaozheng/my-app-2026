# 因子投资与因子挖掘

> **引入时机**：W6 | **核心挑战**：什么是因子？如何挖掘有预测力的因子？IC/IR如何评估？ | **层级**：Essential for quant track

## 为什么要在项目阶段学习这个知识点？

因子投资是量化投资最核心的范式之一。理解因子，你就理解了"什么样的股票特征能预测未来收益"这个问题。不管你最终做的是动量策略、价值投资还是机器学习选股，本质上都在寻找"因子"——只是传统因子投资用线性方法，ML用非线性方法。

因子挖掘不是随意的特征工程。它需要从金融逻辑出发，提出假设，用数据验证，再用IC/IR等指标系统评估。很多初学者犯了"数据挖掘"的错误——试了100个因子，挑出2个好看的，但它们只是噪声的产物。本知识点教你如何避免这种错误，建立严谨的因子研究流程。

对于财经院校学生，因子投资与你们已有的金融知识天然衔接。你已经知道"低PE的股票可能被低估"——这就是价值因子。因子投资只是把这种直觉系统化、量化了。将金融直觉与量化方法结合，是你们最大的竞争优势。

## 这个知识点的核心内容

### 因子投资理论基础

**什么是因子**：
- 因子是能够解释资产收益差异的共同特征
- 类比：股票收益像一道菜，因子是食材——每只股票的收益由多个因子的暴露组合决定
- 因子模型：Ri = αi + βi1×F1 + βi2×F2 + ... + εi

**因子分类**：

| 类别 | 因子示例 | 逻辑 |
|------|---------|------|
| 价值因子 | EP/BP/DP | 便宜的股票未来收益更高 |
| 动量因子 | 过去N月涨幅 | 趋势延续性 |
| 质量因子 | ROE/盈利稳定性 | 好公司有溢价 |
| 规模因子 | 市值 | 小盘股有超额收益 |
| 波动因子 | 历史波动率 | 低波动异象 |
| 流动性因子 | 换手率/Amihud | 低流动性有溢价 |
| 成长因子 | 营收增长率 | 高增长有溢价 |

**A股因子研究的特殊考虑**：
- 壳价值效应：小市值因子在A股部分由壳价值驱动（借壳上市预期）
- 散户情绪：情绪类因子在A股效果显著
- 政策因子：行业政策、监管变化影响因子表现
- 因子周期性：A股因子表现有明显的牛熊周期特征

### 因子挖掘流程

```
1. 提出假设
   "我假设过去5日成交量异常放大的股票，未来20日有超额收益"
   ↓
2. 定义因子
   vol_ratio = MA(vol, 5) / MA(vol, 20)
   ↓
3. 数据准备
   获取全A股日线数据，计算因子值
   ↓
4. 预处理
   去极值（MAD法）→ 标准化（Z-score）→ 中性化（行业+市值）
   ↓
5. IC分析
   计算因子值与未来收益的相关性
   ↓
6. 分层回测
   按因子值分5组，比较多空收益
   ↓
7. 稳定性检验
   滚动窗口IC、IC衰减分析
   ↓
8. 因子组合
   与已有因子正交性检验，决定是否纳入多因子模型
```

### 因子预处理

**去极值（MAD法）**：
```python
def mad_winsorize(factor_values, n=3):
    median = factor_values.median()
    mad = (factor_values - median).abs().median() * 1.4826
    upper = median + n * mad
    lower = median - n * mad
    return factor_values.clip(lower, upper)
```

**标准化（Z-score）**：
```python
def zscore(factor_values):
    return (factor_values - factor_values.mean()) / factor_values.std()
```

**行业中性化**：
```python
def industry_neutralize(factor_df, industry_series):
    factor_neutral = pd.Series(index=factor_df.index, dtype=float)
    for industry in industry_series.unique():
        mask = industry_series == industry
        factor_neutral[mask] = zscore(factor_df[mask])
    return factor_neutral
```

### IC/IR评估体系

**IC（Information Coefficient）**：
- 定义：因子值与未来收益的秩相关系数（Spearman）
- IC > 0.03：弱预测力
- IC > 0.05：中等预测力
- IC > 0.1：强预测力

```python
from scipy import stats

def calc_ic(factor_values, forward_returns):
    ic, _ = stats.spearmanr(factor_values, forward_returns)
    return ic

def calc_ic_series(factor_df, return_df, period=20):
    ic_list = []
    dates = factor_df.index
    for date in dates:
        f = factor_df.loc[date].dropna()
        r = return_df.loc[date].dropna()
        common = f.index.intersection(r.index)
        if len(common) > 30:
            ic = calc_ic(f[common], r[common])
            ic_list.append({'date': date, 'ic': ic})
    return pd.DataFrame(ic_list)
```

**IR（Information Ratio）**：
- 定义：IC均值 / IC标准差
- IR > 0.5：因子较稳定
- IR > 1.0：因子非常稳定
- IR衡量的是因子预测力的"稳定性"，比单期IC更重要

```python
def calc_ir(ic_series):
    return ic_series.mean() / ic_series.std()
```

**IC衰减分析**：
```python
def ic_decay(factor_df, return_df, max_period=60):
    decay_data = []
    for period in range(1, max_period + 1):
        forward_returns = return_df.shift(-period)
        ic = calc_ic_series(factor_df, forward_returns)
        decay_data.append({
            'period': period,
            'mean_ic': ic['ic'].mean(),
            'ir': calc_ir(ic['ic'])
        })
    return pd.DataFrame(decay_data)
```

### 分层回测

分层回测是因子评估的补充方法，直观展示因子的单调性：

```python
def quantile_backtest(factor_df, return_df, n_quantiles=5):
    results = []
    for date in factor_df.index:
        f = factor_df.loc[date].dropna()
        r = return_df.loc[date].dropna()
        common = f.index.intersection(r.index)
        if len(common) < n_quantiles * 10:
            continue
        quantiles = pd.qcut(f[common], n_quantiles, labels=False)
        for q in range(n_quantiles):
            stocks_in_q = common[quantiles == q]
            results.append({
                'date': date,
                'quantile': q + 1,
                'return': r[stocks_in_q].mean()
            })
    df = pd.DataFrame(results)
    return df.groupby('quantile')['return'].mean()
```

单调性好的因子：每层收益递增/递减，第1层和第5层差异显著。

## 关键细节与易错点

1. **数据挖掘偏误**：试了100个因子，总有几个IC看起来不错。这是多重检验问题。解决方法：Bonferroni校正（显著阈值=0.05/因子数）、要求IC在经济逻辑上可解释。

2. **前视偏差**：用当天财报数据计算因子，但财报可能在当天还没公布。必须使用"发布日期"而非"报告期"。

3. **幸存者偏差**：只用了当前存续的股票，忽略了已退市的。小市值因子的超额收益可能部分来自退市股的缺失。

4. **因子衰减**：一个因子在2015-2019年IC=0.08，不代表2024年还有效。市场会学习，因子会衰减。必须做滚动窗口检验。

5. **IC计算用Spearman而非Pearson**：金融数据有大量极端值，Pearson相关系数受极值影响大。Spearman秩相关更稳健。

## 金融数据分析示例

**挖掘A股动量因子**：

```python
import akshare as ak
import pandas as pd
import numpy as np
from scipy import stats

# Step 1: 获取数据
def get_stock_data(codes, start_date, end_date):
    data = {}
    for code in codes:
        try:
            df = ak.stock_zh_a_hist(
                symbol=code, period="daily",
                start_date=start_date, end_date=end_date,
                adjust="hfq"
            )
            data[code] = df.set_index('日期')['收盘']
        except:
            continue
    return pd.DataFrame(data)

# Step 2: 计算动量因子（过去20日收益率）
def calc_momentum_factor(price_df, lookback=20):
    return price_df.pct_change(lookback)

# Step 3: 计算未来收益
def calc_forward_return(price_df, period=20):
    return price_df.pct_change(period).shift(-period)

# Step 4: IC分析
def full_ic_analysis(factor_df, return_df):
    ic_list = []
    for date in factor_df.index[::20]:  # 每月采样
        f = factor_df.loc[date].dropna()
        r = return_df.loc[date].dropna()
        common = f.index.intersection(r.index)
        if len(common) > 50:
            ic, pval = stats.spearmanr(f[common], r[common])
            ic_list.append({'date': date, 'ic': ic, 'pval': pval})
    
    ic_df = pd.DataFrame(ic_list)
    print(f"均值IC: {ic_df['ic'].mean():.4f}")
    print(f"IR: {ic_df['ic'].mean() / ic_df['ic'].std():.4f}")
    print(f"IC胜率: {(ic_df['ic'] > 0).mean():.2%}")
    print(f"IC显著比例: {(ic_df['pval'] < 0.05).mean():.2%}")
    return ic_df
```

分析结果解读：
- 均值IC=0.04：弱预测力，但统计显著
- IR=0.6：因子相对稳定
- IC胜率=58%：58%的月份IC为正
- 结论：动量因子在A股有弱但稳定的预测力，适合与其他因子组合使用

## 拓展学习

- 《Alpha因子挖掘》——WorldQuant 101 Alpha因子
- Barra风险模型——多因子模型的工业标准
- 因子投资论文：Fama-French三因子、五因子模型
- A股因子研究报告——天风/华泰/国盛金工
- 因子动物园（Factor Zoo）——理解因子泛滥与选择问题

## 参考链接

- https://arxiv.org/abs/1601.00991 —— 101 Formulaic Alphas
- https://www.msci.com/ —— Barra风险模型
- https://www.aqr.com —— 因子投资学习资源
- https://zhuanlan.zhihu.com/p/139485497 —— A股因子研究实践
