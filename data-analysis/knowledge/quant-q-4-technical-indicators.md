# 技术指标与策略逻辑

> **引入时机**：W6 | **核心挑战**：常见技术指标的计算逻辑是什么？如何组合指标形成策略？ | **层级**：Essential for quant track

## 为什么要在项目阶段学习这个知识点？

技术指标是量化策略最基础的构建模块。无论是简单的均线交叉还是复杂的MACD背离，理解指标的计算逻辑是设计策略的前提。很多人把技术指标当作"黑箱"——调用库函数得到一个数，然后直接用。但如果你不理解MA和EMA的区别、不理解RSI为什么用14天、不理解布林带的统计假设，你就无法判断指标在你的场景下是否适用。

更重要的是，单一指标几乎不可能构成有效策略。真正有价值的是指标组合——通过多个指标交叉验证，降低假信号。但组合不是随意叠加，需要理解指标之间的逻辑关系和信息冗余。例如，MA和MACD本质上都是趋势类指标，叠加它们不会增加新信息。

对于财经院校学生，技术指标与你们的金融直觉高度相关。"低买高卖"是投资的基本逻辑，技术指标只是将这种逻辑量化。理解了这一点，你就能从直觉出发设计指标，而不是死记硬背公式。

## 这个知识点的核心内容

### 趋势类指标

**移动平均线（MA）**：
```python
def SMA(series, window):
    return series.rolling(window).mean()

def EMA(series, span):
    return series.ewm(span=span, adjust=False).mean()
```

- SMA：简单算术平均，对历史数据等权
- EMA：指数加权平均，近期数据权重大，反应更灵敏
- 常用参数：MA5/MA10/MA20/MA60/MA120/MA250

**MACD（Moving Average Convergence Divergence）**：
```python
def MACD(close, fast=12, slow=26, signal=9):
    ema_fast = EMA(close, fast)
    ema_slow = EMA(close, slow)
    dif = ema_fast - ema_slow
    dea = EMA(dif, signal)
    hist = 2 * (dif - dea)
    return dif, dea, hist
```

- DIF：快慢EMA之差，衡量趋势强度
- DEA：DIF的EMA，作为信号线
- MACD柱：DIF-DEA的2倍，衡量趋势加速度
- 经典用法：DIF上穿DEA买入（金叉），DIF下穿DEA卖出（死叉）

**布林带（Bollinger Bands）**：
```python
def bollinger_bands(close, window=20, num_std=2):
    mid = SMA(close, window)
    std = close.rolling(window).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    return upper, mid, lower
```

- 基于正态分布假设：约95%的价格落在±2σ内
- 突破上轨：可能超买；突破下轨：可能超卖
- 带宽收窄：波动率降低，可能酝酿大行情

### 动量类指标

**RSI（Relative Strength Index）**：
```python
def RSI(close, window=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

- 范围0-100：>70超买，<30超卖
- 注意：强趋势中RSI可以长期>70，此时"超买"不是卖出信号
- 底背离：价格创新低但RSI不创新低——可能的反转信号

**KDJ（随机指标）**：
```python
def KDJ(high, low, close, n=9, m1=3, m2=3):
    lowest_low = low.rolling(n).min()
    highest_high = high.rolling(n).max()
    rsv = (close - lowest_low) / (highest_high - lowest_low) * 100
    K = rsv.ewm(com=m1-1, adjust=False).mean()
    D = K.ewm(com=m2-1, adjust=False).mean()
    J = 3 * K - 2 * D
    return K, D, J
```

- K线上穿D线：买入信号；K线下穿D线：卖出信号
- J>100：超买区；J<0：超卖区
- A股短线交易者常用指标

**CCI（Commodity Channel Index）**：
```python
def CCI(high, low, close, window=20):
    tp = (high + low + close) / 3
    ma = tp.rolling(window).mean()
    md = tp.rolling(window).apply(lambda x: np.abs(x - x.mean()).mean())
    cci = (tp - ma) / (0.015 * md)
    return cci
```

### 成交量类指标

**OBV（On Balance Volume）**：
```python
def OBV(close, volume):
    direction = np.sign(close.diff())
    direction.iloc[0] = 0
    return (direction * volume).cumsum()
```

- 量价配合：价涨OBV涨→健康上涨；价涨OBV跌→量价背离
- OBV创新高而价格未创新高：可能的看涨信号

**VWAP（Volume Weighted Average Price）**：
```python
def VWAP(high, low, close, volume):
    tp = (high + low + close) / 3
    cum_tp_vol = (tp * volume).cumsum()
    cum_vol = volume.cumsum()
    return cum_tp_vol / cum_vol
```

### 指标组合策略

**组合原则**：
1. 不同类别的指标组合（趋势+动量+量价），避免信息冗余
2. 多指标共振时信号更可靠（如MA金叉+RSI<70+放量）
3. 每个指标在策略中有明确的角色（趋势判断/入场时机/止损逻辑）

**双均线交叉策略（经典入门策略）**：
```python
def ma_crossover_strategy(close, fast=5, slow=20):
    ma_fast = SMA(close, fast)
    ma_slow = SMA(close, slow)
    
    signals = pd.Series(0, index=close.index)
    signals[ma_fast > ma_slow] = 1    # 做多
    signals[ma_fast < ma_slow] = -1   # 做空（A股改为空仓）
    
    # 过滤信号：只在交叉时交易
    trade_signals = signals.diff()
    return signals, trade_signals
