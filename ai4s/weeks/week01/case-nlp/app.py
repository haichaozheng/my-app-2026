# -*- coding: utf-8 -*-
"""
Week 01 NLP 上机实验 · 课堂展示版（Streamlit）
对应实验文档：week01-nlp-lab.ipynb

运行方式（在 week01/case-nlp/ 目录下）：
    streamlit run app.py

数据文件与本脚本同目录（case-nlp/），无需复制。
全量双标签（jieba_score / llm_score）由 llm_jieba_score.py 生成
→ cleaned_300251_comments_scored.csv。
"""
from pathlib import Path

import jieba
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from collections import Counter

# ---------------------------------------------------------------- 基础配置
DATA_DIR = Path(__file__).resolve().parent   # case-nlp/（数据与本脚本同目录）
st.set_page_config(page_title="Week01 NLP 实验展示", page_icon="📊", layout="wide")

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

LABELS = ["正面", "中性", "负面"]


def _clean(text) -> str:
    """把 \r\n 和连续空白压成单个空格"""
    return " ".join(text.split()) if isinstance(text, str) else ""


# ---------------------------------------------------------------- 缓存加载
@st.cache_data(show_spinner="读取评论数据…")
def load_comments() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "cleaned_300251_comments.csv", parse_dates=["date"])
    df["text"] = df["comment"].apply(_clean)
    df = df[df["text"] != ""].reset_index(drop=True)
    return df


@st.cache_data(show_spinner="读取全量双标签数据…")
def load_scored() -> pd.DataFrame | None:
    """全量 124,126 条 + jieba_score / llm_score 双标签。
    src_row = 原 csv 数据行号（0-based），保证与原始文件逐行对齐。"""
    path = DATA_DIR / "cleaned_300251_comments_scored.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=["date"])
    df.insert(0, "src_row", range(len(df)))
    df["text"] = df["comment"].apply(_clean)
    df = df[df["text"] != ""].reset_index(drop=True)
    return df


def require_scored() -> pd.DataFrame:
    """取双标签数据；缺失或有未标注行时给出明确提示（失败就是失败，绝不填充）"""
    sc = load_scored()
    if sc is None:
        st.error("未找到 cleaned_300251_comments_scored.csv——"
                 "先在本目录运行 `python llm_jieba_score.py` 生成全量双标签数据。")
        st.stop()
    miss = int(sc["llm_score"].isna().sum())
    if miss:
        st.warning(f"注意：LLM 有 {miss:,} 条未成功标注（失败行留空、绝不填充），"
                   "重新运行 llm_jieba_score.py 可自动补标。")
    return sc


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


