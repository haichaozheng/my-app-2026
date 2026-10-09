"""
股吧评论文本分析 APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对应 notebook: weeks/week08/text_data_processing_1.ipynb
功能：选择时间区间 → jieba 切词 → 词典法情感分析 → Plotly 可视化

数据：光线传媒(300251) 东方财富股吧评论，124K 条（2011-2019）
来源：../../week06/cleaned_300251_comments.csv

运行：streamlit run app.py
"""

import re
from collections import Counter
from pathlib import Path

import jieba
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── 路径 ──
CASES_DIR = Path(__file__).parent
DATA_PATH = CASES_DIR.parent.parent / "week06" / "cleaned_300251_comments.csv"
USERDICT_PATH = CASES_DIR / "userdict.txt"
POS_WORDS_PATH = CASES_DIR / "zhang_unformal_pos.txt"
NEG_WORDS_PATH = CASES_DIR / "zhang_unformal_neg.txt"


# ══════════════════════════════════════════════════════
# 金融情感词表
# 对应 notebook 单元：pos_lst / neg_lst（英文示例）
# notebook 原文：
#   pos_lst = ['awesome','good','nice','super','fun','delightful']
#   neg_lst = ['awful', 'lame', 'horrible', 'bad', 'sorrow']
# 这里替换为中文金融场景词表，从外部文件加载。
# 词表来源：zhang_unformal_pos.txt / zhang_unformal_neg.txt
# ══════════════════════════════════════════════════════

def load_word_set(filepath: Path) -> set:
    """从文本文件加载词表，每行一个词"""
    if not filepath.exists():
        return set()
    with open(filepath, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


POSITIVE_WORDS = load_word_set(POS_WORDS_PATH)
NEGATIVE_WORDS = load_word_set(NEG_WORDS_PATH)


# ══════════════════════════════════════════════════════
# 函数：对应 notebook 各单元
# ══════════════════════════════════════════════════════

# 对应 notebook 单元：import jieba; jieba.lcut("我想去成都")
def tokenize(text: str) -> list:
    """jieba 切词，返回词列表（过滤空白）"""
    return [w for w in jieba.lcut(text) if w.strip()]


# 对应 notebook 单元：评论预处理
# notebook 原文提到 replace("\u3000"," ") 等清洗操作
def clean_comment(text) -> str:
    """清洗评论：合并多余空白、去除换行"""
    if pd.isna(text):
        return ""
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text


# 对应 notebook 单元：情感分析
# notebook 原文：定义一个公式计算一个句子的情感分数 - 正面词汇减去负面词汇
def sentiment_score(text: str, pos_words: set, neg_words: set) -> tuple:
    """词典法情感分数 = 正面词数 - 负面词数"""
    words = tokenize(text)
    pos = sum(1 for w in words if w in pos_words)
    neg = sum(1 for w in words if w in neg_words)
    return pos, neg, pos - neg


# ══════════════════════════════════════════════════════
# 数据加载 + 预计算（缓存）
# ══════════════════════════════════════════════════════

# 对应 notebook 单元：jieba.load_userdict("userdict.txt")
# 加载自定义词典（如果存在），确保金融词汇被正确切分
def init_jieba() -> bool:
    """初始化 jieba，加载自定义词典"""
    jieba.initialize()
    if USERDICT_PATH.exists():
        jieba.load_userdict(str(USERDICT_PATH))
        return True
    return False


@st.cache_data(show_spinner=False)
def load_and_score_data() -> pd.DataFrame:
    """
    一次性完成：加载 CSV → 清洗评论 → 切词 → 情感打分。
    首次执行约 60 秒（124K 条评论），之后缓存。

    对应 notebook 完整链路：
      读取文本 → jieba.lcut 切词 → pos_lst/neg_lst 计算情感分数
    """
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df["date"] = pd.to_datetime(df["date"])
    df["comment_clean"] = df["comment"].apply(clean_comment)
    df = df[df["comment_clean"].str.len() > 0].copy()

    # 批量切词 + 情感打分
    results = df["comment_clean"].apply(
        lambda t: sentiment_score(t, POSITIVE_WORDS, NEGATIVE_WORDS)
    )
    df["pos_count"] = results.apply(lambda x: x[0])
    df["neg_count"] = results.apply(lambda x: x[1])
    df["sentiment"] = results.apply(lambda x: x[2])

    df.sort_values("date", inplace=True)
    return df


@st.cache_data(show_spinner=False)
def compute_word_freq(comments: pd.Series, top_n: int = 30) -> pd.DataFrame:
    """对一批评论做切词并统计词频，返回 Top N"""
    all_words = []
    for text in comments:
        all_words.extend(tokenize(text))
    # 过滤单字（长度 < 2）和纯数字
    word_freq = Counter(w for w in all_words if len(w) >= 2 and not w.isdigit())
    top = word_freq.most_common(top_n)
    return pd.DataFrame(top, columns=["词", "频次"])


# ══════════════════════════════════════════════════════
# Streamlit UI
# ══════════════════════════════════════════════════════

st.set_page_config(page_title="股吧评论文本分析", layout="wide")
st.title("股吧评论文本分析 — 光线传媒(300251)")
st.caption("对应 notebook：text_data_processing_1.ipynb（切词 + 词典法情感分析）")

# 检查数据文件
if not DATA_PATH.exists():
    st.error(
        f"数据文件不存在：`{DATA_PATH}`\n\n"
        "请确认 `week06/cleaned_300251_comments.csv` 已就位。"
    )
    st.stop()

# 初始化 jieba
has_userdict = init_jieba()

# 加载 + 预计算
with st.spinner("正在加载数据并计算情感分数（首次约 60 秒，之后自动缓存）…"):
    df_all = load_and_score_data()

# ── 侧边栏 ──
with st.sidebar:
    st.header("数据筛选")

    min_date = df_all["date"].min().date()
    max_date = df_all["date"].max().date()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "起始日期", min_date, min_value=min_date, max_value=max_date
        )
    with col2:
        end_date = st.date_input(
            "截止日期", max_date, min_value=min_date, max_value=max_date
        )

    if start_date > end_date:
        st.error("起始日期不能晚于截止日期")
        st.stop()

    # 过滤数据
    mask = (df_all["date"].dt.date >= start_date) & (
        df_all["date"].dt.date <= end_date
    )
    df = df_all[mask].copy()

    st.metric("选中区间评论数", f"{len(df):,}")
    st.caption(f"数据范围：{min_date} ~ {max_date}")

    st.divider()

    st.header("词典状态")
    if has_userdict:
        st.success("已加载 userdict.txt", icon="✅")
    else:
        st.info("未找到 userdict.txt\n使用内置简易词典", icon="ℹ️")
    st.caption(f"正面词 {len(POSITIVE_WORDS)} 个 · 负面词 {len(NEGATIVE_WORDS)} 个")

