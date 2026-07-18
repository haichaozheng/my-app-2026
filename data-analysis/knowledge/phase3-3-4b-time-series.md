# 时间序列分析与预测

> **引入时机**：W13 | **核心挑战**：金融数据天然是时间序列——如何预测市场趋势？ | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

金融数据最根本的特征是时间结构——股价、利率、汇率、成交量都是沿时间轴记录的序列。忽视这种时间依赖性，把金融数据当作普通横截面数据处理，会导致严重的建模错误和虚假结论。当你需要在产品中添加趋势预测、季节性分析或周期识别功能时，时间序列分析是不可绕过的核心技能。

金融数据分析产品最常见的用户需求之一就是"未来会怎样"：某行业ETF下月走势如何？利率周期处于什么阶段？大盘是否接近拐点？时间序列模型为这些问题提供了统计框架。与纯粹的机器学习模型相比，时间序列模型更注重趋势、季节性和自相关结构的建模，在金融预测中有独特的价值。

理解时间序列分析还能帮助你正确评估其他模型的表现——如果你的ML模型连简单的ARIMA基线都打不过，那它很可能只是在过拟合噪声而非捕捉真正的信号。

## 这个知识点的核心内容

### 时间序列基础

时间序列数据的核心组成部分：

- **趋势（Trend）**：长期的上升或下降方向，如A股市场的长期增长趋势
- **季节性（Seasonality）**：固定周期的规律性波动，如年末资金面紧张导致的季节性
- **周期性（Cyclicity）**：非固定周期的波动，如经济周期（通常2-10年）
- **不规则成分（Irregularity）**：无法由上述成分解释的随机波动

**平稳性**：时间序列分析的基础假设。平稳序列的统计特性（均值、方差、自相关）不随时间变化。大多数金融价格序列是非平稳的（有趋势），但收益率序列通常是平稳的。检验平稳性使用ADF检验（Augmented Dickey-Fuller Test）。

### ARIMA模型

ARIMA(p, d, q)是经典的时间序列预测模型：

- **AR(p)自回归**：当前值取决于过去p个值的线性组合。yₜ = c + φ₁yₜ₋₁ + φ₂yₜ₋₂ + ... + φₚyₜ₋ₚ + εₜ
- **I(d)差分**：对序列做d次差分使其平稳。d=1表示一阶差分：y'ₜ = yₜ - yₜ₋₁
- **MA(q)移动平均**：当前值取决于过去q个误差项。yₜ = c + εₜ + θ₁εₜ₋₁ + ... + θqεₜ₋q

参数选择方法：
- 画ACF（自相关函数）和PACF（偏自相关函数）图
- ACF拖尾+PACF截尾→AR模型
- ACF截尾+PACF拖尾→MA模型
- 两者都拖尾→ARMA模型
- 使用auto_arima（pmdarima库）自动选择参数

### 趋势分解

将时间序列分解为趋势、季节性和残差：

- **加法分解**：yₜ = Trendₜ + Seasonalₜ + Residualₜ（季节性幅度恒定）
- **乘法分解**：yₜ = Trendₜ × Seasonalₜ × Residualₜ（季节性幅度随趋势变化）
- **STL分解**：基于LOESS的分解方法，对异常值鲁棒，允许季节性随时间变化

在金融中，趋势分解常用于：识别市场长期趋势、去除季节性后分析真实趋势、构建趋势跟踪策略。

### Prophet

Facebook开发的 Prophet 适合具有强季节效应和多个季节模式的时间序列：

- **优点**：自动检测趋势转折点、处理多季节性（周/月/年）、对缺失值和异常值鲁棒、无需大量调参
- **模型组成**：y(t) = g(t) + s(t) + h(t) + εₜ，其中g(t)是趋势、s(t)是季节性、h(t)是假日效应
- **金融应用**：带有节假日效应的市场预测、行业指数趋势分析、资金流向周期识别

### 金融时间序列的特殊模式

金融时间序列有若干独特的统计特征：

- **波动率聚集**：大波动后跟大波动，小波动后跟小波动（GARCH效应）
- **肥尾分布**：极端事件发生的概率高于正态分布假设
- **杠杆效应**：下跌时的波动率上升幅度大于等幅上涨时
- **长记忆性**：收益率绝对值和平方的自相关衰减缓慢
- **日历效应**：周一效应、月末效应、节假日效应等

## 关键细节与易错点

### 对价格序列直接建模

股价是典型的非平稳序列（随机游走），直接对价格建模几乎必然失败。应该对收益率（价格的变化率）建模，或使用差分使序列平稳。这是最常见也最致命的错误。

