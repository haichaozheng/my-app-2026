# 数据分析与可视化 — PBL教学方案

## 课程信息

- **面向对象**：财经院校本科生
- **课程目标**：提高学生做金融数据分析应用与产品的能力，培养学生的创新与创业思维
- **教学方法**：Project Based Learning（PBL）
- **方法论锚定**：设计科学研究（Design Science Research, DSR）
- **课程时长**：17周
- **团队规模**：3-4人/互助小组，每人独立完成1个产品
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

> **AI系统评估是横切实践，不是独立工具**：它不单列为一行，因为它没有专属工具——评估 RAG/Agent/Skill/LLM 功能靠的是 Prompt（构造 evals 集、做可信度提问）与 Skill（封装可复用的回归测试）。评估是"验证搭出来的东西靠不靠谱"的贯穿能力，应用于所有 AI 功能：对 AI 输出做可信度判断（反思日志 4.3）、用 10-20 条"问题—预期答案"做 evals 回归测试（W15）、按设计科学有效性（Larsen，criterion/causal/context validity）严格评估（见「设计科学研究方法（DSR）方法论锚定」节）、并计入 rubric「AI功能价值」的"对AI输出有可信度判断"维度。

**渐进融入节奏**：Prompt+AI辅助编程(W1起步) → RAG(W9进阶) → 建模增强(W12-W15：机器学习基础/特征工程/大模型做数据分析/模型评估与产品化，必做基础+进阶可选) → **评估贯穿全阶段**（对 RAG/Agent/Skill/LLM 功能做可信度判断与 evals，重点嵌入 W15 建模产品化）

## AI-Native 项目工作流

本课程以 **repo 为项目管理中枢**，不引入额外 PM 工具：学生个人产品仓库即项目管理系统，opencode 读取 AGENTS.md 与 artifact thread 接管项目上下文，git 提交历史即审计轨迹。

### 项目脊柱：requirements → design → scope（+ AGENTS.md 稳定）

每轮迭代产出 / 更新四个版本控制的 markdown：

| 文件 | 内容 | 性质 |
|---|---|---|
| requirements.md | ## 问题与用户（强制第一节：痛点/为什么/给谁/社区调研证据）+ ## 需求(Must/Should) + ## 约束与不做 | 问题+需求，per-iteration |
| design.md | ## 架构/组件/数据流 + ## 数据源与处理 + ## AI功能技术设计(RAG or LLM解读如何解决痛点) + ## 部署方案 | 技术 how，per-iteration |
| scope.md | ## 本期范围(从需求圈定子集+边界) + ## 任务清单(feature级，每任务含如何做:改哪些文件/工作顺序/测试/风险) + ## 验收标准 | 范围+任务+实现 how，per-iteration |
| AGENTS.md | 命令/约定/架构/常见错误，一页内 | 产品级稳定，原地更新，不重建 |

### 顺序
requirements → design → scope。scope 的"本期范围"可紧跟 requirements 先草拟（圈范围不需技术设计），但"任务清单（含如何做）"须 design 之后填（架构定了才知道改哪些文件）。

### 循环（loopable）
每轮迭代：小改在文件末尾追加 `## 迭代N（触发：W12用户反馈/…）` 节、大改或转向新建 `-v2` 版本；旧内容不删，git 历史即审计轨迹。用户反馈 / 越界触发新一轮 requirements→design→scope 循环。

### AGENTS.md（稳定上下文）
每个产品一份 AGENTS.md（opencode 约定，等价于机构知识文件）：命令、约定、架构、常见错误，一页内。opencode 每次会话读取它获取项目上下文。规则：AI 在某处犯同样错误两次，就把纠正写进 AGENTS.md。它随产品演进、原地更新，不随迭代重建。学生填空模板见 `templates/AGENTS.md`。

## 设计科学研究方法（DSR）方法论锚定

