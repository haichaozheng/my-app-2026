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
| AI辅助编程(opencode/cursor/trae) | 科研编程生产力工具 | Python/R/Stata代码生成、调试、迭代 |
| Prompt Engineering | 与LLM交互的基础方法论 | 文献综述、选题对话、研究设计、学术写作 |
| RAG | 文献智能与知识管理核心技术 | 个人文献知识库、科研知识检索 |
| Agent | 科研自动化与流程编排 | 文献搜索Agent、数据采集Agent、分析Agent |
| Skill | 可复用的科研AI能力模块 | 文献综述skill、数据分析skill、写作skill |
| AI系统评估 | 科研质量保障方法 | 分析结果评估、AI辅助结论验证、偏见检测 |

**渐进融入节奏**：Prompt+AI辅助编程(W1起步) → RAG(W2文献智能) → Agent(W4研究设计) → Skill(W5-6方案实施) → AI系统评估(W7质量控制)

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
| 4. 研究方案实施 | 数据采集→编码分析→结果解读 | LLM辅助编程(Python/R/Stata)、自动化数据采集、AI解读结果 | AI辅助编程(代码生成) + Skill(分析skill封装) + Agent(数据采集) | LLM代码生成、AI数据分析、质量控制 |
| 5. 论文写作 | 结构规划→撰写修订→格式发表 | LLM辅助各章节起草、学术润色、引用管理 | Prompt(学术写作) + AI辅助编程(LaTeX) + Skill(写作skill) | LLM学术写作、LaTeX+AI、格式化工具 |
| — | 全流程质量保障 | — | AI系统评估(结果验证、偏见检测、稳健性检验) | — |

## 9周课程安排

### Phase 1: Foundation（W1-2）— AI4S框架 + 文献智能

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W1 | AI4S概论 + Prompt Engineering + AI辅助编程 | AI4S理念、社科科研全流程映射、Prompt Engineering方法论（系统Prompt、多轮对话、Deep Research）、AI辅助编程环境搭建(opencode/cursor/trae) | 梳理个人科研现状与痛点、用AI辅助编程搭建科研工具栈骨架 | 个人科研需求清单 |
| W2 | 文献智能模块 + RAG | RAG原理与实践（向量数据库、文档切分、检索策略）、构建个人文献知识库、AI辅助文献综述、用opencode/cursor构建RAG知识库代码 | 构建RAG知识库、生成AI综述 | 文献知识库 + AI综述初稿 |

### Phase 2: Design（W3-4）— 选题 + 研究设计

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W3 | 研究选题模块 + Prompt与Agent | LLM辅助gap analysis、选题对话与验证、研究问题凝练、Prompt驱动的gap analysis对话、Agent辅助文献空白发现 | 用LLM发现研究空白、细化研究问题、用Prompt对话验证选题可行性 | 研究选题报告（含gap分析） |
| W4 | 研究设计模块 + Agent | LLM辅助方法选择、理论框架构建、变量与测量设计、因果推断方案、Agent概念与科研Agent设计、用Agent探索研究设计方案 | 用LLM设计研究框架与方案、用Agent辅助设计方案探索 | 研究设计方案（含假设、变量、数据需求） |

### Phase 3: Implementation（W5-7）— 研究方案实施

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W5 | 数据采集 + AI辅助编程 + Skill | AI辅助数据获取(API/爬虫/NLP文本提取)、LLM代码生成(Python/R/Stata)深度应用、Skill概念与封装方法 | 执行数据采集、完成核心分析代码、封装数据采集Skill | 数据集 + 分析代码 + 数据采集Skill |
| W6 | 数据分析与AI解读 + Skill与Agent编排 | LLM辅助数据分析、结果解读与验证、定量/定性方法AI赋能、Skill封装分析能力、Agent编排分析流程 | 运行分析、AI辅助解读结果、构建数据分析Skill、编排分析Agent | 分析结果 + AI解读报告 + 分析Skill |
| W7 | 质量控制与迭代 + AI系统评估 | AI辅助稳健性检验、效度验证、替代方案探索、AI系统评估方法（结果可信度评估、偏见检测、稳健性验证） | 迭代优化分析、验证结果、用AI系统评估方法验证分析结果 | 稳健性检验 + 最终结果 + 评估报告 |