```

**MACD+RSI组合策略**：
```python
def macd_rsi_strategy(close, fast=12, slow=26, signal=9, rsi_window=14):
    dif, dea, hist = MACD(close, fast, slow, signal)
    rsi = RSI(close, rsi_window)
    
    signals = pd.Series(0, index=close.index)
    
    # 买入条件：MACD金叉 + RSI未超买
    buy_cond = (dif > dea) & (dif.shift(1) <= dea.shift(1)) & (rsi < 70)
    
    # 卖出条件：MACD死叉 或 RSI超买
    sell_cond = (dif < dea) & (dif.shift(1) >= dea.shift(1)) | (rsi > 80)
    
    signals[buy_cond] = 1
    signals[sell_cond] = -1
    
    return signals
```

### 指标的局限性

**指标的共性局限**：
- 滞后性：所有基于历史数据的指标都滞后，金叉出现时趋势可能已走了一半
- 参数依赖：不同参数组合给出不同甚至矛盾的信号
- 市场适应性：趋势指标在震荡市中频繁假信号，震荡指标在趋势市中过早离场
- 自证预言：广泛使用的指标可能因大量交易者同时行动而"自我实现"

**如何应对局限性**：
- 多时间框架确认：日线信号+周线趋势一致时再行动
- 动态参数：根据市场状态（趋势/震荡）切换指标参数
- 信号过滤：增加成交量、波动率等辅助条件过滤假信号
- 承认局限：没有万能指标，策略的盈亏比和风控比指标选择更重要

## 关键细节与易错点

1. **混淆SMA和EMA**：SMA对历史数据等权，EMA偏重近期。同一个策略用SMA和EMA的结果可能差异很大。必须明确你用的是哪种，以及为什么。

2. **参数过拟合**：在历史数据上反复调整MA的窗口期，找到"最优"的5和20，但这可能只是过拟合。参数应该有经济含义（MA5=一周、MA20=一月、MA60=一季）。

3. **忽略复权**：计算技术指标必须用复权价格，否则分红除权会制造虚假的信号。但回测交易时要注意：前复权适合看图，后复权适合算收益。

4. **信号与交易的延迟**：信号在T日收盘产生，实际交易在T+1开盘。这个延迟对短线策略影响很大。回测中必须模拟这个延迟。

5. **过度组合指标**：加入5个指标不一定比2个指标好。指标越多，自由度越高，过拟合风险越大。3个不同类别的指标通常是合理的上限。

## 金融数据分析示例

**构建并回测MA交叉策略**：

```python
import akshare as ak
import pandas as pd
import numpy as np

# 获取数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily",
                         start_date="20200101", end_date="20231231",
                         adjust="hfq")
df = df.set_index('日期')
close = df['收盘']
high = df['最高']
low = df['最低']
volume = df['成交量']

# 计算指标
ma5 = SMA(close, 5)
ma20 = SMA(close, 20)
dif, dea, hist = MACD(close)
rsi = RSI(close, 14)

# 生成信号
position = pd.Series(0, index=close.index)

# 买入：MA5上穿MA20 + MACD金叉 + RSI<70
buy_signal = (ma5 > ma20) & (ma5.shift(1) <= ma20.shift(1)) & \
             (dif > dea) & (rsi < 70)

# 卖出：MA5下穿MA20 或 RSI>80
sell_signal = (ma5 < ma20) & (ma5.shift(1) >= ma20.shift(1)) | (rsi > 80)

position[buy_signal] = 1
position[sell_signal] = 0
position = position.ffill().fillna(0)

# 计算策略收益（T+1：次日开盘价成交）
strategy_returns = close.pct_change().shift(-1) * position
strategy_nav = (1 + strategy_returns).cumprod()
benchmark_nav = (1 + close.pct_change()).cumprod()

# 评估
print(f"策略累计收益: {(strategy_nav.iloc[-1] - 1):.2%}")
print(f"基准累计收益: {(benchmark_nav.iloc[-1] - 1):.2%}")
print(f"最大回撤: {((strategy_nav / strategy_nav.cummax() - 1).min()):.2%}")
```

## 拓展学习

- 《技术分析》——Murphy，技术分析的经典教材
- TA-Lib指标库——Python技术指标计算的标准库
- 海龟交易法则——完整策略系统设计案例
- A股技术分析实战——结合A股特点的技术分析方法
- 量化指标研究——天风/华泰金工的技术指标量化研究

## 参考链接

- https://github.com/ta-lib/ta-lib-python —— TA-Lib Python文档
- https://www.investopedia.com/ —— 技术指标详解
- https://github.com/bukosabino/ta —— Python技术分析库
- https://zhuanlan.zhihu.com/p/337226798 —— A股技术指标量化回测