本课程**教学法层**用 PBL（如何组织学习），**方法论层**用设计科学研究（Design Science Research, DSR，如何保障"从实践中提取问题并开发系统"的学术严谨性）。DSR 的内核是"**创建并评估 IT artifact 以解决真实组织/人的问题**"——学生建金融数据分析产品解决真实痛点，本身就是 DSR 实践；本课程只是用 DSR 的词汇命名它、用 DSR 的评估框架严谨化它。**DSR 还是唯一把"已建成的产品(instantiation)"视为合法研究贡献的方法论**，这正好打通本课程"公开产品兼产学术论文"的双重产出目标（产品即 artifact，深度抽象可升级为 nascent design theory）。

> 轻量适配原则：DSR 作为**命名/定位/评估透镜**叠在现有 `requirements→design→scope` 项目脊柱与里程碑之上，不新增重型交付物。全员必做"简短 DSR 定位 + ≥1 条 criterion validity claim"；完整的 Larsen 有效性消融实验与完整的 Gregor & Hevner 知识贡献论证归入**可选"兼产论文"轨**。

### DSR 三循环 ↔ 课程映射（Hevner 2007）

| DSR Cycle | 含义 | 课程对应 |
|---|---|---|
| Relevance Cycle（相关性循环） | 环境（问题空间）↔ 研究，确保解决真实且重要的问题 | W1-W3 社区倾听 + 用户访谈；W13 5-10 位用户反馈；W16 路演面向真实受众 |
| Rigor Cycle（严谨性循环） | 知识库（基础与方法论）↔ 研究，确保方法严谨 | `knowledge-map.md` + 共同 AI 基础工具栈；引用金融/统计/CS 既有方法 |
| Design Cycle（设计循环，中心） | build & evaluate 反复迭代 | `requirements→design→scope` 循环；MVP v0.1→v0.2→v0.4→v1.0→v1.1；W9 互评打磨 |

### DSRM 六步 ↔ 课程阶段映射（Peffers et al. 2007）

| DSRM 步骤 | 课程阶段 | 对应交付物 |
|---|---|---|
| 1. 问题识别与动机（Problem identification and motivation） | W1-W3 Idea Stage | 问题陈述初稿 + 社区调研记录 + 项目提案 |
| 2. 定义解决方案目标（Define the objectives for a solution） | W3 | `requirements.md`（Must/Should 需求即目标） |
| 3. 设计与开发（Design and development） | W4-W10 MVP Stage | 手动流程→EDA→可视化→原型→AI 功能→打磨 |
| 4. 演示（Demonstration） | W9 互评 / W11 上线 / W16 路演 | MVP v0.4 演示 + 公网可访问产品 + 路演 Demo |
| 5. 评估（Evaluation） | W9 互评 + W12-W15 模型评估 + W13 用户反馈 | 同侪互评 + eval 指标/交叉验证 + Larsen 有效性 |
| 6. 沟通（Communication） | W16 路演 + W17 报告 | 路演（技术 + 管理双重受众）+ `final-report.md` 含 DSR 定位 |

### artifact 四类型与个人产品（Hevner et al. 2004）

DSR 的 artifact = constructs（构念）/ models（模型）/ methods（方法）/ instantiations（实例化系统）。学生产品主要为 **instantiation（Level 1 已落地实现）**；进阶学生可将 RAG 流水线抽象为 **method**、将数据/特征方案抽象为 **model**（达 Gregor & Hevner Level 2 nascent design theory）——这是"产品 → 论文"的升级路径。

### 知识贡献定位（Gregor & Hevner 2013）

每人最终报告须声明个人产品的知识贡献定位（应用域成熟度 × 方案成熟度二维框架）：

- **Improvement（改进）**：为已知问题提出更好的新方案——须证明相对既有方案确有提升
- **Exaptation（跨域迁移）**：把某领域已有设计知识迁移到新的金融应用场景
- **Invention（发明）**：为新问题提出全新方案（本课程罕见，但鼓励）
- **Routine Design（常规设计）**：已知问题 + 已知方案，无重大知识贡献——**不算合格创新，须增加新意**

> 完整论证（为何属于该象限、相对知识库的增量）为可选论文轨要求。

### 评估有效性（Larsen et al. 2025）

W15 评估环节引入设计科学有效性框架：**全员须 ≥1 条 criterion validity claim**——把产品效能与一个**参考实体**比较（如基线模型、手动分析、既有工具、空 RAG 模块等）。可选论文轨可加：

