# 第 2 次课上机实验：Skill 基础与应用

> **实验时长**：90 分钟  
> **实验目标**：配置工具权限、使用 webfetch/websearch、安装和使用 tushare skill、开发简单 Skill、使用 gstack 规划金融分析工具

---

## 实验环境准备（5 分钟）

### 前置条件检查

**验证清单**：

| 检查项 | 验证命令 | 预期结果 | 备注 |
|-------|---------|---------|------|
| opencode 已安装 | `opencode --version` | 显示版本号 | 如未安装，参考第1次课 |
| Python 已安装 | `python --version` | Python 3.7+ | 必需 |
| pandas 已安装 | `pip list | grep pandas` | pandas 已列出 | 用于数据分析 |
| tushare Token 已配置 | `echo $env:TUSHARE_TOKEN` (Windows) | 显示你的 token | **关键！如未配置需先配置** |

---

**⚠️ tushare Token 配置检查（重要）**：

```powershell
# Windows PowerShell 中验证
echo $env:TUSHARE_TOKEN

# 如果输出为空或显示错误，说明 token 未配置
# 必须按以下步骤配置（参考实验 2.2）：

# 临时设置（启动 opencode 前执行）
$env:TUSHARE_TOKEN = "your_actual_token_here"

# 验证设置成功
echo $env:TUSHARE_TOKEN
# 应输出你的 token 值
```

**重要提示**：
- tushare Token 是使用金融数据 Skill 的前提
- 如果未配置，实验 2.3 将无法完成
- 建议在实验开始前就配置好 token

---

### 实验目录设置

**操作步骤**：

```powershell
# 1. 进入项目目录
cd C:\haichao\build\finance-ai-coding

# 2. 创建本次实验的工作目录
mkdir teaching-materials\session-02\lab-work -Force

# 3. 进入实验目录
cd teaching-materials\session-02\lab-work

# ⚠️ 重要：如果需要使用 tushare skill，请在启动 opencode 前设置 token
# 方法 1：临时设置（仅当前窗口有效）
$env:TUSHARE_TOKEN = "your_actual_token_here"

# 验证 token 设置（必须验证）
echo $env:TUSHARE_TOKEN
# 应输出你的 token 值

# 方法 2：一行命令设置并启动
# $env:TUSHARE_TOKEN = "your_token"; opencode

# 4. 启动 opencode（在设置环境变量后）
opencode
```

**验证**：
- opencode TUI 界面成功启动
- 当前目录为 `C:\haichao\build\finance-ai-coding\teaching-materials\session-02\lab-work`
- tushare token 已设置（如果需要使用金融数据 Skill）

**⚠️ 提示**：
- 如果未设置 tushare token，实验 2.3 将无法完成
- 建议在实验开始前就配置好所有必要的环境变量
- 环境变量设置必须在启动 opencode **之前**完成

---

## 实验一：工具配置练习（30 分钟）

### 1.1 创建 opencode.json 配置文件

**实验任务**：在项目根目录创建 `opencode.json`，配置 webfetch 和 websearch 工具权限

**操作步骤**：

**步骤 1**：在 opencode TUI 中输入以下指令：

```
请在当前目录创建一个 opencode.json 文件，配置以下工具权限：
- webfetch: allow
- websearch: allow
- bash: ask
- write: ask
```

**步骤 2**：观察 AI 如何创建文件：
- AI 使用 write 工具创建 opencode.json
- 文件内容包含权限配置

**步骤 3**：验证文件创建成功：
```powershell
# 在 PowerShell 中执行（退出 opencode 或另开终端）
cat opencode.json
```

