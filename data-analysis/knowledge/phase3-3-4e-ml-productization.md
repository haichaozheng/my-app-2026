# ML产品化架构

> **引入时机**：W13 | **核心挑战**：ML模型如何嵌入数据分析产品？ | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

在本地Jupyter Notebook中训练出一个效果不错的ML模型只是起点，真正的挑战在于如何将模型集成到产品中，让用户能实际使用它。模型训练和模型服务是两个截然不同的工程问题——训练关注精度，服务关注延迟、可用性和可维护性。如果不理解ML产品化的架构设计，你可能会在模型集成时遇到各种问题：预测接口响应太慢、模型更新时服务中断、训练-服务特征不一致导致预测偏差。

在PBL项目中，你的金融数据分析产品需要将ML预测功能无缝嵌入用户界面。用户点击"预测"按钮后，产品需要在合理时间内返回结果，并且结果必须与训练时的模型行为一致。这要求你理解从数据管道到模型训练到推理服务的完整链路。

ML产品化还涉及一个关键问题：模型不是静态的。金融市场不断变化，模型效果会随时间衰减，你需要设计模型更新的机制。理解ML产品化架构，能让你在项目初期就考虑这些工程问题，避免后期大规模重构。

## 这个知识点的核心内容

### ML产品化全链路

一个ML产品包含以下核心环节：

1. **数据管道**：数据获取→清洗→特征计算→存储。数据是ML产品的血液，管道必须稳定可靠
2. **模型训练**：特征工程→模型选择→训练→评估→注册。训练可以离线进行，不直接影响用户
3. **模型服务**：模型加载→接收请求→特征计算→推理→返回结果。服务面向用户，需要低延迟高可用
4. **模型监控**：性能监控→数据漂移检测→模型更新决策。持续保障模型质量

### 训练管道（Training Pipeline）

训练管道负责从原始数据到可用模型的全过程：

- **数据版本管理**：每次训练使用的数据快照应该被记录，确保可复现。DVC（Data Version Control）是常用工具
- **特征计算管道**：训练和推理必须使用完全相同的特征计算逻辑。将特征工程代码模块化，避免训练-服务偏差
- **实验跟踪**：记录每次训练的超参数、指标、模型文件。MLflow是主流的实验跟踪工具
- **模型注册**：训练完成的模型存入模型仓库，附带版本号和评估指标

### 推理API（Inference API）

推理API是模型服务的核心，接收用户请求返回预测结果：

- **批量预测**：一次性对大量数据做预测，如每日收盘后更新所有股票的预测评分。延迟要求低，可用定时任务
- **在线预测**：实时响应用户请求，如用户输入股票代码后返回预测结果。延迟要求高，通常需要API服务
- **API设计**：输入（股票代码/特征值）→ 特征计算 → 模型推理 → 输出（预测值/概率）。使用FastAPI构建RESTful API

### 模型服务架构

不同规模的产品需要不同的服务架构：

- **嵌入式**：模型直接加载在应用进程中（如Streamlit应用内加载pickle模型）。最简单，适合低流量原型
- **API服务**：独立部署的模型API，应用通过HTTP调用。解耦训练和服务，适合中等流量
- **微服务**：模型服务、特征服务、数据服务独立部署，通过消息队列通信。适合大规模生产系统

### 训练-服务偏差

这是ML产品化中最隐蔽也最危险的bug：

- **特征偏差**：训练时用了标准化（fit_transform），服务时用新数据标准化（只transform但用训练时的参数）。必须保存训练时的scaler/encoder
- **数据偏差**：训练时用的数据源版本与服务时不同（如数据源API更新了字段含义）
- **代码偏差**：训练时的特征计算逻辑与服务时不一致（如训练用5日均线，服务算成了6日）

防止方法：将特征计算代码统一为一个共享模块，训练和服务都调用同一份代码。

### 模型更新策略

金融模型需要定期更新以适应市场变化：

- **定期重训**：每天/每周用最新数据重新训练模型。简单但可能有训练失败风险
- **模型热切换**：新模型训练完成后无缝替换旧模型，不中断服务。需要模型版本管理
- **灰度发布**：新模型先对少量流量服务，确认效果后再全量切换
- **模型回滚**：新模型出问题时快速回退到上一版本。需要保留历史模型版本

## 关键细节与易错点

### 训练-服务特征不一致

最常见的ML产品化bug。训练时标准化用的是训练集的均值和方差，服务时必须使用保存的scaler参数，而非重新计算。所有预处理步骤（标准化、编码、缺失值填充）的参数都必须持久化保存。

### 模型文件过大