- **Causal validity（因果效度）**：消融实验（去掉某模块如 RAG，对比是否仍有效）
- **Context validity（情境效度）**：外部效度（多用户/多场景）+ 生态效度（W13 的 5-10 真实用户测试即生态效度证据）

> 对照 Monash/Arnott & Pervan (2012) 对 362 篇 DSS 研究的评估警示——**42.3% 无评估、75% 方法弱、85.4% 管理沟通弱**——本课程以"必做评估（针对无评估）+ 引用方法论（针对方法弱）+ 用户反馈与路演双重受众沟通（针对管理沟通弱）"针对性补强。

### Hevner 七指导原则（反思与评分透镜）

不强制逐条交付，但作为反思与 `rubric.md` 评分透镜：① Design as an Artifact（产出可用 artifact）② Problem Relevance（解决重要真实问题）③ Design Evaluation（严格评估效用）④ Research Contributions（清晰研究贡献）⑤ Research Rigor（方法严谨）⑥ Design as a Search Process（迭代搜索解）⑦ Communication of Research（向技术与管理者双受众有效沟通）。

## PBL框架

本课程以"AI赋能的一人公司（OPC）+ 互助小组"为学期长项目模式：学生以3-4人组成互助小组，组内不要求共享同一条赛道或领域，但**每人独立完成并交付一个属于自己的金融数据分析产品**；学期末进行公开路演（每人独立展示个人产品）。互助小组既是互助评审与经验共享的学习共同体，也是"一人公司"之间的创业生态——你的成功部分取决于你能否赋能同伴。

| PBL要素 | 课程实现 | DSR 咬合（方法论层） |
|---|---|---|
| Authentic Problem | 金融领域的真实数据与用户需求 | Relevance Cycle：W1-W3 社区倾听 + W13 用户反馈确保问题真实重要（Hevner 指导②） |
| Sustained Inquiry | 17周持续迭代，从选题到上线 | Design Cycle：build & evaluate 反复迭代（DSRM 步骤3→5 循环） |
| Student Voice & Choice | 学生在赛道中自选具体方向和切入点（包括个人产品方向） | Design as a Search Process：学生在约束下自主搜索解（Hevner 指导⑥） |
| Reflection | 每阶段提交反思日志 | 七指导原则自检透镜 + DSR 定位重构 |
| Critique & Revision | 组内互助评审（个人MVP互评）+ 跨组互评 + 教师反馈迭代 | Design Evaluation：严格评估效用（Hevner 指导③） |
| Public Product | 每人最终产出一个公开部署的产品并进行路演展示 | Artifact 交付 + 向技术/管理双受众沟通（Hevner 指导①⑦） |

## 选题模式：财经新闻驱动 + 真实需求驱动 + 个人爱好

选题来源有三档，鼓励一个选题能同时命中≥2档：

| 来源 | 含义 | 举例 |
|---|---|---|
| 财经新闻驱动 | 从政策/数据发布/财经事件中提炼话题 | 央行降准、CPI超预期、某地房价异动 |
| 真实需求驱动 | 从身边人/社区观察到的真实痛点出发（吸收 Minimalist Entrepreneur"社区先行"方法） | 同学家庭账单一团乱、散户看不懂研报 |
| 个人爱好 | 从学生自身兴趣出发 | 喜欢某行业、迷某类数据可视化 |

采用"学生自选方向 + 教师提供参考选题菜单"模式：学生从三档来源自选具体产品方向，教师提供一套参考选题菜单（详见 `project-selection-guide.md`）作为启发，不强制、不限制领域。

**互助小组与"一人一产品"对齐**：学生3-4人组成互助小组，组内**不要求共享同一条赛道或领域**——每人独立选题、独立交付。互助基于工具/方法/AI应用（互相帮调试、帮选型、帮评审），而非共享领域知识；各人选题可完全不同，仍能互相赋能。这既保留"一人公司"的完整独立作品，又让互助小组成为真实有效的学习共同体（契合AI时代"一人公司"的可行路径）。

### 选题真实性与准入

