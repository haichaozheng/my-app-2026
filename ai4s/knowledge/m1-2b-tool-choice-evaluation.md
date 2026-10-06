# 教学基础工具选择评估：opencode vs DeepSeek Harness

> **引入时机**：W1（工具选定）+ W7（dsh 理念演示） | **核心问题**："AI4S 课程的教学基础工具，选 opencode 还是 DeepSeek Harness？" | **层级**：Essential | **关联**：`m1-2-ai-coding.md` 的延伸决策记录

## 为什么需要这份评估

`m1-2-ai-coding.md` 并列介绍了 opencode（命令行 AI 助手）和 DeepSeek Harness（`dsh`，智能体运行框架），但未给出课程层面的选择结论。本文件记录课程设计者的选择决策与理由，供：

- **学生**：理解"为什么课程让我用 opencode 而不是 dsh"，以及"dsh 在哪一周出现、为什么"
- **助教/后续维护者**：在工具迭代时能复现当初的决策逻辑，避免无依据地更换底座

## 课程对基础工具的隐性要求

从教学方案与知识点文件中归纳出五条硬约束：

| # | 课程要求 | 来源 |
|---|---|---|
| A | 作为 AI 辅助编程底座，W1 即上手 | `x1-ai-coding-progression.md` |
| B | 作为 Skill/Agent 的运行与封装载体（W4-W6） | 教学方案五模块 |
| C | 支撑科研的**可复现/可验证/可审计** | `x1` 可重复性段、`m4-10-ai-evaluation.md` |
| D | 面向社科博士生（编程弱、9周密集、跨学科） | `ai4s-teaching-plan.md` |
| E | 教学材料与文档稳定可依 | PBL"在需求时刻引入知识"节奏 |

两者都声称覆盖 A/B/C，但实现路径与成熟度差异显著。

## opencode 评估

### 优势

1. **稳定性与文档成熟度高**。opencode 已是稳定发行版，有完整文档站（opencode.ai）、AGENTS.md 约定、skill 机制、subagent、plan mode、MCP 支持。`m1-2-ai-coding.md` 已将 opencode 列为日常工具，学生有现成路径。
2. **上手门槛低**。安装即用，终端内 `opencode` 一条命令启动；模型可自由切换（OpenAI/Anthropic/本地），不绑死厂商——对社科博士生（编程弱、时间紧）是决定性优势。
3. **Skill 机制天然对应课程"Skill"模块**。opencode 的 skill 是 Markdown 指令文件，社科博士生可直接用自然语言写"文献综述 skill""数据分析 skill"，无需写插件代码——完美匹配 W5-W6 的 Skill 封装教学目标。
4. **Plan/Subagent 已内置**。W4 的 Agent 概念、W3 的选题对话，可直接用 opencode 的 subagent + plan mode 演示，无需额外框架。
5. **与 Cursor/Trae 互补不冲突**。教学方案已写明"Cursor/Trae 做交互式开发、opencode 做项目级操作"，opencode 占住"项目级/命令行"生态位，分工清晰。

### 劣势

1. **可审计/可复现较弱**。opencode 有 session 记录，但没有 dsh 那种 Trajectory 轨迹——把每一次工具调用、思维链、上下文注入持久化为可分叉/回放的日志。`x1-ai-coding-progression.md` 明确把 Trajectory 能力归给 dsh，这正是 opencode 的短板。
2. **科研流程编排能力有限**。opencode 的 subagent 是会话级的，不是可固化为"科研流程"的 DAG/工作流。W6 的"Agent 编排分析流程"需学生自己用 Python 胶水代码拼接，opencode 不直接提供编排层。
3. **"一切皆插件"理念缺失**。opencode 的扩展点（skill/MCP）偏轻量，不像 dsh 那样把文件系统、终端、网页、子 Agent 全部插件化——对"构建个人 AI4S 工具栈"的深层次目标（把研究流程固化为可复用模块）支撑不足。

## DeepSeek Harness (dsh) 评估

### 优势

