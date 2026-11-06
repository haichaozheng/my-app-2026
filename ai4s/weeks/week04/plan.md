# Week 04 教学计划

## 本周主题

发现空白→凝练问题 — gap analysis 多智能体 + 选题

> Phase 2: Design 第1周。选题是 gap-driven 而非兴趣-driven；AI 辅助发现空白但研究价值由人判断。本周的核心升级：把"发现空白"从一次 LLM 对话升级为一条**有证据锚点、可核验、可审计的流水线**——1 个主 Agent 编排 + 6 个子智能体协作的 gap 分析多智能体（基于 opencode agents 的 primary/subagent 模式）。

## 学习目标

- 能说明 gap analysis 方法论：gap 不是"我觉得没人做"，而是系统性分析（方法论空白、理论空白、数据空白、情境空白），并能用罗家德等（2026）第4章的研究类型图谱为 gap 类型标注坐标系
- 能说明 problematization 与 gap-spotting 的区别，并说明为什么博士论文需要 problematization
- 能说明多智能体分工的价值：单次 LLM 对话无证据锚点、不可核验、无留痕；流水线让每一步可查证、可审计
- 能配置并运行 gap 分析多智能体（1 主 + 6 子）：主 Agent 推进"抽取→标注→核验→侦察→凝练"流程并传递上下文，子智能体各司其职
- 能说明七个角色的职责与权限纪律：主 Agent 只编排不生成内容；Audit Scribe 全程留痕
- 能对 Verifier 与 Feasibility Scout 的输出做**人工裁决**并记录修正点（研究价值由人判断，不可委托给 AI）
- 能对研究问题做"So What?"检验，说明贡献类型（理论/经验/方法论贡献），并用 Davis "That's Interesting!" 标准检验
- 能对 gap 分析做偏误自检（确认偏误、AI 引用文献真实性验证）

## 教学步骤（3节课）

**第1节 · Gap analysis 方法论与 Problematization（45 分钟）**

1. 选题是 gap-driven 而非兴趣-driven（8 分钟）
2. Gap 类型讲解（12 分钟）：方法论空白、理论空白、数据空白、情境空白；用罗家德等（2026）第4章研究类型图谱作标注坐标系
3. Problematization 深讲（15 分钟）：质疑既有研究的隐含假设——从"填空白"到"变视角"；用社科实例（如制度理论从"制度约束行为"到"制度是被建构的"）
4. 从 W3 综述中初步定位 gap（5 分钟）。💡 课堂互动：教师展示 3 个研究问题实例，全班快速判断各属于 gap-spotting 还是 problematization（3 分钟抢答）

**第2节 · Gap 分析多智能体：从一次对话到一条流水线（45 分钟）**