def daily_by_label(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """按标签列聚合每日情绪（两种度量）：
    sentiment = 当天正面数 − 当天负面数（绝对差值，受评论量影响）
    ratio     = (正面 − 负面) / (当天评论数 + 1)（情绪比率，按量归一；
                分母 +1 平滑小样本日，也避免除零）"""
    daily = (df.groupby(df["date"].dt.date)[col]
               .value_counts()
               .unstack(fill_value=0)
               .reindex(columns=LABELS, fill_value=0))
    daily["total"] = daily[LABELS].sum(axis=1)
    daily["sentiment"] = daily["正面"] - daily["负面"]
    daily["ratio"] = daily["sentiment"] / (daily["total"] + 1)
    return daily


# ---------------------------------------------------------------- 侧边栏
st.sidebar.title("Week 01 · NLP 实验")
page = st.sidebar.radio(
    "实验环节",
    ["Part 0 读数据 + 清洗",
     "Part 1 分词",
     "Part 2 停用词 + 词频",
     "Part 3 词典法情感打分",
     "Part 4 LLM 情感分析",
     "Part 5 每日情感分数",
     "Part 6 情绪 vs 股价波动幅度",
     "Part 7 情绪 vs 次日涨跌（0/1）",
     "Part 8 情绪 vs 未来收益率"],
)
st.sidebar.caption("对应实验文档 week01-nlp-lab.ipynb")

df_all = load_comments()
n = st.sidebar.slider("抽样评论数（仅 Part 2/3 使用）",
                      min_value=2000, max_value=len(df_all),
                      value=min(30000, len(df_all)), step=1000)
seed = st.sidebar.number_input("随机种子", value=42, step=1)
st.sidebar.caption(
    "为什么 Part 2/3 要抽样？全量 12.4 万条分词约 2–3 分钟，"
    "抽 3 万条几秒出结果、词频结论基本一致（算过一次就有缓存）。"
    "想看全量把滑杆拉满即可。Part 4–7 永远用全量 124,126 条，不受滑杆影响。")

if page in ("Part 2 停用词 + 词频", "Part 3 词典法情感打分"):
    df, freq = compute_pipeline(int(n), int(seed))

# ================================================================ Part 0
if page == "Part 0 读数据 + 清洗":
    st.header("Part 0：读数据 + 清洗")

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

    st.subheader("发帖时间规律：几点发？周几发？")
    dow_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    hrs = df_all["date"].dt.hour
    dow = df_all["date"].dt.dayofweek

    c1, c2 = st.columns(2)
    with c1:
        hc = hrs.value_counts().reindex(range(24), fill_value=0)
        fig, ax = plt.subplots(figsize=(6.5, 3))
        ax.bar(hc.index, hc.values, color="#4C78A8")
        ax.set_title("按小时：几点发评论？")
        ax.set_xlabel("小时（0–23）")
        ax.set_ylabel("评论数")
        ax.set_xticks(range(0, 24, 2))
        st.pyplot(fig)
        st.caption("💡 峰值集中在 9–11、13–14 点——正好是 A 股交易时段"
                   "（9:30–11:30、13:00–15:00），12 点午休明显低谷。"
                   "为什么行情时段发帖最多？")
    with c2:
        dc = dow.value_counts().reindex(range(7), fill_value=0)
        fig, ax = plt.subplots(figsize=(6.5, 3))
        ax.bar(dow_names, dc.values, color="#4C78A8")
        ax.set_title("按周几：周一到周日")
        ax.set_xlabel("周几")
        ax.set_ylabel("评论数")
        st.pyplot(fig)
        st.caption(f"💡 工作日每天约 {int(dc.iloc[:5].min()):,}–"
                   f"{int(dc.iloc[:5].max()):,} 条，"
                   f"周六周日只有约 {int(dc[5]):,} / {int(dc[6]):,} 条"
                   f"（合计仅 {((dc[5] + dc[6]) / dc.sum()):.1%}）——"
                   "休市日发帖骤减但没归零，周末股民在聊什么？")

    st.markdown("**分周几各自看：周一到周日每天 0–23 点的发帖形态**"
                "（每张图按当天评论总数归一成 %，消除周末总量小的干扰）")
    day_total = dow.value_counts().reindex(range(7), fill_value=0)
    rows_cols = [st.columns(4), st.columns(4)]
    for i, nm in enumerate(dow_names):
        with rows_cols[i // 4][i % 4]:
            sub = (hrs[dow == i].value_counts(normalize=True)
                   .reindex(range(24), fill_value=0) * 100)
            fig, ax = plt.subplots(figsize=(4.2, 2.6))
            ax.bar(sub.index, sub.values, color="#4C78A8")
            ax.set_title(f"{nm}（{int(day_total.loc[i]):,} 条）", fontsize=11)
            ax.set_xlabel("小时", fontsize=9)
            ax.set_ylabel("占当天评论 (%)", fontsize=9)
            ax.set_xticks(range(0, 24, 3))
            ax.tick_params(labelsize=8)
            st.pyplot(fig)
    st.caption("💡 观察：交易日的「开盘高峰」（9–11、13–14 点）在周六、周日"
               "还在吗？哪一天的盘中最活跃？这类「按小时/周几分组」正是 "
               "lab.md 第 2 部分改造 mini_emotion.py 的方向。")

# ================================================================ Part 1
elif page == "Part 1 分词":
    st.header("Part 1：分词")
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

    st.warning("词典法跑通了，但它有天花板（想想反讽）——Part 4 用大模型给全部 "
               "12.4 万条打了标，去比一比两法差在哪。")

# ================================================================ Part 4
elif page == "Part 4 LLM 情感分析":
    st.header("Part 4：大模型情感分析——全量 12.4 万条打标结果")
    st.markdown(
        "词典法是「查表打分」，LLM 法是把文本**发给大模型**、让它像人一样读懂再判断。"
        "本页展示 `llm_jieba_score.py` 对全部 **124,126 条**评论的真实打标结果："
        "模型 `Qwen/Qwen3.8-Flash-Next`（西财校园网关），temperature=0，"
        "单条截断 500 字，每批 20 条 × 10 并发。")

    sc = require_scored()

    # ---------- ① 两法分布对比 ----------
    st.subheader("① 两法标签分布对比")
    dist = pd.DataFrame({
        "词典法 jieba": (sc["jieba_score"].value_counts(normalize=True)
                       .reindex(LABELS) * 100),
        "大模型 LLM": (sc["llm_score"].value_counts(normalize=True)
                     .reindex(LABELS) * 100),
    })
    fig, ax = plt.subplots(figsize=(7, 3.2))
    x = range(len(LABELS))
    w = 0.35
    ax.bar([i - w / 2 for i in x], dist["词典法 jieba"], w,
           label="词典法 jieba", color="#4C78A8")
    ax.bar([i + w / 2 for i in x], dist["大模型 LLM"], w,
           label="大模型 LLM", color="#E45756")
    for i, v in enumerate(dist["词典法 jieba"]):
        ax.text(i - w / 2, v + 0.8, f"{v:.1f}%", ha="center", fontsize=9)
    for i, v in enumerate(dist["大模型 LLM"]):
        ax.text(i + w / 2, v + 0.8, f"{v:.1f}%", ha="center", fontsize=9)
    ax.set_xticks(list(x), LABELS)
    ax.set_ylabel("占比 (%)")
    ax.set_title("同一批 12.4 万条评论，两种方法的标签分布")
    ax.legend()
    st.pyplot(fig)
    st.caption("💡 词典法「中性」占比畸高——没命中情感词典的评论一律 0 分记中性；"
               "LLM 能读懂句子含义，把「没词但有情绪」的评论判成了负面。")

    # ---------- ② 一致率 + 混淆矩阵 ----------
    st.subheader("② 两法一致率与混淆矩阵")
    agree = (sc["jieba_score"] == sc["llm_score"]).mean()
    diff_n = int((sc["jieba_score"] != sc["llm_score"]).sum())
    cm = (pd.crosstab(sc["jieba_score"], sc["llm_score"])
            .reindex(index=LABELS, columns=LABELS, fill_value=0))
    top_combo = (pd.Series({f"{a} → {b}": cm.loc[a, b]
                            for a in LABELS for b in LABELS if a != b})
                 .sort_values(ascending=False))

    c1, c2, c3 = st.columns(3)
    c1.metric("两法一致率", f"{agree:.1%}",
              help="三类均匀乱猜的期望一致率约 33%，52% 显著高于随机")
    c2.metric("分歧条数", f"{diff_n:,} 条",
              help="同一个词典、同一个模型，为什么会有这么多分歧？")
    c3.metric("最大分歧组合", top_combo.index[0],
              help=f"{top_combo.iloc[0]:,} 条")

    col1, col2 = st.columns([3, 2])
    with col1:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        ax.imshow(cm.values, cmap="Blues")
        ax.set_xticks(range(3), cm.columns)
        ax.set_yticks(range(3), cm.index)
        ax.set_xlabel("LLM 标签")
        ax.set_ylabel("jieba 标签")
        vmax = cm.values.max()
        for i in range(3):
            for j in range(3):
                v = int(cm.values[i, j])
                ax.text(j, i, f"{v:,}\n{v / cm.values.sum():.1%}",
                        ha="center", va="center", fontsize=9,
                        color="white" if v > vmax * 0.6 else "black")
        ax.set_title("混淆矩阵（对角线 = 两法一致）")
        st.pyplot(fig)
    with col2:
        st.markdown("**怎么读**\n"
                    "1. **对角线**：两法判一致的评论\n"
                    "2. **最亮的非对角格**：系统性分歧所在——词典法判中性、"
                    "LLM 判负面，正是「没词但有情绪」的那批评论\n"
                    "3. 分歧不是谁「错了」，而是**两种方法对情绪的定义不同**"
                    "（词典命中 vs 句子理解）")

    # ---------- ③ 点选矩阵单元格看评论 ----------
    st.subheader("③ 点击矩阵单元格，看这一格里的评论")
    st.caption("下面是混淆矩阵的「可点击版」（数字 = 该格评论数，对角线也行）。"
               "点任意一格，下方随机展示该格的 5 条原文——"
               "完成实验交付「各找 1-2 条分歧例句」")

    # 默认选中「最大的分歧格」（对角线以外最大的一格）
    if "p4_cell" not in st.session_state:
        best = max(((int(cm.loc[a, b]), a, b)
                    for a in LABELS for b in LABELS if a != b),
                   key=lambda t: t[0])
        st.session_state["p4_cell"] = (best[1], best[2])

    def _pick_cell(cell):
        # 回调在脚本重跑前执行，选中态当轮即生效
        st.session_state["p4_cell"] = cell

    # 表头（列 = LLM 标签，方向与上方热力图一致）
    hdr = st.columns([1.2, 1, 1, 1])
    hdr[0].markdown("**jieba ＼ LLM**")
    for j, b in enumerate(LABELS):
        hdr[j + 1].markdown(f"**{b}**")
    # 3×3 可点击矩阵（行 = jieba 标签）
    for a in LABELS:
        grid_row = st.columns([1.2, 1, 1, 1])
        grid_row[0].markdown(f"**{a}**")
        for j, b in enumerate(LABELS):
            cnt = int(cm.loc[a, b])
            is_sel = st.session_state["p4_cell"] == (a, b)
            grid_row[j + 1].button(
                f"{'👉 ' if is_sel else ''}{cnt:,}",
                key=f"p4cell_{a}_{b}",
                on_click=_pick_cell, args=((a, b),),
                type="primary" if is_sel else "secondary",
                use_container_width=True)

    a, b = st.session_state["p4_cell"]
    subset = sc[(sc["jieba_score"] == a) & (sc["llm_score"] == b)]
    if st.button("🎲 换一批", key="p4_resample"):
        st.session_state["p4_seed"] = st.session_state.get("p4_seed", 42) + 1
    p4_seed = st.session_state.get("p4_seed", 42)
    st.markdown(f"**jieba「{a}」→ LLM「{b}」**：共 {len(subset):,} 条，"
                f"随机展示 {min(5, len(subset))} 条")
    if subset.empty:
        st.caption("这一格没有评论。")
    for _, srow in subset.sample(min(5, len(subset)),
                                 random_state=p4_seed).iterrows():
        st.markdown(f"> {srow['text']}")
        st.caption(f"jieba：{srow['jieba_score']}　|　LLM：{srow['llm_score']}")

    # ---------- ④ 标注工程侧写 ----------
    with st.expander("⚙️ 这份全量标签是怎么跑出来的（工程侧写）"):
        st.markdown(
            "- **模型**：`Qwen/Qwen3.8-Flash-Next`，走校园网关 "
            "`llm.swufe.edu.cn`，`temperature=0` 保证可复现，关闭思考模式提速\n"
            "- **批量**：每批 20 条评论 × 10 线程并发，约 160 条/分；"
            "全量 124,126 条约 9.5 小时（网关白天拥堵、夜间快）\n"
            "- **断点续跑**：每批结果实时写 `llm_labels_checkpoint.csv`，"
            "中断/断网后重跑自动跳过已标注的行\n"
            "- **失败就是失败**：标注失败的行**绝不填充**任何标签（宁可留空），"
            "重跑会自动补标——本次最终 0 条未标注\n"
            "- 对应脚本：`llm_jieba_score.py`，可先 `--limit 100` 小样本验证再全量")

    st.info("✍️ **对比记录**（提交物）：挑 2-3 条分歧评论，写清两法为什么判不同；"
            "思考：词典法免费毫秒级、LLM 要调 API——各自的适用边界在哪？")

# ================================================================ Part 5
elif page == "Part 5 每日情感分数":
    st.header("Part 5：每日情感分数——把文本变成情绪指数")
    st.markdown(
        "**当日情感分数 = 当天正面评论数 − 当天负面评论数**。"
        "这就是一个从股吧文本「算」出来的情绪指数。"
        "（使用全量 124,126 条，不受侧边栏抽样数影响）")

    sc = require_scored()
    cal = st.radio("情绪口径", ["jieba（词典法）", "LLM（大模型）"],
                   horizontal=True)
    meas = st.radio("情绪度量",
                    ["差值（正面−负面）",
                     "比率（正面−负面）/（评论数+1）"],
                    horizontal=True)
    col = "jieba_score" if cal.startswith("jieba") else "llm_score"
    metric_col = "sentiment" if meas.startswith("差值") else "ratio"
    fmt = "{:.2f}" if metric_col == "sentiment" else "{:.4f}"
    daily = daily_by_label(sc, col)

    c1, c2, c3, c4 = st.columns(4)
    s = daily[metric_col]
    c1.metric("有评论的交易日", f"{len(daily):,}")
    c2.metric("日均情绪" + ("差值" if metric_col == "sentiment" else "比率"),
              fmt.format(s.mean()))
    c3.metric("最悲观一天", f"{s.idxmin()}（{fmt.format(s.min())}）")
    c4.metric("最乐观一天", f"{s.idxmax()}（{fmt.format(s.max())}）")

    win = st.slider("滑动平均窗口（日）", 5, 90, 30)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(daily.index, s, alpha=0.4, label="每日情绪")
    ax.plot(daily.index, s.rolling(win, center=True).mean(),
            linewidth=2, label=f"{win} 日滑动平均")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_title(f"股吧每日情绪（{cal} · {meas}）")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

    with st.expander("🔬 两种口径叠加对比（同一批文本，两条情绪曲线）"):
        fig2, ax2 = plt.subplots(figsize=(12, 4))
        for name, c in [("词典法 jieba", "jieba_score"),
                        ("大模型 LLM", "llm_score")]:
            d = daily_by_label(sc, c)
            ax2.plot(d.index, d[metric_col], alpha=0.6, label=name)
        ax2.axhline(0, color="gray", linewidth=0.8)
        ax2.set_title(f"每日情绪：两种口径（{meas}）")
        ax2.legend()
        fig2.autofmt_xdate()
        st.pyplot(fig2)
        st.caption("💡 两条曲线走势相近但幅度不同——LLM 的负面判定更多，"
                   "分歧集中在哪？切回 Part 4 看混淆矩阵。")

    extreme_day = st.date_input("查看某一天的股民在吵什么：", value=s.idxmin())
    day_df = sc[sc["date"].dt.date == extreme_day]
    st.dataframe(day_df[["text", col]].head(20), width="stretch")
    st.info("💡 **思考题**：「差值」受当天评论量影响——评论越多的日子，|正面−负面| 天然越大；"
            "切到「比率」口径就是改进版（除以评论数+1 归一）。"
            "再想：分母为什么要 +1？（提示：小样本日平滑、防止除零）。"
            "→ 想知道改了以后差别多大？去 Part 6 看相关系数的变化。")

# ================================================================ Part 6
elif page == "Part 6 情绪 vs 股价波动幅度":
    st.header("Part 6：情绪 vs 股价波动幅度")
    st.markdown(
        "金融文本分析的经典问题：**股吧情绪和股价波动幅度有关系吗？**"
        "（用 inner join 对齐：周末和节假日发评论没有对应行情，自动剔除）")

    sc = require_scored()
    price = load_price()

    cal_list = [("词典法 jieba", "jieba_score"),
                ("大模型 LLM", "llm_score")]
    meas_list = [("差值", "sentiment"), ("比率", "ratio")]
    rows, merged_by_key = [], {}
    for cal_name, c in cal_list:
        m = (daily_by_label(sc, c).reset_index()
             .merge(price[["day", "close", "pct_chg"]],
                    left_on="date", right_on="day", how="inner"))
        for meas_name, mc in meas_list:
            key = f"{cal_name} · {meas_name}"
            merged_by_key[key] = (m, mc)
            rows.append({
                "口径 · 度量": key,
                "当日 ρ": m[mc].corr(m["pct_chg"], method="spearman"),
                "次日 ρ": m[mc].corr(m["pct_chg"].shift(-1),
                                     method="spearman"),
            })
    table = pd.DataFrame(rows).set_index("口径 · 度量")
    st.subheader("两种口径 × 两种度量 × Spearman 相关系数")
    st.dataframe(table.style.format("{:.3f}"), width="stretch")
    st.caption("全部为 Spearman ρ（秩相关，抗极端值——上市首日 +40.95% "
               "这类极端值撬不动名次，故不报告皮尔森、不用移动平均）。"
               "解读标尺：|ρ|<0.1 几乎不相关；0.1–0.3 弱；0.3–0.5 中等；>0.5 强"
               "　|　行 = 情绪怎么算（差值 = 正面−负面，比率 = (正面−负面)/(评论数+1)）")

    key = st.radio("散点图：口径 · 度量", list(merged_by_key),
                   horizontal=True)
    merged, mc = merged_by_key[key]
    series = merged[mc]
    nxt = merged["pct_chg"].shift(-1)
    r_same = series.corr(merged["pct_chg"], method="spearman")
    r_next = series.corr(nxt, method="spearman")

    c1, c2 = st.columns(2)
    c1.metric("情绪 vs 当日涨跌幅（Spearman ρ）", f"ρ = {r_same:.3f}")
    c2.metric("情绪 vs 次日涨跌幅（Spearman ρ）", f"ρ = {r_next:.3f}")
    st.caption(f"匹配到 {len(merged):,} 个交易日（{key}）——"
               "本页所有相关系数均为 Spearman ρ，不报告皮尔森")

    j_diff = table.loc["词典法 jieba · 差值", "当日 ρ"]
    j_ratio = table.loc["词典法 jieba · 比率", "当日 ρ"]
    l_diff = table.loc["大模型 LLM · 差值", "当日 ρ"]
    l_ratio = table.loc["大模型 LLM · 比率", "当日 ρ"]
    r_same_max = table["当日 ρ"].max()
    r_next_max = table["次日 ρ"].max()

    chart1, chart2 = st.columns(2)
    with chart1:
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        ax.scatter(series, merged["pct_chg"], alpha=0.3, s=10)
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.set_xlabel(f"每日情绪（{key}）")
        ax.set_ylabel("当日涨跌幅 (%)")
        ax.set_title(f"当日情绪 → 当日涨跌幅（ρ = {r_same:.3f}）")
        st.pyplot(fig)
    with chart2:
        pair = pd.DataFrame({"x": series, "y": nxt}).dropna()
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        ax.scatter(pair["x"], pair["y"], alpha=0.3, s=10)
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.set_xlabel(f"每日情绪（{key}）")
        ax.set_ylabel("次日涨跌幅 (%)")
        ax.set_title(f"当日情绪 → 次日涨跌幅（ρ = {r_next:.3f}）")
        st.pyplot(fig)
        st.caption("次日 = 匹配样本中的下一条交易日记录，最后一天无配对自动剔除；"
                   "图中标注的也是 Spearman ρ")

    st.markdown(
        "**观察（本数据实测结论，均为 Spearman ρ）**\n"
        f"1. **当日 ≫ 次日**：当日 ρ 最高 {r_same_max:.3f}"
        "（左图「立得起来」），次日最高仅 "
        f"{r_next_max:.3f}（右图一团散云）——情绪几乎预测不了明天，"
        "更像涨跌的「果」不是「因」\n"
        f"2. **差值里有评论量的水分**：jieba 口径当日 ρ 从 "
        f"差值 {j_diff:.3f} → 比率 {j_ratio:.3f}——放量的日子涨跌也大，"
        "差值天然被评论量撑大，除以评论数归一后挤掉的才是真实相关；"
        f"LLM 口径几乎不变（{l_diff:.3f} → {l_ratio:.3f}），日度信号更干净\n"
        "3. **为什么全用 Spearman**：2011-08-03 上市首日 "
        "pct_chg = +40.95% 这类极端值会把皮尔森相关带偏，"
        "秩相关只看名次、抗极端值——所以本页不报告皮尔森\n"
        "4. **换口径看**：jieba 与 LLM 的 ρ 并不相同——情绪的「测法」"
        "本身会影响结论\n"
        "5. **相关 ≠ 因果**：可能是股价推动情绪，也可能两者都被大盘、"
        "消息面驱动")

# ================================================================ Part 7
elif page == "Part 7 情绪 vs 次日涨跌（0/1）":
    st.header("Part 7：情绪 vs 次日涨跌（0/1）")
    st.markdown(
        "Part 6 用相关系数问「情绪和明天涨*多少*有关吗」，本页换一个更贴近"
        "交易的问法：**明天涨还是跌？**——把次日涨跌幅二值化"
        "（涨 = 1，跌/平 = 0），把情绪当作预测特征，"
        "用**分组检验**评估它到底有没有预测力："
        "按情绪从低到高分五组，看明天上涨比例会不会一路抬升。")

    sc = require_scored()
    price = load_price()

    cal = st.radio("情绪口径", ["jieba（词典法）", "LLM（大模型）"],
                   horizontal=True)
    meas = st.radio("情绪度量",
                    ["差值（正面−负面）",
                     "比率（正面−负面）/（评论数+1）"],
                    horizontal=True)
    col = "jieba_score" if cal.startswith("jieba") else "llm_score"
    mc = "sentiment" if meas.startswith("差值") else "ratio"

    m = (daily_by_label(sc, col).reset_index()
         .merge(price[["day", "pct_chg"]], left_on="date", right_on="day",
                how="inner"))
    m["pct_next"] = m["pct_chg"].shift(-1)      # 下一交易日涨跌幅
    m = (m.assign(s=m[mc])
           .dropna(subset=["pct_next", "s"])
           .reset_index(drop=True))
    m["y"] = (m["pct_next"] > 0).astype(int)    # 1=次日涨，0=次日跌/平
    n, n1 = len(m), int(m["y"].sum())
    base = n1 / n

    # ---------- 指标总览 ----------
    c1, c2 = st.columns(2)
    c1.metric("可配对交易日", f"{n:,}")
    c2.metric("次日上涨基准率", f"{base:.1%}",
              help="红虚线：全体交易日中次日上涨的占比，"
                   "分组比例甩开它才算有信息")

    # ---------- 分位数组间命中率 ----------
    st.subheader("分位数组间命中率——情绪越高，明天越涨吗？")
    grp = pd.qcut(m["s"].rank(method="first"), 5,
                  labels=["Q1 最悲观", "Q2", "Q3", "Q4", "Q5 最乐观"])
    g = (m.assign(grp=grp).groupby("grp", observed=True)
           .agg(天数=("y", "size"),
                次日上涨比例=("y", "mean"),
                次日平均涨跌幅=("pct_next", "mean")))
    spread = (g["次日上涨比例"].iloc[-1] - g["次日上涨比例"].iloc[0]) * 100
    mono = bool(g["次日上涨比例"].is_monotonic_increasing)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.bar(g.index.astype(str), g["次日上涨比例"] * 100,
               color="#4C78A8")
        ax.axhline(base * 100, color="red", linestyle="--",
                   label=f"基准率 {base:.1%}")
        ax.set_ylabel("次日上涨比例 (%)")
        ax.set_title("按情绪从低到高分五组：明天上涨的比例")
        ax.legend()
        st.pyplot(fig)
    with col2:
        st.dataframe(
            g.style.format({"天数": "{:,}",
                            "次日上涨比例": "{:.1%}",
                            "次日平均涨跌幅": "{:.3f}"}),
            width="stretch")
    st.caption(
        f"💡 五组上涨比例从 {g['次日上涨比例'].iloc[0]:.1%} 到 "
        f"{g['次日上涨比例'].iloc[-1]:.1%}（Q5−Q1 = {spread:+.1f} 个百分点），"
        + ("随情绪单调上升，有一点看头；" if mono else "并不随情绪单调上升；")
        + f"基准率是 {base:.1%}。若情绪真有预测力，"
          "应该 Q1→Q5 一路抬升、明显甩开红线。")

    # ---------- 结论 ----------
    obs = [
        f"1. **分组不抬升**：情绪从最悲观到最乐观，次日上涨比例 "
        f"{g['次日上涨比例'].iloc[0]:.1%} → "
        f"{g['次日上涨比例'].iloc[-1]:.1%}"
        f"（Q5−Q1 = {spread:+.1f} 个百分点），"
        + ("方向对但幅度很小" if mono else "并不单调"),
        f"2. **甩不开基准**：五组在基准率 {base:.1%} 上下浮动——"
        "若情绪真有预测力，应该 Q1→Q5 一路抬升、明显高出红线",
        "3. 与 Part 6 互证：次日 ρ ≈ 0、分组不抬升——"
        "**股吧情绪是涨跌的「果」，预测不了「因」**",
    ]
    st.markdown("**观察（本数据实测结论）**\n" + "\n".join(obs))

# ================================================================ Part 8
elif page == "Part 8 情绪 vs 未来收益率":
    st.header("Part 8：情绪 vs 未来收益率（次日 / 次周 / 次月）")
    st.markdown(
        "把时间尺度拉长：**今天的股民情绪，能预测未来 1 天、"
        "1 周（5 个交易日）、1 个月（20 个交易日）的收益率吗？**"
        "收益率 = 未来收盘价 ÷ 今天收盘价 − 1；"
        "相关系数一律 Spearman ρ（抗极端值）。")

    sc = require_scored()
    price = load_price()

    cal = st.radio("情绪口径", ["jieba（词典法）", "LLM（大模型）"],
                   horizontal=True)
    meas = st.radio("情绪度量",
                    ["差值（正面−负面）",
                     "比率（正面−负面）/（评论数+1）"],
                    horizontal=True)
    col = "jieba_score" if cal.startswith("jieba") else "llm_score"
    mc = "sentiment" if meas.startswith("差值") else "ratio"

    m = (daily_by_label(sc, col).reset_index()
         .merge(price[["day", "close", "pct_chg"]], left_on="date",
                right_on="day", how="inner"))
    horizons = {"次日（1 个交易日）": 1,
                "次周（5 个交易日）": 5,
                "次月（20 个交易日）": 20}
    for name, k in horizons.items():
        m[f"ret_{k}"] = m["close"].shift(-k) / m["close"] - 1

    # ---------- 相关系数表 ----------
    rows = []
    for name, k in horizons.items():
        sub = m[[mc, f"ret_{k}"]].dropna()
        rows.append({
            "未来收益": name,
            "Spearman ρ": sub[mc].corr(sub[f"ret_{k}"], method="spearman"),
            "样本数": len(sub),
        })
    table8 = pd.DataFrame(rows).set_index("未来收益")
    st.subheader("情绪与未来收益率的 Spearman 相关系数")
    st.dataframe(table8.style.format({"Spearman ρ": "{:.3f}",
                                      "样本数": "{:,}"}),
                 width="stretch")
    st.caption("解读标尺：|ρ|<0.1 几乎不相关；0.1–0.3 弱；0.3–0.5 中等；>0.5 强"
               "　|　次周/次月的收益窗口相互重叠（相邻样本共享 4 / 19 个"
               "交易日），样本并不独立，解读时要留一分余地")

    # ---------- 三张散点图 ----------
    chart_cols = st.columns(3)
    r_vals = {}
    for i, (name, k) in enumerate(horizons.items()):
        sub = m[[mc, f"ret_{k}"]].dropna()
        rho = sub[mc].corr(sub[f"ret_{k}"], method="spearman")
        r_vals[name] = rho
        with chart_cols[i]:
            fig, ax = plt.subplots(figsize=(4.6, 4))
            ax.scatter(sub[mc], sub[f"ret_{k}"] * 100, alpha=0.3, s=10)
            ax.axhline(0, color="gray", linewidth=0.8)
            ax.set_xlabel(f"当日情绪（{cal} · {meas}）", fontsize=9)
            ax.set_ylabel("未来收益率 (%)")
            ax.set_title(f"{name}（ρ = {rho:.3f}）", fontsize=11)
            ax.tick_params(labelsize=8)
            st.pyplot(fig)

    # ---------- 结论 ----------
    r_d = r_vals["次日（1 个交易日）"]
    r_w = r_vals["次周（5 个交易日）"]
    r_m = r_vals["次月（20 个交易日）"]
    r_same = m[mc].corr(m["pct_chg"], method="spearman")
    worst = max(abs(r_d), abs(r_w), abs(r_m))
    obs = [
        f"1. **三个期限都贴着 0**：次日 ρ = {r_d:+.3f}、"
        f"次周 ρ = {r_w:+.3f}、次月 ρ = {r_m:+.3f}"
        f"——|ρ| 最大只有 {worst:.3f}，按上方标尺全属「几乎不相关」",
        f"2. **对照当天**：同一口径下当日情绪 vs 当日涨跌幅 "
        f"ρ = {r_same:.3f}（Part 6 同款数字），对未来任何期限却只剩 "
        f"|ρ| ≤ {worst:.3f}——情绪是当天行情的「果」，跨期没有预测力",
        (f"3. **次月出现明显的负号**：ρ = {r_m:+.3f}——情绪高涨之后"
         "未来一个月反而略跌，有点「均值回复」的影子；但 |ρ|<0.1 很弱，"
         "且收益窗口重叠、样本不独立，只能当线索不能当结论"
         if r_m < 0 else
         f"3. **次月 ρ = {r_m:+.3f}**：|ρ| < 0.1，同样没有可用信号"),
        "4. **相关 ≠ 因果**：也别急着反着用（情绪高就卖）——"
        "微弱相关 + 重叠样本，离可交易的规律还很远",
    ]
    st.markdown("**观察（本数据实测结论）**\n" + "\n".join(obs))

st.sidebar.divider()
st.sidebar.caption("数据：光线传媒(300251) 股吧评论 + tushare 日线行情")
