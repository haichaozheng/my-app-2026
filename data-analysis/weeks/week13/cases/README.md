# Week13 案例：决策树与随机森林——从规则到集体投票

> 对应课堂 notebook：`../market prediction - random forest_class.ipynb`
>
> 本案例使用上证指数日线数据（`sse_daily.csv`，本目录自带），在同一份数据上跑决策树与随机森林，对比 W11 线性回归，形成"三种模型思路横评"。

## 案例问题

> **上证指数明天涨还是跌？**

W11 是回归问题（涨多少），本案例改为**分类问题**（涨/跌）。同样用技术指标特征，但标签从连续收益率改为二分类。决策树学 if-else 规则，随机森林用多棵树投票——与 W11 线性回归"从数据学规律"和 W12 KNN"找邻居"形成三种思路的完整对照。

## 学习与运行指南

### 三种使用方式

| 方式 | 适合谁 | 命令 | 看什么 |
|------|--------|------|--------|
| 交互探索 | 深入理解原理 | `streamlit run app.py` | 切换模型/调 max_depth → 实时看准确率和特征重要性变化 |
| 一键复现 | 看完整流程 | `python tree_models.py` | 控制台输出每步指标 + output/ 目录生成 4 张图 |
| 看预置结果 | 快速浏览 | 打开 `sse_daily.csv` 看数据 | 表格数据，无需运行代码 |

### 建议学习顺序

1. 先读上方"案例问题"——带着问题往下看
2. 启动 `streamlit run app.py`，先用随机森林默认参数看一遍结果
3. 逐步调参数：调 max_depth 看过拟合曲线变化；切换模型对比准确率
4. 跑 `python tree_models.py`，对照控制台输出理解每一步
5. 读"改造指引"，接到自己的项目数据

### 前置条件

- 数据：`sse_daily.csv` 已预置在本目录，无需 tushare token 即可运行
- 如需重新获取数据：`python fetch_data.py`（需在项目根目录 `.env` 中配置 `TUSHARE_TOKEN`）
- 环境：项目 `.venv` 已激活，依赖已安装（`pip install -r requirements.txt`）

## 为什么需要这个案例？

| 现有材料 | 本案例补什么 |
|---|---|
| `market prediction - random forest_class.ipynb`：课堂演示用 | 一个独立可运行的 `.py`，学生照着改就能接到自己数据 |
| 课堂 notebook 覆盖面广但分散 | 聚焦三件事：树模型训练 → 特征重要性 → 四模型横评 |
| 无 W11-W13 模型横评材料 | 同一份数据上对比线性回归 / KNN / 决策树 / 随机森林 |

## 目录结构

```
cases/
├── README.md              ← 本文件
├── requirements.txt       ← 依赖
├── fetch_data.py          ← 获取上证指数日线（本目录自带数据，非首次无需运行）
├── sse_daily.csv          ← 预置数据
├── tree_models.py         ← 完整流程：分类标签构造 → 决策树 → 随机森林 → 特征重要性 → 四模型横评
├── app.py                 ← Streamlit 交互探索器：切换模型/调参数实时看图表
└── output/                ← 图表输出目录（运行后生成）
    ├── tree_depth_comparison.png
    ├── rf_vs_tree.png
    ├── feature_importance.png
    └── four_models_comparison.png
```

## 运行

```bash
# 在仓库根目录激活虚拟环境
.\.venv\Scripts\activate

# 安装依赖（如已装可跳过）
pip install -r data-analysis/weeks/week13/cases/requirements.txt

# 运行（一键复现）
python data-analysis/weeks/week13/cases/tree_models.py

# 或交互探索
streamlit run data-analysis/weeks/week13/cases/app.py
```

> **数据**：`sse_daily.csv` 已预置在本目录，直接运行即可。

## 数据与特征

本目录自带 `sse_daily.csv`（上证指数日线），特征列与 W11 案例一致：

