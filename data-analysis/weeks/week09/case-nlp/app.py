# -*- coding: utf-8 -*-
"""
Week 09 NLP 上机实验 · 课堂展示版（Streamlit）
对应实验文档：week09-nlp-lab.md / week09-nlp-lab.ipynb

运行方式（在 week09/case-nlp/ 目录下）：
    streamlit run app.py

数据文件沿用 week09/ 根目录下的实验数据，无需复制。
"""
from pathlib import Path
import os

import jieba
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from collections import Counter
from dotenv import load_dotenv

# ---------------------------------------------------------------- 基础配置
DATA_DIR = Path(__file__).resolve().parent.parent   # week09/
REPO_ROOT = DATA_DIR.parents[2]                     # 仓库根目录（全局 .env 所在）
st.set_page_config(page_title="Week09 NLP 实验展示", page_icon="📊", layout="wide")

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def load_api_key() -> str | None:
    """读取 DEEPSEEK_API_KEY：week09/.env 优先，仓库根目录 .env 兜底。

    load_dotenv(override=False) 不覆盖已读到的变量，实现「就近优先」。
    """
    for d in [DATA_DIR, *DATA_DIR.parents]:
        env_file = d / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=False)
    return os.getenv("DEEPSEEK_API_KEY")


# ---------------------------------------------------------------- 缓存加载
@st.cache_data(show_spinner="读取评论数据…")
def load_comments() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "cleaned_300251_comments.csv", parse_dates=["date"])

    def clean(text):
        """把 \r\n 和连续空白压成单个空格"""
        return " ".join(text.split()) if isinstance(text, str) else ""

    df["text"] = df["comment"].apply(clean)
    df = df[df["text"] != ""].reset_index(drop=True)
    return df


@st.cache_data(show_spinner="读取行情数据…")
def load_price() -> pd.DataFrame:
    price = pd.read_csv(DATA_DIR / "300251_daily.csv", parse_dates=["trade_date"])
    price["day"] = price["trade_date"].dt.date
    return price


@st.cache_data
def load_stopwords() -> set:
    with open(DATA_DIR / "stopwordsHIT.txt", encoding="utf-8-sig") as f:
        return {w.strip() for w in f if w.strip()}


@st.cache_data
def load_words(name: str) -> set:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return {w.strip() for w in f if w.strip()}


@st.cache_resource(show_spinner="初始化 jieba…")
def init_jieba():
    jieba.initialize()
    jieba.load_userdict(str(DATA_DIR / "userdict.txt"))
    return jieba


@st.cache_data(show_spinner="分词 + 打分中（全量约 2-3 分钟）…")
def compute_pipeline(n: int, seed: int) -> pd.DataFrame:
    """抽样 n 条：分词、去停用词、词典法情感打分（对应 Part 2 / Part 3）"""
    df = load_comments().sample(n, random_state=seed).reset_index(drop=True)
    stopwords = load_stopwords()
    pos_words = load_words("zhang_unformal_pos.txt")
    neg_words = load_words("zhang_unformal_neg.txt")

    def tokenize(text):
        return [w for w in init_jieba().lcut(text)
                if w not in stopwords and len(w.strip()) > 1]

    def sentiment_score(text):
        words = init_jieba().lcut(text)
        return (sum(w in pos_words for w in words)
                - sum(w in neg_words for w in words))

    words: list = []
    for c in df["text"]:
        words.extend(tokenize(c))
    df["score"] = df["text"].apply(sentiment_score)
    df["label"] = df["score"].apply(
        lambda s: "正面" if s > 0 else ("负面" if s < 0 else "中性"))
    return df, Counter(words)


# ---------------------------------------------------------------- 侧边栏
st.sidebar.title("Week 09 · NLP 实验")
page = st.sidebar.radio(
    "实验环节",
    ["Part 0 读数据 + 清洗",
     "Part 1 分词",
     "Part 2 停用词 + 词频",
     "Part 3 词典法情感打分",
     "Part 4 LLM 情感分析",
     "Part 5 每日情感分数",
     "Part 6 情绪 vs 股价"],
)
st.sidebar.caption("对应实验文档 week09-nlp-lab.md")

df_all = load_comments()
n = st.sidebar.slider("抽样评论数（Part 2/3/5/6 使用）",
                      min_value=2000, max_value=len(df_all),
                      value=min(30000, len(df_all)), step=1000)
seed = st.sidebar.number_input("随机种子", value=42, step=1)

