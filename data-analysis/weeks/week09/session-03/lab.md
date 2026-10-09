# 第 3 次课上机实验：Skill 与 Agent 开发

> **实验时长**：75 分钟  
> **实验目标**：配置 MCP 服务、开发金融数据分析 Skill、创建自定义 Agent、体验 Skill + Agent + MCP 协同工作流

---

## 实验环境准备（5 分钟）

### 前置条件检查

**验证清单**：


| 检查项          | 验证命令                 | 预期结果        | 备注          |
| ------------ | -------------------- | ----------- | ----------- |
| opencode 已安装 | `opencode --version` | 显示版本号       | 如未安装，参考第1次课 |
| Python 已安装   | `python --version`   | Python 3.7+ | 必需          |


---

### 实验目录设置

```powershell
# 1. 进入项目目录
cd C:\haichao\build\finance-ai-coding

# 2. 创建本次实验的工作目录
mkdir teaching-materials\session-03\lab-work -Force

# 3. 进入实验目录
cd teaching-materials\session-03\lab-work

# 4. 启动 opencode
opencode
```

**验证**：

- opencode TUI 界面成功启动

---

## 实验一：MCP 配置练习（10 分钟）

### 1.1 配置 tushare MCP 到项目级 opencode.jsonc

**实验目的**：掌握项目级远程 MCP 的配置方法，理解 MCP 如何让 AI 零代码获取数据

**基础概念**：

- MCP（Model Context Protocol）是一套协议，让 AI 能直接调用外部工具，无需编写中间代码
- 远程型 MCP（`type: "remote"`）通过 URL 连接服务，不需要本地安装
- 项目级配置放在项目根目录的 `opencode.jsonc` 中，仅对当前项目生效
- Token 直接写在 MCP URL 中，opencode 会自动连接

**操作步骤**：

**步骤 1**：在 opencode TUI 中输入以下指令：

```
请在当前目录创建 opencode.jsonc 文件，内容如下：

{
    "mcp": {
        "tushareMcp": {
            "type": "remote",
            "url": "https://api.tushare.pro/mcp/?token=5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521"
        }
    }
}
```

**步骤 2**：观察 AI 的操作：

- AI 使用 write 工具创建 opencode.jsonc 文件
- 确认 write 操作（输入 `y`）

**步骤 3**：验证文件创建成功：

```powershell
# 退出 opencode 或另开终端
cat opencode.jsonc
```

**预期输出**：

```jsonc
{
    "mcp": {
        "tushareMcp": {
            "type": "remote",
            "url": "https://api.tushare.pro/mcp/?token=5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521"
        }
    }
}
```

**步骤 4**：重启 opencode 让 MCP 配置生效：

```powershell
# 重新启动
opencode
```

**步骤 5**：测试 MCP 功能——输入自然语言指令：

```
获取贵州茅台（600519.SH）最近 10 个交易日的日线数据
```

**步骤 6**：观察 AI 行为：

- AI 发现 tushare MCP 工具可用
- AI 直接调用 MCP 工具，不再编写 Python 代码
- 数据直接返回，无需运行脚本

---

### 1.2 对比 MCP 与 Skill 的数据获取方式

**实验目的**：直观感受 MCP 和 Skill 两种数据获取方式的差异

**基础概念**：

- Skill 方式：AI 读 SKILL.md → 写 Python 代码 → 运行 → 解析结果（链路长，易出错）
- MCP 方式：AI 直接调用 MCP 工具 → 返回结果（零代码，低延迟）
- 选型原则：纯数据获取用 MCP，多步骤分析用 Skill

**对比记录**：


| 对比维度           | Skill + SDK 方式 | MCP 方式    |
| -------------- | -------------- | --------- |
| 操作步骤数          | （记录实际步骤数）      | （记录实际步骤数） |
| 是否编写 Python 代码 |                |           |
| 响应速度（主观感受）     |                |           |
| 出错可能性          |                |           |
| 适用场景           |                |           |


**✅ 检查点**：

- tushare MCP 配置成功并能获取数据
- 理解 MCP 和 Skill 数据获取的差异

---

## 实验二：Skill 开发练习（30 分钟）

### 2.0 准备：安装 skill-creator 和 skill-improver 技能

**实验目的**：安装后续实验所需的 Skill 开发辅助工具，确保 skill-creator 和 skill-improver 可用

**基础概念**：