if len(df) == 0:
    st.warning("该时间区间内无评论数据，请调整日期范围。")
    st.stop()

# ── Tab 布局 ──
tab1, tab2, tab3 = st.tabs(["切词分析", "情感分析", "评论探索"])

# ══════════════════════════════════════════════════════
# Tab 1: 切词分析
# 对应 notebook: jieba.lcut() + 词频计数
# ══════════════════════════════════════════════════════
with tab1:
    st.subheader("切词演示")
    st.caption(
        "对应 notebook：`jieba.lcut(comment)` — "
        "中文没有空格，分析前要先切成词。"
        "切出来的是人能读的词，例如「股价」「上涨」。"
    )

    # 抽样展示切词结果
    sample_df = df.sample(min(8, len(df)), random_state=42)

    for _, row in sample_df.iterrows():
        comment = row["comment_clean"]
        display = comment[:80] + ("…" if len(comment) > 80 else "")
        words = tokenize(comment)

        with st.expander(f"📅 {row['date'].strftime('%Y-%m-%d %H:%M')} — {display}"):
            st.write("**原文：**")
            st.text(comment)
            st.write("**切词结果：**")
            st.text(" / ".join(words))
            # 标注情感词
            pos_hits = [w for w in words if w in POSITIVE_WORDS]
            neg_hits = [w for w in words if w in NEGATIVE_WORDS]
            if pos_hits:
                st.markdown(f"🟢 正面词：{', '.join(pos_hits)}")
            if neg_hits:
                st.markdown(f"🔴 负面词：{', '.join(neg_hits)}")
            if not pos_hits and not neg_hits:
                st.caption("（未命中情感词）")

    # 词频统计
    st.subheader("词频统计 Top 20")
    st.caption(
        "对应 notebook：切词后计数 — 量化的第一步。"
        "过滤了单字和纯数字。"
    )

    # 如果数据量太大，抽样做词频
    if len(df) > 10000:
        st.caption(f"⚠️ 选中 {len(df):,} 条，抽样 10,000 条做词频统计")
        word_source = df["comment_clean"].sample(10000, random_state=42)
    else:
        word_source = df["comment_clean"]

    word_df = compute_word_freq(word_source, top_n=20)

    fig = px.bar(
        word_df,
        x="频次",
        y="词",
        orientation="h",
        title=f"{start_date} ~ {end_date} 高频词 Top 20",
        color="频次",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), height=500)
    st.plotly_chart(fig, width="stretch")


