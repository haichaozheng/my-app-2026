# 数据分析与可视化 — PBL教学方案

## 课程信息

- **面向对象**：财经院校本科生
- **课程目标**：提高学生做金融数据分析应用与产品的能力，培养学生的创新与创业思维
- **教学方法**：Project Based Learning（PBL）
- **课程时长**：17周
- **团队规模**：3-4人/组
- **技术栈**：不限（学生自主选择）
- **先修要求**：学生有一定Python基础和大模型使用经验

## 共同AI基础工具栈

两门课程共享以下AI基础工具栈，随项目需求**渐进式融入**教学内容，而非单独设课：

| 工具 | 在课程中的角色 | 主要应用场景 |
|---|---|---|
| AI辅助编程(opencode/cursor/trae) | 开发环境与生产力工具 | 产品代码编写、调试、迭代 |
| Prompt Engineering | 与LLM交互的基础方法论 | 数据探索、用户调研、产品交互设计 |
| RAG | 产品智能功能的核心技术 | 金融数据问答、知识检索、智能解读 |
| Agent | 产品自动化与智能交互 | 金融数据监控Agent、自动化报告Agent |
| Skill | 可复用的AI能力模块 | 数据分析skill、可视化skill、报告生成skill |
| AI系统评估 | 产品质量保障方法 | 模型准确性评估、用户体验评估、产品可靠性评估 |

**渐进融入节奏**：Prompt+AI辅助编程(W1起步) → RAG(W9进阶) → Agent+Skill(W13自动化) → AI系统评估(W14质量保障)

## PBL框架

本课程以"从0到1做一个金融数据分析产品"为学期长项目，学生组队从发现金融领域的真实问题开始，逐步构建一个可公开访问的数据分析产品，学期末进行公开路演。

| PBL要素 | 课程实现 |
|---|---|
| Authentic Problem | 金融领域的真实数据与用户需求 |
| Sustained Inquiry | 17周持续迭代，从选题到上线 |
| Student Voice & Choice | 学生在赛道中自选具体方向和切入点 |
| Reflection | 每阶段提交反思日志 |
| Critique & Revision | 同侪互评 + 教师反馈迭代 |
| Public Product | 最终产品公开部署并进行路演展示 |

## 选题模式：混合模式

采用**企业提供赛道 + 学生自选方向**的混合模式，兼顾真实性与学生自主性。

| 方式 | 优势 | 劣势 |
|---|---|---|
| 企业命题 | 真实问题+真实数据+产业连接 | 学生自主性低，可能缺乏热情 |
| 学生自选 | 最大化学生主动性 | 可能选题不聚焦、缺乏真实数据 |
| **混合：企业提供赛道+学生自选方向** | 兼具真实性与自主性 | 需要企业配合 |

**具体做法**：企业提供3-5个金融赛道（如投资分析、风险管理、信贷评估、量化交易、宏观研究等），学生组内在赛道中自选具体方向和切入点。既保证问题的真实性和数据可得性，又保留学生的自主选择权。

## 17周课程安排

### Phase 1: Idea Stage（Week 1-4）— 发现问题、定义项目

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W1 | 课程启动 + PBL方法论 + AI工具栈起步 | PBL理念、课程框架、团队组建、AI辅助编程环境搭建(opencode/cursor/trae)、Prompt Engineering基础 | 破冰、组队、了解赛道选项、用AI辅助编程完成课程环境配置 | 团队名单 |
| W2 | 金融数据全景 + Prompt驱动探索 | 金融数据源与获取（API/Web Scraping）、数据生态、Prompt驱动的金融数据探索 | 探索赛道、初步调研、用Prompt+AI辅助编程探索赛道数据 | 赛道意向 |
| W3 | 问题发现与用户洞察 + Deep Research | Minimalist Entrepreneur"社区先行"方法、用户访谈技巧、Deep Research Prompt进行用户洞察调研 | 深入社区/论坛调研、访谈潜在用户、用Deep Research Prompt提炼用户痛点 | 问题陈述初稿 |
| W4 | 项目提案 | 如何写好的项目提案、Andrew Ng项目筛选框架 | 撰写并提交项目提案 | 项目提案（含问题、目标、数据来源、初步方案） |

### Phase 2: MVP Stage（Week 5-10）— 构建最小可用产品

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W5 | 手动流程先行 + AI辅助编程加速 | Minimalist Entrepreneur"先建手动流程"理念、数据分析思维、用AI辅助编程加速手动分析中的代码编写 | 手动完成一次完整分析流程 | 手动分析报告 |
| W6 | 数据清洗与探索 + Prompt驱动EDA | Pandas高级、缺失值/异常值处理、探索性数据分析、AI辅助编程生成数据清洗代码、Prompt驱动EDA洞察 | 数据清洗、EDA、用AI辅助编程生成清洗代码 | EDA报告 |
| W7 | 可视化设计 | 可视化原则、Plotly/Pyecharts/Echarts、故事化叙事 | 设计核心可视化方案 | 可视化原型草图 |
| W8 | 产品原型搭建 + AI辅助编程加速原型 | Streamlit/Gradio/其他框架快速原型、用AI辅助编程加速原型搭建 | 搭建MVP原型 | MVP v0.1（可运行） |
| W9 | 大模型赋能产品 + RAG与Agent | LLM API集成、智能摘要/解读/对话功能、RAG构建产品知识库（金融数据问答）、Agent设计产品智能功能 | 为产品添加AI交互功能、添加RAG问答功能和Agent自动报告功能 | MVP v0.2（含AI功能） |
| W10 | MVP评审 | 产品评审标准、同侪互评方法 | 组间互评MVP、迭代改进 | 互评反馈 + MVP v0.3 |