- **skill-creator**：Anthropic 提供的 Skill 创建辅助工具，可根据需求描述自动生成 SKILL.md 框架，包含 frontmatter、步骤大纲、示例占位符，大幅降低 Skill 开发门槛
- **skill-improver**：Skill 质量改进工具，读取改进计划文件（`improvement-plan-{name}.md`）并自动合并执行改进建议，支持按优先级分组处理冲突
- 这两个 Skill 由老师分享，学生只需将其复制到项目的 `.opencode/skills/` 目录即可安装，opencode 在启动时会自动加载该目录下的所有 Skill

**操作步骤**：

**步骤 1**：确认老师在课堂上分享：

- `skill-creator`
- `skill-improver`

**步骤 2**：将 Skill 文件复制到项目的 `.opencode/skills/` 目录。在 **PowerShell** 中执行（可以手动创建和拷贝）：

```powershell
# 进入项目根目录
cd C:\haichao\build\finance-ai-coding

# 创建目标目录（如已存在则跳过）
mkdir .opencode\skills\skill-creator -Force
mkdir .opencode\skills\skill-improver -Force

# 复制文件（将 <老师分享路径> 替换为实际路径）
Copy-Item <老师分享路径>\skill-creator\SKILL.md .opencode\skills\skill-creator\SKILL.md
Copy-Item <老师分享路径>\skill-improver\SKILL.md .opencode\skills\skill-improver\SKILL.md
```

**步骤 3**：验证安装是否成功：

```powershell
# 检查文件是否存在
ls .opencode\skills\skill-creator\SKILL.md
ls .opencode\skills\skill-improver\SKILL.md
```

**预期输出**：两个文件均存在，路径分别为：

- `.opencode/skills/skill-creator/SKILL.md`
- `.opencode/skills/skill-improver/SKILL.md`

**步骤 4**：重启 opencode 以加载新 Skill：

```powershell
opencode
```

**步骤 5**：在 opencode TUI 中验证 Skill 可触发——输入以下测试指令：

```
请使用 skill-creator 帮我创建一个简单的 Skill
```

观察 AI 是否加载了 skill-creator Skill（日志中会显示相关提示），然后回复"暂不创建"即可退出。

**✅ 检查点**：

- skill-creator 的 SKILL.md 已复制到 `.opencode/skills/skill-creator/`
- skill-improver 的 SKILL.md 已复制到 `.opencode/skills/skill-improver/`
- 重启 opencode 后 skill-creator 可正常触发

---

### 2.1 使用 skill-creator 创建技术分析 Skill 框架

**实验目的**：学习使用 AI 辅助工具快速生成 SKILL.md 框架，降低 Skill 开发门槛

**基础概念**：

- skill-creator 是 Anthropic 提供的 Skill 开发辅助工具，能根据需求描述自动生成 SKILL.md 的基本结构
- 生成的框架包含 frontmatter、步骤大纲、示例占位符，开发者只需补充具体细节
- 这种"AI 辅助开发"模式是高效构建 Skill 的推荐路径

**操作步骤**：

**步骤 1**：在 opencode TUI 中输入需求描述：

```
请使用 skill-creator 创建一个"股票技术分析 Skill"，功能要求如下：
- 名称：stock-tech-analysis
- 描述：计算股票均线/MACD/RSI等技术指标并生成分析图表，适用于技术分析场景
- 数据获取：优先使用 tushare MCP 获取日K线数据；若 MCP 不可用，则回退至 tushare skill
- 支持计算的指标：5日/10日/20日均线、MACD(12,26,9)、RSI(14)
- 输出：生成包含价格走势和指标的图表（PNG格式）
```

**步骤 2**：观察 skill-creator 的工作过程：

- AI 加载 skill-creator Skill
- AI 根据需求生成 SKILL.md 框架
- 框架包含 frontmatter、步骤大纲、示例占位符

**步骤 3**：确认 write 操作，将 SKILL.md 保存到 `.opencode/skills/stock-tech-analysis/SKILL.md`

**步骤 4**：检查生成的框架内容：

```
请读取 .opencode/skills/stock-tech-analysis/SKILL.md 的内容
```

**步骤 5**：记录框架的结构要素：

- frontmatter 中 name 和 description 是什么？
- 步骤有几个？每步的概述是什么？
- 示例和注意事项是否完整？

**✅ 检查点**：

- skill-creator 成功触发
- SKILL.md 框架已生成

---

### 2.2 填充技术指标计算指令和示例代码

**实验目的**：在生成的框架基础上补充具体的指令细节，使 Skill 具备完整的可执行性

**基础概念**：

- SKILL.md 的步骤指令需要足够具体，AI 才能据此编写正确的代码
- 金融技术指标的计算有标准公式和参数，需要明确写出
- 示例代码可以帮助 AI 理解预期的代码风格和输出格式

