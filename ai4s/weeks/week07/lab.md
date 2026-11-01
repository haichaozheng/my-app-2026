# Week 07 课堂实验

## 实验目标

用 dsh 开发规则驱动的 Mesa 基线模型，接入 Mesa-LLM 把 LLM 嵌入智能体决策，记录每一次 LLM 调用，对比两种实现的涌现结果并完成验证报告。

## 实验步骤

1. dsh 安装配置：`pip install deepseek-harness-sdk`（推荐路径，无需 Node.js）；隔离 dsh_home 与一次性工作区；记录版本号；配置 DeepSeek API key
2. dsh 热身：用它完成一个小任务（生成并运行脚本），打开 Trajectory 视图看懂每次模型请求与工具执行
3. 模块一：用 dsh 对话式开发自己研究问题的 Mesa 基线模型——定义智能体类型、状态与交互规则（显式 if-then 规则，不接 LLM）；DataCollector 采集指标，Solara 可视化
4. 基线审计：在 Trajectory 里回查开发过程（模型改了什么、为什么），对照检查有无 AI 引入的隐蔽错误；存档基线涌现结果
5. 模块二：用 Mesa-LLM 把 LLM 嵌入智能体决策环节（`ModuleLLM(llm_model="openai/deepseek-chat", api_base="https://api.deepseek.com/v1")`，与 dsh 共用 key）；先小规模试跑（少量智能体 × 少量步数，控制 token 成本）
6. LLM 调用留痕：记录每次调用的时间步、智能体状态、prompt、回复、行动
7. 对比验证：规则驱动 vs LLM 驱动的涌现结果对比；模型验证（假设合理性、参数敏感性）与稳健性检验
8. AI 系统评估：结果可信度、偏见检测、稳健性验证
9. 封装分析 Skill（定义输入/输出/边界）
10. 撰写验证报告，记录发现的问题与修正；附 dsh 使用记录（版本号 + Trajectory 摘要）

## 实验交付

- Mesa 基线模型代码（规则驱动）
- Mesa-LLM 仿真代码与结果
- LLM 调用日志（时间步、智能体状态、prompt、回复、行动）
- 验证报告（对比分析 + 模型验证 + 稳健性检验 + AI 系统评估三维度）
- 分析 Skill 代码
- dsh 使用记录（版本号 + Trajectory 留痕摘要）

## 卡住了

- 卡住 → 问 AI（附报错）→ 同学互助解答 → 举手教师
- dsh 装不上 → 优先检查 Python 版本与网络；Web UI 路线（需 Node.js）作备选
- LLM 仿真太贵/太慢 → 缩小规模（智能体数 × 步数），或先用规则决策混合少量 LLM 决策
- Mesa-LLM API 报错 → 检查锁定的版本号与文档是否一致（活跃开发期 API 可能变动）
