"""Week11 Streamlit 探索器：线性回归预测次日收益率。

完全自包含——数据、特征工程、模型训练全部在本文件内。
交互调参：特征选择 / train-test 比例 / 学习率 / SGD 迭代次数。

运行：streamlit run app.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

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
    df = df.dropna(
        subset=ALL_FEATURES + ["next_return"]
    ).reset_index(drop=True)
    return df


st.set_page_config(page_title="线性回归探索器", layout="wide")
st.title("线性回归探索器：上证指数次日收益率预测")

df = load_and_engineer()

# ── 侧栏 ──
with st.sidebar:
    st.header("参数设置")
    selected_features = st.multiselect(
        "选择特征", ALL_FEATURES, default=ALL_FEATURES,
        format_func=lambda x: FEATURE_LABELS.get(x, x),
    )
    split_ratio = st.slider("训练集比例", 0.5, 0.9, 0.8, 0.05)
    eta = st.slider("SGD 学习率", 0.0001, 0.01, 0.001, 0.0001, format="%.4f")
    n_iter = st.slider("SGD 迭代次数", 10000, 200000, 100000, 10000)

if len(selected_features) == 0:
    st.warning("请至少选择一个特征。")
    st.stop()

# ── Section 1: 数据概览 ──
st.subheader("1. 数据概览")
c1, c2, c3 = st.columns(3)
c1.metric("样本数", f"{len(df)}")
c2.metric("起始日期", df["trade_date"].iloc[0].strftime("%Y-%m-%d"))
c3.metric("结束日期", df["trade_date"].iloc[-1].strftime("%Y-%m-%d"))
st.dataframe(df[["trade_date", "close"] + selected_features].head(10),
             use_container_width=True)

# ── Section 2: 散点图直觉 ──
st.subheader("2. 当日收益率 vs 次日收益率")
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(df["return_1d"], df["next_return"], alpha=0.15, s=10)
ax.axhline(0, color="gray", linewidth=0.8)
ax.axvline(0, color="gray", linewidth=0.8)
ax.set_xlabel("当日收益率")
ax.set_ylabel("次日收益率")
corr = df["return_1d"].corr(df["next_return"])
ax.set_title(f"相关系数 = {corr:.4f}")
ax.grid(True, alpha=0.3)
fig.tight_layout()
st.pyplot(fig)

# ── 准备数据 ──
split_idx = int(len(df) * split_ratio)
X_train = df.iloc[:split_idx][selected_features].values
y_train = df.iloc[:split_idx]["next_return"].values
X_test = df.iloc[split_idx:][selected_features].values
y_test = df.iloc[split_idx:]["next_return"].values

# ── Section 3: sklearn 回归 ──
st.subheader("3. sklearn 线性回归")
model = LinearRegression()
model.fit(X_train, y_train)
train_r2 = r2_score(y_train, model.predict(X_train))
test_r2 = r2_score(y_test, model.predict(X_test))

c1, c2 = st.columns(2)
c1.metric("训练集 R2", f"{train_r2:.4f}")
c2.metric("测试集 R2", f"{test_r2:.4f}")

coef_df = pd.DataFrame({
    "特征": selected_features,
    "系数": model.coef_,
}).style.format({"系数": "{:.6f}"})
st.write("系数：")
st.dataframe(coef_df, use_container_width=True)

y_pred = model.predict(X_test)
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(y_test, y_pred, alpha=0.2, s=10)
lim = max(abs(y_test).max(), abs(y_pred).max())
ax.plot([-lim, lim], [-lim, lim], "r--", linewidth=1, label="y=x")
ax.set_xlabel("真实次日收益率")
ax.set_ylabel("预测次日收益率")
ax.set_title(f"预测 vs 真实（测试集 R2={test_r2:.4f}）")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
st.pyplot(fig)

# ── Section 4: 手写 SGD ──
st.subheader("4. 手写 SGD（梯度下降）")
with st.spinner("SGD 训练中…"):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0) + 1e-8
    Xn_train = (X_train - mean) / std
    Xn_test = (X_test - mean) / std
    w = np.zeros(len(selected_features))
    b = 0.0
    losses = []
    for i in range(n_iter):
        pred = Xn_train @ w + b
        error = pred - y_train
        grad_w = 2 * (Xn_train.T @ error) / len(y_train)
        grad_b = 2 * error.mean()
        w = w - eta * grad_w
        b = b - eta * grad_b
        if i % max(1, n_iter // 20) == 0:
            losses.append((i, (error ** 2).mean()))

    sgd_pred = Xn_test @ w + b
    sgd_r2 = r2_score(y_test, sgd_pred)

c1, c2 = st.columns(2)
c1.metric("SGD 测试集 R2", f"{sgd_r2:.4f}")
c2.metric("sklearn 测试集 R2", f"{test_r2:.4f}")

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot([l[0] for l in losses], [l[1] for l in losses], marker="o")
ax.set_xlabel("迭代次数")
ax.set_ylabel("MSE 损失")
ax.set_title("SGD 损失下降曲线")
ax.set_yscale("log")
ax.grid(True, alpha=0.3)
fig.tight_layout()
st.pyplot(fig)

# ── Section 5: 过拟合自检 ──
st.subheader("5. 过拟合自检")
X_all = df[selected_features].values
y_all = df["next_return"].values
m_full = LinearRegression().fit(X_all, y_all)
full_r2 = r2_score(y_all, m_full.predict(X_all))

X_tr2, X_te2, y_tr2, y_te2 = train_test_split(
    X_all, y_all, test_size=0.2, random_state=42)
m_rand = LinearRegression().fit(X_tr2, y_tr2)
rand_train_r2 = r2_score(y_tr2, m_rand.predict(X_tr2))
rand_test_r2 = r2_score(y_te2, m_rand.predict(X_te2))

time_train_r2 = train_r2
time_test_r2 = test_r2

fig, ax = plt.subplots(figsize=(8, 4))
cats = ["全量fit", "随机split\n训练", "随机split\n测试", "时间split\n训练", "时间split\n测试"]
vals = [full_r2, rand_train_r2, rand_test_r2, time_train_r2, time_test_r2]
colors = ["#3b82f6", "#3b82f6", "#ef4444", "#3b82f6", "#ef4444"]
bars = ax.bar(cats, vals, color=colors, alpha=0.7)
ax.axhline(0, color="gray", linewidth=0.8)
ax.set_ylabel("R2")
ax.set_title("不同 split 方式的 R2 对比")
ax.grid(True, alpha=0.3, axis="y")
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
            f"{val:.4f}", ha="center", va="bottom", fontsize=9)
fig.tight_layout()
st.pyplot(fig)

st.info(
    "时间 split 的测试 R2 通常比随机 split 更低——"
    "因为随机打乱混入了未来信息，是数据泄漏。"
)