**预期输出**：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "webfetch": "allow",
    "websearch": "allow",
    "bash": "ask",
    "write": "ask"
  }
}
```

**✅ 检查点**：opencode.json 文件已创建，内容包含正确的权限配置

---

### 1.2 使用 webfetch 获取西财新闻页面内容

**实验任务**：获取西南财经大学新闻页面并保存为 CSV

**操作步骤**：

**步骤 1**：在 opencode 中输入：

```
请使用 webfetch 工具获取西南财经大学新闻页面（https://www.swufe.edu.cn/index/xcyw.htm）的近期新闻标题和发布日期，并将结果保存为 CSV 文件，文件名为 swufe_news.csv
```

**步骤 2**：观察工具调用过程：
- AI 调用 webfetch 工具获取网页内容
- AI 解析新闻标题和日期
- AI 使用 write 工具创建 CSV 文件（需要用户确认，因为 write 权限为 ask）

**步骤 3**：确认 write 操作：
- opencode 会弹出确认提示："是否允许 write 工具创建文件 swufe_news.csv？"
- 输入 `y` 或 `yes` 确认

**步骤 4**：验证 CSV 文件生成：
```powershell
# 退出 opencode 或另开终端
cat swufe_news.csv | more
```

**预期结果**：
- CSV 文件包含多行新闻数据
- 格式：序号,日期,标题,URL
- 至少包含 10 条以上的新闻

**✅ 检查点**：swufe_news.csv 已生成，包含新闻标题和日期数据

---

### 1.3 读取 CSV 文件并进行数据分析

**实验任务**：读取刚才保存的 CSV 文件，进行简单统计

**操作步骤**：

**步骤 1**：在 opencode 中输入：

```
请读取刚才保存的 swufe_news.csv 文件，统计总共有多少条新闻，并列出最近一周的新闻标题
```

**步骤 2**：观察工具调用：
- AI 使用 read 工具读取 CSV 文件
- AI 使用 bash 工具运行 Python 代码进行数据分析（需要确认）

**步骤 3**：确认 bash 操作：
- opencode 会弹出确认提示："是否允许 bash 工具运行 Python 代码？"
- 输入 `y` 确认

**步骤 4**：查看分析结果：
- AI 输出统计结果："总共有 XX 条新闻"
- AI 输出最近一周的新闻列表

**预期结果**：
- 显示新闻总数
- 显示最近一周的新闻标题

**✅ 检查点**：成功读取 CSV 文件并完成数据分析

---

### 1.4 启用 websearch 工具

**实验任务**：配置并使用 websearch 工具搜索金融新闻

**操作步骤**：

**步骤 1**：关闭当前的 opencode 会话：
```
在 opencode TUI 中输入：exit
```

**步骤 2**：重新启动 opencode 并启用 Exa：
```powershell
# Windows PowerShell
$env:OPENCODE_ENABLE_EXA="1"; opencode

# 验证环境变量已设置
echo $env:OPENCODE_ENABLE_EXA
# 应输出：1
```

**步骤 3**：使用 websearch 搜索金融新闻：
```
请使用 websearch 工具搜索最近的中国金融科技发展趋势相关新闻，列出前 5 条并简要说明
```

**步骤 4**：观察搜索结果：
- AI 调用 websearch 工具
- 返回 5 条新闻标题和摘要
- 每条新闻包含标题、来源、摘要

**预期结果**：
- 显示 5 条金融科技新闻
- 每条新闻包含标题和简要说明

**✅ 检查点**：websearch 成功启用并返回搜索结果

---

### 1.5 对比 webfetch 和 websearch 的使用场景

**实验任务**：理解两种工具的差异

**对比表格**：

| 维度 | webfetch | websearch |
|------|----------|-----------|
| 用途 | 从特定 URL 获取内容 | 在网络搜索信息 |
| 输入 | 明确的 URL 地址 | 关键词搜索 |
| 输出 | 网页完整内容 | 搜索结果列表 |
| 适用场景 | 读取文档、API 说明 | 研究主题、了解时事 |
| 示例 | 获取西财新闻页面内容 | 搜索金融科技新闻 |

**实验记录**：
- 记录 webfetch 成功获取的内容类型：___
- 记录 websearch 返回的结果格式：___
- 总结两者的使用场景差异：___

**✅ 检查点**：理解 webfetch 和 websearch 的使用场景差异

---

## 实验二：Skill 安装与使用练习（60 分钟）

### 2.1 安装 tushare skill（项目级）

**实验任务**：在项目级目录安装 tushare skill

**操作步骤**：

**步骤 1**：检查 tushare skill 是否已安装：
```powershell
# 退出 opencode 或另开终端
ls .opencode\skills\tushare\SKILL.md
```

**步骤 2**：如果未安装，使用 opencode 安装：
```
请在项目级目录 .opencode/skills/ 中安装 tushare skill，从 https://github.com/waditu-tushare/skills 克隆
```

**步骤 3**：观察安装过程：
- AI 使用 bash 工具运行 git clone 命令（需要确认）
- 克隆到 `.opencode/skills/tushare/` 目录

**步骤 4**：验证安装成功：
```powershell
ls .opencode\skills\tushare\
# 应看到：SKILL.md、references、scripts
```

**预期结果**：
- `.opencode/skills/tushare/` 目录已创建
- 包含 SKILL.md 文件

**✅ 检查点**：tushare skill 成功安装到项目级目录

---

### 2.2 配置 tushare Token

**⚠️ 重要提示：这是使用 tushare skill 的关键前提！必须先配置 token！**

**实验任务**：设置 tushare API token

---

**操作步骤**：

**步骤 1**：获取 tushare token：
- 访问 https://tushare.pro
- 注册账号并获取免费 token

---

**步骤 2**：在 Windows PowerShell 中设置环境变量（关键步骤）

**⚠️ 注意：以下命令必须在 Windows PowerShell 中执行！**

```powershell
# 方法 1：临时设置（仅当前窗口有效，关闭即失效）
# 注意：这是 Windows PowerShell 的语法，不是 Linux bash 的语法
$env:TUSHARE_TOKEN = "your_actual_token_here"