### 未来数据泄漏

时间序列模型的训练和测试必须严格按时间划分——训练集在前，测试集在后。绝不能随机打乱顺序。使用`sklearn`的`TimeSeriesSplit`而非`train_test_split`。

### 忽视季节性

金融数据存在显著的日历效应：月末资金面紧张、年初效应、节假日前后成交量变化。如果模型不考虑这些季节性因素，会把季节性波动误认为趋势信号。

### ARIMA不适合长期预测

ARIMA模型的预测在短期（1-5步）内相对可靠，但随着预测步数增加，预测会快速收敛到序列均值。不要用ARIMA做超过10步以上的预测——置信区间会宽到毫无意义。

### 忽视结构变化

金融市场存在结构性变化（regime change）：2008年金融危机前后市场机制不同，2015年股灾前后A股的波动特征不同。如果训练数据跨越了结构变化点，模型的参数估计会失真。需要检测结构变化并在必要时分段建模。

### Prophet的局限性

Prophet在趋势稳定、季节性明显的场景表现好，但对于金融数据的高频波动和快速转折点，Prophet的预测往往滞后。Prophet更适合中低频的宏观指标和行业指数，而非个股日度数据。

## 金融数据分析示例

**场景**：使用ARIMA模型预测某行业ETF的月度收益率，为投资组合调整提供参考。

**步骤1：数据获取与平稳性检验**：

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

df = pd.read_csv("industry_etf_monthly.csv", parse_dates=["date"], index_col="date")
returns = df["close"].pct_change().dropna()

result = adfuller(returns)
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
```

**步骤2：ACF/PACF分析确定模型参数**：

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(returns, lags=12, ax=axes[0])
plot_pacf(returns, lags=12, ax=axes[1])
plt.tight_layout()
plt.savefig("acf_pacf.png", dpi=150)
```

**步骤3：拟合ARIMA模型**：

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(returns, order=(1, 0, 1))
fitted = model.fit()
print(fitted.summary())

forecast = fitted.forecast(steps=3)
print(f"下3个月预测收益率: {forecast.values}")
```

**步骤4：Prophet对比**：

```python
from prophet import Prophet

prophet_df = returns.reset_index()
prophet_df.columns = ["ds", "y"]

m = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    changepoint_prior_scale=0.05
)
m.fit(prophet_df)

future = m.make_future_dataframe(periods=3, freq="M")
forecast_prophet = m.predict(future)
print(forecast_prophet[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(3))
```

**步骤5：时间序列交叉验证**：

```python
from sklearn.metrics import mean_squared_error
import numpy as np

window = 36
forecasts_arima = []
forecasts_naive = []
actuals = []

for i in range(window, len(returns) - 1):
    train = returns.iloc[:i]
    test = returns.iloc[i]

    model = ARIMA(train, order=(1, 0, 1)).fit()
    forecasts_arima.append(model.forecast(steps=1).iloc[0])
    forecasts_naive.append(train.iloc[-1])
    actuals.append(test)

rmse_arima = np.sqrt(mean_squared_error(actuals, forecasts_arima))
rmse_naive = np.sqrt(mean_squared_error(actuals, forecasts_naive))
print(f"ARIMA RMSE: {rmse_arima:.4f}")
print(f"Naive RMSE: {rmse_naive:.4f}")
```

如果ARIMA的RMSE显著低于Naive（上期值作为预测），说明模型捕捉到了有用的模式。

## 拓展学习

- **GARCH模型**：专门建模波动率的模型，捕捉金融数据的波动率聚集现象，VaR计算的核心工具
- **VAR向量自回归**：多变量时间序列模型，可以分析行业间的联动关系和溢出效应
- **状态空间模型与卡尔曼滤波**：时变参数模型，适用于金融市场结构性变化的建模
- **深度学习时间序列**：LSTM、Transformer在时间序列预测中的应用，适合大规模复杂模式
- **协整与配对交易**：非平稳序列之间的长期均衡关系，统计套利的基础

## 参考链接

- https://otexts.com/fpp3/ - 《Forecasting: Principles and Practice》在线版，时间序列预测最佳入门
- https://www.statsmodels.org/stable/tsa.html - Statsmodels时间序列分析文档
- https://facebook.github.io/prophet/ - Prophet官方文档
- https://alkaline-ml.com/pmdarima/ - pmdarima库，auto_arima自动参数选择
- https://vectorbt.dev/ - 量化交易中的时间序列方法
