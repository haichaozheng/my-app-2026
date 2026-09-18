# Week 03 教学计划

## 主题
项目基本文档、虚拟环境、社区互查、数据采集与项目提案

## 本周学习目标

- 能补交 W2 未交的互助小组协议；能在个人仓库备齐基本文档：根目录 `AGENTS.md`，其余进 `docs/`（`docs/journal.md`、`docs/requirements.md`、`docs/design.md`、`docs/scope.md`，并迁入 `docs/community.md`）；能按本课约定建 `.venv`（写入 `.gitignore`，勿提交该文件夹）
- 能自读社区先行与用户访谈，互查 `community.md`（原话、用户是否对得上），并评估数据从哪来
- 能对照西财要闻采集，说出 `requests` 拿 HTML、`BeautifulSoup` 拆字段；能当场展示或对照跑通自己的脚本
- 能用社区倾听记录与 ≥1 次用户访谈区分"假设的问题"与"验证的问题"，说清痛点发现路径
- 能用 Deep Research 对痛点真实性做交叉验证，筛掉无真实需求的方向
- 能用 Andrew Ng 界定范围的五步（业务问题 → 多种方案 → 可行性与价值 → 里程碑 → 资源预算）对照选题准入清单 8 项，写出通过过审的项目提案；「不做」清单必写
- 能对照 Hevner 七指导原则，把 Idea 阶段的决定与缺口写入 `docs/journal.md`（本周交全文为选做；课堂仍记 1 条）

## 预计投入

课堂 3×45 分钟。课外 8-10h

## 教学内容
1. 补交 W2 未交的互助小组协议纸质签字版
2. 超星抽人分享 `journal.md`
3. 项目基本文档落地：根目录只放 `AGENTS.md`；`docs/` 备齐 `journal.md`、`requirements.md`、`design.md`、`scope.md`；鼓励对照 `references/The Founder's Playbook.pdf`（持久上下文、规格与范围）
4. 迁入 `docs/community.md`
5. 个人项目建 `.venv`（第 1 节；跟做 `weeks/week03/venv-setup.md`）
6. 当堂自读 `knowledge/phase1-1-7-community-first.md`（社区先行）与 `knowledge/phase1-1-6-user-insight.md`（用户访谈），再筛痛点、Deep Research、对照准入清单写 `requirements.md` 第一节（第 2 节）
7. 数据采集：`requests` + `BeautifulSoup`（第 3 节开篇：Coding AI Is the New Literacy；西财要闻同学展示运行，对照 `weeks/week03/swufe-news.md`）

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| 补交协议 | W1 纸质互助小组协议 | 第 1 节开场只收 **W2 未交**的组（`templates/group-agreement.md`） |
| 开场抽人 | 超星学习通课堂活动（选人 / 随机点名） | 第 1 节抽人分享 `journal.md` |
| 项目基本文档 | opencode + 个人仓库根目录 | 第 1 节：根目录 `AGENTS.md`；`docs/` 备齐 `journal.md`、`requirements.md`、`design.md`、`scope.md`，迁入 `community.md`；已有的不重做。对照 `references/The Founder's Playbook.pdf` |
| 虚拟环境 | 个人项目根目录 + `.venv` | 第 1 节按 `weeks/week03/venv-setup.md` 建环境；`.gitignore` 写入 `.venv/` |
| 自读 | `knowledge/phase1-1-7-community-first.md`、`knowledge/phase1-1-6-user-insight.md` | 第 2 节学生自己先读，不讲幻灯 |
| 痛点与提案 | `docs/community.md` + `project-selection-guide.md` §8 + workbuddy **产品战略团队** + `templates/requirements.md` | 第 2 节：邻座判验证/假设 → 投影 Ng 五步与准入 8 项 → 教师用 workbuddy「产品战略团队」演示交叉验证 → 收束同一轮改 `docs/` 下 community / journal / requirements |
| 数据采集 | Andrew Ng 导论 + 学生西财要闻脚本 + `weeks/week03/swufe-news.md` | 第 3 节开篇投影 *Coding AI Is the New Literacy*；再邀请同学展示运行；点明 `requests` 拿 HTML、`BeautifulSoup` 拆字段 |
| 辅 | Trae / TraeWork | 只示范如何把访谈记录与社区原话写进提案；TraeWork 可作 workbuddy 的备选调研工具，不新开编程课 |
| 不做 | 全班开 Jupyter / Streamlit | 第 3 节只展示采集脚本，不要求每人打开笔记本；本周无新的代码作业 |

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。

