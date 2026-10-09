# 第 3 次课：Skill 与 Agent 开发

> **课时**：85 分钟  
> **目标**：理解 MCP 的概念及其作为 Skill 工具扩展的价值、掌握 MCP 配置方法、掌握 SKILL.md 编写方法与 AI 辅助开发流程、掌握金融数据分析 Skill 设计方法与错误处理、理解 Agent 概念与创建配置方法、理解 Skill + Agent + MCP 协同架构、能够构建端到端的金融分析工作流

---

## 💡 课前思考

**回顾第2次课的问题**：

> 我们已经会用 tushare skill 获取股票数据了——但它每次都要让 AI 写 Python 代码 → 运行 → 解析结果，链路长、容易出错。

**本节课的新思考**：

- **如果 AI 能直接"调用接口"，跳过写代码步骤，会不会更快？**
- **如何开发一个自己的 Skill？**
- **如何让多个 Skill 和工具协同完成复杂金融分析任务？**

**本次课目标**：

- 学习 MCP——让 AI 直接调用外部工具的协议
- 从"使用 Skill"过渡到"开发 Skill"
- 理解 Agent 概念，掌握 Skill + Agent + MCP 协同架构

---

## 一、MCP——Skill 的外部工具扩展（20 分钟）

> **设计思路**：不单独讲 MCP 架构细节，而是从"Skill 需要数据源"这个痛点切入，自然引出 MCP 作为 Skill 的工具补充。

### 1.1 从 Skill 的痛点出发（5 min）

**回顾第 2 节**：tushare Skill 让 AI 写 Python 代码调 API 获取数据。

**痛点分析**：

```
Skill 方式的数据获取链路：
用户输入 → AI 读 SKILL.md → 写 Python 代码 → 运行代码 → 解析结果

每一步都可能出错：
- Python 代码语法错误
- tushare 包版本不兼容
- 网络超时
- 返回数据格式不是预期的
```

**引出问题**：如果 AI 能直接"调用接口"，跳过写代码环节呢？

---

### 1.2 MCP 解决了什么问题（10 min）

**MCP（Model Context Protocol）**：一套协议，让 AI 直接调用外部工具，无需写中间代码。

**数据流对比**：

```
Skill 方式：AI 读 SKILL.md → 写 Python → 运行 → 解析结果
MCP 方式：  AI 直接调用 MCP 工具 → 返回结果
```

**两者本质**：

| 维度 | Skill | MCP |
|------|-------|-----|
| 本质 | 告诉 AI **"怎么做"**的说明书 | 给 AI **"直接用的工具"**的接口 |
| 交互方式 | AI 写代码 → 运行 → 解析 | AI 发送请求 → 直接返回结果 |
| 是否需要写代码 | 是（中间步骤） | 否（零代码） |
| 延迟 | 较高（代码执行开销） | 较低（直接调用） |
| 灵活性 | 高（可自定义逻辑） | 中（取决于 MCP 提供的接口） |

**选型原则**：

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| 纯数据获取（如获取日线行情） | MCP | 零代码低延迟 |
| 多步骤分析（如计算 MACD 后判断买卖信号） | Skill | 需要自定义逻辑 |
| 数据获取 + 复杂分析 | MCP + Skill | MCP 获取数据，Skill 指导分析 |

---

### 1.3 MCP 配置方法（5 min）

**配置位置**：项目级配置文件 `opencode.jsonc` 中的 `mcp` 字段

**两种 MCP 类型**：

| 类型 | `"type"` 值 | 说明 | 示例 |
|------|------------|------|------|
| 远程 URL 型 | `"remote"` | 通过 URL 直接连接远程服务 | tushare MCP |
| 本地命令型 | `"local"` | 通过本地命令启动服务 | Zotero MCP（stdio） |

**项目级 vs 全局级**：

| 配置级别 | 文件位置 | 作用范围 |
|---------|---------|---------|
| 项目级 | 项目根目录 `opencode.jsonc` | 仅当前项目生效 |
| 全局级 | `~/.config/opencode/opencode.jsonc` | 所有项目生效 |

**安全注意事项**：

- Token **不硬编码**在配置文件中，使用环境变量引用：
  ```jsonc
  "url": "https://api.tushare.pro/mcp/?token={env:TUSHARE_TOKEN}"
  ```
