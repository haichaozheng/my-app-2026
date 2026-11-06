# Week 08 教学计划

## 本周主题

论文写作（上）— LaTeX + AI Agent 协作写作

> Phase 4: Writing & Integration 第1周，阶段成果二。学术写作是结构化表达而非自然语言流；AI 辅助起草但人来把控论证逻辑。写作阶段最高风险的**"验证缺口"是引用**——Agent 生成的引用可能凭空捏造（幻觉引用），因此本周把"生成"与"核验"拆成**两个权限互斥的角色**：Generator 不拥有网络与核验权，Auditor 只核验不下结论，引用核验结论必须可回溯到 Zotero/DOI；AI 使用声明对照 W1-W7 审计记录逐项起草，把全程人机协作痕迹制度化。本周完成五模块工具栈整合。

## 学习目标

- 能说明学术写作规范：论文结构（引言→理论→方法→结果→讨论）、引用规范、论证逻辑
- 能运行写作-审计双 Agent 工作流（学生担任编排与裁决人）：Writing Generator 按章节起草，Citation & Reproducibility Auditor 逐条核验
- 能说明双 Agent 的**权限纪律（生成与核验分离）**：Generator 不拥有网络与核验权、不生成"引用核验通过"的结论；Auditor 只标记核验状态与完整性缺口、不判断"复现成功"
- 能用 LaTeX + AI 进行论文排版（texai 类工作流：直接编辑 .tex，每一处修改在 PDF 上可见）
- 能用 Zotero MCP 管理引用，产出**引用核验报告**（逐条 DOI/元数据核验状态，可回溯到 Zotero/DOI）
- 能起草 **AI 使用声明**（逐项对照 W1-W7 审计记录）与复现包完整性清单
- 能把五模块工具栈整合为可串联的 AI4S 工作流（工具栈 v1），说明各模块间的数据流和逻辑衔接
- 能说明论文论证链路（问题→理论→假设→方法→数据→结果→结论）如何贯穿全文

## 教学步骤（3节课）

**第1节 · 学术写作规范与验证缺口（45 分钟）**

1. 学术写作是结构化表达（10 分钟）：不是自然语言流
2. 论文结构讲解（15 分钟）：引言→理论→方法→结果→讨论，每部分功能与写作逻辑
3. 论证链路（10 分钟）：问题→理论→假设→方法→数据→结果→结论如何贯穿全文。💡 课堂互动：抽取 2-3 位同学投屏自己的论文论证链路图，全班一起找断裂点（缺失环节或逻辑跳跃）
4. 验证缺口：引用（10 分钟）：当场演示 Agent 编造引用（幻觉引用）——为什么写作阶段必须把"生成"与"核验"拆成权限互斥的两个角色

**第2节 · 写作-审计双 Agent 工作流（45 分钟）**

5. 架构讲解（15 分钟）（基于 [opencode agents](https://opencode.ai/v2/docs/agents/) 的 primary/subagent 模式，学生担任 primary 编排与最终裁决）：

   | 角色 | 模式 | 职责 | 关键权限纪律 |
   |---|---|---|---|
   | Writing Generator | subagent | 按章节生成 LaTeX 草稿、润色段落、生成表格、插入 Zotero 引用；在 texai 类工作流中直接编辑 .tex | 不拥有 shell/网络权限（优先使用 texai 的受限模式）；不生成"引用核验通过"的结论 |
   | Citation & Reproducibility Auditor | subagent | 逐条核验 Agent 插入引用的 DOI/元数据；检查复现包完整性；起草 AI 使用声明草稿并对照 W1—W7 审计记录 | 可调 Zotero MCP/学术搜索 MCP 做核验；只标记核验状态和完整性缺口，不判断"复现成功" |

6. texai 类工作流演示（10 分钟）：直接编辑 .tex、每一处修改在 PDF 上可见；Generator 的受限模式
7. Zotero MCP 引用管理（10 分钟）：插入引用、元数据来源可回溯
8. 个人双 Agent 写作实操（10 分钟）：Generator 按章节起草 → Auditor 逐条核验引用 DOI/元数据 → 学生对引用去留做人工裁决

**第3节 · AI 使用声明与五模块整合（45 分钟）**

9. AI 使用声明起草（15 分钟）：逐项对照 W1-W7 审计记录（W1 环境与脚本、W4 人工裁决记录、W5 修订历史、W6 数据路径论证、W7 LLM 调用日志与 dsh Trajectory……），把全程人机协作痕迹制度化
10. 五模块整合为 AI4S 工作流（15 分钟）：各模块间数据流和逻辑衔接；工具栈 v1 整合
11. 案例与经验总结（10 分钟）：关键决策、踩坑经验、方法论心得
12. 收束（5 分钟）：预告 W9——论文评审 skill 模拟评审 + 同侪互评 + 修订展示；课后交换初稿供 W9 同侪互评

## 交付物

- **论文初稿 + 引用核验报告 + AI4S 工具栈 v1**（评分锚点，对应 milestones §4.1，阶段成果二 15%）
  - 论文初稿（LaTeX+PDF，AI 修改可见）
  - **引用核验报告**（逐条 DOI/元数据核验状态）
  - 复现包完整性清单
  - AI 使用声明草稿（对照 W1-W7 审计记录逐项起草）
  - AI4S 工具栈 v1（五模块可串联运行）+ 案例与经验总结
  - 阶段反思日志（阶段成果二组成部分，模板见 `templates/reflection-log.md`，须回应本周方法论阅读：罗家德等（2026）第6章"验证理论的范式"）
- 方法论锚定：体现学术写作规范、生成与核验分离的权限纪律、引用核验可回溯（Zotero/DOI）、AI 使用声明的诚实性（对照审计记录）、五模块整合为工作流、论文论证逻辑、案例经验的方法论提炼

## 课后自学

- 学术写作规范：`knowledge/m5-1-academic-writing.md`
- LLM 辅助学术写作：`knowledge/m5-2-llm-academic-writing.md`
- 论文结构与论证逻辑：`knowledge/m5-3-paper-structure.md`
- LaTeX + AI（推荐）：`knowledge/m5-4-latex-ai.md`
- Skill 封装写作能力（推荐）：`knowledge/m5-5-skill-writing.md`
- 五模块整合为 AI4S 工作流：`knowledge/m5-6-ai4s-workflow-integration.md`
- **方法论阅读（反思日志须回应）**：罗家德等（2026）第6章"验证理论的范式"（验证性研究的方法论，呼应实证收尾与论文写作）

## 课后作业

用双 Agent 工作流完成论文初稿：Generator 起草各章节，Auditor 核验全部 Agent 插入的引用并产出引用核验报告与复现包完整性清单，学生裁决引用去留并定稿 AI 使用声明，整合 AI4S 工具栈 v1 与案例经验总结、阶段反思日志。课后与同侪交换初稿（W9 同侪互评用）。

## 参考资料

- 理念：Booth, W.C., Colomb, G.G. & Williams, J.M. (2008). *The Craft of Research*. University of Chicago Press
- 工具：[LaTeX 文档](https://www.latex-project.org/)、[Overleaf 文档](https://www.overleaf.com/learn)、[Zotero MCP](https://github.com/54yyyu/zotero-mcp)、[opencode Agents 文档](https://opencode.ai/v2/docs/agents/)
- `weeks/week08/lecture.md`、`weeks/week08/lab.md`
