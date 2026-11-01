# Week 01 教学计划

## 本周主题

工具准备 — AI工作环境搭建（AI4S范式入门）

> Phase 1: Foundation 第1周。本周是整门课的起点：不是"装软件"，而是为 AI4S 科研全流程奠定工具基础，并建立"人判断、AI执行"的人机交互姿态。

## 学习目标

- 能用自己的话说明 AI4S 范式：AI 贯穿科研全流程，是"研究伙伴"而非工具箱
- 能配置好 AI 工作环境：Python 3.13 + Cursor（选中解释器）+ opencode（项目根目录打开、选模型、基础命令）
- 能说明 opencode 的工作模式：**对话→改文件→运行**，区别于网页版 Chat 只停在对话
- 能写最简版 `AGENTS.md`，让 opencode 读取作为项目上下文
- 能用 wbgapi 拉取世界银行数据，完成第一个 Prompt 驱动的科研脚本，验证环境可用
- 能说明社科科研全流程的五个环节，并把 AI4S 工具栈映射到每个环节

## 教学步骤（3节课）

**第1节 · 范式定向与全流程映射（45 分钟）**

1. 开场（5 分钟）：点明学期终点——围绕个人科研项目构建 AI4S 工具栈并产出科研成果（论文 + 工具栈仓库）
2. AI4S 范式讲解（15 分钟）：AI4S 不是"用 AI 写代码"，而是用 AI 重构科研全流程；人机交互姿态（人判断、AI 执行）
3. 社科科研全流程映射（15 分钟）：文献→选题→设计→实施→写作五模块，对应 9 周课程安排
4. 个人科研项目启动（10 分钟）：每位博士生在便签上写研究方向关键词 + 1 个痛点。💡 课堂互动：随机抽取 3-4 位同学投屏分享研究方向与痛点，全班交流（4-5 分钟）

**第2节 · 工具环境搭建（45 分钟）**

> 课前把 `weeks/week01/setup.md` 发到课程群，要求带电脑当堂跟装。白板先写课上求助顺序：**卡住 → 问 AI（附报错）→ 同学互助解答 → 举手教师**。安装类问题优先问已跑通的同学。

5. **Python 3.13 + Cursor 安装与选解释器（15 分钟）**：按 `weeks/week01/setup.md` 第一、二部分。全班终端跑 `python --version`（须为 3.13.x）；在 Cursor 里 `Ctrl+Shift+P → Python: Select Interpreter` 选路径里有 `Python313` 的，不要选 Anaconda、不要选 WindowsApps 商店别名。先装 `wbgapi pandas` 两个包（世界银行数据 API 客户端 + 数据分析库）。**不装 Anaconda、不点官网首页 3.14**。
6. **opencode 安装与基础用法（15 分钟）**：按 `weeks/week01/setup.md` 第三部分。官网 LTS Node.js（24.x）→ `npm install -g opencode-ai` → `opencode --version`。在项目根目录输入 `opencode` 启动 TUI；选模型（默认免费可跟课）；练 `/connect` `/model` `/session` `/compact` 四条命令。点明 opencode 的工作模式：**对话→改文件→运行**，不是网页版 Chat 那样只停在对话。
7. **文献管理工具安装（5 分钟）**：Zotero 或同类工具，本周装好即可，W2/W3 用到。
8. **第一个 Prompt 驱动脚本（10 分钟）**：用 opencode 在项目根目录生成 `wb_explore.py`——用 wbgapi 拉取世界银行数据（如中国近 10 年人均 GDP 与增长率），打印 DataFrame。**必须点运行且终端无报错**。世界银行有 1400+ 指标覆盖 19 个主题（经济/教育/健康/性别/贫困/科技等），学生可换成自己研究方向的指标。AGENTS.md 先写一个最简版（3-5 行：项目目标、技术栈、目录约定），opencode 打开时自动读取作为上下文。

**第3节 · Prompt 初体验与下周铺垫（45 分钟）**

9. **Prompt 三原则在实操中自然体验（10 分钟）**：清晰性、上下文、约束。拿第2节那个 `wb_explore.py` 当例子——对比"拉点经济数据"和"用 wbgapi 拉取中国（CHN）近 10 年的人均 GDP（NY.GDP.PCAP.CD）和 GDP 增长率（NY.GDP.MKTP.KD.ZG），输出 pandas DataFrame，年份作为行"两种问法的输出差异。
10. **opencode 工作模式深化（10 分钟）**：演示"对话→改文件→运行"闭环——让 opencode 把 `wb_explore.py` 改成拉取多个国家（如 CHN、USA、IND、BRA）的同一组指标、输出对比表，并简单标注最高增长率的国家。强调 opencode 直接改磁盘文件、可运行，这是它区别于网页 Chat 的核心，也是后续科研编程（W2 检索脚本、W6 数据清洗、W8 论文起草）的工作模式底座。
11. **个人脚本调试与互查（15 分钟）**：每人跑通自己的脚本，同学互助解答。AGENTS.md 至少写好项目目标与技术栈两行。卡住先问同学（对方口述步骤、盯着自己键入）；两分钟仍卡再举手。
12. **下周铺垫（8 分钟）**：文献检索是方法论（PRISMA 流程），不是"搜一下"；预告 W2 检索式与学术 API。本周的 opencode 工作模式就是下周写检索脚本的基础。
13. **收束（2 分钟）**：布置课后自学与作业。

