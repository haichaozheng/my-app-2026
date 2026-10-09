# Week11 案例：用上证指数预测次日收益率——线性回归完整流程

> 对应课堂 notebook：`../machine learning for stock prediction.ipynb`（§prediction tasks → §gradient descent → §线性回归）
>
> 课堂用 `gdp_satisfaction.csv`（GDP 与生活满意度）演示线性回归。本案例把同样的流程**原样搬到金融数据上**：用上证指数日线构造技术指标特征，预测次日收益率。学生照着改，就能接到自己的项目数据。

## 案例问题

> **上证指数明天涨多少？**

不是"涨不涨"（那是 W12 KNN 分类的任务），而是**涨多少**——一个回归问题。用历史日线的技术指标（均线、波动率、成交量变化等）作为特征，次日简单收益率作为标签，用线性回归做预测。

## 学习与运行指南

### 三种使用方式

| 方式 | 适合谁 | 命令 | 看什么 |
|------|--------|------|--------|
| 交互探索 | 深入理解原理 | `streamlit run app.py` | 调参数（特征选择/学习率/split比例）→ 实时看图表变化 |
| 一键复现 | 看完整流程 | `python linear_regression.py` | 控制台输出每步指标 + output/ 目录生成 4 张图 |
| 看预置结果 | 快速浏览 | 打开 `sse_daily.csv` 看数据 | 表格数据，无需运行代码 |

### 建议学习顺序

1. 先读上方"案例问题"——带着问题往下看
2. 启动 `streamlit run app.py`，先用默认参数看一遍结果
3. 逐步调参数：取消某个特征看 R² 怎么变；调学习率看 SGD 是否发散
4. 跑 `python linear_regression.py`，对照控制台输出理解每一步
5. 读"改造指引"，接到自己的项目数据

### 前置条件

- 数据：`sse_daily.csv` 已预置在本目录，无需 tushare token 即可运行
- 如需重新获取数据：`python fetch_data.py`（需在项目根目录 `.env` 中配置 `TUSHARE_TOKEN`）
- 环境：项目 `.venv` 已激活，依赖已安装（`pip install -r requirements.txt`）

## 为什么需要这个案例？

| 课堂 notebook | 本案例 |
|---|---|
| `gdp_satisfaction.csv`：29 个国家，1 个特征（GDP），1 个标签（生活满意度） | 上证指数 10+ 年日线，6+ 个特征，1 个标签（次日收益率） |
| 玩具数据，学生难以迁移 | 金融数据，直接对应学生项目场景 |
| 特征少，看不到特征工程的必要性 | 多特征，自然引出 W12/W13 的特征选择与重要性 |
| 数据量小，过拟合不明显 | 样本量大，train/test 差距可见 |

## 目录结构

```
cases/
├── README.md              ← 本文件
├── requirements.txt       ← 依赖
├── fetch_data.py          ← 用 tushare 获取上证指数日线并落盘（本目录自带数据，非首次无需运行）
├── sse_daily.csv          ← 预置数据（上证指数日线，fetch_data.py 生成）
├── linear_regression.py   ← 完整回归流程：特征构造 → train/test split → sklearn + 手写 SGD → 评估 → 过拟合自检
├── app.py                 ← Streamlit 交互探索器：调参数实时看图表变化
└── output/                ← 图表输出目录（运行后生成）
    ├── scatter_return_vs_ma5.png
    ├── regression_fit.png
    ├── sgd_vs_sklearn.png
    └── overfitting_check.png
```

## 运行

```bash
# 在仓库根目录激活虚拟环境
.\.venv\Scripts\activate

# 安装依赖
pip install -r data-analysis/weeks/week11/cases/requirements.txt

# 数据已预置（sse_daily.csv），直接运行：

# 一键复现（控制台输出 + output/ 图表）
python data-analysis/weeks/week11/cases/linear_regression.py

# 或交互探索（Streamlit 网页）
streamlit run data-analysis/weeks/week11/cases/app.py

# 如需重新获取数据（需 TUSHARE_TOKEN）：
python data-analysis/weeks/week11/cases/fetch_data.py
```

输出：控制台打印各阶段指标，`output/` 目录保存 4 张图。

## 数据

| 文件 | 内容 |
|---|---|
| `sse_daily.csv` | 上证指数（000001.SH）日线，2015-01 至今 |

