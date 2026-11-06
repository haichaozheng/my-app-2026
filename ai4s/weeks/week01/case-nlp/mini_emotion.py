"""
课堂演示参考脚本（兜底用）：股吧文本如何变成数据

课堂上的正规流程是让 opencode 现场生成类似脚本（见 plan.md 第2节第 8 步），
本脚本供教师课前验证效果、课堂网络故障时兜底投屏。

演示问题：第1节案例里提到的"割韭菜"情绪，在 12.4 万条评论中是怎么随时间变化的？

用法：python mini_emotion.py（在 case-nlp 目录下运行）
依赖：pip install pandas
"""

import sys
from pathlib import Path

import pandas as pd

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

csv_path = Path(__file__).parent / 'cleaned_300251_comments.csv'
df = pd.read_csv(csv_path, usecols=['date', 'comment'])
df['comment'] = df['comment'].fillna('').str.replace(r'\s+', '', regex=True)
df['year'] = pd.to_datetime(df['date']).dt.year

# 关键词计数：粗粒度的"情绪代理变量"——正是 W9 词典法的最简雏形
keywords = ['韭菜', '利好', '崩盘', '涨停']
print(f"共 {len(df)} 条评论（光线传媒 300251 股吧）\n")

for kw in keywords:
    hit = df[df['comment'].str.contains(kw, na=False)]
    per_year = hit.groupby('year').size()
    top = per_year.idxmax()
    print(f"「{kw}」出现 {len(hit)} 条，最集中的年份：{top}（{per_year.max()} 条/年）")

print("\n—— 同一批文本，不同的关键词规则会给出不同的'情绪'图景；")
print("   词典法和 LLM 法的分歧，根源也在这里。这就是课堂上留下的那个疑问。")
