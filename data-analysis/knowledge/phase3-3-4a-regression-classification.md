# 回归与分类模型

> **引入时机**：W11 | **核心挑战**：用户想知道"这只股票未来会不会涨"或"违约概率多大" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

当你的金融数据分析产品需要回答预测性问题时，回归和分类是最基础也最实用的两类模型。"这只股票下周会涨吗？"是分类问题；"预计涨多少？"是回归问题；"这只债券的违约概率是多少？"是分类问题中的概率估计。理解回归和分类模型的工作原理和适用场景，是你为产品添加智能预测功能的起点。

很多同学对ML模型存在两极化态度：要么觉得太复杂不敢碰，要么直接上最复杂的模型。实际上，线性回归和逻辑回归在金融领域的应用极其广泛，它们不仅是基线模型，很多时候就是最终选用的模型——因为监管要求可解释性，因为数据量不够支撑复杂模型，因为简单模型在金融非平稳环境中反而更稳健。掌握从简单到复杂的模型梯度，让你在不同场景下做出合理选择。

## 这个知识点的核心内容

### 线性回归

线性回归假设目标变量与特征之间存在线性关系：

- **模型形式**：y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
- **损失函数**：最小化均方误差（MSE）
- **正则化变体**：Ridge（L2正则化，防止系数过大）、Lasso（L1正则化，自动特征选择）、ElasticNet（L1+L2）
- **金融应用**：收益率预测、因子模型（Fama-French三因子模型本质就是线性回归）、风险敞口估计

### 逻辑回归

逻辑回归用于二分类问题，输出概率而非类别：

- **模型形式**：P(y=1) = 1 / (1 + e^(-(β₀ + β₁x₁ + ... + βₙxₙ)))
- **损失函数**：对数损失（Log-Loss / Cross-Entropy）
- **输出解释**：概率值，可以设置阈值转换为类别预测
- **金融应用**：信用违约预测、涨跌方向预测、欺诈检测、贷款审批

### 决策树

决策树通过递归分裂特征空间做出预测：

- **优点**：直观易解释、无需特征缩放、能处理非线性关系和特征交互
- **缺点**：容易过拟合、对数据变化敏感（高方差）、预测面不光滑
- **金融应用**：信用评分规则生成、客户分群、特征重要性分析

### 随机森林

随机森林是决策树的集成方法，通过bagging降低方差：

- **核心思想**：训练多棵决策树，每棵使用数据子集和特征子集，最终投票或平均
- **优点**：抗过拟合、特征重要性排序、对超参数不敏感
- **缺点**：不可解释（黑盒）、训练和预测较慢、对时间序列数据不直接适用
- **金融应用**：因子收益预测、违约概率估计、特征筛选

### XGBoost / 梯度提升

梯度提升是另一种集成策略，通过序列化地训练弱学习器：

- **核心思想**：每棵新树拟合前一轮的残差，逐步逼近目标
- **XGBoost优势**：正则化防过拟合、并行训练、处理缺失值、高效实现
- **缺点**：超参数较多、需要仔细调参、不可解释
- **金融应用**：量化因子选股、信用评分模型、Kaggle金融竞赛的主流选择

### 评估指标

不同模型类型需要不同的评估指标：

**分类指标**：

- Accuracy：准确率，样本不平衡时误导
- Precision：精确率，预测为正的样本中真正为正的比例
- Recall：召回率，真正为正的样本中被正确预测的比例
- F1-Score：Precision和Recall的调和平均
- AUC-ROC：真阳性率vs假阳性率曲线下面积，对样本不平衡鲁棒

**回归指标**：

- MAE：平均绝对误差，对异常值鲁棒
- MSE / RMSE：均方误差/均方根误差，对大误差惩罚更重
- R²：决定系数，模型解释的方差比例
- MAPE：平均绝对百分比误差，适合不同量纲的比较

## 关键细节与易错点

### 逻辑回归不是回归

尽管名字里有"回归"，逻辑回归是分类算法。它用线性回归的形式建模对数概率（log-odds），输出经过sigmoid函数转换为概率。不要用逻辑回归预测连续数值。

