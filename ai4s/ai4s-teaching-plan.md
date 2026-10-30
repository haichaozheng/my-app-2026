# 人工智能大模型应用 — AI4S PBL教学方案

## 课程信息

- **面向对象**：社科类博士生（背景多样：经济学、社会学、政治学、管理学、传播学等）
- **课程目标**：围绕学生个人科研项目构建AI4S工具栈，并应用该工具栈开展科研；进而在AI辅助社会科研的**方法论层面**建立自觉——理解社会计算带来的范式转移，能对自己的AI辅助科研过程做方法论审视与论证
- **教学方法**：Project Based Learning（PBL）
- **课程时长**：9周
- **项目形式**：个人项目为主，每位博士生围绕自己的科研项目独立构建工具栈
- **技术栈**：大模型贯穿全程，作为AI4S工具栈的核心支撑
- **先修要求**：学生有一定Python基础和大模型使用经验

## 方法论基础：社会计算与经典文献阅读

本课程不止于"会用工具"，更要求学生在**AI辅助社会科研的方法论层面**建立自觉：理解社会计算（以大数据与人工智能算法研究社会、经济与管理）为社会科学带来的范式转移，在工具栈的每一步都能对自己的研究过程做方法论审视。方法论内容不单独设课，以"核心参考书 + 经典文献"方式随五模块渐进融入，反思日志需回应当周方法论阅读。

**核心参考书**：罗家德、高馨、刘济帆、傅晓明.《社会计算方法论：社会科学研究的一次范式转移》. 清华大学出版社, 2026. [图书主页](https://www.tup.com.cn/bookscenter/book_11246901.html)（智能社会科学丛书）

该书的主线**"理论、数据挖掘与建模的三角对话"**正是本课程的人机交互姿态——理论（人）引导、计算（AI）执行、在反复对话中逼近"做对"的研究；其梳理的社会计算六类研究方法范式，为各模块提供方法论坐标。

**经典文献阅读清单**（随周次渐进）：

| 周次 | 文献 | 阅读锚点 |
|---|---|---|
| W1 | 罗家德等（2026）第1-2章：范式又一次转移 / 一切以理论为基础 | 社会计算的内涵与范式定位，锚定课程的人机交互姿态 |
| W1 | Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915), 721-723 | 计算社会科学的诞生宣言：新数据、新工具、新问题 |
| W3 | 罗家德等（2026）第3章：三角对话 | 理论引导下的社会计算方法论，呼应综述的结构化综合 |
| W4 | 罗家德等（2026）第4章：社会计算驱动的研究方法 | 研究类型图谱，为gap类型标注提供坐标系 |
| W5 | 罗家德等（2026）第5章：理论探索的范式 | 反复三角对话的研究设计案例，呼应"生成→审计→裁决"循环 |
| W6 | Argyle, L.P. et al. (2023). "Out of One, Many: Using Language Models to Simulate Human Samples." *Political Analysis*, 31(3), 337-351 | 类人调研数据（silicon sampling）的方法论先例：算法保真度、条件化、适用边界 |
| W7 | Lazer, D. et al. (2020). "Computational social science: Obstacles and opportunities." *Science*, 369(6507), 1060-1062 | 范式十年反思：数据质量、伦理、可复现性 |
| W8-9 | 罗家德等（2026）第6章：验证理论的范式 | 验证性研究的方法论，呼应实证收尾与论文写作 |
| 延伸 | Salganik, M.J. (2018). *Bit by Bit: Social Research in the Digital Age*. Princeton University Press | 数字时代社会研究设计的系统参考书 |

## 共同AI基础工具栈

两门课程共享以下AI基础工具栈，随科研流程**渐进式融入**教学内容，而非单独设课：

| 工具 | 在课程中的角色 | 主要应用场景 |
|---|---|---|
| AI辅助编程(opencode/cursor) | 科研编程生产力工具 | Python/R/Stata代码生成、调试、迭代 |
| Prompt Engineering | 与LLM交互的基础方法论 | 文献综述、选题对话、研究设计、学术写作 |
| RAG | 文献智能与知识管理核心技术 | 个人文献知识库、科研知识检索 |
| Agent | 科研自动化与流程编排 | gap分析多智能体（W4）、研究设计生成-审计多智能体（W5）、调研数据生成Agent（W6）、分析Agent（W7）、写作-审计双Agent（W8） |
| Skill | 可复用的科研AI能力模块 | 文献综述skill、数据分析skill、写作skill、论文评审skill |
| AI系统评估 | 科研质量保障方法 | 分析结果评估、AI辅助结论验证、偏见检测 |

