# Week 09 教学计划

## 主题
LLM 原理与 OpenCode Skills 开发 + 同侪互评 + 开始打磨迭代

> **前置**：须已完成 W8 MVP v0.2（含LLM智能解读）。本周理解 LLM 原理，并学会把 AI 工作流封装成 OpenCode Skill；同时开始互评与打磨。

### 为什么本周学 Skills？

W8 你用 LangChain + Prompt Template 给产品加了 LLM 智能解读。但你每次让 AI 帮你分析数据、写代码、生成报告时，都要重新描述需求、贴 prompt——换个场景又要重来。

能不能把你反复使用的 AI 工作流封装成「技能」，让 AI 一调用就知道该怎么做？

这就是 **OpenCode Skills**：把 prompt + 步骤 + 参考资料 + 输出格式打包成一个可复用的 Skill，AI 在需要时自动加载。相当于给你的 AI 助手装上「专业知识包」。

### 教学资料说明

本周核心教学资料来自 `session-02/`（Skill 基础与应用）和 `session-03/`（Skill 与 Agent 开发），已适配到 3×45 分钟课堂：

| 资料 | 内容 | 课堂用途 |
|---|---|---|
| `session-02/lecture.md` | 工具体系、Skill 概念、SKILL.md 结构、tushare/gstack Skill、简单 Skill 创建 | 第1节主讲 |
| `session-02/lab.md` | 工具配置、webfetch/websearch、tushare skill 安装使用、创建 swufe-news Skill | 第1-3节实践 |
| `session-03/lecture.md` | MCP、Skill 开发实践（skill-creator/skill-improver）、Agent、协同架构 | **进阶，课后自学** |
| `session-03/lab.md` | MCP 配置、stock-tech-analysis Skill 开发、Agent 创建、日报系统 | **进阶，课后自学** |
| `llm.ipynb` | LLM 原理：N-gram→RNN→GPT→Attention/Transformer | 第1节原理铺垫 |
| `text_data_processing_2.ipynb` | 向量与余弦相似度（numpy + sklearn） | 第1节数学基础 |
| `skills_development.ipynb` | Skills 开发速览（结构 + 示例 + 实践要点） | 课后参考 |
| `cases/` | 完整 Skill 案例：股评情感分析 Skill | 第3节实践参考 |

## 本周学习目标

- 能说清 LLM 的基本原理（统计语言模型→N-gram→RNN→GPT→Attention/Transformer）
- 能说明 OpenCode Skill 的概念与价值（按需加载、节约上下文、可复用）
- 能创建一个 OpenCode Skill（SKILL.md + frontmatter + 步骤指令），为自己项目中的重复性 AI 任务封装可复用指令
- 能基于明确标准（功能完整度/可用性/分析深度/AI功能价值）给组员产品 ≥3 条结构化反馈，其中至少 1 条可执行
- 能说明收到的反馈为什么采纳/为什么不采纳，并落到 v0.3 迭代

## 预计投入

课堂 3×45 分钟。课外 6-8h（含 session-03 进阶自学）

## 教学内容
1. LLM 原理回顾（`llm.ipynb`）：N-gram→RNN→GPT→Attention/Transformer——理解 LLM 为什么能生成文本
2. 向量与余弦相似度（`text_data_processing_2.ipynb`）：文本如何变成向量、语义距离如何衡量
3. OpenCode 工具体系与 Skill 基础（`session-02/lecture.md` §一-§三）：
   - 内置工具概览（read/write/bash/webfetch/websearch/skill）
   - Skill 概念：结构化指令文档，告诉 AI 如何完成任务；按需加载，节约上下文
   - SKILL.md 结构：frontmatter（name + description）+ 指令正文
   - Skill 触发机制：自动触发（description 匹配）vs 手动调用
   - 常用 Skill：tushare（金融数据）、gstack（产品开发）
4. Skill 开发实践（`session-02/lecture.md` §四 + `session-02/lab.md`）：
   - 创建最简 Skill（swufe-news 示例）
   - 为自己的项目创建 Skill
5. 产品评审标准与同侪互评
6. 据反馈定向打磨，产出 v0.3