**操作步骤**：

**步骤 1**：在 opencode TUI 中输入补充指令：

```
请编辑 .opencode/skills/stock-tech-analysis/SKILL.md，补充以下内容：

1. 在"步骤 3：指标计算"中，添加具体的计算指令：
   - 均线：使用 pandas 的 rolling(window).mean() 方法
   - MACD：使用 EMA 计算，参数为 fast=12, slow=26, signal=9
   - RSI：使用 14 日周期，公式为 RSI = 100 - 100/(1+RS)，RS = 平均涨幅/平均跌幅

2. 在"示例"部分，添加示例输入和预期输出：
   - 输入："分析贵州茅台（600519.SH）最近 60 天的技术指标"
   - 预期输出：包含价格、均线、MACD 三列子图的分析图片

3. 在"注意事项"中，添加以下错误处理：
   - 数据不足：MACD 至少需要 35 个交易日数据，RSI 至少需要 15 个交易日
   - 停牌日：检测交易日期是否连续，如有断层用前值填充
   - 除零风险：RSI 计算时平均跌幅可能为 0，需添加保护逻辑
```

**步骤 2**：观察 AI 的编辑过程：

- AI 使用 edit 工具修改 SKILL.md
- 确认 edit 操作

**步骤 3**：验证修改后的内容：

```
请读取修改后的 SKILL.md，展示完整内容
```

**步骤 4**：检查关键要素是否完整：

- [ ] frontmatter 中 name 和 description 正确
- [ ] 数据获取步骤标注了 MCP 优先、Skill 回退
- [ ] 均线/MACD/RSI 的计算指令具体清晰
- [ ] 示例输入输出完整
- [ ] 错误处理覆盖数据不足、停牌、除零三种情况

**✅ 检查点**：

- SKILL.md 内容充实、步骤具体可执行
- 错误处理已覆盖至少 3 种金融数据异常

---

### 2.3 测试 Skill 的触发和执行

**实验目的**：验证自定义 Skill 的自动触发机制和执行流程是否正确

**基础概念**：

- Skill 的自动触发依赖于 description 字段与用户输入的语义匹配
- 测试时应使用描述中包含的关键词触发，也测试不相关关键词触发作为对照
- 执行流程应按照 SKILL.md 中的步骤依次进行

**操作步骤**：

**步骤 1**：重启 opencode 以加载新 Skill：

```powershell
opencode
```

**步骤 2**：测试自动触发——输入包含技术分析关键词的指令：

```
分析平安银行（000001.SZ）最近 60 天的技术指标，计算均线、MACD 和 RSI
```

**步骤 3**：观察触发行为：

- Skill 是否自动触发？（观察 AI 是否加载了 SKILL.md）
- AI 是否按照步骤执行：获取数据 → 清洗 → 计算指标 → 绘图？

**步骤 4**：验证输出文件：

```powershell
ls *.png *.csv *.py
# 应看到技术分析图表文件
```

**步骤 5**：测试对照——输入不相关的指令：

```
读取 swufe_news.csv 文件，统计新闻数量
```

**步骤 6**：确认 Skill 没有被错误触发（这是预期行为）

**步骤 7**：记录测试结果：


| 测试场景     | 输入关键词        | Skill 是否触发 | 执行是否正确 |
| -------- | ------------ | ---------- | ------ |
| 技术分析（正向） | 技术指标、均线、MACD |            |        |
| 数据查询（对照） | 新闻、统计        |            |        |


**✅ 检查点**：

- 技术分析 Skill 在正确场景下自动触发
- 执行流程按步骤进行并生成预期输出
- 不相关场景下 Skill 未被错误触发

---

### 2.4 使用 skill-improver 评估质量并改进

**实验目的**：学习使用 skill-improver 对 Skill 进行质量评估，并根据建议迭代改进

**基础概念**：

- skill-improver 是质量检查工具，从 description 准确性、内容组织、边界条件三个维度评估 Skill
- 它输出的改进建议可以直接指导 SKILL.md 的修改
- 迭代优化流程：创建 → 测试 → 评估 → 改进 → 再测试

**操作步骤**：

**步骤 1**：在 opencode TUI 中输入评估请求：

```
请使用 skill-improver 评估 .opencode/skills/stock-tech-analysis/SKILL.md 的质量，给出改进建议
```

**步骤 2**：观察评估输出，记录三项评估结果和改进建议：


