# Week14 案例：ML 交易信号 + 策略回测——从预测到赚钱

> 对应课堂 notebook：`../Trading strategy evaluation - sma.ipynb`（SMA 回测）+ `../evaluate trading strategy.ipynb`（策略评估）
>
> 本案例是 W11→W13→W14 故事线的终点：用随机森林预测涨跌 → 生成买卖信号 → 回测 → 评估到底赚不赚钱。本目录完全自包含，自带数据与脚本。

## 案例问题

> **用模型预测涨跌来交易，能赚钱吗？**

W11 建了线性回归（预测涨多少），W13 建了随机森林（预测涨还是跌）。但"预测准"和"能赚钱"之间还有一段路——交易有成本、信号有延迟、回撤会要命。本周把模型预测转化为交易信号，用回测检验到底赚不赚钱。

## 学习与运行指南

### 三种使用方式

| 方式 | 适合谁 | 命令 | 看什么 |
|------|--------|------|--------|
| 交互探索 | 深入理解原理 | `streamlit run app.py` | 调 split 比例/max_depth → 实时看净值曲线和指标变化 |
| 一键复现 | 看完整流程 | `python ml_backtest.py` | 控制台输出每步指标 + output/ 目录生成 4 张图 |
| 看预置结果 | 快速浏览 | 打开 `sse_daily.csv` 看数据 | 表格数据，无需运行代码 |

### 建议学习顺序

1. 先读上方"案例问题"——带着问题往下看
2. 启动 `streamlit run app.py`，先勾选全部策略看净值曲线对比
3. 逐步调参数：调 train/test 比例看过拟合；调 max_depth 看 RF 信号变化
4. 跑 `python ml_backtest.py`，对照控制台输出理解每一步
5. 读"改造指引"，接到自己的项目数据

### 前置条件

- 数据：`sse_daily.csv` 已预置在本目录，无需 tushare token 即可运行
- 如需重新获取数据：`python fetch_data.py`（需在项目根目录 `.env` 中配置 `TUSHARE_TOKEN`）
- 环境：项目 `.venv` 已激活，依赖已安装（`pip install -r requirements.txt`）

## 为什么需要这个案例？

| 现有 notebook | 本案例补什么 |
|---|---|
| `Trading strategy evaluation - sma.ipynb`：SMA 规则型信号 | 从规则型信号升级为 ML 型信号 |
| `evaluate trading strategy.ipynb`：策略评估方法 | 一个完整闭环：数据→特征→ML 信号→回测→评估→对比 SMA |
| W11/W13 有模型，但没接交易 | 把 W13 的随机森林直接接到回测引擎上 |

## 目录结构

```
cases/
├── README.md              ← 本文件
├── requirements.txt       ← 依赖
├── fetch_data.py          ← 获取上证指数日线（本目录自带数据，非首次无需运行）
├── sse_daily.csv          ← 预置数据
├── ml_backtest.py         ← 完整流程：SMA 基线 → ML 信号生成 → 回测 → 评估 → 对比
├── app.py                 ← Streamlit 交互探索器：调参数实时看净值曲线和指标
└── output/                ← 图表输出目录（运行后生成）
    ├── equity_curve_comparison.png
    └── metrics_comparison.png
```

## 运行

```bash
# 在仓库根目录激活虚拟环境
.\.venv\Scripts\activate

# 安装依赖（如已装可跳过）
pip install -r data-analysis/weeks/week14/cases/requirements.txt

# 运行（一键复现）
python data-analysis/weeks/week14/cases/ml_backtest.py

# 或交互探索
streamlit run data-analysis/weeks/week14/cases/app.py
```

> **数据**：`sse_daily.csv` 已预置在本目录，直接运行即可。

## 完整流程

