# Week 01 教学计划

## 本周主题

工具准备 — AI工作环境搭建（AI4S范式入门）

> Phase 1: Foundation 第1周。本周是整门课的起点：不是"装软件"，而是为 AI4S 科研全流程奠定工具基础，并建立"人判断、AI执行"的人机交互姿态。

## 学习目标

- 能用自己的话说明 AI4S 范式：AI 贯穿科研全流程，是"研究伙伴"而非工具箱
- 能配置好 AI 工作环境：Python 3.13 + Cursor（选中解释器）+ opencode（项目根目录打开、选模型、基础命令）
- 能说明 opencode 的工作模式：**对话→改文件→运行**，区别于网页版 Chat 只停在对话
- 能写最简版 `AGENTS.md`，让 opencode 读取作为项目上下文
- 能用 opencode 在真实文本数据上生成并运行第一个 Prompt 驱动的科研脚本，验证环境可用
- 能说明社科科研全流程的五个环节，并把 AI4S 工具栈映射到每个环节

## 教学步骤（3节课）

> 第一节课带电脑的同学少：第 1、2 节以**讲授 + 教师投屏演示**为主，学生观察、记录疑问；第 3 节改为**分组实验**（3-4 人一组，共享电脑，轮流操作）。个人动手实验全部放到课后练习（不需要提交作业，见文末）。

**第1节 · 范式定向与案例预演（45 分钟，不要求操作）**

1. 开场（5 分钟）：点明学期终点——围绕个人科研项目构建 AI4S 工具栈并产出科研成果（论文 + 工具栈仓库）
2. AI4S 范式讲解（15 分钟）：AI4S 不是"用 AI 写代码"，而是用 AI 重构科研全流程；人机交互姿态（人判断、AI 执行）；以"大模型 vs 传统方法"的同题对比为例，第一周就建立"方法选择是研究者的判断、结论可信度须可核验"的方法论意识
3. 社科科研全流程映射（10 分钟）：文献→选题→设计→实施→写作五模块，对应 9 周课程安排
4. W1 案例预演（教师投屏，10 分钟）：运行 `weeks/week01/case-nlp/app.py`（Streamlit），演示"光线传媒股吧情感分析"主线——12.4 万条股吧评论：词典法 vs LLM 法情感打分（Part 3 / Part 4，重点看"利好出尽""割韭菜"等反讽、行情黑话评论上两类方法的分歧）→ 每日情绪曲线（Part 5）→ 情绪与股价相关性（Part 6）。学生只观察并记下一个疑问：同一批文本，两种方法为何结论不同？
5. 个人科研项目启动（5 分钟）：每位博士生在便签上写研究方向关键词 + 1 个痛点。💡 课堂互动：随机抽取 3-4 位同学投屏分享研究方向与痛点

**第2节 · 工具环境搭建演示（45 分钟，教师投屏，学生观察记录）**

> 课前把 `weeks/week01/setup.md` 发到课程群，学生课后按它自行安装。本节教师投屏完整走一遍流程，学生对照文档观察、记录自己课后安装时最容易卡住的步骤。