| 评估维度            | 评分/评价 | 改进建议 |
| --------------- | ----- | ---- |
| description 准确性 |       |      |
| 内容组织            |       |      |
| 边界条件            |       |      |


**步骤 3**：选取至少 2 条改进建议，让 AI 执行修改：

```
请根据 skill-improver 的建议，改进 SKILL.md：
1. [选择建议 1]
2. [选择建议 2]
```

**步骤 4**：确认 edit 操作

**步骤 5**：重新测试 Skill 触发和执行，验证改进效果

**预期结果**：

- skill-improver 输出了评估结果和至少 3 条改进建议
- 根据建议修改后 Skill 运行效果有所提升

**✅ 检查点**：

- skill-improver 成功运行并输出评估结果
- 根据至少 2 条建议完成了改进
- 改进后 Skill 功能正常

---

## 实验三：Agent 创建练习（20 分钟）

### 3.1 使用 Markdown 方式创建数据合规检查子代理

**实验目的**：掌握使用 Markdown 方式创建子代理，理解 frontmatter 各字段的含义和作用

**基础概念**：

- Agent 是独立的智能体，有自己的 prompt、工具权限和运行模式
- 子代理（`mode: subagent`）由主代理委派调用，自动匹配基于 description 字段
- tools 字段控制代理可以使用的工具，限制工具可以缩小代理的行为范围，使其更专注
- Markdown 方式与 Skill 风格统一，便于版本管理，推荐优先使用

**操作步骤**：

**步骤 1**：在 opencode TUI 中输入创建指令：

```
请在 .opencode/agents/ 目录下创建 data-auditor.md 文件，内容如下：

---
description: 检查股票数据中的异常值，输出结构化合规报告
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
---

你是金融数据合规检查专员。读取给定的股票 CSV 数据，检查以下两类异常：
1. 负价格：收盘价 < 0
2. 涨跌幅超限：单日涨跌幅超过 ±10%

输出格式为 Markdown 表格，按异常类型分类列出。
若无异常，输出"数据合规，未发现异常"。
```

**步骤 2**：确认 write 操作

**步骤 3**：验证文件创建：

```
请读取 .opencode/agents/data-auditor.md 的内容
```

**步骤 4**：分析 frontmatter 各字段的作用：


| 字段          | 值   | 作用  |
| ----------- | --- | --- |
| description |     |     |
| mode        |     |     |
| tools.bash  |     |     |
| tools.write |     |     |


**✅ 检查点**：

- data-auditor.md 已创建在正确位置
- frontmatter 各字段设置合理

---

### 3.2 测试代理功能

**实验目的**：验证子代理能否正确执行数据合规检查任务

**基础概念**：

- 子代理由主代理根据 description 自动委派，也可在对话中手动请求
- 子代理只能使用 tools 中允许的工具（如本例中只有 bash 和 read）
- 代理的 prompt 定义了它的行为逻辑和输出格式要求

**操作步骤**：

**步骤 1**：确保有测试数据——如果要使用贵州茅台的 CSV 数据，先获取：

```
获取贵州茅台（600519.SH）最近 60 天的日线数据并保存为 moutai_daily.csv
```

**步骤 2**：触发数据合规检查代理：

```
请检查 moutai_daily.csv 的数据合规性，委派 data-auditor 代理执行
```

**步骤 3**：观察代理行为：

- 主代理是否识别到数据合规检查需求？
- 是否委派了 data-auditor 子代理？
- 子代理是否按照 prompt 中的三类异常进行检查？
- 输出格式是否为 Markdown 表格？

**步骤 4**：记录检查结果：


| 异常类型  | 是否发现异常 | 详情  |
| ----- | ------ | --- |
| 负价格   |        |     |
| 涨跌幅超限 |        |     |


**✅ 检查点**：

- data-auditor 代理成功触发并执行
- 输出格式符合预期（Markdown 表格或"数据合规"）

---

### 3.3 修改 tools 配置，对比行为差异

**实验目的**：理解 tools 配置对代理行为范围的影响

**基础概念**：

- tools 字段限制了代理可以使用的工具
- 设置 `write: false` 意味着代理不能创建或覆盖文件
- 设置 `edit: false` 意味着代理不能修改已有文件
- 合理限制工具范围可以让代理更专注于核心任务，避免误操作

**操作步骤**：

**步骤 1**：修改 data-auditor.md，将 tools 中 bash 和 write 都设为 true：

```
请编辑 .opencode/agents/data-auditor.md，将 frontmatter 中的 tools 修改为：
tools:
  bash: true
  read: true
  write: true
  edit: false
```

**步骤 2**：确认 edit 操作

