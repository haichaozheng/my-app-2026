"""
课堂实验二参考脚本（兜底用）：词典法每日情绪分数

课堂上的正规流程是让 opencode 把 mini_emotion.py 改成这样（见 setup.md 第2练），
本脚本供教师课前验证效果、课堂网络故障时兜底投屏。

词典：zhang_unformal_pos.txt / zhang_unformal_neg.txt（每行一个词），
与 app.py Part 3 词典法、week01-nlp-lab.ipynb 用的是同一份网络情感词典。

用法：python daily_sentiment.py（在 case-nlp 目录下运行）
依赖：pip install pandas jieba
"""

import sys
import time
from pathlib import Path

import jieba
import pandas as pd

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base = Path(__file__).parent


def load_dict(path):
    """读词典：每行一个词，去掉空行和首尾空格"""
    return {w.strip() for w in path.read_text(encoding='utf-8').splitlines() if w.strip()}


pos_words = load_dict(base / 'zhang_unformal_pos.txt')
neg_words = load_dict(base / 'zhang_unformal_neg.txt')
print(f"词典加载：正面 {len(pos_words)} 词，负面 {len(neg_words)} 词\n")

df = pd.read_csv(base / 'cleaned_300251_comments.csv', usecols=['date', 'comment'])
df['comment'] = df['comment'].fillna('').str.replace(r'\s+', '', regex=True)
df['day'] = pd.to_datetime(df['date']).dt.date


def sentiment_score(text):
    """一条评论的分数：分词后命中正面词 +1、负面词 -1（重复出现重复计）"""
    words = jieba.lcut(text)
    return sum(1 for w in words if w in pos_words) - sum(1 for w in words if w in neg_words)


t0 = time.time()
df['score'] = df['comment'].map(sentiment_score)
print(f"对 {len(df)} 条评论分词打分，耗时 {time.time() - t0:.0f} 秒\n")

daily = df.groupby('day')['score'].sum().sort_index()
daily.index.name = 'day'
daily.to_csv(base / 'daily_sentiment.csv', encoding='utf-8-sig')

print(f"共 {len(daily)} 个交易日，已存 daily_sentiment.csv\n")
print("情绪最高的 5 天：")
print(daily.nlargest(5).to_string())
print("\n情绪最低的 5 天：")
print(daily.nsmallest(5).to_string())
