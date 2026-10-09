"""ML 交易信号 + 策略回测：从预测到赚钱。

流程：
  1. 读入本目录 sse_daily.csv，构造特征
  2. SMA 基线策略（ma_5 上穿 ma_20 → 买入）
  3. ML 信号策略（随机森林预测涨跌 → 生成买卖信号）
  4. 回测引擎（收益曲线、夏普比率、最大回撤、胜率）
  5. 三策略对比：买入持有 vs SMA vs ML

对应课堂 notebook：
  - Trading strategy evaluation - sma.ipynb（SMA 回测）
  - evaluate trading strategy.ipynb（策略评估）
  - machine learning for stock prediction.ipynb §strategy

本目录自带 sse_daily.csv（上证指数日线），特征构造与 W11/W13 案例一致。
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 本目录（数据与脚本同级，完全自包含）
DATA_DIR = Path(__file__).resolve().parent
OUT_DIR = Path(__file__).resolve().parent / "output"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FEATURE_COLS = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]

# 回测参数
INITIAL_CAPITAL = 1.0  # 初始净值（1.0 = 100%）
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

    # 标签：次日上涨=1
    df["next_return"] = close.shift(-1) / close - 1
    df["next_up"] = (df["next_return"] > 0).astype(int)

    # 每日收益率（用于回测）
    df["daily_return"] = close.pct_change()

    df = df.dropna(
        subset=FEATURE_COLS + ["next_up", "daily_return"]
    ).reset_index(drop=True)
    return df


# ════════════════════════════════════════════════════════
# 2. SMA 基线策略
# ════════════════════════════════════════════════════════

def sma_signal(df: pd.DataFrame) -> pd.Series:
    """SMA 交叉信号：ma_5 > ma_20 → 持仓(1)，否则空仓(0)。"""
    signal = (df["ma_5"] > df["ma_20"]).astype(int)
    return signal


# ════════════════════════════════════════════════════════
# 3. ML 信号策略
# ════════════════════════════════════════════════════════

def ml_signal(df: pd.DataFrame, split_ratio=0.8) -> pd.Series:
    """用随机森林预测涨跌生成交易信号。

    训练/测试分离：前 80% 训练，后 20% 测试。
    只在测试集上生成信号并回测——在训练集上回测=数据泄漏。
    """
    split_idx = int(len(df) * split_ratio)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]

    X_train = train[FEATURE_COLS].values
    y_train = train["next_up"].values
    X_test = test[FEATURE_COLS].values

    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)

    # 只在测试集上预测
    y_pred = rf.predict(X_test)

    # 信号 = 预测涨→持仓(1)，预测跌→空仓(0)
    signal = pd.Series(0, index=df.index)
    signal.iloc[split_idx:] = y_pred

    # 报告
    y_test = test["next_up"].values
    acc = accuracy_score(y_test, y_pred)
    print(f"  随机森林预测准确率（测试集）：{acc:.4f}")
    print(f"  训练期：{train['trade_date'].iloc[0].date()} ~ "
          f"{train['trade_date'].iloc[-1].date()}（{len(train)} 天）")
    print(f"  测试期：{test['trade_date'].iloc[0].date()} ~ "
          f"{test['trade_date'].iloc[-1].date()}（{len(test)} 天）")
    print(f"  信号持仓天数占比：{signal.iloc[split_idx:].mean():.2%}")

    return signal, split_idx


# ════════════════════════════════════════════════════════
# 4. 回测引擎
# ════════════════════════════════════════════════════════

def backtest(df: pd.DataFrame, signal: pd.Series, start_idx: int = 0,
             name: str = "") -> dict:
    """回测引擎：按信号持仓，计算净值曲线与评估指标。

    策略收益 = 昨日信号 × 今日收益率
    （信号在 t-1 日收盘时产生，t 日持有，收益在 t 日实现）
    """
    test_df = df.iloc[start_idx:].copy()
    test_signal = signal.iloc[start_idx:].values

    # 策略日收益 = 上一日信号 × 当日收益
    strategy_returns = pd.Series(
        np.roll(test_signal, 1) * test_df["daily_return"].values,
        index=test_df.index,
    )
    # 第一天无法用前一日信号，设为 0
    strategy_returns.iloc[0] = 0

    # 净值曲线
    equity = (1 + strategy_returns).cumprod()

    # 评估指标
    n_days = len(strategy_returns)
    cumulative_return = equity.iloc[-1] - 1
    annual_return = (1 + cumulative_return) ** (TRADING_DAYS_PER_YEAR / n_days) - 1

    annual_vol = strategy_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    sharpe = annual_return / annual_vol if annual_vol > 0 else 0

    # 最大回撤
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_drawdown = drawdown.min()

    # 胜率（信号正确且持仓的天数 / 持仓天数）
    held = test_signal[:-1] == 1  # 昨日信号为持仓
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

    print(f"\n  {name}")
    print(f"  {'累计收益率':<12s} {cumulative_return:>10.2%}")
    print(f"  {'年化收益率':<12s} {annual_return:>10.2%}")
    print(f"  {'夏普比率':<12s} {sharpe:>10.4f}")
    print(f"  {'最大回撤':<12s} {max_drawdown:>10.2%}")
    print(f"  {'信号胜率':<12s} {win_rate:>10.2%}")

    return result


# ════════════════════════════════════════════════════════
# 5. 可视化
# ════════════════════════════════════════════════════════

def plot_equity_curve(df: pd.DataFrame, results: list, split_idx: int) -> None:
    """三策略净值曲线对比。"""
    fig, ax = plt.subplots(figsize=(11, 6))

    test_df = df.iloc[split_idx:]
    dates = test_df["trade_date"]

    colors = {"买入持有": "#6b7280", "SMA 交叉": "#3b82f6", "ML 信号": "#ef4444"}

    for r in results:
        ax.plot(dates, r["equity"], label=r["name"],
                color=colors.get(r["name"], None), linewidth=1.5)

    ax.axhline(1.0, color="gray", linewidth=0.5, linestyle="--")
    ax.set_xlabel("日期")
    ax.set_ylabel("净值（初始 = 1.0）")
    ax.set_title("策略净值曲线对比（测试期）")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "equity_curve_comparison.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'equity_curve_comparison.png'}")


def plot_metrics(results: list) -> None:
    """评估指标柱状图对比。"""
    metrics = ["cumulative_return", "annual_return", "sharpe",
               "max_drawdown", "win_rate"]
    labels = ["累计收益率", "年化收益率", "夏普比率", "最大回撤", "信号胜率"]

    fig, axes = plt.subplots(1, 5, figsize=(16, 4))
    names = [r["name"] for r in results]

    for ax, metric, label in zip(axes, metrics, labels):
        vals = [r[metric] for r in results]
        colors = ["#6b7280", "#3b82f6", "#ef4444"]
        bars = ax.bar(names, vals, color=colors[:len(names)], alpha=0.7)
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.set_title(label, fontsize=11)
        ax.grid(True, alpha=0.3, axis="y")
        for bar, val in zip(bars, vals):
            y = bar.get_height()
            offset = 0.01 if y >= 0 else -0.03
            va = "bottom" if y >= 0 else "top"
            fmt = f"{val:.2%}" if "return" in metric or "drawdown" in metric \
                or "win" in metric else f"{val:.3f}"
            ax.text(bar.get_x() + bar.get_width() / 2, y + offset,
                    fmt, ha="center", va=va, fontsize=9)
        ax.tick_params(axis="x", rotation=30, labelsize=9)

    fig.suptitle("三策略评估指标对比", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "metrics_comparison.png", dpi=150,
                bbox_inches="tight")
    plt.close(fig)
    print(f"  → {OUT_DIR / 'metrics_comparison.png'}")


# ════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════

def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("案例：ML 交易信号 + 策略回测")
    print("=" * 60)

    # 1. 数据加载
    print("\n[1/5] 数据加载与特征构造")
    df = load_and_engineer()
    print(f"  样本数：{len(df)}")
    print(f"  日期范围：{df['trade_date'].iloc[0].date()} ~ "
          f"{df['trade_date'].iloc[-1].date()}")

    # 2. 信号生成
    print("\n[2/5] 信号生成")

    print("\n  SMA 交叉信号：")
    sma_sig = sma_signal(df)
    print(f"  持仓天数占比（全样本）：{sma_sig.mean():.2%}")

    print("\n  ML 信号（随机森林）：")
    ml_sig, split_idx = ml_signal(df)

    # 3. 回测（只在测试期回测）
    print("\n[3/5] 回测（测试期）")

    # 买入持有基准
    bh_result = backtest(
        df, pd.Series(1, index=df.index),
        start_idx=split_idx, name="买入持有"
    )

    # SMA 策略
    sma_result = backtest(df, sma_sig, start_idx=split_idx, name="SMA 交叉")

    # ML 策略
    ml_result = backtest(df, ml_sig, start_idx=split_idx, name="ML 信号")

    # 4. 可视化
    print("\n[4/5] 可视化")
    results = [bh_result, sma_result, ml_result]
    plot_equity_curve(df, results, split_idx)
    plot_metrics(results)

    # 5. 总结
    print("\n[5/5] 总结")
    print("\n  " + "=" * 56)
    print(f"  {'策略':<10s} {'累计收益':>10s} {'年化':>10s} "
          f"{'夏普':>8s} {'最大回撤':>10s} {'胜率':>8s}")
    print("  " + "-" * 56)
    for r in results:
        print(f"  {r['name']:<10s} "
              f"{r['cumulative_return']:>10.2%} "
              f"{r['annual_return']:>10.2%} "
              f"{r['sharpe']:>8.3f} "
              f"{r['max_drawdown']:>10.2%} "
              f"{r['win_rate']:>8.2%}")
    print("  " + "=" * 56)

    print(f"\n  解读要点：")
    print(f"  1. ML 信号比 SMA 好吗？好多少？")
    print(f"  2. 夏普比率 > 0.5 算不错；< 0 说明风险调整后不如无风险资产")
    print(f"  3. 最大回撤 > 20% 时，实盘心态很难扛住")
    print(f"  4. 胜率 50%+ 只是基础——关键是赢的时候赚多少、输的时候亏多少")
    print(f"  5. 如果 ML 打不过买入持有，说明模型在这个数据上没学到有用的东西")

    print(f"\n  训练/测试分离的意义：")
    print(f"  - 模型在训练期拟合，信号在测试期生成，回测在测试期进行")
    print(f"  - 这就是 train/test split 在量化交易中的直接应用")
    print(f"  - 在训练期回测 = 数据泄漏 = 自欺欺人")

    print("\n" + "=" * 60)
    print("完成。图表已保存至 output/ 目录。")
    print("=" * 60)
    print("\n下一步：")
    print("  - 换成你 W4 落盘的个股数据（参考 README.md 改造指引）")
    print("  - W15 用 ≥2 种模型生成信号，投票融合后回测对比")


if __name__ == "__main__":
    main()