- 这样即使配置文件被提交到 Git，也不会泄露 Token

---

### 🎯 本次课案例一：配置 tushare MCP 获取金融数据

> 场景：在 opencode 中配置 tushare MCP，通过自然语言直接获取股票行情数据，体验零代码数据获取的便捷性。

**配置步骤**：

1. 在项目根目录创建或编辑 `opencode.jsonc`，在 `mcp` 字段中写入：
   ```jsonc
   {
       "mcp": {
           "tushareMcp": {
               "type": "remote",
               "url": "https://api.tushare.pro/mcp/?token={env:TUSHARE_TOKEN}"
           }
       }
   }
   ```

2. 重启 opencode 会话，AI 将自动发现 tushare MCP 工具

3. 输入自然语言指令："获取贵州茅台最近 30 天的日线数据"

4. 观察 AI 如何直接调用 tushare MCP 返回数据，无需编写 Python 代码

5. 对比第 2 节中通过 Skill + SDK 获取同一数据的方式，讨论两者差异

**教学目标**：让学生掌握项目级远程 MCP 的配置方法，直观感受 MCP 与 Skill 的数据获取差异。

---

## 二、Skill 开发实践（30 分钟）

> **设计思路**：在第 2 节"使用 Skill"的基础上，过渡到"开发 Skill"。用 AI 辅助开发降低门槛。

### 2.1 SKILL.md 编写方法（10 min）

**frontmatter 编写技巧**：

```yaml
---
name: stock-tech-analysis       # 简短、有意义，便于手动调用
description: 计算股票均线/MACD/RSI等技术指标并生成分析图表，适用于技术分析场景
---
```

**description 编写要点**：

- 准确描述**适用场景**（触发条件）
- 包含**关键动词**（计算、分析、生成）
- 包含**领域关键词**（均线、MACD、RSI、技术指标）

**内容结构**：

```
# Skill 标题

## 背景
- 说明数据来源和分析场景

## 步骤说明
- 每个步骤都是 AI 可执行的指令
- 数据获取步骤要标注 MCP / Skill 回退策略

## 示例
- 展示典型输入 → 输出

## 注意事项
- 错误处理要前置
- 列出常见边界条件
```

**关键原则**：

1. **指令要具体**：不要说"分析数据"，要说"计算 20 日均线、MACD（12,26,9 参数）、RSI（14 日）"
2. **步骤要可执行**：每个步骤 AI 都能用工具完成
3. **错误处理要前置**：在注意事项中提前说明可能的异常和处理方式

---

### 2.2 金融 Skill 设计方法（10 min）

**设计流程**：

```
场景分析 → 步骤拆解 → 指令编写 → 错误处理 → 测试验证
```

**步骤拆解示例——股票技术分析**：

| 步骤 | 操作 | 工具/方法 |
|------|------|----------|
| 1. 数据获取 | 获取日线行情数据 | **优先使用 tushare MCP**（零代码）；若不可用，回退至 tushare skill（写代码） |
| 2. 数据清洗 | 处理缺失值、停牌日 | bash 运行 Python |
| 3. 指标计算 | 计算均线/MACD/RSI | bash 运行 Python |
| 4. 可视化 | 绘制技术指标图表 | bash 运行 Python |
| 5. 输出结论 | 生成分析报告 | 直接输出文本 |

**金融数据常见错误处理**：

| 错误类型 | 检测方法 | 处理策略 |
|---------|---------|---------|
| 股票代码无效 | tushare 返回空数据 | 提示用户检查代码格式（如 600519.SH） |
| 停牌日数据缺失 | 交易日期不连续 | 用前值填充或标注停牌 |
| 数据为空 | DataFrame 为空 | 提示"该时间段无数据，请调整日期范围" |
| API 限频 | 返回错误码 | 等待后重试，或降低请求频率 |
| 数据不足计算指标 | 数据行数 < 计算周期 | 提示"数据不足，MACD 至少需要 35 个交易日" |

---

### 2.3 AI 辅助 Skill 开发（10 min）

**迭代优化流程**：

```
创建 → 测试 → 评估 → 改进 → 再测试
  ↑                          |
  └──────────────────────────┘
```

**使用 skill-creator 辅助创建**：

