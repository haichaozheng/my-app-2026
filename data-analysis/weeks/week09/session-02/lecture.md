# 第 2 次课：Skill 基础与应用

> **课时**：80 分钟  
> **目标**：认识 opencode 内置工具体系、掌握 webfetch 和 websearch 工具使用、理解 Skill 的概念和价值、掌握现有 Skill 的安装和使用方法

---

## 💡 课前思考

**回顾第1次课的问题**：

> 请帮我获取贵州茅台（600519）过去 1 年的日线数据，计算日均收益率，并绘制收盘价走势图。

**第1次课的解决方式**：
- 我们直接让 opencode 编写 Python 代码完成
- opencode 自动生成了获取数据、计算指标、绘制图表的代码
- 这种方式可行，但每次都要重新描述详细需求

**本节课的新思考**：
- **如果有一种"专业知识包"，能自动识别金融数据任务，提供标准化的处理流程，效率会不会更高？**
- **opencode 有哪些内置工具能力？**
- **如何让 AI 更专业地完成金融数据分析任务？**

**本次课目标**：
- 学习 opencode 的内置工具体系（webfetch、websearch 等）
- 理解 Skill 的概念和价值
- 学习如何使用 Skill 提升金融数据分析效率

**今天我们将用 Skill 的方式重新完成同样的任务，体验效率提升。**

---

## 一、opencode 内置工具体系（30 分钟）

### 1.1 工具体系概览

**工具是 AI 的"手"**，让 AI 能执行具体操作（读文件、运行命令、搜索网络）。

**类比理解**：
```
类比：工具就像"执行能力的技能"
┌─────────────────────────────────┐
│ 工具（Tools）：执行操作          │ → AI 的"手"
│ Skill：指导如何使用工具           │ → AI 的"说明书"
│ AGENTS.md：项目规则              │ → AI 的"行为准则"
└─────────────────────────────────┘
```

**工具与 Skill 的关系**：
| 维度 | 工具（Tools） | Skill |
|------|-------------|-------|
| 本质 | 执行操作的能力 | 指导如何使用的文档 |
| 作用 | 读文件、运行代码、搜索网络 | 告诉 AI 在什么场景下如何使用工具 |
| 提供方 | opencode 内置 | 用户编写或安装 |
| 例子 | read、write、bash、webfetch | tushare skill、pdf skill |

---

### 1.2 内置工具分类介绍

**文件操作类工具**：
| 工具 | 功能 | 适用场景 |
|------|------|---------|
| read | 读取文件内容 | 查看代码、读取数据文件 |
| write | 创建/覆盖文件 | 生成新代码、保存数据 |
| edit | 精确编辑文件 | 修改代码片段 |
| glob | 文件模式匹配 | 查找 `**/*.py` 文件 |
| grep | 内容搜索 | 搜索代码中的关键词 |

**命令执行类工具**：
| 工具 | 功能 | 适用场景 |
|------|------|---------|
| bash | 执行 Shell 命令 | 运行 Python 代码、git 操作 |
| patch | 应用补丁 | 更新代码片段 |

**网络工具类工具**：
| 工具 | 功能 | 适用场景 |
|------|------|---------|
| webfetch | 获取网页内容 | 查阅文档、读取 API 说明 |
| websearch | 网络搜索 | 研究主题、了解时事 |

**智能工具类工具**：
| 工具 | 功能 | 适用场景 |
|------|------|---------|
| skill | 加载 Skill | 指导 AI 完成特定任务 |
| question | 向用户提问 | 收集用户需求 |
| todowrite | 任务管理 | 跟踪复杂任务进度 |
| lsp（实验性） | 代码智能 | 定义跳转、引用查找 |

---

### 1.3 重点讲解：webfetch 和 websearch

**webfetch 工具详解**：

**功能**：获取指定 URL 的网页内容并转换为可读格式

**配置方式**：在项目级 `opencode.json` 中配置权限
```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "webfetch": "allow"
  }
}
```

**支持格式**：markdown（默认）、text、html

**适用场景**：
- 查阅官方文档
- 获取 API 说明
- 读取在线资源