```
上证指数日线
    │
    ├── 特征构造（复用 W11/W13）
    │
    ├── SMA 基线：ma_5 上穿 ma_20 → 买入；下穿 → 空仓
    │
    ├── ML 信号：随机森林预测涨跌 → 预测涨→买入；预测跌→空仓
    │
    ├── 回测引擎
    │   ├── 买入持有基准
    │   ├── SMA 策略收益曲线
    │   └── ML 策略收益曲线
    │
    └── 评估指标
        ├── 累计收益率
        ├── 夏普比率（风险调整后收益）
        ├── 最大回撤（最惨时亏多少）
        └── 胜率（信号准确率）
```

## 回测设计

### 信号生成

| 策略 | 信号逻辑 | 类型 |
|---|---|---|
| 买入持有 | 一直满仓 | 基准 |
| SMA 交叉 | ma_5 > ma_20 → 买入；否则空仓 | 规则型 |
| ML 信号 | 随机森林预测涨 → 买入；预测跌 → 空仓 | ML 型 |

### 评估指标

| 指标 | 计算 | 含义 |
|---|---|---|
| 累计收益率 | 末日净值 / 初始资金 - 1 | 总共赚了多少 |
| 年化收益率 | (1 + 累计收益率)^(252/天数) - 1 | 换算成年度 |
| 夏普比率 | (年化收益 - 无风险利率) / 年化波动 | 风险调整后收益，越高越好 |
| 最大回撤 | max((peak - trough) / peak) | 最惨时亏多少 |
| 信号胜率 | 正确预测涨跌的比例 | 信号准不准 |

### 关键设计：训练/测试分离（W11 的直接应用）

| 阶段 | 数据 | 用途 |
|---|---|---|
| 训练期 | 前 80% 数据 | 拟合随机森林 |
| 测试期 | 后 20% 数据 | 生成信号 + 回测 |

> **这是 W11 train/test split 在量化交易中的直接应用**——模型在训练集上调好，必须在没见过的测试集上回测。在训练集上回测 = 数据泄漏 = "回测很赚钱，实盘很亏钱"。

## 与课堂 notebook 的对应关系

| notebook | 本案例 |
|---|---|
| `Trading strategy evaluation - sma.ipynb` | `sma_baseline()` 复现 SMA 信号 → 回测 |
| `evaluate trading strategy.ipynb` | `backtest()` + `evaluate()` |
| `machine learning for stock prediction.ipynb` §strategy | `ml_signal()` 把 RF 预测转为信号 |

## 与 W11/W13 的关系

| 周次 | 案例 | 本周复用 |
|---|---|---|
| W11 | 线性回归 + 特征构造 | → 特征构造模板、`sse_daily.csv` 数据 |
| W13 | 决策树/随机森林 | → 随机森林模型直接接入信号生成 |
| **W14** | **ML 信号 + 回测** | **W11+W13 的集大成应用** |

## 改造指引（接到自己的项目数据）

1. **数据**：`load_data()` 里改 CSV 路径为你的个股/指数
2. **特征**：复用 W11 的特征，或加入你 W12 构造的新特征
3. **模型**：换 KNN 或线性回归生成信号，对比哪个效果好
4. **交易规则**：加入交易成本（如每次买卖扣 0.1%）、仓位管理（不满仓）
5. **评估**：加入更多指标（如 Calmar 比率、换手率）

## 教学要点

- **预测准 ≠ 能赚钱**：模型准确率 55% 看起来比随机猜好，但扣除交易成本后可能亏钱
- **回测是测试集验证**：W11 的 train/test split 在这里有了真实意义——在训练集上回测就是作弊
- **SMA 是基线不是敌人**：简单规则有时比复杂模型好——如果 ML 信号打不过 SMA，说明模型没学到有用的东西
- **夏普比率 > 收益率**：赚 20% 但中间亏过 30% 的策略，不如稳定赚 15% 的策略
- **最大回撤决定生死**：回测里 -50% 看起来能恢复，实盘里你可能已经割肉了

## 密钥安全

本案例不直接调用 tushare（复用 W11 落盘的 CSV），无需配置密钥。
如需重新获取数据，请运行 W11 的 `fetch_data.py`。
