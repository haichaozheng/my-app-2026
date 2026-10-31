# Week 09 NLP 上机实验 — 中文金融文本分词与量化

> 定位：配合本周「LLM 原理 + OpenCode Skills」主题。在把文本交给 LLM 之前，先亲手做一遍传统 NLP 的完整流程——**分词 → 词频 → 词典法情感打分 → LLM 情感分析 → 每日情绪曲线 → 情绪与股价的相关性**，理解「文本如何变成数据」，并体会词典法和 LLM 法的边界。约 80–110 分钟，计入平时成绩「技能小练」。对应视频资料：3.1/3.2 词语切分（分词简介 + jieba）。

## 实验环境

1. 已完成 week01 的 Python 环境配置（`py -3.13` + 项目 `.venv`，未配置见 `data-analysis/weeks/week01/python-setup.md`）
2. 安装依赖（在已激活的 `.venv` 中）：

```bash
pip install jieba pandas matplotlib openai python-dotenv
```

3. **工作目录**：在 `week09/` 目录下运行脚本，这样相对路径才能找到数据
4. **LLM API Key**：Part 4 接入 DeepSeek，需要一枚可用的 Key。按 `llm-key-guide.md` 申请（优先免费额度，兜底用课程演示 Key），放到 `week09/.env` 文件里（**不要写进代码、不要提交**，确认 `.gitignore` 里有 `.env`）：

```bash
# week09/.env（加入 .gitignore，永不提交）
DEEPSEEK_API_KEY=sk-你的deepseek密钥
```

5. 数据文件：

| 文件 | 内容 |
|---|---|
| `cleaned_300251_comments.csv` | 光线传媒（300251）股吧评论约 12.4 万条，2011-07 ~ 2019-04，含 `date`（评论时间）与 `comment`（正文）列 |
| `300251_daily.csv` | 光线传媒日线行情（来自 tushare，教师已导出）：1751 个交易日，2011-08-03 ~ 2019-04-10，含 `trade_date`、`close`、`pct_chg`（涨跌幅 %） |
| `stopwordsHIT.txt` | 哈工大停用词表（去重后约 830 词，一词一行） |
| `userdict.txt` | jieba 自定义词典（金融术语，一词一行） |
| `zhang_unformal_pos.txt` | 正面情感词表（911 词） |
| `zhang_unformal_neg.txt` | 负面情感词表（964 词） |

> 本实验所有数据文件都在 `week09/` 目录下，在 `week09/` 目录运行脚本即可直接读取。

---

## Part 0：读数据 + 清洗（10 分钟）

真实评论数据很脏：正文里混着 `\r\n` 和成串空格，还有纯表情/数字的空壳评论。

```python
import pandas as pd

df = pd.read_csv("cleaned_300251_comments.csv", parse_dates=["date"])

def clean(text):
    """把 \r\n 和连续空白压成单个空格"""
    return " ".join(text.split()) if isinstance(text, str) else ""

df["text"] = df["comment"].apply(clean)
df = df[df["text"] != ""].reset_index(drop=True)   # 丢掉空评论

print(f"有效评论 {len(df)} 条")
print("时间范围:", df["date"].min(), "->", df["date"].max())
df[["date", "text"]].head()
```

**观察**：随便看 10 条正文，哪些一看就没有分析价值（纯数字、太短）？你觉得需要多长的最短长度过滤？

## Part 1：分词——中文 NLP 的第一道坎（15 分钟）

英文有空格分隔单词，中文没有。「利好茅台明天加仓」是一整串字符，机器不知道哪几个字是一个词。**分词就是把连续文本切成词**。

### 原理速览：机器怎么知道在哪里切？

同一个句子可以有多种切法——「欢迎新老师生前来就餐」既可以是「欢迎 / 新老 / 师生 / 前来 / 就餐」，也可以切成「欢迎 / 新老师 / 生前 / 来 / 就餐」。所谓「最好的切法」需要规则或优化目标来定义，常见方法分两类：

**① 基于规则：最大匹配方法（Maximum Match Method）**

