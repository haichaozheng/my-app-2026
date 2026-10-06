# 人工智能大模型应用（AI4S）— 知识地图

本知识地图按科研模块（而非学科章节）组织课程知识节点。每个节点标注了学生何时需要该知识、为何需要、以及需要到什么深度。

**使用方式**：开学时预览全貌，但只在科研推进到对应模块时深入学习。知识地图是导航工具，不是教学序列。

**层级定义**：
- **Essential**：完成当前科研模块必须掌握
- **Recommended**：显著提升科研质量
- **Advanced**：追求卓越可选深入

---

## 模块1: 文献智能（W1-3）— 从文献到知识库

本模块核心挑战：**如何在海量文献中高效检索、阅读、综述，并构建个人AI知识库？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 1.1 | AI4S范式与方法论 | W1 | "AI4S不只是用AI写代码，而是用AI重构科研全流程——这个范式如何理解？" | Essential | `weeks/week01/resources.md` |
| 1.2 | AI辅助编程(opencode/cursor) | W1 | "科研编程效率低，如何用AI加速Python/R/Stata代码编写？" | Essential | `ai-toolstack/ai-coding/` |
| 1.3 | Prompt Engineering方法论 | 自学(W1起，贯穿全程) | "如何与LLM有效交互？系统Prompt、多轮对话、Deep Research等方法如何用于科研？" | Essential | `ai-toolstack/prompt-engineering/` |
| 1.4 | 社科科研全流程映射 | W1 | "社科科研有哪些环节？AI4S如何映射到每个环节？" | Essential | `weeks/week01/resources.md` |
| 1.5 | 文献检索策略 | W2 | "如何在Google Scholar/Web of Science/CNKI中系统检索？检索词怎么设计？" | Essential | `weeks/week02/resources.md` |
| 1.6 | RAG原理与实践 | W3 | "如何构建一个能检索个人文献的AI知识库？向量数据库、文档切分、检索策略怎么选？" | Essential | `ai-toolstack/rag/` |
| 1.7 | AI辅助文献综述 | W3 | "读了50篇文献但综述写不出来，如何用LLM辅助综述生成？" | Essential | `ai-toolstack/prompt-engineering/` |
| 1.8 | 综述写作规范 | W3 | "文献综述不是罗列，需要有逻辑框架——如何写好的综述？" | Essential | `weeks/week03/resources.md` |
| 1.9 | 知识图谱与文献计量 | W3 | "如何用可视化工具展示文献间的引用关系和知识结构？" | Recommended | `weeks/week03/resources.md` |

### 本模块知识关系图

```
AI4S范式(1.1) + 科研全流程映射(1.4) ─→ 理解AI4S的大图景
    │
AI辅助编程(1.2) + Prompt(1.3) ─→ 工具基础，贯穿全程
    │
文献检索策略(1.5) ─→ 系统性检索
    │
RAG原理(1.6) ─→ 知识库技术支撑
    │
AI综述生成(1.7) + 综述规范(1.8) + 知识图谱(1.9) ─→ 从文献到综述
```

---

## 模块2: 研究选题（W4）— 从空白到问题

本模块核心挑战：**如何在已有文献中发现研究空白，并凝练为有价值的研究问题？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 2.1 | Gap analysis方法论 | W4 | "读了很多文献但找不到gap，如何系统性地发现研究空白？" | Essential | `weeks/week04/resources.md` |
| 2.2 | Prompt驱动的gap analysis对话 | W4 | "如何用LLM对话式地探索文献空白？Deep Research + 多轮对话如何辅助选题？" | Essential | `ai-toolstack/prompt-engineering/` |
| 2.3 | 选题对话与验证 | W4 | "有了初步想法但不确定是否可行，如何与LLM对话验证？" | Essential | `weeks/week04/resources.md` |
| 2.4 | 研究问题分类与凝练 | W4 | "如何把模糊的兴趣凝练为清晰的研究问题？描述性/解释性/探索性问题如何区分？" | Essential | `weeks/week04/resources.md` |
| 2.5 | 跨范式选题策略 | W4 | "定量研究与定性研究在选题逻辑上有何不同？我的背景适合哪种范式？" | Recommended | `weeks/week04/resources.md` |
| 2.6 | Agent辅助文献空白发现 | W4 | "如何让Agent自动搜索并汇总文献中的gap？" | Essential | `ai-toolstack/agent/` |

### 本模块知识关系图