# 验证设置成功（必须验证）
echo $env:TUSHARE_TOKEN
# 应输出：your_actual_token_here（你的实际 token）

# 如果输出为空，说明设置失败，请检查语法是否正确
```

**💡 重要提示**：
- `$env:TUSHARE_TOKEN` 是 **Windows PowerShell 的环境变量语法**
- **不要**使用 Linux 的 `export TUSHARE_TOKEN="xxx"` 语法
- 这个环境变量只在当前 PowerShell 窗口有效
- 关闭窗口后需要重新设置
- 必须在启动 opencode **之前**设置环境变量

---

**步骤 3**：如果想要永久生效，可以设置用户环境变量：

**方法 2：永久设置（推荐长期使用）**
```
1. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
2. 在"用户变量"区域点击"新建"
3. 输入：
   - 变量名：TUSHARE_TOKEN
   - 变量值：your_actual_token_here
4. 点击"确定"保存
5. 关闭当前 PowerShell，重新打开一个新的 PowerShell 窗口
6. 验证：echo $env:TUSHARE_TOKEN（应显示你的 token）
```

---

**步骤 4**：或者创建 .env 文件（推荐项目级使用）：

```powershell
# 在 opencode 中输入以下指令（让 AI 创建 .env 文件）
请在当前目录创建 .env 文件，内容为：TUSHARE_TOKEN=your_actual_token_here
```

**验证 .env 文件**：
```powershell
# 在 PowerShell 中验证
cat .env
# 应看到：TUSHARE_TOKEN=your_token_here
```

**重要提示**：.env 文件已加入 .gitignore，不会提交到 Git，更安全

---

**步骤 5**：验证 token 配置是否成功（必做）

```powershell
# 验证方法 1：检查环境变量
echo $env:TUSHARE_TOKEN
# 应显示你的 token

# 验证方法 2：检查 .env 文件（如果使用方法 3）
cat .env
# 应显示：TUSHARE_TOKEN=your_token_here
```

**⚠️ 如果验证失败**：
- 检查是否使用正确的 PowerShell 语法 `$env:TUSHARE_TOKEN`
- 检查 token 值是否正确（不要有空格）
- 如果使用临时设置，确认没有关闭 PowerShell 窗口
- 如果使用永久设置，确认已重启 PowerShell

---

**✅ 检查点**：
- tushare token 已成功配置
- 环境变量验证成功（echo $env:TUSHARE_TOKEN 显示正确值）
- 或 .env 文件验证成功（cat .env 显示正确内容）

---

**💡 常见错误提示**：

| 错误现象 | 原因 | 解决方法 |
|---------|------|---------|
| `echo $env:TUSHARE_TOKEN` 输出为空 | 未设置环境变量或语法错误 | 检查 PowerShell 语法，重新设置 |
| 使用了 `export TUSHARE_TOKEN="xxx"` | 这是 Linux 语法，Windows 不支持 | 改用 `$env:TUSHARE_TOKEN = "xxx"` |
| opencode 启动后 token 不生效 | 在 opencode 内部无法设置环境变量 | 必须在启动 opencode **之前**设置 |
| token 有空格或特殊字符 | 复制粘贴时引入了多余字符 | 重新复制 token，确保无空格 |

---

### 2.3 使用 tushare skill 获取股票数据

**⚠️ 前提条件：tushare token 必须已配置成功！**

**实验任务**：获取平安银行（000001）最近 30 天的股价数据

---

**操作步骤**：

**步骤 1**：验证 token 配置（启动前必做）

```powershell
# 在 PowerShell 中验证 token 是否已设置
echo $env:TUSHARE_TOKEN
# 必须显示你的 token 值

