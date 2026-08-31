# 回测框架与策略评估

> **引入时机**：W4 | **核心挑战**：如何用回测验证策略？如何避免回测陷阱？ | **层级**：Essential for quant track

## 为什么要在项目阶段学习这个知识点？

回测是量化策略从"想法"到"验证"的必经之路。但回测也是最容易被误用的工具——一个精心调参的回测可以让你相信任何策略都赚钱，而实盘却亏得一塌糊涂。理解回测的原理和陷阱，是量化研究者最基本的职业素养。

回测陷阱不是理论问题，而是实践中的高频错误。幸存者偏差让你只看到活下来的股票，前视偏差让你用了未来才能知道的信息，过拟合让你的策略完美适配历史但无法应对未来。这些陷阱每一个都能让你的回测结果从"优秀"变成"幻觉"。

对于财经院校学生，回测框架的设计还涉及大量金融领域知识——T+1怎么处理、停牌怎么处理、涨跌停能否成交、交易成本怎么算。如果你不理解这些规则，回测框架本身就不可靠。本知识点将回测的技术实现与金融规则紧密结合。

## 这个知识点的核心内容

### 回测框架设计

**回测的核心组件**：
```
┌──────────────────────────────────────────────┐
│                回测引擎                        │
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐ │
│  │ 数据层   │  │ 策略层   │  │ 执行层        │ │
│  │ 行情数据 │→│ 信号生成 │→│ 订单管理      │ │
│  │ 财务数据 │  │ 因子计算 │  │ 成交模拟      │ │
│  │ 行业分类 │  │ 择时逻辑 │  │ 成本计算      │ │
│  └─────────┘  └─────────┘  └──────────────┘ │
│       │            │              │          │
│       └────────────┼──────────────┘          │
│                    ↓                         │
│              ┌──────────┐                    │
│              │ 评估层    │                    │
│              │ 绩效指标  │                    │
│              │ 风险指标  │                    │
│              │ 可视化    │                    │
│              └──────────┘                    │
└──────────────────────────────────────────────┘
```

**逐日回测流程**：
```python
class BacktestEngine:
    def __init__(self, initial_capital=1e6):
        self.capital = initial_capital
        self.positions = {}
        self.nav_history = []
        self.trade_log = []

    def run(self, data_handler, strategy, executor):
        for date in data_handler.dates:
            # 1. 更新持仓市值
            self._update_positions(date, data_handler)
            
            # 2. 获取当前数据
            market_data = data_handler.get_data(date)
            
            # 3. 策略生成信号
            signals = strategy.generate_signals(market_data, self.positions)
            
            # 4. 执行交易
            trades = executor.execute(signals, market_data, self.capital)
            
            # 5. 更新持仓和资金
            self._process_trades(trades, market_data)
            
            # 6. 记录净值
            self.nav_history.append({
                'date': date,
                'nav': self._calc_nav(market_data)
            })
        
        return pd.DataFrame(self.nav_history)
```

### 常见回测陷阱

**陷阱一：幸存者偏差（Survivorship Bias）**
- 问题：只用当前存续的股票回测，忽略了已退市的
- 影响：小市值因子的超额收益被高估，因为退市的都是小盘股
- 解决：使用包含退市股的历史成分数据，或至少在分析中标注此局限

**陷阱二：前视偏差（Look-Ahead Bias）**
- 问题：使用了未来才能获得的信息
- 常见形式：
  - 用年报数据回测当年的策略（年报次年4月才披露）
  - 使用复权后的价格（复权因子包含未来分红信息）
  - 使用当天收盘价作为买入价（实际只能次日买入）
- 解决：严格使用"可得数据"——用发布日期而非报告期，用次日开盘价成交

```python
# 错误：用当天收盘价计算信号并买入
if close_today > MA20_today:
    buy_at = close_today  # 前视偏差！

# 正确：用当天数据计算信号，次日开盘价买入
if close_today > MA20_today:
    buy_at = open_tomorrow  # T+1约束
```