财经新闻/个人兴趣类选题必须在 W3 经用户访谈验证真实需求，否则调整或重选。完整的选题准入清单、否决清单、参考选题菜单与数据源清单见 `project-selection-guide.md`。

## 17周课程安排

### Phase 1: Idea Stage（Week 1-3）— 发现问题、定义项目（DSR Relevance Cycle 为主；DSRM 步骤 1-2）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W1 | 课程启动 + PBL方法论 + AI工具栈起步 | PBL理念、课程框架、互助小组组建、AI辅助编程环境搭建(opencode/cursor/trae)、Prompt Engineering基础 | 破冰、组建互助小组（基于工具/方法互助，不限同领域）、了解选题来源与参考菜单、用AI辅助编程完成课程环境配置、**初始化个人项目仓库（AGENTS.md 骨架）** | 互助小组名单 |
| W2 | 金融数据全景 + 选题方向探索 | 金融数据源与获取（API/Web Scraping）、数据生态、Prompt驱动的金融数据探索 | 每人从三档选题来源（财经新闻/真实需求/个人爱好）初选2-3个产品方向，用Prompt+AI辅助编程验证数据可得性；锁定目标用户聚集的社区并加入、开始倾听记录；参考菜单见 `project-selection-guide.md` | 个人选题方向初选（含数据可得性初验 + 社区加入记录） |
| W3 | 问题发现、用户洞察与项目提案 | Minimalist Entrepreneur"社区先行"方法（必做：加入社区、倾听真实问题）、用户访谈技巧、Deep Research Prompt进行用户洞察调研、从社区调研中发现并验证可产品化痛点、如何写好的项目提案、Andrew Ng项目筛选框架 | 每人加入1个目标用户聚集的社区（雪球/股吧/知乎话题/相关论坛或群），完成≥1周倾听并记录真实问题（用户原话/帖子≥3条），从社区调研中形成或验证选题痛点；用Deep Research交叉验证痛点真实性；筛掉无真实需求的选题；撰写并提交个人项目提案；**本周末做阶段回顾(15min)，产出含 DSR 自检(Idea 阶段)的阶段反思** | 个人问题陈述初稿（须附社区调研记录：社区名、观察期、真实问题与用户原话）+ 个人项目提案（含问题、目标、数据来源、初步方案；注明互助小组内分工协作设想） |

### Phase 2: MVP Stage（Week 4-10）— 构建最小可用产品（DSR Design Cycle·build；DSRM 步骤 3）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W4 | 手动流程先行 + 批判性思维与判断 + AI辅助编程加速 | Minimalist Entrepreneur"先建手动流程"理念、数据分析思维、批判性思维与判断（偏误自检、AI输出判断、决策框架）、用AI辅助编程加速手动分析中的代码编写 | 每人手动完成一次完整分析流程 | 个人手动分析报告 |
| W5 | 数据清洗与探索 + Prompt驱动EDA | Pandas高级、缺失值/异常值处理、探索性数据分析、AI辅助编程生成数据清洗代码、Prompt驱动EDA洞察 | 每人完成数据清洗、EDA、用AI辅助编程生成清洗代码 | 个人EDA报告 |
| W6 | 可视化设计 | 可视化原则、Plotly/Pyecharts/Echarts、故事化叙事 | 每人设计核心可视化方案 | 个人可视化原型草图 |
| W7 | 产品原型搭建 + AI辅助编程加速原型 | Streamlit/Gradio/其他框架快速原型、用AI辅助编程加速原型搭建 | 每人搭建个人MVP原型 | 个人MVP v0.1（可运行） |
| W8 | 大模型赋能产品 | LLM API集成、智能摘要/解读/对话功能、RAG或LLM智能解读（二选一）构建产品AI交互 | 每人给个人产品添加1个AI功能（RAG问答 或 LLM智能解读，二选一） | 个人MVP v0.2（含AI功能） |
| W9 | MVP评审与打磨迭代 | 产品评审标准、同侪互评方法、据反馈定向打磨与技术债清理 | 组内个人MVP互评；每人针对互评与教师反馈完成一轮打磨迭代，修复关键缺陷、优化可视化/交互、清理技术债，提升完成度 | 组内互评反馈 + 个人MVP v0.4（打磨版，可演示） |
| W10 | 上线前准备：服务器基础 + 云资源申请 + 数据库选型 | 服务器/云基础概念（公网IP、端口、进程常驻、反向代理）、腾讯云账号与轻量应用服务器/CloudBase申请（校园免费额度）、产品上线形态规划；数据库最小可用方案：SQLite（零安装、文件型、Python内置，首选）vs PostgreSQL（开源免费、需安装，适合多用户并发/服务端独立库；腾讯云有云数据库免费额度） | 每人申请腾讯云账号并领取校园/免费额度，确定上线方式（轻量应用服务器 或 CloudBase），若产品使用数据库则完成选型（首选SQLite，需服务端独立库再选PostgreSQL）；**本周末做阶段回顾(15min)，产出含 DSR 自检(MVP 阶段)的阶段反思** | 腾讯云账号 + 免费额度申请完成 + 个人上线部署方案（含数据库选型说明） |