**使用原则**：
- 需要从**特定 URL 获取内容**（检索）时用 `webfetch`
- 需要**搜索信息**（发现）时用 `websearch`

---

**websearch 工具详解**：

**功能**：在网络上搜索信息，基于 Exa AI 搜索引擎

**重要前提**：需要启用 Exa 环境变量

**配置方式**：

**启动时配置**（推荐）：
```bash
# Windows PowerShell
$env:OPENCODE_ENABLE_EXA="1"; opencode

# macOS / Linux
OPENCODE_ENABLE_EXA=1 opencode
```

**权限配置**（在 opencode.json 中）：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "websearch": "allow"
  }
}
```

**特点**：
- 无需 API 密钥：直接连接 Exa AI 托管服务
- 适用场景：研究主题、了解时事动态、获取训练数据截止日期之后的信息

---

### 1.4 工具权限配置最佳实践

**权限三态**：
| 权限值 | 含义 | 适用场景 |
|-------|------|---------|
| allow | 允许执行 | 安全操作（read、webfetch） |
| ask | 询问用户 | 敏感操作（bash、write） |
| deny | 拒绝执行 | 危险操作（删除文件） |

**配置建议**：
```json
{
  "permission": {
    "bash": "ask",          // Shell 命令需确认
    "write": "ask",         // 创建文件需确认
    "webfetch": "allow",    // 网页获取可自动执行
    "websearch": "allow"    // 网络搜索可自动执行
  }
}
```

**配置位置**：
- **项目级**：在项目根目录创建 `opencode.json`（推荐）
- **全局级**：在 `~/.config/opencode/opencode.json` 中配置

---

## 二、Skill 基础概念（20 分钟）

### 2.1 什么是 Skill

**定义**：Skill 是一段结构化的指令文档（SKILL.md），告诉 AI 如何使用工具完成特定任务。

**Skill 的核心价值：逐层披露细节，节约上下文**：
- AI 默认看不到 Skill 内容，只在需要时才加载
- 相比直接把所有指令写在 AGENTS.md 中，Skill 可以按需加载
- 例如：tushare skill 包含详细的 API 调用说明，但平时不加载，只在用户提到"股票数据"时才触发

---

### 2.2 Skill 与工具的关系

**类比理解**：
```
Skill 就像"操作说明书"
┌─────────────────────────────────┐
│ 工具（Tools）：执行操作          │ → AI 的"手"（能力）
│ Skill：指导如何使用工具           │ → AI 的"说明书"（指导）
│ Prompt：即时指令                 │ → 你说的话（需求）
└─────────────────────────────────┘
```

**协作关系**：
```
用户输入 Prompt（需求）
    ↓
Skill 加载（指导）
    ↓
工具执行（能力）
    ↓
返回结果
```

---

### 2.3 Skill 与 AGENTS.md 的关系

**两者互补，共同构建项目上下文**：

| 维度 | AGENTS.md | Skill |
|------|----------|-------|
| 作用范围 | 项目级通用规则 | 特定任务的专项指导 |
| 内容类型 | 编码规范、数据安全、命名约定 | 如何获取股票数据、如何处理 PDF |
| 加载方式 | 常驻上下文（始终可见） | 按需加载（触发时才可见） |
| 示例 | "Python 代码遵循 PEP 8 规范" | "使用 webfetch 获取西财新闻并保存为 CSV" |

---

### 2.4 Skill 的触发机制

**自动触发**：
```
用户输入："获取贵州茅台的日线数据"
    ↓
opencode 分析输入内容
    ↓
匹配 tushare skill 的 description：
"description": "金融数据相关操作..."
    ↓
自动触发 tushare skill，加载指令
    ↓
AI 按照 Skill 指导使用 bash 工具执行任务
```

**手动调用**：
```bash
# 使用 skill 工具显式加载
> 使用 tushare skill

