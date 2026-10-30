# -*- coding: utf-8 -*-
r"""科创50指数（000688.SH）近30天收盘价走势图

数据来源: tushare MCP -> index_daily（已保存为 star50_index_daily.csv）
运行方式: 在仓库根目录执行  .venv\Scripts\python.exe data-analysis\weeks\week08\plot_star50_close.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---- 中文字体设置（Windows） ----
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ---- 数据路径 ----
HERE = Path(__file__).parent
CSV_FILE = HERE / "star50_index_daily.csv"
PNG_FILE = HERE / "star50_close_trend.png"

# ---- 读取数据 ----
df = pd.read_csv(CSV_FILE, parse_dates=["trade_date"])
df = df.sort_values("trade_date")

# ---- 画图 ----
fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(df["trade_date"], df["close"], marker="o", markersize=4,
        linewidth=2, color="#d62728", label="收盘价")

# 标注最高点和最低点
idx_max = df["close"].idxmax()
idx_min = df["close"].idxmin()
for idx, name in [(idx_max, "区间最高"), (idx_min, "区间最低")]:
    row = df.loc[idx]
    ax.annotate(
        f"{name}\n{row['close']:.2f}",
        xy=(row["trade_date"], row["close"]),
        xytext=(0, 18 if idx == idx_max else -34),
        textcoords="offset points",
        ha="center", fontsize=10, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="gray"),
    )

# 区间涨跌幅
first, last = df.iloc[0], df.iloc[-1]
chg = (last["close"] / first["pre_close"] - 1) * 100

ax.set_title(f"科创50指数收盘价走势（近30天，{first['trade_date']:%Y-%m-%d} ~ {last['trade_date']:%Y-%m-%d}）",
             fontsize=14, fontweight="bold")
ax.set_xlabel("交易日")
ax.set_ylabel("收盘价（点）")
ax.text(0.98, 0.95, f"区间涨跌幅：{chg:+.2f}%",
        transform=ax.transAxes, fontsize=12, fontweight="bold",
        color="#d62728" if chg < 0 else "#2ca02c",
        ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.8))

ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="lower left")
fig.autofmt_xdate(rotation=45)
fig.tight_layout()

# ---- 保存 ----
fig.savefig(PNG_FILE, dpi=150, bbox_inches="tight")
print(f"图片已保存: {PNG_FILE}")