```
Gap analysis方法论(2.1) ─→ 系统性发现空白
    │
Prompt gap分析(2.2) + Agent辅助(2.6) ─→ AI驱动的gap发现
    │
选题对话与验证(2.3) ─→ 验证选题可行性
    │
研究问题分类(2.4) + 跨范式(2.5) ─→ 凝练清晰的研究问题
```

---

## 模块3: 研究设计（W5）— 从问题到方案

本模块核心挑战：**如何设计严谨的研究方案——方法、框架、假设、变量？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 3.1 | 理论框架构建 | W5 | "研究问题有了，但缺乏理论支撑——如何找到并构建理论框架？" | Essential | `weeks/week05/resources.md` |
| 3.2 | 因果推断方法论 | W5 | "社科研究需要因果结论，DID/RDD/IV等方法如何选择和应用？" | Essential | `weeks/week05/resources.md` |
| 3.3 | 变量与测量设计 | W5 | "如何把理论概念转化为可操作的变量和测量指标？" | Essential | `weeks/week05/resources.md` |
| 3.4 | 方法选择逻辑 | W5 | "定量、定性、混合方法——如何根据研究问题选择合适的方法？" | Essential | `weeks/week05/resources.md` |
| 3.5 | Prompt辅助方法匹配 | W5 | "如何用LLM对话式地探索适合我研究问题的方法？" | Essential | `ai-toolstack/prompt-engineering/` |
| 3.6 | Agent辅助研究设计 | W5 | "如何让Agent作为'研究设计顾问'帮我探索设计方案？" | Essential | `ai-toolstack/agent/` |
| 3.7 | 混合方法设计 | W5 | "如何设计定量+定性相结合的混合方法研究？" | Recommended | `weeks/week05/resources.md` |
| 3.8 | Skill研究方案模板 | W5 | "如何用Skill快速生成研究方案框架？" | Essential | `ai-toolstack/skill/` |
| 3b | 批判性思维与判断 | W5 | "我怎么知道我的研究设计是对的？我该不该信任AI给出的gap和方法建议？" | Essential | `knowledge/phase3-3b-critical-thinking.md` |

### 本模块知识关系图

```
理论框架(3.1) ─→ 理论支撑
    │
因果推断(3.2) ─→ 社科因果逻辑
    │
变量与测量(3.3) ─→ 概念→操作化
    │
方法选择(3.4) + 混合方法(3.7) ─→ 方法匹配
    │
Prompt方法匹配(3.5) + Agent设计顾问(3.6) + Skill方案模板(3.8) ─→ AI辅助设计
    │
批判性思维与判断(3b) ─→ 审视推理过程，提高研究设计判断可靠性
```

---

## 模块4: 研究实施（W6-7）— 从方案到结果

本模块核心挑战：**如何执行研究方案——构建数据集、实证估计、经济学建模、仿真？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 4.1 | 数据集构建方法论 | W6 | "研究需要的数据在哪里？变量如何操作化？API/爬虫/NLP文本提取如何选择？" | Essential | `weeks/week06/resources.md` |
| 4.2 | AI辅助编程(Python/R/Stata)深度应用 | W6 | "代码量大、逻辑复杂，如何用LLM深度辅助编程？" | Essential | `ai-toolstack/ai-coding/` |
| 4.3 | Skill封装数据采集能力 | W6 | "如何把常用的数据采集流程封装为可复用Skill？" | Essential | `ai-toolstack/skill/` |
| 4.4 | Agent数据采集 | W6 | "如何让Agent自动执行数据采集流程？" | Recommended | `ai-toolstack/agent/` |
| 4.5 | 实证估计方法AI赋能 | W6 | "回归、面板、DID、IV——如何用AI辅助实证估计？" | Essential | `weeks/week06/resources.md` |
| 4.6 | 经济学建模方法论 | W7 | "如何对经验现象构建理论模型？模型假设如何设定？" | Essential | `weeks/week07/resources.md` |
| 4.7 | 仿真实验设计 | W7 | "如何用模型做反事实实验、政策模拟？参数如何标定？" | Essential | `weeks/week07/resources.md` |
| 4.8 | Skill封装分析能力 | W7 | "如何把分析流程封装为可复用Skill？" | Essential | `ai-toolstack/skill/` |
| 4.9 | Agent编排分析流程 | W7 | "如何用Agent编排多步骤分析流程？" | Recommended | `ai-toolstack/agent/` |
| 4.10 | AI系统评估方法 | W7 | "AI辅助得出的分析结果可信吗？如何评估准确性、检测偏见、做稳健性检验？" | Essential | `ai-toolstack/ai-evaluation/` |
| 4.11 | 稳健性检验 | W7 | "核心结果是否在不同条件下都成立？如何系统性地验证？" | Essential | `weeks/week07/resources.md` |
| 4.12 | 效度验证与替代方案 | W7 | "研究结论的效度如何？有无替代解释？" | Essential | `weeks/week07/resources.md` |