1. 在 opencode 中输入需求描述
2. skill-creator 自动生成 SKILL.md 框架
3. 根据金融场景补充细节指令和示例代码

**使用 skill-improver 检查质量**：

1. 评估 description 准确性——是否能正确触发
2. 评估内容组织——步骤是否清晰可执行
3. 评估边界条件——是否覆盖常见异常
4. 输出改进建议

**实践要点**：

- 创建后立即测试触发是否正常
- 用真实金融数据测试执行流程
- 根据执行结果迭代改进

---

### 🎯 本次课案例二：开发"股票技术分析 Skill"（含 MCP 调用）

> 场景：开发一个计算均线/MACD/RSI 的 Skill，其中数据获取环节可选用 tushare MCP（零代码）或 tushare skill（代码方式），展示 Skill 与 MCP 的协作。

**步骤**：

1. **使用 skill-creator 生成 SKILL.md 框架**
   - 输入："创建一个股票技术分析 Skill，能计算均线、MACD、RSI 指标并绘图"
   - 得到基本的 frontmatter 和步骤框架

2. **填充技术指标计算指令和示例代码**
   - 均线：pandas rolling 计算
   - MACD：EMA(12)、EMA(26)、DEA(9)
   - RSI：14 日相对强弱指标

3. **在数据获取步骤中标注双通道策略**
   ```
   ## 步骤 1：获取日线数据
   - 优先使用 tushare MCP 获取日线数据（零代码，低延迟）
   - 若 MCP 不可用，则使用 tushare skill（编写 Python 代码获取）
   ```

4. **使用 skill-improver 评估质量**
   - 检查触发准确性
   - 检查步骤完整性
   - 检查边界条件

5. **根据建议添加错误处理**
   - 停牌日数据缺失 → 前值填充
   - 数据不足计算 MACD → 需至少 35 个交易日
   - RSI 计算除零风险 → 添加保护逻辑

6. **测试验证**
   - 用贵州茅台数据测试完整流程
   - 验证图表输出正确

**教学目标**：让学生完整体验 Skill 开发流程，理解 Skill 与 MCP 协作的双通道数据获取策略。

---

## 三、Agent 与协同架构（35 分钟）

> **设计思路**：Agent 是"调度者"，编排 Skill 和 MCP 完成复杂任务。

### 3.1 Agent 基础概念（10 min）

**什么是 Agent**：能自主规划、调用工具、返回结果的智能体。

**主代理 vs 子代理**：

| 维度 | 主代理 | 子代理 |
|------|--------|--------|
| 交互方式 | 用户直接交互 | 由主代理委派调用 |
| 切换方式 | Tab 键循环切换 | 由主代理根据 description 自动选择 |
| 代表角色 | 默认助手（Build）、规划助手（Plan） | 专业助手（如数据采集、报告生成） |

**OpenCode 内置的两个主代理**：

| 代理 | 模式 | 定位 | 工具权限 |
|------|------|------|---------|
| **Build** | primary | 默认主代理，启用所有工具 | 全部开放 |
| **Plan** | primary | 受限主代理，专注分析和规划 | 文件编辑、bash 均设为 ask |

**Agent 与 Skill 的本质区别**：

| 维度 | Agent | Skill |
|------|-------|-------|
| 本质 | 独立的智能体，有自己的 prompt、工具、模型 | 指令模板，指导 AI 如何使用工具 |
| 能力 | 可自主规划、调用工具、委派子代理、返回结果 | 被动加载，提供步骤说明 |
| 是否独立运行 | 是，可作为主代理或子代理独立执行任务 | 否，必须由 Agent 加载后才能生效 |
| 配置内容 | prompt + tools + permission + model | SKILL.md（步骤 + 示例 + 注意事项） |
| 类比 | 有明确职责的"专员" | 给专员的"操作手册" |

**Agent 的生命周期**：

```
创建 → 配置 → 触发 → 执行 → 返回结果
```

---

### 3.2 Agent 创建与配置（5 min）

**两种配置方式**：

| 方式 | 文件位置 | 特点 |
|------|---------|------|
| Markdown（推荐） | `.opencode/agents/{name}.md` | 与 Skill 风格统一，版本管理友好 |
| JSON | `opencode.jsonc` 的 `agent` 字段 | 配置集中，适合简单代理 |

**Markdown 方式的字段说明**：