if page in ("Part 2 停用词 + 词频", "Part 3 词典法情感打分",
            "Part 5 每日情感分数", "Part 6 情绪 vs 股价"):
    df, freq = compute_pipeline(int(n), int(seed))
    # 每日情感分数 = 当天正面评论数 − 负面评论数（Part 5 / Part 6 共用）
    daily = (df.groupby(df["date"].dt.date)["label"]
               .value_counts()
               .unstack(fill_value=0))
    daily["sentiment"] = daily.get("正面", 0) - daily.get("负面", 0)

# ================================================================ Part 0
if page == "Part 0 读数据 + 清洗":
    st.header("Part 0：读数据 + 清洗")
    st.markdown(
        "真实评论数据很脏：正文混着 `\\r\\n` 和成串空格，还有纯表情/数字的空壳评论。"
        "清洗 = 压缩空白 + 丢掉空评论。")

    c1, c2, c3 = st.columns(3)
    c1.metric("有效评论", f"{len(df_all):,} 条")
    c2.metric("起始日期", str(df_all["date"].min().date()))
    c3.metric("结束日期", str(df_all["date"].max().date()))

    st.subheader("清洗后的数据预览")
    st.dataframe(df_all[["date", "text"]].head(20), width="stretch")

    st.subheader("评论长度分布")
    lengths = df_all["text"].str.len()
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.hist(lengths.clip(upper=200), bins=60, color="#4C78A8")
    ax.axvline(lengths.mean(), color="red", linestyle="--",
               label=f"平均 {lengths.mean():.0f} 字")
    ax.set_xlabel("评论长度（>200 字截断显示）")
    ax.set_ylabel("评论数")
    ax.legend()
    st.pyplot(fig)
    st.info("💡 观察：哪些一看就没有分析价值（纯数字、太短）？你觉得需要多长的最短长度过滤？")

# ================================================================ Part 1
elif page == "Part 1 分词":
    st.header("Part 1：分词——中文 NLP 的第一道坎")
    with st.expander("📖 原理速览：机器怎么知道在哪里切？", expanded=False):
        st.markdown(
            "**① 基于规则：最大匹配方法**——预定义词典 + 贪心切最长词。"
            "例：词典 {南京、南京市、市长、江、大桥、长江、长江大桥}，max_len=4，"
            "「南京市长江大桥」→ 南京市 / 长江大桥（也可能切成 南京市长 / 江大桥，这就是歧义）。\n\n"
            "**② 基于统计：统计切词法（语言模型）**——比较各种切法哪个更可能出现，"
            "选联合概率 p(w₁,…,wₙ) 最大的切分。\n\n"
            "**jieba = 两种思路的结合**：前缀词典找出所有切分位置 → 构造 DAG → "
            "动态规划取最大概率路径。")

    text = st.text_input("输入一句股评试试", "利好茅台，明天加仓稳稳的幸福")
    init_jieba()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**① 不加载自定义词典（jieba 默认词典）**")
        default_tok = jieba.Tokenizer()   # 新建一个未加载 userdict 的分词器
        st.code(" / ".join(default_tok.lcut(text)), language=None)
    with col2:
        st.markdown("**② 加载金融自定义词典 userdict.txt 后**")
        jieba.load_userdict(str(DATA_DIR / "userdict.txt"))
        st.code(" / ".join(jieba.lcut(text)), language=None)

    st.info("💡 观察：加载 userdict.txt 前后，「加仓」「稳稳」等金融/网络用语被正确切出了吗？")

    st.subheader("从真实数据抽 3 条检查分词质量")
    if st.button("🎲 换一批"):
        st.session_state["p1_seed"] = st.session_state.get("p1_seed", 42) + 1
    sample_seed = st.session_state.get("p1_seed", 42)
    for c in load_comments()["text"].sample(3, random_state=sample_seed):
        st.markdown(f"- {c}")
        st.caption(" / ".join(jieba.lcut(c)))
    st.warning("✍️ 记录：找出至少 1 条分词分错的评论（思考题要用）。")

# ================================================================ Part 2
elif page == "Part 2 停用词 + 词频":
    st.header("Part 2：停用词 + 词频统计")
    st.markdown(
        f"使用**哈工大停用词表**（{len(load_stopwords())} 词），"
        "去掉「的、了、是、吗」这类出现最多但对分析没用的词。"
        f"当前样本 **{len(df):,} 条**。")

    top_n = st.slider("Top N", 10, 50, 20)
    top = freq.most_common(top_n)
    labels, counts = zip(*top)

    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.28)))
    ax.barh(range(len(labels))[::-1], counts, color="#4C78A8")
    ax.set_yticks(range(len(labels))[::-1], labels)
    ax.set_title(f"股评高频词 Top {top_n}")
    st.pyplot(fig)
    st.info("💡 观察：哪些词反映了股民情绪？哪些词其实还是噪音（该加进停用词表）？")