**步骤 3**：重启 opencode 并重新测试：

```
请检查 moutai_daily.csv 的数据合规性，委派 data-auditor 代理执行，同时将合规报告保存为 audit_report.md
```

**步骤 4**：观察行为差异：

- 之前配置（write: false）：代理能否保存报告文件？
- 修改后配置（write: true）：代理能否保存报告文件？

**步骤 5**：记录对比结果：


| 配置  | write 权限 | 能否保存审计报告 |
| --- | -------- | -------- |
| 修改前 | false    |          |
| 修改后 | true     |          |


**✅ 检查点**：

- 理解 tools 配置如何影响代理行为
- 修改配置后代理行为确实发生变化

---

## 实验四：构建"股票日报自动生成系统"——主代理 + 子代理协同（15 分钟）

> 对应 lecture.md 案例四。本实验将创建一个完整的日报系统：一个主代理负责理解和编排任务，两个子代理分别负责数据采集和报告生成。

### 4.1 创建数据采集子代理

**实验目的**：创建专门负责金融数据采集的子代理，理解子代理的设计思路和工具配置

**基础概念**：

- 子代理（`mode: subagent`）由主代理根据 description 自动委派调用
- 数据采集代理的核心任务是通过 MCP 或 Skill 获取结构化金融数据
- 给予 `bash: true` 权限，使其可在 MCP 不可用时回退到 tushare Skill 编写 Python 代码获取数据
- 不给予 `write: true` 和 `edit: true`，避免采集过程中意外修改项目文件

**操作步骤**：

**步骤 1**：了解要创建的文件。以下为 `.opencode/agents/data-collector.md` 的完整内容，请先阅读理解：

```markdown
---
description: 采集股票指数行情和板块涨跌数据
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
---

你是金融数据采集专员。收到采集任务后，按以下流程执行：

1. 明确数据需求：用户需要哪些指数、板块或个股的数据？时间范围是什么？
2. 优先使用 tushare MCP 直接获取数据（零代码、低延迟）
3. 如果 MCP 不可用或未配置，使用 tushare skill（编写 Python 代码调用 SDK）
4. 对获取的数据做基本校验：数据是否为空、日期是否合理、字段是否完整

输出格式为 JSON，结构如下：

```json
{
  "indices": [
    {"name": "上证指数", "code": "000001.SH", "close": 3200.5, "pct_chg": 0.5},
    {"name": "深证成指", "code": "399001.SZ", "close": 10500.3, "pct_chg": -0.3}
  ],
  "sectors": [
    {"name": "银行", "pct_chg": 1.2},
    {"name": "房地产", "pct_chg": -0.8}
  ],
  "data_source": "tushare_mcp",
  "collect_time": "2026-06-12 15:30:00"
}
```

注意：
- 如果用户未指定具体指数，默认采集上证指数和深证成指
- 数据时间范围未指定时，默认取最近 1 个交易日
- 始终标注数据来源（mcp 或 skill）和采集时间
```

**步骤 2**：在 opencode TUI 中输入以下指令创建文件（将步骤 1 中的完整内容粘贴到方括号位置）：

```
请在 .opencode/agents/ 目录下创建 data-collector.md，内容如下：

[粘贴步骤 1 中的完整文件内容]
```

**步骤 3**：确认 write 操作（输入 `y`）

**步骤 4**：验证文件创建成功：

```
请读取 .opencode/agents/data-collector.md 的内容，确认文件已正确创建
```

**步骤 5**：分析该代理的设计要点，填写以下表格：


| 设计要点                      | 你的理解 |
| ------------------------- | ---- |
| 为什么 tools 中 bash 设为 true？ |      |
| 为什么 write 设为 false？       |      |
| 为什么定义了 JSON 输出格式？         |      |
| 为什么要标注数据来源和采集时间？          |      |


**✅ 检查点**：

- data-collector.md 已创建在 `.opencode/agents/` 目录下
- frontmatter 中 mode 为 subagent，tools 配置合理
- prompt 中包含双通道策略（MCP 优先、Skill 回退）

---

### 4.2 创建报告生成子代理

**实验目的**：创建专门负责撰写日报的子代理，理解"数据采集"与"报告生成"职责分离的设计思路

**基础概念**：

- 报告生成代理只负责将结构化数据转化为可读文案，不负责数据采集
- 给予 `write: true` 权限，使其可以将生成的日报保存为文件
- 不给予 `bash: true`，使其专注于文本撰写而非代码执行——职责越单一，输出越稳定
- 日报格式统一为 Markdown，便于阅读和版本管理