### 本模块知识关系图

```
数据集构建(4.1) + AI编程(4.2) + Skill封装(4.3) + Agent采集(4.4) + 实证估计(4.5) ─→ 数据获取与实证
    │
经济学建模(4.6) + 仿真实验(4.7) + Skill分析(4.8) + Agent编排(4.9) ─→ 建模与仿真
    │
AI评估(4.10) + 稳健性检验(4.11) + 效度验证(4.12) ─→ 质量控制（嵌入各步）
```

---

## 模块5: 论文写作（W8）— 从结果到论文

本模块核心挑战：**如何将研究成果组织为规范的学术论文？**

### 知识节点

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 5.1 | 学术写作规范 | W8 | "学术论文不是报告，有严格的结构、引用、论证逻辑规范。" | Essential | `weeks/week08/resources.md` |
| 5.2 | LLM辅助学术写作 | W8 | "如何用LLM辅助各章节起草、润色、修订？注意学术诚信边界。" | Essential | `ai-toolstack/prompt-engineering/` |
| 5.3 | 论文结构与论证逻辑 | W8 | "引言→方法→结果→讨论，每部分的功能和写作逻辑是什么？" | Essential | `weeks/week08/resources.md` |
| 5.4 | LaTeX+AI | W8 | "如何用AI辅助编程(LaTeX)进行论文排版？" | Recommended | `ai-toolstack/ai-coding/` |
| 5.5 | Skill封装写作能力 | W8 | "如何把写作辅助流程封装为Skill？" | Recommended | `ai-toolstack/skill/` |
| 5.6 | 五模块整合为AI4S工作流 | W8 | "文献→选题→设计→实施→写作，如何串联为统一工作流？" | Essential | `weeks/week08/resources.md` |

### 本模块知识关系图

```
学术写作规范(5.1) + 论文结构(5.3) ─→ 写作框架
    │
LLM辅助写作(5.2) + LaTeX(5.4) + Skill写作(5.5) ─→ AI写作工具链
    │
五模块整合(5.6) ─→ AI4S全流程工作流
```

---

## 展示与反思（W9）

| # | 知识节点 | 引入时机 | 触发挑战 | 层级 | 参考资源 |
|---|---|---|---|---|---|
| 6.1 | AI4S工具栈展示与互评 | W9 | "如何向跨学科同伴清晰展示我的AI4S工具栈？" | Essential | — |
| 6.2 | 反思方法论 | W9 | "9周密集构建后，如何从经历中提炼可迁移的AI4S方法论？" | Essential | `templates/reflection-log.md` |

---

## 全程贯穿知识

| # | 知识节点 | 起始周 | 持续范围 | 层级 | 说明 |
|---|---|---|---|---|---|
| X.1 | AI辅助编程 | W1 | 全程 | Essential | Python/R/Stata代码生成的核心工具 |
| X.2 | Prompt Engineering | 自学(W1起) | 全程 | Essential | 与LLM交互的基础方法论 |
| X.3 | Prompt→RAG→Agent→Skill→评估 渐进融入 | W1→W3→W4→W6→W7 | 渐进 | Essential | AI工具栈随科研流程自然深入 |
| X.4 | 社科方法论意识 | W1 | 全程 | Essential | "做对"比"做出来"更重要的方法论自觉 |

---

## 知识引入节奏总览

```
W1  AI4S范式 + AI辅助编程(opencode/cursor) ──────── 理解大图景 + 工具起步（PE自学）
W2  文献检索策略 + API检索脚本 ──────────────────── 文献检索模块
W3  RAG + AI综述 + 综述规范 ─────────────────────── 文献综述模块
W4  Gap analysis + 选题对话 + Agent选题 ──────────── 研究选题模块
W5  理论框架 + 因果推断 + Agent设计 + Skill + 批判性思维 ─── 研究设计模块
W6  数据集构建 + AI编程深度 + Skill封装 + 实证估计 ──── 研究实施(数据+实证)
W7  经济学建模 + 仿真 + AI评估 + 稳健性检验 ──────── 研究实施(建模+仿真)
W8  学术写作 + LLM写作 + 五模块整合 ──────────── 论文写作模块
W9  工具栈展示 + 反思方法论 ───────────────────── 展示与反思
```