# ================================================================ Part 3
elif page == "Part 3 词典法情感打分":
    st.header("Part 3：情感词典打分——词典法完整流程")
    pos_words = load_words("zhang_unformal_pos.txt")
    neg_words = load_words("zhang_unformal_neg.txt")
    st.markdown(
        f"**规则**：score = 正面词数 − 负面词数（正面词表 {len(pos_words)} 个，"
        f"负面词表 {len(neg_words)} 个）。score > 0 记正面，< 0 记负面，= 0 记中性。")

    dist = df["label"].value_counts(normalize=True).round(3)
    c1, c2, c3 = st.columns(3)
    c1.metric("正面", f"{dist.get('正面', 0):.1%}")
    c2.metric("中性", f"{dist.get('中性', 0):.1%}")
    c3.metric("负面", f"{dist.get('负面', 0):.1%}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("情感分数分布")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(df["score"], bins=range(-5, 7), color="#4C78A8", align="left")
        ax.set_xlabel("score")
        ax.set_ylabel("评论数")
        st.pyplot(fig)
    with col2:
        st.subheader("最正面 / 最负面的评论")
        st.dataframe(df.nlargest(3, "score")[["text", "score"]],
                     width="stretch")
        st.dataframe(df.nsmallest(3, "score")[["text", "score"]],
                     width="stretch")

    st.warning("词典法跑通了，但它有天花板（想想反讽）。下一步用 LLM 分析同样的评论比一比。")

# ================================================================ Part 4
elif page == "Part 4 LLM 情感分析":
    st.header("Part 4：接入大模型做情感分析——LLM 法")
    st.markdown(
        "词典法是「查表打分」，LLM 法是把文本**发给大模型**、让它像人一样读懂再判断。"
        "这里用 `openai` 工具包以 API 形式接入 DeepSeek（OpenAI 兼容接口）。\n\n"
        "> **成本考虑**：只发 **10 条**评论做示例——10 条短评论成本不到 1 分钱；"
        "12 万条全量既烧钱又可能触发限流。工程习惯：**先小样本验证逻辑，再决定全量的性价比**。")

    api_key = load_api_key()

    if not api_key:
        st.error("未找到 DEEPSEEK_API_KEY：请配置 week09/.env 或仓库根目录 .env"
                 "（见 llm-key-guide.md）")
    else:
        if st.button("🚀 调用 DeepSeek 分析 10 条评论"):
            from openai import OpenAI

            with st.spinner("请求 DeepSeek 中…"):
                client = OpenAI(
                    base_url="https://api.deepseek.com",
                    api_key=api_key,
                )
                sample10 = (df_all[["text"]].sample(10, random_state=42)
                            .reset_index(drop=True))
                # 用词典法（Part 3 的规则）先打分，方便并排对比
                pos_words = load_words("zhang_unformal_pos.txt")
                neg_words = load_words("zhang_unformal_neg.txt")

                def _score(t):
                    ws = init_jieba().lcut(t)
                    return (sum(w in pos_words for w in ws)
                            - sum(w in neg_words for w in ws))

                sample10["score"] = sample10["text"].apply(_score)
                sample10["label"] = sample10["score"].apply(
                    lambda s: "正面" if s > 0 else ("负面" if s < 0 else "中性"))

                system_prompt = """你是金融文本情感分析助手。对给出的每条股吧评论判断情感倾向：
- 正面：看多、乐观、买入意愿
- 中性：陈述事实、提问、无明显情感
- 负面：看空、抱怨、悲观、反讽

注意反讽和网络用语（如"利好"可能是反讽）。只输出 JSON，不要输出其他内容，格式：
{"results": [{"id": 0, "label": "正面", "reason": "一句话理由"}, ...]}"""
                user_prompt = "评论列表：\n" + "\n".join(
                    f"{i}. {t}" for i, t in enumerate(sample10["text"]))

                completion = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0,
                )

            raw = completion.choices[0].message.content
            st.caption("模型原始返回：")
            st.code(raw, language="json")
            try:
                import json
                cleaned = raw.strip()
                if cleaned.startswith("```"):          # 剥掉 ```json 围栏
                    cleaned = cleaned.strip("`").lstrip("json").strip()
                results = json.loads(cleaned)["results"]
                sample10["llm_label"] = [r["label"] for r in results]
                sample10["llm_reason"] = [r["reason"] for r in results]
                st.dataframe(
                    sample10[["text", "label", "llm_label", "llm_reason"]],
                    width="stretch")
                agree = (sample10["label"] == sample10["llm_label"]).mean()
                st.metric("两种方法一致率", f"{agree:.0%}")
            except Exception as e:
                st.warning(f"解析失败（{e}）；temperature=0 下通常很稳定，重试即可。")

        st.markdown(
            "**对比记录**（提交物）：判不一致的评论、能否识别反讽、成本与速度"
            "（词典法免费毫秒级可跑 12 万条 vs LLM 约 1 分钱/10 条）。")

