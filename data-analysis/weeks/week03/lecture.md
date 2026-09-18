# Week 03 课堂串讲

今天怎么走：根目录只留 `AGENTS.md`，其余文档进 `docs/`、建 `.venv` → 先读再筛痛点、Ng 五步对照准入、workbuddy 交叉验证、收束改 `docs/` 下三份文件 → 代码是新识字、同学展示西财要闻、`requests` 拿 / `BeautifulSoup` 拆。

**下课时你应能：** 根目录有 `AGENTS.md` 和 `.venv`，`docs/` 里能打开其余文档；用一句话说清痛点是验证的还是假设的；提案第一节写在同一份 `docs/requirements.md` 里；能指到自己脚本里「拿」和「拆」在哪。

## 本周学习目标

- 根目录 `AGENTS.md`；`docs/` 备齐 `journal.md`、`requirements.md`、`design.md`、`scope.md`，迁入 `community.md`；建 `.venv`（勿提交该文件夹）
- 先听社区再写产品；邻座能判断痛点是验证的还是假设的
- 课后 ≥1 次用户访谈是**补充调研**：加深已有原话、拓展相邻麻烦，写回同一份 `docs/community.md`
- 用 Ng 五步把想法收小；提案过审对照准入 **8 项**（数据源 / 用户 / 痛点 / AI 功能 / 可视化 / 范围 / 部署 / 合规）；「不做」清单必写；workbuddy 产品战略团队做网上旁证
- 西财要闻：`requests` 拿 HTML，`BeautifulSoup` 拆字段

卡住了：

```
问 AI（附报错）→ 互助组（盯着你自己键入，不代跑）→ 课程群（附截图）
```

