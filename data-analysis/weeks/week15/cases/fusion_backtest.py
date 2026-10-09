"""多模型信号融合 Capstone：三模型投票 + 加权融合 + 五策略回测横评。

流程：
  1. 读入本目录 sse_daily.csv，构造特征
  2. 三个模型各自预测涨跌 → 生成信号：
     - 逻辑回归（W11 线性思路，分类版）
     - KNN (k=7)（W12）
     - 随机森林（W13）
  3. 两种融合方式：
     - 投票法：三模型多数表决
     - 加权法：按各自测试准确率分配权重
  4. 回测引擎（复用 W14 的 backtest 逻辑）
  5. 五策略横评：买入持有 / SMA / 单一RF / 投票融合 / 加权融合

对应 plan.md 第1节"多模型信号融合实践"。
这是 W11→W14 故事线的 capstone 整合案例。
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

# 本目录（数据与脚本同级，完全自包含）
DATA_DIR = Path(__file__).resolve().parent
OUT_DIR = Path(__file__).resolve().parent / "output"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FEATURE_COLS = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]

TRADING_DAYS_PER_YEAR = 252


# ════════════════════════════════════════════════════════
# 1. 数据加载与特征构造
# ════════════════════════════════════════════════════════

def load_and_engineer() -> pd.DataFrame:
    """读本目录 sse_daily.csv。"""
    csv_path = DATA_DIR / "sse_daily.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"未找到 {csv_path}\n"
            "请先运行本目录下的 fetch_data.py：\n"
            "  python fetch_data.py"
        )

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


# ════════════════════════════════════════════════════════
# 2. 三模型信号生成
# ════════════════════════════════════════════════════════

def generate_signals(df: pd.DataFrame, split_ratio=0.8):
    """三个模型各自训练 + 在测试集上生成信号。

    返回：
      signals: dict，每个模型的信号 pd.Series（测试期内 0/1）
      accuracies: dict，每个模型的测试准确率
      split_idx: 训练/测试分割点
    """
    split_idx = int(len(df) * split_ratio)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]

    X_train = train[FEATURE_COLS].values
    y_train = train["next_up"].values
    X_test = test[FEATURE_COLS].values
    y_test = test["next_up"].values

    models = {
        "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "随机森林": RandomForestClassifier(
            n_estimators=100, max_depth=5, random_state=42),
    }

    signals = {}
    accuracies = {}

    print(f"  训练期：{train['trade_date'].iloc[0].date()} ~ "
          f"{train['trade_date'].iloc[-1].date()}（{len(train)} 天）")
    print(f"  测试期：{test['trade_date'].iloc[0].date()} ~ "
          f"{test['trade_date'].iloc[-1].date()}（{len(test)} 天）")

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        # 信号：只在测试期有值，训练期填 0
        sig = pd.Series(0, index=df.index)
        sig.iloc[split_idx:] = y_pred

        signals[name] = sig
        accuracies[name] = acc

        print(f"  {name:<8s}  准确率={acc:.4f}  "
              f"持仓占比={sig.iloc[split_idx:].mean():.2%}")

    return signals, accuracies, split_idx


# ════════════════════════════════════════════════════════
# 3. 信号融合
# ════════════════════════════════════════════════════════

def fuse_vote(signals: dict, split_idx: int) -> pd.Series:
    """投票法：三模型多数表决（≥2 票 → 持仓）。

    简单、无参数，但忽略模型间强弱差异。
    """
    # 测试期三个信号相加
    vote_sum = (
        signals["逻辑回归"]
        + signals["KNN"]
        + signals["随机森林"]
    )
    # ≥2 票 → 持仓
    fused = (vote_sum >= 2).astype(int)
    # 训练期保持 0
    fused.iloc[:split_idx] = 0

    print(f"  投票融合  持仓占比={fused.iloc[split_idx:].mean():.2%}")
    return fused


def fuse_weighted(signals: dict, accuracies: dict, split_idx: int) -> pd.Series:
    """加权法：按各自测试准确率分配权重。

    更准的模型话语权更大。比投票法多一步——先算准确率再定权重。
    """
    names = ["逻辑回归", "KNN", "随机森林"]
    weights = np.array([accuracies[n] for n in names])
    threshold = 0.5 * weights.sum()

    # 加权投票
    weighted_sum = sum(
        accuracies[name] * signals[name] for name in names
    )
    fused = (weighted_sum >= threshold).astype(int)
    fused.iloc[:split_idx] = 0

    print(f"  加权融合  持仓占比={fused.iloc[split_idx:].mean():.2%}")
    print(f"  权重：", end="")
    for name in names:
        print(f"  {name}={accuracies[name]:.4f}", end="")
    print()
    return fused


# ════════════════════════════════════════════════════════
# 4. 回测引擎（复用 W14 逻辑）
# ════════════════════════════════════════════════════════

def backtest(df: pd.DataFrame, signal: pd.Series, start_idx: int = 0,
             name: str = "") -> dict:
    """回测引擎：按信号持仓，计算净值曲线与评估指标。

    策略收益 = 昨日信号 × 今日收益率
    （信号在 t-1 日收盘时产生，t 日持有，收益在 t 日实现）
    """
    test_df = df.iloc[start_idx:].copy()
    test_signal = signal.iloc[start_idx:].values

    strategy_returns = pd.Series(
        np.roll(test_signal, 1) * test_df["daily_return"].values,
        index=test_df.index,
    )
    strategy_returns.iloc[0] = 0

    equity = (1 + strategy_returns).cumprod()

    n_days = len(strategy_returns)
    cumulative_return = equity.iloc[-1] - 1
    annual_return = (1 + cumulative_return) ** (TRADING_DAYS_PER_YEAR / n_days) - 1

    annual_vol = strategy_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    sharpe = annual_return / annual_vol if annual_vol > 0 else 0

    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_drawdown = drawdown.min()

    held = test_signal[:-1] == 1
    if held.sum() > 0:
        wins = (test_df["daily_return"].values[1:] > 0) & held
        win_rate = wins.sum() / held.sum()
    else:
        win_rate = 0

    result = {
        "name": name,
        "cumulative_return": cumulative_return,
        "annual_return": annual_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "equity": equity,
        "returns": strategy_returns,
    }

    print(f"  {name:<10s}  累计={cumulative_return:>8.2%}  "
          f"年化={annual_return:>8.2%}  "
          f"夏普={sharpe:>6.3f}  "
          f"回撤={max_drawdown:>8.2%}  "
          f"胜率={win_rate:>6.2%}")

    return result


# ════════════════════════════════════════════════════════
# 5. 可视化
# ════════════════════════════════════════════════════════

def plot_equity_curve(df: pd.DataFrame, results: list, split_idx: int) -> None:
    """五策略净值曲线对比。"""
    fig, ax = plt.subplots(figsize=(12, 6))

    test_df = df.iloc[split_idx:]
    dates = test_df["trade_date"]

    colors = {
        "买入持有": "#9ca3af",
        "SMA 交叉": "#6b7280",
        "单一 RF": "#3b82f6",
        "投票融合": "#10b981",
        "加权融合": "#ef4444",
    }
    linestyles = {
        "买入持有": "--",
        "SMA 交叉": ":",
        "单一 RF": "-",
        "投票融合": "-",
        "加权融合": "-",
    }

    for r in results:
        ax.plot(
            dates, r["equity"],
            label=r["name"],
            color=colors.get(r["name"], None),
            linestyle=linestyles.get(r["name"], "-"),
            linewidth=1.8 if "融合" in r["name"] else 1.2,
        )

    ax.axhline(1.0, color="gray", linewidth=0.5, linestyle="--")
    ax.set_xlabel("日期")
    ax.set_ylabel("净值（初始 = 1.0）")
    ax.set_title("五策略净值曲线对比（测试期）")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "equity_curve_5strategies.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'equity_curve_5strategies.png'}")


def plot_metrics(results: list) -> None:
    """五策略评估指标柱状图对比。"""
    metrics = ["cumulative_return", "annual_return", "sharpe",
               "max_drawdown", "win_rate"]
    labels = ["累计收益率", "年化收益率", "夏普比率", "最大回撤", "信号胜率"]

    fig, axes = plt.subplots(1, 5, figsize=(18, 4.5))
    names = [r["name"] for r in results]
    colors = ["#9ca3af", "#6b7280", "#3b82f6", "#10b981", "#ef4444"]

    for ax, metric, label in zip(axes, metrics, labels):
        vals = [r[metric] for r in results]
        bars = ax.bar(names, vals, color=colors[:len(names)], alpha=0.75)
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.set_title(label, fontsize=11)
        ax.grid(True, alpha=0.3, axis="y")
        for bar, val in zip(bars, vals):
            y = bar.get_height()
            offset = 0.01 if y >= 0 else -0.03
            va = "bottom" if y >= 0 else "top"
            fmt = (
                f"{val:.2%}"
                if "return" in metric or "drawdown" in metric
                or "win" in metric
                else f"{val:.3f}"
            )
            ax.text(
                bar.get_x() + bar.get_width() / 2, y + offset,
                fmt, ha="center", va=va, fontsize=8,
            )
        ax.tick_params(axis="x", rotation=30, labelsize=8)

    fig.suptitle("五策略评估指标对比", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "metrics_5strategies.png", dpi=150,
                bbox_inches="tight")
    plt.close(fig)
    print(f"  → {OUT_DIR / 'metrics_5strategies.png'}")


def plot_fusion_vs_single(results: list) -> None:
    """融合 vs 单一模型：聚焦对比图。"""
    # 找融合和单一策略
    single_names = ["买入持有", "SMA 交叉", "单一 RF"]
    fusion_names = ["投票融合", "加权融合"]

    single = [r for r in results if r["name"] in single_names]
    fusion = [r for r in results if r["name"] in fusion_names]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：夏普比率对比
    ax = axes[0]
    all_names = [r["name"] for r in single] + [r["name"] for r in fusion]
    all_sharpes = [r["sharpe"] for r in single] + [r["sharpe"] for r in fusion]
    colors = ["#9ca3af", "#6b7280", "#3b82f6", "#10b981", "#ef4444"]
    bars = ax.bar(all_names, all_sharpes, color=colors, alpha=0.75)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_title("夏普比率：融合 vs 单一", fontsize=11)
    ax.set_ylabel("夏普比率")
    ax.grid(True, alpha=0.3, axis="y")
    for bar, val in zip(bars, all_sharpes):
        y = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y + (0.02 if y >= 0 else -0.04),
            f"{val:.3f}", ha="center",
            va="bottom" if y >= 0 else "top", fontsize=9,
        )
    ax.tick_params(axis="x", rotation=30, labelsize=9)

    # 右图：最大回撤对比（越小越好，所以用绝对值）
    ax = axes[1]
    all_dd = [abs(r["max_drawdown"]) for r in single] + [
        abs(r["max_drawdown"]) for r in fusion
    ]
    bars = ax.bar(all_names, all_dd, color=colors, alpha=0.75)
    ax.set_title("最大回撤：融合 vs 单一（越小越好）", fontsize=11)
    ax.set_ylabel("最大回撤（绝对值）")
    ax.grid(True, alpha=0.3, axis="y")
    for bar, val in zip(bars, all_dd):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.005,
            f"{val:.2%}", ha="center", va="bottom", fontsize=9,
        )
    ax.tick_params(axis="x", rotation=30, labelsize=9)

    fig.suptitle("融合 vs 单一模型：风险调整后收益与回撤", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fusion_vs_single.png", dpi=150,
                bbox_inches="tight")
    plt.close(fig)
    print(f"  → {OUT_DIR / 'fusion_vs_single.png'}")


# ════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════

def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("Capstone 案例：多模型信号融合 + 五策略回测横评")
    print("W11→W14 集大成：线性回归/KNN/随机森林 → 融合 → 回测")
    print("=" * 60)

    # 1. 数据加载
    print("\n[1/6] 数据加载与特征构造")
    df = load_and_engineer()
    print(f"  样本数：{len(df)}")
    print(f"  日期范围：{df['trade_date'].iloc[0].date()} ~ "
          f"{df['trade_date'].iloc[-1].date()}")

    # 2. 三模型信号生成
    print("\n[2/6] 三模型信号生成（各自训练 + 测试集预测）")
    signals, accuracies, split_idx = generate_signals(df)

    # 3. 信号融合
    print("\n[3/6] 信号融合")
    print("\n  投票法（等权多数表决）：")
    vote_signal = fuse_vote(signals, split_idx)

    print("\n  加权法（按准确率分配权重）：")
    weighted_signal = fuse_weighted(signals, accuracies, split_idx)

    # 4. 回测（五策略）
    print("\n[4/6] 回测（测试期，五策略）")
    print()

    # 买入持有基准
    bh_result = backtest(
        df, pd.Series(1, index=df.index),
        start_idx=split_idx, name="买入持有",
    )

    # SMA 交叉基线
    sma_sig = (df["ma_5"] > df["ma_20"]).astype(int)
    sma_result = backtest(df, sma_sig, start_idx=split_idx, name="SMA 交叉")

    # 单一 RF（W14 的策略）
    rf_result = backtest(
        df, signals["随机森林"], start_idx=split_idx, name="单一 RF",
    )

    # 投票融合
    vote_result = backtest(
        df, vote_signal, start_idx=split_idx, name="投票融合",
    )

    # 加权融合
    weighted_result = backtest(
        df, weighted_signal, start_idx=split_idx, name="加权融合",
    )

    # 5. 可视化
    print("\n[5/6] 可视化")
    results = [bh_result, sma_result, rf_result, vote_result, weighted_result]
    plot_equity_curve(df, results, split_idx)
    plot_metrics(results)
    plot_fusion_vs_single(results)

    # 6. 总结
    print("\n[6/6] 总结")
    print("\n  " + "=" * 72)
    print(f"  {'策略':<10s} {'累计收益':>10s} {'年化':>10s} "
          f"{'夏普':>8s} {'最大回撤':>10s} {'胜率':>8s}")
    print("  " + "-" * 72)
    for r in results:
        print(f"  {r['name']:<10s} "
              f"{r['cumulative_return']:>10.2%} "
              f"{r['annual_return']:>10.2%} "
              f"{r['sharpe']:>8.3f} "
              f"{r['max_drawdown']:>10.2%} "
              f"{r['win_rate']:>8.2%}")
    print("  " + "=" * 72)

    print(f"\n  融合 vs 单一模型：")
    print(f"  1. 融合的夏普比率比单一 RF 高吗？高多少？")
    print(f"  2. 融合的最大回撤比单一 RF 小吗？小多少？")
    print(f"  3. 投票法 vs 加权法——哪个更好？为什么？")
    print(f"  4. 融合打不过买入持有吗？如果是，可能原因：")
    print(f"     - 三个模型基于同一份特征，犯了同样的错")
    print(f"     - 金融数据噪声大，模型预测能力本身就弱")
    print(f"     - 需要多源信息（如价格 + 文本 + 宏观）才能真正互补")

    print(f"\n  capstone 闭环回顾：")
    print(f"  W11 线性回归（train/test split）")
    print(f"  → W12 KNN + 特征工程")
    print(f"  → W13 决策树/随机森林 + 特征重要性")
    print(f"  → W14 ML 信号 + 回测引擎")
    print(f"  → W15 多模型融合（本案例）")
    print(f"  完整路径：数据→特征→建模→信号→融合→回测→评估")

    print(f"\n  路演提示：")
    print(f"  - 五策略净值曲线图可直接放到路演 PPT")
    print(f"  - '融合比单一模型夏普高 X%' 是一句话价值主张")
    print(f"  - 如果融合效果不好，诚实说——这也是发现")

    print("\n" + "=" * 60)
    print("完成。图表已保存至 output/ 目录。")
    print("=" * 60)


if __name__ == "__main__":
    main()
