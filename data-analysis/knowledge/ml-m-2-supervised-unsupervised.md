# 监督学习vs无监督学习

> **引入时机**：W5 | **核心挑战**：聚类/分类等不同ML范式各自解决什么问题？ | **层级**：Recommended for ML track

## 为什么要在项目阶段学习这个知识点？

ML赛道的学生必须理解两大范式——监督学习和无监督学习——的根本区别，才能在面对金融问题时选择正确的方法。监督学习需要标签（"这只股票未来涨了"），无监督学习不需要标签（"这些股票行为模式相似"）。选错范式，就像用锤子拧螺丝——不是不行，但很别扭。

金融场景中两种范式都有丰富的应用。信用评分需要标签（违约/未违约），这是监督学习；行业分组不需要预定义标签，这是无监督学习。很多实际项目需要两种范式结合——先用无监督方法发现模式，再用监督方法做预测。

理解这两种范式还有更深层的好处：它帮你理解ML的本质——监督学习是在寻找输入到输出的映射，无监督学习是在发现数据内在的结构。这种理解比记住算法名称重要得多。

## 这个知识点的核心内容

### 监督学习

**核心特征**：有标签数据，学习输入到输出的映射

**分类问题**：输出是离散类别

| 金融场景 | 输入特征 | 输出标签 | 模型 |
|---------|---------|---------|------|
| 信用评分 | 收入、负债率、历史记录 | 违约/不违约 | 逻辑回归、XGBoost |
| 涨跌预测 | 技术指标、因子值 | 涨/跌 | 随机森林、SVM |
| 欺诈检测 | 交易模式、行为特征 | 正常/欺诈 | 异常检测（半监督） |
| 客户分群营销 | 交易频次、持仓特征 | 高价值/普通/流失 | 逻辑回归、神经网络 |

**回归问题**：输出是连续值

| 金融场景 | 输入特征 | 输出标签 | 模型 |
|---------|---------|---------|------|
| 收益率预测 | 因子值、宏观指标 | 未来N日收益率 | 线性回归、XGBoost |
| 波动率预测 | 历史波动率、交易量 | 未来波动率 | GARCH、LSTM |
| 房价预测 | 面积、位置、楼层 | 房价 | 随机森林、XGBoost |
| 信用额度 | 信用评分、收入 | 合理额度 | 回归树 |

**监督学习的标准流程**：
```python
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# 1. 准备数据
X = feature_df
y = target_series

# 2. 时间序列切分（不能用随机切分！）
tscv = TimeSeriesSplit(n_splits=5)

# 3. 训练与评估
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # 标准化（只用训练集的统计量）
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 训练
    model.fit(X_train_scaled, y_train)

    # 评估
    y_pred = model.predict(X_test_scaled)
    print(classification_report(y_test, y_pred))
```

### 无监督学习

**核心特征**：无标签数据，发现数据内在结构

**聚类**：将数据分为若干组，组内相似、组间差异大

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# K-Means聚类
def cluster_stocks(feature_df, n_clusters=5):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_df)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    score = silhouette_score(X_scaled, labels)
    print("轮廓系数: {:.3f}".format(score))

    feature_df['cluster'] = labels
    return feature_df, kmeans

# 选择最优K
def find_optimal_k(feature_df, k_range=range(2, 11)):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_df)

    scores = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        scores.append({'k': k, 'silhouette': score})
        print("K={}, 轮廓系数={:.3f}".format(k, score))

    return pd.DataFrame(scores)
```

**降维**：将高维数据压缩到低维，保留主要信息

```python
from sklearn.decomposition import PCA

def reduce_dimensions(feature_df, n_components=2):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_df)

    pca = PCA(n_components=n_components)
    X_reduced = pca.fit_transform(X_scaled)

    print("解释方差比: {}".format(pca.explained_variance_ratio_))
    print("累计解释方差: {:.2%}".format(pca.explained_variance_ratio_.sum()))

    return X_reduced, pca
```

**异常检测**：识别与大多数数据差异显著的样本

```python
from sklearn.ensemble import IsolationForest

