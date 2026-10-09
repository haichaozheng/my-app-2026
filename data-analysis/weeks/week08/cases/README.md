# Week08 案例：股吧评论文本分析

## 运行

```bash
# 在仓库根目录激活虚拟环境
.\.venv\Scripts\activate

# 安装依赖（首次）
pip install -r data-analysis/weeks/week08/cases/requirements.txt

# 启动
streamlit run data-analysis/weeks/week08/cases/app.py
```

## 数据

- **数据文件**：`../../week06/cleaned_300251_comments.csv`
- **内容**：光线传媒(300251) 东方财富股吧评论，124,126 条
- **时间范围**：2011-07-14 ~ 2019-04-10
- **字段**：`date`（时间戳）、`comment`（评论内容）、`author`（作者）等

> 数据来自 Week06 课堂练习。如该文件不存在，请先完成 Week06 数据获取。

## 词典文件

三个词典文件位于 `cases/` 目录下（与 app.py 同级）：

| 文件 | 用途 | 对应 notebook |
|---|---|---|
| `userdict.txt` | jieba 自定义词典，确保金融词汇正确切分 | `jieba.load_userdict("userdict.txt")` |
| `zhang_unformal_pos.txt` | 正面情感词表 | `pos_lst`（中文金融版） |
| `zhang_unformal_neg.txt` | 负面情感词表 | `neg_lst`（中文金融版） |

`userdict.txt` 格式（每行一条，UTF-8 编码）：`词语 词频(可选) 词性(可选)`

## 与 notebook 的对应关系

| app.py 函数/模块 | notebook 单元 |
|---|---|
| `tokenize()` | `jieba.lcut("我想去成都")` — jieba 切词 |
| `init_jieba()` + `userdict.txt` | `jieba.load_userdict("userdict.txt")` — 自定义词典 |
| `sentiment_score()` | `pos_lst` / `neg_lst` + 情感分数计算 — 词典法情感分析 |
| `load_word_set()` | 从 `zhang_unformal_pos.txt` / `zhang_unformal_neg.txt` 加载情感词表 |
| `clean_comment()` | notebook 提到的 `replace("\u3000"," ")` 等文本预处理 |
| 词频统计（Tab 1） | 切词后计数 — 量化的第一步 |
| 正/负面词频对比（Tab 2） | notebook 英文示例的中文金融版 |

## App 结构

| Tab | 内容 | 对应 notebook 知识点 |
|---|---|---|
| **切词分析** | 抽样展示切词结果 + 词频 Top 20 条形图 | jieba 切词、词频统计 |
| **情感分析** | 情感分布直方图 + 每日趋势折线 + 正负面词频对比 | 词典法情感分析 |
| **评论探索** | 按情感/关键词筛选评论 + 最正/最负评论展示 | 结果核对与可信度检验 |

## 教学要点

> 对应 plan.md：分词和情感分析在大模型下已经是基本解决的任务。
> 项目里直接调用，不必再自己做分词器或训练情感分类器。
> 剩下的工作是**核对结果是否可信**。

- 词典法能快速给出方向性判断，但在反讽、上下文依赖等场景会出错
- Tab 2 底部的「思考」引导学生关注词典法的局限性
- Tab 3 让学生主动搜索、筛选、核对具体评论的判断结果