### 忽视特征缩放

正则化线性模型（Ridge、Lasso、ElasticNet）和梯度提升对特征量纲敏感。不同量纲的特征会导致正则化对某些特征惩罚过重。需要对特征进行标准化（StandardScaler）或归一化（MinMaxScaler）。决策树和随机森林不需要特征缩放。

### 决策树深度不加控制

决策树不加限制会一直分裂直到每个叶节点只有一个样本，导致严重过拟合。必须设置`max_depth`、`min_samples_split`、`min_samples_leaf`等参数限制树的复杂度。

### XGBoost不加正则化

XGBoost默认配置容易过拟合，尤其在金融数据这种信噪比低的场景。关键参数：`max_depth`（通常3-6）、`learning_rate`（通常0.01-0.1）、`n_estimators`与`early_stopping`配合使用、`reg_alpha`和`reg_lambda`正则化项。

### 只看Accuracy评估分类模型

在金融分类问题中，Accuracy是最容易误导的指标。如果违约率2%，模型把所有样本都预测为"不违约"就能获得98%的Accuracy。应该使用AUC-ROC、F1-Score或Precision-Recall曲线来评估。

### 线性回归假设不检验

线性回归有若干假设：线性关系、误差独立同分布、同方差性、无多重共线性。金融数据经常违反这些假设（如异方差、自相关），直接使用可能导致推断不可靠。至少检查残差图和VIF（方差膨胀因子）。

## 金融数据分析示例

**场景**：构建一个信用违约预测模型，使用上市公司的财务指标预测其是否会在未来1年内违约。

**数据准备**：

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("company_financials.csv")
features = ["debt_ratio", "current_ratio", "roe", "revenue_growth",
            "net_margin", "asset_turnover", "interest_coverage"]
X = df[features]
y = df["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**逻辑回归基线模型**：

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

lr = LogisticRegression(class_weight="balanced", random_state=42)
lr.fit(X_train_scaled, y_train)

y_pred = lr.predict(X_test_scaled)
y_prob = lr.predict_proba(X_test_scaled)[:, 1]

print(classification_report(y_test, y_pred))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.4f}")
```

**XGBoost提升模型**：

```python
from xgboost import XGBClassifier

xgb = XGBClassifier(
    max_depth=4,
    learning_rate=0.05,
    n_estimators=200,
    scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1]),
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42
)
xgb.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

y_pred_xgb = xgb.predict(X_test)
y_prob_xgb = xgb.predict_proba(X_test)[:, 1]
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob_xgb):.4f}")
```

**特征重要性分析**：

```python
import matplotlib.pyplot as plt

importance = pd.Series(xgb.feature_importances_, index=features)
importance.sort_values().plot(kind="barh")
plt.title("Feature Importance - Credit Default Prediction")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
```

通过对比逻辑回归和XGBoost的AUC-ROC，可以量化模型提升幅度。逻辑回归的优点是系数可直接解释（如"资产负债率每增加1个标准差，违约概率的对数增加0.5"），XGBoost的优点是预测精度更高。

## 拓展学习

- **LightGBM与CatBoost**：与XGBoost并列的梯度提升框架，各有优势。LightGBM训练更快，CatBoost自动处理类别特征
- **多分类问题**：One-vs-Rest和Softmax回归，适用于预测涨/跌/平等多类别场景
- **概率校准**：Platt Scaling和Isotonic Regression，让模型输出的概率更准确，金融风险估计中关键
- **SHAP值**：解释任何模型的预测结果，金融监管合规的重要工具
- **样本不平衡处理**：SMOTE过采样、ADASYN、类权重调整等技巧

## 参考链接

- https://scikit-learn.org/stable/supervised_learning.html - Scikit-learn监督学习文档
- https://xgboost.readthedocs.io/ - XGBoost官方文档
- https://christophm.github.io/interpretable-ml-book/ - 可解释ML在线教材
- https://imbalanced-learn.org/ - 样本不平衡处理库
- https://shap.readthedocs.io/ - SHAP模型解释库