1. **Trajectory 轨迹 = 科研可审计性的天然底座**。`x1` 和 `m1-2` 都强调：仅追加日志记录模型所见、思维链、工具调用与结果、子 Agent 调度、上下文注入，支持恢复/分叉/回放。直接命中课程"可复现、可验证、可审计"核心要求，且比 opencode 保存脚本更进一层。
2. **"一切皆插件"契合 AI4S 工具栈理念**。dsh 基于 Cordis，把研究流程固化为可复用 Tool/Skill，模型路由支持 DeepSeek/OpenAI 兼容/自定义 Provider——对应课程"把研究流程固化为可复用 Tool/Skill"目标，且避免厂商锁定。
3. **进阶教学价值高**。对 W4 Agent、W5-6 Skill 封装、W7 AI 系统评估，dsh 的插件架构和 Trajectory 能提供比 opencode 更深的教学素材（学生能看到 Agent 的真实执行过程）。
4. **中文生态友好**。DeepSeek 出品，文档有中文版，模型对中文社科场景适配好——对社科博士生是加分项。

### 劣势（关键问题）

1. **⚠️ 开发者预览版，明确会有破坏性变更**。dsh README 原文："DeepSeek Harness is in *developer preview* and iterating rapidly. **THERE WILL BE COMPATIBILITY-BREAKING CHANGES.**" 这是决定性风险——9周课程中途 API/插件协议变，教学材料全部要返工。
2. **⚠️ 需要 Node.js + 插件概念基础**。`m1-2-ai-coding.md` 已注明"需 Node.js 环境与一定插件概念基础"。社科博士生普遍不具备，W1 上手成本高，与 PBL"在需求时刻引入"节奏冲突。
3. **文档与教学材料不足**。opencode 有成熟文档站和社区案例，dsh 文档站内容有限，教学材料需从零构建。9周密集课程没有试错空间。
4. **Skill 概念偏重代码**。dsh 的 Tool/Skill 是代码插件，社科博士生用自然语言封装 skill 的门槛高于 opencode 的 Markdown skill 文件。
5. **星标与社区虽大，但教学生态尚早**。作为教学工具的"可复现教学路径"尚未沉淀。

## 综合对比矩阵

| 维度 | opencode | dsh | 胜出 |
|---|---|---|---|
| W1 上手门槛 | 低（装即用） | 高（Node + 插件概念） | opencode |
| 稳定性（9周不返工） | 稳定 | 预览版，破坏性变更 | opencode |
| 文档与教学材料 | 成熟 | 不足 | opencode |
| Skill 封装（自然语言） | Markdown skill，低门槛 | 代码插件，高门槛 | opencode |
| Agent 概念教学 | subagent 内置 | 插件化 Agent，更彻底 | dsh（理论深度）|
| 可审计/Trajectory | session 记录，较弱 | Trajectory 强 | dsh |
| 流程编排 | 需自己拼 | 插件化编排 | dsh |
| 模型路由自由度 | 高 | 高 | 平 |
| 中文友好 | 一般 | 好（DeepSeek） | dsh |
| 跨学科适配（定量+定性） | 高（通用） | 中（偏工程） | opencode |
| "构建个人工具栈"理念契合 | 中 | 高（一切皆插件） | dsh（理念层）|

## 决策：分层定位，而非二选一

课程的核心矛盾是：**理念上 dsh 更契合 AI4S 工具栈愿景，但工程上 opencode 是9周课程唯一能稳定交付的底座**。采用分层定位：

| 层级 | 工具 | 角色 | 出现时机 |
|---|---|---|---|
| **基础层（全员必修）** | opencode + Cursor/Trae | AI辅助编程与 Skill 封装的实操底座 | W1 起贯穿全程 |
| **进阶层（演示+可选探索）** | dsh | Trajectory 可审计性、插件化 Agent 理念的**演示与理念锚点** | W7（AI系统评估） |

### 决策理由

1. **W1-W6 全员可用性优先**。社科博士生9周内要完成工具栈构建，opencode 的低门槛和稳定性能保证所有人"做出来"。dsh 的预览版风险会让 PBL 的"在需求时刻引入知识"变成"在需求时刻排环境坑"。
2. **W7 用 dsh 做"可审计理想"的演示**。`x1-ai-coding-progression.md` 已把 Trajectory 归给 dsh——在 W7"AI系统评估"环节，用 dsh 演示"可复现、可审计的 Agent 执行轨迹"，让学生看到 opencode 之外更彻底的科研审计形态，作为理念锚点而非作业工具。既不增加全员负担，又保留 dsh 的教学价值。
3. **保留升级路径**。等 dsh 进入稳定版（README 移除 developer preview 警告），可在下一学期把进阶层升级为必修层。`m1-2-ai-coding.md` 已并列列出两者，分层方案与之自洽。

## dsh 专题课位置：W7

### 候选周次对比

