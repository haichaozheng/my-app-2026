"""
中国 2005-2024 发展趋势图——6 个子图

从 china_trend.csv 读取数据，画 6 张时序图，展示中国 20 年的发展轨迹。
不调 API，离线可跑。

用法：python wb_china_trend.py
依赖：pip install pandas matplotlib
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# 修复 Windows 终端中文乱码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_china(csv_path):
    """读取中国趋势 CSV"""
    df = pd.read_csv(csv_path, encoding='utf-8-sig', index_col='year')
    df.index = df.index.astype(int)
    return df.sort_index()


def plot_china_trends(df, out_path):
    """画 6 个子图：经济、健康、不平等、科技、治理、性别"""

    fig, axes = plt.subplots(3, 2, figsize=(14, 15))
    fig.suptitle('中国 2005-2024 发展趋势\n数据来源：世界银行 WDI & WGI',
                 fontsize=16, fontweight='bold', y=0.98)

    # 颜色
    C_BLUE = '#2E86AB'
    C_RED = '#E63946'
    C_GREEN = '#06A77D'
    C_ORANGE = '#F4A261'
    C_PURPLE = '#7B2CBF'
    C_BROWN = '#9C6644'

    # ── 子图 1：经济——人均 GDP（对数轴）+ GDP 增长率 ──
    ax = axes[0, 0]
    ax2 = ax.twinx()
    ax.plot(df.index, df['人均GDP(美元)'], color=C_BLUE, linewidth=2.5, marker='o',
            markersize=4, label='人均GDP')
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.set_ylabel('人均GDP（美元，对数轴）', color=C_BLUE, fontsize=11)
    ax.tick_params(axis='y', labelcolor=C_BLUE)

    ax2.bar(df.index, df['GDP增长率(%)'], color=C_ORANGE, alpha=0.4, width=0.6,
            label='GDP增长率')
    ax2.set_ylabel('GDP增长率（%）', color=C_ORANGE, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=C_ORANGE)
    ax2.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')

    ax.set_title('经济增长：人均GDP 20年翻7倍', fontsize=13, fontweight='bold')
    ax.set_xlim(2004.5, 2024.5)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 标注 2020 疫情冲击
    if 2020 in df.index:
        gdp2020 = df.loc[2020, 'GDP增长率(%)']
        if pd.notna(gdp2020):
            ax2.annotate(f'疫情\n{gdp2020:.1f}%', xy=(2020, gdp2020),
                         xytext=(2020.5, gdp2020 - 3), fontsize=8, color=C_RED,
                         arrowprops=dict(arrowstyle='->', color=C_RED, lw=0.8))

    # ── 子图 2：健康——预期寿命 + 婴儿死亡率 ──
    ax = axes[0, 1]
    ax2 = ax.twinx()
    ax.plot(df.index, df['预期寿命(岁)'], color=C_GREEN, linewidth=2.5, marker='o',
            markersize=4, label='预期寿命')
    ax.set_ylabel('预期寿命（岁）', color=C_GREEN, fontsize=11)
    ax.tick_params(axis='y', labelcolor=C_GREEN)
    ax.set_ylim(73, 79)

    if '婴儿死亡率(千分之一)' in df.columns:
        ax2.plot(df.index, df['婴儿死亡率(千分之一)'], color=C_RED, linewidth=2,
                 marker='s', markersize=3, linestyle='--', label='婴儿死亡率')
        ax2.set_ylabel('婴儿死亡率（千分之一）', color=C_RED, fontsize=11)
        ax2.tick_params(axis='y', labelcolor=C_RED)

    ax.set_title('健康：寿命续升，婴儿死亡率持续下降', fontsize=13, fontweight='bold')
    ax.set_xlim(2004.5, 2024.5)
    ax.grid(True, alpha=0.3, linestyle='--')

    # ── 子图 3：不平等——基尼系数 ──
    ax = axes[1, 0]
    gini = df['基尼系数'].dropna()
    ax.plot(gini.index, gini.values, color=C_RED, linewidth=2.5, marker='o', markersize=5)
    ax.fill_between(gini.index, gini.values, alpha=0.15, color=C_RED)
    ax.axhline(y=40, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.text(2005, 40.3, '国际警戒线 40', fontsize=8, color='gray')
    ax.set_ylabel('基尼系数', fontsize=11)
    ax.set_title('不平等：从 40.9 降到 36.0——越过库兹涅茨拐点？',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(2004.5, 2024.5)
    ax.set_ylim(34, 45)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 标注拐点
    peak_year = gini.idxmax()
    peak_val = gini.max()
    ax.annotate(f'峰值 {peak_val:.1f}\n({peak_year})',
                xy=(peak_year, peak_val),
                xytext=(peak_year + 2, peak_val + 1.5),
                fontsize=9, color=C_RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=1))

    # 标注最新值
    last_year = gini.index.max()
    last_val = gini.loc[last_year]
    ax.annotate(f'{last_val:.1f} ({last_year})',
                xy=(last_year, last_val),
                xytext=(last_year - 3.5, last_val - 2),
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=1))

    # ── 子图 4：科技——互联网普及率 + 专利数 ──
    ax = axes[1, 1]
    ax2 = ax.twinx()
    ax.plot(df.index, df['互联网普及率(%)'], color=C_BLUE, linewidth=2.5, marker='o',
            markersize=4, label='互联网普及率')
    ax.set_ylabel('互联网普及率（%）', color=C_BLUE, fontsize=11)
    ax.tick_params(axis='y', labelcolor=C_BLUE)
    ax.set_ylim(0, 100)

    patent = df['本国居民专利申请数'].dropna()
    ax2.plot(patent.index, patent.values / 1e4, color=C_PURPLE, linewidth=2,
             marker='s', markersize=3, linestyle='--', label='专利数(万件)')
    ax2.set_ylabel('本国居民专利申请（万件）', color=C_PURPLE, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=C_PURPLE)

    ax.set_title('科技：互联网从 8.5% → 92%，专利爆发式增长',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(2004.5, 2024.5)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 标注互联网跳变点
    if 2018 in df.index and 2017 in df.index:
        v18 = df.loc[2018, '互联网普及率(%)']
        v17 = df.loc[2017, '互联网普及率(%)']
        if pd.notna(v18) and pd.notna(v17):
            ax.annotate(f'跳变\n{v17:.0f}%→{v18:.0f}%',
                        xy=(2018, v18), xytext=(2019, v18 - 20),
                        fontsize=8, color=C_BLUE,
                        arrowprops=dict(arrowstyle='->', color=C_BLUE, lw=0.8))

    # ── 子图 5：治理——5 个 WGI 指标 ──
    ax = axes[2, 0]
    gov_cols = {
        '腐败控制指数':   (C_RED, '-'),
        '法治指数':       (C_BLUE, '--'),
        '政府效能指数':   (C_GREEN, '-.'),
        '话语权与问责指数': (C_ORANGE, ':'),
        '政治稳定指数':   (C_PURPLE, '-'),
    }
    for col, (color, ls) in gov_cols.items():
        if col in df.columns:
            s = df[col].dropna()
            if len(s) > 0:
                ax.plot(s.index, s.values, color=color, linewidth=1.8,
                        linestyle=ls, marker='o', markersize=3, label=col)

    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_ylabel('WGI 指数（-2.5 ~ +2.5）', fontsize=11)
    ax.set_title('治理：腐败控制改善，话语权低位徘徊',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(2004.5, 2024.5)
    ax.set_ylim(-2, 1.5)
    ax.legend(fontsize=8, loc='lower right', ncol=2)
    ax.grid(True, alpha=0.3, linestyle='--')

    # ── 子图 6：性别与结构——女性劳动参与率 + 城镇化率 ──
    ax = axes[2, 1]
    ax2 = ax.twinx()

    if '女性劳动参与率(%)' in df.columns:
        ax.plot(df.index, df['女性劳动参与率(%)'], color=C_RED, linewidth=2.5,
                marker='o', markersize=4, label='女性劳动参与率')
        ax.set_ylabel('女性劳动参与率（%）', color=C_RED, fontsize=11)
        ax.tick_params(axis='y', labelcolor=C_RED)

    ax2.plot(df.index, df['城镇化率(%)'], color=C_BROWN, linewidth=2.5,
             marker='s', markersize=4, linestyle='--', label='城镇化率')
    ax2.set_ylabel('城镇化率（%）', color=C_BROWN, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=C_BROWN)

    ax.set_title('性别与结构：城镇化率从 43%→66%，女性劳动参与率缓降',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(2004.5, 2024.5)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"  趋势图 → {out_path}")
    plt.close()


def main():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    csv_path = os.path.join(data_dir, 'china_trend.csv')

    if not os.path.exists(csv_path):
        print("错误：找不到 china_trend.csv，请先运行 wb_explore.py 生成数据")
        return

    print(f"读取 {csv_path}…")
    df = load_china(csv_path)
    print(f"  {len(df)} 年 × {len(df.columns)} 指标\n")

    out_path = os.path.join(data_dir, 'china_trend.png')
    plot_china_trends(df, out_path)

    # 打印关键发现
    print("── 6 张图的关键发现 ──")
    print()
    print("  图1 经济：人均GDP从$1,778涨到$13,293（7.5倍），2020年增长率骤降至2.3%")
    print("  图2 健康：预期寿命从74.1升到78.0岁，婴儿死亡率持续下降")
    print("  图3 不平等：基尼系数2008年达峰值43.0，之后降到36.0——越过库兹涅茨拐点")
    print("  图4 科技：互联网从8.5%飙到92%，专利从9万件涨到143万件")
    print("  图5 治理：腐败控制从-0.7升到+0.1，话语权与问责在-1.7低位")
    print("  图6 结构：城镇化率从43%升到66%，女性劳动参与率从65.8%缓降到60%")
    print()
    print("── 思考题 ──")
    print("  1. 基尼系数2008年拐点——是政策效应还是经济规律？")
    print("  2. 互联网2018年跳变——统计口径变化还是真实普及？")
    print("  3. 腐败控制改善但话语权不变——经济反腐败 vs 政治反腐？")
    print("  4. 女性劳动参与率下降——城镇化推高了家务替代成本？")


if __name__ == '__main__':
    main()