需要一个预定义词典，按「贪心地切出最长的词」来分。步骤：

1. 从句首取 m 个字符作为候选（m = 词典里最长词的长度）；
2. 查词典：**匹配成功** → 切出一个词；**匹配失败** → 去掉最后一个字，再匹配；
3. 重复直到句子切完。从左往右扫是**正向最大匹配**，从右往左是**逆向最大匹配**，两者都跑再择优的是**双向最大匹配**。

> **例**：词典 {南京、南京市、市长、江、大桥、长江、长江大桥}，max_len = 4，对「南京市长江大桥」做正向最大匹配——先取「南京市长」不在词典，去掉「长」→「南京市」命中，切出「南京市」；剩下「长江大桥」→「长江大桥」命中。结果：**南京市 / 长江大桥**。但同一句话也能切成「南京市长 / 江大桥」——规则法只顾「往前贪最长」，无法回头比较整体，这就是歧义问题。

**② 基于统计：统计切词法（语言模型）**

思路换了一个角度：不是「查词」，而是**比较各种切法哪种更可能出现**。语言模型给长度为 n 的词序列分配一个概率 p(w₁, w₂, …, wₙ)，我们选择概率最大的切分结果。

- 最简单的假设是各词独立（uni-gram），联合概率 = 各词概率的乘积；词的概率从语料库的词频统计得到。也可以用 n-gram 考虑词与词的搭配条件概率。
- 概率也可以不靠人工统计，而由序列模型（循环神经网络，乃至今天的大语言模型）来估计。

**jieba = 两种思路的结合**：先利用**前缀词典**找出句中所有可能的切分位置，构造一个**有向无环图（DAG）**；再用**动态规划**算出概率最大的路径，作为最终切分。

了解了原理，我们来看 jieba 在真实股评上的表现：

```python
text = "利好茅台，明天加仓稳稳的幸福"

# ① 不加载自定义词典
print(list(jieba.cut(text)))

# ② 加载金融自定义词典后再分
jieba.load_userdict("userdict.txt")
print(list(jieba.cut(text)))
```

**观察**：加载 `userdict.txt` 前后，「加仓」「稳稳」等金融/网络用语被正确切出了吗？

再从真实数据抽 3 条检查分词质量：

```python
for c in df["text"].sample(3, random_state=42):
    print(c, "->", jieba.lcut(c))
```

**记录**：找出至少 1 条分词分错的评论，写下来错在哪（这一步很重要，思考题要用）。

## Part 2：停用词 + 词频统计（15 分钟）

分出来的词里大量是「的、了、是、吗」——出现最多但对分析没用。这里用**哈工大停用词表**（`stopwordsHIT.txt`），而不是手写几个词：

```python
from collections import Counter

# utf-8-sig 会自动去掉文件开头的 BOM 字符
with open("stopwordsHIT.txt", encoding="utf-8-sig") as f:
    stopwords = {w.strip() for w in f if w.strip()}
print(f"停用词 {len(stopwords)} 个")

def tokenize(text):
    """分词 + 去停用词 + 去单字和空白"""
    return [w for w in jieba.lcut(text)
            if w not in stopwords and len(w.strip()) > 1]

# 12 万条全量分词约 1-2 分钟，正好喝口水
words = []
for c in df["text"]:
    words.extend(tokenize(c))

freq = Counter(words)
print(freq.most_common(20))
```

画成图（提交物之一）：

```python
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]   # 中文显示
plt.rcParams["axes.unicode_minus"] = False

top20 = freq.most_common(20)
labels, counts = zip(*top20)

plt.figure(figsize=(8, 6))
plt.barh(range(len(labels))[::-1], counts)
plt.yticks(range(len(labels))[::-1], labels)
plt.title("股评高频词 Top 20")
plt.tight_layout()
plt.savefig("nlp_top20_words.png", dpi=150)
plt.show()
```

**观察**：Top 20 里哪些词反映了股民情绪？哪些词其实还是噪音（该加进停用词表）？

