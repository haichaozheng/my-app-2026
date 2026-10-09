# Week09 案例：OpenCode Skill — 股评情感分析

## 这是什么？

一个完整的 OpenCode Skill 示例。把它放到项目 `.opencode/skills/` 目录下，AI 助手就会在你说「分析股评」时自动加载这套指令，按定义好的步骤和格式输出——不用每次重新贴 prompt。

## 目录结构

```
cases/
├── .opencode/
│   └── skills/
│       └── stock-comment-analysis/
│           ├── SKILL.md                          # ← Skill 主文件（指令）
│           └── references/
│               └── sentiment-guide.md            # ← 参考资料（情感判断标准）
├── sse_comments.txt                               # 样本数据（401 条股评）
├── userdict.txt                                   # jieba 自定义词典
├── zhang_unformal_pos.txt                         # 正面情感词表
├── zhang_unformal_neg.txt                         # 负面情感词表
└── README.md                                      # 本文件
```

## SKILL.md 核心结构

```markdown
---
name: Stock Comment Sentiment Analysis
description: Analyze sentiment of Chinese stock forum comments. Use this skill when
  the user asks to analyze stock comments, classify sentiment of financial text,
  or generate a sentiment summary from comment data.
---

## 场景
[什么时候用这个 Skill]

## 输入
[需要什么数据]

## 分析步骤
1. 读取数据
2. 逐条分析（正面/中性/负面）
3. 识别难点（反讽、网络用语）
4. 生成摘要

## 输出格式
[结构化模板]

## 注意事项
[金融文本的特殊处理]
```

**关键字段**：
- `name`：Skill 名称，简短
- `description`：**最重要**——AI 根据这段话判断何时调用。写清「什么任务用这个 Skill」
- 正文：场景 → 步骤 → 输出格式 → 注意事项

## 怎么用

### 1. 把 Skill 放到你的项目

```bash
# 复制到你的项目根目录
cp -r cases/.opencode/skills/stock-comment-analysis  你的项目/.opencode/skills/
```

或在 Trae / OpenCode 中，项目根目录创建 `.opencode/skills/stock-comment-analysis/SKILL.md`。

### 2. 让 AI 帮你分析股评

在 Trae / OpenCode 的对话中直接说：

> 帮我分析 sse_comments.txt 里的股评情感

AI 会自动识别这是一个「股评情感分析」任务，加载 Skill，按照 SKILL.md 里定义的步骤和格式输出。

### 3. 对比：不带 Skill vs 带 Skill

**不带 Skill**（AI 自由发挥）：
- 输出格式不固定（每次不同）
- 可能忽略金融反讽
- 不知道你有情感词典

**带 Skill**：
- 固定输出格式（概览 + 高频话题 + 典型评论）
- 知道识别反讽和网络用语
- 参考情感判断标准（references/sentiment-guide.md）

## 数据文件

| 文件 | 用途 |
|---|---|
| `sse_comments.txt` | 上证指数股吧评论 401 条（2025-10 采集） |
| `userdict.txt` | jieba 自定义词典（金融术语） |
| `zhang_unformal_pos.txt` | 正面情感词表 |
| `zhang_unformal_neg.txt` | 负面情感词表 |

> 词典文件复用自 W8 案例。W8 用词典法做情感分析（代码实现），本周用 Skill 让 AI 按同样的标准分析（指令封装）。

## 与 notebook 的对应关系

| Skill 部分 | notebook 单元 |
|---|---|
| `description` 字段 | Skills 概念：AI 如何判断何时调用 |
| 分析步骤 | 对比 W8 词典法 vs W9 Skill 法 |
| 输出格式 | SKILL.md 结构详解 |
| references/ | 如何附带参考资料 |
| 注意事项（反讽识别） | LLM 原理：为什么 LLM 能理解上下文 |

## 教学要点

- **Skill = 给 AI 的 SOP**：不是代码，是「标准操作流程」——告诉 AI 遇到这类任务该怎么做
- **description 是灵魂**：写不好 description，AI 不知道何时调用，Skill 就白写了
- **参考资料让 Skill 更强**：`references/sentiment-guide.md` 让 AI 知道金融用语和反讽规则
- **迭代改进**：先写一个 3 行的 Skill，用一次，发现 AI 输出不对，再补充步骤和约束——和写代码一样迭代

## 为自己的项目创建 Skill

1. 想清楚：你的 AI 助手反复帮你做什么？
   - 分析数据 → EDA 报告生成 Skill
   - 写代码 → 代码审查 Skill
   - 生成内容 → 内容模板 Skill
2. 在项目根目录创建 `.opencode/skills/<你的skill名>/SKILL.md`
3. 写好 frontmatter（name + description）
4. 写好指令正文（场景 → 步骤 → 输出格式）
5. （可选）放参考资料文件
6. 用一次，看 AI 输出是否符合预期，迭代改进