6. **Python 3.13 + Cursor 安装流程演示（15 分钟）**：按 `weeks/week01/setup.md` 第一、二部分投屏走一遍——官网装 3.13（**不装 Anaconda、不点官网首页 3.14**）；终端 `python --version` 验收（须为 3.13.x）；Cursor 里 `Ctrl+Shift+P → Python: Select Interpreter` 选路径里有 `Python313` 的，不要选 Anaconda、不要选 WindowsApps 商店别名；`pip install pandas jieba` 装包（数据分析 + 中文分词，正是 case-nlp 案例的两个依赖）。
7. **opencode 安装与基础用法演示（15 分钟）**：按 `weeks/week01/setup.md` 第三部分投屏走一遍——官网 LTS Node.js（24.x）→ `npm install -g opencode-ai` → `opencode --version`。在项目根目录输入 `opencode` 启动 TUI；选模型（默认免费可跟课）；演示 `/connect` `/model` `/session` `/compact` 四条命令。点明 opencode 的工作模式：**对话→改文件→运行**，不是网页版 Chat 那样只停在对话。
8. **第一个 Prompt 驱动脚本演示（10 分钟）**：直接接第1节的案例——让 opencode 读 `case-nlp/cleaned_300251_comments.csv`（12.4 万条股吧评论），现场生成 `mini_emotion.py`：统计"韭菜""利好""崩盘""涨停"等关键词各出现多少条、最集中在哪一年，**点运行且终端无报错**。结果印证第1节的观察：「涨停」6606 条集中在 2015、「韭菜」集中在 2018——同一批文本，不同的关键词规则给出不同的"情绪"图景，这正是词典法 vs LLM 法分歧的根源。参考/兜底脚本：`weeks/week01/case-nlp/mini_emotion.py`。
9. **AGENTS.md 说明（5 分钟）**：展示最简版 `AGENTS.md`（3-5 行：项目目标、技术栈、目录约定），说明 opencode 打开时自动读取它作为项目上下文——这就是"在项目根目录打开"的原因。

**第3节 · 课堂实验与课后任务布置（45 分钟，分组实验）**

> 分组实验：3-4 人一组，每组至少 1 台电脑（课前协调带电脑的同学拼组，教师备 1-2 台备用机）。组内轮流操作、共同观察记录，目标是"感受一次"，不是人人跑通——人人跑通放在课后练习。

10. **分组实验一：同题不同问（15 分钟）**：任务相同——让 opencode 读 `case-nlp/cleaned_300251_comments.csv`，统计"韭菜""利好""崩盘""涨停"关键词的分布。一半小组用模糊问法（"帮我分析一下这些股吧评论"），一半小组用明确问法（指定文件路径、date/comment 两列、按年分组、输出格式）。各组运行后对比：哪次输出更接近想要的？清楚在哪？教师收拢归纳三条经验——**说清楚要什么、给足上下文、给足约束**，从体验中带出，不先讲术语。
11. **分组实验二：让 AI 改脚本（10 分钟）**：各组接着让 opencode 把脚本改成词典法每日情绪分数——从 `zhang_unformal_pos.txt` / `zhang_unformal_neg.txt` 读入正负词典（与第1节 app.py Part 3 词典法是同一份），用 jieba 分词打分，按日汇总输出，与 Part 5"每日情绪曲线"直接呼应。分词打分约 1-2 分钟，等待时组内讨论。组内一人键入、其他人盯终端输出并记一句发现。卡住顺序：**问 AI（附报错）→ 组内互助 → 举手教师**。这是"对话→改文件→运行"闭环的亲身体验，也是后续科研编程（W2 检索脚本、W6 数据清洗、W8 论文起草）的工作模式底座。参考/兜底脚本：`case-nlp/daily_sentiment.py`。
12. **课后任务布置（12 分钟）**：逐条过文末"课后练习"清单——环境安装验收、改造课上脚本（换成自己研究方向的文本与关键词）、写最简版 `AGENTS.md`；推荐实验：打开 `weeks/week01/case-nlp/week01-nlp-lab.ipynb` 亲手做一遍"分词→词典法 vs LLM 法情感打分→情绪曲线→情绪与股价相关性"，回应第1节留下的疑问"同一批文本，两种方法为何结论不同"。写明课后求助顺序：**问 AI（附报错）→ 同学互助 → 课程群提问**。
13. **下周铺垫（6 分钟）**：文献检索是方法论（PRISMA 流程），不是"搜一下"；预告 W2 检索式与学术 API。本周"对话→改文件→运行"的工作模式就是下周写检索脚本的基础。
14. **收束（2 分钟）**：课后练习不需要提交作业，但 W2 课前须环境就绪，否则下周跟不动检索脚本。

## 交付物