# 如果显示为空，必须先按 2.2 步骤设置 token
# 注意：必须在启动 opencode 之前设置环境变量
```

---

**步骤 2**：重启 opencode（确保 token 环境变量生效）

```powershell
# 关闭之前的 opencode（如果在运行）
# 重新启动 opencode（确保 token 在启动前已设置）

# 方法 1：临时设置后启动
$env:TUSHARE_TOKEN = "your_actual_token_here"; opencode

# 方法 2：如果已永久设置，直接启动
opencode
```

**⚠️ 重要提示**：
- **必须**在启动 opencode 之前设置 token
- **不能**在 opencode 运行时设置环境变量
- opencode 启动时会读取环境变量，之后无法修改

---

**步骤 3**：在 opencode 中输入白话指令

```
获取平安银行（000001）最近 30 天的股价数据，分析波动趋势并绘制走势图
```

---

**步骤 4**：观察 Skill 触发过程：
- AI 分析输入内容，识别"股价数据"关键词
- 自动触发 tushare skill
- Skill 注入金融数据获取的上下文

---

**步骤 5**：观察 AI 执行：
- AI 使用 bash 工具运行 Python 代码（需要确认）
- 代码调用 tushare API 获取数据
- 代码计算波动率、均线
- 代码生成走势图

---

**步骤 6**：确认 bash 操作：
- 输入 `y` 确认运行 Python 代码

---

**步骤 7**：验证生成文件：
```powershell
ls *.png *.csv *.py
# 应看到：走势图文件、数据文件、Python代码文件
```

---

**预期结果**：
- 成功生成 Python 代码文件
- 成功生成股价走势图（PNG 格式）
- 成功生成数据文件（CSV 格式）

---

**⚠️ 如果 tushare API 调用失败**：

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `token is invalid` | token 未设置或无效 | 检查 `$env:TUSHARE_TOKEN` 是否正确 |
| `积分不足` | 新用户积分不足 | 登录 tushare.pro 查看积分，使用基础接口 |
| `网络错误` | 无法连接 tushare | 检查网络连接 |
| `No data found` | 股票代码错误 | 确认股票代码正确（000001.SH） |

---

**✅ 检查点**：
- tushare skill 成功触发
- Python 代码成功生成
- 股价走势图成功绘制
- 数据文件成功保存

---

### 2.4 开发一个简单的 Skill：西财新闻抓取 Skill

**实验任务**：创建一个简单的 Skill 实现西财新闻抓取

**操作步骤**：

**步骤 1**：创建 Skill 目录：
```
请在 .opencode/skills/ 目录下创建 swufe-news 目录
```

**步骤 2**：编写 SKILL.md 文件：
```
请在 .opencode/skills/swufe-news/ 目录下创建 SKILL.md 文件，内容如下：

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
3. 使用 write 工具创建 CSV 文件，格式：序号,日期,标题,URL
4. 文件命名为 swufe_news.csv

## 示例
用户输入："抓取西财最近新闻并保存"
AI 操作：webfetch → 解析 → write → 输出"已保存 XX 条新闻"

