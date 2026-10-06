"""
发展为了什么？——GDP、治理与发展的跨国速览

W1 课堂案例：用 wbgapi 拉取世界银行数据
验证 Python + wbgapi 环境可用，同时展示一个真实的社科研究问题。

用法：python wb_explore.py
依赖：pip install wbgapi pandas
数据源：https://data.worldbank.org/indicator?tab=all

数据覆盖：
  - 国家：全部（200+，自动排除地区汇总）
  - 年份：2005-2024（20 年，足够面板回归）
  - 指标：30 个，覆盖经济/健康/教育/性别/不平等/科技/治理/金融/人口 9 个主题
"""

import sys
import os
import time
import wbgapi as wb
import pandas as pd

# 修复 Windows 终端中文乱码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def wb_fetch(code, countries, **kwargs):
    """带重试的 wbgapi 调用（世界银行 API 偶尔限流返回空响应）"""
    # WGI 治理指标在 db=3，其余在 db=2（WDI）
    if code.startswith('GOV_WGI'):
        kwargs.setdefault('db', 3)
    for attempt in range(3):
        try:
            return wb.data.DataFrame(code, countries, **kwargs)
        except Exception as e:
            if attempt < 2:
                wait = 3 * (attempt + 1)
                print(f"    [{code}] 第 {attempt+1} 次失败，{wait}s 后重试… ({e.__class__.__name__})")
                time.sleep(wait)
            else:
                print(f"    [{code}] 重试 3 次仍失败，跳过此指标")
                return None


# ─── 配置区（学生可自行修改）──────────────────────────

# 展示用：6 个代表性国家（课堂速览只看这几个）
FEATURED = ['CHN', 'USA', 'KOR', 'BRA', 'IND', 'NGA']

# 面板数据用：全部国家（排除地区汇总如"东亚合计""高收入合计"）
ALL_COUNTRIES = 'all'

# 时间范围：20 年，足够 W6 面板回归
YEARS = range(2005, 2025)

# 30 个指标，覆盖 9 个社科主题
# 代码可在 https://data.worldbank.org/indicator?tab=all 查到
# WGI 治理指标在 db=3，其余在 db=2（WDI）
INDICATORS = {
    # ═══ 经济与增长（X / Z）═══
    'NY.GDP.PCAP.CD':    '人均GDP(美元)',
    'NY.GDP.MKTP.KD.ZG': 'GDP增长率(%)',
    'NE.TRD.GNFS.ZS':    '贸易开放度(%)',          # 贸易占GDP，全球化代理
    'BX.KLT.DINV.CD.WD': 'FDI净流入(美元)',         # 外资流入
    'NV.IND.TOTL.ZS':    '工业增加值占GDP(%)',      # 产业结构
    'NV.SRV.TOTL.ZS':    '服务业增加值占GDP(%)',    # 产业结构
    'FP.CPI.TOTL.ZG':    '通货膨胀率(%)',           # 宏观稳定
    'GC.TAX.TOTL.GD.ZS': '税收占GDP(%)',            # 政府财力 / 财政能力

    # ═══ 金融（X / Z）═══
    'FS.AST.PRVT.GD.ZS': '国内信贷占GDP(%)',        # 金融发展深度
    'FM.LBL.BMNY.GD.ZS': '广义货币占GDP(%)',        # 金融发展

    # ═══ 健康（Y）═══
    'SP.DYN.LE00.IN':    '预期寿命(岁)',
    'SP.DYN.IMRT.IN':    '婴儿死亡率(千分之一)',

    # ═══ 教育（Y / X / Z）═══
    'SE.TER.ENRR':       '高等教育入学率(%)',
    'SE.XPD.TOTL.GD.ZS': '教育支出占GDP(%)',

    # ═══ 性别（Y / X）═══
    'SL.TLF.CACT.FE.ZS': '女性劳动参与率(%)',
    'SP.ADO.TFRT':       '青少年生育率(千分之一)',
    'SG.GEN.PARL.ZS':    '女性议会席位(%)',         # 政治代表 / 治理结果

    # ═══ 不平等（Y）═══
    'SI.POV.GINI':       '基尼系数',

    # ═══ 科技与创新（Y / X）═══
    'IT.NET.USER.ZS':    '互联网普及率(%)',
    'IT.CEL.SETS.P2':    '移动电话订阅率(每百人)',
    'IP.PAT.RESD':       '本国居民专利申请数',
    'GB.XPD.RSDV.GD.ZS': '研发支出占GDP(%)',
    'SP.POP.SCIE.RD.P6': '每百万人研究人员',

    # ═══ 治理 WGI（Y / X，范围 -2.5 ~ +2.5）═══
    'GOV_WGI_CC.EST':    '腐败控制指数',
    'GOV_WGI_VA.EST':    '话语权与问责指数',
    'GOV_WGI_RL.EST':    '法治指数',
    'GOV_WGI_GE.EST':    '政府效能指数',
    'GOV_WGI_PV.EST':    '政治稳定指数',

    # ═══ 人口（Z）═══
    'SP.POP.TOTL':       '总人口',
    'SP.URB.TOTL.IN.ZS': '城镇化率(%)',
}