**陷阱三：过拟合（Overfitting）**
- 问题：参数过度调优，策略完美适配历史但无法泛化
- 识别方法：
  - 参数微调导致结果剧变（参数敏感性过高）
  - 样本内表现远好于样本外
  - 策略逻辑无法用经济学原理解释
- 解决方法：
  - 样本内/外分割（如2018-2021训练，2022-2023验证）
  - Walk-forward分析
  - 要求策略逻辑有经济学解释
  - 参数稳健性检验：参数变化±20%后策略仍有效

**陷阱四：忽略交易成本**
- A股交易成本明细：
  - 佣金：万2.5（双边）= 0.05%
  - 印花税：卖出0.05%
  - 滑点：约0.1%-0.3%（视流动性）
  - 合计双边约0.2%-0.4%

```python
def apply_transaction_cost(trade_value, is_buy, commission=0.00025, stamp_tax=0.0005):
    cost = trade_value * commission
    if not is_buy:
        cost += trade_value * stamp_tax
    return cost
```

**陷阱五：忽略涨跌停和停牌**
- 涨停日无法买入，跌停日无法卖出
- 停牌日无法交易，收益率为0
- 忽略这些约束会高估策略收益

```python
def can_trade(stock, date, direction, data):
    if data.loc[date, stock, 'volume'] == 0:  # 停牌
        return False
    chg = data.loc[date, stock, 'pct_change']
    if direction == 'buy' and chg >= 9.9:  # 涨停无法买入
        return False
    if direction == 'sell' and chg <= -9.9:  # 跌停无法卖出
        return False
    return True
```

### 绩效评估指标

**收益类指标**：
| 指标 | 计算方式 | 说明 |
|------|---------|------|
| 累计收益 | (期末净值/期初净值) - 1 | 总收益 |
| 年化收益 | (1+累计收益)^(252/天数) - 1 | 折算年化 |
| 超额收益 | 策略收益 - 基准收益 | 跑赢市场多少 |

**风险类指标**：
| 指标 | 计算方式 | 说明 |
|------|---------|------|
| 年化波动率 | 日收益标准差×√252 | 收益的波动程度 |
| 最大回撤 | max((峰谷差)/峰值) | 最坏情况亏多少 |
| 下行偏差 | 负收益的标准差 | 只考虑亏损波动 |

**风险调整指标**：
| 指标 | 计算方式 | 说明 |
|------|---------|------|
| 夏普比率 | (超额收益)/波动率 | 每单位风险收益 |
| 索提诺比率 | (超额收益)/下行偏差 | 只考虑下行风险 |
| 卡尔马比率 | 年化收益/最大回撤 | 收益vs最坏情况 |

**策略特有指标**：
| 指标 | 计算方式 | 说明 |
|------|---------|------|
| 胜率 | 盈利交易数/总交易数 | 多少次交易赚钱 |
| 盈亏比 | 平均盈利/平均亏损 | 赚的比亏的多多少 |
| 换手率 | 买入额+卖出额/(2×总资产) | 交易频率 |

### 回测工具

**自建回测框架 vs 现成平台**：

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| 自建（Python） | 完全可控，理解每个细节 | 开发成本高，容易有Bug | 学习、研究 |
| Backtrader | 成熟框架，社区活跃 | 文档偏旧，A股支持弱 | 通用策略回测 |
| 聚宽/米筐 | A股数据齐全，回测引擎成熟 | 灵活性受限，依赖平台 | A股策略快速验证 |
| VectorBT | 向量化回测，速度极快 | 不适合复杂交易逻辑 | 快速原型验证 |

**推荐路径**：先用自建简单框架理解原理（W5-W6），再用聚宽等平台快速验证（W7+）。

## 关键细节与易错点

1. **回测周期太短**：至少3年，最好5年+。1年的回测可能是特定市场环境的结果，不具代表性。A股一个牛熊周期约3-5年。

2. **忽视换仓日的选择**：月度换仓在月初还是月末？月末可能有机构调仓效应，月初有资金流入效应。换仓日选择会影响结果，需做敏感性分析。

3. **组合权重分配**：等权 vs 市值加权 vs 因子得分加权。不同权重方式导致不同结果。等权最简单但可能放大小盘股影响。