## Part 3：情感词典打分——词典法完整流程（20 分钟）

W8 你见过词典法；这次自己从零跑通，为下一步画每日情绪曲线做准备。

```python
def load_words(path):
    with open(path, encoding="utf-8") as f:
        return {w.strip() for w in f if w.strip()}

pos_words = load_words("zhang_unformal_pos.txt")
neg_words = load_words("zhang_unformal_neg.txt")
print(f"正面词 {len(pos_words)} 个，负面词 {len(neg_words)} 个")

def sentiment_score(text):
    words = jieba.lcut(text)
    return sum(w in pos_words for w in words) - sum(w in neg_words for w in words)

# 12 万条全量打分约 2-3 分钟；建议先在抽样上调试通过，再跑全量
df["score"] = df["text"].apply(sentiment_score)
df["label"] = df["score"].apply(lambda s: "正面" if s > 0 else ("负面" if s < 0 else "中性"))

print(df["label"].value_counts(normalize=True).round(3))
print(df.nlargest(3, "score")[["date", "text", "score"]].to_string())
print(df.nsmallest(3, "score")[["date", "text", "score"]].to_string())
```

词典法跑通了，但它有天花板（想想反讽）。下一步用 LLM 分析**同样的评论**，两种方法正面比一比。

## Part 4：接入大模型做情感分析——LLM 法（15 分钟）

词典法是「查表打分」，LLM 法是把文本**发给大模型**、让它像人一样读懂再判断。这里用 `openai` 工具包以 API 形式接入 DeepSeek（OpenAI 兼容接口，改 `base_url` 就能换平台）。

> **成本考虑**：只发 **10 条**评论做示例。10 条短评论约 1–2 千 token，成本不到 1 分钱；但如果把 12 万条全量发给 API，既烧钱又可能触发限流。工程上的习惯是：**先小样本验证逻辑，再决定全量的性价比**。

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)   # 读取 week09/.env

client = OpenAI(
    base_url="https://api.deepseek.com",      # OpenAI 兼容接口：换平台只需改这一行
    api_key=os.getenv("DEEPSEEK_API_KEY"),    # Key 永远从环境变量读，不写进代码
)

# 抽 10 条（带词典法结果，方便对比）
sample10 = df[["text", "score", "label"]].sample(10, random_state=42).reset_index(drop=True)

system_prompt = """你是金融文本情感分析助手。对给出的每条股吧评论判断情感倾向：
- 正面：看多、乐观、买入意愿
- 中性：陈述事实、提问、无明显情感
- 负面：看空、抱怨、悲观、反讽

注意反讽和网络用语（如"利好"可能是反讽）。只输出 JSON，不要输出其他内容，格式：
{"results": [{"id": 0, "label": "正面", "reason": "一句话理由"}, ...]}"""

user_prompt = "评论列表：\n" + chr(10).join(
    f"{i}. {t}" for i, t in enumerate(sample10["text"]))

completion = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},   # 定角色、定规则、定输出格式
        {"role": "user", "content": user_prompt},       # 带数据
    ],
    temperature=0,          # 分类任务要稳定，不要发散
)
print(completion.choices[0].message.content)
```

> `messages` 里 system 和 user 的分工是 LLM 应用的通用范式：**system 定角色和规则（每次任务基本不变），user 带具体数据（每次不同）**。这样换任务时只改 user 部分。

解析返回结果，和词典法并排对比：

```python
import json

results = json.loads(completion.choices[0].message.content)["results"]
sample10["llm_label"] = [r["label"] for r in results]
sample10["llm_reason"] = [r["reason"] for r in results]

print(sample10[["text", "label", "llm_label", "llm_reason"]].to_string())
agree = (sample10["label"] == sample10["llm_label"]).mean()
print(f"\n两种方法一致率: {agree:.0%}")
```

> 若 JSON 解析报错：DeepSeek 偶尔会用 ` ```json ` 围栏包住输出，把围栏剥掉再 `json.loads` 即可；`temperature=0` 下通常很稳定。