课前：教师机 opencode、workbuddy「产品战略团队」可打开（否则 TraeWork）；超星抽人已建；带着 W2 未交协议名单；合格/不合格提案各 1 份（隐去姓名）。学生带 `journal.md`、`community.md`（第 1 节拷进 `docs/`）、西财要闻代码和数据。其余材料见文末「学习资料」。

**第1节 · 项目基本文档与虚拟环境（45 分钟）**

**`AGENTS.md` 必须在根目录**（opencode / Cursor 读这一层）。其余文档进新建的 `docs/`：`docs/journal.md`、`docs/requirements.md`、`docs/design.md`、`docs/scope.md`。对应 Playbook 的说法：给 AI 留持久上下文（规格、架构决定、范围），不要每次对话从头解释项目。鼓励课外读 `references/The Founder's Playbook.pdf`（可读摘录：`references/the-founders-playbook.md`，尤其 MVP 阶段「persistent context」、`CLAUDE.md` / 规格 / 书面 scope）。本课里：`AGENTS.md` 相当于项目规则（类似 CLAUDE.md）；`docs/requirements.md` / `docs/design.md` 是规格与架构；`docs/scope.md` 写清做什么、不做什么；`docs/journal.md` 记下决定，避免下一轮对话把项目做飘。`.venv` 在文档落地后单独建，不和写文档混在一轮对话里。必须在**项目根目录**打开 opencode，不要在 `docs/` 里打开。

1. **补交互助小组协议纸质签字版（5 分钟）**：只收 W2 未交的组。打印件为 `templates/group-agreement.md`，须全员签字。按组交一份，教师清点组名与人数。已交的组不重复交。没带的记下，本周内补交纸质版，不影响后面跟做文件。
2. **超星抽人分享 journal.md（8 分钟）**：打开超星课堂活动，随机抽取同学分享（3 问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点）。抽到的同学打开自己的文件口述或投屏；没写的换下一位，不占用讲解。点明：`journal.md` 全学期共用一份、按日追加。本周拷进 `docs/journal.md`，不要放根目录。
3. **落地五份基本文档（15 分钟）**：必须在**项目根目录**打开 opencode（不要在 `docs/` 里打开）。`docs/` 让 opencode 建，不要自己 mkdir。已有的不重做，缺的当场补。跟做 `weeks/week03/opencode-workflow-files.md`。
  - **`docs/journal.md`**：让 opencode 建 `docs/`（没有就建），把已写的日志写入 `docs/journal.md`（没有则从 `templates/journal.md` 拷入并贴上已有条目）。仍是这一份，不要另开一篇。
  - **`AGENTS.md`（根目录）**：给 opencode 的项目规则，内容会进入模型上下文（类似 Cursor 的规则，也类似 Playbook 里的 CLAUDE.md）。**只这一份留在根目录。** 根目录运行 `/init`：扫描项目并生成；已有则补充。空项目也可以直接让模型生成。可以把 `docs/journal.md` 的使用规则写进去。生成后提交进 Git。
  - **`docs/requirements.md` / `docs/design.md` / `docs/scope.md`**：让 opencode 建 `docs/`（没有就建）并生成骨架（不要放根目录）。requirements 为用户需求，design 为系统技术设计，scope 为功能范围与开发工作安排（本期做什么、不做什么）。可按自己的项目补。
4. **迁入 community.md（7 分钟）**：让 opencode 把已填的 `community.md` 放到 `docs/community.md`（没有 `docs/` 就先建），仍是这一份。推远端为选做（不要加 `.venv`）。
5. **建 `.venv`（10 分钟）**：独立一块，不和第 1 节文档混在一起。第 1 节文档落地后，按 `weeks/week03/venv-setup.md` 在项目根目录建 `.venv`；`.gitignore` 写入 `.venv/`。装不上的记下，周末补。推远端不要加 `.venv`。

**第2节 · 用户需求痛点分析（45 分钟）**

读完社区先行 / 用户访谈，立刻筛痛点；接着用 Ng 五步对照准入 8 项，再用 workbuddy「产品战略团队」做可行性与价值的交叉验证；收束时同一轮改 `docs/` 下三份：`community.md`、`journal.md`、`requirements.md`。互查并入痛点筛选（对照 `docs/community.md` 原话），不另开一块。