```markdown
---
description: 描述代理功能与使用场景（必填，决定子代理何时被自动调用）
mode: subagent          # primary（主代理）/ subagent（子代理）/ all（两者皆可）
tools:                  # 控制代理可用的工具
  bash: true
  read: true
  write: false
  edit: false
permission:             # 控制工具权限（可选）
  bash: allow
---
你是 [角色描述]。[具体指令]。
```

**关键字段**：

- `mode`：`primary` / `subagent` / `all`
- `model`：可选，不指定时主代理使用全局配置的模型
- `description`：**必填**，决定子代理何时被自动调用
- `tools`：控制可用工具
- `permission`：控制工具权限（ask / allow / deny）

**交互式创建**：

```bash
opencode agent create
```

按提示完成配置即可。

---

### 3.3 Skill + Agent + MCP 协同架构（10 min）

**三者关系**：

```
Agent（调度）：决定"做什么"、编排执行顺序
Skill（方法）：指导"怎么做"、提供步骤指令
MCP（工具）：提供"直接调用的接口"、获取外部数据
```

**三种设计模式**：

| 模式 | 结构 | 适用场景 |
|------|------|---------|
| Skill 驱动 | Agent 加载 Skill → 用内置工具执行 | 数据清洗、技术分析 |
| MCP 增强 | Agent 加载 Skill → 调 MCP 获取数据 → 分析 | 实时行情查询 |
| 全链路协同 | Agent 编排多个 Skill + 多个 MCP | 端到端金融分析报告 |

**金融分析端到端工作流示例**：

```
用户输入 → 日报Agent(主代理)
              ├── 委派 → 数据采集子代理
              │          ├── tushare MCP（零代码获取行情）
              │          └── tushare Skill（分析方法指导）
              │          └── 返回结构化数据
              └── 委派 → 报告生成子代理
                         └── 接收数据 → 输出日报文案
```

**设计原则**：

1. **单一职责**：每个 Agent 只做一件事
2. **松耦合**：Agent 之间通过数据传递而非直接调用
3. **渐进增强**：先用 Skill 驱动跑通流程，再加入 MCP 提升效率，最后实现全链路协同

---

### 🎯 本次课案例三：创建"金融数据合规检查代理"——两种配置方式实操

> 场景：创建一个子代理，检查股票数据中的异常（负价格、日期不连续、涨跌幅超限），输出结构化检查报告。通过此案例实操 Agent 的两种配置方式。

**方式一：Markdown 方式**（推荐）

在项目级目录 `.opencode/agents/data-auditor.md` 中创建：

```markdown
---
description: 检查股票数据中的异常值，输出结构化合规报告
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
---
你是金融数据合规检查专员。读取给定的股票 CSV 数据，检查以下三类异常：
1. 负价格：收盘价 < 0
2. 日期不连续：交易日之间存在缺漏
3. 涨跌幅超限：单日涨跌幅超过 ±10%

输出格式为 Markdown 表格，按异常类型分类列出。
若无异常，输出"数据合规，未发现异常"。
```

**方式二：JSON 方式**

在 `opencode.jsonc` 中配置等效代理：

```jsonc
{
  "agent": {
    "data-auditor": {
      "description": "检查股票数据中的异常值，输出结构化合规报告",
      "mode": "subagent",
      "prompt": "你是金融数据合规检查专员。读取给定的股票 CSV 数据，检查以下三类异常：1. 负价格 2. 日期不连续 3. 涨跌幅超限。输出 Markdown 表格。",
      "tools": { "bash": true, "read": true, "write": false, "edit": false }
    }
  }
}
```

**测试与对比**：

1. 分别用两种方式创建同一个代理，用第 1 节课获取的贵州茅台 CSV 数据测试
2. 观察两者行为是否一致
3. 讨论 Markdown 方式的优势：与 Skill 风格统一、版本管理友好、prompt 内容长时更清晰

**教学目标**：让学生掌握 Agent 的两种配置方式，亲手完成第一个代理的创建与测试。

---

### 🎯 本次课案例四：构建"股票日报自动生成系统"（主代理 + 子代理协同）

> 场景：创建一个日报主代理，它负责理解用户需求、编排任务，并将数据采集和报告撰写分别委派给两个子代理执行。

**角色分工**：