跟做：`weeks/week03/lab.md`。展示站：[https://haichaozheng.github.io/data-analysis-showcase/](https://haichaozheng.github.io/data-analysis-showcase/)

---

## 第 1 节 · 项目基本文档与虚拟环境

给 AI 留持久上下文，不要每次对话从头解释项目。课外读 `references/The Founder's Playbook.pdf`。

`**AGENTS.md` 必须在根目录。** 其余进 `docs/`。必须在项目根目录打开 opencode，不要在 `docs/` 里打开。`docs/` 让 opencode 建，不要自己 mkdir。

投影对应：


| 本课文件              | 位置      | 干什么                                        |
| ----------------- | ------- | ------------------------------------------ |
| `AGENTS.md`       | 根目录     | 项目规则（类似 Cursor 规则 / Playbook 里的 CLAUDE.md） |
| `journal.md`      | `docs/` | 记下决定，全学期一份、按日追加                            |
| `requirements.md` | `docs/` | 用户需求                                       |
| `design.md`       | `docs/` | 系统技术设计                                     |
| `scope.md`        | `docs/` | 本期做什么、不做什么                                 |
| `community.md`    | `docs/` | 场合、原话、用户（迁入，不另开）                           |


`.venv` 文档落地后再建，不和写文档混在一轮对话里。

1. **补交互助小组协议（5 分钟）**
  只收 W2 未交的组。`templates/group-agreement.md`，全员签字，按组一份。没带的记下，本周内补纸质版。
2. **超星抽人分享 journal.md（8 分钟）**
  三问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点。没写的换下一位。点明：全学期共用一份；本周拷进 `docs/journal.md`。
3. **落地五份基本文档（15 分钟）**
  必须在**项目根目录**打开 opencode。已有的不重做。跟做 `weeks/week03/opencode-workflow-files.md`。
  - `docs/journal.md`：让 opencode 建 `docs/` 并写入，仍是这一份
  - `AGENTS.md`：根目录 `/init`；可把 `docs/journal.md` 用法写进去；提交进 Git
  - `docs/requirements.md` / `docs/design.md` / `docs/scope.md`：让 opencode 建 `docs/`（没有就建）并生成骨架
4. **迁入 community.md（7 分钟）**
  让 opencode 把已填的放到 `docs/community.md`。推远端选做，不要加 `.venv`。
5. **建 `.venv`（10 分钟）**
  独立一块。按 `weeks/week03/venv-setup.md`。`.gitignore` 写入 `.venv/`。装不上记下，周末补。

这一节结束：根目录有 `AGENTS.md` + `.venv`；`docs/` 能打开其余文档（含 `community.md`）。

---

## 第 2 节 · 用户需求痛点分析

先读 → 一句话痛点 → Ng 五步对照准入 8 项 → workbuddy 旁证 → 同一轮改 `docs/` 下三份文件。教师这一节不讲社区材料的幻灯。

1. **自己先读（8 分钟）**
  `knowledge/phase1-1-7-community-first.md`（社区先行）  
  `knowledge/phase1-1-6-user-insight.md`（用户访谈）  
  读完能说出：为什么先听再写产品；访谈不要问「你要不要这个功能」。  
  点一句：**倾听**已经听到原话；**访谈**是课后补充调研，用来加深、拓展，不当堂另开一份。
2. **痛点筛选（8 分钟）**
  打开自己的 `docs/community.md`。一句话：谁、在什么场合、卡在哪（不要写产品名）。  
  邻座只判两种：**验证的**（原话撑得住）/ **仍是假设**。  
  顺带：数据从哪来（`weeks/week02/data-taxonomy.md`）。互助小组不是用户社区。
3. **准入清单 + Andrew Ng 五步（8 分钟）**
  投影：`project-selection-guide.md` 第 8 节；`references/build-career-in-ai-era.md` 第 4 章。  
  **两套东西不要混：** Ng 是**界定范围的五步**（怎么把想法收小），不是打分表。过审看本课准入 **8 项**（硬门槛，缺一项须调整或重选）：

  | #   | 准入    | 当堂要能说到                                     |
  | --- | ----- | ------------------------------------------ |
  | 1   | 数据源   | 具体名称 + 已验证可访问的 URL / API（须免费）              |
  | 2   | 用户    | 具体人群 + 触达 5–10 人的路径                        |
  | 3   | 痛点    | 一句话，须社区原话，非假设                              |
  | 4   | AI 功能 | RAG 或 LLM 解读，须扛痛点，非套壳                      |
  | 5   | 可视化骨架 | 哪 3–5 张图是产品核心                              |
  | 6   | 范围    | MVP 12 周一人可完；**「不做」必写**                    |
  | 7   | 部署    | 免费方案（Streamlit Cloud / HF Spaces / Gradio） |
  | 8   | 合规    | 不涉交易、不泄个人数据                                |

  投影时按 Ng 五步讲，每步对上 8 项里相关的几条。当堂只要求写清「问题与用户」第一节；其余课后补。

  | Ng 五步                 | 对准入                   |
  | --------------------- | --------------------- |
  | ① 先找业务问题，不是 AI 问题     | 2 用户、3 痛点（须原话）        |
  | ② 再头脑风暴多种方案           | 4 AI 功能               |
  | ③ 可行性 + 价值（至少写清这 2 项） | 1 数据源、2–3 用户与痛点       |
  | ④ 定里程碑                | 当堂只写「问题与用户」第一节        |
  | ⑤ 资源预算；走不通退回上一步       | 6 范围；5 图、7 部署、8 合规各一句 |

  合格提案：痛点、给谁、社区证据。不合格：假设痛点，或一上来写功能。
4. **Deep Research 演示（10 分钟）**
  对应第 ③ 步。打开 **workbuddy → 产品战略团队**（不要默认闲聊；登不上改 TraeWork）。  
  只问真实性：这类人是不是真的反复遇到、有没有公开讨论或替代做法、来源是什么。  
  10 分钟取执行摘要，收成提案一两句，禁止粘长文。检索不替代原话。
5. **收束（11 分钟）**
  同一轮改 `docs/` 下三份，不要另开：  
  - `docs/community.md`：原话追加（最好补到 10 条），题目可换  
  - `docs/journal.md`：当日 1 条五格（互助：谁帮了你、对项目有何影响 / 无）  
  - `docs/requirements.md`：「问题与用户」+ workbuddy 一两句 + 8 项缺口（含「不做」）

这一节结束：每人有一句经过邻座判断的痛点；`docs/requirements.md` 第一节已动笔。

---

## 第 3 节 · 数据采集：requests + BeautifulSoup

W2 说「具体代码下节课再学」，本节兑现。提案主线不再讲。全班不要求打开 Jupyter。

1. **开篇：Coding AI Is the New Literacy（5 分钟）**
  投影 `references/build caree in AI era.pdf` 导论，不要通读。三句再落地：
  - 识字曾是少数人的事；写代码（尤其为 AI）有一天也应像识字一样普遍
  - 文字是人与人最深的交流；**代码是人与机器最深的交流**
  - 不必人人做游戏、建网站；披萨店用数据估需求，就是 AI 向的代码素养  
  落到本节：西财要闻是第一次用代码把网页数据拿下来。
2. **同学展示（10 分钟）**
  邀请跑西财要闻数据和代码（W2 作业不交这两样）。能跑通的投屏；跑不通的说卡在哪。
3. **对照拆代码（22 分钟）**
  打开 `weeks/week03/swufe-news.md`（笔记本同目录 `swufe-news.ipynb`）。  
  口诀：**requests 负责拿，BeautifulSoup 负责拆。**  
  列表页：日期、标题、链接（只选 `a.publine`）。正文页：`.v_news_content`。  
  顺带一句：encoding 是字→字节，decoding 是字节→字；西财用 UTF-8，`resp.encoding = "utf-8"`。  
  当堂：能指到自己代码里拿 / 拆在哪。
4. **收束（8 分钟）**
  确定本周**补充调研**的访谈对象（约不到走互助池 / 家人）：不是另做一份调研，而是把第 2 节那句痛点**加深、拓展**。提案未过审：48h 重提。  
  本周 `docs/journal.md` 全文**选做**（仓库里继续写；W10 / W15 / W17 再必交）。  
  `docs/requirements.md` 同一份继续改：采集能说明数据从哪来的，写入准入第 1 项（数据源）。

---

## 课后

1. **补充调研：≥1 次用户访谈**（课内未完成则补）
  社区倾听已经有原话；访谈不是另开调研，是把同一条痛点**加深、拓展**，写回同一份 `docs/community.md`。能改提案的再改 `docs/requirements.md` 第一节。  
  - **加深**：问上次具体怎么做、怎么凑合、哪一步最麻烦（不要问「你要不要这个功能」）  
  - **拓展**：还有谁也卡在这、他们试过什么、有没有你没听到的相邻麻烦  
  约不到人走互助池 / 家人。对照 `knowledge/phase1-1-6-user-insight.md`。
2. 完善项目提案（准入 8 项；「不做」清单必写）
3. 提交个人仓库 `docs/journal.md`（截至本周的全文）——**选做**
4. 对照 `weeks/week03/swufe-news.md` 补 `requests` + `BeautifulSoup`（第 3 节已展示的，课后把缺的补上）
5. 阅读 `references/The Founder's Playbook.pdf`（可读摘录 `references/the-founders-playbook.md`）
6. 课外可用 workbuddy **产品战略团队** 对自己的痛点再跑一遍