1. **自己先读（8 分钟）**：每人打开 `knowledge/phase1-1-7-community-first.md`（社区先行）和 `knowledge/phase1-1-6-user-insight.md`（用户访谈）。教师不讲幻灯。读完能说出：为什么先听社区再写产品；访谈不要问「你要不要这个功能」。点一句：倾听已经听到原话；访谈是课后补充调研，用来加深、拓展，不当堂另开一份。没读完的课后看完。
2. **痛点筛选（8 分钟）**：打开自己的 `docs/community.md`（W1 未交齐的当场对着模板补）。每人用一句话写当前痛点（谁、在什么场合、卡在哪；不要写产品名）。邻座对照刚读材料和对方原话判断：验证的 / 仍是假设。对不上的当场改句子或记下本周补听。顺带看数据从哪来（`weeks/week02/data-taxonomy.md`：公开还是要自己采），说清来源即可。互助小组不是用户社区。
3. **准入清单 + Andrew Ng 五步（8 分钟）**：本课过审看 `project-selection-guide.md` 第 8 节 8 项；怎么把想法收小看 Andrew Ng *How to Build Your Career in AI* 第 4 章（摘录 `references/build-career-in-ai-era.md`，PDF 文件名 `references/build caree in AI era.pdf`）。先点明：Ng 给的是**界定范围的五步**，不是打分表；8 项是本课硬门槛，缺一项须调整或重选。投影时按五步讲，每步立刻对上 8 项里相关的几条。
  - **① 先找业务问题，不是 AI 问题**：问「谁、哪三件事变好、现在为什么不行」。对清单 **2 用户、3 痛点**。痛点须来自 `docs/community.md` 原话，不要先写「我要做 RAG」。
  - **② 再头脑风暴多种方案**：不要一兴奋就做第一个功能；有时没有合适的 AI 方案也可以接受。对清单 **4 AI 功能**：RAG 或 LLM 解读必须扛痛点，不是套壳。
  - **③ 评估可行性（feasibility）和价值（value）**：可行性看能否免费拿到数据、12 周一人能否做完、技术是否现学现用；价值问领域里的人（本课即社区用户）。提案里**至少就可行性、价值这两项写出论证**（不要空喊「很有意义」）。对清单 **1 数据源、2–3 用户与痛点**。下一格用 workbuddy **产品战略团队** 做这一步的网上旁证。
  - **④ 定里程碑**：既要有产品能不能用的标准，也要有「谁会反复打开」。定不出来说明对问题还不熟。当堂只要求写清「问题与用户」第一节；其余 8 项课后补。
  - **⑤ 做资源预算**：数据、时间、就你一个人。某一步走不通就退回前面一步。对清单 **6 范围**：MVP 12 周一人可完，**「不做」清单必写**；另点 **5 可视化骨架、7 部署、8 合规** 各一句（3–5 张图、免费部署、不涉交易/不泄个人数据）。
  - **收束对照**：打开 1 份合格、1 份不合格提案（隐去姓名），只看「问题与用户」第一节——合格稿能看到痛点、给谁、社区证据；不合格稿是假设痛点或一上来写功能。点明下一格：先写这一节，8 项其余课后补全。
4. **Deep Research 演示（10 分钟）**：对应刚讲的第 ③ 步（可行性与价值）。教师机打开 **workbuddy**，建议走 **「产品战略团队」**（不要用默认闲聊；该团队面向用户痛点、替代方案与市场旁证，正好交叉验证选题）。登不上改用 TraeWork。挑一句刚筛出来的课堂痛点交给产品战略团队，只问真实性：这类人是不是真的反复遇到这件事、有没有公开讨论或替代做法、请给来源。10 分钟够用执行摘要，不必等完整长报告。示范把检索结论收成提案里的一两句，而不是粘贴长文。网上对不上的标成待验证或换方向；检索不替代社区原话。学生课后用同一入口（workbuddy → 产品战略团队）对自己的痛点再跑一遍。
5. **收束（11 分钟）**：同一轮打开 `docs/` 下三份已有文件，不要另开。`docs/community.md`：继续倾听，原话追加到同一份（最好补到 10 条），题目和方向可以换。`docs/journal.md`：当日追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录；互助只写「谁帮了你、对项目有何影响」，没有则写「无」）。`docs/requirements.md`：把「问题与用户」（痛点、给谁、社区证据、为什么现在做）、workbuddy 的一两句、准入 8 项缺口（含「不做」清单）写进同一份；第 1 节骨架不够就覆盖改。教师巡视，拿不准的当场问。