### Phase 3: Launch Stage（Week 11-15）— 上线与迭代（DSRM 步骤 4 演示 + 步骤 5 评估；Larsen 有效性：W15 须 ≥1 条 criterion validity claim）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W11 | 产品部署 | 云部署（Streamlit Cloud/Vercel/其他）、基本运维 | 每人将个人产品上线（含 W9 AI 功能的 MVP，建模增强将在 W12-W15 加入） | 个人产品公网可访问 |
| W12 | 机器学习建模基础 + 获客起步 | 监督学习(回归/分类)、训练/测试划分、过拟合初识；金融场景(违约预测/收益预测)；获客渠道与方法准备 | 每人从金融数据建立第一个基础模型（回归或分类，必做基础）；开始向目标用户推广准备 | 个人基础模型(回归/分类) + 获客准备 |
| W13 | 特征工程与模型选择（必做基础+进阶可选）+ 用户反馈收集 | 特征工程、模型选择逻辑、避免数据泄漏；进阶(可选)：时间序列/因子模型/无监督；获客方法论（如何找到 5-10 用户） | 完善特征与模型选择；每人获取 5-10 位目标用户反馈并记录 | 模型迭代版 + 个人用户反馈记录(5-10) |
| W14 | 大模型做数据分析（必做）+ 据反馈迭代 | LLM 作为分析引擎——解读规律/生成洞察/代码生成做分析；LLM vs 传统 ML 适用边界与互补；据 W13 反馈迭代建模方向 | 用 LLM 做数据分析/建模实验；据用户反馈迭代模型方向 | LLM 分析实验 + 模型 v1.0(据反馈迭代) |
| W15 | 模型评估与建模产品化（必做基础+进阶可选）+ 路演准备（轻） | 评估指标(MSE/R²/准确率/F1/混淆矩阵)、交叉验证、偏差-方差；**设计科学有效性（Larsen 2025：每产品≥1条 criterion validity claim——产品效能相对参考实体如基线模型/手动分析/空RAG模块比较）**；把模型嵌入产品；evals 回归测试；进阶(可选)：Agent 自动化/Skill 封装/AB 测试/深度评估；UX 优化；路演叙事 | 评估模型并嵌入产品、撰写使用文档、准备路演 PPT 与 Demo（轻）；**本周末做阶段回顾(15min)，产出含 DSR 自检(Launch 阶段)与有效性 claim 草稿的阶段反思** | 个人产品 v1.1(含模型+评估+文档) + 路演材料 |

### Phase 4: Scale Stage（Week 16-17）— 展示与反思（DSRM 步骤 6 沟通；全员 DSR 定位写入 `final-report.md`）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W16 | 公开路演（海报展 + 精选Demo） | — | 全体参加海报展（每人1-2分钟闪讲）；精选6-8个完整Demo（每个5分钟） | 路演评分 |
| W17 | 反思与展望 | Founder's Playbook"Scale"阶段思维 | 每人撰写最终反思报告 | 个人项目最终报告 + 个人产品仓库链接 |

## 评分体系

