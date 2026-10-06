# Week 02 教学计划

## 本周主题

文献检索 — 检索工具与策略

> Phase 1: Foundation 第2周。文献检索是方法论（PRISMA 流程、检索式、纳入排除标准），不是"搜一下"；AI 辅助筛选但人来定标准。

## 学习目标

- 能说明系统性文献检索的策略：检索词设计、数据库选择、纳入排除标准
- 能运用 PRISMA 流程组织文献检索过程
- 能调用学术 API（Semantic Scholar/Crossref/知网）批量获取文献元数据
- 能用 AI 辅助初筛文献，并说明 AI 辅助筛选的边界（人来定标准）

## 教学步骤（3节课）

**第1节 · 文献检索方法论（45 分钟）**

1. 文献检索为什么是方法论（10 分钟）：不是"搜一下"，而是系统性检索
2. PRISMA 流程讲解（15 分钟）：检索式构建、数据库选择、纳入排除标准
3. 检索工具盘点（10 分钟）：检索数据库（Google Scholar / Web of Science / CNKI / Semantic Scholar / Crossref）、第三方文献平台（AMiner）、个人文献管理数据库（Zotero）
4. 个人研究领域检索式初稿（10 分钟）：每位博士生草拟自己领域的检索式。💡 课堂互动：完成后与邻座交换检索式，互相指出遗漏关键词或冗余条件（3 分钟）

**第2节 · API 检索脚本实操（45 分钟）**

5. Semantic Scholar / Crossref API 演示（15 分钟）：调用 API 获取文献元数据
6. opencode 检索脚本编写（20 分钟）：批量获取文献元数据、保存为结构化文献库
7. AI 辅助初筛（10 分钟）：用 LLM 对元数据做初步筛选分类

**第3节 · 原始文献库构建与下周铺垫（45 分钟）**

8. 文献库整理与去重（15 分钟）：元数据规范化、重复剔除
9. 个人检索式迭代（15 分钟）：根据初筛结果调整检索式，补全文献
10. 纳入排除标准确认（10 分钟）：明确时间范围、方法论类型等标准
11. 下周铺垫（5 分钟）：RAG 改变文献管理范式——从"读完记住"到"检索即用"

## 交付物

- **文献检索工具列表 + 原始文献库**（评分锚点，对应 milestones §1.2）
  - 工具列表：所用的数据库、API、工具、检索式、纳入排除标准
  - 原始文献库：按检索策略获取的文献集合（含元数据）
- 方法论锚定：体现系统性检索策略、PRISMA 流程意识、AI 辅助筛选的边界

## 课后自学

- 文献检索策略：`knowledge/m1-6-literature-search.md`
- AI 辅助编程：`knowledge/m1-2-ai-coding.md`

## 课后作业

构建个人研究领域的检索式，用 API 批量获取至少 20 篇文献元数据，形成原始文献库。提交检索式、纳入排除标准与文献库。

## 参考资料

- 理念：Page, M.J. et al. (2021). "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews." *BMJ*, 372, n71
- 工具：[Semantic Scholar API](https://api.semanticscholar.org/)、[Crossref REST API](https://www.crossref.org/services/metadata-delivery/rest-api/)
- 文献平台与管理：[AMiner](https://www.aminer.cn/)、[Zotero](https://www.zotero.org/)
- `weeks/week02/lecture.md`、`weeks/week02/lab.md`
