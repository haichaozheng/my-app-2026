# 数据分析与可视化 — PBL教学方案

> **基准关系**：本总方案由各周 `weeks/weekXX/plan.md` 生成汇总；**每周 plan.md 为唯一准绳**，两者冲突时以 plan.md 为准并同步修订本文档。每周 plan 固定含五要素：学习目标、预计投入、三层任务（必做/进阶/兜底）、评分锚点（挂 milestones/rubric）、求助路径；另含教师向 **课堂演示工具** 与 **教学步骤**（每周 3 节×每节 45 分钟分步，见各周 plan）。

## 课程信息

- **面向对象**：财经院校本科生
- **课程目标**：提高学生做数据分析应用与产品的能力，培养学生的创新与创业思维
- **教学方法**：Project Based Learning（PBL）
- **方法论锚定**：设计科学研究（Design Science Research, DSR）
- **课程时长**：17周
- **课堂课时**：每周 3 节，每节 45 分钟（课间另计）
- **团队规模**：互助小组鼓励5人一组，每人独立完成1个产品
- **技术栈**：不限（学生自主选择）
- **先修要求**：不要求会写 Python。会使用电脑、会用大模型对话即可。编程小白走「编程小白路径」（见下节），不另开语法课。
- **课程公约**：师生共建，详见课程公约文档（待制定）
- **课程展示**：[data-analysis-showcase](https://haichaozheng.github.io/data-analysis-showcase)

## 编程小白路径

财经本科班会有从未写过代码的学生。本课程**不因此降低「一人一产品」的终点**，也不另开 Python 语法课。小白的达标从「能手写」改为：**会驱动 Cursor 写出能跑的分析，跑通后能说清这段在干什么、结果信不信**（登录或网络不顺可用 Trae）。W1 开场说清：这不是程序员训练营，第一胜是环境能跑 + 能判断 AI 对错。

| 会（学期末仍成立） | 不必会 |
|---|---|
| 安装 Cursor、打开文件夹、运行脚本 | 手写完整程序、背 API |
| 把报错最后几行贴给 AI 并改到能跑 | 独立调试复杂环境 |
| 读懂 `read_csv` / 选一列 / 出一张图 | 类、装饰器、算法、从零爬虫 |
| 改模板里的数据路径、列名、标题 | 自选 React/FastAPI |
| 对 AI 输出写一句「信/不信，因为」 | 不看代码直接交 |

| 原则 | 做法 |
|---|---|
| 混编互助组 | W1 每组至少 1 人能装环境；禁止代写，允许盯着对方自己键入 |
| 先会问再会写 | 任务说清楚、报错全文贴给 AI、会看终端红字，比背 `for` 优先 |
| 先复制再改 | 课堂回退脚本 / `weeks/week07/mvp-template/`，只改路径、列名、标题 |
| 选题收缩 | 一个公开 CSV、一类用户、一条主分析；W4 不选爬虫作主数据源 |
| 评分看判断 | 交「AI 生成 + 我改了何处 + 结果对照」即达标；抄通、说不清的不达标 |

**分阶段底线（过了就算跟上）**

- **W1–W2**：按 `weeks/week01/python-setup.md` 装 **Python 3.13（官网，不要 Anaconda，不要点首页 3.14）** + **Cursor（推荐；登录或网络不顺可用 Trae）**；一句话让 AI 读 xlsx 并打印行数/列名。W3 建仓时按 `weeks/week03/venv-setup.md` 在项目里建 `.venv`。opencode 装不上则全程 Cursor。
- **W3–W4**：选「数据已有、问题真实」；W4 主战场是 Excel 手动分析（小白优势周）；获取脚本复制课堂成品只改文件名。
- **W5–W7**：只改课堂上演示过的单元格；W7 **必须**从 mvp-template 起步，禁止空白文件从零建站。
- **W8–W15**：用课堂模板；LLM 功能沿用 W6 自学的自家 API key（`llm_api.ipynb`）；sklearn 换模型数行即可，不推公式。
- **W16**：产品能打开、能讲清问题与价值即可，不因是否手写扣路演分。

**不要做**：第一周讲变量/循环/面向对象；把《廖雪峰》整本当先修作业；让小白与有基础者比代码量；第 3 节不巡视小白座位。

## 共同AI基础工具栈

两门课程共享以下AI基础工具栈，随项目需求**渐进式融入**教学内容，而非单独设课：

| 工具 | 在课程中的角色 | 主要应用场景 |
|---|---|---|
| AI辅助编程(opencode/cursor/trae) | 开发环境与生产力工具 | 产品代码编写、调试、迭代 |
| Prompt Engineering | 与LLM交互的基础方法论 | 数据探索、用户调研、产品交互设计 |
| RAG | 产品智能功能的核心技术 | 金融数据问答、知识检索、智能解读 |
| Agent | 产品自动化与智能交互 | 金融数据监控Agent、自动化报告Agent |
| Skill | 可复用的AI能力模块 | 数据分析skill、可视化skill、报告生成skill |

> **AI系统评估是横切实践，不是独立工具**：它不单列为一行，因为它没有专属工具——评估 RAG/Agent/Skill/LLM 功能靠的是 Prompt（构造 evals 集、做可信度提问）与 Skill（封装可复用的回归测试）。评估是"验证搭出来的东西靠不靠谱"的贯穿能力，应用于所有 AI 功能：对 AI 输出做可信度判断（反思日志 4.3）、W14 策略回测中 ML 信号 vs SMA 基线即一条 criterion validity claim（产品效能 vs 参考实体）、按设计科学有效性（Larsen，criterion/causal/context validity）严格评估（见「设计科学研究方法（DSR）方法论锚定」节）、并计入 rubric「AI功能价值」的"对AI输出有可信度判断"维度。

**渐进融入节奏**：Prompt+AI辅助编程(W1起步) → **LLM API 初尝(W6课后自学 `llm_api.ipynb`，W7 起在产品内使用)** → Skills开发(W9：OpenCode Skill 封装可复用 AI 工作流) → 建模增强(W11-W15：线性回归+梯度下降/KNN+特征工程/决策树·随机森林/量化交易基础·ML信号+策略回测/多模型信号融合+路演准备) → **评估贯穿全阶段**（对 AI 输出做可信度判断，反思日志记录；W14 策略回测中 ML 信号 vs SMA 基线对比即一条 criterion validity claim；期末报告含 DSR 定位）

## 课堂演示工具约定

学生工具栈（**鼓励 Cursor**；Trae 为登录/网络备选；另有 opencode / Streamlit 等）与**教师课堂投影用什么**分开写。原则：一次课只深演示一个主工具；教师机与学生跟做环境对齐；课前备好已跑通回退成品（现场 AI 或敲代码超时即切换）。

| 课堂在做什么 | 默认工具 |
|---|---|
| 方法论、思政、评分、周目标 | 薄幻灯（约 6–15 页，不讲 API 细节） |
| 采集/清洗/EDA/可视化思维链、sklearn 对照实验 | Jupyter Notebook（cell-by-cell） |
| AI 编程、仓库、`AGENTS.md`、把分析迁进产品 | Cursor（推荐；教师机主演示。Trae 仅登录/网络不顺时学生备用，教师机备着作回退） |
| W2 数据采集与改站 / W3 建仓与 Agent 工作流 | opencode 终端（投影放大字号） |
| W7 起产品形态、路演试用 | 浏览器打开 Streamlit（本机或公网） |

各周具体组合见 `weeks/weekXX/plan.md` 的「课堂演示工具」；落到第几分钟做什么见同文件「教学步骤」（每周 3 节、每节 45 分钟，课间另计）。不把 Colab、网页 Chat、TraeWork 当投影主工具；Excel 仅 W4「手动流程」教学使用。

## AI-Native 项目工作流

本课程以 **repo 为项目管理中枢**，不引入额外 PM 工具：学生个人产品仓库即项目管理系统，opencode 读取根目录 `AGENTS.md` 与 artifact thread 接管项目上下文，git 提交历史即审计轨迹。

学生个人产品仓库约定：**根目录只放 `AGENTS.md`**（opencode / Cursor 会读这一层）；其余项目文档进 `docs/`：`journal.md`、`requirements.md`、`design.md`、`scope.md`、`community.md`。

### 项目脊柱：requirements → design → scope（+ AGENTS.md 稳定）

每轮迭代产出 / 更新四个版本控制的 markdown：

| 文件 | 位置 | 内容 | 性质 |
|---|---|---|---|
| requirements.md | `docs/` | ## 问题与用户（强制第一节：痛点/为什么/给谁/社区调研证据）+ ## 需求(Must/Should) + ## 约束与不做 | 问题+需求，per-iteration |
| design.md | `docs/` | ## 架构/组件/数据流 + ## 数据源与处理 + ## AI功能技术设计(RAG or LLM解读如何解决痛点) + ## 部署方案 | 技术 how，per-iteration |
| scope.md | `docs/` | ## 本期范围(从需求圈定子集+边界) + ## 任务清单(feature级，每任务含如何做:改哪些文件/工作顺序/测试/风险) + ## 验收标准 | 范围+任务+实现 how，per-iteration |
| AGENTS.md | 仓库根目录 | 命令/约定/架构/常见错误，一页内 | 产品级稳定，原地更新，不重建 |

### 顺序
requirements → design → scope。scope 的"本期范围"可紧跟 requirements 先草拟（圈范围不需技术设计），但"任务清单（含如何做）"须 design 之后填（架构定了才知道改哪些文件）。

### 循环（loopable）
每轮迭代：小改在文件末尾追加 `## 迭代N（触发：W12用户反馈/…）` 节、大改或转向新建 `-v2` 版本；旧内容不删，git 历史即审计轨迹。用户反馈 / 越界触发新一轮 requirements→design→scope 循环。

### AGENTS.md（稳定上下文）
每个产品一份 `AGENTS.md`（必须在仓库根目录；opencode 约定，等价于机构知识文件）：命令、约定、架构、常见错误，一页内。opencode 每次会话读取它获取项目上下文。规则：AI 在某处犯同样错误两次，就把纠正写进 AGENTS.md。它随产品演进、原地更新，不随迭代重建。学生填空模板见 `templates/AGENTS.md`。学生于 **W3 随项目基本文档课堂首次创建**（初始化个人项目仓库 + AGENTS.md 骨架，先创建、再被 opencode 读取接管；W2 先用 opencode 对话生成采集脚本与更新课程网站，不当堂建仓），此后全程维护。`docs/` 下其余文档同周随项目基本文档落地。

## 设计科学研究方法（DSR）方法论锚定

本课程**教学法层**用 PBL（如何组织学习），**方法论层**用设计科学研究（Design Science Research, DSR，如何保障"从实践中提取问题并开发系统"的学术严谨性）。DSR 的内核是"**创建并评估 IT artifact 以解决真实组织/人的问题**"——学生建金融数据分析产品解决真实痛点，本身就是 DSR 实践；本课程只是用 DSR 的词汇命名它、用 DSR 的评估框架严谨化它。**DSR 还是唯一把"已建成的产品(instantiation)"视为合法研究贡献的方法论**，这正好打通本课程"公开产品兼产学术论文"的双重产出目标（产品即 artifact，深度抽象可升级为 nascent design theory）。

> 轻量适配原则：DSR 作为**命名/定位/评估透镜**叠在现有 `requirements→design→scope` 项目脊柱与里程碑之上，不新增重型交付物。全员必做"简短 DSR 定位 + ≥1 条 criterion validity claim"；完整的 Larsen 有效性消融实验与完整的 Gregor & Hevner 知识贡献论证归入**可选"兼产论文"轨**。

### DSR 三循环 ↔ 课程映射（Hevner 2007）

| DSR Cycle | 含义 | 课程对应 |
|---|---|---|
| Relevance Cycle（相关性循环） | 环境（问题空间）↔ 研究，确保解决真实且重要的问题 | W1-W3 社区倾听 + 用户访谈；W11 部署成功当天起滚动触达（W11-W14）与 5-10 位用户反馈（W15 整理为路演素材）；W16 路演面向真实受众 |
| Rigor Cycle（严谨性循环） | 知识库（基础与方法论）↔ 研究，确保方法严谨 | `knowledge-map.md` + 共同 AI 基础工具栈；引用金融/统计/CS 既有方法 |
| Design Cycle（设计循环，中心） | build & evaluate 反复迭代 | `requirements→design→scope` 循环；MVP v0.1→v0.2→v0.3（W10 公网上线）→模型增强 v0.1→v0.2→v0.3→v1.0（W11-W15）→路演就绪；W9 互评打磨 |

### DSRM 六步 ↔ 课程阶段映射（Peffers et al. 2007）

| DSRM 步骤 | 课程阶段 | 对应交付物 |
|---|---|---|
| 1. 问题识别与动机（Problem identification and motivation） | W1-W3 Idea Stage | 问题陈述初稿 + 社区调研记录 + 项目提案 |
| 2. 定义解决方案目标（Define the objectives for a solution） | W3 | `requirements.md`（Must/Should 需求即目标） |
| 3. 设计与开发（Design and development） | W4-W10 MVP Stage | 手动流程→EDA→可视化→原型→AI 功能→打磨 |
| 4. 演示（Demonstration） | W9 互评 / W10 上线（当堂部署） / W16 路演 | MVP v0.4 演示 + 公网可访问产品 + 路演 Demo |
| 5. 评估（Evaluation） | W9 互评 + W11-W14 模型建模与回测评估 + W15 路演呈现 | 同侪互评 + 模型评估指标/回测评估 + Larsen 有效性 |
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

W14 回测评估引入设计科学有效性框架：**全员须 ≥1 条 criterion validity claim**——把产品效能与一个**参考实体**比较（如 ML 信号 vs SMA 基线、模型 vs 买入持有、手动分析 vs 自动化等）。可选论文轨可加：

- **Causal validity（因果效度）**：消融实验（去掉某模块如 RAG，对比是否仍有效）
- **Context validity（情境效度）**：外部效度（多用户/多场景）+ 生态效度（W11-W14 的 5-10 真实用户触达与反馈即生态效度证据）

> 对照 Monash/Arnott & Pervan (2012) 对 362 篇 DSS 研究的评估警示——**42.3% 无评估、75% 方法弱、85.4% 管理沟通弱**——本课程以"必做评估（针对无评估）+ 引用方法论（针对方法弱）+ 用户反馈与路演双重受众沟通（针对管理沟通弱）"针对性补强。

### Hevner 七指导原则（反思与评分透镜）

不强制逐条交付，但作为反思与 `rubric.md` 评分透镜：① Design as an Artifact（产出可用 artifact）② Problem Relevance（解决重要真实问题）③ Design Evaluation（严格评估效用）④ Research Contributions（清晰研究贡献）⑤ Research Rigor（方法严谨）⑥ Design as a Search Process（迭代搜索解）⑦ Communication of Research（向技术与管理者双受众有效沟通）。

## PBL框架

本课程以"AI赋能的一人公司（OPC）+ 互助小组"为学期长项目模式：鼓励学生5人一组组成互助小组，组内不要求共享同一条赛道或领域，但**每人独立完成并交付一个属于自己的金融数据分析产品**；学期末进行公开路演（每人独立展示个人产品；路演时产品须公网可访问，其他人可当场打开试用）。互助小组既是互助评审与经验共享的学习共同体，也是"一人公司"之间的创业生态——你的成功部分取决于你能否赋能同伴。

| PBL要素 | 课程实现 | DSR 咬合（方法论层） |
|---|---|---|
| Authentic Problem | 金融领域的真实数据与用户需求 | Relevance Cycle：W1-W3 社区倾听 + W11-W14 用户触达与反馈确保问题真实重要（Hevner 指导②） |
| Sustained Inquiry | 17周持续迭代，从选题到上线 | Design Cycle：build & evaluate 反复迭代（DSRM 步骤3→5 循环） |
| Student Voice & Choice | 学生在赛道中自选具体方向和切入点（包括个人产品方向） | Design as a Search Process：学生在约束下自主搜索解（Hevner 指导⑥） |
| Reflection | 每阶段提交反思日志 | 七指导原则自检透镜 + DSR 定位重构 |
| Critique & Revision | 组内互助评审（个人MVP互评）+ 跨组互评 + 教师反馈迭代 | Design Evaluation：严格评估效用（Hevner 指导③） |
| Public Product | 每人最终产出一个公开部署的产品并进行路演展示；路演现场其他人可打开试用 | Artifact 交付 + 向技术/管理双受众沟通（Hevner 指导①⑦） |

## 选题模式：财经新闻驱动 + 真实需求驱动 + 个人爱好

选题来源有三档，鼓励一个选题能同时命中≥2档：

| 来源 | 含义 | 举例 |
|---|---|---|
| 财经新闻驱动 | 从政策/数据发布/财经事件中提炼话题 | 央行降准、CPI超预期、某地房价异动 |
| 真实需求驱动 | 从身边人/社区观察到的真实痛点出发（吸收 Minimalist Entrepreneur"社区先行"方法） | 同学家庭账单一团乱、散户看不懂研报 |
| 个人爱好 | 从学生自身兴趣出发 | 喜欢某行业、迷某类数据可视化 |

采用"学生自选方向 + 教师提供参考选题菜单"模式：学生从三档来源自选具体产品方向，教师提供一套参考选题菜单（详见 `project-selection-guide.md`）作为启发，不强制、不限制领域。

**互助小组与"一人一产品"对齐**：鼓励学生5人一组组成互助小组，组内**不要求共享同一条赛道或领域**——每人独立选题、独立交付。互助基于工具/方法/AI应用（互相帮调试、帮选型、帮评审），而非共享领域知识；各人选题可完全不同，仍能互相赋能。这既保留"一人公司"的完整独立作品，又让互助小组成为真实有效的学习共同体（契合AI时代"一人公司"的可行路径）。

### 选题真实性与准入

财经新闻/个人兴趣类选题必须在 W3 经用户访谈验证真实需求，否则调整或重选。完整的选题准入清单、否决清单、参考选题菜单与数据源清单见 `project-selection-guide.md`。

## 17周课程安排

> 下表按各周 `weeks/weekXX/plan.md` 汇总生成；负荷提示、兜底路径、课堂演示工具、教学步骤、配套文件（mvp-template / deployment-faq / user-test-pool 等）详见各周 plan。

### Phase 1: Idea Stage（Week 1-3）— 发现问题、定义项目（DSR Relevance Cycle 为主；DSRM 步骤 1-2）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W1 | 课程启动 + PBL方法论 + AI工具栈起步 | PBL理念与 Challenge→Gap→Knowledge→Apply 循环、课程框架与公约共建（课后填问卷，不当场改措辞）、"一人公司+互助小组"模式、AI辅助编程实操（**鼓励 Cursor**；Trae 为登录/网络备选；TraeWork、workbuddy 体验）、国家财政数据案例演示、Prompt三原则实操中体验（不单独讲）、社区调研（人为谁、场合在哪、三种进入方式、原话） | 破冰、组建互助小组（基于工具/方法互助，不限同领域）、安装配置环境并用 AI 辅助完成环境验证、国家财政数据探索（提3个有趣问题）、完成并提交社区调研（`templates/community.md` 全文，含 ≥3 条原话）。**仓库与 AGENTS.md 有意留到 W3 随项目基本文档课堂创建**（W2 先用 opencode 对话拉数与改站，不当堂建仓） | 互助小组协议 + 社区调研记录（milestones §1.1）+ 公约问卷（`pic/class-norms.png`） |
| W2 | 数据全景 + opencode + 社区倾听延续 | opencode 安装配置与选模型（默认免费可跟课）、用 opencode 分析 W1 公约问卷并改 `rules.html` 更新课程网站（不只对话）、数据生态概览与多维分类（生成/开放/成本/通道；产业新闻导入）、opencode 全程对话生成 `.py` 拉西财要闻一页（具体代码 W3 再学）、社区倾听延续 | 收 W1 互助小组协议纸质签字版、课堂定稿公约并更新课程网站、跟做生成抓取脚本并课后继续拉数（本周交 Word 实验报告，数据与代码 W3 课堂展示运行）、继续社区倾听补原话（W1 未满 3 条的补齐，最好补到 10 条）。**建仓与 AGENTS.md 留到 W3 随项目基本文档课堂创建** | 西财要闻采集 Word 实验报告（须用 opencode + Cursor 完成；milestones §1.2） |
| W3 | 项目基本文档、虚拟环境、社区互查、数据采集与项目提案 | **初始化个人项目仓库与创建根目录 `AGENTS.md`**（`docs/` 下 journal / requirements / design / scope / community 五件骨架）、`.venv` 虚拟环境与 Jupyter 内核（`weeks/week03/venv-setup.md`）、批判性读财经新闻（数字 vs 判断）、requests + BeautifulSoup 采集代码精讲（同学展示 W2 作业数据；Andrew Ng「Coding AI Is the New Literacy」导入）、社区先行/用户访谈、Deep Research Prompt 用户洞察调研、从社区调研中发现并验证可产品化痛点、如何写好的项目提案（`docs/requirements.md` 格式与准入8项）、Andrew Ng 项目筛选框架（痛点筛选与 Ng 五步 W4 补课） | 建仓并补齐 `docs/` 五件、按约定建 `.venv`（勿提交该文件夹）、互查 `docs/community.md`（人=后续产品服务对象，原话追加）、完成≥1周社区倾听、形成或验证选题痛点、Deep Research 交叉验证、筛掉无真实需求选题、完成≥1次用户访谈（补充调研写回同一份 `community.md`）、以 `docs/requirements.md` 提交提案并过选题准入清单8项。兜底：未过审走48h快速重提通道 | 个人项目仓库（根目录 `AGENTS.md` + `docs/` 五件骨架；推远端为选做）+ 个人问题陈述初稿（附 `docs/community.md`；milestones §1.3）+ 个人项目提案（`docs/requirements.md` 形式；milestones §1.4） |

### Phase 2: MVP Stage（Week 4-10）— 构建最小可用产品（DSR Design Cycle·build；DSRM 步骤 3）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W4 | 手动流程先行 + 项目数据获取与落盘 + 批判性思维与判断（**课外12-15h，全课程工程最重周，提示错峰**） | 项目数据获取与落盘（复用W2知识：AKShare/Tushare、限流/复权/对齐、落盘CSV/DuckDB）、网页数据采集（requests+BeautifulSoup、crawl4ai、爬虫伦理与合规）、Minimalist Entrepreneur"先建手动流程"理念、数据分析思维链、批判性思维与判断、AI辅助编程加速获取脚本编写 | 编写获取脚本落盘项目数据集（API或网页采集+合规自检）、在落盘数据上手动完成一次完整分析、记录边界问题与假设。**"手动流程转代码"移入 W5**（本周只要求拿到数据+跑通逻辑）；兜底：数据源拉不通走备选源/收缩数据定义并周五报备 | 项目数据集 + 个人手动分析报告（milestones §2.1） |
| W5 | 数据清洗与探索 + Prompt驱动EDA | Pandas高级、缺失值/异常值处理、EDA、AI辅助编程生成清洗代码与转化手动流程、Prompt驱动EDA洞察 | 完成清洗与EDA、**用 opencode 将 W4 手动流程转化为代码并验证一致性**（转化代码服务 W6/W7）、Prompt 生成≥3洞察 | 个人EDA报告 + 手动→自动转化代码（含验证对比；milestones §2.2） |
| W6 | NumPy/Pandas 进阶与 Matplotlib 静态可视化（**工具基础周**） | NumPy 基础（ndarray vs list、数组属性与布尔索引、矩阵乘法——神经网络全连接层视角、切片步长）、pandas 数据预处理（类型转换/排序/删列删行、Timestamp/Timedelta 与 apply）、groupby（单列/多列）+ unstack/MultiIndex、matplotlib 与 pandas.plot 静态图；**课后自学 `llm_api.ipynb`**（DeepSeek API 接入：密钥管理、openai SDK 对接、封装 `deepseek_chat`，为 W7 产品接入大模型能力铺垫） | 项目数据聚合与静态图 Notebook（≥1 个 groupby 聚合 + ≥2 张静态图，每图配一句"回答什么问题"，图之间不要求叙事）；课后跑通 DeepSeek API 并完成新闻关键词提取/一句话摘要练习（自备 API key，LOGO 生成选学） | 项目数据聚合与静态图 Notebook（milestones §2.3 的图表素材储备）+ 技能小练 |
| W7 | 产品原型搭建 + AI辅助编程加速原型 | Streamlit 快速原型（必做）、Gradio（可选）、AI辅助编程加速、Skill作为可选产品形式；进阶自学 React/Vue+FastAPI | 将 W5 EDA 发现与 W6 静态图迁移进产品框架，搭建个人 MVP 原型（产品内 LLM 能力用 W6 自学的 DeepSeek API）；**课后提交个人项目选题报告**（`docs/requirements.md` 更新版「选题报告 v2」：整合 W1-W6 痛点验证、数据落地、EDA 发现与图表储备，作为迭代至路演的锚与教师深评点）；兜底：`weeks/week07/mvp-template/` 最小骨架起步，底线=能打开+展示一个核心分析 | 个人MVP v0.1（可运行；milestones §2.4）+ 个人项目选题报告（milestones §1.4 的期中定稿版） |
| W8 | 可视化设计（**弹性缓冲周**）+ 文本分析入门 | 可视化设计原则（好图/坏图对照、叙事序列）、传统分词 vs 大模型 tokenization、情感分析（词典/分类器 vs 大模型——均已是基本解决的任务，重在核对结果可信度）、Plotly/Pyecharts 交互式可视化（承载主体 Jupyter Notebook，当周或随后迁入产品）、故事化叙事 | 设计核心可视化方案+图表设计说明（必做）；交互式图表实现可当周迁入产品或随后合并完成；本周同时用于吸收 W4-W7 欠账 | 个人可视化方案（设计说明必做；milestones §2.3） |
| W9 | LLM 原理与 OpenCode Skills 开发 + 同侪互评 + 开始打磨 | LLM 原理回顾（N-gram→RNN→GPT→Attention/Transformer）、向量与余弦相似度、OpenCode 工具体系与 Skill 基础（SKILL.md 结构、按需加载、tushare/gstack Skill）、Skill 开发实践（创建最简 Skill、为自己的项目封装可复用指令）、产品评审标准、同侪互评方法（`templates/peer-review.md` Part A）、定向打磨与技术债清理；进阶自学 MCP/Agent/协同架构 | 组内MVP互评（每人≥3条"情境-现象-建议"结构化反馈）、据反馈产出采纳/不采纳理由并迭代 v0.3、为自己的项目创建 ≥1 个 OpenCode Skill（SKILL.md） | 组内互评反馈 + 个人MVP v0.3 + OpenCode Skill（milestones §2.6） |
| W10 | 打磨迭代 + 上线部署（**首选 Streamlit Cloud，当堂部署**） | 据反馈定向打磨与技术债清理、Streamlit Cloud 部署五步（GitHub 仓库 → `requirements.txt` 冻结依赖 → streamlit.io 平台配置 → Secrets 管理密钥（`st.secrets`）→ 验证公网 URL）、部署三件事（依赖/密钥/数据）与平台三约束（休眠冷启动、资源限额、临时文件系统——SQLite 只读可用、写入会丢）、进阶自建路线（腾讯云轻量/CloudBase，校园免费额度**审核有等待期，周初申请**，适合需数据库写入/常驻进程/自定义域名者）、DSR 自检方法（写入本周提交的 `journal.md`，不另开反思文件；排障随查 `weeks/week10/deployment-faq.md`） | 完成打磨产出 v0.4（可演示）、**部署 v0.4 到 Streamlit Cloud 公网可访问（当堂人人出 URL，课后手机/异地网络各验证一次）**、撰写部署方案（路线理由+密钥管理+数据方案+升级触发条件）；进阶：腾讯云自建两路线对比/自定义域名/UptimeRobot 监控；兜底：当堂未出 URL 课后 48h 对照 FAQ 排障，仍不通先用 `mvp-template` 部署占位 URL 保底；**本周末做阶段回顾，DSR 自检(MVP 阶段)写入 `journal.md` 全文提交** | 个人MVP v0.4 + 公网可访问的部署 URL（首选 Streamlit Cloud）+ 个人上线部署方案（milestones §2.7） |

### Phase 3: Launch Stage（Week 11-15）— 上线与迭代（DSRM 步骤 4 演示 + 步骤 5 评估；Larsen 有效性：W14 回测中 ML 信号 vs SMA 基线即 ≥1 条 criterion validity claim）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W11 | 机器学习建模基础 | 训练/测试划分直觉（全量fit vs 划分后测试分对比）、预测任务与ML范式（分类/回归、监督/无监督/强化学习）、梯度下降（f(x)=x² 可视化学习率过大/过小）、线性回归（sklearn LinearRegression + 手写SGD填空，gdp_satisfaction.csv）、接到自己的数据（三步改法） | 部署验收为课后事项（提交URL即可，未通者按W10兜底执行）；建立第一个基础模型（线性回归）+划分+初步评估；**部署成功当天即发产品链接开始用户触达**（班级群/朋友圈/已加入社区，滚动至W14） | 个人产品公网可访问（MVP v0.4）+ 基础模型（线性回归）（milestones §3.1） |
| W12 | KNN + 特征工程 | KNN分类（课堂手算K值、sklearn KNeighborsClassifier、投票一致性——与W11线性回归对比"回归学规律 vs KNN找邻居"）、特征工程（选择/构造/转换）、评估指标初步（准确率/MSE）、避免数据泄漏、朴素贝叶斯（自学视频10.1/10.2，约1h）、进阶可选：时间序列/因子/无监督、获客渠道复盘与深化（触达自W11已开始） | 用KNN升级或对比W11基础模型、结合特征工程完善特征、过拟合自检；自学朴素贝叶斯；复盘W11以来触达进展、调整扩大渠道（目标W14收口5-10条反馈）；兜底：互助测试池（`weeks/week13/user-test-pool.md`）+教师转介 | 模型迭代版（KNN或改进特征的W11模型）+ 获客进展记录（milestones §3.2） |
| W13 | 决策树与随机森林 | 决策树（分裂直觉：信息增益/基尼系数、过拟合倾向、剪枝一句话带过）、随机森林（bagging+随机特征→为何比单树稳、特征重要性反哺W12特征工程）、三种模型对比（线性回归学规律/KNN找邻居/决策树学规则——思路差异与适用场景） | 用决策树/随机森林升级或对比W11-W12模型、结合特征重要性完善特征；进阶：调max_depth/n_estimators观察过拟合、四模型同数据同指标对比 | 决策树/随机森林模型（含特征重要性）（milestones §3.3） |
| W14 | 量化交易基础：从SMA到ML信号 + 策略回测评估 | 量化交易流程（数据→信号生成→回测→评估）、SMA策略回测入门（`Trading strategy evaluation - sma.ipynb`）、ML信号生成（用RF/KNN/线性回归预测涨跌→买卖信号）、多模型融合思路引入（投票法/加权法）、策略回测评估（收益曲线、夏普比率、最大回撤、胜率）、训练集vs测试集在量化中的应用（W11 train/test split的复用） | 用≥1种已学模型从金融数据生成交易信号、完成策略回测、与SMA基线或买入持有对比；进阶：用≥2种模型生成信号对比效果 | ML信号生成+策略回测报告（含评估指标、与基线对比、训练/测试划分说明）（milestones §3.4） |
| W15 | 多模型信号融合 + 路演准备 | 多模型信号融合实践（≥2种模型生成信号→投票/加权融合→回测对比单一模型）、课程总结（W11-W15完整路径：三种模型+量化交易+Skills开发）、路演叙事方法论（故事线"问题→方案→产品(含模型)→价值"、Demo设计原则）、PPT大纲制作与Demo脚本设计 | 多模型信号融合实践；路演PPT大纲（≤8页）+Demo脚本（≤3步）；用户反馈整理为路演"价值与数据"页素材 | 多模型信号融合结果 + 路演PPT大纲与Demo脚本（milestones §3.5） |

### Phase 4: Scale Stage（Week 16-17）— 展示与反思（DSRM 步骤 6 沟通；全员 DSR 定位写入 `final-report.md`）

| 周次 | 主题 | 教学内容 | 项目活动 | 交付物 |
|---|---|---|---|---|
| W16 | 路演叙事 + 公开路演（产品公网可访问，现场可打开试用） | 路演叙事与演讲（故事线、Demo设计、时间控制、价值传达）、课堂制作与彩排、公网访问与现场试用规则 | 课堂完成路演材料并彩排；全员公开路演，产品须公网可访问，其他同学和观众当场打开试用；课程展示网站作为入口；兜底：现场故障切录屏Demo | 路演评分（milestones §4.1） |
| W17 | 反思与展望 | Founder's Playbook Scale阶段思维、反思方法论与个人知识框架重构（课堂工作坊）、期末360°互评实施流程 | 撰写最终报告（`templates/final-report.md`，含必做DSR定位节）、整理仓库与公开链接、课堂完成360°匿名互评、最终阶段反思（DSR自检全程版）；兜底：产品未完整上线仍以repo+演示视频构成评估证据 | 个人项目最终报告 + 个人产品仓库链接 + 360°互评表（milestones §4.2） |

## 评分体系

采用"总成绩 = 平时成绩 + 个人项目"结构（满分100 = 50 + 50）。平时成绩含其他条目40分与协作互评10分。**凡打分处一律采用百分制(0-100)**，评出的百分制分再折算为对应分数。

**第一层**：

| 评分项 | 满分 | 内部构成 | 评分方式 |
|---|---|---|---|
| 平时成绩 | 50分 | 平时其他条目40 + 协作互评10 | 见下表 |
| 个人项目 | 50分 | 百分制分 = 产品质量×0.6 + 项目报告×0.4（两项均百分制） | 教师百分制评分÷100×50 |

**平时成绩构成细目（第二层）**：

| 构成项 | 满分 | 内部构成 | 评分方式 |
|---|---|---|---|
| 平时其他条目 | 40分 | 出勤与课堂参与、技能小练、阶段里程碑交付、项目日志(journal.md) | 教师百分制综合评分÷100×40（子项比例不细分） |
| 协作互评 | 10分 | 组内其他成员匿名百分制打分算术平均 | 计入平时，期末(W17)一次360°互评，÷100×10 |

**个人项目内部（折算满分50分）**
- **产品质量（占个人项目0.6）**：百分制评分。最终产品（含模型与路演 Demo）+ 公开路演Demo
- **项目报告（占个人项目0.4）**：百分制评分。一份综合文档，含产品论证与设计资料、组内协作贡献记录、用户反馈与获客、最终反思、**DSR 定位（全员必做：artifact 类型 + 知识贡献定位 + ≥1 条 criterion validity claim + 参考实体 + relevance/rigor 证据）**（模板见`templates/final-report.md`）

**协作互评（折算满分10分，计入平时，期末评定）**：期末(W17)一次360°匿名互评，每人给组内其他成员打0-100分，算术平均÷100×10折算。依据为各人报告中的"协作贡献"记录 + 亲历。

**总成绩公式**

```
总成绩 = 平时成绩 + 个人项目                    （满分 100）

平时成绩（满分50）   = 平时其他条目 + 协作互评
  平时其他条目（满分40） = 平时其他百分制评分 ÷ 100 × 40
  协作互评（满分10）     = 组内他人打分(百分制)均值 ÷ 100 × 10
      （计入平时，期末评定）

个人项目（满分50）     = 个人项目百分制分 ÷ 100 × 50
    个人项目百分制分 = 产品质量(百分制)×0.6 + 项目报告(百分制)×0.4
```

**合计**：平时50（其他条目40 + 协作互评10）+ 个人项目50。

> 详细量化标准见 `rubric.md`；阶段里程碑定义见 `milestones.md`；报告模板见 `templates/final-report.md`（含必做的「DSR 定位」节，对应本课程「设计科学研究方法（DSR）方法论锚定」节）。

## 关键设计原则

1. **真实性优先**：选题来自金融领域真实痛点，数据来自真实数据源
2. **先手动再自动**：Week 4的核心理念——先用手动流程验证价值，再自动化为产品
3. **大模型作为赋能工具**：学生在产品中集成LLM能力（智能解读、对话交互），而非仅用大模型写代码；AI辅助编程是单人交付产品的核心生产力杠杆
4. **社区驱动选题**：Inspired by Minimalist Entrepreneur——从金融社区中发现问题
5. **财经新闻 + 真实需求 + 个人爱好驱动选题**：从财经新闻观察、身边真实需求或自身兴趣出发提炼选题，并经用户访谈验证真实性——避免选题偏离真实需求
6. **公开产品为终点**：路演面向全校/企业合作伙伴，每人产出并可公开访问一个独立产品；路演现场其他人可打开试用
7. **AI基础工具栈渐进融入**：Prompt+AI辅助编程(W1起步) → LLM API初尝(W6课后自学、W7产品内使用) → Skills开发(W9：OpenCode Skill 封装可复用 AI 工作流) → 建模增强(W11-W15：线性回归+梯度下降/KNN+特征工程/决策树·随机森林/量化交易基础/多模型信号融合+路演准备) → 评估贯穿（W14 回测即 criterion validity claim）；工具随项目需求自然引入，进阶(Agent/MCP/RAG/时间序列)可选
8. **AI赋能个体 / 一人公司（OPC）导向**：在强AI工具加持下，5人互助小组内**每人独立完成并交付一个完整产品**，模拟"一人公司"的真实可行路径；互助小组替代传统分工团队，强调"一人公司的创业生态"——既锻炼独立交付，又通过协作互评（计入平时）激励彼此赋能
9. **知识框架有机支撑**：知识按项目阶段而非学科章节组织（见`knowledge-map.md`），通过里程碑制造知识缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply节奏），反思写在 `docs/journal.md`（见 `templates/journal.md`、`templates/journal-rules.md`），交付物锚定核心知识概念（见`milestones.md`）
10. **AI-Native 项目工作流**：以 requirements→design→scope（循环）+ AGENTS.md（稳定）为项目脊柱，repo 为真相源，opencode 读 AGENTS.md 接管项目上下文，git 历史为审计轨迹——不引入额外 PM 工具（详见上文「AI-Native 项目工作流」节）
11. **设计科学方法论锚定**：以 DSR 三循环（相关性/严谨性/设计）与 DSRM 六步为方法论骨架，使 PBL 项目既具教学真实性又具研究严谨性；产品即 artifact、评估即 evaluation、社区反馈即 relevance cycle——为"公开产品兼产论文"提供学术方法保障（详见上文「设计科学研究方法（DSR）方法论锚定」节）
12. **反思与日志闭环**：`docs/journal.md` 按学习日追加（决定、学习、卡点、互助），一周条目合起来即周反思；W3 交全文选做，W10 / W15 / W17 提交全文；期末 `final-report.md` 综合闭环（详见 `templates/journal.md`、`templates/journal-rules.md`）
13. **课程公约师生共建**：W1 课后填公约问卷，教师收集为数据；W2 课堂一起分析分歧条款，整理成课堂公约，作为课程文化与协作的基础
14. **周计划透明化与兜底**：每周 plan.md 固定五要素——学习目标（可测量）、预计投入（课外工时预算）、三层任务（必做/进阶/兜底）、评分锚点（挂 milestones §与 rubric 维度 + 提交前自检清单）、求助路径（AI→互助组→课程群 24h→课堂一对一交流）；配套兜底资源：W7 `mvp-template`、W10-W11 `deployment-faq`（W10 当堂部署/W11 验收随查，录屏暂过）、W12-W14 `user-test-pool`（互助测试池/转介/3深访替代）——保证任何单点受阻不致掉队
15. **负荷节奏控制**：W4 为全课程工程最重周（课外12-15h，提示错峰）；W11 部署验收改课后不占课堂；W15 路演准备较轻（课外4-6h）；W6 插入工具基础周补齐 NumPy/Pandas/静态可视化底子，W8 指定为弹性缓冲周吸收欠账；技能小练仅在负荷可承受周设置（W1/W2/W5-W9/W11/W12/W13 共 10 次，见 rubric 与 `weeks/weekXX/lab.md`）

## 参考资料

- **视频资料库**（`video-resources.md`，超星学习通平台 <https://v8.chaoxing.com/>）：网络爬虫/词语切分/文本量化/Numpy/Pandas/数据可视化/数据库/机器学习/朴素贝叶斯/SVM/决策树随机森林/深度学习/自然语言技术系列视频的按需资源目录，含逐周映射与使用模式（课前预习/安排自学/按需补缺/进阶拓展/课后自愿）
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
├── video-resources.md               # 视频资料库（超星学习通）：按需资源目录+逐周映射
├── ai-toolstack/                    # 共同AI基础工具栈教学材料
│   ├── ai-coding/                   # AI辅助编程(opencode/cursor/trae)
│   ├── prompt-engineering/          # Prompt Engineering
│   ├── rag/                         # RAG原理与实践
│   ├── agent/                       # Agent设计与开发
│   ├── skill/                       # Skill封装与复用
│   └── ai-evaluation/               # AI系统评估
├── templates/                       # 学生模板文件
│   ├── project-proposal.md          # 项目提案模板（历史，已并入 requirements.md）
│   ├── peer-review.md               # 同侪互评模板
│   ├── final-report.md              # 最终报告模板
│   ├── requirements.md              # 产品需求模板（项目工作流，W3提交）
│   ├── design.md                    # 技术方案设计模板（项目工作流，W4提交）
│   ├── scope.md                     # 范围与任务模板（项目工作流，W4提交）
│   ├── journal.md                   # 学生复制到 docs/journal.md 后按日填写
│   ├── journal-rules.md             # 项目日志用途与交法
│   ├── community.md                 # 社区调研：W1 交齐全文，W3 迁入 docs/community.md 后续追加
│   └── AGENTS.md                    # 产品稳定上下文模板（opencode 读取）
├── weeks/                           # 每周教学材料
│   ├── week01/
│   │   ├── plan.md                  # 周计划（准绳：目标/投入/三层任务/评分锚点/求助路径）
│   │   ├── lab.md                   # 技能小练（W1/W2/W5-W9/W11/W12/W13 实配；其余周标注"本周无小练"及理由）
│   │   └── lecture.md               # 课堂内容（待补）
│   ├── week07/mvp-template/         # Streamlit 最小骨架（app.py + requirements.txt + README，W7 兜底）
│   ├── week10/deployment-faq.md     # 部署排障 FAQ（W10 当堂部署 / W11 验收随查）
│   ├── week13/user-test-pool.md     # 互助测试池规则（W12-W14 获客兜底）
│   ├── ...                          # week02-week17（lecture.md 与 resources.md 待补）
├── examples/                        # 示例产品/案例
│   ├── prediction-market/           # 人机融合预测市场示例（可fork的独立产品）
│   ├── stock-dashboard/              # 股票分析Dashboard示例
│   ├── credit-scoring/              # 信贷评分示例
│   └── risk-monitor/                # 风险监控示例
└── data/                            # 示例数据集
