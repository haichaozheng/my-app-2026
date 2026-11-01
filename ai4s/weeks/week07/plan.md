# Week 07 教学计划

## 本周主题

研究实施（下）— 仿真（DeepSeek Harness + Mesa + LLM 智能体）

> Phase 3: Implementation 第2周。仿真是用模型做反事实实验：先跑通规则驱动的基线模型，再把 LLM 嵌入决策环节，从"if-then 规则智能体"走向"语言推理智能体"；每一次 LLM 调用都须记录，可审计性是科研诚信底线。本周同时引入第二个编程智能体 harness——DeepSeek Harness（dsh），与 opencode 形成双 harness 对比；质量控制（AI 系统评估）嵌入各步验证。本周不单独教经济学建模，理论抽象体现在模型的规则与交互设计中。

## 学习目标

- 能说明仿真是用模型做反事实实验：先规则驱动基线、后 LLM 智能体，观察智能体行为与涌现结果有何不同
- 能安装配置 dsh（推荐 Python SDK 路径，无需 Node.js），并说明双 harness 对比的意义：harness 是**可替换的类别而非单一产品**（dsh 的 model-agnostic 与"一切皆插件"）
- 能用 dsh 作为 AI 辅助编程工具开发规则驱动的 Mesa 基线模型，理解 Model/Agent/AgentSet/DataCollector 基本盘
- 能用 dsh 的 **Trajectory 视图**逐步检视开发过程中的模型响应、工具调用、token 用量与耗时——"每一次 LLM 调用可审计"的现成教具
- 能用 Mesa-LLM 把 LLM 嵌入智能体的**决策环节**（推荐 DeepSeek API 为默认后端），并对每次 LLM 调用留痕（时间步、智能体状态、prompt、回复、行动）
- 能对比规则驱动与 LLM 驱动两种实现的涌现结果，做模型验证与稳健性检验
- 能做 AI 系统评估三维度：结果可信度评估、偏见检测、稳健性验证
- 能把分析流程封装为可复用 Skill

## 教学步骤（3节课）

**第1节 · 仿真方法论与 dsh 上手（45 分钟）**

1. "Why Model?" 与仿真方法论（15 分钟）：Epstein 的建模哲学；仿真是反事实实验；两模块路线总览——先规则基线后 LLM 接入；本周不单独教经济学建模，理论抽象体现在模型的规则与交互设计中
2. 双 harness 对比：引入 dsh（15 分钟）：安装配置（推荐 `pip install deepseek-harness-sdk`，自带运行时；或 `npx @deepseek-ai/dsh web` 启动 Web UI）；核心主张"一切皆插件"（模型、工具、界面、agent loop 都是可热替换的插件）、model-agnostic；与 opencode 对比——harness 是可替换的类别；Trajectory 视图预览；纪律：developer preview，锁版本 + 一次性工作区
3. dsh 首个任务体验（10 分钟）：每人用 dsh 完成一个小任务（如生成并运行一段脚本），学会看 Trajectory 里的每次模型请求与工具执行
4. 个人模型框架梳理（5 分钟）：按研究问题定义智能体类型、状态与交互规则

**第2节 · 模块一：Mesa 基线模型（dsh 开发）（45 分钟）**

5. Mesa 核心组件讲解（10 分钟）：Mesa 3 的 Agent/Model/AgentSet 调度、空间网格、DataCollector 采集指标、Solara 浏览器可视化
6. dsh 开发 Mesa 基线演示（15 分钟）：教师用 dsh 对话式开发一个规则驱动基线（如 Schelling 隔离模型），全程用 Trajectory 检视——模型每步说了什么、改了哪些文件、token 花在哪里
7. 个人基线模型开发实操（15 分钟）：每人用 dsh 开发自己研究问题的规则驱动基线模型。💡 课堂互动：抽取 2-3 位同学投屏基线涌现结果，全班挑战"如果…会怎样"的反事实场景，看模型能否应对（3-4 分钟）
8. 基线结果记录（5 分钟）：DataCollector 指标与 Solara 可视化存档，作为模块二的对照