## 交付物

- **工具环境就绪**（评分锚点，对应 milestones §1.1）
  - opencode/cursor 可正常运行（`opencode --version` 截图 + Cursor 选中 Python313 截图）
  - Python 环境配置完成（`python --version` 为 3.13.x）
  - wbgapi + pandas 安装成功（`pip install wbgapi pandas` 无报错）
  - API key 配置完成（opencode 至少能连一个模型；默认免费模型也算）
  - 文献管理工具安装完成（Zotero 或同类）
  - 至少一个 Prompt 驱动的小脚本（`wb_explore.py`，用 wbgapi 拉取世界银行数据，能运行、终端无报错）
  - 最简版 `AGENTS.md`（项目目标 + 技术栈 + 目录约定，3-5 行起步）
- 方法论锚定：体现 AI4S 范式理解、Prompt Engineering 初步应用、工具选择意识（说明选择了 opencode/cursor 还是其他、为什么）

## 课后自学

- **环境安装**：`weeks/week01/setup.md`（Python 3.13 + Cursor + opencode，当堂没装完的课后补齐）
- Prompt Engineering 方法论：`knowledge/m1-3-prompt-engineering.md`
- AI4S 范式与方法论：`knowledge/m1-1-ai4s-paradigm.md`
- 社科科研全流程映射：`knowledge/m1-4-research-workflow-mapping.md`
- AI 辅助编程（opencode/cursor）：`knowledge/m1-2-ai-coding.md`
- opencode 规则：[AGENTS.md 与 `/init`](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)
- **方法论阅读（反思日志须回应）**：罗家德等（2026）《社会计算方法论》第1-2章（范式又一次转移 / 一切以理论为基础，锚定课程的人机交互姿态）；Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915), 721-723（计算社会科学的诞生宣言：新数据、新工具、新问题）

## 课后作业

> 本周不提交课程作业，以下为当堂未完成时的自查清单，确保环境就绪以支撑后续周次。

1. 按 `weeks/week01/setup.md` 补齐环境（当堂未装完的部分），验收六步截图（见 setup.md 末尾"安装顺序速查"）
2. 用 opencode 在项目根目录完成 `wb_explore.py`：用 wbgapi 拉取世界银行数据（自己选择国家与指标，至少 2 个指标、近 10 年），终端能跑通
3. 浏览 [世界银行指标](https://data.worldbank.org/indicator?tab=all)，选出 3-5 个与你自己研究方向相关的指标，记录指标代码
4. 写最简版 `AGENTS.md`（项目目标 + 技术栈 + 目录约定），后续随项目演进逐步完善
5. 写第一篇反思日志（模板见 `templates/reflection-log.md`，2-3 段即可）：回应对罗家德第1-2章或 Lazer (2009) 的阅读，写下你对"人判断、AI执行"姿态的初步理解与疑问
6. 自查留存：脚本代码 + 运行截图 + `AGENTS.md` + 环境验收截图 + 选定指标列表 + 反思日志（本周不提交，W3 阶段成果一检查时作为环境就绪与方法论锚定证据）

## 参考资料

- 理念：Wang, H. et al. (2023). "Scientific discovery in the age of artificial intelligence." *Nature*, 620, 47-60
- 方法论：罗家德、高馨、刘济帆、傅晓明. (2026). 《社会计算方法论：社会科学研究的一次范式转移》第1-2章. 清华大学出版社；Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915), 721-723
- 工具：[opencode 文档](https://opencode.ai/docs/)、[Cursor 文档](https://docs.cursor.com/)、[AGENTS.md 规则](https://opencode.ai/docs/zh-cn/rules/)
- 数据：[wbgapi PyPI](https://pypi.org/project/wbgapi/)、[世界银行指标浏览](https://data.worldbank.org/indicator)、[世界银行开发者文档](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386)
- 安装指南：`weeks/week01/setup.md`（Python 3.13 + Cursor + opencode 全流程，含排障）
- `weeks/week01/lecture.md`、`weeks/week01/lab.md`