**对比记录**（提交物）：

| 对比点 | 词典法（你的代码） | LLM 法（DeepSeek） |
|---|---|---|
| 10 条判断结果 | | |
| 判不一致的评论 | | |
| 能识别反讽吗 | | |
| 成本与速度 | 免费毫秒级，可跑 12 万条 | 约 1 分钱/10 条，全量又贵又慢 |

挑 1–2 条**两种方法判不一致**的评论，说说你站哪边、为什么。

## Part 5：每日情感分数——把文本变成情绪指数（20 分钟）

单条评论的情感有了，现在按天聚合：**当日情感分数 = 当天正面评论数 − 当天负面评论数**。这就是一个从股吧文本「算」出来的情绪指数。

```python
daily = (df.groupby(df["date"].dt.date)["label"]
           .value_counts()
           .unstack(fill_value=0))
daily["sentiment"] = daily.get("正面", 0) - daily.get("负面", 0)
print(daily["sentiment"].describe())

plt.figure(figsize=(12, 4))
plt.plot(daily.index, daily["sentiment"], alpha=0.4, label="每日情感分数")
plt.plot(daily.index, daily["sentiment"].rolling(30, center=True).mean(),
         linewidth=2, label="30 日滑动平均")
plt.axhline(0, color="gray", linewidth=0.8)
plt.title("股吧每日情感分数（正面评论数 − 负面评论数）")
plt.legend()
plt.tight_layout()
plt.savefig("nlp_daily_sentiment.png", dpi=150)
plt.show()
```

**观察**：

1. 情绪曲线有没有明显的极端日？取 `daily["sentiment"].idxmin()` 和 `idxmax()` 找到那几天，去原始数据里看看当天股民在吵什么
2. **一个隐患**：这个「分数」受当天评论量影响——评论越多的日子，正面−负面的绝对值天然越大。怎么改更公平？（提示：除以当天评论总数，得到净情感比例；放进思考题）

## Part 6：情绪与股价——相关系数（20 分钟）

情绪曲线有了，股价数据也备好了（`300251_daily.csv`）。现在回答一个金融文本分析的经典问题：**股吧情绪和股价涨跌幅有关系吗？**

```python
price = pd.read_csv("300251_daily.csv", parse_dates=["trade_date"])
price["day"] = price["trade_date"].dt.date
print(price.head())

# 情绪表（Part 5 的 daily）与行情表按日期对齐
# 用 inner join：周末和节假日发评论没有对应行情，自动剔除
merged = daily.reset_index().merge(
    price[["day", "close", "pct_chg"]],
    left_on="date", right_on="day", how="inner")
print(f"匹配到 {len(merged)} 个交易日")

# 同日相关：情绪是「同步反映」涨跌吗？
r_same = merged["sentiment"].corr(merged["pct_chg"])

# 滞后相关：情绪能「预测」明天吗？（把涨跌幅向前挪一天）
merged["next_pct_chg"] = merged["pct_chg"].shift(-1)
r_next = merged["sentiment"].corr(merged["next_pct_chg"])

print(f"当日情绪 vs 当日涨跌幅: r = {r_same:.3f}")
print(f"当日情绪 vs 次日涨跌幅: r = {r_next:.3f}")
```

画散点图看关系的形状（提交物之一）：

```python
plt.figure(figsize=(6, 5))
plt.scatter(merged["sentiment"], merged["pct_chg"], alpha=0.3, s=10)
plt.axhline(0, color="gray", linewidth=0.8)
plt.xlabel("每日情感分数（正面数 − 负面数）")
plt.ylabel("当日涨跌幅 (%)")
plt.title(f"股吧情绪 vs 当日涨跌幅（r = {r_same:.3f}）")
plt.tight_layout()
plt.savefig("nlp_sentiment_vs_return.png", dpi=150)
plt.show()
```

**解读标尺**：|r| < 0.1 几乎不相关；0.1–0.3 弱；0.3–0.5 中等；> 0.5 强。样本大时（这里上千个交易日）很小的 r 也可能统计显著，但**显著 ≠ 有用**。

