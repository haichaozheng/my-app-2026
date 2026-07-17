# AI辅助ML建模全流程

> **引入时机**：W13 | **核心挑战**：如何用AI辅助编程完成ML建模全流程？ | **层级**：Recommended for ML track

## 为什么要在项目阶段学习这个知识点？

ML建模不是一步到位的——从数据准备到特征工程，从模型训练到评估调优，从部署到监控，每个环节都需要写大量代码。AI辅助编程可以显著加速这个过程，但前提是你知道在哪个环节、以什么方式、让AI帮你做什么。

AI辅助ML建模的核心不是"让AI替你做ML"，而是"让AI处理重复性编码工作，你专注于高价值的决策"。数据清洗的样板代码、特征工程的模板函数、评估指标的计算——这些AI可以快速生成。但选择什么特征、用什么模型、如何解释结果——这些需要你的判断力。

对于财经院校学生，AI辅助ML建模还有一个特殊价值：你们可能对ML的实现细节不够熟悉，AI可以帮你跨越"知道方法但写不出代码"的鸿沟。你只需清楚地描述你想做什么，AI就能生成对应的代码框架，然后你再根据金融场景的需求进行调整。

## 这个知识点的核心内容

### 环节一：数据准备

AI擅长：生成数据加载、清洗、预处理的代码模板
你的角色：定义清洗规则、处理领域特定的数据问题

Prompt要点：描述数据格式 + 清洗规则 + 金融领域约束

```python
import pandas as pd
import numpy as np

def preprocess_stock_data(df):
    df = df.sort_values(['code', 'date'])

    suspended = df['volume'] == 0
    df.loc[suspended, 'close'] = df.groupby('code')['close'].ffill()
    df.loc[suspended, 'return'] = 0

    df['return'] = df.groupby('code')['close'].pct_change()

    listing_days = df.groupby('code').cumcount()
    df = df[listing_days >= 60]

    return df
```

### 环节二：特征工程

AI擅长：生成常见特征的计算代码、特征变换方法
你的角色：基于金融逻辑定义有意义的特征、避免数据泄露

Prompt要点：列出因子定义 + 强调无look-ahead bias + 指定输出格式

```python
def generate_factors(df):
    result = pd.DataFrame(index=df.index)

    result['momentum_20'] = df.groupby('code')['close'].pct_change(20)

    result['volatility_20'] = df.groupby('code')['return'].transform(
        lambda x: x.rolling(20).std()
    )

    result['turnover_20'] = df.groupby('code')['turnover'].transform(
        lambda x: x.rolling(20).mean()
    )

    return result
```

### 环节三：模型训练

AI擅长：生成模型训练的标准代码、超参数搜索框架
你的角色：选择模型类型、设定合理的超参数范围、防止过拟合

Prompt要点：指定模型 + 时序切分 + 类别不平衡 + 防过拟合约束

```python
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score

def train_xgboost_pipeline(X, y, n_splits=5):
    tscv = TimeSeriesSplit(n_splits=n_splits)

    pos_ratio = y.sum() / len(y)
    scale_pos = (1 - pos_ratio) / pos_ratio

    scores = []
    models = []

    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = XGBClassifier(
            max_depth=5, min_child_weight=10,
            scale_pos_weight=scale_pos,
            n_estimators=100, learning_rate=0.1,
            random_state=42
        )
        model.fit(X_train, y_train)

        y_prob = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_prob)
        scores.append(auc)
        models.append(model)

        print("Fold {} AUC: {:.4f}".format(fold + 1, auc))

    print("Average AUC: {:.4f} +/- {:.4f}".format(np.mean(scores), np.std(scores)))
    return models, scores
```

### 环节四：模型评估

AI擅长：生成评估指标计算代码、可视化代码
你的角色：选择合适的评估指标、解读结果、判断模型是否可用

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, classification_report)
import matplotlib.pyplot as plt

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred))
    print("AUC: {:.4f}".format(roc_auc_score(y_test, y_prob)))

    # 特征重要性
    importance = pd.Series(model.feature_importances_, index=X_test.columns)
    importance.nlargest(10).plot(kind='barh')
    plt.title("Top 10 Feature Importance")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    plt.close()

    return {
        'auc': roc_auc_score(y_test, y_prob),
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
    }
```

### 环节五：模型解释

AI擅长：生成SHAP分析代码、可视化代码
你的角色：将模型解释与金融逻辑关联、识别可疑的特征依赖

```python
import shap

def explain_model(model, X_sample):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    shap.summary_plot(shap_values, X_sample, show=False)
    plt.tight_layout()
    plt.savefig("shap_summary.png")
    plt.close()

    # 单个预测解释
    shap.force_plot(explainer.expected_value, shap_values[0], X_sample.iloc[0],
                    matplotlib=True, show=False)
    plt.savefig("shap_single.png")
    plt.close()

    return shap_values
```

### 环节六：部署集成

AI擅长：生成API服务代码、Streamlit界面代码
你的角色：设计用户交互流程、处理边界情况、性能优化

```python
# FastAPI服务
from fastapi import FastAPI
import joblib