def detect_anomalies(feature_df, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    labels = iso_forest.fit_predict(feature_df)

    feature_df['anomaly'] = labels == -1
    n_anomalies = feature_df['anomaly'].sum()
    print("检测到{}个异常样本({:.1%})".format(n_anomalies, n_anomalies/len(feature_df)))

    return feature_df
```

### 金融场景下的范式选择

**决策树**：

```
你有标签数据吗？
├── 是 → 监督学习
│   ├── 输出是类别？→ 分类
│   │   ├── 二分类：涨跌、违约/正常
│   │   └── 多分类：市场状态、信用等级
│   └── 输出是连续值？→ 回归
│       ├── 收益率预测、波动率预测
│       └── 房价预测、额度预测
└── 否 → 无监督学习
    ├── 想分组？→ 聚类
    │   ├── 股票风格分组、行业自动分类
    │   └── 客户细分
    ├── 想压缩维度？→ 降维
    │   ├── 因子提取（PCA）
    │   └── 高维可视化
    └── 想找异常？→ 异常检测
        ├── 交易异常、闪崩预警
        └── 财务造假检测
```

**两种范式结合的常见模式**：
1. 先聚类再分类：先用聚类将股票分组，每组内分别训练预测模型
2. 用无监督特征增强监督学习：用PCA/聚类结果作为新特征加入监督模型
3. 半监督学习：少量标签+大量无标签数据联合训练

### 聚类用于行业分组 vs 分类用于信用评分

**场景一：无监督聚类做行业分组**
```python
# 用财务指标对股票聚类，发现"隐性行业分组"
financial_features = pd.DataFrame({
    'roe': [...],
    'revenue_growth': [...],
    'debt_ratio': [...],
    'profit_margin': [...],
    'pe_ratio': [...],
}, index=stock_codes)

stock_clusters, model = cluster_stocks(financial_features, n_clusters=8)

# 分析每个簇的特征
for cluster_id in range(8):
    cluster_stocks = stock_clusters[stock_clusters['cluster'] == cluster_id]
    print("\n簇{} - {}只股票".format(cluster_id, len(cluster_stocks)))
    print("  平均ROE: {:.2%}".format(cluster_stocks['roe'].mean()))
    print("  平均营收增长: {:.2%}".format(cluster_stocks['revenue_growth'].mean()))
    print("  代表股票: {}".format(cluster_stocks.index[:5].tolist()))
```

**场景二：监督分类做信用评分**
```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# 有标签：客户是否违约
X = customer_features  # 收入、负债率、信用历史等
y = customer_default   # 0=正常, 1=违约

# 时间序列切分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, shuffle=False
)

# 训练
model = GradientBoostingClassifier(n_estimators=100, max_depth=4)
model.fit(X_train, y_train)

# 评估
y_prob = model.predict_proba(X_test)[:, 1]
print("AUC: {:.4f}".format(roc_auc_score(y_test, y_prob)))

# 信用评分映射
def prob_to_score(prob, base_score=600, pdo=20):
    odds = (1 - prob) / prob
    score = base_score + pdo / np.log(2) * np.log(odds)
    return int(score)
```

## 关键细节与易错点

1. **金融数据不能用随机切分**：金融时序数据有强时间依赖性，随机切分会导致数据泄露。必须用TimeSeriesSplit或按时间点切分。

2. **聚类结果需要解释**：聚类给出分组但不给含义。必须人工分析每个簇的特征，赋予业务解释。没有解释的聚类是没用的。

3. **类别不平衡问题**：金融中违约/欺诈是少数类（<5%）。直接训练会导致模型把所有样本都预测为多数类。解决方法：SMOTE过采样、类别权重调整、关注AUC而非准确率。

4. **无监督方法的评估更难**：监督学习有明确的评估指标（准确率、AUC），无监督学习没有。轮廓系数、肘部法则只是参考，最终还是要看业务效果。

5. **特征标准化**：不同量纲的特征必须标准化。PE比率可能是10-100，ROE可能是-50%到50%，不标准化会让量纲大的特征主导聚类/模型。

## 金融数据分析示例

**聚类用于股票风格分组 + 分类用于涨跌预测**：

```python
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Part 1: 无监督聚类 - 股票风格分组
# 计算每只股票的风格因子
style_features = pd.DataFrame({
    'market_cap': [...],      # 市值
    'pe_ratio': [...],        # PE
    'momentum_12m': [...],    # 12月动量
    'volatility_60d': [...],  # 60日波动率
    'turnover_60d': [...],    # 60日换手率
}, index=stock_codes)

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(style_features)

# 聚类
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
style_features['style_cluster'] = kmeans.fit_predict(X_scaled)

# 分析风格分组
style_names = {
    0: '大盘价值', 1: '小盘成长', 2: '大盘成长',
    3: '小盘价值', 4: '高波动投机'
}
for cluster_id, name in style_names.items():
    stocks_in_cluster = style_features[style_features['style_cluster'] == cluster_id]
    print("{}: {}只股票, 平均市值{:.0f}亿".format(
        name, len(stocks_in_cluster), stocks_in_cluster['market_cap'].mean()))

# Part 2: 监督分类 - 涨跌预测
# 在每个风格组内训练预测模型
for cluster_id in range(5):
    cluster_stocks = style_features[style_features['style_cluster'] == cluster_id].index

    # 获取该组股票的特征和标签
    X_cluster = feature_df.loc[cluster_stocks]
    y_cluster = (future_return_df.loc[cluster_stocks] > 0).astype(int)

    # 训练
    model = RandomForestClassifier(n_estimators=50, max_depth=5)
    model.fit(X_cluster, y_cluster)

    # 预测
    y_pred = model.predict(X_cluster)
    print("风格组{} 预测准确率: {:.2%}".format(
        cluster_id, accuracy_score(y_cluster, y_pred)))
```

## 拓展学习

- Scikit-learn用户指南——监督和无监督方法的系统教程
- 《统计学习方法》——李航，ML算法的理论基础
- 聚类算法对比——K-Means vs DBSCAN vs 层次聚类
- 不平衡学习——金融场景中类别不平衡的处理方法
- 半监督学习——少标签+多无标签的混合方法

## 参考链接

- https://scikit-learn.org/stable/unsupervised_learning.html —— 无监督学习教程
- https://scikit-learn.org/stable/supervised_learning.html —— 监督学习教程
- https://imbalanced-learn.org/ —— 不平衡学习库
- https://scikit-learn.org/stable/modules/clustering.html —— 聚类算法对比