**操作步骤**：

**步骤 1**：了解要创建的文件。以下为 `.opencode/agents/report-writer.md` 的完整内容，请先阅读理解：

```markdown
---
description: 根据采集的金融数据撰写结构化日报
mode: subagent
tools:
  bash: false
  read: true
  write: true
  edit: false
---

你是金融分析师，专注于根据数据撰写市场日报。

收到数据后，按以下结构撰写 Markdown 格式日报：

# 股市日报 - {日期}

## 行情概览
- 用 2-3 句话概括当日市场整体表现
- 列出主要指数收盘价和涨跌幅

## 板块分析
- 涨幅前 3 板块及简要原因分析
- 跌幅前 3 板块及简要原因分析

## 重点关注
- 提示 1-2 个值得关注的信号或事件
- 给出简短的操作建议（仅供参考）

## 免责声明
- 声明本报告仅为数据分析结果，不构成投资建议

格式要求：
- 使用二级标题（##）分隔各节
- 数据用列表形式呈现
- 总字数控制在 500 字以内
- 结论段落不超过 100 字

将生成的日报保存为文件，命名为 daily_report_{日期}.md
```

**步骤 2**：在 opencode TUI 中输入以下指令创建文件（将步骤 1 中的完整内容粘贴到方括号位置）：

```
请在 .opencode/agents/ 目录下创建 report-writer.md，内容如下：

[粘贴步骤 1 中的完整文件内容]
```

**步骤 3**：确认 write 操作

**步骤 4**：验证文件创建成功：

```
请读取 .opencode/agents/report-writer.md 的内容，确认文件已正确创建
```

**步骤 5**：对比两个子代理的设计差异：


| 对比维度     | data-collector | report-writer |
| -------- | -------------- | ------------- |
| 核心职责     |                |               |
| bash 权限  |                |               |
| write 权限 |                |               |
| 输出格式     |                |               |
| 为什么权限不同？ |                |               |


**✅ 检查点**：

- report-writer.md 已创建在 `.opencode/agents/` 目录下
- frontmatter 中 mode 为 subagent，tools 配置与 data-collector 互补
- prompt 中包含完整的日报结构模板

---

### 4.3 配置日报主代理

**实验目的**：创建日报主代理，理解主代理的角色——负责理解用户需求、拆分子任务、委派子代理、汇总结果

**基础概念**：

- 主代理（`mode: primary`）是用户直接交互的入口，可通过 Tab 键切换选择
- 主代理的 prompt 要明确描述任务分解和委派逻辑，否则 AI 可能自己直接做而非委派
- 主代理需要知道有哪些子代理可用，以及何时委派给哪个子代理
- 本实验使用 Markdown 配置主代理；也可选用 JSON 方式在 `opencode.jsonc` 中配置

**操作步骤**：

**步骤 1**：了解要创建的文件。以下为 `.opencode/agents/daily-report.md` 的完整内容，请先阅读理解：

```markdown
---
description: 生成股票市场日报，协调数据采集和报告撰写
mode: primary
---

你是日报主编，负责协调生成市场日报。

收到用户的日报请求后，按以下步骤执行：

**第 1 步：理解需求**
- 用户想要哪天的日报？如果未指定，默认为最近的交易日
- 是否需要特定板块或个股的数据？

**第 2 步：委派数据采集**
- 将数据需求整理后，委派给 data-collector 子代理
- 明确告知需要采集的指数、板块和时间范围
- 等待 data-collector 返回 JSON 格式的数据

**第 3 步：委派报告撰写**
- 将 data-collector 返回的数据传递给 report-writer 子代理
- 明确告知日报日期
- 等待 report-writer 生成 Markdown 格式的日报

**第 4 步：汇总输出**
- 检查报告内容是否完整（包含行情概览、板块分析、重点关注、免责声明）
- 如有缺失，补充完善
- 向用户展示最终日报内容

注意事项：
- 不要自己采集数据或撰写报告，必须委派给对应的子代理
- 如果子代理执行失败，尝试用更简单的需求重新委派
- 最终输出应包含日报全文和保存路径
```

**步骤 2**：在 opencode TUI 中输入以下指令创建文件（将步骤 1 中的完整内容粘贴到方括号位置）：

```
请在 .opencode/agents/ 目录下创建 daily-report.md，内容如下：

[粘贴步骤 1 中的完整文件内容]
```

**步骤 3**：确认 write 操作

**步骤 4**：验证文件创建成功：

```
请读取 .opencode/agents/daily-report.md 的内容，确认文件已正确创建
```