### Phase 4: Writing & Integration（W8-9）— 论文写作 + 整合展示

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W8 | 论文写作模块 + 工具栈整合 | LLM辅助学术写作（结构/起草/修订）、五模块整合为统一AI4S工作流、Skill封装写作能力 | 撰写论文初稿、整合工具栈 | 论文初稿 + AI4S工具栈v1 |
| W9 | 展示与反思 | — | 展示AI4S工具栈+科研产出、同侪互评 | 工具栈仓库 + 科研产出 + 反思报告 |

## 评分体系

| 评分维度 | 权重 | 说明 |
|---|---|---|
| AI4S工具栈完整性 | 25% | 五模块是否完整构建、大模型与共同AI工具是否有效贯穿 |
| 科研产出质量 | 25% | 论文/报告的学术质量与规范 |
| 研究过程与方法论 | 20% | 选题→设计→实施→写作全链条的规范性 |
| 同侪互评 | 15% | 跨学科视角互评工具栈与产出 |
| 最终反思报告 | 15% | 对AI4S赋能社科科研的深度反思 |

## 关键设计原则

1. **科研全流程映射**：五模块对应社科科研的五个核心环节（文献→选题→设计→实施→写作），而非技术工具分类
2. **大模型贯穿支撑**：LLM在每个模块中既是工具也是"研究伙伴"，而非仅在代码层面辅助
3. **跨学科适配**：背景多样的社科博士生，工具栈需兼顾定量（计量/统计）与定性（文本/案例）研究范式
4. **个人项目驱动**：每位博士生围绕自己的科研项目构建工具栈，确保真实性与实用性
5. **方法论优先**：工具栈服务于研究方法论，而非技术炫技；AI辅助"做对"比"做出来"更重要
6. **AI基础工具栈渐进融入**：Prompt+AI辅助编程(W1起步) → RAG(W2文献智能) → Agent(W4研究设计) → Skill(W5-6方案实施) → AI系统评估(W7质量控制)，工具随科研流程自然引入而非单独设课
7. **知识框架有机支撑**：科研方法论知识按五模块而非学科章节组织（见`knowledge-map.md`），通过科研阶段制造方法论缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply节奏），反思环节重构个人AI4S方法论框架（见`templates/reflection-log.md`），交付物锚定核心方法论概念（见`milestones.md`）

## 与课程1的关键差异

| 维度 | 数据分析与可视化（本科生） | 人工智能大模型应用（博士生） |
|---|---|---|
| 项目主体 | 团队协作做产品 | 个人科研项目构建工具栈 |
| 成果导向 | 公开产品+路演 | AI4S工具栈+科研产出 |
| 技术深度 | 应用层（做出来） | 方法层（做出来+做对） |
| PBL驱动 | 创业/产品思维 | 科研方法论+AI工具链 |
| 课程节奏 | 17周宽松迭代 | 9周密集构建 |
| 大模型定位 | 产品中的AI功能 | 贯穿科研全流程的"研究伙伴" |
| AI工具引入节奏 | W1起步→W9进阶→W13自动化→W14质量 | W1起步→W2进阶→W4自动化→W5-6封装→W7质量 |

## 参考资料

- [PBLWorks - What is PBL](https://www.pblworks.org/what-is-pbl)
- Andrew Ng - How to Build Your Career in AI（项目筛选与科研成长框架）
- The Founder's Playbook: Building an AI-Native Startup（AI-Native工作方法论）
- The Minimalist Entrepreneur（社区先行、最小化方法）

## 目录结构规划

```
ai4s/
├── ai4s-teaching-plan.md              # 本文件：AI4S课程教学方案
├── knowledge-map.md                    # 知识地图（按科研模块组织）
├── syllabus.md                         # 课程大纲
├── rubric.md                           # 评分标准
├── milestones.md                       # 阶段里程碑
├── ai-toolstack/                       # 共同AI基础工具栈教学材料
│   ├── ai-coding/                      # AI辅助编程(opencode/cursor/trae)
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