有些复杂模型（如XGBoost with n_estimators=10000）的pickle文件可能达到数百MB，每次请求加载模型耗时很长。解决方案：应用启动时加载模型到内存，保持常驻；或使用ONNX格式减小模型体积。

### 忽视推理延迟

训练时只关注模型精度，服务时才发现预测太慢。用户点击"分析"后等待30秒是不可接受的。在精度和延迟之间需要权衡——可能需要用更轻量的模型或预计算部分结果。

### 没有模型版本管理

直接覆盖模型文件，出了问题无法回滚。每次训练应生成带版本号的模型文件（如`model_v1.3.pkl`），并记录对应的训练数据和超参数。

### 缺少健康检查和降级方案

模型API可能因内存不足、依赖缺失等原因崩溃。如果没有健康检查，用户会看到不明错误。降级方案：当模型服务不可用时，返回规则引擎的结果或缓存的历史预测，而非直接报错。

## 金融数据分析示例

**场景**：设计一个股票分析产品的ML架构——从数据管道到模型训练到API服务到Streamlit展示。

**整体架构**：

```
数据管道 → 特征存储 → 模型训练 → 模型注册 → API服务 → Streamlit前端
    |            |           |           |           |
    v            v           v           v           v
 AKShare      Redis      MLflow      MinIO      FastAPI
 (行情数据)   (特征缓存)  (实验跟踪)  (模型存储)  (推理API)
```

**特征计算模块（共享）**：

```python
from sklearn.preprocessing import StandardScaler
import joblib

def compute_features(df):
    df = df.copy()
    df["return_5d"] = df["close"].pct_change(5)
    df["volatility_20d"] = df["return_5d"].rolling(20).std()
    df["ma5"] = df["close"].rolling(5).mean()
    df["price_vs_ma5"] = df["close"] / df["ma5"] - 1
    return df

class FeaturePipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_cols = ["return_5d", "volatility_20d", "price_vs_ma5"]

    def fit(self, df):
        features = df[self.feature_cols].dropna()
        self.scaler.fit(features)
        return self

    def transform(self, df):
        features = df[self.feature_cols].dropna()
        scaled = self.scaler.transform(features)
        return scaled

    def save(self, path):
        joblib.dump({"scaler": self.scaler, "cols": self.feature_cols}, path)

    @classmethod
    def load(cls, path):
        data = joblib.load(path)
        pipeline = cls()
        pipeline.scaler = data["scaler"]
        pipeline.feature_cols = data["cols"]
        return pipeline
```

**训练脚本**：

```python
from xgboost import XGBClassifier
import joblib

pipeline = FeaturePipeline()
train_features = pipeline.fit(train_df)
X_train = pipeline.transform(train_df)
y_train = train_df["target"].dropna()

model = XGBClassifier(max_depth=4, n_estimators=200)
model.fit(X_train, y_train)

pipeline.save("artifacts/feature_pipeline_v1.pkl")
joblib.dump(model, "artifacts/model_v1.pkl")
```

**推理API（FastAPI）**：

```python
from fastapi import FastAPI
import joblib
import akshare as ak

app = FastAPI()
pipeline = FeaturePipeline.load("artifacts/feature_pipeline_v1.pkl")
model = joblib.load("artifacts/model_v1.pkl")

@app.get("/predict/{symbol}")
def predict(symbol: str):
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", count=60)
    features = pipeline.transform(df)
    prob = model.predict_proba(features[-1:])[:, 1][0]
    return {"symbol": symbol, "up_probability": round(prob, 4)}
```

**Streamlit前端调用**：

```python
import streamlit as st
import requests

symbol = st.text_input("Stock Symbol", "000001")
if st.button("Predict"):
    resp = requests.get(f"http://localhost:8000/predict/{symbol}")
    result = resp.json()
    st.metric("Up Probability", f"{result['up_probability']:.1%}")
```

## 拓展学习

- **MLflow**：开源ML平台，实验跟踪、模型注册、模型部署一体化
- **Kubeflow**：Kubernetes上的ML平台，适合大规模ML系统
- **Feature Store**：特征存储（Feast、Hopsworks），统一管理训练和服务的特征
- **模型压缩**：量化、剪枝、蒸馏，减小模型体积和推理延迟
- **边缘部署**：将模型部署到终端设备，减少网络延迟，适合实时交易场景

## 参考链接

- https://mlflow.org/ - MLflow官方文档
- https://fastapi.tiangolo.com/ - FastAPI官方文档
- https://feast.dev/ - Feast特征存储
- https://mad.withgoogle.com/ - Google的ML系统设计指南
- https://docs.databricks.com/ - Databricks ML平台文档
