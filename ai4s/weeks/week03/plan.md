# Week 03 教学计划

## 本周主题

文献综述 — RAG 知识库 + AI 综述

> Phase 1: Foundation 第3周，阶段成果一。RAG 改变文献管理范式：从"读完记住"到"检索即用"；综述是结构化综合而非摘抄堆砌。

## 学习目标

- 能说明 RAG 改变文献管理范式的原理：从"读完记住"到"检索即用"
- 能构建个人文献 RAG 知识库（向量数据库、文档切分、检索策略）
- 能用 Prompt 驱动 LLM 生成有逻辑框架的文献综述
- 能说明综述写作规范：综述有逻辑框架（按主题/方法论/时间线组织），而非逐篇罗列

## 教学步骤（3节课）

**第1节 · RAG 原理与文献管理范式（45 分钟）**

1. RAG 改变文献管理范式（15 分钟）：从"读完记住"到"检索即用"
2. RAG 技术原理（15 分钟）：向量数据库、文档切分、嵌入、检索策略
3. 工具盘点（10 分钟）：LangChain、FAISS、Chroma
4. 个人知识库设计（5 分钟）：每位博士生规划自己的文献知识库结构

**第2节 · RAG 知识库构建实操（45 分钟）**

5. 文档切分与嵌入演示（15 分钟）：把 W2 的文献库导入向量数据库
6. 检索策略调优（15 分钟）：chunk size、overlap、top-k 参数调整
7. 个人知识库构建（15 分钟）：每人构建自己的 RAG 知识库（至少 20 篇文献）

**第3节 · AI 综述生成与阶段收束（45 分钟）**

8. Prompt 驱动综述生成（15 分钟）：用 Prompt 引导 LLM 生成有结构的综述
9. 综述写作规范（10 分钟）：逻辑框架（主题/方法论/时间线），而非逐篇罗列
10. 综述初稿撰写与互评（15 分钟）：每人生成 AI 辅助综述初稿，组内互评逻辑框架
11. 阶段收束（5 分钟）：Phase 1 完成，回顾文献智能模块；预告 Phase 2 选题

## 交付物

- **文献综述**（评分锚点，对应 milestones §1.3，阶段成果一 15%）
  - RAG 知识库代码 + 至少 20 篇文献的向量数据库
  - AI 辅助综述文稿（含逻辑框架）
- 方法论锚定：体现 RAG 设计与构建逻辑、综述写作规范、Prompt 驱动的综述生成过程

## 课后自学

- RAG 原理与实践：`knowledge/m1-5-rag.md`
- AI 辅助文献综述：`knowledge/m1-7-ai-literature-review.md`
- 综述写作规范：`knowledge/m1-8-review-writing.md`
- 知识图谱与文献计量（推荐）：`knowledge/m1-9-knowledge-graph.md`

## 课后作业

构建 RAG 知识库（至少 20 篇文献），生成 AI 辅助综述初稿。提交知识库代码与综述文稿。

## 参考资料

- 理念：Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2020*
- 工具：[LangChain 文档](https://python.langchain.com/docs/)、[FAISS 文档](https://faiss.ai/)
- `weeks/week03/lecture.md`、`weeks/week03/lab.md`
