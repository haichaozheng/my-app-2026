# W3 课堂案例：项目基本文档

> 给谁：第 1 节当场跟做。opencode 已在 W2 装好并会选模型。  
> 教师案例仓库：`data-analysis-showcase`（课程网站）。  
> 你在**自己的项目根目录**跟做。已有的文件不要重做，缺的当场补。  
> **`AGENTS.md` 必须在根目录**（opencode / Cursor 会读这一层）。其余文档放进新建的 `docs/`：`docs/journal.md`、`docs/requirements.md`、`docs/design.md`、`docs/scope.md`、`docs/community.md`。  
> 课外对照 `references/The Founder's Playbook.pdf`（可读摘录：`references/the-founders-playbook.md`）：给 AI 留持久上下文。`AGENTS.md` 类似其中的 CLAUDE.md；`docs/requirements.md` / `docs/design.md` 是规格与架构；`docs/scope.md` 写清做什么、不做什么；`docs/journal.md` 记下决定。  
> 规则说明：[opencode 规则 · 初始化](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)

**必须在项目根目录打开 opencode**（有 `index.html` / 以后有 `AGENTS.md` 的那一层），不要在 `docs/` 里打开。`docs/` **不要自己 mkdir**，交给 opencode 建：没有这个文件夹就先建，再往里面写文件。

---

## 0. docs/journal.md

把已写的日志交给 opencode，让它新建 `docs/`（没有就建）并写入 `docs/journal.md`（没有底稿则从 `templates/journal.md` 拷入并贴上已有条目）。全学期共用这一份，按日追加，不要另开一篇。不要放在根目录。可对 opencode 说：

> 没有 `docs/` 就先建这个文件夹。把我已写的项目日志放到 `docs/journal.md`（不要放根目录）。全学期共用一份，按日追加、旧条目不删。

---

## 1. AGENTS.md（根目录）

先分清它做什么：`AGENTS.md` 是给 opencode 的**项目规则**。内容会进入模型上下文，用来按本项目定制行为（类似 Cursor 的规则）。**只这一份留在根目录。**

在根目录运行：

```text
/init
```

它会扫描项目并生成 `AGENTS.md`；已经有这份文件，则在原有基础上补充。

**如果是空项目**（几乎还没有代码可扫描），也可以直接让模型生成，例如：

> 这是一个空项目。请在根目录新建 `AGENTS.md`，写清以后怎么运行、代码约定、架构和常见错误。没有 `docs/` 就先建这个文件夹。项目文档放在 `docs/`：`journal.md`、`requirements.md`、`design.md`、`scope.md`、`community.md`。不要把这些文件再写到根目录。

**也可以把 `docs/journal.md` 的使用规则写进 `AGENTS.md`**，例如：

> 把 `docs/journal.md` 的用法写进 `AGENTS.md`：全学期共用一份，按日追加、旧条目不删；课堂收束写 1 条；五格为今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录；互助只写谁帮了你、对项目有何影响，没有则写「无」。不要替我编日志，提醒我自己写。

生成或补充后**提交进 Git**。

---

## 2. docs/requirements.md、docs/design.md、docs/scope.md

让 opencode 在 **`docs/`** 生成下面三份，并可按自己的项目补内容：

| 文件 | 写什么 |
|---|---|
| `docs/requirements.md` | 项目的**用户需求**（给谁、解决什么问题、要什么能力） |
| `docs/design.md` | 系统的**技术设计**（怎么实现、用什么结构） |
| `docs/scope.md` | 系统的**功能范围**和开发工作安排（本期做什么、不做什么、按什么顺序） |

可对 opencode 说：

> 没有 `docs/` 就先建这个文件夹，再在里面新建 `requirements.md`、`design.md`、`scope.md`（不要放根目录）。requirements 写用户需求，design 写系统技术设计，scope 写功能范围和开发工作安排。根目录只保留 `AGENTS.md`。

---

## 3. docs/community.md

已填的社区调研交给 opencode，写入 `docs/community.md`（没有 `docs/` 就先建），仍是这一份，不要另开一篇。可对 opencode 说：

> 没有 `docs/` 就先建这个文件夹。把我已填的社区调研放到 `docs/community.md`（不要放根目录），旧内容不删。