# ══════════════════════════════════════════════════════
# Tab 2: 情感分析
# 对应 notebook: pos_lst / neg_lst → 情感分数
# ══════════════════════════════════════════════════════
with tab2:
    st.subheader("情感分数分布")
    st.caption(
        "对应 notebook：`正面词汇减去负面词汇` — "
        "词典法给每条评论一个正/负/中性判断。"
    )

    # 概览指标
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("正面评论", f"{(df['sentiment'] > 0).sum():,}")
    with col2:
        st.metric("中性评论", f"{(df['sentiment'] == 0).sum():,}")
    with col3:
        st.metric("负面评论", f"{(df['sentiment'] < 0).sum():,}")

    # 情感分数分布直方图
    fig1 = px.histogram(
        df,
        x="sentiment",
        nbins=30,
        title="情感分数分布",
        labels={"sentiment": "情感分数（正面词数 − 负面词数）"},
        color_discrete_sequence=["#6366f1"],
    )
    fig1.update_layout(height=350)
    st.plotly_chart(fig1, width="stretch")

    # 每日正面/负面情感词频趋势
    st.subheader("每日正面与负面情感词频趋势")
    st.caption(
        "绿线 = 每日正面词总数，红线 = 每日负面词总数。"
        "两条线放在一起看，能直观对比市场乐观与悲观情绪的消长。"
    )

    daily = (
        df.groupby(df["date"].dt.date)
        .agg(
            pos_count=("pos_count", "sum"),
            neg_count=("neg_count", "sum"),
            avg_sentiment=("sentiment", "mean"),
            count=("sentiment", "size"),
        )
        .reset_index()
    )
    daily.columns = ["日期", "正面词数", "负面词数", "平均情感", "评论数"]

    fig2 = go.Figure()
    # 评论数柱状图（背景）
    fig2.add_trace(
        go.Bar(
            x=daily["日期"],
            y=daily["评论数"],
            name="评论数",
            marker_color="rgba(100, 116, 139, 0.15)",
            yaxis="y2",
            hovertemplate="评论数: %{y}<extra></extra>",
        )
    )
    # 正面词频折线
    fig2.add_trace(
        go.Scatter(
            x=daily["日期"],
            y=daily["正面词数"],
            mode="lines",
            name="正面词频",
            line=dict(color="#22c55e", width=2),
            hovertemplate="正面词: %{y}<extra></extra>",
        )
    )
    # 负面词频折线
    fig2.add_trace(
        go.Scatter(
            x=daily["日期"],
            y=daily["负面词数"],
            mode="lines",
            name="负面词频",
            line=dict(color="#ef4444", width=2),
            hovertemplate="负面词: %{y}<extra></extra>",
        )
    )
    fig2.update_layout(
        title="每日正面 vs 负面情感词频（折线）与评论数（柱）",
        xaxis_title="日期",
        yaxis_title="词频",
        yaxis2=dict(title="评论数", overlaying="y", side="right"),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        hovermode="x unified",
    )
    st.plotly_chart(fig2, width="stretch")

    # 每日平均情感分数折线（净情感）
    st.subheader("每日平均情感分数（正面 − 负面）")
    st.caption("净情感分数 = 正面词数 − 负面词数 的逐日均值，正值偏乐观，负值偏悲观")

    fig2b = go.Figure()
    fig2b.add_trace(
        go.Scatter(
            x=daily["日期"],
            y=daily["平均情感"],
            mode="lines",
            name="平均情感分数",
            line=dict(color="#6366f1", width=2),
            hovertemplate="平均情感: %{y:.2f}<extra></extra>",
        )
    )
    fig2b.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="中性",
        annotation_position="bottom left",
    )
    fig2b.update_layout(
        title="每日平均情感分数",
        xaxis_title="日期",
        yaxis_title="平均情感分数",
        height=350,
    )
    st.plotly_chart(fig2b, width="stretch")

    # 正面/负面词频对比
    st.subheader("正面 vs 负面 词频")

    pos_total = int(df["pos_count"].sum())
    neg_total = int(df["neg_count"].sum())

    sentiment_df = pd.DataFrame(
        {"类别": ["正面词", "负面词"], "总次数": [pos_total, neg_total]}
    )

    fig3 = px.bar(
        sentiment_df,
        x="类别",
        y="总次数",
        color="类别",
        color_discrete_map={"正面词": "#22c55e", "负面词": "#ef4444"},
        title="正/负面情感词总频次",
        text="总次数",
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig3, width="stretch")

    # 讨论引导
    st.info(
        "💡 **思考**：词典法在哪些情况会出错？\n\n"
        "- 反讽：「表面利好实则利空」——词典看到「利好」判正面，实际是负面\n"
        "- 上下文依赖：「不看好」——词典可能分别命中「好」和「不看好」\n"
        "- 词典未覆盖的新词、网络用语\n\n"
        "这正是 plan 提到的：**分词和情感分析在大模型下已基本解决，但需核对结果是否可信。**"
    )