| 候选 | 周次主题 | dsh 切入点 | 是否合适 | 理由 |
|---|---|---|---|---|
| W4 | 研究设计 + Agent + 批判性思维 | 插件化 Agent 展示 | ❌ | 学生还在做研究设计，编程需求弱，新工具打断节奏 |
| W6 | 数据分析 + Skill与Agent编排 | 插件化 Agent 编排 | △ | 有契合点，但学生正赶分析进度，无余裕审视工具本身 |
| **W7** | 质量控制 + AI系统评估 | **Trajectory 可审计性** | ✅ | 最佳，见下文 |

### 为什么是 W7

**1. 主题天然咬合**。W7 的核心是"AI系统评估——结果可信度评估、偏见检测、稳健性验证"，而 dsh 的核心价值正是 Trajectory 轨迹：把 Agent 的每一次工具调用、思维链、上下文注入持久化为可恢复/分叉/回放的日志。这是"可审计性"理念的**理想形态**，比 opencode 的 session 记录更彻底。用 dsh 做 W7 的演示，能直接制造 PBL 的认知缺口：

> Challenge（"我的分析过程能被别人追溯吗？"）→ Gap（opencode 的 session 记录不够）→ Knowledge（dsh 的 Trajectory 理念）→ Apply（审视自己的工具栈是否可审计）

**2. 时机是收口而非引入**。W7 是 Phase 3 最后一周，学生已完成数据采集和分析，进入"迭代优化"阶段。此时引入 dsh 不是"再加一个要学的工具"，而是"用一个理想参照审视已有工具栈"——学生带着自己一周的分析成果来对比 dsh 的 Trajectory，反思"我的过程记录缺了什么"。这比在 W4/W6 引入新工具（会变成负担）更符合 PBL 节奏。

**3. 为 W8 整合留出选择空间**。W7 看到 dsh 的理念后，学生在 W8"工具栈整合"时可以自主决定：是否采纳 Trajectory 理念到自己的工具栈（即使不用 dsh 本身，也可以借鉴"记录每一步执行过程"的思路）。这呼应教学方案的"Student Voice & Choice"——工具栈围绕个人研究方向定制。

**4. 避免预览版风险传导**。dsh 是 developer preview，如果在 W1-W6 全员必修阶段引入，API 变更会波及所有学生作业。放到 W7 作为"演示+可选探索"，即使 dsh 有破坏性变更，影响范围可控——学生只是观摩理念，不依赖它交付作业。

### 不选 W6 的补充说明

W6 的"Agent 编排"确实是 dsh 插件化 Agent 的强项，但 W6 学生正处于"运行分析、AI辅助解读结果"的执行高峰，认知负荷已满。把 dsh 放这里会变成"又一个要学的工具"而非"一个启发性的参照"。**理念展示应在学生有余裕反思时进行，而非在赶进度时。**

## W7 dsh 专题课的内容建议

| 环节 | 内容 | 时长 |
|---|---|---|
| 演示 | 用 dsh 跑一个简化科研 Agent（如文献检索→摘要→综述生成），展示 Trajectory 轨迹视图 | 20min |
| 对比 | 同一任务用 opencode 跑，对比 session 记录与 Trajectory 的信息粒度差异 | 15min |
| 讨论 | "我的分析过程目前记录了什么？缺了什么？如果要审计我的研究，评审者能看到什么？" | 15min |
| 可选实践 | 有余力的学生尝试用 dsh 跑自己的一个分析步骤，导出 Trajectory 作为"过程可审计"证据 | 课外 |

### 评分关联

W7 交付物"评估报告"中增加一条可选项：
> （可选）若使用 dsh 或借鉴 Trajectory 理念记录分析过程，附 Trajectory 导出或过程日志，作为可审计性证据。此项为加分项，不作硬性要求。

## 后续行动项

- [ ] W7 lecture.md / lab.md 中加入 dsh 演示环节（待 weeks/ 目录建设时落实）
- [ ] 关注 dsh 版本状态：当 README 移除 "developer preview" 警告时，重新评估是否升级为必修层
- [ ] `m1-2-ai-coding.md` 中 dsh 段落保持"进阶/演示"定位，与本文档决策一致

## 参考链接

- https://opencode.ai — opencode 命令行 AI 编程助手
- https://deepseek-harness.github.io/deepseek-harness/ — DeepSeek Harness 文档
- https://github.com/deepseek-ai/deepseek-harness — DeepSeek Harness 源码仓库（注意 developer preview 警告）