字段（`fetch_data.py` 从 tushare `daily` 接口获取）：

| 字段 | 说明 |
|---|---|
| `trade_date` | 交易日期 |
| `open` / `high` / `low` / `close` | 开高低收 |
| `vol` | 成交量（手） |
| `amount` | 成交额（千元） |
| `pct_chg` | 涨跌幅（%） |

## 特征构造

`linear_regression.py` 从原始日线构造以下特征：

| 特征 | 计算 | 直觉 |
|---|---|---|
| `ma_5` | 5 日收盘均价 | 短期趋势 |
| `ma_20` | 20 日收盘均价 | 中期趋势 |
| `ma_diff` | ma_5 − ma_20 | 金叉/死叉信号 |
| `vol_ratio` | 当日成交量 / 5 日均量 | 量价配合 |
| `volatility_5` | 5 日收益率标准差 | 近期波动 |
| `return_1d` | 当日涨跌幅 | 动量 |
| `return_5d` | 5 日累计收益率 | 中期动量 |

**标签**：次日简单收益率 `next_return = close[t+1] / close[t] - 1`

## 完整流程（与课堂 notebook 对应）

| 步骤 | 课堂 notebook | 本案例 | 对应代码 |
|---|---|---|---|
| 1. 数据加载 | `gdp_satisfaction.csv` | `sse_daily.csv` + 特征构造 | `load_and engineer()` |
| 2. 散点图直觉 | GDP vs 满意度散点图 | return_1d vs next_return 散点图 | `plot_scatter()` |
| 3. train/test split | `train_test_split` | 同（按时间切，前 80% 训练，后 20% 测试） | `split_data()` |
| 4. sklearn 回归 | `LinearRegression().fit()` | 同 | `sklearn_fit()` |
| 5. 看系数 | `model.coef_` | 同，并打印特征名对照 | `sklearn_fit()` |
| 6. 画回归线 | 回归线叠加散点 | 预测值 vs 真实值散点 + y=x 参考线 | `plot_prediction()` |
| 7. 手写 SGD | `gd()` 函数填空 | 完整实现（`code.docx` 有课堂答案） | `sgd_fit()` |
| 8. 过拟合自检 | 全量 fit vs split fit | 训练 R² vs 测试 R² 对比 | `overfitting_check()` |

### 关键设计：时间序列的 train/test split

课堂用 `train_test_split(random_state=42)` 随机打乱。本案例**按时间切**——前 80% 训练、后 20% 测试——因为金融数据有强时序性，随机打乱会造成数据泄漏（用未来信息预测过去）。这一点在 W12 数据泄漏一节会正式讲，这里先埋下。

## 与课堂 notebook 的对应关系

| notebook 单元 | 本案例代码 |
|---|---|
| §prediction tasks + §what is ML | README"案例问题"部分 |
| §gradient descent | `sgd_fit()`：完整实现梯度下降 |
| §train/test split | `split_data()`：时间序列分割 |
| §线性回归 sklearn | `sklearn_fit()` |
| `gd()` 函数填空 | `sgd_fit()`（完整版，可对照 `code.docx`） |
| `gdp_satisfaction.csv` | `sse_daily.csv` + 特征工程 |

## 改造指引（接到自己的项目数据）

1. **换数据**：`fetch_data.py` 里的 `ts_code` 换成你的股票/指数，或直接读 W4 落盘的 CSV
2. **换特征**：在 `engineer_features()` 里增减特征列
3. **换标签**：把 `next_return` 换成你要预测的目标（如 5 日收益率、波动率、是否涨停）
4. **保持流程不变**：load → engineer → split → fit → evaluate → check

## 教学要点

- **fit 不是魔法**：手写 SGD 让学生看到 `fit` 就是用梯度下降反复更新参数——`code.docx` 的答案可以对照
- **时间序列不能随机 split**：与课堂随机 split 形成对比，为 W12 数据泄漏埋伏笔
- **R² 可能是负的**：金融数据噪声大，测试集 R² 为负（模型还不如直接猜均值）是正常的——这正是"预测很难"的直观体会
- **特征多≠更好**：6 个特征里有几个可能没用，为 W13 特征重要性埋伏笔

## 密钥安全

- 如使用 `.env`，已在 `.gitignore`，不要提交到仓库
- 不要在代码中硬编码 token