### Phase 3: Launch Stage（Week 11-15）— 上线与迭代

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W11 | 产品部署 | 云部署（Streamlit Cloud/Vercel/其他）、基本运维 | 产品上线 | 产品公网可访问 |
| W12 | 获客与推广 | Minimalist Entrepreneur"Sell to Your First 100 Customers"、推广渠道 | 向目标用户推广、收集反馈 | 用户反馈记录 |
| W13 | 高级分析增强 + Agent与Skill | 机器学习/时间序列/因子分析等进阶方法、Agent驱动高级分析功能（自动化监控）、Skill封装可复用分析能力 | 根据用户反馈增加高级功能、用Agent实现自动化监控、封装数据分析Skill | 产品v1.0 |
| W14 | 产品打磨 + AI系统评估 | UX优化、错误处理、文档撰写、AI系统评估方法（准确性/可靠性/用户体验评估） | 产品最终打磨、对产品进行AI系统评估 | 产品v1.1 + 使用文档 + 评估报告 |
| W15 | 路演准备 | 演讲技巧、Demo演示、故事线构建 | 准备路演PPT和Demo | 路演材料 |

### Phase 4: Scale Stage（Week 16-17）— 展示与反思

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W16 | 公开路演 | — | 公开路演展示产品 | 路演评分 |
| W17 | 反思与展望 | Founder's Playbook"Scale"阶段思维 | 撰写最终反思报告 | 项目最终报告 + 产品仓库链接 |

## 评分体系

基于PBL六要素设计评分维度：

| 评分维度 | 权重 | 对应PBL要素 | 评价方式 |
|---|---|---|---|
| 项目提案质量 | 10% | Authentic Problem | 教师评分 |
| 过程参与与迭代 | 20% | Sustained Inquiry + Critique & Revision | 反思日志+迭代记录 |
| 产品质量 | 30% | Public Product | 路演评分+代码评审 |
| 同侪互评 | 10% | Critique & Revision | 互评表 |
| 最终反思报告 | 15% | Reflection | 教师评分 |
| 用户反馈与获客 | 15% | Authentic Problem + Student Voice | 反馈记录 |

## 关键设计原则

1. **真实性优先**：选题来自金融领域真实痛点，数据来自真实数据源
2. **先手动再自动**：Week 5的核心理念——先用手动流程验证价值，再自动化为产品
3. **大模型作为赋能工具**：学生在产品中集成LLM能力（智能解读、对话交互），而非仅用大模型写代码
4. **社区驱动选题**：Inspired by Minimalist Entrepreneur——从金融社区中发现问题
5. **公开产品为终点**：路演面向全校/企业合作伙伴，产品可公开访问
6. **AI基础工具栈渐进融入**：Prompt+AI辅助编程(W1起步) → RAG(W9进阶) → Agent+Skill(W13自动化) → AI系统评估(W14质量保障)，工具随项目需求自然引入而非单独设课
7. **知识框架有机支撑**：知识按项目阶段而非学科章节组织（见`knowledge-map.md`），通过里程碑制造知识缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply节奏），反思环节逼迫学生重构个人知识框架（见`templates/reflection-log.md`），交付物锚定核心知识概念（见`milestones.md`）

## 参考资料

- [PBLWorks - What is PBL](https://www.pblworks.org/what-is-pbl)
- Andrew Ng - How to Build Your Career in AI（项目筛选框架）
- The Founder's Playbook: Building an AI-Native Startup（四阶段创业生命周期）
- The Minimalist Entrepreneur（社区先行、手动流程先行、先卖再建）

## 目录结构规划

```
data-analysis/
├── data-analysis-teaching-plan.md  # 本文件：PBL教学方案
├── knowledge-map.md                # 知识地图（按项目阶段组织）
├── syllabus.md                      # 课程大纲（17周详细安排）
├── rubric.md                        # 评分标准（PBL六要素对应）
├── milestones.md                    # 阶段里程碑与交付物定义
├── ai-toolstack/                    # 共同AI基础工具栈教学材料
│   ├── ai-coding/                   # AI辅助编程(opencode/cursor/trae)
│   ├── prompt-engineering/          # Prompt Engineering
│   ├── rag/                         # RAG原理与实践
│   ├── agent/                       # Agent设计与开发
│   ├── skill/                       # Skill封装与复用
│   └── ai-evaluation/               # AI系统评估
├── templates/                       # 学生模板文件
│   ├── project-proposal.md          # 项目提案模板
│   ├── reflection-log.md            # 反思日志模板
│   ├── peer-review.md               # 同侪互评模板
│   └── final-report.md              # 最终报告模板
├── weeks/                           # 每周教学材料
│   ├── week01/
│   │   ├── lecture.md               # 课堂内容
│   │   ├── lab.md                   # 实践任务
│   │   └── resources.md             # 推荐资源
│   ├── ...                          # week02-week17
├── examples/                        # 示例产品/案例
│   ├── stock-dashboard/             # 股票分析Dashboard示例
│   ├── credit-scoring/              # 信贷评分示例
│   └── risk-monitor/                # 风险监控示例
└── data/                            # 示例数据集
