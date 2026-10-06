# 人工智能大模型应用 — AI4S PBL教学方案

## 课程信息

- **面向对象**：社科类博士生（背景多样：经济学、社会学、政治学、管理学、传播学等）
- **课程目标**：围绕学生个人科研项目构建AI4S工具栈，并应用该工具栈开展科研
- **教学方法**：Project Based Learning（PBL）
- **课程时长**：9周
- **项目形式**：个人项目为主，每位博士生围绕自己的科研项目独立构建工具栈
- **技术栈**：大模型贯穿全程，作为AI4S工具栈的核心支撑
- **先修要求**：学生有一定Python基础和大模型使用经验

## 共同AI基础工具栈

两门课程共享以下AI基础工具栈，随科研流程**渐进式融入**教学内容，而非单独设课：

| 工具 | 在课程中的角色 | 主要应用场景 |
|---|---|---|
| AI辅助编程(opencode/cursor) | 科研编程生产力工具 | Python/R/Stata代码生成、调试、迭代 |
| Prompt Engineering | 与LLM交互的基础方法论 | 文献综述、选题对话、研究设计、学术写作 |
| RAG | 文献智能与知识管理核心技术 | 个人文献知识库、科研知识检索 |
| Agent | 科研自动化与流程编排 | 文献搜索Agent、数据采集Agent、分析Agent |
| Skill | 可复用的科研AI能力模块 | 文献综述skill、数据分析skill、写作skill |
| AI系统评估 | 科研质量保障方法 | 分析结果评估、AI辅助结论验证、偏见检测 |

**渐进融入节奏**：Prompt+AI辅助编程(W1起步) → RAG(W3文献综述) → Agent(W4发现空白) → Skill(W6-7研究实施) → AI系统评估(W7质量控制，嵌入各步验证)

## PBL框架

本课程以"构建个人AI4S工具栈并产出科研成果"为学期项目，每位博士生围绕自己的科研项目，逐步构建覆盖科研全流程的AI4S工具栈，学期末展示工具栈与科研产出。

| PBL要素 | 课程实现 |
|---|---|
| Authentic Problem | 博士生个人科研项目中的真实痛点与需求 |
| Sustained Inquiry | 9周持续构建，从文献智能到论文写作 |
| Student Voice & Choice | 工具栈围绕个人研究方向定制，兼顾定量与定性 |
| Reflection | 每阶段提交反思日志 |
| Critique & Revision | 跨学科同侪互评 + 教师反馈迭代 |
| Public Product | AI4S工具栈仓库 + 科研产出公开展示 |

## AI4S工具栈五模块（社科科研全流程，大模型贯穿支撑）

| 模块 | 科研环节 | 大模型赋能方式 | 共同AI工具支撑 | 关键工具/技术 |
|---|---|---|---|---|
| 1. 文献智能 | 文献检索→阅读→综述 | LLM辅助检索筛选、RAG构建个人知识库、AI综述生成 | RAG(知识库构建) + Prompt(综述生成) + Agent(文献搜索) | RAG+LLM、向量数据库、文献API |
| 2. 研究选题 | 发现空白→凝练问题 | LLM gap analysis、选题对话与验证、研究问题细化 | Prompt(gap analysis) + Agent(选题对话) | LLM对话式选题、文献gap挖掘 |
| 3. 研究设计 | 方法选择→框架搭建→假设推导 | LLM辅助方法匹配、理论框架构建、变量与测量设计 | Prompt(方法匹配) + Agent(设计顾问) + Skill(研究方案模板) | LLM研究设计顾问、因果推断方案 |
| 4. 研究实施 | 数据集构建→实证估计→经济学建模→仿真 | LLM辅助编程(Python/R/Stata)、AI辅助建模与仿真、质量控制嵌入各步验证 | AI辅助编程(代码生成) + Skill(能力封装) + Agent(流程编排) | LLM代码生成、AI数据分析、经济学建模、仿真实验 |
| 5. 论文写作 | 结构规划→撰写修订→格式发表 | LLM辅助各章节起草、学术润色、引用管理 | Prompt(学术写作) + AI辅助编程(LaTeX) + Skill(写作skill) | LLM学术写作、LaTeX+AI、格式化工具 |
| — | 全流程质量保障 | — | AI系统评估(结果验证、偏见检测、稳健性验证)，嵌入研究实施各步而非独立环节 | — |

## 9周课程安排

每周教学设计严格围绕**理念—工具—操作—交付成果**四核心，四核齐备且互相咬合：理念解释为什么用这个工具，工具支撑操作，操作产出交付物。

### Phase 1: Foundation（W1-3）— 工具准备 + 文献检索与综述

#### W1 工具准备 — AI工作环境搭建