# ================================================================ Part 5
elif page == "Part 5 每日情感分数":
    st.header("Part 5：每日情感分数——把文本变成情绪指数")
    st.markdown(
        "**当日情感分数 = 当天正面评论数 − 当天负面评论数**。"
        "这就是一个从股吧文本「算」出来的情绪指数。")

    c1, c2, c3, c4 = st.columns(4)
    s = daily["sentiment"]
    c1.metric("有评论的交易日", f"{len(daily):,}")
    c2.metric("日均情感分数", f"{s.mean():.2f}")
    c3.metric("最悲观一天", f"{s.idxmin()}（{s.min():.0f}）")
    c4.metric("最乐观一天", f"{s.idxmax()}（{s.max():.0f}）")

    win = st.slider("滑动平均窗口（日）", 5, 90, 30)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(daily.index, daily["sentiment"], alpha=0.4, label="每日情感分数")
    ax.plot(daily.index, daily["sentiment"].rolling(win, center=True).mean(),
            linewidth=2, label=f"{win} 日滑动平均")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_title("股吧每日情感分数（正面评论数 - 负面评论数）")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

    extreme_day = st.date_input("查看某一天的股民在吵什么：", value=s.idxmin())
    day_df = df[df["date"].dt.date == extreme_day]
    st.dataframe(day_df[["text", "score"]].head(20), width="stretch")
    st.info("💡 隐患：这个「分数」受当天评论量影响——评论越多的日子，|正面−负面| 天然越大。"
            "怎么改更公平？（提示：除以当天评论总数；放进思考题）")

# ================================================================ Part 6
elif page == "Part 6 情绪 vs 股价":
    st.header("Part 6：情绪与股价——相关系数")
    st.markdown(
        "金融文本分析的经典问题：**股吧情绪和股价涨跌幅有关系吗？**"
        "（用 inner join 对齐：周末和节假日发评论没有对应行情，自动剔除）")

    price = load_price()
    merged = daily.reset_index().merge(
        price[["day", "close", "pct_chg"]],
        left_on="date", right_on="day", how="inner")

    r_same = merged["sentiment"].corr(merged["pct_chg"])
    r_next = merged["sentiment"].corr(merged["pct_chg"].shift(-1))
    r_spearman = merged["sentiment"].corr(merged["pct_chg"], method="spearman")

    c1, c2, c3 = st.columns(3)
    c1.metric("当日情绪 vs 当日涨跌幅", f"r = {r_same:.3f}")
    c2.metric("当日情绪 vs 次日涨跌幅", f"r = {r_next:.3f}")
    c3.metric("Spearman（抗极端值）", f"r = {r_spearman:.3f}")
    st.caption(f"匹配到 {len(merged):,} 个交易日　|　"
               "解读标尺：|r|<0.1 几乎不相关；0.1–0.3 弱；0.3–0.5 中等；>0.5 强")

    col1, col2 = st.columns([3, 2])
    with col1:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(merged["sentiment"], merged["pct_chg"], alpha=0.3, s=10)
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.set_xlabel("每日情感分数（正面数 - 负面数）")
        ax.set_ylabel("当日涨跌幅 (%)")
        ax.set_title(f"股吧情绪 vs 当日涨跌幅（r = {r_same:.3f}）")
        st.pyplot(fig)
    with col2:
        st.markdown("**观察**\n"
                    "1. 当日相关 vs 次日相关谁大？当日明显更强 → 情绪更像涨跌的「果」不是「因」\n"
                    "2. 2011-08-03 上市首日 pct_chg = +40.95% 是极端值——对比 Spearman 看它的影响\n"
                    "3. **相关 ≠ 因果**：可能是股价推动情绪，也可能两者都被大盘、消息面驱动")

st.sidebar.divider()
st.sidebar.caption("数据：光线传媒(300251) 股吧评论 + tushare 日线行情")
