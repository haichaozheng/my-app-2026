# Week 06 教学计划

## 本周主题

研究实施（上）— 数据集（三路径）+ 实证（StatsPAI）

> Phase 3: Implementation 第1周。数据集构建是研究实施基石；数据来源有**三路径**——第三方数据集、自己采集实验、智能体辅助调研生成类人数据——各有适用场景、效度边界与伦理要求，**选择本身是方法论判断**（须与 W5 审计配置一致并在交付物中论证）；实证是经验检验，AI 辅助编程但方法论判断在人。本周引入 **Skill**（可复用科研 AI 能力封装——有了真实可复用的科研流程才值得封装），并接入 agent-native 计量库 **StatsPAI**。

## 学习目标

- 能说明数据来源三路径的适用场景、效度边界与伦理要求，并论证自己选择的路径（与 W5 研究设计的审计配置一致）
- 能完成数据获取与清洗、变量操作化（理论概念→可分析变量）
- 能用 StatsPAI 实施实证估计（回归/DID/IV/断点回归/合成控制/匹配/DML 等），说明模型选择理由、前提假设检验、结果解读逻辑
- 能导出出版级表格（`sp.regtable()` → Word/Excel/LaTeX），并说明估计器的 `validation_status`——哪个数字可信、凭什么可信，须可查证
- 能做数据验证（缺失值处理、异常值检测、编码一致性检查）
- 能说明 Skill 的基本概念（输入/输出/边界），把数据采集流程封装为可复用的数据 Skill（本周首次引入）
- 能说明"硅基样本（LLM-as-subject）"作为生成式数据源的适用边界与有效性校准逻辑（Argyle 2023）

## 教学步骤（3节课）

**第1节 · 数据来源三路径：选择即方法论（45 分钟）**

1. 数据集构建是研究实施基石（8 分钟）：变量操作化、编码、清洗
2. 三路径讲解（20 分钟）：

   | 路径 | 做法 | 关键要求 |
   |---|---|---|
   | 第三方数据集 | 公开数据库（如 CFPS/CGSS/CHFS 等）与文献配套数据 | 数据质量与适配性论证、变量操作化映射、引用与授权合规 |
   | 自己采集实验 | 实验、问卷、访谈等一手数据采集 | 变量操作化与测量信效度、样本设计、伦理审查 |
   | 智能体辅助生成类人数据 | 用 LLM 智能体模拟受访者（silicon sampling），辅助问卷预测试、情景预演、低成本先验估计 | 须与真实数据校准（算法保真度）、显式声明生成属性、不得替代需要真实人类被试的因果推断 |

   第三路径的方法论先例锚点：Argyle 2023（本周方法论阅读）——算法保真度、条件化、适用边界
3. 路径选择论证（7 分钟）：选择须与 W5 审计配置一致，在交付物中论证理由。💡 课堂互动：数据需求关键词写便签上白板/共享文档，同学互相推荐可获取的数据源（3 分钟）
4. 个人数据需求梳理（10 分钟）：每位博士生明确路径选择与获取计划

**第2节 · StatsPAI 实证工作台（45 分钟）**

5. StatsPAI 是什么（10 分钟）：Stanford REAP 团队开发、发表于 JOSS 的 Python 因果推断与计量库——把 Stata/R 常用工作流（`regress`/`ivregress`/`reghdfe`/`csdid`/`rdrobust`/`synth`/`psmatch2`/DML）原生带到 Python；统一 API + 结构化结果对象 + 出版级表格导出
6. agent-native 用法（10 分钟）：机器可读 schema（`sp.list_functions()`/`sp.describe_function()`）；自带 `statspai-mcp` 服务器，让 opencode 中的智能体直接调用估计器（detect→estimate→audit 循环）
7. 课堂锚定练习（15 分钟）：用自带经典数据集（Card 1995 / LaLonde-NSW / mpdta）跑通 1-2 个估计器，观察 `validation_status`（是否与 Stata/R 数值对齐）——呼应 W5 的可审计姿态
8. 与 W5 的衔接（10 分钟）：实证方法以研究设计中经审计确认的方法条目为准，用 StatsPAI 对应估计器实施

**第3节 · 数据验证 + Skill 引入与封装（45 分钟）**

9. Skill 引入（12 分钟）：可复用能力封装，输入/输出/边界——类比"写函数"但粒度更大、可被 AI 调用；opencode Skill 创建与调用；为什么现在才引入（W6 起有了真实可复用的科研流程）
10. 数据 Skill 封装实操（15 分钟）：每人把自己的数据采集流程封装为数据 Skill（输入：数据源与参数；输出：清洗后数据集；边界清晰）
11. 数据验证与实证结果检查（13 分钟）：缺失值、异常值、编码一致性；表格导出与 validation_status 检查
12. 收束（5 分钟）：预告 W7 仿真（Mesa 基线 + LLM 智能体，及第二个 harness：DeepSeek Harness）

## 交付物

- **数据集 + 实证结果 + 数据 Skill**（评分锚点，对应 milestones §3.1）
  - 数据集（已清洗、变量操作化、可分析，含**数据来源路径选择说明**——选择理由及与 W5 审计配置的一致性）
  - 实证结果（StatsPAI 代码与出版级表格，含 validation_status 说明）
  - 数据 Skill（可复用，输入/输出/边界清晰）
- 方法论锚定：体现三路径选择的方法论自觉、数据集构建合理性、StatsPAI 的可审计姿态（validation_status：哪个数字可信、凭什么可信）、数据验证、Skill 封装逻辑、硅基样本适用边界

## 课后自学

- 数据集构建方法论：`knowledge/m4-1-data-collection.md`
- AI 辅助编程深度应用：`knowledge/m4-2-ai-coding-advanced.md`
- Skill 封装数据采集能力：`knowledge/m4-3-skill-data-collection.md`
- Agent 数据采集（推荐）：`knowledge/m4-4-agent-data-collection.md`
- 大模型类人智能体数据采集（硅基样本，推荐）：`knowledge/m4-4b-llm-subject-data.md`
- LLM 辅助数据解读：`knowledge/m4-5-llm-data-interpretation.md`
- **方法论阅读（反思日志须回应）**：Argyle, L.P. et al. (2023). "Out of One, Many: Using Language Models to Simulate Human Samples." *Political Analysis*, 31(3), 337-351（锚点：算法保真度、条件化、适用边界——为"硅基样本"路径提供方法论自觉）

## 课后作业

完成数据集构建与清洗（说明数据来源路径及选择理由，与 W5 审计配置一致），用 StatsPAI 完成实证估计并导出出版级表格，封装数据采集 Skill。提交数据集、路径选择说明、StatsPAI 代码与表格、Skill 代码。

## 参考资料

- 理念：Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology*, 13(6), e1005510
- 理念：Argyle, L.P. et al. (2023). "Out of One, Many: Using Language Models to Simulate Human Samples." *Political Analysis*, 31(3), 337-351
- 工具：[StatsPAI](https://github.com/brycewang-stanford/statspai)、[opencode Skill 文档](https://opencode.ai/docs/)
- `weeks/week06/lecture.md`、`weeks/week06/lab.md`