# 或使用 Skill 名称明确指定
> 用 tushare skill 获取股票数据
```

---

### 2.5 Skill 的组织存放方式

**项目级 Skill**（推荐学生使用）：
- 存放位置：项目的 `.opencode/skills/` 目录
- 仅对该项目生效
- 优势：独立可控，便于调试和版本管理

**用户全局级 Skill**：
- 存放位置：`~/.opencode/skills/` 目录
- 对所有项目生效

**Skill 包（二级 Skill）**：
- 例如 gstack 包含 45 个子 Skill
- 结构：`~/.opencode/skills/gstack/skills/office-hours/SKILL.md`

---

## 三、常用内置 Skill（10 分钟）

### 3.1 tushare Skill（金融数据）

**功能**：获取股票、基金、期货等金融数据

**适用场景**：
- 获取股票日线数据："获取贵州茅台过去 30 天的股价数据"
- 计算技术指标："分析波动趋势，预测未来走势"

**重要提示：tushare token 配置**：

**⚠️ 注意：这是金融数据 Skill 使用的关键前提！**

**获取 token**：访问 [tushare.pro](https://tushare.pro) 注册并获取免费 token

---

**Windows 系统设置方法（必看）**：

**方法 1：临时设置（仅当前 PowerShell 窗口有效，关闭即失效）**
```powershell
# 在 PowerShell 中执行（注意：这是 Windows PowerShell 语法）
$env:TUSHARE_TOKEN = "your_token_here"

# 验证设置成功
echo $env:TUSHARE_TOKEN
# 应输出你的 token 值

# 然后启动 opencode
opencode
```

**💡 提示**：
- `$env:TUSHARE_TOKEN` 是 Windows PowerShell 的环境变量语法
- 关闭 PowerShell 窗口后，环境变量会失效
- 每次使用前需要重新设置

---

**方法 2：永久设置（写入用户环境变量）**
```
1. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
2. 在"用户变量"区域点击"新建"
3. 变量名：TUSHARE_TOKEN
4. 变量值：your_token_here
5. 点击"确定"保存
6. 重启 PowerShell 或重新打开命令行窗口
```

**💡 提示**：
- 这种方式设置的环境变量永久有效
- 所有新打开的 PowerShell 窗口都能使用
- 推荐长期使用

---

**方法 3：在项目根目录创建 .env 文件（推荐）**
```
# 在项目根目录创建 .env 文件
# 文件内容：TUSHARE_TOKEN=your_token_here

# 注意：.env 文件已加入 .gitignore，不会提交到 Git
```

**💡 提示**：
- 这种方式更安全，不会泄露 token
- 只在当前项目中生效
- 适合团队协作项目

---

**macOS/Linux 系统设置方法**：
```bash
# 方法 1：临时设置
export TUSHARE_TOKEN="your_token_here"

# 方法 2：永久设置（写入 ~/.bashrc 或 ~/.zshrc）
echo 'export TUSHARE_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

---

### 3.2 gstack Skill 包（产品开发）

**gstack 是 YC CEO 开发的虚拟工程团队 Skill 包，包含 45 个专业角色**。

**核心 Skill**：
| Skill | 功能 | 适用场景 |
|-------|------|---------|
| `/office-hours` | YC Office Hours 模式 | 产品构思、需求分析 |
| `/plan-ceo-review` | CEO 视角产品评审 | 产品规划、范围控制 |

---

## 四、实践案例演示（20 分钟）

### 🎯 案例一：使用 tushare skill 完成股价波动趋势预测

**场景**：获取股票数据，分析波动趋势并进行简单预测

**步骤演示**：

1. **输入白话指令**：
   ```
   获取贵州茅台（600519）最近 30 天的股价数据，分析波动趋势，预测未来一周的走势
   ```

2. **观察 Skill 触发**：
   - tushare skill 自动触发（因为包含"股价数据"关键词）
   - AI 加载 SKILL.md，理解如何调用 tushare API

3. **AI 执行任务**：
   - 使用 bash 工具运行 Python 代码
   - 调用 tushare API 获取日线数据
   - 计算波动率、均线等技术指标
   - 绘制价格走势图和波动分析图

4. **教学要点**：
   - Skill 的"按需加载"机制：只在需要时才触发
   - Skill 如何节约上下文：平时不加载详细 API 说明
   - 白话指令的便捷性：无需记忆 API 参数

---

### 🎯 案例二：使用 webfetch 查询西财近期新闻并进行数据分析

