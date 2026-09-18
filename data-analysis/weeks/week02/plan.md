# Week 02 教学计划

## 主题

数据全景 + opencode

## 本周学习目标

- 能在 opencode 里选模型（默认免费即可；也可接入付费模型或 token plan）
- 能和全班一起用 opencode 分析 W1 公约问卷，并把课堂公约写进课程网站（改文件，不只对话）
- 能从生成、开放、成本、通道等维度说清一份数据（客观/合成/公开/私有/免费/付费等）
- 能用 opencode 采集西财要闻：本周交 Word 实验报告；数据和代码下周课堂邀请同学展示运行；不锁定选题

## 预计投入

课堂 3×45 分钟。课外 6-8h

## 教学内容

1. 收取已带到的 W1 互助小组协议纸质签字版（`templates/group-agreement.md`，全员签字）
2. opencode 安装、选模型、课堂公约
  - 安装配置（见 `weeks/week02/opencode-setup.md`）
  - 选模型：默认免费模型即可跟课；也可接入付费模型或 token plan
  - 用 opencode 分析 W1 公约问卷，讨论定稿后**改 `rules.html` 并更新课程网站**（不只对话；学生可跟做一部分，教师机改站点）
3. 数据生态概览 + 数据从哪来：先分享展示站产业新闻「数博会探寻数据要素价值释放新路径」，再白板口述多维分类（见 `weeks/week02/data-taxonomy.md`），不另做幻灯
4. 拉一次数据示范：用 opencode 全程对话生成 `.py`，当堂只抓西财新闻一页；具体代码下节课再学；课后继续拉，本周交 Word 实验报告

## 课堂演示工具


