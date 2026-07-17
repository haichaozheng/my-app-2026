# 数据分析与可视化 — 知识地图

本知识地图按项目阶段（而非学科章节）组织课程知识节点。每个节点标注了学生何时需要该知识、为何需要、以及需要到什么深度。

**使用方式**：开学时预览全貌，但只在项目推进到对应阶段时深入学习。知识地图是导航工具，不是教学序列。

**层级定义**：
- **Essential**：完成当前阶段必须掌握
- **Recommended**：显著提升工作质量
- **Advanced**：追求卓越可选深入

---

## Phase 1: Idea Stage（W1-4）— 发现问题、定义项目

本阶段核心挑战：**如何发现金融领域的真实问题并定义一个有价值的项目？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 1.1 | PBL学习方法论 | W1 | "这门课不是老师讲我听，我要如何在做项目中有效学习？" | Essential | [PBLWorks](https://www.pblworks.org/what-is-pbl) |
| 1.2 | AI辅助编程(opencode/cursor/trae) | W1 | "如何高效编写代码、减少重复劳动？" | Essential | `ai-toolstack/ai-coding/` |
| 1.3 | Prompt Engineering基础 | W1-2 | "如何与LLM有效交互，让它帮我完成任务？" | Essential | `ai-toolstack/prompt-engineering/` |
| 1.4 | 金融数据生态与获取 | W2 | "金融数据在哪里？怎么获取？有哪些API和数据源？" | Essential | `weeks/week02/resources.md` |
| 1.5 | Prompt驱动的金融数据探索 | W2 | "拿到数据后不知道从哪里开始分析，如何用Prompt引导探索？" | Essential | `ai-toolstack/prompt-engineering/` |
| 1.6 | 用户洞察方法论 | W3 | "我访谈了5个人但提炼不出痛点，如何系统性地从用户对话中发现需求？" | Essential | `weeks/week03/resources.md` |
| 1.7 | Minimalist Entrepreneur社区先行 | W3 | "如何发现真实需求而非假想需求？为什么应该先去社区而不是先写代码？" | Recommended | `references/The Minimalist Entrepreneur.md` |
| 1.8 | Deep Research | W3 | "如何用AI做深度调研，快速了解一个领域？" | Essential | `ai-toolstack/prompt-engineering/` |
| 1.9 | 项目提案方法论 | W4 | "如何写出清晰的项目提案，让老师和同伴理解我要做什么？" | Essential | `weeks/week04/resources.md` |
| 1.10 | Andrew Ng项目筛选框架 | W4 | "我的想法够好吗？如何判断一个项目是否值得投入？" | Recommended | `references/build-career-in-ai-era.md` |

### 本阶段知识关系图

```
PBL方法论(1.1) ─→ 理解"做中学"的节奏
    │
AI辅助编程(1.2) + Prompt(1.3) ─→ 工具基础，贯穿全程
    │
金融数据生态(1.4) + Prompt探索(1.5) ─→ 从数据端发现问题
    │
用户洞察(1.6) + 社区先行(1.7) + Deep Research(1.8) ─→ 从用户端发现问题
    │
项目提案(1.9) + 项目筛选(1.10) ─→ 把发现凝练为可执行的项目
```

---

## Phase 2: MVP Stage（W5-10）— 构建最小可用产品

本阶段核心挑战：**如何把一个想法变成可运行的数据分析产品？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 2.1 | 手动流程先行理念 | W5 | "我想直接写代码做产品，但不知道分析逻辑对不对——如何先验证价值再自动化？" | Essential | `references/The Minimalist Entrepreneur.md` |
| 2.2 | 数据分析思维链 | W5 | "从数据到洞察的逻辑推导过程是什么？不是画图，而是思考链路。" | Essential | `weeks/week05/resources.md` |
| 2.3 | Pandas高级操作 | W6 | "数据量大、格式复杂，如何高效处理金融数据？" | Essential | `weeks/week06/resources.md` |
| 2.4 | 数据清洗方法论 | W6 | "数据有缺失值、异常值、格式混乱，直接分析会得出错误结论。" | Essential | `weeks/week06/resources.md` |
| 2.5 | EDA多视角分析 | W6 | "只看均值和分布不够，如何从多个角度发现数据中隐藏的规律？" | Essential | `weeks/week06/resources.md` |
| 2.6 | Prompt驱动EDA洞察 | W6 | "做了EDA但没发现有意思的结论，如何用Prompt引导AI帮我发现洞察？" | Essential | `ai-toolstack/prompt-engineering/` |
| 2.7 | 可视化设计原则 | W7 | "为什么我的图表没人能看懂？如何选择合适的图表类型？" | Essential | `weeks/week07/resources.md` |
| 2.8 | 可视化叙事 | W7 | "如何用可视化讲故事，而不是只是展示数据？" | Recommended | `weeks/week07/resources.md` |
| 2.9 | 交互式可视化工具(Plotly/Pyecharts/Echarts) | W7 | "静态图表不够，用户需要交互探索数据。" | Essential | `weeks/week07/resources.md` |
| 2.10 | 快速原型方法论 | W8 | "如何快速搭建可运行的产品原型，验证核心功能？" | Essential | `weeks/week08/resources.md` |
| 2.11 | Streamlit/Gradio | W8 | "用什么框架做数据分析产品原型？" | Essential | `weeks/week08/resources.md` |
| 2.12 | AI辅助编程加速原型 | W8 | "原型搭建速度慢，如何用AI辅助编程加速？" | Essential | `ai-toolstack/ai-coding/` |
| 2.13 | LLM API集成 | W9 | "产品需要AI交互功能——智能解读、对话问答，如何集成？" | Essential | `weeks/week09/resources.md` |
| 2.14 | RAG构建产品知识库 | W9 | "如何让产品回答金融数据相关问题？需要知识库支撑。" | Essential | `ai-toolstack/rag/` |
| 2.15 | Agent设计产品智能功能 | W9 | "如何让产品自动执行任务——自动监控、自动报告？" | Essential | `ai-toolstack/agent/` |
| 2.16 | 产品评审标准 | W10 | "如何评判一个数据产品的好坏？功能完整度、可用性、分析深度？" | Essential | `weeks/week10/resources.md` |
| 2.17 | 同侪互评方法 | W10 | "如何有效评价别人的产品，给出有建设性的反馈？" | Essential | `weeks/week10/resources.md` |

### 本阶段知识关系图

```
手动流程先行(2.1) ─→ 先验证价值再自动化
    │
数据分析思维链(2.2) ─→ 从数据到洞察的思考链路
    │
Pandas(2.3) + 数据清洗(2.4) + EDA多视角(2.5) + PromptEDA(2.6) ─→ 数据处理与洞察发现
    │
可视化原则(2.7) + 叙事(2.8) + 交互式工具(2.9) ─→ 洞察的视觉传达
    │
快速原型(2.10) + Streamlit/Gradio(2.11) + AI加速(2.12) ─→ 产品骨架搭建
    │
LLM API(2.13) + RAG(2.14) + Agent(2.15) ─→ 产品AI能力注入
    │
产品评审(2.16) + 同侪互评(2.17) ─→ 评价与迭代
```

---

## Phase 3: Launch Stage（W11-15）— 上线与迭代

本阶段核心挑战：**如何让产品上线、找到用户、持续改进？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 3.1 | 云部署 | W11 | "产品只能在本地跑，如何让目标用户公网访问？" | Essential | `weeks/week11/resources.md` |
| 3.2 | 获客与推广方法论 | W12 | "产品上线了但没人用，如何让目标用户知道并愿意尝试？" | Essential | `weeks/week12/resources.md` |
| 3.3 | Sell to Your First 100 Customers | W12 | "如何找到第一批用户？从哪里触达他们？" | Recommended | `references/The Minimalist Entrepreneur.md` |
| 3.4 | ML基础与模型选择逻辑 | W13 | "想给产品加AI预测功能，但不知道选什么模型——监督/无监督/回归/分类，如何根据问题选模型？" | Recommended | `weeks/week13/resources.md` |
| 3.4a | 回归与分类模型 | W13 | "用户想知道'这只股票未来会不会涨'或'这个客户违约概率多大'——如何用回归/分类模型做预测？" | Recommended | `weeks/week13/resources.md` |
| 3.4b | 时间序列分析与预测 | W13 | "金融数据天然是时间序列——如何用ARIMA/趋势分解/季节性分析预测市场趋势？" | Recommended | `weeks/week13/resources.md` |
| 3.4c | 特征工程与因子构建 | W13 | "ML模型效果不好，可能不是模型问题而是特征问题——如何从金融数据中提取有预测力的特征/因子？" | Recommended | `weeks/week13/resources.md` |
| 3.4d | 模型评估与验证 | W13 | "模型训练出来后，如何判断它是否真的有效？交叉验证、过拟合、偏差-方差权衡怎么处理？" | Recommended | `weeks/week13/resources.md` |
| 3.4e | ML产品化架构 | W13 | "ML模型如何嵌入数据分析产品？训练→推理→展示的架构怎么设计？" | Recommended | `weeks/week13/resources.md` |
| 3.5 | Agent驱动高级功能 | W13 | "如何让产品自动监控市场变化、自动生成报告？" | Essential | `ai-toolstack/agent/` |
| 3.6 | Skill封装可复用分析能力 | W13 | "如何把常用的分析流程封装为可复用模块，加速迭代？" | Recommended | `ai-toolstack/skill/` |
| 3.7 | UX优化 | W14 | "用户反馈产品不好用，如何改进交互体验？" | Essential | `weeks/week14/resources.md` |
| 3.8 | AI系统评估 | W14 | "产品的AI功能准确吗？可靠吗？如何系统性地评估？" | Essential | `ai-toolstack/ai-evaluation/` |
| 3.9 | 路演叙事与演讲 | W15 | "如何讲好产品故事？路演时怎么让听众理解产品价值？" | Essential | `weeks/week15/resources.md` |

### 本阶段知识关系图

```
云部署(3.1) ─→ 产品公网可达
    │
获客推广(3.2) + First 100(3.3) ─→ 找到真实用户
    │
进阶分析: ML基础(3.4) + 回归分类(3.4a) + 时间序列(3.4b) + 特征工程(3.4c) + 模型评估(3.4d) + ML产品化(3.4e) ─→ 产品分析能力深化 + Agent高级功能(3.5) + Skill封装(3.6) ─→ 产品能力深化
    │
UX优化(3.7) + AI系统评估(3.8) ─→ 产品质量打磨
    │
路演叙事(3.9) ─→ 价值传达
```

---

## Phase 4: Scale Stage（W16-17）— 展示与反思

本阶段核心挑战：**如何展示成果、反思收获、提炼可迁移的知识？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 4.1 | 路演展示与Demo | W16 | "如何在公开场合展示产品、说服评委和观众？" | Essential | `weeks/week16/resources.md` |
| 4.2 | 反思方法论 | W17 | "17周做了很多事，但收获是什么？如何从项目经历中提炼可迁移的知识？" | Essential | `templates/reflection-log.md` |
| 4.3 | 创业思维与Scale | W17 | "产品是否有商业化潜力？下一步是什么？" | Recommended | `references/the-founders-playbook.md` |

---

## 全程贯穿知识

以下知识节点不限定于某个阶段，而是贯穿全程：

| # | 知识节点 | 起始周 | 持续范围 | 层级 | 说明 |
|---|---|---|---|---|---|
| X.1 | AI辅助编程 | W1 | 全程 | Essential | 每周代码编写的基础工具 |
| X.2 | Prompt Engineering | W1 | 全程 | Essential | 与LLM交互的基础方法论 |
| X.3 | Prompt→RAG→Agent→Skill→评估 渐进融入 | W1→W9→W13→W14 | 渐进 | Essential | AI工具栈随项目需求自然深入 |
| X.4 | 金融领域知识 | W2 | 全程 | Recommended | 具体赛道领域的专业知识，学生在项目中自学 |
| X.5 | 产品思维 | W5 | W5-15 | Recommended | 从问题到产品的完整链路思维 |

---

## 赛道领域知识：量化投资

以下知识节点面向选择**量化投资/投资分析**赛道的学生。其他赛道的学生可参考但不必深入学习。量化投资知识与ML知识有交叉（因子构建、回测评估），两者共同支撑量化类产品的专业深度。

**层级说明**：对于量化赛道学生为 **Essential**，其他赛道为 **Advanced**。

| # | 知识节点 | 引入时机 | 触发挑战 | 层级(量化赛道) | 层级(其他赛道) | 参考资源 |
|---|---|---|---|---|---|---|
| Q.1 | 量化投资基础概念 | W2 | "量化投资到底是什么？策略开发全流程是怎样的？Alpha/Beta/夏普比率这些术语什么意思？" | Essential | Advanced | `weeks/week02/resources.md` |
| Q.2 | 因子投资与因子挖掘 | W6 | "量化策略的核心是因子——什么是因子？如何从金融数据中挖掘有预测力的因子？IC/IR如何评估因子质量？" | Essential | Advanced | `weeks/week06/resources.md` |
| Q.3 | 回测框架与策略评估 | W5 | "策略想法有了，但不知道能不能赚钱——如何用回测验证策略？回测引擎怎么搭建？如何避免回测陷阱（过拟合、滑点、幸存者偏差）？" | Essential | Advanced | `weeks/week05/resources.md` |
| Q.4 | 技术指标与策略逻辑 | W6 | "均线、动量、反转、波动率——常见技术指标的计算逻辑是什么？如何组合指标形成策略？" | Essential | Advanced | `weeks/week06/resources.md` |
| Q.5 | 组合优化与风险控制 | W13 | "单策略不够，如何构建投资组合？资产配置、VaR、最大回撤、风险分散的逻辑是什么？" | Essential | Advanced | `weeks/week13/resources.md` |
| Q.6 | 量化策略产品化 | W13 | "回测跑通了，但用户需要的是一个能看策略信号、实时监控、风险预警的产品——如何把策略逻辑产品化？" | Essential | Advanced | `weeks/week13/resources.md` |

### 量化投资知识关系图

```
量化基础概念(Q.1) ─→ 理解量化投资全貌
    │
回测框架(Q.3) ─→ 先验证策略再产品化（与手动流程先行(2.1)呼应）
    │
因子挖掘(Q.2) + 技术指标(Q.4) ─→ 策略核心逻辑
    │                                ↕ 与ML特征工程(3.4c)交叉
组合优化(Q.5) ─→ 从单策略到投资组合
    │
量化策略产品化(Q.6) ─→ 从策略到产品
    │                    ↕ 与ML产品化(3.4e)交叉
```

---

## 赛道领域知识：机器学习应用

以下知识节点面向所有在产品中使用**机器学习**功能的学生（不限于量化赛道）。ML知识在知识地图中有两处体现：Phase 3的3.4系列节点（侧重ML作为产品进阶功能），以及此处的赛道视角（侧重ML作为分析思维）。

**层级说明**：对于使用ML功能的学生为 **Recommended**，不使用ML的学生为 **Advanced**。

| # | 知识节点 | 引入时机 | 触发挑战 | 层级(ML产品) | 层级(非ML) | 参考资源 |
|---|---|---|---|---|---|---|
| M.1 | ML思维：从描述到预测 | W5 | "手动分析只能描述'发生了什么'，用户还想知道'未来会怎样'——ML如何从描述性分析跨越到预测性分析？" | Recommended | Advanced | `weeks/week05/resources.md` |
| M.2 | 监督学习 vs 无监督学习 | W6 | "EDA发现数据有分组/聚类特征，但不知道如何系统化——聚类/分类等不同ML范式各自解决什么问题？" | Recommended | Advanced | `weeks/week06/resources.md` |
| M.3 | ML在金融场景的应用地图 | W2 | "ML在金融领域有哪些典型应用？信用评分、风险预测、市场趋势、异常检测——每个场景用什么模型？" | Recommended | Advanced | `weeks/week02/resources.md` |
| M.4 | AI辅助ML建模全流程 | W13 | "如何用AI辅助编程完成ML建模全流程？数据准备→特征工程→模型训练→评估→部署，每一步LLM如何加速？" | Recommended | Advanced | `ai-toolstack/ai-coding/` |

### ML应用知识关系图

```
ML思维(M.1) ─→ 理解ML从描述到预测的价值跃迁
    │
ML应用地图(M.3) ─→ 金融场景与ML方法的匹配
    │
监督vs无监督(M.2) ─→ ML范式选择逻辑
    │
AI辅助ML建模(M.4) ─→ 用AI加速ML全流程
    │                    ↕ 与Phase 3的3.4系列节点衔接
```

---

## 知识引入节奏总览

```
W1  AI辅助编程 + Prompt ─────────────────────────────── 起步
W2  金融数据生态 + Prompt探索 + ML应用地图(量化赛道+ML产品) ──── 数据端探索
W3  用户洞察 + Deep Research + 社区先行 ───────────── 用户端洞察
W4  项目提案 + 项目筛选 ──────────────────────────── 凝练项目
W5  手动流程先行 + 数据分析思维链 + 回测框架(量化赛道) + ML思维(ML产品) ── 验证价值
W6  Pandas + 数据清洗 + EDA多视角 + PromptEDA + 因子挖掘+技术指标(量化赛道) + ML范式(ML产品) ── 处理与洞察
W7  可视化原则 + 叙事 + 交互式工具 ──────────────────── 视觉传达
W8  快速原型 + Streamlit/Gradio ──────────────────────── 骨架搭建
W9  LLM API + RAG + Agent ──────────────────────────── AI能力注入
W10 产品评审 + 同侪互评 ────────────────────────────── 评价迭代
W11 云部署 ─────────────────────────────────────────── 上线
W12 获客推广 ───────────────────────────────────────── 找用户
W13 进阶分析: ML基础+回归分类+时间序列+特征工程+模型评估+ML产品化 + Agent高级功能 + Skill + 组合优化+量化产品化 ── 能力深化
W14 UX优化 + AI系统评估 ────────────────────────────── 质量打磨
W15 路演叙事 ────────────────────────────────────────── 价值传达
W16 路演展示 ────────────────────────────────────────── 公开展示
W17 反思方法论 + 创业思维 ──────────────────────────── 知识重构
```