**第3节 · 模块二：Mesa-LLM 接入 + 质量控制（45 分钟）**

9. Mesa-LLM 接入（15 分钟）：把 LLM 嵌入智能体决策与智能体间通信（支持 OpenAI/Anthropic/Gemini/Ollama 等 provider，课程推荐 DeepSeek API 为默认后端，与 dsh 共用同一 API key）；替换或混合规则决策与 LLM 决策
10. LLM 调用留痕（10 分钟）：对每次 LLM 调用记录时间步、智能体状态、prompt、回复、行动；调用日志与仿真数据一并交付——可审计性是科研诚信底线，与 dsh Trajectory 互相印证
11. 对比验证与 AI 系统评估（15 分钟）：对比规则驱动与 LLM 驱动的涌现结果；模型验证（假设合理性、参数敏感性）与稳健性检验；AI 系统评估三维度：结果可信度、偏见检测、稳健性验证；验证报告与"做对"自觉
12. 收束（5 分钟）：Phase 3 完成，预告 Phase 4 论文写作（W8 写作-审计双 Agent）

## 交付物

- **研究实施结果**（评分锚点，对应 milestones §3.2）
  - Mesa 基线模型（规则驱动，含 DataCollector 指标与 Solara 可视化）
  - Mesa-LLM 仿真结果（LLM 嵌入决策环节的实现）
  - LLM 调用日志（每次调用的时间步、智能体状态、prompt、回复、行动）
  - 验证报告（规则 vs LLM 涌现结果对比 + 模型验证 + 稳健性检验 + AI 系统评估三维度）
  - 封装的分析 Skill
  - dsh 使用记录（版本号 + Trajectory 留痕摘要：turns、steps、模型时间、工具时间、token 用量）
- 方法论锚定：体现仿真作为反事实实验的方法论自觉、规则基线先行的研究设计、每次 LLM 调用可审计的意识、双 harness 对比（harness 是类别而非产品）、质量控制嵌入验证、AI 系统评估三维度、"做对"比"做出来"重要的自觉

## 课后自学

- DeepSeek Harness 使用指南：`knowledge/m4-13-deepseek-harness.md`
- Skill 封装分析能力：`knowledge/m4-8-skill-analysis.md`
- Agent 分析工作流（推荐）：`knowledge/m4-9-agent-analysis-workflow.md`
- AI 系统评估方法：`knowledge/m4-10-ai-evaluation.md`
- 稳健性检验：`knowledge/m4-11-robustness-check.md`
- 效度验证与替代方案：`knowledge/m4-12-validity.md`
- **方法论阅读（反思日志须回应）**：Lazer, D. et al. (2020). "Computational social science: Obstacles and opportunities." *Science*, 369(6507), 1060-1062（锚点：数据质量、伦理、可复现性——范式十年反思）

## 课后作业

用 dsh 完成 Mesa 基线模型开发（附 dsh 版本号与 Trajectory 留痕摘要），完成 Mesa-LLM 接入实现，提交 LLM 调用日志与规则 vs LLM 对比分析、验证报告，封装分析 Skill。版本纪律：Mesa-LLM 与 dsh 均安装后锁定版本号并在报告中记录（本身即是可复现性训练的一环）。

## 参考资料

- 理念：Epstein, J.M. (2008). "Why Model?" *Journal of Artificial Societies and Social Simulation*, 11(4)
- 工具：[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)、[dsh 文档](https://deepseek-harness.github.io/deepseek-harness/)
- 工具：[Mesa 文档](https://mesa.readthedocs.io/latest/)、[Mesa-LLM](https://github.com/mesa/mesa-llm)、[Mesa-LLM 文档](https://mesa-llm.readthedocs.io/)
- `weeks/week07/lecture.md`、`weeks/week07/lab.md`
