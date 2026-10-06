# Week 01 课堂串讲

> 本文件为课堂投影串讲稿，规格与兜底以 `plan.md` 为准。

## 第1节 · 范式定向与全流程映射

- 学期终点：个人科研项目 + AI4S 工具栈仓库 + 论文
- AI4S 范式：AI 是研究伙伴，贯穿科研全流程
- 人机交互姿态：人判断、AI 执行
- 五模块映射：文献→选题→设计→实施→写作
- 9 周课程安排总览

## 第2节 · 工具环境搭建

> 课前发 `weeks/week01/setup.md`。白板先写：**卡住 → 问 AI（附报错）→ 同组互查 → 举手教师**。

### 2.1 Python 3.13 + Cursor

- 全班统一 **3.13**，不点官网首页 3.14，不装 Anaconda
- 终端 `python --version` 须为 3.13.x
- Cursor 里 `Ctrl+Shift+P → Python: Select Interpreter`，选路径里有 `Python313` 的
- 不要选 `anaconda3`，不要选 WindowsApps 商店别名
- 已装 Anaconda 的：`conda config --set auto_activate_base false`，重开终端
- 先装 `wbgapi pandas`（世界银行数据 API + 数据分析库）

### 2.2 opencode

- Node.js LTS（24.x）→ `npm install -g opencode-ai` → `opencode --version`
- **必须在项目根目录打开**（有 `AGENTS.md` 的那一层）
- 选模型：默认免费可跟课
- 练四条命令：`/connect` `/model` `/session` `/compact`
- **工作模式**：对话→改文件→运行，不是网页 Chat 那样只停在对话

### 2.3 第一个脚本

- 在项目根目录让 opencode 生成 `wb_explore.py`
- 用 wbgapi 拉取中国近 10 年人均 GDP 和 GDP 增长率
- **必须点运行且终端无报错**
- 世界银行 1400+ 指标覆盖 19 个主题，可换成自己研究方向的指标

## 第3节 · Prompt 初体验与下周铺垫

### 3.1 Prompt 三原则

- 清晰性、上下文、约束
- 对比"拉点经济数据" vs "用 wbgapi 拉取中国（CHN）近 10 年的人均 GDP（NY.GDP.PCAP.CD）和 GDP 增长率（NY.GDP.MKTP.KD.ZG），输出 pandas DataFrame，年份作为行"

### 3.2 opencode 工作模式深化

- 演示闭环：让 opencode 把 `wb_explore.py` 改成拉取多个国家（CHN、USA、IND、BRA）的同一组指标、输出对比表
- opencode 直接改磁盘文件、可运行——这是后续科研编程的工作模式底座

### 3.3 AGENTS.md

- 最简版 3-5 行：项目目标 + 技术栈 + 目录约定
- opencode 打开时自动读取作为上下文
- 后续随项目演进逐步完善

### 3.4 下周铺垫

- 文献检索是方法论（PRISMA 流程），不是"搜一下"
- 本周的 opencode 工作模式就是下周写检索脚本的基础