| 角色 | 模式 | 职责 | 依赖 |
|------|------|------|------|
| 日报Agent（主代理） | primary | 接收用户指令、拆分子任务、委派子代理、汇总结果 | — |
| 数据采集子代理 | subagent | 获取指数行情、板块涨跌等数据 | tushare MCP + tushare Skill |
| 报告生成子代理 | subagent | 对采集的数据进行解读，撰写结构化日报文案 | — |

**演示架构**：

```
用户输入 → 日报Agent(主代理)
              ├── 委派 → 数据采集子代理 → tushare MCP(获取数据) + tushare Skill(分析方法) → 返回数据
              └── 委派 → 报告生成子代理 ← 接收数据 → 输出日报文案
```

**演示步骤**：

1. 在 `.opencode/agents/data-collector.md` 中编写数据采集子代理：
   ```markdown
   ---
   description: 采集股票指数行情和板块涨跌数据
   mode: subagent
   tools:
     bash: true
   ---
   你是金融数据采集专员。使用 tushare MCP 获取数据，若不可用则使用 tushare skill。
   输出格式：JSON，包含指数名称、收盘价、涨跌幅。
   ```

2. 在 `.opencode/agents/report-writer.md` 中编写报告生成子代理：
   ```markdown
   ---
   description: 根据采集的金融数据撰写结构化日报
   mode: subagent
   tools:
     write: true
   ---
   你是金融分析师。根据提供的数据撰写 Markdown 格式日报，包含行情概览、板块分析、重点关注。
   ```

3. 在 `opencode.jsonc` 中配置日报主代理（或在 `.opencode/agents/daily-report.md` 中配置）：
   ```jsonc
   {
     "agent": {
       "daily-report": {
         "description": "生成股票市场日报，协调数据采集和报告撰写",
         "mode": "primary",
         "prompt": "你是日报主编。先委派 data-collector 采集数据，再委派 report-writer 撰写报告，最后汇总输出。"
       }
     }
   }
   ```

4. 测试运行：使用 Tab 键切换到日报主代理，输入"生成今日股市日报"，观察主代理如何逐步委派子代理并汇总结果

**教学目标**：让学生理解主智能体与子智能体的分工协作机制，以及 Skill、Agent、MCP 如何在多层调度中协同完成复杂金融分析任务。

---

## 四、本次课总结

**核心要点**：

1. **MCP 的价值**：让 AI 直接调用外部工具，实现零代码数据获取，弥补 Skill 需要写代码的短板
2. **选型原则**：纯数据获取优先 MCP，多步骤分析优先 Skill，复杂任务两者协同
3. **Skill 开发流程**：场景分析 → 步骤拆解 → 指令编写 → 错误处理 → AI 辅助迭代
4. **Agent 的角色**：调度者，编排 Skill 和 MCP 完成复杂任务的关键枢纽
5. **协同架构**：Skill 驱动、MCP 增强、全链路协同三种模式，根据任务复杂度选用

**三者协作全景**：

```
                     ┌─────────────────────────────┐
                     │        Agent（调度）          │
                     │  决定"做什么"、编排执行顺序    │
                     └──────┬──────────┬───────────┘
                            │          │
                  ┌─────────▼──┐  ┌───▼──────────┐
                  │  Skill（方法）│  │  MCP（工具）  │
                  │ 指导"怎么做"│  │ 提供"直接用  │
                  │ 提供步骤指令 │  │  的接口"     │
                  └────────────┘  └──────────────┘
```

---

## 参考资料

**官方文档**：
- OpenCode MCP 服务器文档：https://opencode.ai/docs/zh-cn/mcp-servers/
- OpenCode 代理文档：https://opencode.ai/docs/zh-cn/agents/
- MCP 协议规范：https://modelcontextprotocol.io

**Skill 开发工具**：
- Anthropic skill-creator：https://github.com/anthropics/skills/tree/main/skills/skill-creator
- Claude Scholar skill-improver：https://github.com/Galaxy-Dawn/claude-scholar/tree/main/skills/skill-improver
- gstack skillify：https://github.com/garrytan/gstack/tree/main/skillify

**文献管理工具**：
- Zotero：https://www.zotero.org/
- Zotero MCP 服务器：https://github.com/Galaxy-Dawn/zotero-mcp

---

*本次课结束，开始上机实验！*
