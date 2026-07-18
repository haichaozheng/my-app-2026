# 模型评估与验证

> **引入时机**：W13 | **核心挑战**：模型训练出来后，如何判断它是否真的有效？ | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

训练出一个ML模型并不难，但判断它是否"真的有效"却极具挑战性。在金融领域，这个挑战尤为严峻——金融数据的信噪比极低，模型很容易在训练集上表现优异而在实盘中完全失效。历史上无数的量化基金都因为过拟合的模型在训练中回测表现完美，但上线后亏损累累。如果你的产品集成了不可靠的预测功能，轻则流失用户，重则误导投资决策造成实际损失。

模型评估不仅仅是看一个准确率数字。不同的业务场景需要不同的评估指标，不同的数据特性需要不同的验证策略。金融时间序列的验证尤其复杂——不能随机打乱数据，不能有未来信息泄漏，还要考虑市场状态的变化。理解评估方法论，是你构建可靠金融ML产品的安全网。

在PBL项目中，你需要向用户和评审展示你的模型确实有效。科学严谨的评估结果比"训练准确率99%"的数字更有说服力，也更能体现你的专业能力。

## 这个知识点的核心内容

### 分类评估指标

**混淆矩阵**：评估分类模型的起点

|  | 预测正 | 预测负 |
|--|-------|-------|
| 实际正 | TP | FN |
| 实际负 | FP | TN |

- **Accuracy**：(TP+TN) / (TP+TN+FP+FN)，总体正确率，样本不平衡时误导
- **Precision**：TP / (TP+FP)，预测为正中真正为正的比例，"宁缺毋滥"
- **Recall**：TP / (TP+FN)，真正为正中被找出的比例，"宁错勿漏"
- **F1-Score**：2 x Precision x Recall / (Precision + Recall)，两者的调和平均
- **AUC-ROC**：真阳性率vs假阳性率曲线下面积，衡量分类器整体排序能力，0.5为随机，1.0为完美
- **AUC-PR**：Precision-Recall曲线下面积，样本极度不平衡时比AUC-ROC更可靠

金融场景的指标选择：
- 信用违约预测：关注Recall（漏掉违约客户代价大），看AUC-PR
- 欺诈检测：关注Precision（误报代价高），看F1-Score
- 选股信号：关注AUC-ROC（排序能力）和IC（信息系数）

### 回归评估指标

- **MAE**：绝对误差均值，直观、对异常值鲁棒
- **MSE / RMSE**：平方误差均值/均方根，对大误差惩罚更重
- **R-squared**：模型解释的方差比例，1为完美，0为等同均值预测
- **MAPE**：百分比误差均值，适合不同量纲比较，但y接近0时失效
- **IC（信息系数）**：预测值与真实值的秩相关系数（Spearman），量化因子预测能力的标准指标

### 交叉验证

交叉验证是评估模型泛化能力的核心方法：

- **K折交叉验证**：将数据分为K份，轮流用K-1份训练、1份测试。不适用于时间序列
- **时间序列交叉验证（Rolling Window）**：按时间顺序滑动窗口，训练集在前、测试集在后。金融数据必须使用此方法
- **扩展窗口验证**：训练窗口逐步扩大，每次在最新数据上测试。适合样本量少的场景
- **组合式交叉验证（Combinatorial Purged CV）**：Marcos Lopez de Prado提出，避免金融数据中的信息泄漏

### 过拟合识别与防止

过拟合是模型在训练集上表现好但泛化差的现象：

- **症状**：训练集指标远优于测试集指标；训练集R-squared=0.95但测试集R-squared=0.1
- **偏差-方差权衡**：简单模型欠拟合（高偏差），复杂模型过拟合（高方差），需要找到平衡点
- **防止方法**：正则化（L1/L2）、早停（Early Stopping）、Dropout、集成方法、增加数据量

### 金融回测

金融模型特有的评估框架：

- **回测（Backtesting）**：在历史数据上模拟模型的表现，计算策略收益
- **关键回测指标**：年化收益率、最大回撤、夏普比率、Calmar比率
- **回测陷阱**：幸存者偏差（只分析现存股票）、未来函数、过拟合回测、忽略交易成本
- **样本外检验**：保留最近一段数据完全不参与训练和调参，只在最终评估时使用

## 关键细节与易错点

### 用Accuracy评估不平衡数据