**进阶（课后自学，`session-03/`）**：
- MCP：让 AI 直接调用外部工具，零代码数据获取
- skill-creator / skill-improver：AI 辅助 Skill 开发与质量评估
- Agent：独立智能体，编排 Skill 和 MCP 完成复杂任务
- Skill + Agent + MCP 协同架构

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| LLM 原理 | `llm.ipynb` | N-gram→RNN→GPT→Attention 串讲 |
| 向量数学 | `text_data_processing_2.ipynb` | 余弦相似度演示 |
| Skill 主演示 | OpenCode/Trae | 工具体系演示 + tushare skill 触发 + 创建 swufe-news Skill |
| 互评主演示 | 学生产品（Streamlit） | 教师用评审单当场评 1 个示例 |
| 学生主活动 | `.opencode/skills/` + `templates/peer-review.md` | 创建 Skill + 互评 |

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：`llm.ipynb` 可投影；OpenCode/Trae 中 tushare skill 已安装可用（token 已配置）；`session-02/lecture.md` 投影备用；评审单投影；组员座位按互助组排。

**第1节 · LLM 原理 + Skill 基础（45 分钟）**

1. **分享上周 journal + LLM 原理串讲（15 分钟）**：随机邀请同学分享上周 journal（3 问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点）。用 `llm.ipynb` 串讲：统计语言模型→N-gram→RNN（有了记忆）→GPT（Transformer，自回归生成）→Attention（每个词「看」其他所有词）。点到「LLM 本质上是超大规模神经网络」即可。
2. **OpenCode 工具体系与 Skill 概念（15 分钟）**（对应 `session-02/lecture.md` §一-§二）：
   - **工具是 AI 的「手」**（5 分钟）：read/write/bash/webfetch/websearch——AI 用工具执行操作
   - **Skill 是 AI 的「说明书」**（5 分钟）：告诉 AI 遇到这类任务该怎么做；按需加载，节约上下文；`.opencode/skills/<id>/SKILL.md`
   - **SKILL.md 结构**（5 分钟）：frontmatter（name + description）+ 指令正文（场景→步骤→输出格式）。**description 最重要**——AI 根据它判断何时调用
3. **演示：tushare Skill 触发（15 分钟）**（对应 `session-02/lecture.md` §三-§四）：
   - 在 OpenCode/Trae 中输入「获取贵州茅台最近 30 天的股价数据」
   - 观察 tushare skill 自动触发 → AI 加载 SKILL.md → 按步骤执行
   - 对比：不带 skill 时 AI 自由发挥的差异
   - 展示 `cases/.opencode/skills/stock-comment-analysis/` 作为另一个领域示例

**第2节 · 组内互评（45 分钟）**

4. **四维标准 + 教师示范评（10 分钟）**：四维：功能完整度 / 可用性 / 分析深度 / AI 功能价值。教师打开 1 个产品，用评审单写 ≥3 条（情境–现象–建议），其中 1 条可执行。
5. **轮转互评（30 分钟）**：组内每人被评；时间凑不齐则先完成 1 人份，其余书面异步、周末补。
6. **中场对齐（5 分钟）**：提醒反馈要有维度、有例子，不要「做得很棒」。

**第3节 · Skill 开发实践 + v0.3（45 分钟）**

7. **创建最简 Skill 演示（10 分钟）**（对应 `session-02/lecture.md` §四案例三 + `session-02/lab.md` §2.4）：
   - 教师演示创建 swufe-news Skill（或用 `cases/` 的 stock-comment-analysis Skill）
   - 展示 SKILL.md 最小结构：frontmatter + 步骤 + 示例
   - 测试 Skill 触发
8. **学生为自己的项目创建 Skill（20 分钟）**：在项目 `.opencode/skills/<your-skill>/SKILL.md` 创建。分步检查点：
   - [ ] 想清楚：你的 AI 助手反复帮你做什么？（获取数据？分析文本？生成报告？）
   - [ ] 写好 frontmatter：name + description（description 决定 AI 何时调用）
   - [ ] 写好指令正文：场景 → 步骤 → 输出格式
   - [ ] 测试 Skill 是否能被正确触发
   教师巡场，帮学生把 description 写准。参考 `skills_development.ipynb` 的设计原则部分。