**观察**：

1. 两个 r 哪个更大？如果当日相关明显强于次日相关，说明情绪更像涨跌的「果」而不是「因」——当天涨了股民才兴奋
2. 极端值的影响：2011-08-03 上市首日 `pct_chg` 高达 +40.95%，2015 年牛市顶部也有极端波动。用 `method="spearman"`（按秩算相关，抗极端值）重算一次，r 变了多少？
3. **相关 ≠ 因果**：就算 r 不小，也说明不了「看多情绪推动股价」——可能是股价推动情绪，也可能两者都被第三因素（大盘、消息面）驱动

## 提交

- 一个可运行的脚本或 notebook（Part 0–6 完整流程）
- 三张图：高频词 Top 20、每日情感分数曲线、情绪 vs 涨跌幅散点图
- Part 6 的两个相关系数（同日 + 次日）和一句话解读
- Part 4 的对比表（填好）+ 3–5 句结论：词典法和 LLM 法各输在哪、你会在自己项目里用哪种（考虑成本）
- 当日在 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）

## 自检（达标线）

- [ ] 能说清为什么中文必须分词、以及自定义词典解决了什么问题
- [ ] 能指出至少 1 条分词错误、并说出你会往 `userdict.txt` 里加什么词
- [ ] Part 4 的 LLM 调用跑通了，对比表里两种方法各有具体数字
- [ ] 每日情感曲线画出来了，并指出一个指数的局限（评论量偏差或反讽误判）
- [ ] 两个相关系数算出来了，并能说出「当日相关 vs 次日相关」谁大说明什么
- [ ] 能说出为什么示例只发 10 条（成本与限流），以及全量 12 万条该怎么做
- [ ] 结论不是「AI 更聪明」这种空话，而是指出具体差异（如：LLM 法识别了反讽，词典法把它计为正面）

## 思考题（连接 LLM，写在提交末尾）

1. **分词的歧义**：「南京市长江大桥」可以切成「南京市 / 长江大桥」也可以是「南京市长 / 江大桥」。jieba 靠什么决定切法？什么情况下会切错？
2. **情绪指数的口径**：Part 5 的「正面数 − 负面数」和「（正面 − 负面）÷ 当日评论总数」哪个更适合当情绪指数？各会在什么情况下误导你？
3. **LLM 不用 jieba**：LLM 的 tokenizer（如 BPE）把文本切成 subword 而不是「词」。为什么 LLM 不需要人工维护 `userdict.txt` 这样的词典？
4. **词典法的天花板**：找到一条你的词典法判错、但 LLM 判对的评论（比如反讽）。LLM 靠什么做到了词典法做不到的事？（提示：回看 `llm.ipynb` 里 Attention 部分——每个词「看」它的上下文）
5. **成本与工程**：如果老师要求给全部 12 万条评论都打上 LLM 情感标签，你会怎么设计方案控制成本？（提示：抽样估计、批量请求、便宜的小模型、或只对「词典法不确定」的评论调用 LLM）
6. **情绪能预测股价吗**：如果 Part 6 里次日相关的 r 非常小，能得出「股吧情绪没有预测价值」的结论吗？（提示：情绪指数的口径、极端行情日、以及「预测」需要的是显著为正的 r_next 而不只是接近 0 的相关性）

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

## 学习资料

- `text_data_processing_2.ipynb`（向量与余弦相似度：课后想深入「文本变成向量」的同学看这个，涉及 TF-IDF 的进阶用法）
- 视频（超星学习通）：3.1/3.2 词语切分；4.1 文本量化 TF-IDF（课后延伸，本次课上不做）
- `llm-key-guide.md`（API Key 申请路径与安全红线）
- DeepSeek API 文档（OpenAI 兼容接口）：https://api-docs.deepseek.com
- tushare 行情接口（`300251_daily.csv` 的来源，进阶可自己拉取）：https://tushare.pro/document/2?doc_id=27
- jieba 文档：https://github.com/fxsjy/jieba
