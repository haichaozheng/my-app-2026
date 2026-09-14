# Week 02 课堂串讲

今天怎么走：交互助小组协议纸质签字版 → 抽人分享 `journal.md` → 装 opencode 并生成项目规则与三份工作流文件 → 公约写进课程网站 → 仓库收口（迁入 journal / community，建 `.venv`）→ 数据从哪来 → 示范拉西财要闻 → 互查 `community.md`、评估数据来源 → 写当天日志。

**下课时你应能：** 在项目根目录用 opencode 生成 `AGENTS.md`、`requirements.md`、`design.md`、`scope.md`；根目录有 `journal.md` 和 `community.md`；能用多维分类说清一份数据从哪来、怎么拿；和同学互查过社区调研；见过用 opencode 对话生成并跑通「抓一页西财要闻」的 `.py`。当堂不锁定选题。具体采集代码下节课再学。

卡住了：

```
问 AI（附报错）→ 互助组（盯着你自己键入，不代跑）→ 课程群（安装问题附截图）
```

课程群里已有：`opencode-setup.md`、`opencode-class-norm-case.md`、`venv-setup.md`、`data-taxonomy.md`。展示站：[https://haichaozheng.github.io/data-analysis-showcase/](https://haichaozheng.github.io/data-analysis-showcase/)  
新闻页：[数博会一文](https://haichaozheng.github.io/data-analysis-showcase/news.html)　公约页：[rules.html](https://haichaozheng.github.io/data-analysis-showcase/rules.html)

本周起项目工作流主工具是 **opencode**；日常写代码仍用 Cursor（Trae 亦可）。装不上 opencode 先用 Trae，周末补齐。课堂不装 WSL。

---

## 第 1 节 · 交协议 + 分享 journal + 装 opencode

先把上周签字的互助小组协议交上来，再装 opencode、把文件放进个人仓库。第 3 节互查 `community.md`、评估数据来源，不锁定题目。

1. **提交互助小组协议纸质签字版**
  按组交一份 W1 打印的 `templates/group-agreement.md`，须全员签字。没带来的本周补交纸质版，不影响后面安装和建仓。
2. **抽人分享 `journal.md`**
  打开超星课堂活动，随机抽人。三问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点。抽到的同学打开自己的文件口述或投屏；没写的换下一位。
3. **安装 opencode**
  按 `weeks/week02/opencode-setup.md`。官网 **LTS Node.js（24.x）**，不要 Current。然后：

  ```
  npm install -g opencode-ai
  opencode --version
  ```

  装不上先用 Trae，报错截图进群。
4. **初步使用**（必须在**项目根目录**打开，不要在别的文件夹。教师案例：`data-analysis-showcase`。跟做见 `opencode-class-norm-case.md`）
  - **选模型**：界面里选一个即可。**默认免费模型可以跟课。** 有付费模型或 token plan 的可自行接入。
  - **`AGENTS.md`**：给 opencode 的项目规则，内容会进入模型上下文（类似 Cursor 的规则）。根目录运行 `/init`：扫描项目并生成；已有则补充。**空项目也可以直接让模型生成。** 可以把 `journal.md` 的使用规则写进去。
  - **另三份文件**：让 opencode 在根目录生成 `requirements.md`（用户需求）、`design.md`（系统技术设计）、`scope.md`（功能范围与开发工作安排）。骨架即可，可按自己的项目补。
  - **课堂公约**：把 W1 问卷汇总交给 opencode，一起讨论定稿；接着 **改 `rules.html` 并更新课程网站**，不只停在对话。学生可跟做分析与改文件；教师机改站点并推送。

这一节结束：多数人已经能在根目录生成四份文件。装不上的先用 Trae 建同一组文件。

---

## 第 2 节 · 仓库收口 + 数据全景

把上周的记录放进仓库，再问：产品要用的数据从哪来、能不能拿到。

1. **个人仓库收口**
  第 1 节已有的文件不要重做；缺的当场补。装不上环境的先完成拷文件，`.venv` 按 `venv-setup.md` 周末补。
  - **迁入两份记录**：W1 的 `journal.md`（没有则从 `templates/journal.md` 拷入并贴上 W1 那条）和已填的 `community.md` 放到仓库根目录。仍是这两份，不要另开一篇。
  - **建 `.venv`**：先问 opencode 虚拟环境有什么用，再用 `python -m venv .venv`；`.gitignore` 写入 `.venv/`。W1 的系统 Python 只负责「电脑上有解释器」；个人项目的包装进 `.venv`。
  - **推到远端（选做）**：`git add`（不要加 `.venv`）→ 提交 → 推到 GitHub/Gitee。若做了：链接能打开；根目录有 `journal.md`、`community.md`；远端看不到 `.venv`。
2. **产业新闻 + 数据从哪来**
  打开 [产业新闻](https://haichaozheng.github.io/data-analysis-showcase/news.html)，先看 **「数博会探寻数据要素价值释放新路径」**：高质量数据集、数据要素要流通才有用。**不另做幻灯，看白板。** 口述底稿：`weeks/week02/data-taxonomy.md`。  
   同一份数据会落在多条轴上，不是互斥菜单。先问四件事：从哪来、谁能看、花不花钱、怎么拿。

  | 轴 | 常见落点 |
  | --- | --- |
  | 生成 | 客观 / 合成（含仿真） |
  | 开放 | 公开 / 受限 / 私有 |
  | 成本 | 免费 / 付费 |
  | 通道 | API / 下载 / 自己采集 |

  产品要先找到能拿到、能用、能上线的数据。
3. **拉一次数据示范**
  不当场拆代码。打开 opencode，对着 [西财要闻](https://www.swufe.edu.cn/index/xcyw.htm) **全程对话**：说清要一页新闻 → 生成 `.py` → 当场跑通。学生跟做同一问话，方便带走这个文件。  
  **当堂只抓一页。** 具体代码下节课再学。课后作业用同一办法拉全部要闻，交代码和数据；间隔请求，不要并行、不要把学校网站打挂。

这一节结束：仓库根目录有 journal 和 community；能说出一份数据落在哪几条轴上；手里有一个 opencode 生成的、能抓一页新闻的 `.py`。

---

## 第 3 节 · 互查 community.md

上周听人说话。这节看对方写得对不对，并评估：若做成数据分析产品，数据从哪来。当堂不拉数据、不锁定选题。

1. **两人一组，打开对方仓库里的 `community.md`**
  W1 未交齐的当场对着模板补，不影响建仓。
  - 第 4 节是否 ≥3 条原话（不是概括、不是「用户需要更好的体验」）
  - 第 5 节用户是否从这些原话里抽出来的
  - 对不上：当场改第 1 节场合或第 5 节用户，约定本周补听，往表里追加一行
2. **评估数据来源**
  对照第 1 节的候选方向，用上一节的多维分类（`weeks/week02/data-taxonomy.md`）问：公开还是要自己采、免费还是付费、网页 / API / 原话本身。**说清来源与拿法即可。** 互助小组不是用户社区。
3. **布置课后 + 写当天 `journal.md`（最后一项工作）**
  作业见下。技能小练见 `lab.md`：四份文件与迁入 `community.md` 当堂起笔。拉西财全部要闻是课后作业，必须用 opencode。  
  打开 `journal.md`，按五格追加今天 1 条：今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录。互助只写谁帮了你、对项目有何影响，没有则写「无」。

---

## 课后

1. **课后作业 · 拉西财全部要闻**：必须用 **opencode** 写代码并跑通（不要手搓交差）。提交 **代码 + 数据**。范围：[西财要闻](https://www.swufe.edu.cn/index/xcyw.htm) 全部列表和正文，不是当堂那 1 页。可对照 `swufe-news.md`。每请求间隔，不要并行，不要把学校网站打挂。
2. **继续倾听**：原话追加到同一份 `community.md`（W1 未满 3 条的本周补齐）。**下周课堂分享**：会查看你补充或更新的内容；题目和方向可以换。
3. **本周课后学习**
  - `knowledge/phase1-1-7-community-first.md`（社区先行）
  - `knowledge/phase1-1-6-user-insight.md`（用户访谈）
