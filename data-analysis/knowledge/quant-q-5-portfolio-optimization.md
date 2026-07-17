# 组合优化与风险控制

> **引入时机**：W13 | **核心挑战**：如何构建投资组合？VaR、最大回撤、风险分散的逻辑？ | **层级**：Essential for quant track

## 为什么要在项目阶段学习这个知识点？

选出了好股票不等于构建了好组合。单只股票的波动可能很大，但通过组合可以降低整体风险——这就是分散化的力量。组合优化教你如何在收益和风险之间找到最优平衡，而风险控制教你如何在极端情况下保护组合。

很多初学者认为"多买几只股票就是分散化"。但如果你买的5只银行股同涨同跌，分散化效果几乎为零。真正的分散化需要理解资产之间的相关性——只有相关性低的资产组合才能有效分散风险。

对于财经院校学生，组合优化和风险控制是你们进入金融行业后的核心技能。无论是公募基金的组合管理、私募基金的风控、还是银行的投资决策，都离不开这套方法论。课程项目中的组合优化实践，是你们建立直觉和技能的最佳时机。

## 这个知识点的核心内容

### 投资组合理论基础

**马科维茨均值-方差模型**：
- 核心思想：在给定预期收益下最小化风险，或在给定风险下最大化收益
- 有效前沿：所有帕累托最优组合的集合
- 关键输入：预期收益向量、协方差矩阵

```python
import numpy as np
from scipy.optimize import minimize

def mean_variance_optimize(returns, target_return=None, risk_free=0.03):
    n = returns.shape[1]
    mu = returns.mean() * 252
    sigma = returns.cov() * 252

    def portfolio_volatility(weights):
        return np.sqrt(weights @ sigma.values @ weights)

    def portfolio_return(weights):
        return weights @ mu.values

    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    ]

    if target_return is not None:
        constraints.append(
            {'type': 'eq', 'fun': lambda w: portfolio_return(w) - target_return}
        )

    bounds = [(0, 1) for _ in range(n)]
    init_weights = np.ones(n) / n

    result = minimize(
        portfolio_volatility, init_weights, method='SLSQP',
        bounds=bounds, constraints=constraints
    )

    return result.x

def max_sharpe_portfolio(returns, risk_free=0.03):
    n = returns.shape[1]
    mu = returns.mean() * 252
    sigma = returns.cov() * 252

    def neg_sharpe(weights):
        ret = weights @ mu.values
        vol = np.sqrt(weights @ sigma.values @ weights)
        return -(ret - risk_free) / vol

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n)]
    init_weights = np.ones(n) / n

    result = minimize(neg_sharpe, init_weights, method='SLSQP',
                      bounds=bounds, constraints=constraints)
    return result.x
```

### 风险度量指标

**VaR（Value at Risk）**：
- 定义：在给定置信度下，组合在未来N天内的最大可能损失
- 三种计算方法：

```python
def var_historical(returns, confidence=0.95):
    return -np.percentile(returns, (1 - confidence) * 100)

def var_parametric(returns, confidence=0.95):
    mu = returns.mean()
    sigma = returns.std()
    from scipy.stats import norm
    z = norm.ppf(1 - confidence)
    return -(mu + z * sigma)

def var_monte_carlo(returns, confidence=0.95, n_simulations=10000):
    mu = returns.mean()
    sigma = returns.std()
    simulated = np.random.normal(mu, sigma, n_simulations)
    return -np.percentile(simulated, (1 - confidence) * 100)
```

- 历史模拟法：直接用历史收益分布，无需分布假设
- 参数法：假设正态分布，计算简单但可能低估尾部风险
- 蒙特卡洛：灵活但计算量大

**CVaR（Conditional VaR / Expected Shortfall）**：
- 定义：当损失超过VaR时的平均损失
- 比VaR更保守，能捕捉尾部风险

```python
def cvar_historical(returns, confidence=0.95):
    var = var_historical(returns, confidence)
    return -returns[returns < -var].mean()
```

**最大回撤与回撤持续时间**：
```python
def drawdown_analysis(nav_series):
    cummax = nav_series.cummax()
    drawdown = (nav_series - cummax) / cummax

    max_dd = drawdown.min()
    max_dd_end = drawdown.idxmin()
    max_dd_start = nav_series[:max_dd_end].idxmax()

    recovery_mask = nav_series[max_dd_end:] >= cummax[max_dd_end]
    if recovery_mask.any():
        recovery_date = recovery_mask.idxmax()
        recovery_days = (recovery_date - max_dd_end).days
    else:
        recovery_days = None

    return {
        'max_drawdown': max_dd,
        'start_date': max_dd_start,
        'end_date': max_dd_end,
        'recovery_days': recovery_days
    }
```

### 分散化与相关性

**分散化的数学原理**：
```python
def diversification_benefit(returns, weights):
    port_vol = np.sqrt(weights @ returns.cov().values @ weights * 252)
    weighted_vol = np.sum(weights * returns.std().values * np.sqrt(252))
    benefit = (weighted_vol - port_vol) / weighted_vol
    return benefit
```

- 组合波动率 <= 成分股加权波动率
- 差额就是分散化带来的"免费午餐"
- 相关性越低，分散化收益越大

**相关性分析**：
```python
def correlation_analysis(returns):
    corr = returns.corr()
    corr_values = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    corr_stack = corr_values.stack()

    most_correlated = corr_stack.idxmax()
    least_correlated = corr_stack.idxmin()

    print("最高相关性: {} = {:.2f}".format(most_correlated, corr_stack.max()))
    print("最低相关性: {} = {:.2f}".format(least_correlated, corr_stack.min()))
    print("平均相关性: {:.2f}".format(corr_stack.mean()))

    return corr
```

