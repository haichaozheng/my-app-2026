# Week 07 课堂串讲

> 本文件为课堂投影串讲稿，规格与兜底以 `plan.md` 为准。

## 第1节 · 仿真方法论与 dsh 上手

- "Why Model?"：仿真是反事实实验
- 两模块路线：先规则基线，后 LLM 智能体
- 本周不单独教经济学建模：理论抽象体现在规则与交互设计中
- 双 harness 对比：dsh 安装配置（Python SDK 路径）、"一切皆插件"、model-agnostic
- harness 是可替换的类别而非单一产品
- dsh 首个任务 + Trajectory 视图：每次模型请求与工具执行可见
- 纪律：developer preview，锁版本、一次性工作区

## 第2节 · 模块一：Mesa 基线模型（dsh 开发）

- Mesa 3 核心组件：Agent/Model/AgentSet、空间网格、DataCollector、Solara 可视化
- dsh 对话式开发演示（Schelling 隔离模型），Trajectory 检视开发过程
- 个人基线模型实操：按研究问题定义智能体、状态、交互规则
- 互动：投屏涌现结果，全班挑战"如果…会怎样"
- 基线结果存档，作为模块二对照

## 第3节 · 模块二：Mesa-LLM 接入 + 质量控制

- Mesa-LLM 接入：LLM 嵌入智能体决策与通信（DeepSeek API 默认后端）
- 替换或混合规则决策与 LLM 决策
- LLM 调用留痕：时间步、智能体状态、prompt、回复、行动
- 对比验证：规则 vs LLM 涌现结果
- AI 系统评估三维度：可信度、偏见、稳健性
- Phase 3 收束，预告 W8 写作-审计双 Agent