**场景**：获取西财新闻，存储为 CSV，并进行数据分析

**步骤演示**：

1. **输入指令**：
   ```
   请使用 webfetch 工具获取西南财经大学新闻页面（https://www.swufe.edu.cn/index/xcyw.htm）的近期新闻标题和发布日期，并将结果保存为 CSV 文件
   ```

2. **观察工具组合使用**：
   - webfetch 获取网页内容
   - write 创建 CSV 文件存储数据

3. **继续输入分析指令**：
   ```
   请读取刚才保存的新闻 CSV 文件，统计最近一周的新闻数量，并列出涉及'金融'关键词的新闻
   ```

4. **观察分析过程**：
   - read 读取 CSV 文件
   - bash 运行 Python 代码进行数据分析

5. **教学要点**：
   - 工具组合使用：webfetch + write + read + bash
   - 完整的数据处理流程：获取 → 存储 → 分析
   - 为金融数据分析建立基础认知

---

### 🎯 案例三：开发一个最简洁的 Skill —— 西财新闻抓取 Skill

**场景**：学习如何开发一个最简单的 Skill

**Skill 文件结构**：
```
.opencode/skills/swufe-news/SKILL.md
```

**最小结构示例**：
```yaml
---
name: swufe-news
description: 抓取西南财经大学新闻并存储为CSV文件，支持数据分析和统计
---

# 西财新闻抓取 Skill

## 背景
西南财经大学新闻页面：https://www.swufe.edu.cn/index/xcyw.htm

## 步骤说明

1. 使用 webfetch 工具获取新闻页面内容
2. 解析新闻标题和发布日期
3. 使用 write 工具创建 CSV 文件
4. 提示用户可以使用 read 工具读取或 bash 工具分析

## 示例
用户输入："抓取西财最近新闻并保存"
AI 操作：webfetch → 解析 → write → 输出结果

## 注意事项
- 建议保存后立即读取验证数据质量
```

**教学要点**：
- SKILL.md 的最小结构：frontmatter + 步骤 + 示例
- Skill 如何指导 AI 使用工具
- 为第 3 节课的 Skill 开发实践建立基础

---

### 🎯 案例四：使用 gstack 规划金融数据分析产品

**场景**：规划一个"股票技术指标分析工具"

**步骤演示**：

1. **输入产品构思**：
   ```
   我想开发一个股票技术指标分析工具，能计算 MACD、RSI、布林带，帮我想想这个产品
   ```

2. **使用 `/office-hours`**：
   - AI 会问 6 个引导问题
   - 帮助理清产品定位、目标用户、MVP范围

3. **生成设计文档**：
   - 包含：产品定位、核心功能、技术方案、迭代计划

4. **教学要点**：
   - AI 辅助产品开发流程
   - 结构化思维引导
   - 从构思到规划的完整流程

---

## 五、本次课总结

**核心要点**：

1. **工具体系**：工具是 AI 的"手"，包括文件操作、命令执行、网络工具、智能工具
2. **webfetch vs websearch**：webfetch 用于获取特定 URL 内容，websearch 用于搜索信息
3. **Skill 的核心价值**：逐层披露细节，节约上下文
4. **Skill 与工具的关系**：Skill 是"说明书"，指导 AI 如何使用工具
5. **Skill 的触发机制**：自动触发（description 匹配）和手动调用
6. **常用 Skill**：tushare（金融数据）、gstack（产品开发）

**下次课预告**：

下次课将学习 **Skill 开发实践**，内容包括：
- SKILL.md 文件编写方法
- 金融数据分析 Skill 设计方法
- 使用 skill-creator 辅助开发
- 错误处理和优化技巧

---

## 参考资料

**官方文档**：
- OpenCode 工具文档：https://opencode.ai/docs/zh-cn/tools/
- OpenCode Skills 文档：https://opencode.ai/docs/skills/

**推荐学习项目**：
- anthropics/skills：官方 Skills 仓库（126K Stars）
- garrytan/gstack：虚拟工程团队（45 个专业角色）
- datawhalechina/agent-skills-with-anthropic：吴恩达课程中文版

---

*本次课结束，开始上机实验！*