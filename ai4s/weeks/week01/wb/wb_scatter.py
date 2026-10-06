"""
发展散点图——GDP vs 预期寿命（气泡=人口，颜色=腐败控制）

从 panel.csv 读取数据，画一张 Hans Rosling 风格的散点图。
不调 API，离线可跑。

用法：python wb_scatter.py
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

# 设置中文字体（Windows 用微软雅黑，Mac 用 PingFang）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 6 个标注国家
FEATURED = ['CHN', 'USA', 'KOR', 'BRA', 'IND', 'NGA']

# 国家代码 → 中文简称
NAME_MAP = {
    'CHN': '中国', 'USA': '美国', 'KOR': '韩国',
    'BRA': '巴西', 'IND': '印度', 'NGA': '尼日利亚',
}


def load_latest(panel_path, year=2020):
    """从面板 CSV 读取某一年的截面数据"""
    df = pd.read_csv(panel_path, encoding='utf-8-sig')
    df = df[df['year'] == year].copy()
    return df


def scatter_gdp_life(df, year, out_path):
    """GDP vs 预期寿命散点图（气泡=人口，颜色=腐败控制）"""

    fig, ax = plt.subplots(figsize=(12, 8))

    # 过滤掉缺失值
    plot_df = df.dropna(subset=['人均GDP(美元)', '预期寿命(岁)', '总人口'])
    # 腐败控制缺失的用灰色
    has_gov = plot_df['腐败控制指数'].notna()

    # 气泡大小：人口缩放到合理范围
    sizes = (plot_df['总人口'] / 1e6).clip(lower=1) * 4

    # 有治理数据的点：按腐败控制着色
    sc1 = ax.scatter(
        plot_df.loc[has_gov, '人均GDP(美元)'],
        plot_df.loc[has_gov, '预期寿命(岁)'],
        s=sizes.loc[has_gov],
        c=plot_df.loc[has_gov, '腐败控制指数'],
        cmap='RdYlGn',          # 红→黄→绿，低腐败=绿
        vmin=-2.5, vmax=2.5,    # WGI 范围
        alpha=0.7, edgecolors='gray', linewidths=0.5,
        zorder=3,
    )

    # 无治理数据的点：灰色
    ax.scatter(
        plot_df.loc[~has_gov, '人均GDP(美元)'],
        plot_df.loc[~has_gov, '预期寿命(岁)'],
        s=sizes.loc[~has_gov],
        c='lightgray', alpha=0.5, edgecolors='gray', linewidths=0.5,
        zorder=2,
    )

    # 标注 6 个代表国家
    for code in FEATURED:
        row = plot_df[plot_df['country'] == code]
        if len(row) == 0:
            continue
        x = row['人均GDP(美元)'].values[0]
        y = row['预期寿命(岁)'].values[0]
        name = NAME_MAP.get(code, code)
        ax.annotate(
            f'{name}\n${x:,.0f} · {y:.1f}岁',
            xy=(x, y),
            xytext=(12, 12), textcoords='offset points',
            fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='gray', alpha=0.8),
            arrowprops=dict(arrowstyle='->', color='gray', lw=0.8),
            zorder=5,
        )

    # 对数 X 轴
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    # 轴标签
    ax.set_xlabel('人均 GDP（美元，对数轴）', fontsize=12)
    ax.set_ylabel('预期寿命（岁）', fontsize=12)
    ax.set_title(f'发展为了什么？——GDP vs 预期寿命（{year}年）\n'
                 f'气泡大小=人口  ·  颜色=腐败控制（绿=好，红=差）',
                 fontsize=14, fontweight='bold')

    # 颜色条
    cbar = plt.colorbar(sc1, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('腐败控制指数（-2.5 ~ +2.5）', fontsize=11)

    # 网格
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(300, 200000)
    ax.set_ylim(45, 88)

    # 底部注释
    fig.text(0.5, 0.01,
             '数据来源：世界银行 WDI & WGI  ·  '
             '绿点=腐败控制好  ·  红点=腐败控制差  ·  灰点=无治理数据',
             ha='center', fontsize=9, color='gray')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"  散点图 → {out_path}")
    plt.close()


def main():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    panel_path = os.path.join(data_dir, 'panel.csv')

    if not os.path.exists(panel_path):
        print("错误：找不到 panel.csv，请先运行 wb_explore.py 生成数据")
        return

    year = 2020
    print(f"读取 {panel_path}，提取 {year} 年截面数据…")
    df = load_latest(panel_path, year)
    print(f"  {len(df)} 个国家有数据\n")

    out_path = os.path.join(data_dir, 'scatter_gdp_life.png')
    scatter_gdp_life(df, year, out_path)

    # 速览发现
    featured_df = df[df['country'].isin(FEATURED)].dropna(
        subset=['人均GDP(美元)', '预期寿命(岁)']
    )
    print("── 6 国速览 ──")
    for _, row in featured_df.sort_values('人均GDP(美元)', ascending=False).iterrows():
        code = row['country']
        name = NAME_MAP.get(code, code)
        gdp = row['人均GDP(美元)']
        life = row['预期寿命(岁)']
        gov = row.get('腐败控制指数')
        gov_str = f'{gov:+.2f}' if pd.notna(gov) else 'N/A'
        print(f"  {name:6s}  ${gdp:>8,.0f}  {life:.1f}岁  腐败控制={gov_str}")
    print()

    print("── 图中能看到什么 ──")
    print("  • 右上角：富国长寿（美国、韩国）——但美国不如韩国长寿")
    print("  • 左下角：穷国短寿（尼日利亚）——但印度比尼日利亚穷却活更久")
    print("  • 颜色：绿点（低腐败）集中在右上，红点（高腐败）在左下")
    print("  • 气泡：中国和印度的气泡最大（人口多）")
    print("  • 对数轴上 GDP 与寿命呈 S 形而非直线——边际递减")


if __name__ == '__main__':
    main()