# ══════════════════════════════════════════════════════
# Tab 3: 评论探索
# ══════════════════════════════════════════════════════
with tab3:
    st.subheader("评论搜索与筛选")

    # 情感筛选
    sentiment_filter = st.radio(
        "情感筛选",
        ["全部", "正面（sentiment > 0）", "负面（sentiment < 0）", "中性（sentiment = 0）"],
        horizontal=True,
    )

    # 关键词搜索
    keyword = st.text_input(
        "关键词搜索（可选）", placeholder="输入关键词，如「涨停」「割肉」「光线」"
    )

    # 应用筛选
    filtered = df.copy()
    if "正面" in sentiment_filter:
        filtered = filtered[filtered["sentiment"] > 0]
    elif "负面" in sentiment_filter:
        filtered = filtered[filtered["sentiment"] < 0]
    elif "中性" in sentiment_filter:
        filtered = filtered[filtered["sentiment"] == 0]

    if keyword.strip():
        filtered = filtered[
            filtered["comment_clean"].str.contains(keyword.strip(), na=False)
        ]

    st.metric("筛选结果", f"{len(filtered):,} 条")

    if len(filtered) == 0:
        st.warning("无匹配评论，请调整筛选条件。")
        st.stop()

    # 数据表
    display_df = filtered[["date", "comment_clean", "pos_count", "neg_count", "sentiment"]].copy()
    display_df.columns = ["日期", "评论内容", "正面词数", "负面词数", "情感分数"]
    display_df["日期"] = display_df["日期"].dt.strftime("%Y-%m-%d %H:%M")
    display_df["评论内容"] = display_df["评论内容"].str[:120] + "…"

    st.dataframe(
        display_df.sort_values("情感分数", ascending=False),
        width="stretch",
        height=400,
    )

    # 最正面 / 最负面评论
    st.subheader("情感最强烈的评论")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("🟢 **最正面评论**")
        top_pos = filtered.nlargest(3, "sentiment")
        for _, row in top_pos.iterrows():
            st.success(
                f"📅 {row['date'].strftime('%Y-%m-%d')}  |  "
                f"情感分: {row['sentiment']}  "
                f"（正 {row['pos_count']} / 负 {row['neg_count']}）\n\n"
                f"{row['comment_clean'][:200]}"
            )

    with col2:
        st.markdown("🔴 **最负面评论**")
        top_neg = filtered.nsmallest(3, "sentiment")
        for _, row in top_neg.iterrows():
            st.error(
                f"📅 {row['date'].strftime('%Y-%m-%d')}  |  "
                f"情感分: {row['sentiment']}  "
                f"（正 {row['pos_count']} / 负 {row['neg_count']}）\n\n"
                f"{row['comment_clean'][:200]}"
            )