采用"平时成绩 + 个人项目 + 协作"三层次、全百分制结构。所有分项均先按百分制评分，再乘以权重计入总成绩。

| 评分项 | 权重 | 内部构成 | 评分方式 |
|---|---|---|---|
| 平时成绩 | 30% | 综合（含出勤、技能小练、阶段里程碑交付、周反思日志与项目日志(journal.md)，不细分比例） | 教师评分 |
| 个人项目 | 50% | 产品质量 60% + 项目报告 40% | 教师评分 |
| 协作互评 | 10% | 组内其他成员匿名百分制打分算术平均 | 组员360°互评 |
| 组内项目平均 | 10% | 组内其他成员"个人项目"百分制成绩的算术平均 | 公式 |

**个人项目内部（50%）**
- **产品质量（60% → 占总成绩30%）**：最终产品v1.1（功能完整度、分析深度、AI功能价值）+ 公开路演Demo
- **项目报告（40% → 占总成绩20%）**：一份综合文档，含产品论证与设计资料、组内协作贡献记录、用户反馈与获客、最终反思、**DSR 定位（全员必做：artifact 类型 + 知识贡献定位 + ≥1 条 criterion validity claim + 参考实体 + relevance/rigor 证据）**（模板见`templates/final-report.md`）

**协作项内部（20%）**
- **协作互评（10%）**：期末(W17)一次360°匿名互评，每人给组内其他成员打0-100分，算术平均后÷10计入权重。依据为各人报告中的"协作贡献"记录 + 亲历。
- **组内项目平均（10%）**：取组内其他成员"个人项目"百分制成绩（即产品质量+报告合并后的百分制分）的算术平均，÷10计入权重。该项的含义是"你的成绩与同伴成功绑定"，激励一人公司之间的互助赋能。

**总成绩公式**

```
总成绩 = 平时成绩×0.30
       + 个人项目×0.50      （个人项目 = 产品质量×0.6 + 项目报告×0.4，均百分制）
       + 协作互评×0.10      （协作互评 = 组内他人匿名打分均值，百分制）
       + 组内项目平均×0.10  （组内项目平均 = 组内他人个人项目分均值，百分制）
```

**个人与协作占比**：个人合计80%（平时30 + 个人项目50），协作合计20%（互评10 + 组内项目平均10）。

> 详细量化标准见 `rubric.md`；阶段里程碑定义见 `milestones.md`；报告模板见 `templates/final-report.md`（含必做的「DSR 定位」节，对应本课程「设计科学研究方法（DSR）方法论锚定」节）。

## 关键设计原则

1. **真实性优先**：选题来自金融领域真实痛点，数据来自真实数据源
2. **先手动再自动**：Week 5的核心理念——先用手动流程验证价值，再自动化为产品
3. **大模型作为赋能工具**：学生在产品中集成LLM能力（智能解读、对话交互），而非仅用大模型写代码；AI辅助编程是单人交付产品的核心生产力杠杆
4. **社区驱动选题**：Inspired by Minimalist Entrepreneur——从金融社区中发现问题
5. **财经新闻 + 真实需求 + 个人爱好驱动选题**：从财经新闻观察、身边真实需求或自身兴趣出发提炼选题，并经用户访谈验证真实性——避免选题偏离真实需求
6. **公开产品为终点**：路演面向全校/企业合作伙伴，每人产出并可公开访问一个独立产品
7. **AI基础工具栈渐进融入**：Prompt+AI辅助编程(W1起步) → RAG(W9进阶) → 建模增强(W12-W15：ML基础/特征工程/大模型做数据分析/模型评估产品化) → AI系统评估(嵌入W15建模产品化)；工具随项目需求自然引入，进阶(Agent/Skill/深度模型)可选
8. **AI赋能个体 / 一人公司（OPC）导向**：在强AI工具加持下，3-4人互助小组内**每人独立完成并交付一个完整产品**，模拟"一人公司"的真实可行路径；互助小组替代传统分工团队，强调"一人公司的创业生态"——既锻炼独立交付，又通过协作互评与组内项目平均激励彼此赋能
9. **知识框架有机支撑**：知识按项目阶段而非学科章节组织（见`knowledge-map.md`），通过里程碑制造知识缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply节奏），反思环节逼迫学生重构个人知识框架（见`templates/reflection-log.md`），交付物锚定核心知识概念（见`milestones.md`）
10. **AI-Native 项目工作流**：以 requirements→design→scope（循环）+ AGENTS.md（稳定）为项目脊柱，repo 为真相源，opencode 读 AGENTS.md 接管项目上下文，git 历史为审计轨迹——不引入额外 PM 工具（详见上文「AI-Native 项目工作流」节）
11. **设计科学方法论锚定**：以 DSR 三循环（相关性/严谨性/设计）与 DSRM 六步为方法论骨架，使 PBL 项目既具教学真实性又具研究严谨性；产品即 artifact、评估即 evaluation、社区反馈即 relevance cycle——为"公开产品兼产论文"提供学术方法保障（详见上文「设计科学研究方法（DSR）方法论锚定」节）
12. **反思与日志闭环**：用双层反思+日志养成元认知习惯——`journal.md`（in-action 即时日志，记跨文件决策与学习轨迹，映射 DSR 指导⑥ 搜索过程）+ 周反思日志（on-action 知识重构）+ 阶段边界 DSR 自检（W3/W10/W15/W17）+ `final-report.md` 综合闭环；知识缺口须 feed-forward（追踪是否真补上），形成 Challenge→Gap→Knowledge→Apply 闭环（详见 `templates/journal.md`、`templates/reflection-log.md`）