**第3节 · 数据采集：requests + BeautifulSoup（45 分钟）**

W2 说「具体代码下节课再学」，本节兑现。提案主线已在第 2 节做完，不再重复。不做访谈复盘（多数人尚未访谈）。

1. **开篇：Coding AI Is the New Literacy（5 分钟）**：投影 Andrew Ng *How to Build Your Career in AI* 导论（`references/build-career-in-ai-era.md` 开头；PDF：`references/build caree in AI era.pdf`）。不要通读全文。点三句，再落到今天的采集：
  - 几百年前识字只是少数人的事，后来读写成为常识，社会因此更富。他希望写代码（尤其为 AI 写）有一天也像识字一样普遍。
  - 文字是人与人之间最深的交流；**代码是人与机器之间最深的交流**。机器越进入日常生活，这种交流越重要。
  - 传统入门课用做游戏、建网站当例子，多数职业并不需要这个。AI / 数据科学换了一条路：计算机从数据里抽出知识。披萨店用线性回归估需求、备夏威夷披萨，就是「为 AI 写代码」对非软件工程师也有用。因此 **AI 向的代码素养，往往比传统软件工程更值钱**。
  - 落到本节：西财要闻不是为了交爬虫作业，而是第一次用代码跟网页这台「机器」把数据拿下来。`requests` 拿 HTML，`BeautifulSoup` 拆字段——这就是今天的识字练习。鼓励课外把导论读完。
2. **同学展示（10 分钟）**：邀请同学展示西财要闻数据和代码（W2 作业不交这两样，本周当场跑）。能跑通的投屏；跑不通的说卡在哪。全班不要求打开 Jupyter。
3. **对照拆代码（22 分钟）**：打开 `weeks/week03/swufe-news.md`。口诀：**requests 负责拿，BeautifulSoup 负责拆**。点明列表页字段（日期、标题、链接）和正文页怎么拆。学生对照自己的脚本看这两步在哪；缺的当场补或课后按该页补。当堂目标：说清拿 / 拆，能指到自己代码里的对应位置。
4. **收束（8 分钟）**：每人确定本周**补充调研**的访谈对象（约不到走互助池/家人补位）：不是另做一份调研，而是把第 2 节那句痛点加深、拓展，写回同一份 `docs/community.md`。过审规则与 48h 重提通道。技能小练见 `lab.md`。提醒：本周 `docs/journal.md` 全文**选做**（仓库里继续写；W10 / W15 / W17 再必交）。第 2 节已写过日志的，补一句采集上的决定即可。`docs/requirements.md` 也继续改同一份：采集能说明数据从哪来的，写进清单第 1 项（数据源）；仍空的 8 项课后补。

## 项目活动

**必做**
1. 补齐个人项目仓库：根目录有 `AGENTS.md`；`docs/` 有 `journal.md`、`requirements.md`、`design.md`、`scope.md` 骨架，以及迁入的 `community.md`。推远端为选做。课外阅读 `references/The Founder's Playbook.pdf`，对照这些文档理解「给 AI 留持久上下文」
2. 第 1 节按 `weeks/week03/venv-setup.md` 建 `.venv`（勿提交该文件夹）
3. 互查并补充 `docs/community.md`（人 = 后续产品计划服务的人；原话追加到同一份）。对照候选方向评估数据分析来源。W1 未交齐的本周补进仓库，原话 ≥3 条、最好补到 10 条
4. 在已进入的目标用户社区中继续倾听（线下或线上；人须为后续产品服务对象），完成≥1周倾听；原话仍写在 `docs/community.md`
5. 从社区调研中形成或验证选题痛点，筛掉无真实需求的选题
6. 用Deep Research交叉验证痛点真实性
7. 完成 ≥1 次用户访谈（补充调研：加深已有原话、拓展相邻麻烦；写回同一份 `docs/community.md`，能改提案的再改 `docs/requirements.md`）
8. 以 `templates/requirements.md` 格式撰写并提交个人项目提案，对照 `project-selection-guide.md` 选题准入清单 8 项过审

**进阶（可选）**
- 用 workbuddy **产品战略团队**（或 TraeWork）对自己的痛点再做一轮深入调研（课堂演示已走产品战略团队；课外换 TraeWork 也可以）

