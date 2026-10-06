# Week 04 教学计划

## 本周主题

发现空白→凝练问题 — gap analysis + 选题 + Skill 封装

> Phase 2: Design 第1周。选题是 gap-driven 而非兴趣-driven；AI 辅助发现空白但研究价值由人判断；本周深化 Skill 应用——封装 gap 识别 Skill。

## 学习目标

- 能说明 gap analysis 方法论：gap 不是"我觉得没人做"，而是系统性分析（方法论空白、理论空白、数据空白、情境空白）
- 能说明 problematization 与 gap-spotting 的区别，并说明为什么博士论文需要 problematization
- 能用 Prompt 驱动 LLM 进行多轮 gap analysis 对话
- 能用 Agent 三种方式辅助文献空白发现（汇总"未来研究"段落、对比方法论差异、识别理论矛盾）
- 能对 gap 做评估筛选：重要性、可行性、新颖性、与个人研究方向匹配度
- 能对研究问题做"So What?"检验，说明填 gap 后的理论或实践贡献
- 能把模糊兴趣凝练为清晰的研究问题，说明贡献类型（理论/经验/方法论贡献），并用 Davis "That's Interesting!" 标准检验
- 能把 gap 识别流程封装为 Skill（输入文献库→输出 gap 清单+选题建议）
- 能对 gap 分析做偏误自检（确认偏误、AI 引用文献真实性验证）

## 教学步骤（3节课）

**第1节 · Gap analysis 与 Problematization（45 分钟）**

1. 选题是 gap-driven 而非兴趣-driven（8 分钟）
2. Gap 类型讲解（12 分钟）：方法论空白、理论空白、数据空白、情境空白
3. Problematization 深讲（15 分钟）：质疑既有研究的隐含假设——从"填空白"到"变视角"；用社科实例（如制度理论从"制度约束行为"到"制度是被建构的"）
4. 从 W3 综述中初步定位 gap（5 分钟）。💡 课堂互动：教师展示 3 个研究问题实例，全班快速判断各属于 gap-spotting 还是 problematization（3 分钟抢答）

**第2节 · Prompt 与 Agent 驱动的 gap 发现与评估（45 分钟）**

5. Prompt 驱动多轮 gap analysis 对话演示（10 分钟）：Deep Research / 多轮对话
6. Agent 辅助文献空白发现（12 分钟）：三种具体用法——(a) Agent 汇总 Zotero 文献库中"未来研究"段落；(b) Agent 对比论文间方法论差异；(c) Agent 识别文献间理论矛盾
7. gap 评估框架（12 分钟）：找到 gap 后怎么判断值不值得做——重要性（填了之后谁在意？理论推进还是实践改变？）、可行性（数据可得性、方法适用性、时间范围）、新颖性（是真空白还是已有人做了你没搜到？）、与个人研究方向的匹配度（你有没有积累和优势？）；用 2-3 个 gap 实例当场演示评估过程
8. 个人 gap analysis 对话实操（8 分钟）：每位博士生进行至少 1 轮 LLM gap analysis + 初步评估
9. AI 引用文献真实性验证（3 分钟）：当场演示 AI 编造文献的过程与核查方法

**第3节 · "So What?" 检验与 Skill 开发（45 分钟）**

10. "So What?" 检验（12 分钟）：填了这个 gap 之后——谁在意？什么理论被推进？什么实践被改变？用 2-3 个社科博士论文实例演示从 gap 到贡献的转化
11. 研究问题凝练与贡献类型（10 分钟）：贡献类型意识（理论贡献/经验贡献/方法论贡献）；Davis "That's Interesting!" 标准——好问题挑战而非确认既有假设
12. gap 识别 Skill 开发（15 分钟）：每人封装自己的 gap 识别 Skill——输入文献库（标题+摘要），输出 gap 清单（按四类分类）+ 选题建议。💡 课堂互动：抽取 2-3 位同学投屏演示 Skill 运行，全班评估 gap 识别质量（3-4 分钟）
13. 选题可行性自检（8 分钟）：数据可得性、方法适用性、博士论文工作量评估

## 交付物

- **研究问题陈述 + gap 识别 Skill**（评分锚点，对应 milestones §2.1，与 W5 合并评分）
  - 研究领域现状概述
  - gap 分析过程和发现的研究空白
  - 凝练的研究问题和初步研究方向（含贡献类型与"So What?"检验）
  - 选题可行性的初步判断
  - gap 识别 Skill（可复用，输入文献库→输出 gap 清单+选题建议）
- 方法论锚定：体现 gap analysis 方法论、problematization 意识、Prompt 驱动对话、Agent 辅助（三种用法）、gap 评估框架、"So What?"检验、贡献类型与"有趣"标准、偏误自检、Skill 封装逻辑

## 课后自学

- Gap analysis 方法论：`knowledge/m2-1-gap-analysis.md`
- Prompt 驱动 gap 分析：`knowledge/m2-2-prompt-gap-analysis.md`
- Agent 辅助文献空白发现：`knowledge/m2-6-agent-topic-discovery.md`
- 选题对话与验证：`knowledge/m2-3-topic-dialogue.md`
- 研究问题分类与凝练：`knowledge/m2-4-question-classification.md`
- 跨范式选题策略（推荐）：`knowledge/m2-5-cross-paradigm.md`
- Davis "That's Interesting!" 与贡献类型（推荐）：`knowledge/m2-7-contribution-types.md`
- Skill 封装进阶：[opencode Skill 文档](https://opencode.ai/docs/)

## 课后作业

完成至少 1 轮 LLM gap analysis 多轮对话，封装 gap 识别 Skill，形成研究问题陈述初稿（含 gap 分析、问题表述、贡献类型与"So What?"检验、可行性判断、偏误自检记录、Skill 代码）。

## 参考资料

- 理念：Sandberg, J. & Alvesson, M. (2011). "Ways of constructing research questions: gap-spotting or problematization?" *Organization*, 18(1), 23-44
- 理念：Davis, M.S. (1971). "That's Interesting! Towards a Phenomenology of Sociology and a Sociology of Phenomenology." *Social Studies of Science*, 1(2), 309-344
- 理念：Locke, K. & Golden-Biddle, K. (1997). "Constructing Opportunities for Contribution: Structuring Intertextual Coherence and 'Problematizing' in Organizational Studies." *Academy of Management Journal*, 40(5), 1023-1042
- 工具：Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629
- 工具：[opencode Skill 文档](https://opencode.ai/docs/)
- `weeks/week04/lecture.md`、`weeks/week04/lab.md`
