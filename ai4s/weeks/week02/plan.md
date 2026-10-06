# Week 02 教学计划

## 本周主题

文献检索 — 检索工具与策略 + Skill 基础

> Phase 1: Foundation 第2周。文献检索是方法论（PRISMA 流程、检索式、纳入排除标准），不是"搜一下"；AI 辅助筛选但人来定标准。本周引入 Skill 概念——把检索能力封装为可复用工具。

## 学习目标

- 能说明系统性文献检索的策略：检索词设计、数据库选择、纳入排除标准
- 能运用 PRISMA 流程组织文献检索过程
- 能调用学术 API（Semantic Scholar/Crossref/知网）批量获取文献元数据
- 能用 AI 辅助初筛文献，并说明 AI 辅助筛选的边界（人来定标准）
- 能说明 Skill 的基本概念（输入/输出/边界），并把检索脚本封装为可复用 Skill

## 教学步骤（3节课）

**第1节 · 文献检索方法论（45 分钟）**

1. 文献检索为什么是方法论（10 分钟）：不是"搜一下"，而是系统性检索
2. PRISMA 流程讲解（15 分钟）：检索式构建、数据库选择、纳入排除标准
3. 检索工具盘点（10 分钟）：检索数据库（Google Scholar / Web of Science / CNKI / Semantic Scholar / Crossref）、第三方文献平台（AMiner）、个人文献管理数据库（Zotero）
4. 个人研究领域检索式初稿（10 分钟）：每位博士生草拟自己领域的检索式。💡 课堂互动：抽取 2-3 位同学投屏检索方式，全班交流（3-4 分钟）

**第2节 · Skill 基础知识（45 分钟）**

5. Skill 是什么（10 分钟）：可复用能力封装，输入/输出/边界——类比"写函数"但粒度更大、可被 AI 调用
6. opencode Skill 创建与调用（15 分钟）：skill 文件结构、参数传递、调用方式
7. 演示：把 W1 的 `wb_explore.py` 封装为 Skill（10 分钟）：输入指标代码和国家→输出 DataFrame，边界清晰
8. 学生跟做最简 Skill（10 分钟）：每人写一个能跑的最简 Skill

**第3节 · API + Skill 检索实操（45 分钟）**

9. Semantic Scholar / Crossref API 演示（10 分钟）：调用 API 获取文献元数据
10. 用 Skill 封装检索脚本（20 分钟）：把 API 调用封装为"文献检索 Skill"——输入检索词，输出文献列表（含元数据）
11. AI 辅助初筛（8 分钟）：用 LLM 对元数据做初步筛选分类
12. 下周铺垫（7 分钟）：W3 会把这些原始文献导入 Zotero 清洗 + 用第三方工具做智能检索与综述

## 交付物

- **文献检索工具列表 + 检索 Skill + 原始文献元数据**（评分锚点，对应 milestones §1.2）
  - 工具列表：所用的数据库、API、工具、检索式、纳入排除标准
  - 检索 Skill：封装的文献检索 Skill（可复用，输入检索词→输出文献列表）
  - 原始文献元数据：按检索策略获取的文献集合（CSV 格式，尚未清洗去重）
- 方法论锚定：体现系统性检索策略、PRISMA 流程意识、AI 辅助筛选的边界、Skill 封装逻辑

## 课后自学

- 文献检索策略：`knowledge/m1-6-literature-search.md`
- AI 辅助编程：`knowledge/m1-2-ai-coding.md`
- Skill 基础与封装：[opencode Skill 文档](https://opencode.ai/docs/)

## 课后作业

构建个人研究领域的检索式，用 API 批量获取至少 20 篇文献元数据（CSV），封装为文献检索 Skill。提交检索式、纳入排除标准、文献元数据 CSV 与 Skill 代码。

## 参考资料

- 理念：Page, M.J. et al. (2021). "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews." *BMJ*, 372, n71
- 工具：[Semantic Scholar API](https://api.semanticscholar.org/)、[Crossref REST API](https://www.crossref.org/services/metadata-delivery/rest-api/)、[opencode Skill 文档](https://opencode.ai/docs/)
- 文献平台与管理：[AMiner](https://www.aminer.cn/)、[Zotero](https://www.zotero.org/)
- `weeks/week02/lecture.md`、`weeks/week02/lab.md`