## 参考资料

- [PBLWorks - What is PBL](https://www.pblworks.org/what-is-pbl)
- Andrew Ng - How to Build Your Career in AI（项目筛选框架）
- The Founder's Playbook: Building an AI-Native Startup（四阶段创业生命周期）
- The Minimalist Entrepreneur（社区先行、手动流程先行、先卖再建）
- **设计科学（DSR）方法论（见 `../references/design-science/` 目录，已提取为 md）**
  - Hevner et al. (2004) - Design Science in Information Systems Research（七指导原则、artifact 四类型、IS 研究框架）
  - Hevner (2007) - A Three Cycle View of Design Science Research（Relevance/Rigor/Design 三循环原文）
  - Peffers et al. (2007) - A Design Science Research Methodology for Information Systems Research（DSRM 六步）
  - Gregor & Hevner (2013) - Positioning and Presenting Design Science Research for Maximum Impact（知识贡献二维框架、DSR 沟通范式）
  - Larsen et al. (2025) - Validity in Design Science（criterion/causal/context 有效性框架）
  - Arnott & Pervan (2012) - Design Science in Decision Support Systems Research: An Assessment using the Hevner, March, Park, and Ram Guidelines（DSS 研究评估 + 严谨性警示）

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
│   ├── project-proposal.md          # 项目提案模板（历史，已并入 requirements.md）
│   ├── reflection-log.md            # 反思日志模板
│   ├── peer-review.md               # 同侪互评模板
│   ├── final-report.md              # 最终报告模板
│   ├── requirements.md              # 产品需求模板（项目工作流，W3提交）
│   ├── design.md                    # 技术方案设计模板（项目工作流，W4提交）
│   ├── scope.md                     # 范围与任务模板（项目工作流，W4提交）
│   ├── reflection-log.md            # 周反思日志模板（on-action，每周提交）
│   ├── journal.md                   # 项目日志模板（in-action，repo 内随手记）
│   └── AGENTS.md                    # 产品稳定上下文模板（opencode 读取）
├── weeks/                           # 每周教学材料
│   ├── week01/
│   │   ├── lecture.md               # 课堂内容
│   │   ├── lab.md                   # 实践任务
│   │   └── resources.md             # 推荐资源
│   ├── ...                          # week02-week17
├── examples/                        # 示例产品/案例
│   ├── prediction-market/           # 人机融合预测市场示例（可fork的独立产品）
│   ├── stock-dashboard/              # 股票分析Dashboard示例
│   ├── credit-scoring/              # 信贷评分示例
│   └── risk-monitor/                # 风险监控示例
└── data/                            # 示例数据集