9. **采纳/不采纳 → v0.3 + 收束（15 分钟）**：每人针对收到的互评反馈写理由，标出本周先改哪 1–2 项。`lab.md` 当堂起笔。当日在 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）。互助记录只写「谁帮了你、对项目有何影响」，没有则写「无」。本周回顾：理解了 LLM 原理，学会用 Skills 封装 AI 工作流，完成互评并开始 v0.3 迭代。进阶自学：`session-03/`（MCP + Agent + 协同架构）。W10 部署上线。

## 项目活动

**必做**
1. 组内个人MVP互评：基于评审标准给每位组员结构化反馈（书面评审单）
2. 根据互评反馈开始迭代打磨，产出 v0.3——对每条反馈写明采纳/不采纳及理由
3. 为自己的项目创建 ≥1 个 OpenCode Skill（SKILL.md + frontmatter + 步骤指令）

**进阶（可选）**
4. 安装并使用 tushare skill 获取金融数据（需配置 tushare token）
5. 使用 skill-creator 辅助创建 Skill，用 skill-improver 评估质量（见 `session-03/lab.md`）
6. 学习 MCP 配置，体验零代码数据获取（见 `session-03/lecture.md` §一）
7. 创建 Agent，构建 Skill + Agent 协同工作流（见 `session-03/lecture.md` §三）

**兜底**
- 小组时间凑不齐：先完成 1 人份完整结构化评审，其余转书面异步反馈，周末前补齐
- Skill 写不出来：先把 description 写对（一句话说清「什么任务用这个 Skill」），指令正文可以先 3-5 行，后续迭代
- tushare token 未配置：用 `cases/` 的 stock-comment-analysis Skill 替代（不需要 token）

## 交付物（评分锚点）

- 组内互评反馈（`templates/peer-review.md` 评审单）
- 个人MVP v0.3（含初步打磨）
- OpenCode Skill（`.opencode/skills/<id>/SKILL.md`）

—— 规格与知识锚定见 milestones §2.6（RAG 选做替换为 Skills 开发）；计入平时成绩（形成性），并作为期末协作互评的形成性依据。提交前自检：反馈按维度、有等级、有例子？采纳/不采纳有理由？Skill 的 description 写准了？指令正文有步骤和输出格式？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

## 课后任务
1. 完成组内互评
2. 根据反馈开始优化产品，产出 v0.3
3. 完善自己的 Skill（指令正文 + 参考资料）
4. 回看 `llm.ipynb` 中 Attention/Transformer 部分（未理解者补看）
5. （进阶）自学 `session-03/`：MCP + Agent + 协同架构

## 学习资料
- `llm.ipynb`（LLM 原理：N-gram→RNN→GPT→Attention/Transformer）
- `text_data_processing_2.ipynb`（向量与余弦相似度：numpy + sklearn）
- `skills_development.ipynb`（Skills 开发速览：结构 + 示例 + 设计原则）
- `session-02/lecture.md`（Skill 基础与应用：工具体系 + Skill 概念 + SKILL.md + 演示案例）
- `session-02/lab.md`（实验：工具配置 + tushare skill + 创建 swufe-news Skill）
- `session-03/lecture.md`（**进阶**：MCP + Skill 开发实践 + Agent + 协同架构）
- `session-03/lab.md`（**进阶实验**：MCP 配置 + stock-tech-analysis Skill + Agent + 日报系统）
- `cases/`（完整 Skill 案例：股评情感分析 Skill，含 SKILL.md + 参考资料）
- `knowledge/phase2-2-16-product-review.md`（产品评审标准）
- `knowledge/phase2-2-17-peer-review.md`（同侪互评方法）
- `templates/peer-review.md`（互评评审单）
- OpenCode Skills 官方文档：https://opencode.ai/v2/docs/skills
- 视频资料（超星学习通，详见 `video-resources.md`）：3.1/3.2 词语切分（分词简介 + jieba）+ 4.1 文本量化 TF-IDF（理解中文金融文本切分与向量化原理）