## 注意事项
- 建议保存后立即读取验证数据质量
```

**步骤 3**：观察文件创建：
- AI 使用 write 工具创建 SKILL.md 文件（需要确认）
- 输入 `y` 确认

**步骤 4**：验证 Skill 创建：
```powershell
cat .opencode\skills\swufe-news\SKILL.md | more
```

**步骤 5**：测试 Skill 触发：
```
抓取西财最近新闻并保存
```

**步骤 6**：观察 Skill 执行：
- Skill 是否自动触发？
- AI 是否按照 SKILL.md 的步骤执行？

**预期结果**：
- SKILL.md 文件已创建
- Skill 成功触发并生成 swufe_news.csv

**✅ 检查点**：成功开发简单 Skill 并验证触发

---

### 2.5 安装 gstack skill 包

**实验任务**：安装 gstack skill 包

**操作步骤**：

**步骤 1**：安装 gstack：
```
请在用户全局目录 ~/.opencode/skills/ 中安装 gstack skill 包
克隆地址：https://github.com/garrytan/gstack.git
并运行 setup 脚本
```

**步骤 2**：观察安装过程：
- AI 使用 bash 工具运行 git clone（需要确认）
- AI 运行 setup 脚本（需要确认）

**步骤 3**：验证安装：
```powershell
ls .opencode\skills\gstack\skills\
# 应看到多个子 Skill 目录（如 office-hours、plan-ceo-review 等）
```

**步骤 4**：检查 Skill 数量：
```powershell
(ls .opencode\skills\gstack\skills\).Count
# 应显示约 45 个子 Skill
```

**预期结果**：
- gstack skill 包已安装
- 包含约 45 个子 Skill

**✅ 检查点**：gstack skill 包成功安装

---

### 2.6 使用 gstack 规划金融分析工具

**实验任务**：使用 office-hours 和 plan-ceo-review 规划产品

**操作步骤**：

**步骤 1**：输入产品构思：
```
我想开发一个股票技术指标分析工具，能计算 MACD、RSI、布林带，帮我想想这个产品
```

**步骤 2**：手动触发 office-hours：
```
使用 gstack 的 office-hours skill
```

**步骤 3**：回答 AI 的引导问题：
- **痛点**：现有工具需要手动写代码，效率低
- **目标用户**：金融专业学生、个人投资者
- **MVP 范围**：先实现 MACD 计算
- **验证方式**：对比通达信功能，找同学试用
- **技术方案**：Python + pandas + matplotlib
- **迭代计划**：第一周 MACD，第二周 RSI，第三周布林带

**步骤 4**：观察设计文档生成：
- AI 生成设计文档（Markdown 格式）
- 包含：产品定位、核心功能、技术方案、迭代计划

**步骤 5**：使用 plan-ceo-review 评审：
```
使用 gstack 的 plan-ceo-review skill 评审刚才的产品设计
```

**步骤 6**：观察评审过程：
- AI 从 CEO 视角提问
- 检查产品范围、优先级、可行性

**步骤 7**：生成评审报告：
- AI 生成评审报告（Markdown 格式）
- 包含：优点、风险点、改进建议

**预期结果**：
- 成功生成设计文档（design_doc.md）
- 成功生成评审报告（ceo_review.md）

**✅ 检查点**：成功使用 gstack 完成产品规划和评审

---

## 实验总结与验证（5 分钟）

### 验证清单

| 实验内容 | 完成状态 | 验证结果 |
|---------|---------|---------|
| 创建 opencode.json 配置文件 | ✅/❌ | |
| 配置 webfetch 和 websearch 权限 | ✅/❌ | |
| 使用 webfetch 获取西财新闻 | ✅/❌ | |
| 使用 websearch 搜索金融新闻 | ✅/❌ | |
| 安装 tushare skill（项目级） | ✅/❌ | |
| 配置 tushare Token | ✅/❌ | |
| 使用 tushare skill 获取股价数据 | ✅/❌ | |
| 开发简单的 swufe-news Skill | ✅/❌ | |
| 安装 gstack skill 包 | ✅/❌ | |
| 使用 office-hours 规划产品 | ✅/❌ | |
| 使用 plan-ceo-review 评审产品 | ✅/❌ | |

---

### 实验成果展示

**应生成的文件**：
```powershell
ls
# 应包含：
# - opencode.json                # 工具权限配置文件
# - swufe_news.csv               # 西财新闻数据文件
# - pingan_bank_*.png            # 平安银行股价走势图
# - pingan_bank_*.csv            # 平安银行股价数据
# - .opencode/skills/tushare/    # tushare skill 目录
# - .opencode/skills/swufe-news/ # 自定义 Skill 目录
# - design_doc.md                # 产品设计文档
# - ceo_review.md                # CEO 评审报告
```

---

### 实验反思

**记录实验心得**：

1. **工具权限配置**：
   - allow、ask、deny 三种权限的区别是什么？
   - 为什么 write 和 bash 设置为 ask？
   
2. **webfetch vs websearch**：
   - 何时使用 webfetch？何时使用 websearch？
   - 两者的输出格式有何差异？

3. **Skill 的价值**：
   - Skill 如何节约上下文？
   - Skill 的"按需加载"机制如何工作？

4. **遇到的困难**：
   - tushare Token 配置遇到什么问题？如何解决？
   - gstack 安装遇到什么问题？如何解决？

---

## 实验常见问题

### Q1: opencode.json 配置后权限不生效？

**答**：
- 原因可能：文件位置错误、JSON 格式错误
- 解决方法：
  1. 确认 opencode.json 在项目根目录
  2. 使用 `cat opencode.json` 验证 JSON 格式正确
  3. 重启 opencode 会话

---

### Q2: websearch 工具无法使用？

**答**：
- 原因可能：未启用 Exa 环境变量
- 解决方法：
  1. 关闭 opencode
  2. 设置环境变量：`$env:OPENCODE_ENABLE_EXA="1"; opencode`
  3. 验证环境变量：`echo $env:OPENCODE_ENABLE_EXA`

---

### Q3: tushare skill 没有自动触发？

**答**：
- 原因可能：Skill 未安装、description 不匹配、Token 未配置
- 解决方法：
  1. 检查 Skill 是否安装：`ls .opencode/skills/tushare/SKILL.md`
  2. 手动调用：`使用 tushare skill`
  3. 检查 Token：`echo $env:TUSHARE_TOKEN`
  4. 使用明确的金融关键词："股价数据"、"日线数据"

---

### Q4: tushare API 调用失败？

**答**：
- 原因可能：Token 无效、积分不足、网络问题、**环境变量语法错误**
- 解决方法：
  1. **验证 Token 是否正确设置（必做）**：
     ```powershell
     # Windows PowerShell 验证
     echo $env:TUSHARE_TOKEN
     # 应显示你的 token 值，如果为空则未设置
     
     # 如果为空，检查是否使用了错误的语法：
     # ❌ 错误：export TUSHARE_TOKEN="xxx"（这是 Linux 语法）
     # ✅ 正确：$env:TUSHARE_TOKEN = "xxx"（Windows PowerShell 语法）
     ```
  
  2. **重新设置 Token（如果验证失败）**：
     ```powershell
     # 方法 1：临时设置
     $env:TUSHARE_TOKEN = "your_actual_token_here"
     echo $env:TUSHARE_TOKEN  # 验证
     
     # 方法 2：启动 opencode 前设置
     $env:TUSHARE_TOKEN = "your_token"; opencode
     ```
  
  3. **登录 tushare.pro 验证 Token 和积分**
  
  4. **使用基础接口（如 daily），新用户通常可访问**
  
  5. **检查网络连接**
  
  6. **在代码中添加错误处理：`try-except`**

---

**⚠️ Windows 环境变量设置常见错误**：

| 错误语法 | 原因 | 正确语法 |
|---------|------|---------|
| `export TUSHARE_TOKEN="xxx"` | 这是 Linux/bash 语法，Windows PowerShell 不支持 | `$env:TUSHARE_TOKEN = "xxx"` |
| `set TUSHARE_TOKEN=xxx` | 这是 cmd 语法，PowerShell 不支持 | `$env:TUSHARE_TOKEN = "xxx"` |
| `$env:TUSHARE_TOKEN=xxx` | PowerShell 语法错误（缺少空格） | `$env:TUSHARE_TOKEN = "xxx"` |
| 在 opencode 内部设置环境变量 | opencode 运行时无法修改环境变量 | 在启动 opencode **之前**设置 |

---

**💡 正确的 Windows PowerShell 环境变量设置流程**：

```powershell
# 步骤 1：在 PowerShell 中设置环境变量
$env:TUSHARE_TOKEN = "your_actual_token_here"

