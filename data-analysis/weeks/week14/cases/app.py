"""Week14 Streamlit 探索器：ML 交易信号 + 策略回测。

完全自包含——数据、特征工程、回测引擎全部在本文件内。
交互调参：策略选择 / train-test 比例 / RF max_depth。

运行：streamlit run app.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FEATURE_COLS = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]
TRADING_DAYS = 252


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


st.set_page_config(page_title="ML 回测探索器", layout="wide")
st.title("ML 交易信号 + 策略回测探索器")

df = load_and_engineer()

# ── 侧栏 ──
with st.sidebar:
    st.header("参数设置")
    strategies = st.multiselect(
        "选择策略对比", ["买入持有", "SMA 交叉", "单一 RF"],
        default=["买入持有", "SMA 交叉", "单一 RF"],
    )
    split_ratio = st.slider("训练集比例", 0.5, 0.9, 0.8, 0.05)
    rf_depth = st.slider("RF max_depth", 1, 15, 5)

# ── 准备数据 ──
split_idx = int(len(df) * split_ratio)
X_train = df.iloc[:split_idx][FEATURE_COLS].values
y_train = df.iloc[:split_idx]["next_up"].values
X_test = df.iloc[split_idx:][FEATURE_COLS].values
y_test = df.iloc[split_idx:]["next_up"].values

# ── RF 信号 ──
rf = RandomForestClassifier(
    n_estimators=100, max_depth=rf_depth, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

rf_signal = pd.Series(0, index=df.index)
rf_signal.iloc[split_idx:] = rf_pred

sma_signal = (df["ma_5"] > df["ma_20"]).astype(int)
bh_signal = pd.Series(1, index=df.index)

# ── Section 1: 数据概览 ──
st.subheader("1. 数据概览")
c1, c2, c3 = st.columns(3)
c1.metric("样本数", f"{len(df)}")
c2.metric("训练期", f"{df['trade_date'].iloc[0].date()} ~ "
         f"{df['trade_date'].iloc[split_idx-1].date()}")
c3.metric("测试期", f"{df['trade_date'].iloc[split_idx].date()} ~ "
         f"{df['trade_date'].iloc[-1].date()}")

# ── Section 2: 信号生成 ──
st.subheader("2. ML 信号生成")
c1, c2 = st.columns(2)
c1.metric("RF 预测准确率", f"{rf_acc:.4f}")
c2.metric("RF 持仓天数占比", f"{rf_signal.iloc[split_idx:].mean():.2%}")

# ── Section 3: 净值曲线 ──
st.subheader("3. 净值曲线对比")

SIGNAL_MAP = {
    "买入持有": bh_signal,
    "SMA 交叉": sma_signal,
    "单一 RF": rf_signal,
}

results = []
for name in strategies:
    sig = SIGNAL_MAP[name]
    r = backtest(df, sig, split_idx, name)
    results.append(r)

fig, ax = plt.subplots(figsize=(11, 5))
test_df = df.iloc[split_idx:]
dates = test_df["trade_date"]
colors = {"买入持有": "#6b7280", "SMA 交叉": "#3b82f6", "单一 RF": "#ef4444"}
for r in results:
    ax.plot(dates, r["equity"], label=r["name"],
            color=colors.get(r["name"]), linewidth=1.5)
ax.axhline(1.0, color="gray", linewidth=0.5, linestyle="--")
ax.set_xlabel("日期")
ax.set_ylabel("净值（初始 = 1.0）")
ax.set_title("策略净值曲线对比（测试期）")
ax.legend()
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
fig.tight_layout()
st.pyplot(fig)

# ── Section 4: 指标卡片 ──
st.subheader("4. 评估指标")
if results:
    cols = st.columns(len(results))
    for col, r in zip(cols, results):
        with col:
            st.write(f"**{r['name']}**")
            st.metric("累计收益", f"{r['cumulative_return']:.2%}")
            st.metric("年化收益", f"{r['annual_return']:.2%}")
            st.metric("夏普比率", f"{r['sharpe']:.3f}")
            st.metric("最大回撤", f"{r['max_drawdown']:.2%}")
            st.metric("胜率", f"{r['win_rate']:.2%}")

# ── Section 5: 指标柱状图 ──
st.subheader("5. 指标对比")
metrics = ["cumulative_return", "sharpe", "max_drawdown", "win_rate"]
labels = ["累计收益率", "夏普比率", "最大回撤", "胜率"]
fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
names = [r["name"] for r in results]
for ax, metric, label in zip(axes, metrics, labels):
    vals = [r[metric] for r in results]
    bars = ax.bar(names, vals, color=["#6b7280", "#3b82f6", "#ef4444"][:len(names)],
                  alpha=0.7)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_title(label, fontsize=10)
    ax.grid(True, alpha=0.3, axis="y")
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    for bar, val in zip(bars, vals):
        y = bar.get_height()
        fmt = f"{val:.2%}" if "return" in metric or "drawdown" in metric or "win" in metric else f"{val:.3f}"
        ax.text(bar.get_x() + bar.get_width() / 2,
                y + (0.01 if y >= 0 else -0.03),
                fmt, ha="center",
                va="bottom" if y >= 0 else "top", fontsize=8)
fig.suptitle("策略评估指标对比", fontsize=12, y=1.02)
fig.tight_layout()
st.pyplot(fig)

st.info(
    "训练/测试分离的意义：模型在训练期拟合，信号在测试期生成，回测在测试期进行。"
    "在训练期回测 = 数据泄漏 = 自欺欺人。"
)
