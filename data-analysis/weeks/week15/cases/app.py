"""Week15 Streamlit 探索器：多模型信号融合 Capstone。

完全自包含——数据、特征工程、回测引擎、融合逻辑全部在本文件内。
交互调参：融合方式 / 模型组合 / train-test 比例。

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

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FEATURE_COLS = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]
TRADING_DAYS = 252

MODEL_OPTIONS = ["逻辑回归", "KNN", "随机森林"]


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
    df["daily_return"] = close.pct_change()
    df = df.dropna(
        subset=FEATURE_COLS + ["next_up", "daily_return"]
    ).reset_index(drop=True)
    return df


def backtest(df, signal, start_idx, name):
    test_df = df.iloc[start_idx:].copy()
    test_signal = signal.iloc[start_idx:].values
    strategy_returns = pd.Series(
        np.roll(test_signal, 1) * test_df["daily_return"].values,
        index=test_df.index,
    )
    strategy_returns.iloc[0] = 0
    equity = (1 + strategy_returns).cumprod()
    n_days = len(strategy_returns)
    cum_ret = equity.iloc[-1] - 1
    ann_ret = (1 + cum_ret) ** (TRADING_DAYS / n_days) - 1
    ann_vol = strategy_returns.std() * np.sqrt(TRADING_DAYS)
    sharpe = ann_ret / ann_vol if ann_vol > 0 else 0
    peak = equity.cummax()
    max_dd = ((equity - peak) / peak).min()
    held = test_signal[:-1] == 1
    win_rate = (
        ((test_df["daily_return"].values[1:] > 0) & held).sum() / held.sum()
        if held.sum() > 0 else 0
    )
    return {
        "name": name, "cumulative_return": cum_ret, "annual_return": ann_ret,
        "sharpe": sharpe, "max_drawdown": max_dd, "win_rate": win_rate,
        "equity": equity,
    }


st.set_page_config(page_title="多模型融合探索器", layout="wide")
st.title("多模型信号融合 Capstone 探索器")

df = load_and_engineer()

# ── 侧栏 ──
with st.sidebar:
    st.header("参数设置")
    selected_models = st.multiselect(
        "参与融合的模型", MODEL_OPTIONS, default=MODEL_OPTIONS
    )
    fusion_method = st.radio(
        "融合方式", ["投票法", "加权法", "不融合（只看单一模型）"]
    )
    split_ratio = st.slider("训练集比例", 0.5, 0.9, 0.8, 0.05)

if len(selected_models) == 0:
    st.warning("请至少选择一个模型。")
    st.stop()

# ── 准备数据 ──
split_idx = int(len(df) * split_ratio)
X_train = df.iloc[:split_idx][FEATURE_COLS].values
y_train = df.iloc[:split_idx]["next_up"].values
X_test = df.iloc[split_idx:][FEATURE_COLS].values
y_test = df.iloc[split_idx:]["next_up"].values

# ── 训练三个模型 ──
MODEL_BUILDERS = {
    "逻辑回归": lambda: LogisticRegression(max_iter=1000, random_state=42),
    "KNN": lambda: KNeighborsClassifier(n_neighbors=7),
    "随机森林": lambda: RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=42),
}

signals = {}
accuracies = {}
for name in selected_models:
    mdl = MODEL_BUILDERS[name]()
    mdl.fit(X_train, y_train)
    pred = mdl.predict(X_test)
    acc = accuracy_score(y_test, pred)
    sig = pd.Series(0, index=df.index)
    sig.iloc[split_idx:] = pred
    signals[name] = sig
    accuracies[name] = acc

# ── Section 1: 数据概览 ──
st.subheader("1. 数据概览")
c1, c2, c3 = st.columns(3)
c1.metric("样本数", f"{len(df)}")
c2.metric("训练/测试", f"{split_idx} / {len(df) - split_idx}")
c3.metric("参与融合模型数", f"{len(selected_models)}")

# ── Section 2: 模型准确率 ──
st.subheader("2. 各模型测试准确率")
cols = st.columns(len(selected_models))
for col, name in zip(cols, selected_models):
    col.metric(name, f"{accuracies[name]:.4f}",
               delta=f"{accuracies[name] - 0.5:+.4f} vs 随机")

# ── 生成融合信号 ──
bh_signal = pd.Series(1, index=df.index)
sma_signal = (df["ma_5"] > df["ma_20"]).astype(int)

strategies_to_compare = []

# 基线
strategies_to_compare.append(("买入持有", bh_signal))
strategies_to_compare.append(("SMA 交叉", sma_signal))

# 单一模型
for name in selected_models:
    strategies_to_compare.append((f"单一{name}", signals[name]))

# 融合
if fusion_method == "投票法" and len(selected_models) >= 2:
    vote_sum = sum(signals[n] for n in selected_models)
    fused = (vote_sum >= (len(selected_models) / 2)).astype(int)
    fused.iloc[:split_idx] = 0
    strategies_to_compare.append(("投票融合", fused))
elif fusion_method == "加权法" and len(selected_models) >= 2:
    weights = np.array([accuracies[n] for n in selected_models])
    threshold = 0.5 * weights.sum()
    weighted_sum = sum(accuracies[n] * signals[n] for n in selected_models)
    fused = (weighted_sum >= threshold).astype(int)
    fused.iloc[:split_idx] = 0
    strategies_to_compare.append(("加权融合", fused))

# ── Section 3: 净值曲线 ──
st.subheader("3. 策略净值曲线对比")
results = []
for name, sig in strategies_to_compare:
    r = backtest(df, sig, split_idx, name)
    results.append(r)

fig, ax = plt.subplots(figsize=(12, 5))
test_df = df.iloc[split_idx:]
dates = test_df["trade_date"]
colors_map = {
    "买入持有": "#9ca3af", "SMA 交叉": "#6b7280",
    "单一逻辑回归": "#60a5fa", "单一KNN": "#818cf8",
    "单一随机森林": "#3b82f6", "投票融合": "#10b981", "加权融合": "#ef4444",
}
for r in results:
    lw = 2.0 if "融合" in r["name"] else 1.2
    ax.plot(dates, r["equity"], label=r["name"],
            color=colors_map.get(r["name"]), linewidth=lw)
ax.axhline(1.0, color="gray", linewidth=0.5, linestyle="--")
ax.set_xlabel("日期")
ax.set_ylabel("净值（初始 = 1.0）")
ax.set_title("策略净值曲线对比（测试期）")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
fig.tight_layout()
st.pyplot(fig)

# ── Section 4: 指标对比 ──
st.subheader("4. 评估指标对比")
metrics = ["cumulative_return", "sharpe", "max_drawdown", "win_rate"]
labels = ["累计收益率", "夏普比率", "最大回撤", "胜率"]
fig, axes = plt.subplots(1, 4, figsize=(16, 3.5))
names = [r["name"] for r in results]
for ax, metric, label in zip(axes, metrics, labels):
    vals = [r[metric] for r in results]
    bars = ax.bar(range(len(names)), vals, alpha=0.75)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_title(label, fontsize=10)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=7)
    ax.grid(True, alpha=0.3, axis="y")
    for bar, val in zip(bars, vals):
        y = bar.get_height()
        fmt = f"{val:.2%}" if "return" in metric or "drawdown" in metric or "win" in metric else f"{val:.3f}"
        ax.text(bar.get_x() + bar.get_width() / 2,
                y + (0.01 if y >= 0 else -0.03),
                fmt, ha="center",
                va="bottom" if y >= 0 else "top", fontsize=7)
fig.suptitle("策略评估指标对比", fontsize=12, y=1.02)
fig.tight_layout()
st.pyplot(fig)

# ── Section 5: 融合 vs 单一聚焦 ──
if any("融合" in r["name"] for r in results):
    st.subheader("5. 融合 vs 单一模型")
    single = [r for r in results if "单一" in r["name"]]
    fusion = [r for r in results if "融合" in r["name"]]
    baselines = [r for r in results if r["name"] in ("买入持有", "SMA 交叉")]

    compare = baselines + single + fusion
    c_names = [r["name"] for r in compare]
    c_sharpes = [r["sharpe"] for r in compare]
    c_dds = [abs(r["max_drawdown"]) for r in compare]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(c_names, c_sharpes, alpha=0.75)
    axes[0].axhline(0, color="gray", linewidth=0.5)
    axes[0].set_title("夏普比率对比")
    axes[0].set_ylabel("夏普比率")
    axes[0].grid(True, alpha=0.3, axis="y")
    axes[0].tick_params(axis="x", rotation=45, labelsize=8)

    axes[1].bar(c_names, c_dds, color="#ef4444", alpha=0.75)
    axes[1].set_title("最大回撤对比（越小越好）")
    axes[1].set_ylabel("最大回撤")
    axes[1].grid(True, alpha=0.3, axis="y")
    axes[1].tick_params(axis="x", rotation=45, labelsize=8)

    fig.suptitle("融合 vs 单一模型", fontsize=12, y=1.02)
    fig.tight_layout()
    st.pyplot(fig)

    st.info(
        "融合不是为了用更多模型，是为了降低单一模型的盲区。"
        "如果三个模型都基于同一份特征，它们可能犯了同样的错——"
        "真正有效的融合需要多源信息（如价格 + 文本 + 宏观）。"
    )
