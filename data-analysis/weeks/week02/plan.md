# Week 02 教学计划

## 主题

数据全景 + opencode + 社区倾听延续

## 本周学习目标

- 能在 opencode 里选模型（默认免费即可；也可接入付费模型或 token plan），用 `/init` 生成 `AGENTS.md`，并在项目根目录新建 `requirements.md`、`design.md`、`scope.md`
- 能和全班一起用 opencode 分析 W1 公约问卷，并把课堂公约写进课程网站（改文件，不只对话）
- 能初始化个人项目仓库，放入上述四份文件与 `journal.md`、`community.md`，完成首次交互
- 能从生成、开放、成本、通道等维度说清一份数据（客观/合成/公开/私有/免费/付费等），并对照 `community.md` 里的候选方向评估数据分析来源（从哪来、能否拿到、怎么拿）；课后用 opencode 采集西财新闻，本周交 Word 实验报告，数据和代码下周展示，不锁定选题
- 能把 W1 已交的 `community.md` 迁入仓库；第 3 节先自读社区先行与用户访谈，再互查并补充调研（原话往下追加），核对「人 = 后续产品服务对象」

## 预计投入

课堂 3×45 分钟。课外 6-8h

## 教学内容

1. 收取 W1 互助小组协议纸质签字版（`templates/group-agreement.md`，全员签字；没带的本周补交）
2. opencode 初步使用
  - 安装配置（见 `weeks/week02/opencode-setup.md`）
  - 选模型：默认免费模型即可跟课；也可接入付费模型或 token plan
  - `**AGENTS.md**`：给 opencode 的项目规则（类似 Cursor 的规则）。写入后会进入模型上下文，让它按这个项目的方式工作。在根目录运行 `/init`：扫描项目并生成该文件；已有则会补充。空项目也可以直接让模型生成。**可以把 `journal.md` 的使用规则写进 `AGENTS.md`。** 提交进 Git。说明见 [opencode 规则 · 初始化](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)
  - 在项目根目录新建 `requirements.md`（用户需求）、`design.md`（系统技术设计）、`scope.md`（功能范围与开发工作安排）（教师案例：`data-analysis-showcase`）
  - 用 opencode 分析 W1 公约问卷，讨论定稿后**改 `rules.html` 并更新课程网站**（不只对话；学生可跟做一部分，教师机改站点）
3. 初始化个人项目仓库（四份文件骨架 + `journal.md` + W1 的 `community.md` + `.venv`；推远端为选做）
4. 数据生态概览 + 数据从哪来：先分享展示站产业新闻「数博会探寻数据要素价值释放新路径」，再白板口述多维分类（见 `weeks/week02/data-taxonomy.md`），不另做幻灯
5. 拉一次数据示范：用 opencode 全程对话生成 `.py`，当堂只抓西财新闻一页；具体代码下节课再学；课后继续拉，本周交 Word 实验报告
6. 第 3 节先自读 `knowledge/phase1-1-7-community-first.md`（社区先行）与 `knowledge/phase1-1-6-user-insight.md`（用户访谈），再小组互查 `community.md`（补充调研、评估数据来源；当堂不实拉、不锁定选题）

## 课堂演示工具


