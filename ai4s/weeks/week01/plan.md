# Week 01 教学计划

## 本周主题

工具准备 — AI工作环境搭建（AI4S范式入门）

> Phase 1: Foundation 第1周。本周是整门课的起点：不是"装软件"，而是为 AI4S 科研全流程奠定工具基础，并建立"人判断、AI执行"的人机交互姿态。

## 学习目标

- 能用自己的话说明 AI4S 范式：AI 贯穿科研全流程，是"研究伙伴"而非工具箱
- 能配置好 AI 工作环境（opencode/cursor）、Python 环境、API key、文献管理工具
- 能写第一个 Prompt 驱动的小脚本（如调用 LLM API 总结一段文本），验证环境可用
- 能说明社科科研全流程的五个环节，并把 AI4S 工具栈映射到每个环节

## 教学步骤（3节课）

**第1节 · 范式定向与全流程映射（45 分钟）**

1. 开场（5 分钟）：点明学期终点——围绕个人科研项目构建 AI4S 工具栈并产出科研成果（论文 + 工具栈仓库）
2. AI4S 范式讲解（15 分钟）：AI4S 不是"用 AI 写代码"，而是用 AI 重构科研全流程；人机交互姿态（人判断、AI 执行）
3. 社科科研全流程映射（15 分钟）：文献→选题→设计→实施→写作五模块，对应 9 周课程安排
4. 个人科研项目启动（10 分钟）：每位博士生简述自己研究方向与初步痛点

**第2节 · 工具环境搭建（45 分钟）**

5. opencode/cursor 配置演示（15 分钟）：安装、登录、API key 配置、Python 解释器选择
6. Python 环境配置（10 分钟）：`.venv` 虚拟环境、核心依赖库安装
7. 文献管理工具安装（5 分钟）：Zotero 或同类工具
8. 第一个 Prompt 驱动脚本（15 分钟）：用 opencode/cursor 调用 LLM API 总结一段文本，验证环境可用

**第3节 · Prompt 初体验与下周铺垫（45 分钟）**

9. Prompt 三原则在实操中自然体验（15 分钟）：清晰性、上下文、约束
10. 个人脚本调试与互查（15 分钟）：每人跑通自己的脚本，组内互查
11. 下周铺垫（10 分钟）：文献检索是方法论（PRISMA 流程），不是"搜一下"；预告 W2 检索式与 API
12. 收束（5 分钟）：布置课后自学与作业

## 交付物

- **工具环境就绪**（评分锚点，对应 milestones §1.1）
  - opencode/cursor 可正常运行
  - Python 环境配置完成（解释器、虚拟环境、核心依赖库）
  - API key 配置完成（至少一个 LLM API 可用）
  - 文献管理工具安装完成
  - 至少一个 Prompt 驱动的小脚本
- 方法论锚定：体现 AI4S 范式理解、Prompt Engineering 初步应用、工具选择意识

## 课后自学

- Prompt Engineering 方法论：`knowledge/m1-3-prompt-engineering.md`
- AI4S 范式与方法论：`knowledge/m1-1-ai4s-paradigm.md`
- 社科科研全流程映射：`knowledge/m1-4-research-workflow-mapping.md`
- AI 辅助编程（opencode/cursor）：`knowledge/m1-2-ai-coding.md`

## 课后作业

用 opencode/cursor 完成一个 Prompt 驱动的小脚本（如调用 LLM API 总结一段文本），验证环境可用，为 W2 文献检索脚本做技术热身。提交脚本与运行截图。

## 参考资料

- 理念：Wang, H. et al. (2023). "Scientific discovery in the age of artificial intelligence." *Nature*, 620, 47-60
- 工具：[opencode 文档](https://opencode.ai/docs/)、[Cursor 文档](https://docs.cursor.com/)
- `weeks/week01/lecture.md`、`weeks/week01/lab.md`
