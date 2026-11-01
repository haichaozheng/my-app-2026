# Week 02 教学计划

## 本周主题

文献检索 — 检索工具与策略

> Phase 1: Foundation 第2周。文献检索是方法论（PRISMA 流程、检索式、纳入排除标准），不是"搜一下"；AI 辅助筛选但人来定标准。本周是 W1 AI 辅助编程的第一次真实科研应用——用 opencode 开发结构化检索脚本。

## 学习目标

- 能说明系统性文献检索的策略：检索词设计、数据库选择、纳入排除标准
- 能运用 PRISMA 流程组织文献检索过程
- 能调用学术 API（Semantic Scholar/Crossref/知网）批量获取文献元数据
- 能用 opencode 开发结构化检索脚本（检索式参数化、API 批量调用、CSV 存储），并与 AI 结对调试迭代
- 能用 AI 辅助初筛文献，并说明 AI 辅助筛选的边界（人来定标准）
- 能说明检索可复现意识：检索式、数据库、日期、命中数留痕，每次检索可复现

## 教学步骤（3节课）

**第1节 · 文献检索方法论（45 分钟）**

1. 文献检索为什么是方法论（10 分钟）：不是"搜一下"，而是系统性检索
2. PRISMA 流程讲解（15 分钟）：检索式构建、数据库选择、纳入排除标准
3. 检索工具盘点（10 分钟）：检索数据库（Google Scholar / Web of Science / CNKI / Semantic Scholar / Crossref）、第三方文献平台（AMiner）、个人文献管理数据库（Zotero）
4. 个人研究领域检索式初稿（10 分钟）：每位博士生草拟自己领域的检索式。💡 课堂互动：抽取 2-3 位同学投屏检索方式，全班交流（3-4 分钟）

**第2节 · AI 辅助编程深化：开发结构化检索脚本（45 分钟）**

5. 从小脚本到结构化脚本（10 分钟）：W1 的 `wb_explore.py` 是单文件小脚本；检索脚本需要结构——检索式参数化、API 调用、分页与限流、异常处理、CSV 存储
6. opencode 开发检索脚本演示（15 分钟）：对话式开发学术 API 检索脚本——参数化检索式、批量获取 ≥20 篇元数据、增量写入 CSV；AGENTS.md 同步更新（目录约定、原始文献库数据说明）
7. 学生跟做与结对调试（12 分钟）：每人把演示脚本改成自己领域的检索式，跑通拿到第一批元数据；报错按"问 AI（附报错）→ 同学互助 → 举手教师"顺序排障
8. 检索留痕意识（8 分钟）：检索式、数据库、日期、命中数——每次检索可复现，为 W3 清洗与 PRISMA 流程图留证据

**第3节 · 多源检索实操与 AI 辅助初筛（45 分钟）**

9. 多源 API 检索实操（15 分钟）：Semantic Scholar / Crossref（/知网）同一检索式分别检索，比较结果差异，标记去重字段
10. 补全原始文献库（10 分钟）：迭代检索式，补全至 ≥20 篇；增量写入 CSV
11. AI 辅助初筛（12 分钟）：人定纳入排除标准 → AI 按标准对元数据（标题/摘要）做初步筛选分类 → 抽查校准；边界：AI 执行筛选，人来定标准
12. 下周铺垫（8 分钟）：W3 把原始文献库导入 Zotero 清洗、用第三方工具做智能检索与综述；预告进阶轨（手写最小 RAG，加分）

## 交付物

- **文献检索工具列表 + 原始文献元数据**（评分锚点，对应 milestones §1.2）
  - 工具列表：所用的数据库、API、工具、检索式、纳入排除标准
  - 检索脚本：可运行的 opencode 检索脚本（检索式参数化，可复现）
  - 原始文献元数据：按检索策略获取的文献集合（CSV 格式，尚未清洗去重，含检索留痕：检索式、数据库、日期、命中数）
- 方法论锚定：体现系统性检索策略、PRISMA 流程意识、AI 辅助筛选的边界、检索可复现意识

## 课后自学

- 文献检索策略：`knowledge/m1-6-literature-search.md`
- AI 辅助编程：`knowledge/m1-2-ai-coding.md`

## 课后作业

构建个人研究领域的检索式，用 API 批量获取至少 20 篇文献元数据（CSV）。提交检索式、纳入排除标准、文献元数据 CSV 与检索脚本代码。

## 参考资料

- 理念：Page, M.J. et al. (2021). "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews." *BMJ*, 372, n71
- 工具：[Semantic Scholar API](https://api.semanticscholar.org/)、[Crossref REST API](https://www.crossref.org/services/metadata-delivery/rest-api/)、[opencode 文档](https://opencode.ai/docs/)
- 文献平台与管理：[AMiner](https://www.aminer.cn/)、[Zotero](https://www.zotero.org/)
- `weeks/week02/lecture.md`、`weeks/week02/lab.md`