| 环节    | 工具                                                                        | 用法                                                                                    |
| ----- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 开场收协议 | W1 纸质互助小组协议                                                          | 第 1 节开头按组收打印签字版（`templates/group-agreement.md`）；没带的本周补交                              |
| 开场抽人  | 超星学习通课堂活动（选人 / 随机点名）                                                      | 课前建好活动；收完协议后抽人分享 `journal.md`                                                             |
| 现场主演示 | opencode（投影放大字号）                                                          | 教师在 **data-analysis-showcase** 根目录：选模型 → `/init` 生成 `AGENTS.md` → 新建另三份文件 → 分析问卷并改公约页 |
| 公约    | 课程展示站公约页                                                                  | 用 opencode 根据问卷改稿，当场更新到课程网站（W1 已预告）                                                   |
| 产业新闻  | [展示站新闻页](https://haichaozheng.github.io/data-analysis-showcase/news.html) | 数据分类前先分享「数博会探寻数据要素价值释放新路径」                                                            |
| 数据分类  | 白板（`weeks/week02/data-taxonomy.md`）                                       | 口述多维分类，不另做幻灯                                                                               |
| 拉数据   | opencode（生成 `.py`）                                                        | 全程对话生成脚本；当堂只抓西财新闻一页；具体代码下节课再学；课后继续拉，本周交 Word 实验报告；数据和代码下周展示 |
| 第 3 节自读 | `knowledge/phase1-1-7-community-first.md`、`knowledge/phase1-1-6-user-insight.md` | 学生自己先读，不讲幻灯；读完再互查 `community.md`                                              |
| 互查    | 仓库内 `community.md`                                                         | 小组互查：对照刚读的两份材料补调研 + 用多维分类评估候选方向的数据来源                                          |
| 辅演示   | Trae                                                                      | 终端看不清或 opencode 装不上时，用同一问话在 Trae 里建文件；拉要闻这道作业必须用 opencode                         |
| 学生跟做  | opencode（装不上则 Trae 兜底）                                                    | 第 1 节在自己的项目根目录新建四份文件；第 2 节跟做生成抓一页的 `.py`；第 3 节先自读再互查 `community.md`          |


## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：教师机 opencode 可运行，**已在本地打开 `data-analysis-showcase` 仓库根目录**；终端字号放大；课程群发 `weeks/week02/venv-setup.md`、`weeks/week02/opencode-setup.md`、`weeks/week02/opencode-class-norm-case.md`、`weeks/week02/data-taxonomy.md`、`weeks/week02/swufe-news.md`、`knowledge/phase1-1-7-community-first.md` 与 `knowledge/phase1-1-6-user-insight.md`；**超星学习通已建好课堂活动（选人 / 随机点名），课上直接开**；学生带着 W1 写好的 `journal.md`、`community.md`（仓库本周才建），以及 **W1 打印、全员签字的互助小组协议纸质版**（`templates/group-agreement.md`）；**W1 公约问卷已收齐并做成可粘进 opencode 的汇总**（条数、分歧点即可）；展示站公约页能改；新闻页 [数博会一文](https://haichaozheng.github.io/data-analysis-showcase/news.html) 能打开。

**第1节 · 交协议 + 分享 journal + 装 opencode（45 分钟）**

1. **提交互助小组协议纸质签字版（5 分钟）**：开场先收 W1 布置的 `templates/group-agreement.md` 打印件，须全员签字。按组交一份，教师清点组名与人数。没带来的记下，本周补交纸质版，不影响后面装 opencode、建仓。
2. **超星抽人分享 journal.md（10 分钟）**：打开超星课堂活动，随机抽取同学分享上周 `journal.md`（3 问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点）。抽到的同学打开自己的文件口述或投屏；没写的换下一位，不占用讲解。点明本周目标：先会用 opencode，再把文件放进个人仓库；第 3 节先自读两份材料，再互查 `community.md`、评估数据来源，不锁定题目。
3. **opencode 安装（10 分钟）**：分享结束后立刻装。按 `weeks/week02/opencode-setup.md`：官网 LTS Node.js（24.x）→ `npm install -g opencode-ai` → `opencode --version`。教师投屏；学生跟做。装不上的先用 Trae，周末补齐，报错截图进群。课堂不装 WSL。
4. **初步使用 opencode（20 分钟）**：按 `weeks/week02/opencode-class-norm-case.md`。必须在**项目根目录**打开（不要在别的文件夹）。教师案例是 `data-analysis-showcase`。连着做：
  - **选模型**：界面里选一个即可。**默认免费模型可以跟课。** 有付费模型或 token plan 的可自行接入。
  - `**AGENTS.md**`：先说清作用——它是给 opencode 的项目规则，内容会进入模型上下文，用来按本项目定制行为（类似 Cursor 的规则）。然后在根目录运行 `**/init**`：扫描项目并生成 `AGENTS.md`；已有文件则补充。**空项目也可以直接让模型生成 `AGENTS.md`。** 也可以把 `journal.md` 的使用规则写进去。生成后提交进 Git。
  - **另三份文件**：让 opencode 在根目录生成 `requirements.md`、`design.md`、`scope.md`。requirements 为项目用户需求，design 为系统技术设计，scope 为系统功能范围与开发工作安排。可按自己的项目补充内容。
  - **课堂公约**（学生可以跟做一部分）：把 W1 问卷汇总交给 opencode，和同学一起分析讨论，形成课堂公约；接着让 opencode **直接改 `rules.html` 并更新课程网站**，不只停在对话。学生可跟做分析与改文件；教师机改站点并推送。

**第2节 · 仓库收口 + 数据全景（45 分钟）**

1. **个人仓库收口（15 分钟）**：在自己的项目根目录做完迁入记录和建 `.venv`。教师一步一停。第 1 节已有 `AGENTS.md` 等文件的，不要重做；缺的当场补。装不上环境的先完成拷文件，`.venv` 按 `venv-setup.md` 周末补。
  - **迁入两份记录**：把 W1 写好的 `journal.md`（没有则从 `templates/journal.md` 拷入并贴上 W1 那条）和已填的 `community.md` 放到仓库根目录。仍是这两份文件，不要另开一篇。
  - **建 `.venv`**：按 `weeks/week02/venv-setup.md`。先问 opencode 虚拟环境有什么用，再用 `python -m venv .venv`；`.gitignore` 写入 `.venv/`。点明一句：W1 的系统 Python 只负责「电脑上有解释器」；个人项目的包装进 `.venv`，装包、部署都靠它。
  - **推到远端（选做）**：`git add`（不要加 `.venv`）→ 提交 → 推到 GitHub/Gitee。若做了：仓库链接能打开；根目录有 `journal.md`、`community.md`；远端看不到 `.venv` 文件夹。
2. **产业新闻 + 数据从哪来（15 分钟）**：先打开展示站 [产业新闻](https://haichaozheng.github.io/data-analysis-showcase/news.html)，和学生分享 **「数博会探寻数据要素价值释放新路径」**（高质量数据集、数据要素要流通才有用）。**不另做幻灯。** 白板口述多维分类（底稿 `weeks/week02/data-taxonomy.md`）：生成（客观 / 合成含仿真）、开放（公开 / 受限 / 私有）、成本（免费 / 付费）、通道（API / 下载 / 自己采集）、形态、时效、权属。同一份数据会落在多条轴上。接一句：产品要先找到能拿到、能用、能上线的数据。
3. **拉一次数据示范（15 分钟）**：不当场拆 `requests` / 选择器。教师用 opencode **全程对话**生成一个 `.py`（说清：西财要闻、只要一页、写成文件并运行）。学生跟做同一问话，方便带走能跑的脚本。数据：[西财要闻](https://www.swufe.edu.cn/index/xcyw.htm)。**当堂只抓一页。** 点明：具体代码下节课再学；课后用同一办法继续拉。本周交 Word 实验报告；数据和代码下周课堂展示，本周作业不交这两样。必间隔请求、不要并行。`swufe-news.md` 留给课后对照，课堂上不逐步讲。

**第3节 · 先读再互查（45 分钟）**

1. **自己先读（15 分钟）**：每人打开 `knowledge/phase1-1-7-community-first.md`（社区先行）和 `knowledge/phase1-1-6-user-insight.md`（用户访谈）。教师不讲幻灯。读完能说出：为什么先听社区再写产品；访谈不要问「你要不要这个功能」。
2. **小组互查 community.md（20 分钟）**：两人一组（或同组），打开对方已拷进仓库的 `community.md`（W1 未交齐的当场对着模板补）。对照刚读的两份材料看：第 4 节是否 ≥3 条原话（本周最好补到 10 条）；第 5 节用户是否从这些原话里抽出来的。对不上的当场改第 1 节场合或第 5 节用户，并约定本周补听、往表里追加一行。接着对照第 1 节的候选方向，用第 2 节的多维分类（`weeks/week02/data-taxonomy.md`）评估「若做成数据分析产品，数据从哪来」：公开还是要自己采、免费还是付费、网页 / API / 原话本身——说清来源与拿法即可，当堂不要求把数据拉下来，也不锁定选题。
3. **收束（10 分钟）**：布置课后作业（用 opencode 采集西财新闻，交 Word 实验报告；数据和代码下周展示）。两份材料没读完的课后看完。技能小练见 `lab.md`。提醒：本周起项目工作流主工具是 opencode + Cursor（Trae 亦可）。继续倾听，原话追加到同一份 `community.md`（最好补到 10 条）；**下周课堂分享，会查看补充或更新的内容，题目和方向可以换。** 当日在 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）。互助记录只写「谁帮了你、对项目有何影响」，没有则写「无」。

## 项目活动

**必做**

1. 初始化个人项目仓库：在项目根目录用 opencode 新建 `AGENTS.md`、`requirements.md`、`design.md`、`scope.md`（骨架即可），并把 `templates/journal.md` 与 W1 的 `community.md` 复制到仓库根目录；`git init` 后按 `weeks/week02/venv-setup.md` 建 `.venv`（`.venv/` 勿提交）。推到 GitHub/Gitee 为选做
2. 把 W1 社区调研迁入仓库：互查并补充 `community.md`（人 = 后续产品计划服务的人；原话追加到同一份）。对照候选方向评估数据分析来源（从哪来、能否拿到、怎么拿），不锁定选题。入社区即选题探索，W3 收敛方向。W1 未交齐的本周补进仓库
3. 课后作业：用 **opencode** 采集 [西财要闻](https://www.swufe.edu.cn/index/xcyw.htm)（当堂一页、课后继续）。本周交 Word 实验报告（实验目标、opencode 过程截图、踩坑、解决经验、是否完成及条数、最初 10 条截图）。数据和代码下周课堂展示，本周作业不交这两样。每请求间隔，不要并行

**进阶（可选）**

- 提前选修网页数据采集（`knowledge/phase1-1-4b-web-data-collection.md`，W4 正式引入）

**兜底**

- 数据源拉不通：记录失败原因，换 `project-selection-guide.md` §7 备选数据源
- opencode 装不上：带报错走课程群，第 3 节互查与评估来源不依赖它；四份工作流文件可先用 Trae；采集西财新闻这道作业必须用 opencode，周末补齐再交
- 找不到或进不去场合 / 人和产品对不上：换 `community.md` 第 3 节备选或身边一个会反复聊这类事的场合（家里管钱的人、社团、实习点），须仍是你打算服务的人
- W1 互助小组协议未交纸质签字版：记下组名，本周补交，不影响装 opencode、建仓
- W1 社区调研未交齐：本周拷入仓库时补满 ≥3 条原话，不另开一篇

## 交付物（评分锚点）

- 个人赛道意向（含候选方向、当堂数据来源评估；社区倾听见仓库内 `community.md`，不另写一份）
- 个人项目仓库（含 `AGENTS.md`、`requirements.md`、`design.md`、`scope.md` 骨架、journal.md、`community.md`；推远端为选做）
- 课后作业：西财新闻采集的 **Word 实验报告**（须用 opencode 完成；数据和代码下周展示）

—— 规格与知识锚定见 milestones §1.2；计入平时成绩（形成性）。提交前自检：对照 `community.md` 候选方向，≥2 个数据源写清从哪来、怎么拿？仓库内 `community.md` 有 ≥3 条原话且人和产品对得上？根目录有四份工作流文件骨架？Word 报告含过程截图、条数与最初 10 条？本地有 `.venv` 且未提交该文件夹？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。opencode 安装/数据源拉不通类问题直接走 ③ 并附截图。

## 课后任务

1. 熟练使用 opencode + Cursor（本周起作为项目工作流主工具）
2. 继续倾听，原话追加到仓库内 `community.md`（W1 未满 3 条的本周补齐，最好补到 10 条）。下周课堂分享：教师查看补充或更新的内容；题目和方向可以换
3. 第 3 节两份材料没读完的课后看完：`knowledge/phase1-1-7-community-first.md`、`knowledge/phase1-1-6-user-insight.md`

## 学习资料

- `weeks/week02/opencode-class-norm-case.md`（第 1 节跟做：选模型、`/init`、三份工作流文件、课堂公约）
- `weeks/week02/opencode-setup.md`（Node.js LTS + 全局安装 opencode；官网 [https://opencode.ai/）](https://opencode.ai/）)
- [opencode 规则：AGENTS.md 与 `/init](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)`
- `weeks/week02/swufe-news.md`（课后对照；当堂不拆讲。具体代码下节课再学）
- `weeks/week02/data-taxonomy.md`（第 2 节白板底稿；第 3 节评估数据来源时对照）
- `weeks/week02/venv-setup.md`（先问 opencode 虚拟环境是什么；本课用 `python -m venv .venv`）
- `knowledge/phase1-1-4-financial-data-ecosystem.md`
- `knowledge/phase1-1-4b-web-data-collection.md`（提前选修：网页数据采集 requests + crawl4ai + 爬虫合规；W4 正式引入，感兴趣的同学可提前学习）
- `knowledge/phase1-1-2-ai-assisted-coding.md`
- `knowledge/phase1-1-7-community-first.md`（第 3 节当堂自读：社区先行）
- `knowledge/phase1-1-6-user-insight.md`（第 3 节当堂自读：用户访谈技巧）
- `templates/AGENTS.md`、`templates/requirements.md`、`templates/design.md`、`templates/scope.md`（课堂用 opencode 在根目录生成骨架，对照模板）；`templates/journal.md`（复制到仓库根目录按日填写）、`templates/journal-rules.md`（用途与交法）、`templates/community.md`（W1 已交全文迁入后继续追加）
- 视频资料（超星学习通，详见 `video-resources.md`）：2.1 网络爬虫（进阶预习：配合网页数据采集提前选修，为 W4 正式引入打底）

