# Week 03 教学计划

## 本周主题

文献综述 — 文献管理 + AI 综述

> Phase 1: Foundation 第3周，阶段成果一。文献库整理是检索到综述的桥梁；第三方智能检索工具改变文献阅读范式——从"读完记住"到"检索即用"；综述是结构化综合而非摘抄堆砌。

## 学习目标

- 能用 Zotero 管理文献库：导入、去重、标签、规范化、纳入排除标准筛选
- 能说明 RAG 改变文献管理范式的原理（从概念层面理解，不要求从代码搭建）
- 能用第三方工具（Kimi / 智谱清言 / Coze / AMiner）进行文献智能检索与问答
- 能用 Prompt 驱动 LLM 生成有逻辑框架的文献综述
- 能说明综述写作规范：综述有逻辑框架（按主题/方法论/时间线组织），而非逐篇罗列
- 能设计并搭建文献综述写作 skill：拆解综述写作流程，在智能体平台上配置知识库与 Prompt 链

## 教学步骤（3节课）

**第1节 · 文献库整理与智能检索工具（45 分钟）**

1. 文献库整理与去重（15 分钟）：把 W2 的原始元数据导入 Zotero，去重、规范化、打标签
2. 纳入排除标准确认（10 分钟）：在 Zotero 中按时间范围、方法论类型等标准筛选文献
3. 第三方智能检索工具盘点（10 分钟）：Kimi（长上下文 PDF 问答）、智谱清言（文档解读）、Coze（知识库+智能体）、AMiner（学者图谱+文献发现）
4. 第三方工具实操演示（10 分钟）：把文献 PDF 上传到 Kimi/智谱清言，对话式提取关键观点、对比研究结论

**第2节 · 综述写作规范与RAG介绍（45 分钟）**

5. 综述写作规范（15 分钟）：逻辑框架（主题/方法论/时间线），而非逐篇罗列；好综述与差综述对比
6. RAG 改变文献管理范式（15 分钟）：从"读完记住"到"检索即用"——概念讲解与原理示意（检索→增强→生成）；RAG 与文献综述写作的关系
7. 本地 RAG 构建方案介绍（可选，10 分钟）：LangChain + FAISS + 智谱 embedding 方案概览；演示效果展示
8. 小结与过渡（5 分钟）：综述写作规范与 RAG 回顾；从理解 RAG 到构建综述写作 skill 的铺垫

**第3节 · 文献综述写作skill构建（45 分钟）**

9. 综述写作 skill 设计（10 分钟）：分析综述写作流程，拆解为可自动化的子任务（检索→筛选→提取→组织→生成），明确 skill 的输入输出与知识库配置
10. 个人文献智能检索实操（15 分钟）：每人用自己的文献库，用第三方工具提取综述所需的关键信息。💡 课堂互动：抽取 2-3 位同学投屏演示智能检索过程，全班交流检索策略与效果（3-4 分钟）
11. 综述写作 skill 搭建与测试（15 分钟）：在 Coze/智谱清言上搭建文献综述写作 skill，配置知识库、Prompt 链、输出模板；用自己的文献库测试生成综述初稿
12. 阶段收束（5 分钟）：Phase 1 完成，回顾文献智能模块；预告 Phase 2 选题

## 交付物

- **文献综述**（评分锚点，对应 milestones §1.3，阶段成果一 15%）
  - Zotero 文献库（去重、标签、规范化，至少 20 篇）
  - AI 辅助综述文稿（含逻辑框架）
  - 文献综述写作 skill（配置截图或链接）
- 方法论锚定：体现文献库整理逻辑、RAG 概念理解、智能检索工具使用、综述写作规范、Prompt 驱动的综述生成过程、skill 构建思路

## 课后自学

- RAG 原理与实践：`knowledge/m1-5-rag.md`
- 本地 RAG 构建方案（可选）：LangChain + FAISS + 智谱 embedding 完整案例代码（见 `weeks/week03/local-rag-guide.md`）
- AI 辅助文献综述：`knowledge/m1-7-ai-literature-review.md`
- 综述写作规范：`knowledge/m1-8-review-writing.md`
- 知识图谱与文献计量（推荐）：`knowledge/m1-9-knowledge-graph-bibliometrics.md`
- Skill 构建入门（推荐）：Coze/智谱清言智能体搭建教程（见 `weeks/week03/skill-building-guide.md`）

## 课后作业

整理 Zotero 文献库（去重、标签、规范化，至少 20 篇），用第三方工具进行智能检索，搭建文献综述写作 skill 并生成 AI 辅助综述初稿。提交 Zotero 文献库导出文件、综述文稿与 skill 配置截图或链接。

## 参考资料

- 理念：Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2020*
- 工具：[Zotero](https://www.zotero.org/)、[Kimi](https://kimi.moonshot.cn/)、[智谱清言](https://chatglm.cn/)、[Coze（扣子）](https://www.coze.cn/)、[AMiner](https://www.aminer.cn/)
- `weeks/week03/lecture.md`、`weeks/week03/lab.md`
