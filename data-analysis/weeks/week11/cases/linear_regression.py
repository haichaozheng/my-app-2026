"""上证指数次日收益率预测：线性回归完整流程。

流程：
  1. 读入 sse_daily.csv（fetch_data.py 生成）
  2. 构造技术指标特征 + 次日收益率标签
  3. 散点图直觉
  4. 按时间切 train/test（前 80% 训练，后 20% 测试）
  5. sklearn LinearRegression
  6. 手写 SGD（梯度下降）
  7. 过拟合自检：训练 R² vs 测试 R²

对应课堂 notebook：machine learning for stock prediction.ipynb
  §gradient descent → §线性回归 → §train/test split
课堂用 gdp_satisfaction.csv；本案例把同一流程搬到上证指数上。
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent
OUT_DIR = DATA_DIR / "output"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


# ════════════════════════════════════════════════════════
# 1. 数据加载与特征构造
# ════════════════════════════════════════════════════════

def load_and_engineer() -> pd.DataFrame:
    """读入上证指数日线，构造特征与标签。"""
    csv_path = DATA_DIR / "sse_daily.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"未找到 {csv_path}\n"
            "请先运行：python fetch_data.py"
        )

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    df["trade_date"] = pd.to_datetime(df["trade_date"], format="%Y%m%d")
    df = df.sort_values("trade_date").reset_index(drop=True)

    close = df["close"]

    # ── 特征构造 ──
    df["ma_5"] = close.rolling(5).mean()
    df["ma_20"] = close.rolling(20).mean()
    df["ma_diff"] = df["ma_5"] - df["ma_20"]
    df["vol_ratio"] = df["vol"] / df["vol"].rolling(5).mean()

    # 5 日收益率标准差（波动率）
    daily_return = close.pct_change()
    df["volatility_5"] = daily_return.rolling(5).std()

    # 动量特征
    df["return_1d"] = df["pct_chg"] / 100  # pct_chg 是百分比，转小数
    df["return_5d"] = (close / close.shift(5) - 1)

    # ── 标签：次日简单收益率 ──
    df["next_return"] = close.shift(-1) / close - 1

    # 丢掉前 20 行（MA20 需要预热）和最后一行（无次日收益）
    df = df.dropna(subset=[
        "ma_5", "ma_20", "ma_diff", "vol_ratio",
        "volatility_5", "return_1d", "return_5d", "next_return",
    ]).reset_index(drop=True)

    return df


FEATURE_COLS = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]
LABEL_COL = "next_return"


# ════════════════════════════════════════════════════════
# 2. 散点图直觉
# ════════════════════════════════════════════════════════

def plot_scatter(df: pd.DataFrame) -> None:
    """当日涨跌幅 vs 次日收益率散点图——看有没有线性关系。"""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["return_1d"], df["next_return"], alpha=0.15, s=10)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("当日收益率")
    ax.set_ylabel("次日收益率")
    ax.set_title("当日收益率 vs 次日收益率")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "scatter_return_vs_ma5.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'scatter_return_vs_ma5.png'}")

    corr = df["return_1d"].corr(df["next_return"])
    print(f"  当日收益率与次日收益率相关系数：{corr:.4f}")
    print(f"  （接近 0 说明单变量线性关系很弱——这正是需要多特征的原因）")


# ════════════════════════════════════════════════════════
# 3. 按时间切 train/test
# ════════════════════════════════════════════════════════

def split_data(df: pd.DataFrame):
    """按时间切：前 80% 训练，后 20% 测试。

    注意：金融数据不能随机打乱（会造成数据泄漏）。
    课堂 notebook 用 train_test_split(random_state=42) 是因为
    gdp_satisfaction 每行是一个独立国家，没有时序性。
    """
    split_idx = int(len(df) * 0.8)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]

    X_train = train[FEATURE_COLS].values
    y_train = train[LABEL_COL].values
    X_test = test[FEATURE_COLS].values
    y_test = test[LABEL_COL].values

    print(f"  训练集：{len(train)} 条（{train['trade_date'].iloc[0].date()} ~ "
          f"{train['trade_date'].iloc[-1].date()}）")
    print(f"  测试集：{len(test)} 条（{test['trade_date'].iloc[0].date()} ~ "
          f"{test['trade_date'].iloc[-1].date()}）")

    return X_train, y_train, X_test, y_test


# ════════════════════════════════════════════════════════
# 4. sklearn 线性回归
# ════════════════════════════════════════════════════════

def sklearn_fit(X_train, y_train, X_test, y_test) -> LinearRegression:
    """用 sklearn LinearRegression 拟合并评估。"""
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 训练集
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_mse = mean_squared_error(y_train, y_train_pred)

    # 测试集
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)

    print("\n  sklearn LinearRegression")
    print(f"  {'特征':<16s} {'系数':>12s}")
    for name, coef in zip(FEATURE_COLS, model.coef_):
        print(f"  {name:<16s} {coef:>12.6f}")
    print(f"  {'截距':<16s} {model.intercept_:>12.6f}")

    print(f"\n  训练集  R2 = {train_r2:.4f}  MSE = {train_mse:.8f}")
    print(f"  测试集  R2 = {test_r2:.4f}  MSE = {test_mse:.8f}")
    print(f"  （测试 R2 可能是负的——金融数据噪声大，"
          "负 R² 意味着模型还不如直接猜均值）")

    # 预测值 vs 真实值散点
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_test, y_test_pred, alpha=0.2, s=10)
    lim = max(abs(y_test).max(), abs(y_test_pred).max())
    ax.plot([-lim, lim], [-lim, lim], "r--", linewidth=1, label="y = x（完美预测）")
    ax.set_xlabel("真实次日收益率")
    ax.set_ylabel("预测次日收益率")
    ax.set_title(f"sklearn 预测 vs 真实（测试集 R²={test_r2:.4f}）")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "regression_fit.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'regression_fit.png'}")

    return model


# ════════════════════════════════════════════════════════
# 5. 手写 SGD（梯度下降）
# ════════════════════════════════════════════════════════

def sgd_fit(X_train, y_train, X_test, y_test, eta=0.001, n_iter=100_000):
    """手写梯度下降拟合线性回归。

    对应课堂 notebook 中的 gd() 函数（code.docx 有答案）。
    这里用矩阵形式实现，但逻辑完全一致：
      预测 = X @ w + b
      损失 = (预测 - y)²
      梯度 = 2 * (预测 - y) * X   （对 w）
      更新 = w - eta * 梯度
    """
    n_samples, n_features = X_train.shape

    # 标准化特征（梯度下降需要，否则不同量级的特征收敛速度差异巨大）
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0) + 1e-8
    X_train_norm = (X_train - mean) / std
    X_test_norm = (X_test - mean) / std

    # 初始化参数
    w = np.zeros(n_features)
    b = 0.0

    # 记录损失变化
    losses = []

    for i in range(n_iter):
        pred = X_train_norm @ w + b
        error = pred - y_train

        # 梯度
        grad_w = 2 * (X_train_norm.T @ error) / n_samples
        grad_b = 2 * error.mean()

        # 更新
        w = w - eta * grad_w
        b = b - eta * grad_b

        if i % 10000 == 0:
            loss = (error ** 2).mean()
            losses.append((i, loss))
            print(f"    iter {i:>6d}  loss = {loss:.8f}")

    # 评估
    y_test_pred = X_test_norm @ w + b
    sgd_r2 = r2_score(y_test, y_test_pred)

    print(f"\n  手写 SGD 结果")
    print(f"  测试集 R2 = {sgd_r2:.4f}")

    # 与 sklearn 对比
    fig, ax = plt.subplots(figsize=(7, 4))
    iters = [l[0] for l in losses]
    vals = [l[1] for l in losses]
    ax.plot(iters, vals, marker="o")
    ax.set_xlabel("迭代次数")
    ax.set_ylabel("MSE 损失")
    ax.set_title("手写 SGD 损失下降曲线")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "sgd_vs_sklearn.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'sgd_vs_sklearn.png'}")

    print(f"\n  对照课堂 code.docx 答案：")
    print(f"  课堂 gd(eta, w, b, x, y) 处理单变量；")
    print(f"  本案例扩展到多变量，梯度逻辑相同：grad_w = 2 * X.T @ (X@w + b - y) / n")

    return w, b


# ════════════════════════════════════════════════════════
# 6. 过拟合自检
# ════════════════════════════════════════════════════════

def overfitting_check(df: pd.DataFrame) -> None:
    """对比：全量 fit vs train/test split fit。"""
    X = df[FEATURE_COLS].values
    y = df[LABEL_COL].values

    # 全量 fit
    model_full = LinearRegression()
    model_full.fit(X, y)
    full_r2 = r2_score(y, model_full.predict(X))

    # split fit
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model_split = LinearRegression()
    model_split.fit(X_tr, y_tr)
    train_r2 = r2_score(y_tr, model_split.predict(X_tr))
    test_r2 = r2_score(y_te, model_split.predict(X_te))

    print(f"\n  过拟合自检")
    print(f"  全量 fit R2           = {full_r2:.4f}")
    print(f"  随机 split 训练 R2     = {train_r2:.4f}")
    print(f"  随机 split 测试 R2     = {test_r2:.4f}")
    print(f"  训练-测试差距          = {train_r2 - test_r2:.4f}")
    print(f"  （差距大 = 过拟合；差距小 = 模型可能本身就没什么用）")

    # 图：时间序列 split vs 随机 split 对比
    split_idx = int(len(df) * 0.8)
    X_time_tr = df.iloc[:split_idx][FEATURE_COLS].values
    y_time_tr = df.iloc[:split_idx][LABEL_COL].values
    X_time_te = df.iloc[split_idx:][FEATURE_COLS].values
    y_time_te = df.iloc[split_idx:][LABEL_COL].values

    model_time = LinearRegression()
    model_time.fit(X_time_tr, y_time_tr)
    time_train_r2 = r2_score(y_time_tr, model_time.predict(X_time_tr))
    time_test_r2 = r2_score(y_time_te, model_time.predict(X_time_te))

    fig, ax = plt.subplots(figsize=(8, 4))
    categories = ["全量\nfit", "随机 split\n训练", "随机 split\n测试",
                  "时间 split\n训练", "时间 split\n测试"]
    values = [full_r2, train_r2, test_r2, time_train_r2, time_test_r2]
    colors = ["#3b82f6", "#3b82f6", "#ef4444", "#3b82f6", "#ef4444"]
    bars = ax.bar(categories, values, color=colors, alpha=0.7)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_ylabel("R²")
    ax.set_title("过拟合自检：不同 split 方式的 R² 对比")
    ax.grid(True, alpha=0.3, axis="y")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                f"{val:.4f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "overfitting_check.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'overfitting_check.png'}")
    print(f"\n  注意：时间 split 的测试 R2 通常比随机 split 更低——")
    print(f"  因为随机打乱混入了未来信息，是数据泄漏。")


# ════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════

def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("案例：用上证指数预测次日收益率——线性回归")
    print("=" * 60)

    # 1. 数据加载与特征构造
    print("\n[1/6] 数据加载与特征构造")
    df = load_and_engineer()
    print(f"  样本数：{len(df)}")
    print(f"  日期范围：{df['trade_date'].iloc[0].date()} ~ "
          f"{df['trade_date'].iloc[-1].date()}")
    print(f"  特征列：{FEATURE_COLS}")
    print(f"  标签列：{LABEL_COL}")

    # 2. 散点图直觉
    print("\n[2/6] 散点图直觉")
    plot_scatter(df)

    # 3. train/test split
    print("\n[3/6] 按时间切 train/test（前 80% 训练，后 20% 测试）")
    X_train, y_train, X_test, y_test = split_data(df)

    # 4. sklearn 回归
    print("\n[4/6] sklearn LinearRegression")
    sklearn_fit(X_train, y_train, X_test, y_test)

    # 5. 手写 SGD
    print("\n[5/6] 手写 SGD（梯度下降）")
    sgd_fit(X_train, y_train, X_test, y_test)

    # 6. 过拟合自检
    print("\n[6/6] 过拟合自检")
    overfitting_check(df)

    print("\n" + "=" * 60)
    print("完成。图表已保存至 output/ 目录。")
    print("=" * 60)
    print("\n下一步：")
    print("  - 换成你 W4 落盘的项目数据（参考 README.md 改造指引）")
    print("  - W13 用决策树/随机森林升级模型，看特征重要性")
    print("  - W14 用模型预测生成交易信号，做策略回测")


if __name__ == "__main__":
    main()