app = FastAPI(title="ML Prediction Service")
model = joblib.load("model.pkl")

@app.post("/predict")
def predict(features: dict):
    df = pd.DataFrame([features])
    prob = model.predict_proba(df)[0][1]
    score = prob_to_score(prob)
    return {
        "default_probability": round(float(prob), 4),
        "credit_score": int(score),
        "risk_level": "high" if prob > 0.3 else "medium" if prob > 0.1 else "low"
    }

# Streamlit界面
import streamlit as st

st.title("ML预测演示")
input_data = {}
for feature_name in feature_names:
    input_data[feature_name] = st.number_input(feature_name)

if st.button("预测"):
    result = predict(input_data)
    st.metric("信用评分", str(result["credit_score"]))
    st.metric("风险等级", result["risk_level"])
```

### ML场景的Prompt模式

**数据准备Prompt**：
```
角色：Python数据分析专家
任务：为{金融场景}编写数据预处理pipeline
数据描述：{字段、格式、已知问题}
处理要求：{缺失值、异常值、特征变换规则}
约束：{不能有look-ahead bias、必须按时间排序}
输出：可运行的Python函数
```

**特征工程Prompt**：
```
角色：量化研究员
任务：为{预测目标}设计特征工程方案
可用数据：{数据字段列表}
需要因子：{列出因子名称和定义}
约束：所有特征只能使用t日及之前的数据
输出：每个因子的计算代码 + 简要说明
```

**模型训练Prompt**：
```
角色：ML工程师
任务：训练{模型类型}用于{预测目标}
数据特点：{样本量、类别比例、特征维度}
约束：
  - 使用TimeSeriesSplit而非random split
  - 处理类别不平衡
  - 限制模型复杂度防过拟合
  - 输出每折评估指标
输出：完整训练代码 + 评估结果
```

### AI辅助ML的注意事项

**必须人工检查的环节**：
1. 数据泄露：AI可能无意中使用了未来数据
2. 特征逻辑：AI生成的因子是否符合金融常识
3. 评估方法：是否用了正确的时序切分
4. 结果解读：AI可能过度乐观地解读模型效果

**AI容易出错的地方**：
1. 随机切分金融时序数据（导致数据泄露）
2. 忽略类别不平衡
3. 过度复杂的模型架构
4. 不正确的交叉验证方式
5. 忽略特征的时序依赖性

## 关键细节与易错点

1. **AI生成的代码必须逐行审查**：特别是特征工程部分，AI很容易引入look-ahead bias。检查每个特征的计算是否只用了历史数据。

2. **不要让AI替你选模型**：AI倾向于推荐"最先进"的模型，但金融场景中简单模型往往更稳健。模型选择应基于问题特点而非技术新颖度。

3. **Prompt越具体，输出越可靠**：包含数据格式、约束条件、输出要求、金融规则的Prompt，比泛泛的"帮我训练一个模型"效果好得多。

4. **迭代式Prompt**：不要期望一次Prompt得到完美的ML Pipeline。先让AI生成框架，再针对每个环节逐步优化。

5. **保留所有版本**：AI生成的代码可能被覆盖。用Git管理每个版本的代码，方便回退和比较。

## 金融数据分析示例

**使用AI辅助完成股票涨跌预测的全流程**：

```python
# Step 1: 数据准备（AI生成框架 + 你调整规则）
df = preprocess_stock_data(raw_data)

# Step 2: 特征工程（AI生成计算代码 + 你验证无泄露）
features = generate_factors(df)

# Step 3: 构建标签
target = (df.groupby('code')['return'].shift(-5) > 0).astype(int)

# Step 4: 合并并去NaN
ml_data = pd.concat([features, target.rename('target')], axis=1).dropna()

# Step 5: 训练模型（AI生成pipeline + 你设定约束）
X = ml_data.drop('target', axis=1)
y = ml_data['target']
models, scores = train_xgboost_pipeline(X, y)

# Step 6: 评估（AI生成评估代码 + 你解读结果）
best_model = models[-1]
metrics = evaluate_model(best_model, X_test, y_test)

# Step 7: 解释（AI生成SHAP代码 + 你关联金融逻辑）
shap_values = explain_model(best_model, X_test[:100])

# Step 8: 部署（AI生成API/UI代码 + 你设计交互流程）
# FastAPI + Streamlit集成
```

完整的AI辅助ML流程：你定义问题→AI生成代码框架→你审查和调整→AI帮你调试→你解读结果→AI帮你可视化→你设计产品→AI帮你生成界面。

## 拓展学习

- Scikit-learn Pipeline——标准化ML工作流
- MLflow——ML实验追踪与模型管理
- SHAP——模型可解释性工具
- AutoML工具——H2O、FLAML等自动化ML
- MLOps实践——模型部署与监控的最佳实践

## 参考链接

- https://scikit-learn.org/stable/modules/compose.html —— Scikit-learn Pipeline
- https://mlflow.org/docs/latest/index.html —— MLflow文档
- https://shap.readthedocs.io/ —— SHAP模型解释
- https://microsoft.github.io/FLAML/ —— FLAML AutoML