# ─── 数据拉取 ──────────────────────────────────────

def fetch_panel(indicators, countries, years):
    """拉取面板数据，返回长表 DataFrame（country, year, 各指标列）。

    逐个指标拉取，避免不同指标年份错位导致 NaN。
    WGI 指标自动使用 db=3。
    """
    frames = []
    for i, (code, name) in enumerate(indicators.items()):
        print(f"  [{i+1}/{len(indicators)}] {code} {name}…")
        df = wb_fetch(code, countries, time=years, skipAggs=True)
        if df is None:
            continue
        if df.index.nlevels > 1:
            df = df.reset_index()
            df = df.rename(columns={'economy': 'country', 'time': 'year'})
        else:
            df = df.reset_index().melt(
                id_vars='economy', var_name='year', value_name=name
            )
            df = df.rename(columns={'economy': 'country'})

        df['year'] = df['year'].astype(str).str.replace('YR', '')
        df = df.dropna(subset=[name])
        frames.append(df)
        time.sleep(0.5)  # 礼貌延迟，避免限流

    # 按 country, year 合并所有指标
    panel = frames[0]
    for f in frames[1:]:
        panel = panel.merge(f, on=['country', 'year'], how='outer')
    panel = panel.sort_values(['country', 'year']).reset_index(drop=True)
    return panel


def fetch_latest(indicators, countries):
    """取每个国家最近的非空值（跨国横向对比用）"""
    frames = []
    for code, name in indicators.items():
        df = wb_fetch(code, countries, mrv=3, skipAggs=True)
        if df is None:
            s = pd.Series(name=name, dtype=float)
            frames.append(s)
            continue
        if df.index.nlevels > 1:
            s = df.groupby(level='economy').apply(
                lambda g: g.droplevel('economy').dropna().iloc[-1, 0]
                if g.droplevel('economy').dropna().shape[0] > 0
                else float('nan')
            )
        else:
            df = df.sort_index(axis=1)
            s = df.apply(
                lambda row: row.dropna().iloc[-1] if row.dropna().any() else float('nan'),
                axis=1
            )
        s.name = name
        frames.append(s)
        time.sleep(0.5)
    return pd.concat(frames, axis=1)


# ─── 终端展示 ──────────────────────────────────────

def show_featured_comparison():
    """6 国速览：核心 Y 和 X 各几个"""
    print("正在从世界银行拉取数据…\n")

    # 速览用 8 个最有冲击力的指标
    showcase = {
        'NY.GDP.PCAP.CD':    '人均GDP(美元)',
        'SP.DYN.LE00.IN':    '预期寿命(岁)',
        'SI.POV.GINI':       '基尼系数',
        'GOV_WGI_CC.EST':    '腐败控制',
        'GOV_WGI_VA.EST':    '话语权与问责',
        'GOV_WGI_RL.EST':    '法治',
        'SG.GEN.PARL.ZS':    '女性议会席位(%)',
        'IP.PAT.RESD':       '本国居民专利数',
    }
    df = fetch_latest(showcase, FEATURED)

    print("=" * 70)
    print("  发展指标跨国对比（6 国 · 最近可用年份）")
    print("=" * 70)
    print(df.to_string(float_format='{:,.1f}'.format))
    print()

    # 速览发现
    gdp   = df['人均GDP(美元)'].dropna()
    life  = df['预期寿命(岁)'].dropna()
    gini  = df['基尼系数'].dropna()
    corrupt = df['腐败控制'].dropna()
    patent  = df['本国居民专利数'].dropna()
    parl    = df['女性议会席位(%)'].dropna()

    print("── 速览发现 ──")
    if len(gdp) >= 2:
        print(f"  最富裕：{gdp.idxmax()}  ${gdp.max():,.0f}")
        print(f"  最贫穷：{gdp.idxmin()}  ${gdp.min():,.0f}")
    if len(life) >= 2:
        print(f"  最长寿：{life.idxmax()}  {life.max():.1f} 岁")
        print(f"  最短寿：{life.idxmin()}  {life.min():.1f} 岁")
    if len(gini) >= 2:
        print(f"  最不平等：{gini.idxmax()}  基尼 {gini.max():.1f}")
        print(f"  最平等：{gini.idxmin()}  基尼 {gini.min():.1f}")
    if len(corrupt) >= 2:
        print(f"  腐败控制最好：{corrupt.idxmax()}  {corrupt.max():.2f}")
        print(f"  腐败控制最差：{corrupt.idxmin()}  {corrupt.min():.2f}")
    if len(patent) >= 2:
        print(f"  专利最多：{patent.idxmax()}  {patent.max():,.0f}")
        print(f"  专利最少：{patent.idxmin()}  {patent.min():,.0f}")
    if len(parl) >= 2:
        print(f"  女性议会席位最高：{parl.idxmax()}  {parl.max():.1f}%")
        print(f"  女性议会席位最低：{parl.idxmin()}  {parl.min():.1f}%")
    print()