**渐进融入节奏**：Prompt+AI辅助编程(W1起步) → RAG(W3文献综述) → Agent(W4-W5 选题gap分析多智能体与研究设计生成-审计多智能体，W6-W8延续：调研数据生成/分析/写作-审计双Agent) → Skill(W6-7研究实施、W9论文评审) → AI系统评估(W7质量控制，嵌入各步验证)

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
| 2. 研究选题 | 发现空白→凝练问题 | 多智能体gap分析流水线（抽取→标注→核验→侦察→凝练→留痕），产出带证据锚点的Gap证据表 | Prompt(gap analysis) + Agent(主Agent+六子智能体) | gap analysis多智能体系统（opencode agents） |
| 3. 研究设计 | 方法选择→框架搭建→假设推导 | 学生为自己的研究方法构建可被智能体加载、可随研究修订的**审计配置**；"生成草案→审计追问→学生裁决→定稿"循环 | Agent(五层五角色设计-审计架构) + Skill(方法审计配置) | 方法条目路由、检索型审计、置信度标注、修订痕迹 |
| 4. 研究实施 | 数据集构建→实证估计→仿真 | 数据来源三路径（第三方数据集/自采实验/智能体辅助调研生成类人数据）；AI辅助编程(Python/R/Stata)、agent-native计量（StatsPAI）、基于Mesa的智能体仿真（规则驱动基线 + LLM智能体仿真）、质量控制嵌入各步验证 | AI辅助编程(代码生成) + Agent(调研数据生成、流程编排) + Skill(能力封装) | StatsPAI（因果推断与计量）、LLM代码生成、AI数据分析、Mesa（ABM仿真）、Mesa-LLM（LLM智能体仿真） |
| 5. 论文写作 | 结构规划→撰写修订→格式发表 | 写作-审计双Agent（生成与核验分离）、LLM辅助各章节起草、学术润色、引用核验与文献管理、模拟评审 | Prompt(学术写作) + Agent(写作Generator + 引用/复现性Auditor) + Skill(写作skill、论文评审skill) | LLM学术写作、LaTeX+AI（texai类工作流）、Zotero MCP、格式化工具 |
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

#### W4 发现空白→凝练问题 — gap analysis + 选题（多智能体）

