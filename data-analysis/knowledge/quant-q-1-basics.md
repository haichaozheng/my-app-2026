# 量化投资基础概念

> **引入时机**：W2 | **核心挑战**：量化投资到底是什么？Alpha/Beta/夏普比率这些术语什么意思？ | **层级**：Essential for quant track

## 为什么要在项目阶段学习这个知识点？

选择了量化赛道，就必须理解量化投资的语言。Alpha、Beta、夏普比率、信息比率——这些术语不仅是行话，更是你评估策略、比较产品、沟通想法的基础工具。不理解这些概念，你连量化研究的论文都读不懂，更不用说构建自己的策略。

量化投资不是"用代码炒股"这么简单。它是一套系统性的投资方法论：从市场观察到假设形成，从策略设计到回测验证，从风险控制到产品化。理解这套方法论的全貌，你才能在项目中找到自己的位置——是做因子挖掘、策略开发、还是风险控制？

对于财经院校学生，你们有一个独特的优势：对金融市场的直觉。量化投资不是纯数学游戏，最成功的量化策略往往来自于对市场微观结构的深刻理解。将你们的金融直觉与数据分析能力结合，就是你们的竞争优势。

## 这个知识点的核心内容

### 量化投资概述

**什么是量化投资**：
- 用数学模型和统计方法指导投资决策
- 核心特征：系统性、纪律性、可验证性
- 与主观投资的区别：决策由模型驱动而非人为判断

**量化投资的流派**：
| 流派 | 核心思路 | 典型策略 | 代表 |
|------|---------|---------|------|
| 因子投资 | 寻找预测收益的因子 | 价值、动量、质量 | AQR |
| 统计套利 | 利用统计规律获利 | 配对交易、均值回归 | Renaissance |
| 高频交易 | 速度优势获利 | 做市、延迟套利 | Citadel |
| 机器学习 | 用ML发现非线性模式 | 深度学习选股 | Two Sigma |
| 另类数据 | 用非传统数据获取信息优势 | 卫星图像、社交情绪 | Numerai |

**A股量化的特殊性**：
- T+1制度：不能当日买卖，影响高频策略
- 涨跌停限制：极端行情下流动性约束
- 散户占比高：市场效率较低，alpha机会更多
- 集中持仓限制：公募双10%限制
- 做空受限：融券成本高、券源少

### 核心术语详解

**Alpha与Beta**：
- Beta（β）：跟随市场的收益，即系统性风险暴露
  - β = 1：与市场同步
  - β > 1：比市场波动更大
  - β < 1：比市场波动更小
- Alpha（α）：超越市场的超额收益，即策略的真正价值
  - α = 策略收益 - β × 市场收益
  - 正α才是策略的"超额能力"

```python
import numpy as np

def calc_alpha_beta(portfolio_returns, benchmark_returns, risk_free=0.03/252):
    excess_portfolio = portfolio_returns - risk_free
    excess_benchmark = benchmark_returns - risk_free
    
    beta = np.cov(excess_portfolio, excess_benchmark)[0, 1] / np.var(excess_benchmark)
    alpha = np.mean(excess_portfolio) - beta * np.mean(excess_benchmark)
    annualized_alpha = (1 + alpha) ** 252 - 1
    
    return annualized_alpha, beta
```

**夏普比率（Sharpe Ratio）**：
- 定义：每承担一单位风险获得的超额收益
- 公式：SR = (Rp - Rf) / σp
- 解读：SR > 1 优秀，SR > 2 卓越，SR < 0 亏损
- 年化：SR_annual = SR_daily × √252

```python
def calc_sharpe(returns, risk_free=0.03/252):
    excess_returns = returns - risk_free
    sharpe_daily = np.mean(excess_returns) / np.std(excess_returns)
    sharpe_annual = sharpe_daily * np.sqrt(252)
    return sharpe_annual
```

**信息比率（Information Ratio）**：
- 定义：每承担一单位主动风险获得的超额收益
- 公式：IR = (Rp - Rb) / σ(Rp - Rb)
- 与夏普比率的区别：基准不同（无风险利率 vs 市场基准）
- 量化策略更关注IR，因为衡量的是"超越基准的能力"

**最大回撤（Maximum Drawdown）**：
- 定义：从净值最高点到最低点的最大跌幅
- 计算：遍历每个时间点，计算到该点的最大回撤，取全局最大值
- 直觉：如果投资者在最差时机入场，最多亏多少

```python
def calc_max_drawdown(nav_series):
    cummax = nav_series.cummax()
    drawdown = (nav_series - cummax) / cummax
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()
    return max_dd, max_dd_date
```

**换手率**：
- 定义：一段时间内买入/卖出金额占组合总价值的比例
- 量化策略的换手率通常较高，但换手率过高意味着交易成本侵蚀利润
- A股双面印花税0.1%+佣金≈0.025%，总交易成本约0.15%

### 策略开发生命周期