5. 为什么需要多智能体（10 分钟）：单次 LLM 对话的三个局限——无证据锚点（gap 从哪来查不到）、不可核验（新颖性靠模型一张嘴）、无留痕（过程不可复现）；流水线的价值：每一步有输出物、可回查、可审计
6. 架构讲解（15 分钟）：1 主 + 6 子（基于 [opencode agents](https://opencode.ai/v2/docs/agents/) 的 primary/subagent 模式）——

   | 角色 | 模式 | 职责 |
   |---|---|---|
   | 主Agent（编排） | primary | 推进"抽取→标注→核验→侦察→凝练"流程，传递综述语料与上下文；**只编排不生成内容** |
   | Gap Extractor | subagent | 从综述中抽取 gap 候选，标注类型与锚点（文献、章节、页码） |
   | Innovation Mapper | subagent | 标注创新类型、最近邻对比、差异声明 |
   | Verifier | subagent | 新颖性三档核验：伪空白 / 相邻 / 候选真空白 |
   | Feasibility Scout | subagent | 数据、方法、时间、伦理四维侦察，输出 MVR（最小可行研究）建议 |
   | Prober | subagent | 条件化 + 科创凝练追问（把 gap 逼成可研究的问题） |
   | Audit Scribe | subagent | 记录证据锚点、核验日志、人工修正点 |

7. 配置与演示（12 分钟）：用 opencode agents 配置七个角色；教师演示完整运行一轮，重点展示 Gap 证据表长什么样（每条 gap 带文献锚点、类型标注、核验状态）
8. AI 引用文献真实性验证（8 分钟）：当场演示 AI 编造文献的过程与核查方法——这正是 Verifier 角色存在的理由，也是学生做人工裁决时必须复查的点

**第3节 · 运行、裁决与凝练（45 分钟）**

9. 个人多智能体运行实操（15 分钟）：每人以自己的 W3 综述为语料，跑通至少 1 轮完整流程
10. 人工裁决（12 分钟）：阅读 Verifier（伪空白/相邻/候选真空白）与 Feasibility Scout（四维侦察 + MVR）的输出，对关键节点做裁决并记录修正点。💡 课堂互动：抽取 2-3 位同学投屏自己的裁决过程——哪里同意智能体、哪里推翻、为什么（3-4 分钟）
11. "So What?" 检验与贡献类型（10 分钟）：填了这个 gap 之后——谁在意？什么理论被推进？什么实践被改变？贡献类型意识（理论/经验/方法论）；Davis "That's Interesting!" 标准——好问题挑战而非确认既有假设
12. Prober 凝练与收束（8 分钟）：用 Prober 的条件化追问把 gap 逼成可研究的问题；选题可行性自检（数据可得性、方法适用性、博士论文工作量）；预告 W5 研究设计（本周 Gap 证据表与协变量结构是 W5 的直接输入）

## 交付物

- **研究问题陈述 + Gap 证据表**（评分锚点，对应 milestones §2.1，计入阶段成果一（研究选题与研究设计）25%）
  - 研究领域现状概述
  - gap 分析过程和发现的研究空白（多智能体流水线产出）
  - 凝练的研究问题和初步研究方向（含贡献类型与"So What?"检验）
  - 选题可行性的初步判断
  - **Gap 证据表与协变量结构**（每条 gap 带证据锚点、类型标注、核验状态；与问题陈述共同构成 W5 输入）
  - 子智能体核验日志（Audit Scribe 留痕）与人工修正点记录
- 方法论锚定：体现 gap analysis 方法论、problematization 意识、多智能体流水线价值、权限纪律、人工裁决记录、"So What?"检验、贡献类型与"有趣"标准、偏误自检

## 课后自学

- Gap analysis 方法论：`knowledge/m2-1-gap-analysis.md`
- Prompt 驱动 gap 分析：`knowledge/m2-2-prompt-gap-analysis.md`
- Agent 辅助文献空白发现：`knowledge/m2-6-agent-topic-discovery.md`
- 选题验证：`knowledge/m2-3-topic-validation.md`
- 研究问题凝练：`knowledge/m2-4-research-question.md`
- 跨范式选题策略（推荐）：`knowledge/m2-5-cross-paradigm-topic.md`
- **方法论阅读（反思日志须回应）**：罗家德等（2026）第4章"社会计算驱动的研究方法"（研究类型图谱，为 gap 类型标注提供坐标系）
- 工具：[opencode Agents 文档](https://opencode.ai/v2/docs/agents/)（primary/subagent 配置方法）

## 课后作业

运行 gap 分析多智能体完成至少 1 轮完整流程，对 Verifier 与 Feasibility Scout 的输出做人工裁决并记录修正点，形成研究问题陈述初稿（含 Gap 证据表与协变量结构、偏误自检记录）。

## 参考资料

- 理念：Sandberg, J. & Alvesson, M. (2011). "Ways of constructing research questions: gap-spotting or problematization?" *Organization*, 18(1), 23-44
- 理念：Davis, M.S. (1971). "That's Interesting! Towards a Phenomenology of Sociology and a Sociology of Phenomenology." *Social Studies of Science*, 1(2), 309-344
- 理念：Locke, K. & Golden-Biddle, K. (1997). "Constructing Opportunities for Contribution: Structuring Intertextual Coherence and 'Problematizing' in Organizational Studies." *Academy of Management Journal*, 40(5), 1023-1042
- 工具：Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629
- 工具：[opencode Agents 文档](https://opencode.ai/v2/docs/agents/)
- `weeks/week04/lecture.md`、`weeks/week04/lab.md`