def show_china_trend():
    """中国 20 年发展趋势"""
    print("=" * 70)
    print("  中国 2005-2024 发展趋势（8 个核心指标）")
    print("=" * 70)

    core = {
        'NY.GDP.PCAP.CD':    '人均GDP(美元)',
        'NY.GDP.MKTP.KD.ZG': 'GDP增长率(%)',
        'SP.DYN.LE00.IN':    '预期寿命(岁)',
        'SI.POV.GINI':       '基尼系数',
        'IT.NET.USER.ZS':    '互联网普及率(%)',
        'SP.URB.TOTL.IN.ZS': '城镇化率(%)',
        'GOV_WGI_CC.EST':    '腐败控制',
        'IP.PAT.RESD':       '本国居民专利数',
    }

    frames = []
    for code, name in core.items():
        s = wb_fetch(code, 'CHN', time=YEARS)
        if s is None:
            continue
        if s.index.nlevels > 1:
            s = s.droplevel('economy')
        else:
            s = s.T
        s.index = s.index.astype(str).str.replace('YR', '')
        s.columns = [name]
        frames.append(s)

    df = pd.concat(frames, axis=1).sort_index()

    print(df.to_string(float_format='{:,.1f}'.format))
    print()


# ─── 存 CSV ────────────────────────────────────────

def save_csv(panel):
    """保存 CSV：完整面板 + 跨国对比 + 中国趋势"""
    out_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(out_dir, exist_ok=True)

    # 1) 完整面板
    path_panel = os.path.join(out_dir, 'panel.csv')
    panel.to_csv(path_panel, index=False, encoding='utf-8-sig', float_format='%.1f')
    n_countries = panel['country'].nunique()
    n_indicators = len([c for c in panel.columns if c not in ('country', 'year')])
    print(f"  面板数据 → {path_panel}")
    print(f"    {len(panel)} 行 · {n_countries} 国 · {n_indicators} 指标 · 2005-2024")

    # 2) 跨国对比（6 国最近值，全指标）
    df_cross = fetch_latest(INDICATORS, FEATURED)
    df_cross.index.name = 'country'
    path_cross = os.path.join(out_dir, 'cross_country.csv')
    df_cross.to_csv(path_cross, encoding='utf-8-sig', float_format='%.1f')
    print(f"  跨国对比 → {path_cross}（6 国 × {len(INDICATORS)} 指标）")

    # 3) 中国 20 年趋势（全指标）
    china = panel[panel['country'] == 'CHN'].copy()
    china = china.set_index('year').drop(columns='country')
    path_china = os.path.join(out_dir, 'china_trend.csv')
    china.to_csv(path_china, encoding='utf-8-sig', float_format='%.1f')
    print(f"  中国趋势 → {path_china}（20 年 × {len(INDICATORS)} 指标）")

    print()


# ─── 主流程 ────────────────────────────────────────

def main():
    show_featured_comparison()
    show_china_trend()

    print("── 拉取完整面板数据并存为 CSV（可能需要 2-3 分钟）──\n")
    panel = fetch_panel(INDICATORS, ALL_COUNTRIES, YEARS)
    save_csv(panel)

    print("── 思考题 ──")
    print("  1. 最富裕的国家一定腐败控制最好吗？（GDP → 治理？）")
    print("  2. 中国的腐败控制指数 20 年来怎么变？增长是否伴随治理改善？")
    print("  3. 互联网普及率与女性议会席位有什么关系？")
    print("  4. 法治指数对预期寿命的影响——控制 GDP 后还显著吗？（W6）")
    print("  5. panel.csv 有 200+ 国家 × 30 指标 × 20 年——")
    print("     能否做'贸易开放度 → 腐败控制'的面板回归？（W6）")
    print("  6. 换成你自己研究方向的指标——")
    print("     浏览 https://data.worldbank.org/indicator?tab=all 找代码")


if __name__ == '__main__':
    main()
