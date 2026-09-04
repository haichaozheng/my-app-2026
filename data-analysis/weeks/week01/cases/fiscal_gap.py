"""国家财政收支缺口：近十年是「少收」还是「多花」在主导？

只用全年：取 12 月、且支出与收入量级相当的年份（丢掉明显仍是当月值的 12 月，以及两边都空的 2016 年）。
支出为不含债务还本，单位亿元。
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "nation"
OUT_DIR = Path(__file__).resolve().parent / "output"


def load_series(filename: str, value_name: str, growth_name: str) -> pd.DataFrame:
    df = pd.read_excel(DATA_DIR / filename)
    df.columns = ["time_raw", value_name, growth_name]
    parsed = df["time_raw"].astype(str).str.extract(r"(\d{4}).*?(\d{1,2})")
    df["year"] = pd.to_numeric(parsed[0], errors="coerce")
    df["month"] = pd.to_numeric(parsed[1], errors="coerce")
    return df.dropna(subset=["year", "month", value_name]).copy()


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    rev = load_series("财政收入-月度数据.xlsx", "revenue", "revenue_yoy")
    exp = load_series("财政支出-月度数据.xlsx", "expenditure", "expenditure_yoy")
    both = rev.merge(exp, on=["year", "month"], how="inner")
    both["gap"] = both["expenditure"] - both["revenue"]
    both["gap_to_revenue"] = both["gap"] / both["revenue"] * 100
    both["growth_gap"] = both["expenditure_yoy"] - both["revenue_yoy"]

    # 12 月：支出至少达到收入的一半，才像全年数而不是当月值。
    annual = (
        both[(both["month"] == 12) & (both["expenditure"] > 0.5 * both["revenue"])]
        .sort_values("year")
        .copy()
    )

    print("问题：近十年国家财政全年收支缺口（支出−收入）是在扩大还是收窄？")
    print("      缺口扩大时，主要是收入掉得快，还是支出加得猛？")
    print()
    print("只用 12 月；支出须与收入量级相当。2016 年 12 月两边都空，故缺一年。")
    print()
    print("—— 全年（12 月，亿元）——")
    cols = [
        "year",
        "revenue",
        "expenditure",
        "gap",
        "gap_to_revenue",
        "revenue_yoy",
        "expenditure_yoy",
        "growth_gap",
    ]
    print(annual[cols].round(1).to_string(index=False))

    latest = annual.iloc[-1]
    y2019 = annual.loc[annual["year"] == 2019].iloc[0]
    y2012 = annual.iloc[0]

    print()
    print("要点")
    print(
        f"- {int(y2012['year'])} 年缺口占收入 {y2012['gap_to_revenue']:.1f}%，"
        f"2019 年为 {y2019['gap_to_revenue']:.1f}%，"
        f"{int(latest['year'])} 年为 {latest['gap_to_revenue']:.1f}%"
        f"（{latest['gap']:.0f} 亿元）。"
    )
    print(
        f"- {int(latest['year'])} 年收入累计增速 {latest['revenue_yoy']:.1f}%，"
        f"支出 {latest['expenditure_yoy']:.1f}%："
        + (
            "缺口扩大主要来自收入走弱。"
            if latest["revenue_yoy"] < latest["expenditure_yoy"]
            else "支出比收入收得更紧。"
        )
    )

    annual[cols].to_csv(OUT_DIR / "annual_gap.csv", index=False, encoding="utf-8-sig")
    print()
    print(f"已写入 {OUT_DIR / 'annual_gap.csv'}")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("未安装 matplotlib，跳过作图。")
        return

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

    axes[0].plot(annual["year"], annual["gap"] / 10000, marker="o")
    axes[0].axhline(0, color="gray", linewidth=0.8)
    axes[0].set_ylabel("收支缺口（万亿元）")
    axes[0].set_title("国家财政全年收支缺口（12 月：支出 − 收入）")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(annual["year"], annual["revenue_yoy"], marker="o", label="收入增速")
    axes[1].plot(annual["year"], annual["expenditure_yoy"], marker="s", label="支出增速")
    axes[1].axhline(0, color="gray", linewidth=0.8)
    axes[1].set_xlabel("年")
    axes[1].set_ylabel("累计同比（%）")
    axes[1].set_title("全年收入与支出增速")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "fiscal_gap.png", dpi=150)
    print(f"已写入 {OUT_DIR / 'fiscal_gap.png'}")


if __name__ == "__main__":
    main()