| 特征 | 说明 |
|---|---|
| `ma_5` | 5 日收盘均价 |
| `ma_20` | 20 日收盘均价 |
| `ma_diff` | ma_5 − ma_20 |
| `vol_ratio` | 当日成交量 / 5 日均量 |
| `volatility_5` | 5 日收益率标准差 |
| `return_1d` | 当日涨跌幅 |
| `return_5d` | 5 日累计收益率 |

**标签变化**：W11 用 `next_return`（连续值，回归）；本案例用 `next_up`（0/1，分类）——次日收盘上涨为 1，下跌为 0。

## 完整流程

| 步骤 | 内容 | 对应课堂 |
|---|---|---|
| 1. 数据加载 | 读入本目录 `sse_daily.csv`，构造分类标签 | notebook §数据加载 |
| 2. 决策树 | `DecisionTreeClassifier`，观察过拟合倾向 | notebook §决策树 |
| 3. 树深度对比 | max_depth=1/3/5/10/None，看训练 vs 测试分数 | 课堂讨论"树太深→记住噪声" |
| 4. 随机森林 | `RandomForestClassifier`，对比单树 | notebook §随机森林 |
| 5. 特征重要性 | 随机森林的 `feature_importances_`，画排名图 | 课堂"反哺 W12 特征工程" |
| 6. 四模型横评 | 线性回归 / KNN / 决策树 / 随机森林，同一数据同一指标 | W11+W12+W13 三种思路总结 |

## 与课堂 notebook 的对应关系

| notebook 单元 | 本案例代码 |
|---|---|
| 决策树分裂演示 | `fit_decision_tree()` |
| 树过拟合讨论 | `compare_tree_depth()` |
| 随机森林 vs 单树 | `fit_random_forest()` |
| 特征重要性 | `plot_feature_importance()` |
| 三种模型对比（课堂口头） | `compare_four_models()`（代码实现） |

## 四模型横评设计

| 模型 | sklearn 类 | 思路 | 适用场景 |
|---|---|---|---|
| 逻辑回归 | `LogisticRegression` | 从数据学线性规律 | 线性可分，可解释 |
| KNN | `KNeighborsClassifier` | 找最近的 K 个邻居 | 小数据，非参 |
| 决策树 | `DecisionTreeClassifier` | 学 if-else 规则 | 非线性，可解释 |
| 随机森林 | `RandomForestClassifier` | 多棵树投票 | 非线性，稳健 |

> 注：W11 课堂讲的是线性回归（回归任务），这里横评改为分类任务，所以用逻辑回归替代线性回归。如果学生项目是回归任务，改回 `LinearRegression` 即可。

## 改造指引（接到自己的项目数据）

1. **数据**：`load_and_engineer()` 里改 CSV 路径为你的项目数据
2. **标签**：`next_up` 换成你要预测的分类标签（如"下周是否涨幅超 5%"）
3. **特征**：增减 `FEATURE_COLS` 里的列
4. **对比模型**：如果你的项目不是分类而是回归，把四个模型换成回归版本

## 教学要点

- **树深度=过拟合旋钮**：`compare_tree_depth()` 直观展示 max_depth 越大训练分越高、测试分先升后降
- **特征重要性反哺 W12**：随机森林告诉你哪些特征有用，直接对应 W12 特征工程的选择步骤
- **三种思路一句话**：线性回归学规律（fit 参数）、KNN 找邻居（不学习）、决策树学规则（if-else）——各有适用场景，不是"谁最好"
- **随机森林不是万能的**：如果单树测试分就很低，森林也救不了；特征工程才是根本

## 与 W11/W14 的关系

| 周次 | 案例 | 关系 |
|---|---|---|
| W11 | 线性回归预测次日收益率 | ← 数据来源，特征构造模板 |
| **W13** | **决策树/随机森林预测涨跌** | **同源数据，升级模型** |
| W14 | ML 信号 + 策略回测 | → 用 W13 的随机森林生成交易信号 |
