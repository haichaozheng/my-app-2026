"""Week13 Streamlit 探索器：决策树与随机森林。

完全自包含——数据、特征工程、模型训练全部在本文件内。
交互调参：模型选择 / max_depth / n_estimators / K / 特征选择。

运行：streamlit run app.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

ALL_FEATURES = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]
FEATURE_LABELS = {
    "ma_5": "5日均线", "ma_20": "20日均线", "ma_diff": "均线差",
    "vol_ratio": "量比", "volatility_5": "5日波动率",
    "return_1d": "当日收益率", "return_5d": "5日收益率",
}


def load_and_engineer() -> pd.DataFrame:
    csv_path = Path(__file__).resolve().parent / "sse_daily.csv"
    if not csv_path.exists():
        st.error(f"未找到 {csv_path}，请先运行 `python fetch_data.py` 获取数据。")
        st.stop()
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    df["trade_date"] = pd.to_datetime(df["trade_date"], format="%Y%m%d")
    df = df.sort_values("trade_date").reset_index(drop=True)
    close = df["close"]
    df["ma_5"] = close.rolling(5).mean()
    df["ma_20"] = close.rolling(20).mean()
    df["ma_diff"] = df["ma_5"] - df["ma_20"]
    df["vol_ratio"] = df["vol"] / df["vol"].rolling(5).mean()
    daily_return = close.pct_change()
    df["volatility_5"] = daily_return.rolling(5).std()
    df["return_1d"] = df["pct_chg"] / 100
    df["return_5d"] = close / close.shift(5) - 1
    df["next_return"] = close.shift(-1) / close - 1
    df["next_up"] = (df["next_return"] > 0).astype(int)
    df = df.dropna(subset=ALL_FEATURES + ["next_up"]).reset_index(drop=True)
    return df


st.set_page_config(page_title="树模型探索器", layout="wide")
st.title("决策树与随机森林探索器：上证指数涨跌预测")

df = load_and_engineer()

# ── 侧栏 ──
with st.sidebar:
    st.header("参数设置")
    model_name = st.selectbox(
        "选择模型", ["随机森林", "决策树", "KNN", "逻辑回归"]
    )
    selected_features = st.multiselect(
        "选择特征", ALL_FEATURES, default=ALL_FEATURES,
        format_func=lambda x: FEATURE_LABELS.get(x, x),
    )
    max_depth = st.slider("max_depth（树模型）", 1, 20, 5)
    n_estimators = st.slider("n_estimators（随机森林）", 10, 200, 100, 10)
    k_neighbors = st.slider("K（KNN）", 1, 20, 7)

if len(selected_features) == 0:
    st.warning("请至少选择一个特征。")
    st.stop()

# ── 准备数据 ──
split_idx = int(len(df) * 0.8)
X_train = df.iloc[:split_idx][selected_features].values
y_train = df.iloc[:split_idx]["next_up"].values
X_test = df.iloc[split_idx:][selected_features].values
y_test = df.iloc[split_idx:]["next_up"].values

# ── Section 1: 数据概览 ──
st.subheader("1. 数据概览")
c1, c2, c3 = st.columns(3)
c1.metric("样本数", f"{len(df)}")
c2.metric("涨占比", f"{df['next_up'].mean():.2%}")
c3.metric("训练/测试", f"{len(y_train)} / {len(y_test)}")

# ── Section 2: 当前模型结果 ──
st.subheader(f"2. {model_name} 训练结果")

MODEL_MAP = {
    "随机森林": lambda: RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, random_state=42),
    "决策树": lambda: DecisionTreeClassifier(
        max_depth=max_depth, random_state=42),
    "KNN": lambda: KNeighborsClassifier(n_neighbors=k_neighbors),
    "逻辑回归": lambda: LogisticRegression(max_iter=1000, random_state=42),
}

model = MODEL_MAP[model_name]()
model.fit(X_train, y_train)
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc = accuracy_score(y_test, model.predict(X_test))

c1, c2 = st.columns(2)
c1.metric("训练准确率", f"{train_acc:.4f}")
c2.metric("测试准确率", f"{test_acc:.4f}", delta=f"{test_acc - 0.5:+.4f} vs 随机")

# ── Section 3: 树深度对比（始终显示） ──
st.subheader("3. 树深度对比（过拟合观察）")
depths = [1, 2, 3, 5, 8, 10, 15, None]
tr_scores, te_scores = [], []
for d in depths:
    t = DecisionTreeClassifier(max_depth=d, random_state=42)
    t.fit(X_train, y_train)
    tr_scores.append(accuracy_score(y_train, t.predict(X_train)))
    te_scores.append(accuracy_score(y_test, t.predict(X_test)))

fig, ax = plt.subplots(figsize=(8, 4))
labels = [str(d) if d else "None" for d in depths]
x = range(len(labels))
ax.plot(x, tr_scores, "o-", label="训练准确率", color="#3b82f6")
ax.plot(x, te_scores, "s-", label="测试准确率", color="#ef4444")
ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--", label="随机猜测")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel("max_depth")
ax.set_ylabel("准确率")
ax.set_title("决策树深度 vs 过拟合")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
st.pyplot(fig)

# ── Section 4: 特征重要性 ──
if model_name in ("随机森林", "决策树"):
    st.subheader("4. 特征重要性")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_names = [selected_features[i] for i in indices]
    sorted_vals = importances[indices]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(range(len(sorted_names)), sorted_vals,
                   color="#10b981", alpha=0.7)
    ax.set_yticks(range(len(sorted_names)))
    ax.set_yticklabels([FEATURE_LABELS.get(n, n) for n in sorted_names])
    ax.invert_yaxis()
    ax.set_xlabel("重要性")
    ax.set_title(f"{model_name} 特征重要性排名")
    ax.grid(True, alpha=0.3, axis="x")
    for bar, val in zip(bars, sorted_vals):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{val:.4f}", va="center", fontsize=9)
    fig.tight_layout()
    st.pyplot(fig)

# ── Section 5: 四模型横评 ──
st.subheader("5. 四模型横评")
all_models = {
    "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=7),
    "决策树": DecisionTreeClassifier(max_depth=5, random_state=42),
    "随机森林": RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=42),
}
results = []
for name, mdl in all_models.items():
    mdl.fit(X_train, y_train)
    tr = accuracy_score(y_train, mdl.predict(X_train))
    te = accuracy_score(y_test, mdl.predict(X_test))
    results.append((name, tr, te))

fig, ax = plt.subplots(figsize=(8, 4))
names = [r[0] for r in results]
tr_vals = [r[1] for r in results]
te_vals = [r[2] for r in results]
x = np.arange(len(names))
w = 0.3
ax.bar(x - w / 2, tr_vals, w, label="训练", color="#3b82f6", alpha=0.7)
ax.bar(x + w / 2, te_vals, w, label="测试", color="#ef4444", alpha=0.7)
ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--", label="随机猜测")
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel("准确率")
ax.set_title("四模型横评")
ax.legend()
ax.grid(True, alpha=0.3, axis="y")
fig.tight_layout()
st.pyplot(fig)

st.info(
    "三种思路：逻辑回归学线性规律（fit 参数）、"
    "KNN 找邻居（不学习）、决策树学规则（if-else）。"
    "没有绝对赢家——看你的数据选模型。"
)
