"""上证指数涨跌预测：决策树与随机森林 + 四模型横评。

流程：
  1. 读入本目录 sse_daily.csv，构造分类标签（次日涨=1, 跌=0）
  2. 决策树训练 + 过拟合观察
  3. 树深度对比（max_depth=1/3/5/10/None）
  4. 随机森林 vs 单树
  5. 特征重要性排名
  6. 四模型横评（逻辑回归 / KNN / 决策树 / 随机森林）

对应课堂 notebook：market prediction - random forest_class.ipynb
本目录自带 sse_daily.csv（上证指数日线），特征构造与 W11/W14 案例一致，标签改为分类。
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# 本目录（数据与脚本同级，完全自包含）
DATA_DIR = Path(__file__).resolve().parent
OUT_DIR = Path(__file__).resolve().parent / "output"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FEATURE_COLS = [
    "ma_5", "ma_20", "ma_diff", "vol_ratio",
    "volatility_5", "return_1d", "return_5d",
]
LABEL_COL = "next_up"  # 0=跌, 1=涨


# ════════════════════════════════════════════════════════
# 1. 数据加载与标签构造
# ════════════════════════════════════════════════════════

def load_and_engineer() -> pd.DataFrame:
    """读本目录 sse_daily.csv，构造分类标签。"""
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

    # 特征（与 W11 完全一致）
    df["ma_5"] = close.rolling(5).mean()
    df["ma_20"] = close.rolling(20).mean()
    df["ma_diff"] = df["ma_5"] - df["ma_20"]
    df["vol_ratio"] = df["vol"] / df["vol"].rolling(5).mean()
    daily_return = close.pct_change()
    df["volatility_5"] = daily_return.rolling(5).std()
    df["return_1d"] = df["pct_chg"] / 100
    df["return_5d"] = close / close.shift(5) - 1

    # 标签：次日上涨=1，下跌=0（与 W11 回归标签不同）
    df["next_return"] = close.shift(-1) / close - 1
    df["next_up"] = (df["next_return"] > 0).astype(int)

    df = df.dropna(subset=FEATURE_COLS + [LABEL_COL]).reset_index(drop=True)
    return df


def time_split(df: pd.DataFrame, ratio=0.8):
    """按时间切 train/test。"""
    split_idx = int(len(df) * ratio)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    X_train = train[FEATURE_COLS].values
    y_train = train[LABEL_COL].values
    X_test = test[FEATURE_COLS].values
    y_test = test[LABEL_COL].values
    print(f"  训练集：{len(train)} 条  测试集：{len(test)} 条")
    print(f"  训练集涨占比：{y_train.mean():.2%}  "
          f"测试集涨占比：{y_test.mean():.2%}")
    return X_train, y_train, X_test, y_test


# ════════════════════════════════════════════════════════
# 2. 决策树
# ════════════════════════════════════════════════════════

def fit_decision_tree(X_train, y_train, X_test, y_test) -> DecisionTreeClassifier:
    """训练决策树，观察过拟合倾向。"""
    tree = DecisionTreeClassifier(max_depth=5, random_state=42)
    tree.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, tree.predict(X_train))
    test_acc = accuracy_score(y_test, tree.predict(X_test))

    print(f"\n  决策树（max_depth=5）")
    print(f"  训练准确率 = {train_acc:.4f}")
    print(f"  测试准确率 = {test_acc:.4f}")
    print(f"  差距 = {train_acc - test_acc:.4f}（差距大=过拟合）")

    return tree


# ════════════════════════════════════════════════════════
# 3. 树深度对比
# ════════════════════════════════════════════════════════

def compare_tree_depth(X_train, y_train, X_test, y_test) -> None:
    """max_depth=1/3/5/10/None，看训练 vs 测试分数变化。"""
    depths = [1, 2, 3, 5, 8, 10, 15, None]
    train_scores = []
    test_scores = []

    for d in depths:
        tree = DecisionTreeClassifier(max_depth=d, random_state=42)
        tree.fit(X_train, y_train)
        train_scores.append(accuracy_score(y_train, tree.predict(X_train)))
        test_scores.append(accuracy_score(y_test, tree.predict(X_test)))

    labels = [str(d) if d is not None else "None" for d in depths]

    print(f"\n  树深度对比")
    print(f"  {'depth':<8s} {'训练准确率':>12s} {'测试准确率':>12s} {'差距':>8s}")
    for label, tr, te in zip(labels, train_scores, test_scores):
        print(f"  {label:<8s} {tr:>12.4f} {te:>12.4f} {tr - te:>8.4f}")

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(labels))
    ax.plot(x, train_scores, "o-", label="训练准确率", color="#3b82f6")
    ax.plot(x, test_scores, "s-", label="测试准确率", color="#ef4444")
    ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--", label="随机猜测")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("max_depth")
    ax.set_ylabel("准确率")
    ax.set_title("决策树深度 vs 过拟合（max_depth 越大，训练分越高但测试分下降）")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "tree_depth_comparison.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'tree_depth_comparison.png'}")


# ════════════════════════════════════════════════════════
# 4. 随机森林 vs 单树
# ════════════════════════════════════════════════════════

def fit_random_forest(X_train, y_train, X_test, y_test) -> RandomForestClassifier:
    """随机森林 vs 单树对比。"""
    # 单树（不限深度，容易过拟合）
    single_tree = DecisionTreeClassifier(random_state=42)
    single_tree.fit(X_train, y_train)
    tree_train = accuracy_score(y_train, single_tree.predict(X_train))
    tree_test = accuracy_score(y_test, single_tree.predict(X_test))

    # 随机森林（100 棵树）
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_train = accuracy_score(y_train, rf.predict(X_train))
    rf_test = accuracy_score(y_test, rf.predict(X_test))

    print(f"\n  随机森林 vs 单树")
    print(f"  {'模型':<12s} {'训练准确率':>12s} {'测试准确率':>12s} {'差距':>8s}")
    print(f"  {'单树':<12s} {tree_train:>12.4f} {tree_test:>12.4f} "
          f"{tree_train - tree_test:>8.4f}")
    print(f"  {'随机森林':<12s} {rf_train:>12.4f} {rf_test:>12.4f} "
          f"{rf_train - rf_test:>8.4f}")

    print(f"\n  观察：")
    print(f"  - 单树训练分接近 1.0（完全记住训练数据）→ 严重过拟合")
    print(f"  - 随机森林训练-测试差距更小 → bagging + 随机特征降低过拟合")
    print(f"  - 测试分可能只比单树高一点点 → 森林不是万能的")

    # 图
    fig, ax = plt.subplots(figsize=(6, 5))
    models = ["单树\n(无限制)", "随机森林\n(100棵, depth=5)"]
    train_vals = [tree_train, rf_train]
    test_vals = [tree_test, rf_test]
    x = np.arange(len(models))
    w = 0.3
    ax.bar(x - w / 2, train_vals, w, label="训练", color="#3b82f6", alpha=0.7)
    ax.bar(x + w / 2, test_vals, w, label="测试", color="#ef4444", alpha=0.7)
    ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--", label="随机猜测")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("准确率")
    ax.set_title("随机森林 vs 单树")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "rf_vs_tree.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'rf_vs_tree.png'}")

    return rf


# ════════════════════════════════════════════════════════
# 5. 特征重要性
# ════════════════════════════════════════════════════════

def plot_feature_importance(rf: RandomForestClassifier) -> None:
    """随机森林的特征重要性排名——反哺 W12 特征工程。"""
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]

    print(f"\n  特征重要性（随机森林）")
    print(f"  {'排名':<6s} {'特征':<16s} {'重要性':>10s}")
    for rank, idx in enumerate(indices):
        print(f"  {rank + 1:<6d} {FEATURE_COLS[idx]:<16s} "
              f"{importances[idx]:>10.4f}")

    fig, ax = plt.subplots(figsize=(8, 5))
    sorted_names = [FEATURE_COLS[i] for i in indices]
    sorted_vals = importances[indices]
    bars = ax.barh(range(len(sorted_names)), sorted_vals, color="#10b981", alpha=0.7)
    ax.set_yticks(range(len(sorted_names)))
    ax.set_yticklabels(sorted_names)
    ax.invert_yaxis()
    ax.set_xlabel("重要性")
    ax.set_title("随机森林特征重要性排名")
    ax.grid(True, alpha=0.3, axis="x")
    for bar, val in zip(bars, sorted_vals):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{val:.4f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "feature_importance.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'feature_importance.png'}")

    print(f"\n  解读：")
    print(f"  - 重要性高的特征 → W12 特征工程应保留或强化")
    print(f"  - 重要性低的特征 → 考虑丢弃或重构（可能信息量不足）")
    print(f"  - 特征重要性 ≠ 因果关系，只是模型用了多少")


# ════════════════════════════════════════════════════════
# 6. 四模型横评
# ════════════════════════════════════════════════════════

def compare_four_models(X_train, y_train, X_test, y_test) -> None:
    """逻辑回归 / KNN / 决策树 / 随机森林，同一数据同一指标。"""
    models = {
        "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
        "KNN (k=7)": KNeighborsClassifier(n_neighbors=7),
        "决策树": DecisionTreeClassifier(max_depth=5, random_state=42),
        "随机森林": RandomForestClassifier(
            n_estimators=100, max_depth=5, random_state=42),
    }

    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        tr = accuracy_score(y_train, model.predict(X_train))
        te = accuracy_score(y_test, model.predict(X_test))
        results.append((name, tr, te))
        print(f"  {name:<10s}  训练={tr:.4f}  测试={te:.4f}  "
              f"差距={tr - te:.4f}")

    # 图
    names = [r[0] for r in results]
    train_vals = [r[1] for r in results]
    test_vals = [r[2] for r in results]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(names))
    w = 0.3
    bars1 = ax.bar(x - w / 2, train_vals, w, label="训练准确率",
                   color="#3b82f6", alpha=0.7)
    bars2 = ax.bar(x + w / 2, test_vals, w, label="测试准确率",
                   color="#ef4444", alpha=0.7)
    ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--",
               label="随机猜测(0.5)")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("准确率")
    ax.set_title("四模型横评：上证指数次日涨跌预测")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    for bars, vals in [(bars1, train_vals), (bars2, test_vals)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.005,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "four_models_comparison.png", dpi=150)
    plt.close(fig)
    print(f"  → {OUT_DIR / 'four_models_comparison.png'}")

    print(f"\n  三种思路总结：")
    print(f"  - 逻辑回归：从数据学线性规律（fit 参数）→ 适合线性关系")
    print(f"  - KNN：找最近的 K 个邻居（不学习）→ 适合小数据")
    print(f"  - 决策树：学 if-else 规则 → 适合非线性 + 可解释")
    print(f"  - 随机森林：多棵树投票 → 适合非线性 + 稳健")
    print(f"  没有绝对赢家——看你的数据和问题选模型。")


# ════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════

def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("案例：决策树与随机森林——上证指数涨跌预测")
    print("=" * 60)

    # 1. 数据加载
    print("\n[1/6] 数据加载与标签构造")
    df = load_and_engineer()
    print(f"  样本数：{len(df)}")
    print(f"  涨占比：{df[LABEL_COL].mean():.2%}")
    print(f"  数据来源：本目录 sse_daily.csv")

    # 2. train/test split
    print("\n[2/6] 按时间切 train/test")
    X_train, y_train, X_test, y_test = time_split(df)

    # 3. 决策树
    print("\n[3/6] 决策树")
    fit_decision_tree(X_train, y_train, X_test, y_test)

    # 4. 树深度对比
    print("\n[4/6] 树深度对比（过拟合观察）")
    compare_tree_depth(X_train, y_train, X_test, y_test)

    # 5. 随机森林 + 特征重要性
    print("\n[5/6] 随机森林 + 特征重要性")
    rf = fit_random_forest(X_train, y_train, X_test, y_test)
    plot_feature_importance(rf)

    # 6. 四模型横评
    print("\n[6/6] 四模型横评")
    compare_four_models(X_train, y_train, X_test, y_test)

    print("\n" + "=" * 60)
    print("完成。图表已保存至 output/ 目录。")
    print("=" * 60)
    print("\n下一步：")
    print("  - 换成你的项目数据（参考 README.md 改造指引）")
    print("  - W14 用随机森林生成交易信号，做策略回测")


if __name__ == "__main__":
    main()