| 要点 | 内容 |
|---|---|
| 科研步骤 | 发现空白→凝练问题 |
| 理念 | 选题是gap-driven而非兴趣-driven；AI辅助发现空白但研究价值由人判断；多智能体分工的价值在于把"发现空白"从一次对话升级为一条有证据锚点、可核验、可审计的流水线 |
| 工具 | Agent（1个主Agent编排 + 6个子智能体协作，基于[opencode agents](https://opencode.ai/v2/docs/agents/)的primary/subagent模式实现） |
| 操作 | 配置并运行gap分析多智能体：主Agent推进"抽取→标注→核验→侦察→凝练"流程并传递上下文，子智能体各司其职，Audit Scribe全程留痕；学生阅读智能体输出并对关键节点做人工裁决 |
| 交付成果 | **研究问题陈述**（gap分析 + 问题表述 + 研究意义）+ Gap证据表与协变量结构（与问题陈述共同构成W5输入）+ 子智能体核验日志与人工修正点记录 |
| 课后自学 | Gap analysis方法论（`knowledge/m2-1-gap-analysis.md`）、Prompt驱动gap分析（`knowledge/m2-2-prompt-gap-analysis.md`）、Agent辅助文献空白发现（`knowledge/m2-6-agent-topic-discovery.md`）、罗家德等（2026）第3-4章 |
| 课后作业 | 运行gap分析多智能体完成至少1轮完整流程，对Verifier与Feasibility Scout的输出做人工裁决并记录修正点，形成研究问题陈述初稿（含Gap证据表与协变量结构） |
| 参考资源 | 理念：Sandberg, J. & Alvesson, M. (2011). "Ways of constructing research questions: gap-spotting or problematization?" *Organization*, 18(1), 23-44；工具：[opencode Agents文档](https://opencode.ai/v2/docs/agents/)、Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629 |

**W4 Gap分析多智能体架构**（1主 + 6子；主Agent只编排不生成内容，子智能体各受权限约束）：

| 角色 | 模式 | 职责 |
|---|---|---|
| 主Agent（编排） | primary | 推进"抽取→标注→核验→侦察→凝练"流程，向子智能体传递综述语料与上下文 |
| Gap Extractor | subagent | 从综述中抽取gap候选，标注类型与锚点（文献、章节、页码） |
| Innovation Mapper | subagent | 标注创新类型、最近邻对比、差异声明 |
| Verifier | subagent | 新颖性三档核验：伪空白 / 相邻 / 候选真空白 |
| Feasibility Scout | subagent | 数据、方法、时间、伦理四维侦察，输出MVR（最小可行研究）建议 |
| Prober | subagent | 条件化 + 科创凝练追问（把gap逼成可研究的问题） |
| Audit Scribe | subagent | 记录证据锚点、核验日志、人工修正点 |

#### W5 研究设计 — 方法审计配置与"生成→审计→裁决→定稿"循环

| 要点 | 内容 |
|---|---|
| 科研步骤 | 研究设计 |
| 理念 | "做对"比"做出来"重要；方法选择是研究者的核心判断，不可委托给AI。本周**不教"所有方法"**，而是让学生为自己的研究方法构建**可被智能体加载、可随研究修订的审计配置**——方法知识在审计追问中按需检索、在裁决中内化；偏误自检是人机交互的关键素养 |
| 工具 | Agent深化（五层五角色设计-审计架构，基于[opencode agents](https://opencode.ai/v2/docs/agents/)实现）、检索型审计（方法论先例 / 文献证据 / 复现性检查三类工具与MCP） |
| 操作 | 携W4输出进入五阶段循环（见下）：路由确认→草案生成→检索型审计→学生裁决与定稿→记录与交付；每个字段显式确认或标记待定，大幅修改触发Generator局部重生成 |
| 交付成果 | **研究设计方案**（逐字段带依据、置信度标注、待核验点、修订痕迹）+ 个人**方法审计配置**（可被智能体加载、可随研究修订） |
| 课后自学 | 理论框架构建（`knowledge/m3-1-theoretical-framework.md`）、因果推断方法论（`knowledge/m3-2-causal-inference.md`）、批判性思维与判断（`knowledge/phase3-3b-critical-thinking.md`）、罗家德等（2026）第4-5章 |
| 课后作业 | 完成五阶段循环至少一轮：产出研究设计方案定稿（含裁决记录与修订历史），提交方法审计配置v1与偏误自检记录 |
| 参考资源 | 理念：Angrist, J.D. & Pischke, J.S. (2009). *Mostly Harmless Econometrics*. Princeton University Press；Kahneman, D. (2011). *Thinking, Fast and Slow*；工具：[opencode Agents文档](https://opencode.ai/v2/docs/agents/)、Paul, R. & Elder, L. (2014). *Critical Thinking: Tools for Taking Charge of Your Professional and Personal Life*. Pearson |

**W5 五阶段流程**：

```
W4 输入（问题陈述 + 协变量结构 + Gap 证据表）
        ↓
① 路由确认：学生确认方法条目 → 加载设计模板结构与追问规则
        ↓
② 草案生成：Design Draft Generator 产出完整设计草案（逐字段带依据/置信度/待核验点）
        ↓
③ 检索型审计：Auditor 逐字段追问 → 按需调用工具/MCP检索方法论先例、文献证据、复现性检查
              → 带证据再追问或提改进建议 → 用户裁决/修改指令 → 受控写回 → 重新追问
        ↓
④ 学生裁决与定稿：每个字段显式确认或标记待定；大幅修改触发 Generator 局部重生成
        ↓
⑤ 记录与交付：Scribe 整理草案、diff、检索证据、裁决理由、修订历史
```

**W5 Agent架构（五层五角色）**：

| 层 | 角色 | 模式 | 职责 | 权限纪律 |
|---|---|---|---|---|
| 编排层 | W5-Lead | primary | 推进五阶段流程，传递W4输入和路由条目 | 不调MCP、不写文件、不做判断；subagent白名单仅允许下列四个 |
| 路由层 | Router | subagent | 按条目元类别标签加载设计模板结构与追问规则 | 只选文件，不生成内容 |
| 生成层 | Design Draft Generator | subagent | 主动生成完整设计草案，逐字段标注依据、置信度、待核验点 | 可读W3/W4输入与路由条目；可调学术搜索MCP查先例；只写草案 |
| 审计层 | Auditor | subagent | 按字段追问；按需调用工具/MCP检索证据；执行用户明确指令的受控写回；对修改后字段重新追问 | 可调方法论/文献/复现性三类工具；检索结果只构成建议，不直接写回；写回仅限被追问字段及其直接依赖字段，且须用户指令触发 |
| 记录层 | Audit Scribe | subagent | 记录草案、diff、用户原话、修改理由、检索证据引用、新待核验点、修订历史 | 只写不读，不调MCP |

### Phase 3: Implementation（W6-7）— 研究实施

#### W6 研究实施（上）— 数据集（三路径）+ 实证（StatsPAI）

| 要点 | 内容 |
|---|---|
| 科研步骤 | 研究实施（上）：数据集 + 实证 |
| 理念 | 数据集构建是研究实施基石（变量操作化、编码、清洗）；数据来源有**三路径**——第三方数据集、自己采集实验、大模型智能体辅助调研生成类人数据——各有适用场景、效度边界与伦理要求，选择本身是方法论判断；实证是经验检验，AI辅助编程但方法论判断在人 |
| 工具 | AI辅助编程深化（Python/R/Stata）、**StatsPAI**（agent-native因果推断与计量库）、Skill（数据采集skill） |
| 操作 | 按研究问题选择数据路径（见下"三路径"）并论证理由；数据获取与清洗、变量操作化；用StatsPAI实施实证估计（回归/DID/IV/断点回归/合成控制/匹配/DML等）并导出出版级表格；数据验证、封装数据Skill |
| 交付成果 | 数据集（含**数据来源路径选择说明**）+ 实证结果（StatsPAI代码与表格）+ 数据Skill |
| 课后自学 | 数据集构建方法论（`knowledge/m4-1-data-collection.md`）、AI辅助编程深度应用（`knowledge/m4-2-ai-coding-advanced.md`）、Skill封装（`knowledge/m4-3-skill-data-collection.md`） |
| 课后作业 | 完成数据集构建与清洗（说明数据来源路径及选择理由），用StatsPAI完成实证估计并导出表格，封装数据采集Skill |
| 参考资源 | 理念：Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology*, 13(6), e1005510；Argyle, L.P. et al. (2023). "Out of One, Many: Using Language Models to Simulate Human Samples." *Political Analysis*, 31(3), 337-351；工具：[StatsPAI](https://github.com/brycewang-stanford/statspai)、[opencode Skill文档](https://opencode.ai/docs/) |

**W6 数据来源三路径**（选择须与研究设计W5的审计配置一致，并在交付物中论证）：

| 路径 | 做法 | 关键要求 |
|---|---|---|
| 第三方数据集 | 公开数据库（如CFPS/CGSS/CHFS等）与文献配套数据 | 数据质量与适配性论证、变量操作化映射、引用与授权合规 |
| 自己采集实验 | 实验、问卷、访谈等一手数据采集 | 变量操作化与测量信效度、样本设计、伦理审查 |
| 智能体辅助调研生成类人数据 | 用LLM智能体模拟受访者（silicon sampling），辅助问卷预测试、情景预演、低成本先验估计 | 须与真实数据校准（算法保真度）、显式声明生成属性、不得替代需要真实人类被试的因果推断 |

**W6 StatsPAI接入**（agent-native实证工作台）：

- **定位**：Stanford REAP团队开发、发表于JOSS的Python因果推断与计量库，把Stata/R常用工作流（`regress`/`ivregress`/`reghdfe`/`csdid`/`rdrobust`/`synth`/`psmatch2`/DML等）原生带到Python，统一API + 结构化结果对象 + 出版级表格导出（`sp.regtable()` → Word/Excel/LaTeX）
- **与学生W5产出的衔接**：实证方法以研究设计中经审计确认的方法条目为准，用StatsPAI对应估计器实施；每个估计器带`validation_status`（是否与Stata/R数值对齐），呼应W5的可审计姿态——哪个数字可信、凭什么可信，须可查证
- **agent-native用法**：每个公开函数有机器可读schema（`sp.list_functions()`/`sp.describe_function()`），自带`statspai-mcp`服务器，让opencode/cursor中的智能体直接调用估计器（detect→estimate→audit循环）；自带的14个经典数据集（Card 1995、LaLonde/NSW、mpdta等）可作课堂锚定练习

#### W7 研究实施（下）— 仿真（Mesa + LLM智能体）

| 要点 | 内容 |
|---|---|
| 科研步骤 | 研究实施（下）：仿真 |
| 理念 | 仿真是用模型做反事实实验：先跑通规则驱动的基线模型，再把LLM嵌入决策环节，从"if-then规则智能体"走向"语言推理智能体"，观察智能体行为与涌现结果有何不同；每一次LLM调用都须记录（谁在什么状态下说了什么、做了什么），可审计性是科研诚信底线；本周不单独教经济学建模，理论抽象体现在模型的规则与交互设计中 |
| 工具 | **Mesa**（Python智能体建模ABM框架：核心组件、Solara浏览器可视化、内置数据采集与分析）、**Mesa-LLM**（把LLM直接接入Mesa智能体的决策与通信）、Skill（分析skill） |
| 操作 | 模块一：跑通规则驱动的Mesa基线模型（智能体行为用显式规则实现，理解Model/Agent/AgentSet/DataCollector基本盘）；模块二：接入Mesa-LLM，把LLM嵌入智能体决策环节，运行仿真并记录每一次LLM调用；对比规则驱动与LLM驱动两种实现的涌现结果，做模型验证与稳健性检验 |
| 交付成果 | **研究实施结果**（Mesa基线模型 + Mesa-LLM仿真结果 + LLM调用日志 + 验证报告 + 分析Skill） |
| 课后自学 | AI系统评估方法（`knowledge/m4-10-ai-evaluation.md`）、稳健性检验（`knowledge/m4-11-robustness-check.md`）、效度验证（`knowledge/m4-12-validity.md`） |
| 课后作业 | 完成Mesa基线模型与Mesa-LLM接入两种实现，提交LLM调用日志与对比分析、验证报告，封装分析Skill |
| 参考资源 | 理念：Epstein, J.M. (2008). "Why Model?" *Journal of Artificial Societies and Social Simulation*, 11(4)；工具：[Mesa文档](https://mesa.readthedocs.io/latest/)、[Mesa-LLM](https://github.com/mesa/mesa-llm)、[Mesa-LLM文档](https://mesa-llm.readthedocs.io/) |

**W7 仿真两模块路线**（先基线后LLM，两步都围绕学生的研究问题）：

| 模块 | 定位 | 关键内容 |
|---|---|---|
| 模块一：Mesa基线 | 先跑通一个**规则驱动**的模型，建立ABM基本盘 | 按研究问题定义智能体类型、状态与交互规则；用Mesa 3核心组件（Agent/Model/AgentSet调度、空间网格）搭建模型；DataCollector采集指标，Solara浏览器可视化；以基线涌现结果为后续对照 |
| 模块二：Mesa-LLM接入 | 把LLM嵌入智能体的**决策环节**，并记录每一次调用 | 用Mesa-LLM把LLM接入智能体决策与智能体间通信（支持OpenAI/Anthropic/Gemini/Ollama等provider）；替换或混合规则决策与LLM决策；对每次LLM调用留痕（时间步、智能体状态、prompt、回复、行动），调用日志与仿真数据一并交付，支撑复现与审计 |

> 注：Mesa-LLM仍处于活跃开发期（API可能变动），课程统一固定版本（`pip install -U mesa-llm`后锁定版本号）并在实验报告中记录所用版本，本身即是可复现性训练的一环。

### Phase 4: Writing & Integration（W8-9）— 论文写作 + 整合展示

#### W8 论文写作（上）— LaTeX + AI Agent 协作写作

| 要点 | 内容 |
|---|---|
| 科研步骤 | 论文写作（上）：结构 + 起草 |
| 理念 | 学术写作是结构化表达而非自然语言流；AI辅助起草但人来把控论证逻辑。写作阶段最高风险的**"验证缺口"是引用**——Agent生成的引用可能凭空捏造（幻觉引用），因此本周把"生成"与"核验"拆成**两个权限互斥的角色**：Generator不拥有网络与核验权，Auditor只核验不下结论，引用核验结论必须可回溯到Zotero/DOI；AI使用声明对照W1-W7审计记录逐项起草，把全程人机协作痕迹制度化 |
| 工具 | Agent深化（写作-审计双Agent架构，基于[opencode agents](https://opencode.ai/v2/docs/agents/)的primary/subagent模式实现）、LaTeX+AI（**texai类工作流**：直接编辑.tex、每一处修改在PDF上可见）、Zotero MCP（引用管理）、Skill（写作skill） |
| 操作 | 学生担任编排与裁决人，运行写作双Agent流程：Writing Generator按章节生成LaTeX草稿、润色段落、生成表格、插入Zotero引用；Citation & Reproducibility Auditor逐条核验引用DOI/元数据、检查复现包完整性、起草AI使用声明并逐项对照W1-W7审计记录；学生对引用去留与AI声明做人工裁决；五模块工具栈整合 |
| 交付成果 | 论文初稿（LaTeX+PDF，AI修改可见）+ **引用核验报告**（逐条DOI/元数据核验状态）+ 复现包完整性清单 + AI使用声明草稿 + AI4S工具栈v1 |
| 课后自学 | 学术写作规范（`knowledge/m5-1-academic-writing.md`）、LLM辅助学术写作（`knowledge/m5-2-llm-academic-writing.md`）、五模块整合（`knowledge/m5-6-ai4s-workflow-integration.md`） |
| 课后作业 | 用双Agent工作流完成论文初稿：Generator起草各章节，Auditor核验全部Agent插入的引用并产出复现包完整性清单，学生裁决引用去留并定稿AI使用声明，整合AI4S工具栈v1 |
| 参考资源 | 理念：Booth, W.C., Colomb, G.G. & Williams, J.M. (2008). *The Craft of Research*. University of Chicago Press；工具：[LaTeX文档](https://www.latex-project.org/)、[Overleaf文档](https://www.overleaf.com/learn)、[Zotero MCP](https://github.com/54yyyu/zotero-mcp) |

**W8 写作-审计双Agent架构**（生成与核验分离、权限互斥；学生担任primary编排与最终裁决）：

| 角色 | 模式 | 职责 | 关键权限纪律 |
|---|---|---|---|
| Writing Generator | subagent | 按章节生成LaTeX草稿、润色段落、生成表格、插入Zotero引用；在texai类工作流中直接编辑.tex，但每一处修改在PDF上可见 | 不拥有shell/网络权限（优先使用texai的受限模式）；不生成"引用核验通过"的结论 |
| Citation & Reproducibility Auditor | subagent | 逐条核验Agent插入引用的DOI/元数据；检查复现包完整性；生成AI使用声明草稿并逐项对照W1—W7审计记录 | 可调Zotero MCP/学术搜索MCP做核验；不判断"复现成功"，只标记核验状态和完整性缺口 |

#### W9 论文写作（下）— 修订 + 展示

| 要点 | 内容 |
|---|---|
| 科研步骤 | 论文写作（下）：修订 + 展示 |
| 理念 | 科研成果需经同侪检验并公开；**论文评审skill**把"审稿人视角"封装为可复用能力——在正式投稿前用评审规范对初稿做结构化模拟评审，让修订有据可依；AI辅助评审但接受与回应评审意见的判断在人；反思重构个人AI4S方法论框架 |
| 工具 | **论文评审skill**（把同侪评审规范封装为可复用skill：结构/论证/贡献/方法/写作五维评审提示 + AI使用声明核验清单）、**工具栈最终形态**（整合定稿，非新引入） |
| 操作 | 用论文评审skill对初稿做模拟评审（逐维生成评审意见草稿并标注依据锚点）；结合同侪互评修订论文终稿；用评审skill的AI使用声明核验清单复核W8声明；工具栈最终整合、展示与反思 |
| 交付成果 | **论文终稿** + 论文评审skill + 模拟评审意见与修订对照记录 + 工具栈仓库 + 反思报告 |
| 课后自学 | 反思方法论（`knowledge/m6-2-reflection.md`） |
| 课后作业 | 封装论文评审skill，用它生成模拟评审意见；结合同侪互评与模拟评审修订论文终稿，完成工具栈最终整合与反思报告 |
| 参考资源 | 理念：Smith, R. (2006). "Peer review: a flawed process at the heart of science and the public sphere." *Journal of the Royal Society of Medicine*, 99(4), 178-182；工具：Sandve, G.K. et al. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLOS Computational Biology*, 9(10), e1003285、[opencode Skill文档](https://opencode.ai/docs/) |

## 评分体系

| 类别 | 项目 | 权重 | 时间节点 | 说明 |
|---|---|---|---|---|
| 平时60% | 出勤与课堂参与 | 15% | 全程 | 9周出勤+课堂讨论参与度 |
| | 阶段成果一：文献综述 | 15% | W3 | 检索工具列表+RAG知识库+综述文稿 |
| | 阶段成果二：研究选题与研究设计 | 15% | W5 | gap多智能体分析+研究问题陈述（含Gap证据表与协变量结构）+研究设计方案（含方法审计配置、置信度标注与修订痕迹） |
| | 阶段成果三：个人科研工具栈汇总 | 15% | W8 | 五模块工具栈v1（含论文初稿、引用核验报告、复现包完整性清单、AI使用声明草稿）+案例与经验总结 |
| 期末40% | 个人科研报告 | 40% | W9 | 论文终稿+工具栈仓库+反思报告 |

## 关键设计原则

1. **科研全流程映射**：五模块对应社科科研的五个核心环节（文献→选题→设计→实施→写作），而非技术工具分类
2. **大模型贯穿支撑**：LLM在每个模块中既是工具也是"研究伙伴"，而非仅在代码层面辅助
3. **跨学科适配**：背景多样的社科博士生，工具栈需兼顾定量（计量/统计）与定性（文本/案例）研究范式
4. **个人项目驱动**：每位博士生围绕自己的科研项目构建工具栈，确保真实性与实用性
5. **方法论优先**：工具栈服务于研究方法论，而非技术炫技；AI辅助"做对"比"做出来"更重要；以社会计算方法论（罗家德等2026"三角对话"）与经典文献阅读为方法论支撑，让学生在范式转移的自觉中做AI辅助科研
6. **AI基础工具栈渐进融入**：Prompt+AI辅助编程(W1起步) → RAG(W3文献综述) → Agent(W4-W5 选题gap分析多智能体与研究设计生成-审计多智能体) → Skill(W6-7研究实施) → AI系统评估(W7质量控制，嵌入各步验证)，工具随科研流程自然引入而非单独设课
7. **知识框架有机支撑**：科研方法论知识按五模块而非学科章节组织（见`knowledge-map.md`），通过科研阶段制造方法论缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply节奏），反思环节重构个人AI4S方法论框架（见`templates/reflection-log.md`），交付物锚定核心方法论概念（见`milestones.md`）
8. **四核设计原则**：每周教学设计严格围绕"理念—工具—操作—交付成果"四核心，四核齐备且互相咬合：理念解释为什么用这个工具，工具支撑操作，操作产出交付物。理念核涵盖科研方法论与AI辅助科研、人机交互两个维度
9. **多智能体权限纪律**：W4/W5/W8的多智能体系统遵循"主Agent只编排不做判断、子智能体各受权限约束、检索结果只构成建议不直接写回、关键裁决留给学生"的纪律，把可审计的人机交互制度化——学生交付的不只是结果，更是带证据锚点、置信度标注与修订痕迹的科研过程；W8写作阶段额外遵循**生成与核验分离**：Generator不拥有网络与核验权、不生成"引用核验通过"的结论，Auditor只标记核验状态与完整性缺口、不判断"复现成功"

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