**步骤 5**：确认三个代理文件都已就绪。退出 opencode 或另开终端执行：

```powershell
ls .opencode\agents\
```

应看到：`data-collector.md`、`data-auditor.md`、`report-writer.md`、`daily-report.md`

**✅ 检查点**：

- daily-report.md 已创建在 `.opencode/agents/` 目录下
- frontmatter 中 mode 为 primary，表示可作为主代理切换使用
- prompt 中明确描述了四步工作流程和数据委派逻辑

---

### 4.4 测试完整的日报生成流程

**实验目的**：验证主代理 + 子代理协同机制，体验从数据采集到报告生成的端到端流程

**基础概念**：

- 主代理切换方式：在 opencode TUI 中按 **Tab** 键循环切换可用的主代理
- 主代理会根据 description 自动识别何时委派子代理
- 完整数据流：用户 → 日报主代理 → data-collector（获取数据）→ report-writer（生成报告）→ 日报主代理 → 用户

**操作步骤**：

**步骤 1**：重启 opencode 以加载所有新建的代理：

```powershell
opencode
```

**步骤 2**：按 **Tab** 键切换到日报主代理，直到底部状态栏显示 `daily-report`（日报主编）

**步骤 3**：输入日报请求：

```
生成今日股市日报
```

**步骤 4**：观察完整的协同执行流程，依次记录各阶段行为：


| 执行阶段                 | 观察到的行为                            | 是否符合预期 |
| -------------------- | --------------------------------- | ------ |
| 1. 主代理理解需求           | 主代理是否识别需要采集数据和撰写报告？               |        |
| 2. 委派 data-collector | 是否将采集任务委派给了 data-collector？       |        |
| 3. data-collector 执行 | 使用了 MCP 还是 Skill 获取数据？返回了 JSON 吗？ |        |
| 4. 委派 report-writer  | 是否将数据和撰写任务委派给了 report-writer？     |        |
| 5. report-writer 执行  | 是否生成了 Markdown 格式的日报？保存了文件吗？      |        |
| 6. 主代理汇总             | 最终输出是否完整展示日报内容？                   |        |


**步骤 5**：验证生成的日报文件：

```
请读取刚才生成的日报文件内容
```

**步骤 6**：检查日报内容是否包含以下必要部分：

- 标题（含日期）
- 行情概览
- 板块分析
- 重点关注
- 免责声明

**步骤 7**：尝试自定义需求，再次生成：

```
生成今日股市日报，重点关注银行和科技板块，不要房地产板块
```

**步骤 8**：观察主代理是否能正确传递定制需求给子代理：


| 定制需求        | 是否传递给了对应子代理 | 子代理是否响应了定制需求 |
| ----------- | ----------- | ------------ |
| 重点关注银行和科技板块 |             |              |
| 不要房地产板块     |             |              |


**预期结果**：

- 按 Tab 键可切换到 daily-report 主代理
- 主代理按流程依次委派 data-collector 和 report-writer
- 最终生成包含完整结构的 Markdown 日报文件

**✅ 检查点**：

- 成功切换到日报主代理
- 主代理正确委派子代理，未自己直接采集数据或撰写报告
- 日报文件生成且内容完整

---

## 实验总结与验证（5 分钟）

### 验证清单


| 实验内容                                 | 完成状态 | 验证结果 |
| ------------------------------------ | ---- | ---- |
| 配置 tushare MCP 到 opencode.jsonc      | ✅/❌  |      |
| 通过 MCP 获取股票数据                        | ✅/❌  |      |
| 对比 MCP 与 Skill 方式获取数据                | ✅/❌  |      |
| 安装 skill-creator 和 skill-improver 技能 | ✅/❌  |      |
| 使用 skill-creator 创建 Skill 框架         | ✅/❌  |      |
| 充实 Skill 内容（指令 + 示例 + 错误处理）          | ✅/❌  |      |
| 测试 Skill 触发和执行                       | ✅/❌  |      |
| 使用 skill-improver 评估并改进              | ✅/❌  |      |
| 使用 Markdown 方式创建子代理                  | ✅/❌  |      |
| 测试代理功能                               | ✅/❌  |      |
| 修改 tools 配置对比行为差异                    | ✅/❌  |      |
| 创建 data-collector 子代理                | ✅/❌  |      |
| 创建 report-writer 子代理                 | ✅/❌  |      |
| 配置 daily-report 主代理                  | ✅/❌  |      |
| 测试完整的日报生成流程                          | ✅/❌  |      |


---

### 实验成果展示