```
1. 观察与假设
   ↓ "我观察到X现象，假设Y因子有预测力"
2. 数据准备
   ↓ 获取数据、清洗、特征工程
3. 因子构建
   ↓ 计算因子值、去极值、标准化
4. 因子检验
   ↓ IC/IR分析、分层回测
5. 策略构建
   ↓ 因子组合、权重分配
6. 回测验证
   ↓ 历史表现、敏感性分析
7. 风险评估
   ↓ 最大回撤、压力测试
8. 实盘模拟
   ↓ 纸面交易、小仓位验证
9. 产品化
   ↓ 信号展示、监控系统
```

### 市场微观结构基础

**订单簿**：
- 买盘（Bid）：限价买入订单，价格从高到低排列
- 卖盘（Ask）：限价卖出订单，价格从低到高排列
- 买卖价差（Bid-Ask Spread）：卖一价-买一价，反映流动性
- 深度（Depth）：各价位的订单量

**成交机制**：
- 限价单：指定价格，可能不成交
- 市价单：按当前最优价成交，可能有滑点
- A股集中竞价：最大成交量原则撮合

**对数据分析的影响**：
- 日线数据掩盖了日内微观结构信息
- 收盘价可能受集合竞价影响，不代表全天均衡价
- 小盘股流动性差，实际交易中滑点显著

## 关键细节与易错点

1. **Alpha不等于高收益**：Alpha是扣除了Beta暴露后的超额收益。一个策略年化收益30%，但如果β=2且市场涨了20%，那α只有30%-2×20%=-10%，策略实际上跑输了市场。

2. **夏普比率的陷阱**：高夏普可能来自尾部风险未体现（如卖期权策略）。看夏普的同时必须看最大回撤和收益分布。

3. **忽视交易成本**：A股交易成本约0.15%（双边），换手率10倍/年意味着1.5%的成本。很多看起来不错的策略扣掉成本后就不赚钱了。

4. **混淆日频和年频指标**：日夏普×√252 = 年夏普，日收益×252 ≠ 年收益（应该用复利）。换算公式要正确。

5. **对回测结果过度自信**：回测好看≠实盘赚钱。过拟合、幸存者偏差、前视偏差是回测的三大陷阱，后面的知识点会深入讲解。

## 金融数据分析示例

**场景：理解Alpha的含义——分析一个策略的超额收益**

假设你开发了一个动量策略，过去3年的回测结果如下：

```python
import pandas as pd
import numpy as np

# 模拟策略净值数据
dates = pd.date_range('2021-01-01', '2023-12-31', freq='B')
n_days = len(dates)

# 策略日收益率（年化约20%）
np.random.seed(42)
strategy_returns = np.random.normal(0.0008, 0.015, n_days)

# 沪深300基准日收益率（年化约5%）
benchmark_returns = np.random.normal(0.0002, 0.012, n_days)

returns_df = pd.DataFrame({
    'strategy': strategy_returns,
    'benchmark': benchmark_returns
}, index=dates)

# 计算关键指标
# 1. 年化收益
ann_strategy = (1 + returns_df['strategy']).prod() ** (252/n_days) - 1
ann_benchmark = (1 + returns_df['benchmark']).prod() ** (252/n_days) - 1

# 2. Beta
cov_matrix = returns_df.cov()
beta = cov_matrix.loc['strategy', 'benchmark'] / returns_df['benchmark'].var()

# 3. Alpha（年化）
alpha = ann_strategy - beta * ann_benchmark

# 4. 夏普比率
sharpe_strategy = returns_df['strategy'].mean() / returns_df['strategy'].std() * np.sqrt(252)
sharpe_benchmark = returns_df['benchmark'].mean() / returns_df['benchmark'].std() * np.sqrt(252)

# 5. 信息比率
active_return = returns_df['strategy'] - returns_df['benchmark']
ir = active_return.mean() / active_return.std() * np.sqrt(252)

# 6. 最大回撤
nav = (1 + returns_df['strategy']).cumprod()
max_dd = ((nav - nav.cummax()) / nav.cummax()).min()

print(f"策略年化收益: {ann_strategy:.2%}")
print(f"基准年化收益: {ann_benchmark:.2%}")
print(f"Beta: {beta:.2f}")
print(f"Alpha: {alpha:.2%}")
print(f"策略夏普: {sharpe_strategy:.2f}")
print(f"基准夏普: {sharpe_benchmark:.2f}")
print(f"信息比率: {ir:.2f}")
print(f"最大回撤: {max_dd:.2%}")
```

通过这个分析，你不仅能看到策略赚了多少，还能回答：策略的超额收益来自市场暴露（Beta）还是真正的选股能力（Alpha）？每承担一单位风险获得了多少超额回报（夏普/IR）？最坏情况下会亏多少（最大回撤）？

## 拓展学习

- 《主动投资组合管理》——Grinold & Kahn，量化投资的圣经
- 《量化投资：策略与技术》——丁鹏，A股量化实践
- AQR论文合集——理解因子投资的理论基础
- 量化投资入门视频——B站/YouTube上的系统教程
- 聚宽/米筐量化社区——实践平台和策略分享

## 参考链接

- https://www.aqr.com —— AQR研究论文
- https://www.joinquant.com/ —— 聚宽量化平台
- https://www.ricequant.com/ —— 米筐量化平台
- https://zhuanlan.zhihu.com/p/139485497 —— 量化投资核心指标详解