**A股行业分散化的实践建议**：
- 跨行业配置：金融、消费、科技、医药、周期
- 跨市值配置：大盘蓝筹+中盘成长
- 跨风格配置：价值+动量
- 避免过度分散：超过20只股票分散化收益递减

### 风险预算与风险平价

**等风险贡献（Risk Parity）**：
```python
def risk_parity_weights(returns):
    n = returns.shape[1]
    sigma = returns.cov() * 252

    def risk_contribution(weights):
        port_vol = np.sqrt(weights @ sigma.values @ weights)
        marginal = sigma.values @ weights / port_vol
        rc = weights * marginal
        return rc

    def objective(weights):
        rc = risk_contribution(weights)
        target_rc = np.ones(n) / n
        return np.sum((rc / rc.sum() - target_rc) ** 2)

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1) for _ in range(n)]
    init_weights = np.ones(n) / n

    result = minimize(objective, init_weights, method='SLSQP',
                      bounds=bounds, constraints=constraints)
    return result.x
```

- 等权配置：每只股票权重相同，但波动大的股票风险贡献更大
- 风险平价：每只股票的风险贡献相同，低波动股票权重大
- 在A股实践中，风险平价通常配更多债券类资产

### 压力测试

```python
def stress_test(portfolio_returns, scenarios):
    results = {}
    for name, shock in scenarios.items():
        shocked_returns = portfolio_returns + shock
        var = var_historical(shocked_returns)
        nav = (1 + shocked_returns).cumprod()
        max_dd = ((nav / nav.cummax() - 1).min())
        results[name] = {'VaR': var, 'MaxDD': max_dd}
    return pd.DataFrame(results)

scenarios = {
    'normal': 0,
    'mild_decline': -0.01,
    'severe_decline': -0.03,
    'extreme_crisis': -0.05,
    '2015_crash': -0.06,
}
```

## 关键细节与易错点

1. **均值-方差优化的不稳定性**：输入的预期收益和协方差矩阵的微小变化会导致权重剧变。实践中的解决方法：收缩估计（shrinkage）、Black-Litterman模型、约束权重范围。

2. **VaR的局限性**：VaR不满足次可加性——两个组合合并后的VaR可能大于各自VaR之和。CVaR（Expected Shortfall）更合理，也是巴塞尔协议推荐的风险指标。

3. **相关性在危机中上升**：正常时期相关性0.3的资产，在危机时可能升到0.8。基于正常时期相关性做的分散化在危机中可能失效。需要做压力测试验证。

4. **忽视流动性风险**：组合优化只考虑了波动率风险。但小盘股的流动性风险（想卖卖不掉）是实际组合管理中的重要约束。应加入流动性约束。

5. **过度依赖历史数据**：协方差矩阵基于历史数据估计，但市场结构会变化。2020年疫情前后的相关性结构完全不同。考虑使用指数加权协方差。

## 金融数据分析示例

**优化一个5只股票的组合，计算风险指标**：

```python
import akshare as ak
import pandas as pd
import numpy as np

stocks = {
    '600519': '贵州茅台', '601318': '中国平安',
    '000858': '五粮液', '300750': '宁德时代', '002475': '立讯精密'
}

price_data = {}
for code in stocks:
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                             start_date="20200101", end_date="20231231",
                             adjust="hfq")
    price_data[code] = df.set_index('日期')['收盘']

prices = pd.DataFrame(price_data)
returns = prices.pct_change().dropna()

# 最大夏普组合
sharpe_weights = max_sharpe_portfolio(returns)
print("最大夏普组合权重:")
for code, w in zip(stocks.keys(), sharpe_weights):
    print("  {}: {:.2%}".format(stocks[code], w))

# 风险平价组合
rp_weights = risk_parity_weights(returns)
print("\n风险平价组合权重:")
for code, w in zip(stocks.keys(), rp_weights):
    print("  {}: {:.2%}".format(stocks[code], w))

# 风险指标
port_returns = (returns * sharpe_weights).sum(axis=1)
print("\n95% VaR(日): {:.2%}".format(var_historical(port_returns)))
print("95% CVaR(日): {:.2%}".format(cvar_historical(port_returns)))

nav = (1 + port_returns).cumprod()
dd_info = drawdown_analysis(nav)
print("最大回撤: {:.2%}".format(dd_info['max_drawdown']))
print("回撤持续: {}天".format(dd_info['recovery_days']))

# 分散化收益
benefit = diversification_benefit(returns, sharpe_weights)
print("分散化收益: {:.2%}".format(benefit))

# 压力测试
stress_results = stress_test(port_returns, scenarios)
print("\n压力测试:")
print(stress_results)
```

## 拓展学习

- 《投资组合理论》——马科维茨的经典理论
- Black-Litterman模型——结合市场均衡和投资者观点的组合优化
- 风险平价实践——Bridgewater All Weather策略
- 巴塞尔协议风险计量——银行风控的监管框架
- 尾部风险管理——黑天鹅事件下的组合保护策略

## 参考链接

- https://www.portfoliovisualizer.com/ —— 组合优化可视化工具
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2299415 —— 风险平价论文
- https://www.bridgewater.com/resources/ All-Weather-Strategy.pdf —— All Weather策略
- https://www.mathworks.com/help/finance/portfolio-optimization.html —— 组合优化教程