# 步骤 2：验证设置成功
echo $env:TUSHARE_TOKEN
# 应输出：your_actual_token_here

# 步骤 3：启动 opencode（在设置环境变量后）
opencode

# 步骤 4：在 opencode 中使用 tushare skill
获取贵州茅台的股价数据
```

---

### Q5: gstack 安装失败？

**答**：
- 原因可能：Git 克隆失败、setup 脚本权限问题
- 解决方法：
  1. 检查网络，确保能访问 GitHub
  2. 确认目录存在：`mkdir -Force ~/.opencode/skills`
  3. 手动执行 setup：`cd ~/.opencode/skills/gstack; ./setup`

---

### Q6: 生成的代码有错误？

**答**：
- 这是正常的，Skill 提供指导，代码可能需要调整
- 解决方法：
  1. 将错误信息反馈给 opencode，让它修正
  2. 根据错误提示手动修改代码
  3. 记录遇到的错误和解决方法

---

## 实验延伸任务（可选）

### 任务一：对比工具和 Skill 的效率

**实验内容**：对比直接使用工具和使用 Skill 的效率差异

| 任务 | 直接使用工具（分钟） | 使用 Skill（分钟） | 效率提升 |
|------|------------------|------------------|---------|
| 获取西财新闻 | | | |
| 获取股价数据 | | | |
| 产品规划 | | | |

---

### 任务二：探索更多 Skill

**实验内容**：尝试安装和使用其他 Skill
- pdf skill：读取 PDF 文件
- literature-search skill：搜索学术论文
- code-review-excellence skill：代码审查

---

### 任务三：优化自定义 Skill

**实验内容**：改进 swufe-news Skill
- 添加错误处理
- 优化 description 提升触发准确率
- 添加数据分析功能

---

*实验结束，开始课后作业！*