**兜底**
- 提案未过审：从选题指南 §3 菜单种子中选方向，48h 内走教师快速通道重提——已加入的社区与已验数据可继续沿用，不算从零开始
- 访谈约不到人：从课程互助测试池/同学家人中补位
- W2 互助小组协议仍未交纸质签字版：第 1 节记下组名，本周内补交
- opencode 装不上：带报错走课程群；第 1 节五份基本文档可先用 Trae；第 3 节西财要闻展示运行须能当场跑起来
- `.venv` 当堂建不上：第 1 节先完成 `AGENTS.md` 与 `docs/` 下文档（含迁入 `community.md`），按 `weeks/week03/venv-setup.md` 周末补；勿把 `.venv/` 提交进 Git
- W1 社区调研未交齐：第 1 节拷入 `docs/community.md` 时补满 ≥3 条原话，不另开一篇

## 交付物（评分锚点）

- 个人项目仓库（含根目录 `AGENTS.md`；`docs/` 下 `journal.md`、`requirements.md`、`design.md`、`scope.md` 骨架、`community.md`；推远端为选做）—— 本周第 1 节落地项目基本文档
- 个人问题陈述初稿（须附 `docs/community.md`：场合、进入方式、观察期、真实问题与用户原话）—— milestones §1.3
- 个人项目提案（以 `templates/requirements.md` 形式提交，"问题与用户"为强制第一节；含问题、目标、数据来源、初步方案）—— milestones §1.4；须通过选题准入清单 8 项

—— 计入平时成绩（形成性）；提案是本课程第一个真实性关口，未过审须调整或重选。提交前自检：痛点哪些是验证的、哪些是假设待验证的（已标注）？命中哪档选题来源？Andrew Ng 框架至少 2 项论证？列出"不做"清单？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。提案拿不准随时问，不必等答辩。

## 课后任务
1. 完成≥1次用户访谈（课内未完成则补）：补充调研，加深、拓展已有社区原话，写回同一份 `docs/community.md`
2. 完善项目提案
3. 提交个人仓库 `docs/journal.md`（截至本周的全文）——**选做**
4. 准备西财要闻数据和代码，第 3 节课堂邀请展示运行（W2 作业不交这两样；对照 `weeks/week03/swufe-news.md` 补 `requests` + `BeautifulSoup`）
5. 阅读 `references/The Founder's Playbook.pdf`（可读摘录：`references/the-founders-playbook.md`），重点看持久上下文、规格与书面范围，对照自己仓库里的根目录 `AGENTS.md` 与 `docs/` 下其余文档

## 学习资料
- `references/The Founder's Playbook.pdf`（第 1 节鼓励阅读；可读摘录 `references/the-founders-playbook.md`）
- `weeks/week03/lab.md`（第 1 节项目基本文档与 `.venv`；第 3 节对照西财要闻）
- `weeks/week03/opencode-workflow-files.md`（第 1 节：根目录 `AGENTS.md`；`docs/` 下其余基本文档）
- `weeks/week03/venv-setup.md`（第 1 节建 `.venv`）
- `weeks/week03/swufe-news.md`（第 3 节：`requests` + `BeautifulSoup` 采集西财要闻）
- `knowledge/phase1-1-7-community-first.md`（第 2 节当堂自读：社区先行）
- `knowledge/phase1-1-6-user-insight.md`（第 2 节当堂自读：用户访谈技巧）
- `weeks/week02/data-taxonomy.md`（第 2 节评估数据来源时对照）
- `knowledge/phase1-1-10-project-screening.md`（第 2 节：Ng 五步的教学改写，课堂以原文第 4 章为准）
- `references/build-career-in-ai-era.md`（第 2 节投影 Chapter 4 五步；第 3 节开篇导论 *Coding AI Is the New Literacy*；PDF `references/build caree in AI era.pdf`）
- `knowledge/phase1-1-8-deep-research.md`（第 2 节 Deep Research 演示）
- `knowledge/phase1-1-9-project-proposal.md`（第 2 节写提案第一节）
- `templates/journal.md`（本周交 `docs/journal.md` 全文为选做）；`templates/journal-rules.md`（交法）
- `templates/requirements.md`
- `templates/community.md`（W3 提案「真实性证据」引用本文件，不另写调研报告）
- `project-selection-guide.md`（第 2 节投影第 8 节准入清单 8 项）
