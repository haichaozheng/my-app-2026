# Week 02 技能小练 — opencode 与 AGENTS.md 首次连接

> 定位：本周里程碑（赛道意向 + 项目仓库）的热身，约 30-45 分钟；计入平时成绩"技能小练"。

## 任务

1. **建仓库**：`git init` 个人项目仓库，放入 `AGENTS.md`（复制 `templates/AGENTS.md` 填三行即可：怎么运行、代码约定、一个 AI 易错点），并把 `templates/journal.md` 与 W1 已交的 `community.md` 复制到仓库根目录，按 `venv-setup.md` 建 `.venv`（文件夹勿提交），推送到 GitHub/Gitee。
2. **接管上下文**：在项目目录启动 opencode，问它"我这个项目的运行命令和代码约定是什么？"——回答正确即证明 AGENTS.md 被读取接管。
3. **故意留错**（可选 2 分钟）：让 AI 写一段违反你 AGENTS.md 约定的代码，纠正后把该纠正写回 AGENTS.md 的"常见错误"——体验机构知识文件的用法。
4. **一次 Prompt 探索**：用 opencode 让 AI 拉一个 AKShare 接口（如指数日线），输出前 5 行 + 一句话数据说明，把对话记录进赛道意向。

## 提交

- 仓库链接（公开可访问）
- 任务 2 的问答截图一张
- 任务 4 的 Prompt 记录（并入赛道意向）

## 自检（达标线）

- [ ] opencode 能正确复述你 AGENTS.md 里的内容
- [ ] 仓库含 AGENTS.md + journal.md + community.md，git log 有首次提交；本地有 `.venv` 且未提交该文件夹
- [ ] 数据源拉通与否都记录了结果和原因
