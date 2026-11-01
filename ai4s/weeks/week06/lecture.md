# Week 06 课堂串讲

> 本文件为课堂投影串讲稿，规格与兜底以 `plan.md` 为准。

## 第1节 · 数据来源三路径：选择即方法论

- 数据集构建是研究实施基石：变量操作化、编码、清洗
- 三路径：第三方数据集（CFPS/CGSS/CHFS）/ 自己采集实验 / 智能体辅助生成类人数据
- 第三路径边界：算法保真度校准、显式声明生成属性、不得替代真实被试的因果推断（Argyle 2023）
- 选择须与 W5 审计配置一致，交付物中论证
- 互动：数据需求便签互荐数据源

## 第2节 · StatsPAI 实证工作台

- StatsPAI 定位：Stata/R 工作流原生到 Python；统一 API + 结构化结果 + 出版级表格
- agent-native：`sp.list_functions()` / `sp.describe_function()` / `statspai-mcp`（detect→estimate→audit）
- 锚定练习：Card 1995 / LaLonde-NSW / mpdta；看 `validation_status`
- 与 W5 衔接：实证方法以经审计确认的方法条目为准——哪个数字可信、凭什么可信

## 第3节 · 数据验证 + Skill 引入与封装

- Skill 引入：可复用能力封装（输入/输出/边界）；为什么 W6 才引入
- 数据 Skill 封装实操
- 数据验证：缺失值、异常值、编码一致性
- 预告 W7：Mesa 基线 + LLM 智能体 + DeepSeek Harness