- **工具环境就绪**（评分锚点，对应 milestones §1.1）
  - opencode/cursor 可正常运行（`opencode --version` 截图 + Cursor 选中 Python313 截图）
  - Python 环境配置完成（`python --version` 为 3.13.x）
  - pandas + jieba 安装成功（`pip install pandas jieba` 无报错）
  - API key 配置完成（opencode 至少能连一个模型；默认免费模型也算）
  - 文献管理工具安装完成（Zotero 或同类）
  - 至少一个 Prompt 驱动的小脚本，能运行、终端无报错（课上分组实验生成的 `mini_emotion.py`，或课后改造版，均可）
  - 最简版 `AGENTS.md`（项目目标 + 技术栈 + 目录约定，3-5 行起步）
- 方法论锚定：体现 AI4S 范式理解、Prompt Engineering 初步应用、工具选择意识（说明选择了 opencode/cursor 还是其他、为什么）

## 课后自学

- **环境安装**：`weeks/week01/setup.md`（Python 3.13 + Cursor + opencode，课后按此安装，见课后练习）
- Prompt Engineering 方法论：`knowledge/m1-3-prompt-engineering.md`
- AI4S 范式与方法论：`knowledge/m1-1-ai4s-paradigm.md`
- 社科科研全流程映射：`knowledge/m1-4-research-workflow-mapping.md`
- AI 辅助编程（opencode/cursor）：`knowledge/m1-2-ai-coding.md`
- opencode 规则：[AGENTS.md 与 `/init`](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)
- **方法论阅读（反思日志须回应）**：罗家德等（2026）《社会计算方法论》第1-2章（范式又一次转移 / 一切以理论为基础，锚定课程的人机交互姿态）；Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915), 721-723（计算社会科学的诞生宣言：新数据、新工具、新问题）

## 课后练习

> 本周不需要提交作业。第一节未安排当堂操作，以下实验任务请课后完成，确保 W2 课前环境就绪。

1. 按 `weeks/week01/setup.md` 完成环境安装（Python 3.13 + Cursor + opencode + Zotero 或同类文献管理工具，W2/W3 用到），验收六步截图（见 setup.md 末尾"安装顺序速查"）
2. 用 opencode 对课上脚本做一处自己的改造：换 3-5 个与你研究方向相关的关键词（或改按小时/星期统计发帖高峰），终端跑通并截图
3. 写最简版 `AGENTS.md`（项目目标 + 技术栈 + 目录约定），后续随项目演进逐步完善
4. 推荐实验（约 80-110 分钟）：打开 `weeks/week01/case-nlp/week01-nlp-lab.ipynb`，亲手做一遍"分词 → 词频 → 词典法 vs LLM 法情感打分 → 每日情绪曲线 → 情绪与股价相关性"，回应第1节课堂演示留下的疑问：同一批股吧文本，两种方法为何结论不同？
5. 写第一篇反思日志（模板见 `templates/reflection-log.md`，2-3 段即可）：回应对罗家德第1-2章或 Lazer (2009) 的阅读，写下你对"人判断、AI执行"姿态的初步理解与疑问
6. 自查留存：脚本代码 + 运行截图 + `AGENTS.md` + 环境验收截图 + 反思日志（本周不提交，W3 文献综述交付检查时作为环境就绪与方法论锚定证据）

## 参考资料

- 理念：Wang, H. et al. (2023). "Scientific discovery in the age of artificial intelligence." *Nature*, 620, 47-60
- 方法论：罗家德、高馨、刘济帆、傅晓明. (2026). 《社会计算方法论：社会科学研究的一次范式转移》第1-2章. 清华大学出版社；Lazer, D. et al. (2009). "Computational Social Science." *Science*, 323(5915), 721-723
- 工具：[opencode 文档](https://opencode.ai/docs/)、[Cursor 文档](https://docs.cursor.com/)、[AGENTS.md 规则](https://opencode.ai/docs/zh-cn/rules/)
- 数据：`weeks/week01/case-nlp/`（光线传媒股吧评论 + tushare 日线行情，W9 的 NLP 实验会再用到）
- 安装指南：`weeks/week01/setup.md`（Python 3.13 + Cursor + opencode 全流程，含排障）
- `weeks/week01/lecture.md`、`weeks/week01/lab.md`