| 要点 | 内容 |
|---|---|
| 科研步骤 | 工具准备 |
| 理念 | AI4S范式：AI贯穿科研全流程，是"研究伙伴"而非工具箱；人机交互的基本姿态（人判断、AI执行） |
| 工具 | opencode/cursor |
| 操作 | 配置AI工作环境、Python环境、API key、文献管理工具；写第一个Prompt驱动的小脚本 |
| 交付成果 | **工具环境就绪** |
| 课后自学 | Prompt Engineering方法论（`knowledge/m1-3-prompt-engineering.md`）、AI4S范式与方法论（`knowledge/m1-1-ai4s-paradigm.md`）、社科科研全流程映射（`knowledge/m1-4-research-workflow-mapping.md`） |
| 课后作业 | 用opencode/cursor完成一个Prompt驱动的小脚本（如调用LLM API总结一段文本），验证环境可用，为W2文献检索脚本做技术热身 |
| 参考资源 | 理念：Wang, H. et al. (2023). "Scientific discovery in the age of artificial intelligence." *Nature*, 620, 47-60；工具：[opencode文档](https://opencode.ai/docs/)、[Cursor文档](https://docs.cursor.com/) |

#### W2 文献检索 — 检索工具与策略

| 要点 | 内容 |
|---|---|
| 科研步骤 | 文献检索 |
| 理念 | 文献检索是方法论（PRISMA流程、检索式、纳入排除标准），不是"搜一下"；AI辅助筛选但人来定标准 |
| 工具 | 学术API（Semantic Scholar/Crossref/知网）、opencode检索脚本 |
| 操作 | 构建检索式、调用API批量获取文献元数据、AI辅助初筛 |
| 交付成果 | **文献检索工具列表**（数据库/API/工具/检索式/纳入排除标准）+ 原始文献库 |
| 课后自学 | 文献检索策略（`knowledge/m1-6-literature-search.md`）、AI辅助编程（`knowledge/m1-2-ai-coding.md`） |
| 课后作业 | 构建个人研究领域的检索式，用API批量获取至少20篇文献元数据，形成原始文献库 |
| 参考资源 | 理念：Page, M.J. et al. (2021). "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews." *BMJ*, 372, n71；工具：[Semantic Scholar API](https://api.semanticscholar.org/)、[Crossref REST API](https://www.crossref.org/services/metadata-delivery/rest-api/) |

#### W3 文献综述 — RAG知识库 + AI综述

| 要点 | 内容 |
|---|---|
| 科研步骤 | 文献综述 |
| 理念 | RAG改变文献管理范式：从"读完记住"到"检索即用"；综述是结构化综合而非摘抄堆砌 |
| 工具 | RAG（向量库/切分/检索）、AI综述生成 |
| 操作 | 构建个人文献知识库、AI辅助阅读与综述生成 |
| 交付成果 | **文献综述**（知识库代码 + 综述文稿） |
| 课后自学 | RAG原理与实践（`knowledge/m1-5-rag.md`）、AI辅助文献综述（`knowledge/m1-7-ai-literature-review.md`）、综述写作规范（`knowledge/m1-8-review-writing.md`） |
| 课后作业 | 构建RAG知识库（至少20篇文献），生成AI辅助综述初稿 |
| 参考资源 | 理念：Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2020*；工具：[LangChain文档](https://python.langchain.com/docs/)、[FAISS文档](https://faiss.ai/) |

### Phase 2: Design（W4-5）— 选题 + 研究设计

#### W4 发现空白→凝练问题 — gap analysis + 选题

| 要点 | 内容 |
|---|---|
| 科研步骤 | 发现空白→凝练问题 |
| 理念 | 选题是gap-driven而非兴趣-driven；AI辅助发现空白但研究价值由人判断 |
| 工具 | Agent（gap analysis agent、文献空白发现agent） |
| 操作 | LLM gap analysis对话、Agent辅助空白发现、选题可行性验证 |
| 交付成果 | **研究问题陈述**（gap分析 + 问题表述 + 研究意义） |
| 课后自学 | Gap analysis方法论（`knowledge/m2-1-gap-analysis.md`）、Prompt驱动gap分析（`knowledge/m2-2-prompt-gap-analysis.md`）、Agent辅助文献空白发现（`knowledge/m2-6-agent-topic-discovery.md`） |
| 课后作业 | 完成至少1轮LLM gap analysis多轮对话，形成研究问题陈述初稿 |
| 参考资源 | 理念：Sandberg, J. & Alvesson, M. (2011). "Ways of constructing research questions: gap-spotting or problematization?" *Organization*, 18(1), 23-44；工具：Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629 |

#### W5 研究设计 — 方法选择与规划

| 要点 | 内容 |
|---|---|
| 科研步骤 | 研究设计 |
| 理念 | "做对"比"做出来"重要；方法选择是研究者的核心判断，不可委托给AI；偏误自检是人机交互的关键素养 |
| 工具 | Agent深化（设计顾问）、批判性思维框架 |
| 操作 | LLM辅助方法匹配、理论框架构建、变量与测量设计、偏误自检 |
| 交付成果 | **研究设计方案**（假设、变量、数据需求、方法选择理由） |
| 课后自学 | 理论框架构建（`knowledge/m3-1-theoretical-framework.md`）、因果推断方法论（`knowledge/m3-2-causal-inference.md`）、批判性思维与判断（`knowledge/phase3-3b-critical-thinking.md`） |
| 课后作业 | 完成研究设计方案（理论框架、假设、变量、方法选择理由），提交偏误自检记录 |
| 参考资源 | 理念：Angrist, J.D. & Pischke, J.S. (2009). *Mostly Harmless Econometrics*. Princeton University Press；Kahneman, D. (2011). *Thinking, Fast and Slow*；工具：Paul, R. & Elder, L. (2014). *Critical Thinking: Tools for Taking Charge of Your Professional and Personal Life*. Pearson |

### Phase 3: Implementation（W6-7）— 研究实施

#### W6 研究实施（上）— 数据集 + 实证

| 要点 | 内容 |
|---|---|
| 科研步骤 | 研究实施（上）：数据集 + 实证 |
| 理念 | 数据集构建是研究实施基石（变量操作化、编码、清洗）；实证是经验检验，AI辅助编程但方法论判断在人 |
| 工具 | AI辅助编程深化（Python/R/Stata）、Skill（数据采集skill） |
| 操作 | 数据获取与清洗、变量操作化、实证估计（回归/DID/IV等）、数据验证、封装数据Skill |
| 交付成果 | 数据集 + 实证结果 + 数据Skill |
| 课后自学 | 数据集构建方法论（`knowledge/m4-1-data-collection.md`）、AI辅助编程深度应用（`knowledge/m4-2-ai-coding-advanced.md`）、Skill封装（`knowledge/m4-3-skill-data-collection.md`） |
| 课后作业 | 完成数据集构建与清洗、实证估计代码，封装数据采集Skill |
| 参考资源 | 理念：Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology*, 13(6), e1005510；工具：[opencode Skill文档](https://opencode.ai/docs/) |

#### W7 研究实施（下）— 经济学建模 + 仿真

| 要点 | 内容 |
|---|---|
| 科研步骤 | 研究实施（下）：经济学建模 + 仿真 |
| 理念 | 建模是对经验现象的理论抽象；仿真是用模型做反事实实验；质量控制嵌入各步验证而非独立环节；可审计性是科研诚信底线（dsh Trajectory演示锚定） |
| 工具 | Skill（分析skill）、AI辅助建模与仿真代码、dsh演示（Trajectory可审计理念） |
| 操作 | 经济学模型构建、参数标定、仿真实验（反事实/政策模拟）、模型验证与稳健性检验 |
| 交付成果 | **研究实施结果**（模型 + 仿真结果 + 验证报告 + 分析Skill） |
| 课后自学 | AI系统评估方法（`knowledge/m4-10-ai-evaluation.md`）、稳健性检验（`knowledge/m4-11-robustness-check.md`）、效度验证（`knowledge/m4-12-validity.md`） |
| 课后作业 | 完成经济学模型构建、仿真实验、验证报告，封装分析Skill |
| 参考资源 | 理念：Epstein, J.M. (2008). "Why Model?" *Journal of Artificial Societies and Social Simulation*, 11(4)；工具：[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) |

### Phase 4: Writing & Integration（W8-9）— 论文写作 + 整合展示

#### W8 论文写作（上）— 结构 + 起草

| 要点 | 内容 |
|---|---|
| 科研步骤 | 论文写作（上）：结构 + 起草 |
| 理念 | 学术写作是结构化表达而非自然语言流；AI辅助起草但人来把控论证逻辑 |
| 工具 | AI学术写作（结构/起草）、LaTeX+AI、Skill（写作skill） |
| 操作 | 各章节起草、LaTeX排版、五模块工具栈整合 |
| 交付成果 | 论文初稿 + AI4S工具栈v1 |
| 课后自学 | 学术写作规范（`knowledge/m5-1-academic-writing.md`）、LLM辅助学术写作（`knowledge/m5-2-llm-academic-writing.md`）、五模块整合（`knowledge/m5-6-ai4s-workflow-integration.md`） |
| 课后作业 | 完成论文各章节初稿，整合AI4S工具栈v1 |
| 参考资源 | 理念：Booth, W.C., Colomb, G.G. & Williams, J.M. (2008). *The Craft of Research*. University of Chicago Press；工具：[LaTeX文档](https://www.latex-project.org/)、[Overleaf文档](https://www.overleaf.com/learn) |

#### W9 论文写作（下）— 修订 + 展示

| 要点 | 内容 |
|---|---|
| 科研步骤 | 论文写作（下）：修订 + 展示 |
| 理念 | 科研成果需经同侪检验并公开；反思重构个人AI4S方法论框架 |
| 工具 | **工具栈最终形态**（整合定稿，非新引入） |
| 操作 | 同侪互评修订、工具栈最终整合、展示与反思 |
| 交付成果 | **论文终稿** + 工具栈仓库 + 反思报告 |
| 课后自学 | 反思方法论（`knowledge/m6-2-reflection.md`） |
| 课后作业 | 根据同侪互评修订论文终稿，完成工具栈最终整合与反思报告 |
| 参考资源 | 理念：Smith, R. (2006). "Peer review: a flawed process at the heart of science and the public sphere." *Journal of the Royal Society of Medicine*, 99(4), 178-182；工具：Sandve, G.K. et al. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLOS Computational Biology*, 9(10), e1003285 |

## 评分体系

| 类别 | 项目 | 权重 | 时间节点 | 说明 |
|---|---|---|---|---|
| 平时60% | 出勤与课堂参与 | 15% | 全程 | 9周出勤+课堂讨论参与度 |
| | 阶段成果一：文献综述 | 15% | W3 | 检索工具列表+RAG知识库+综述文稿 |
| | 阶段成果二：研究选题与研究设计 | 15% | W5 | gap分析+研究问题陈述+研究设计方案 |
| | 阶段成果三：个人科研工具栈汇总 | 15% | W8 | 五模块工具栈v1+案例与经验总结 |
| 期末40% | 个人科研报告 | 40% | W9 | 论文终稿+工具栈仓库+反思报告 |

## 关键设计原则

1. **科研全流程映射**：五模块对应社科科研的五个核心环节（文献→选题→设计→实施→写作），而非技术工具分类
2. **大模型贯穿支撑**：LLM在每个模块中既是工具也是"研究伙伴"，而非仅在代码层面辅助
3. **跨学科适配**：背景多样的社科博士生，工具栈需兼顾定量（计量/统计）与定性（文本/案例）研究范式
4. **个人项目驱动**：每位博士生围绕自己的科研项目构建工具栈，确保真实性与实用性
5. **方法论优先**：工具栈服务于研究方法论，而非技术炫技；AI辅助"做对"比"做出来"更重要
6. **AI基础工具栈渐进融入**：Prompt+AI辅助编程(W1起步) → RAG(W3文献综述) → Agent(W4发现空白) → Skill(W6-7研究实施) → AI系统评估(W7质量控制，嵌入各步验证)，工具随科研流程自然引入而非单独设课
7. **知识框架有机支撑**：科研方法论知识按五模块而非学科章节组织（见`knowledge-map.md`），通过科研阶段制造方法论缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply节奏），反思环节重构个人AI4S方法论框架（见`templates/reflection-log.md`），交付物锚定核心方法论概念（见`milestones.md`）
8. **四核设计原则**：每周教学设计严格围绕"理念—工具—操作—交付成果"四核心，四核齐备且互相咬合：理念解释为什么用这个工具，工具支撑操作，操作产出交付物。理念核涵盖科研方法论与AI辅助科研、人机交互两个维度

## 目录结构规划

```
ai4s/
├── ai4s-teaching-plan.md              # 本文件：AI4S课程教学方案
├── knowledge-map.md                    # 知识地图（按科研模块组织）
├── syllabus.md                         # 课程大纲
├── rubric.md                           # 评分标准
├── milestones.md                       # 阶段里程碑
├── ai-toolstack/                       # 共同AI基础工具栈教学材料
│   ├── ai-coding/                      # AI辅助编程(opencode/cursor)
│   ├── prompt-engineering/             # Prompt Engineering
│   ├── rag/                            # RAG原理与实践
│   ├── agent/                          # Agent设计与开发
│   ├── skill/                          # Skill封装与复用
│   └── ai-evaluation/                  # AI系统评估
├── templates/
│   ├── research-needs.md               # 科研需求清单模板
│   ├── toolstack-blueprint.md          # 工具栈蓝图模板
│   ├── reflection-log.md               # 反思日志模板
│   ├── peer-review.md                  # 同侪互评模板
│   └── final-report.md                 # 最终报告模板
├── weeks/
│   ├── week01/
│   │   ├── lecture.md
│   │   ├── lab.md
│   │   └── resources.md
│   ├── ...                             # week02-week09
├── toolstack-examples/                 # AI4S工具栈示例
│   ├── literature-rag/                 # 文献智能示例
│   ├── topic-selection/                # 研究选题示例
│   ├── research-design/                # 研究设计示例
│   ├── implementation/                 # 研究方案实施示例
│   └── ai-writing/                     # 论文写作示例
└── data/                               # 示例数据集