4. **回测结果的统计显著性**：即使回测年化收益20%，如果夏普比率只有0.5，可能只是噪声。用t检验判断策略超额收益是否统计显著。

5. **只用一个评估指标**：不能只看年化收益。一个好策略应该是：年化>15% + 夏普>1.0 + 最大回撤<15% + 换手率<10倍。

## 金融数据分析示例

**回测一个简单动量策略，正确处理A股特殊规则**：

```python
import pandas as pd
import numpy as np

class AShareBacktest:
    def __init__(self, initial_capital=1e6, commission=0.00025, stamp_tax=0.0005):
        self.capital = initial_capital
        self.commission = commission
        self.stamp_tax = stamp_tax

    def run(self, price_df, volume_df, rebalance_freq='M'):
        dates = price_df.index
        strategy_nav = pd.Series(index=dates, dtype=float)
        strategy_nav.iloc[0] = self.capital
        
        holdings = {}
        rebalance_dates = self._get_rebalance_dates(dates, rebalance_freq)
        
        for i in range(1, len(dates)):
            date = dates[i]
            prev_date = dates[i-1]
            
            # 计算当前持仓市值
            portfolio_value = self._calc_portfolio_value(holdings, price_df, date)
            
            # 换仓日
            if date in rebalance_dates:
                # 1. 计算动量因子（过去20日收益）
                lookback = 20
                momentum = price_df.loc[prev_date] / price_df.shift(lookback).loc[prev_date] - 1
                
                # 2. 排除停牌和涨跌停
                tradable = volume_df.loc[prev_date] > 0
                
                # 3. 选择动量前10名
                candidates = momentum[tradable].nlargest(10)
                
                # 4. 清仓旧持仓（考虑交易成本）
                for stock, shares in holdings.items():
                    sell_price = price_df.loc[date, stock] if stock in price_df.columns else 0
                    if sell_price > 0 and volume_df.loc[date, stock] > 0:
                        sell_value = shares * sell_price
                        cost = sell_value * (self.commission + self.stamp_tax)
                        portfolio_value += sell_value - cost
                
                # 5. 等权买入新持仓（次日开盘价=T+1）
                holdings = {}
                weight = portfolio_value * 0.99 / len(candidates)  # 留1%现金
                for stock in candidates.index:
                    if date < len(dates) - 1:
                        next_date = dates[min(i+1, len(dates)-1)]
                        buy_price = price_df.loc[next_date, stock]
                        shares = weight / buy_price
                        cost = weight * self.commission
                        portfolio_value -= (weight + cost)
                        holdings[stock] = shares
            
            strategy_nav.loc[date] = portfolio_value
        
        return strategy_nav

    def evaluate(self, nav_series, benchmark_nav=None):
        returns = nav_series.pct_change().dropna()
        
        ann_return = (1 + returns).prod() ** (252 / len(returns)) - 1
        ann_vol = returns.std() * np.sqrt(252)
        sharpe = (ann_return - 0.03) / ann_vol
        
        cummax = nav_series.cummax()
        drawdown = (nav_series - cummax) / cummax
        max_dd = drawdown.min()
        calmar = ann_return / abs(max_dd)
        
        print(f"年化收益: {ann_return:.2%}")
        print(f"年化波动率: {ann_vol:.2%}")
        print(f"夏普比率: {sharpe:.2f}")
        print(f"最大回撤: {max_dd:.2%}")
        print(f"卡尔马比率: {calmar:.2f}")
```

## 拓展学习

- 《量化回测的艺术》——回测设计的系统性方法论
- DePrado《金融机器学习》——过拟合的数学分析与解决方案
- Walk-Forward Optimization——比简单样本分割更稳健的验证方法
- 聚宽回测教程——A股回测的实践指南
- Backtrader文档——Python回测框架的使用

## 参考链接

- https://www.backtrader.com/ —— Backtrader回测框架
- https://www.joinquant.com/help/ —— 聚宽回测平台文档
- https://vectorbt.dev/ —— VectorBT向量化回测
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3039142 —— DePrado回测过拟合论文