| 环节    | 工具                                                                        | 用法                                                                                    |
| ----- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 开场收协议 | W1 纸质互助小组协议                                                          | 按组收已带到的打印签字版（`templates/group-agreement.md`）                              |
| 现场主演示 | opencode（投影放大字号）                                                          | 教师在 **data-analysis-showcase** 根目录：选模型 → 分析问卷并改公约页 |
| 公约    | 课程展示站公约页                                                                  | 用 opencode 根据问卷改稿，当场更新到课程网站（W1 已预告）                                                   |
| 产业新闻  | [展示站新闻页](https://haichaozheng.github.io/data-analysis-showcase/news.html) | 数据分类前先分享「数博会探寻数据要素价值释放新路径」                                                            |
| 数据分类  | 白板（`weeks/week02/data-taxonomy.md`）                                       | 口述多维分类，不另做幻灯                                                                               |
| 拉数据   | opencode（生成 `.py`）                                                        | 全程对话生成脚本；当堂只抓西财新闻一页；具体代码下节课再学；课后继续拉，本周交 Word 实验报告；数据和代码下周课堂邀请同学展示运行 |
| 辅演示   | Trae                                                                      | 终端看不清或 opencode 装不上时，用同一问话在 Trae 里建文件；拉要闻这道作业必须用 opencode                         |
| 学生跟做  | opencode（装不上则 Trae 兜底）                                                    | 跟做生成抓一页的 `.py`          |


## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：教师机 opencode 可运行，**已在本地打开 `data-analysis-showcase` 仓库根目录**；终端字号放大；课程群发 `weeks/week02/opencode-setup.md`、`weeks/week02/opencode-class-norm-case.md`、`weeks/week02/data-taxonomy.md`、`weeks/week02/homework02-name-id.md`；**W1 公约问卷已收齐并做成可粘进 opencode 的汇总**（条数、分歧点即可）；展示站公约页能改；新闻页 [数博会一文](https://haichaozheng.github.io/data-analysis-showcase/news.html) 能打开。

**第1节 · 装 opencode + 公约（45 分钟）**

1. **收取已带到的互助小组协议纸质签字版**：按组交一份 W1 打印的 `templates/group-agreement.md`，须全员签字。没带来的记下，本周补交纸质版，不影响后面装 opencode。
2. **opencode 安装**：按 `weeks/week02/opencode-setup.md`：官网 LTS Node.js（24.x）→ `npm install -g opencode-ai` → `opencode --version`。教师投屏；学生跟做。装不上的先用 Trae，周末补齐，报错截图进群。课堂不装 WSL。PowerShell 若禁止运行 `npm.ps1`，用 `npm.cmd` 或把当前用户执行策略改为 `RemoteSigned`。
3. **初步使用 opencode（选模型 + 课堂公约）**：按 `weeks/week02/opencode-class-norm-case.md`。必须在**项目根目录**打开（不要在别的文件夹）。教师案例是 `data-analysis-showcase`。
  - **选模型**：界面里选一个即可。**默认免费模型可以跟课。** 有付费模型或 token plan 的可自行接入。
  - **课堂公约**（学生可以跟做一部分）：把 W1 问卷汇总交给 opencode，和同学一起分析讨论，形成课堂公约；接着让 opencode **直接改 `rules.html` 并更新课程网站**，不只停在对话。学生可跟做分析与改文件；教师机改站点并推送。

**第2节 · 数据全景（45 分钟）**

1. **产业新闻 + 数据从哪来**：先打开展示站 [产业新闻](https://haichaozheng.github.io/data-analysis-showcase/news.html)，和学生分享 **「数博会探寻数据要素价值释放新路径」**（高质量数据集、数据要素要流通才有用）。**不另做幻灯。** 白板口述多维分类（底稿 `weeks/week02/data-taxonomy.md`）：生成（客观 / 合成含仿真）、开放（公开 / 受限 / 私有）、成本（免费 / 付费）、通道（API / 下载 / 自己采集）、形态、时效、权属。同一份数据会落在多条轴上。接一句：产品要先找到能拿到、能用、能上线的数据。
2. **拉一次数据示范**：不当场拆 `requests` / 选择器。教师用 opencode **全程对话**生成一个 `.py`（说清：西财要闻、只要一页、写成文件并运行）。学生跟做同一问话，方便带走能跑的脚本。数据：[西财要闻](https://www.swufe.edu.cn/index/xcyw.htm)。**当堂只抓一页。** 点明：具体代码下节课再学；课后用同一办法继续拉。本周交 Word 实验报告；数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。`swufe-news.md` 留给课后对照，课堂上不逐步讲。

**第3节 · 作业说明与 journal（45 分钟）**

1. **西财要闻实验报告**：对照 `weeks/week02/homework02-name-id.md`。必须用 opencode + Cursor。本周交 Word；数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。在超星学习通提交，提交前检查内容，不要交错文件。
2. **继续倾听**：原话追加到同一份 `community.md`。W1 未满 3 条的本周必须补齐，最好补到 10 条。题目和方向可以换。
3. **写当天 `journal.md`**：按五格追加今天 1 条：今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录。互助只写谁帮了你、对项目有何影响，没有则写「无」。W3 建仓时拷到 `docs/journal.md`。

## 项目活动

**必做**

1. 课后作业：用 **opencode + Cursor** 采集 [西财要闻](https://www.swufe.edu.cn/index/xcyw.htm)。本周交 Word 实验报告（实验目标、opencode 过程截图、踩坑、解决经验、是否完成及条数、最初 10 条截图）。数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。见 `weeks/week02/homework02-name-id.md`
2. 继续倾听，原话追加到同一份 `community.md`（W1 未满 3 条的本周补齐，最好补到 10 条）

**进阶（可选）**

- 提前选修网页数据采集（`knowledge/phase1-1-4b-web-data-collection.md`，W4 正式引入）

**兜底**

- 数据源拉不通：记录失败原因，换 `project-selection-guide.md` §7 备选数据源
- opencode 装不上：带报错走课程群，周末补齐；采集西财新闻这道作业必须用 opencode
- 找不到或进不去场合 / 人和产品对不上：换 `community.md` 第 3 节备选或身边一个会反复聊这类事的场合（家里管钱的人、社团、实习点），须仍是你打算服务的人
- W1 互助小组协议未交纸质签字版：记下组名，本周补交，不影响已完成的装 opencode
- W1 社区调研未交齐：本周补满 ≥3 条原话，不另开一篇

## 交付物（评分锚点）

- 课后作业：西财要闻采集的 **Word 实验报告**（须用 opencode + Cursor 完成；数据和代码下周课堂邀请同学展示运行）

—— 规格与知识锚定见 milestones §1.2；计入平时成绩（形成性）。提交前自检：Word 报告含过程截图、条数与最初 10 条？文件名有姓名和学号？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。opencode 安装/数据源拉不通类问题直接走 ③ 并附截图。

## 课后任务

1. 熟练使用 opencode + Cursor（本周起作为项目工作流主工具）
2. 继续倾听，原话追加到同一份 `community.md`（W1 未满 3 条的本周补齐，最好补到 10 条）
3. 按 `weeks/week02/homework02-name-id.md` 交西财要闻 Word 实验报告

## 学习资料

- `weeks/week02/homework02-name-id.md`（本周 Word 实验报告模板）
- `weeks/week02/opencode-class-norm-case.md`（选模型、课堂公约）
- `weeks/week02/opencode-setup.md`（Node.js LTS + 全局安装 opencode；官网 [https://opencode.ai/）](https://opencode.ai/）)
- [opencode 规则：AGENTS.md 与 `/init](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)`
- `weeks/week02/swufe-news.md`（课后对照；当堂不拆讲。具体代码下节课再学）
- `weeks/week02/data-taxonomy.md`（第 2 节白板底稿）
- `knowledge/phase1-1-4-financial-data-ecosystem.md`
- `knowledge/phase1-1-4b-web-data-collection.md`（提前选修：网页数据采集 requests + crawl4ai + 爬虫合规；W4 正式引入，感兴趣的同学可提前学习）
- `knowledge/phase1-1-2-ai-assisted-coding.md`
- `knowledge/phase1-1-7-community-first.md`（社区先行）
- `knowledge/phase1-1-6-user-insight.md`（用户访谈技巧）
- `templates/journal.md`（按日填写）、`templates/journal-rules.md`（用途与交法）、`templates/community.md`（继续追加原话）
- 视频资料（超星学习通，详见 `video-resources.md`）：2.1 网络爬虫（进阶预习：配合网页数据采集提前选修，为 W4 正式引入打底）