退出 opencode 或另开终端，查看生成的文件：

```powershell
ls
ls .opencode\agents\
ls .opencode\skills\stock-tech-analysis\
```

应包含的文件：


| 文件                                              | 说明           |
| ----------------------------------------------- | ------------ |
| `opencode.jsonc`                                | MCP 配置文件     |
| `.opencode/skills/skill-creator/SKILL.md`       | Skill 创建辅助工具 |
| `.opencode/skills/skill-improver/SKILL.md`      | Skill 改进辅助工具 |
| `.opencode/skills/stock-tech-analysis/SKILL.md` | 技术分析 Skill   |
| `.opencode/agents/data-auditor.md`              | 数据合规检查代理     |
| `.opencode/agents/data-collector.md`            | 数据采集子代理      |
| `.opencode/agents/report-writer.md`             | 报告生成子代理      |
| `.opencode/agents/daily-report.md`              | 日报主代理        |
| `moutai_daily.csv`                              | 茅台日线数据（如果生成） |
| `*.png`                                         | 技术分析图表（如果生成） |
| `audit_report.md`                               | 合规报告（如果生成）   |
| `daily_report_*.md`                             | 日报文件（如果生成）   |


---

### 实验反思

1. **MCP vs Skill**：
  - MCP 的零代码数据获取体验如何？什么场景下更优？
  - Skill 方式的代码执行有什么 MCP 不具备的优势？
2. **Skill 开发流程**：
  - skill-creator 生成的框架质量如何？需要多少手动补充？
  - skill-improver 的建议是否切实有用？
3. **Agent 的价值**：
  - 子代理相比在主代理中直接描述任务，有什么优势？
  - tools 权限控制对代理行为有何影响？
4. **协同架构**：
  - 主代理 + 子代理的分工协作体验如何？主代理是否正确委派而非自己直接做？
  - data-collector 和 report-writer 的权限差异设计是否合理？
  - 遇到了哪些困难？如何解决？

---

## 实验常见问题

**Q1: MCP 配置后 AI 仍然写 Python 代码获取数据？**

原因可能：opencode 未重启、配置文件格式有误、MCP 连接失败。解决方法：

1. 确认已重启 opencode 会话
2. 检查 `cat opencode.jsonc` 确保格式正确
3. 在指令中明确指定："使用 tushare MCP 获取数据，不要写 Python 代码"

**Q2: skill-creator 没有触发？**

原因可能：skill-creator 未安装、description 匹配失败。解决方法：

1. 确认 skill-creator 已安装：`ls .opencode\skills\skill-creator\SKILL.md`
2. 使用明确的指令："请使用 skill-creator 创建一个..."
3. 手动加载：在指令中提及"skill-creator"

**Q3: 自定义 Agent 没有被自动调用？**

原因可能：description 过于宽泛或过窄、mode 设置不对。解决方法：

1. 检查 description 是否准确描述了触发场景
2. 确认 mode 设为 `subagent`
3. 在主代理对话中明确请求委派："委派 data-auditor 代理执行数据检查"

**Q4: 技术指标计算报错数据不足？**

原因：MACD 需要至少 35 个交易日、RSI 需要至少 15 个交易日。解决方法：

1. 增大时间范围（如改为 90 天或 120 天）
2. 在 SKILL.md 的注意事项中添加数据量检查逻辑
3. 让 AI 在代码中添加数据量校验并提供友好提示

**Q5: MCP 连接超时？**

原因可能：网络问题、token 无效、tushare 服务暂时不可用。解决方法：

1. 检查网络连接
2. 验证 MCP 配置：`cat opencode.jsonc`
3. 等待后重试
4. 若 MCP 不可用，回退到 Skill + SDK 方式获取数据

---

## 实验延伸任务（可选）

**任务一：用 JSON 方式配置代理**

参照实验三的 Markdown 配置，在 `opencode.jsonc` 中用 JSON 方式创建一个等效的 `data-auditor-json` 代理，对比两种配置的效果差异。

**任务二：添加风控预警子代理**

在 `.opencode/agents/risk-monitor.md` 中创建一个风控预警子代理，用于检测个股异常波动（涨跌幅超限、成交量异常放大等），并将其集成到日报主代理的工作流中，形成"数据采集 → 报告撰写 → 风控预警"三步协同。

**任务三：优化 stock-tech-analysis Skill**

- 添加布林带指标计算
- 优化 description 提升触发准确率
- 添加"数据缓存"逻辑（避免重复请求 API）
- 使用 skill-improver 再次评估改进效果

---

*实验结束，开始课后作业！*