金融数据普遍不平衡（违约率2-5%、涨停概率小于1%）。Accuracy在这种场景下完全失去意义——把所有样本都预测为多数类就能获得95%以上的Accuracy。必须使用AUC-ROC、F1或Precision-Recall曲线。

### 随机划分时间序列数据

使用`train_test_split`随机打乱金融时间序列数据，会导致未来信息泄漏到训练集中。必须按时间顺序划分，使用`TimeSeriesSplit`或手动按日期切分。

### 在测试集上调参

反复在测试集上评估并据此调整超参数，测试集实际上变成了训练集。正确做法：将数据分为训练/验证/测试三份，在验证集上调参，只在测试集上做最终评估（且只评估一次）。

### 忽视交易成本和滑点

回测中模型看起来赚钱，但加入交易成本、滑点和冲击成本后可能亏损。尤其是高频交易策略，交易成本对净收益影响巨大。回测时务必加入合理的交易成本假设。

### 过拟合回测

通过反复调整策略参数使回测结果最优化，本质上是把噪声当信号。防止方法：样本外验证、参数稳定性检验（参数微调不应导致结果剧变）、复杂度惩罚（AIC/BIC）。

### 评估窗口太短

用太短的测试窗口评估模型（如只用最近1个月）可能恰好处于某个特殊市场状态，结果不可靠。测试窗口应覆盖不同市场环境（牛市、熊市、震荡市）。

## 金融数据分析示例

**场景**：评估一个股票5日收益方向预测模型（分类），使用时间序列交叉验证。

**时间序列交叉验证**：

```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score)

tscv = TimeSeriesSplit(n_splits=5)
metrics = {"accuracy": [], "precision": [], "recall": [],
           "f1": [], "auc_roc": []}

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics["accuracy"].append(accuracy_score(y_test, y_pred))
    metrics["precision"].append(precision_score(y_test, y_pred))
    metrics["recall"].append(recall_score(y_test, y_pred))
    metrics["f1"].append(f1_score(y_test, y_pred))
    metrics["auc_roc"].append(roc_auc_score(y_test, y_prob))

for name, values in metrics.items():
    print(f"{name}: {np.mean(values):.4f} +/- {np.std(values):.4f}")
```

**与基线模型对比**：

```python
from sklearn.dummy import DummyClassifier

dummy = DummyClassifier(strategy="most_frequent")
dummy_metrics = {"auc_roc": []}

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    dummy.fit(X_train, y_train)
    y_prob_dummy = dummy.predict_proba(X_test)[:, 1]
    dummy_metrics["auc_roc"].append(roc_auc_score(y_test, y_prob_dummy))

print(f"Baseline AUC-ROC: {np.mean(dummy_metrics['auc_roc']):.4f}")
print(f"Model AUC-ROC: {np.mean(metrics['auc_roc']):.4f}")
```

**回测评估**：

```python
def backtest_strategy(predictions, returns, cost_rate=0.001):
    positions = np.where(predictions == 1, 1, 0)
    trade_costs = np.abs(np.diff(positions, prepend=0)) * cost_rate
    strategy_returns = positions * returns - trade_costs
    cumulative = (1 + strategy_returns).cumprod()

    max_drawdown = (cumulative / cumulative.cummax() - 1).min()
    sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
    annual_return = (1 + strategy_returns.mean()) ** 252 - 1

    return {
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
    }

results = backtest_strategy(y_pred, test_returns)
print(f"Annual Return: {results['annual_return']:.2%}")
print(f"Max Drawdown: {results['max_drawdown']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
```

## 拓展学习

- **Walk-forward分析**：比简单回测更严谨的模型评估方法，模拟真实的投资决策过程
- **White Reality Check**：检验模型收益是否统计显著，防止数据窥探偏差
- **Deflated Sharpe Ratio**：考虑多次测试后的夏普比率修正，避免多重比较问题
- **模型监控与漂移检测**：上线后持续监控模型表现，检测数据分布漂移
- **A/B测试**：在真实用户中对比不同模型版本的效果

## 参考链接

- https://scikit-learn.org/stable/modules/model_evaluation.html - Scikit-learn模型评估文档
- https://mlflow.org/ - MLflow模型跟踪与评估平台
- https://github.com/ranaroussi/quantstats - QuantStats组合回测分析库
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3870260 - Marcos Lopez de Prado的组合式交叉验证论文
- https://www.backtrader.com/ - Backtrader回测框架
