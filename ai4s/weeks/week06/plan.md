# Week 06 教学计划

## 本周主题

研究实施（上）— 数据集 + 实证

> Phase 3: Implementation 第1周。数据集构建是研究实施基石（变量操作化、编码、清洗）；实证是经验检验，AI 辅助编程但方法论判断在人。本周引入 Skill 工具。

## 学习目标

- 能说明数据集构建方法的合理性：数据源选择、变量操作化、数据代表性
- 能用 AI 辅助编程（Python/R/Stata）深度处理数据获取与清洗
- 能进行实证估计（回归/DID/IV 等），并说明模型选择理由、前提假设检验、结果解读逻辑
- 能做数据验证（缺失值处理、异常值检测、编码一致性检查）
- 能把数据采集流程封装为可复用 Skill，说明封装逻辑（输入/输出/边界）

## 教学步骤（3节课）

**第1节 · 数据集构建方法论（45 分钟）**

1. 数据集构建是研究实施基石（10 分钟）：变量操作化、编码、清洗
2. 数据源选择（15 分钟）：API/爬虫/NLP 文本提取如何选择
3. 数据验证逻辑（10 分钟）：缺失值、异常值、编码一致性
4. 个人数据需求梳理（10 分钟）：每位博士生明确数据需求与获取路径

**第2节 · AI 辅助编程深度应用（45 分钟）**

5. AI 辅助编程深度演示（15 分钟）：用 LLM 深度辅助编写复杂数据处理代码
6. 数据获取与清洗实操（15 分钟）：调用 API / 爬虫 / 文本提取
7. 实证估计（15 分钟）：回归/DID/IV，模型选择与前提假设检验

**第3节 · Skill 封装与数据验证（45 分钟）**

8. Skill 封装演示（10 分钟）：把数据采集流程封装为可复用 Skill
9. 个人 Skill 封装实操（15 分钟）：每人封装自己的数据采集 Skill
10. 数据验证与实证结果检查（15 分钟）
11. 收束（5 分钟）：预告 W7 建模与仿真

## 交付物

- **数据集 + 实证结果 + 数据 Skill**（评分锚点，对应 milestones §3.1）
  - 完成的数据集（已清洗、变量操作化、可分析）
  - 实证估计结果（可运行的回归/检验代码与输出）
  - 封装的数据采集 Skill（可复用）
- 方法论锚定：体现数据集构建合理性、实证估计方法论自觉、AI 辅助编程深度应用、数据验证、Skill 封装逻辑

## 课后自学

- 数据集构建方法论：`knowledge/m4-1-data-collection.md`
- AI 辅助编程深度应用：`knowledge/m4-2-ai-coding-advanced.md`
- Skill 封装数据采集能力：`knowledge/m4-3-skill-data-collection.md`
- Agent 数据采集（推荐）：`knowledge/m4-4-agent-data-collection.md`
- 实证估计方法 AI 赋能：`knowledge/m4-5-empirical-estimation.md`

## 课后作业

完成数据集构建与清洗、实证估计代码，封装数据采集 Skill。提交数据集、实证代码与输出、Skill 代码。

## 参考资料

- 理念：Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology*, 13(6), e1005510
- 工具：[opencode Skill 文档](https://opencode.ai/docs/)
- `weeks/week06/lecture.md`、`weeks/week06/lab.md`
