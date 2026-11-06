# Week 01 动手实验（课后练习）

> 第一节课以讲授与教师投屏演示为主（第 3 节有分组实验），本实验为课后练习，不需要提交作业。第 1 部分与课堂的 case-nlp 演示是同一批数据；第 2 部分把脚本改造成你自己的版本。W2 课前须完成全部三部分。

## 实验目标

亲手把股吧文本变成数据，回应课堂疑问"同一批文本，两种方法为何结论不同"；再把课上脚本改造成自己的版本；写最简版 `AGENTS.md`。

## 第 1 部分 · case-nlp 情感分析主线（约 80-110 分钟）

1. 打开 `weeks/week01/case-nlp/week01-nlp-lab.ipynb`，按 notebook 顺序亲手做：
   - 分词（体会 `userdict.txt` 加入"光线传媒""股吧"等词前后的切分差异）
   - 停用词 + 词频
   - 词典法情感打分（`zhang_unformal_pos/neg.txt`）
   - LLM 情感分析（需 `DEEPSEEK_API_KEY`，与词典法并排对比）
   - 每日情绪曲线 → 情绪 vs 股价相关性
2. 边做边回应课堂疑问：词典法和 LLM 法为何在"利好出尽""割韭菜"这类评论上结论不同？分歧最大的是哪类评论？各找 1-2 条例子
3. 小改动实验：往词典里加/删 3-5 个你自己的词（如行情黑话），看每日情绪曲线怎么变

## 第 2 部分 · 改造成你自己的脚本（约 30 分钟）

4. 从自己研究方向出发，想 3-5 个想在社交媒体/论坛文本里追踪的关键词、黑话或品牌名
5. 用 opencode 改造课上脚本 `mini_emotion.py`：换成你的关键词，或改分组维度（按小时/星期看发帖高峰、按点赞数看高热评论），终端跑通并截图

## 第 3 部分 · AGENTS.md

6. 在项目根目录建 `AGENTS.md`，写最简版（3-5 行）：
   - 项目目标（一句话）
   - 技术栈（Python 3.13、pandas、jieba 等）
   - 目录结构约定
7. 退出 opencode 再重新打开，确认它读到了 `AGENTS.md`

## 实验交付（自查留存，本周不提交）

- notebook 运行记录（关键单元格输出截图）+ 对课堂疑问的 2-3 句回答（含 1-2 条分歧评论例句）
- `mini_emotion.py` 改造版（代码 + 运行截图）+ 一句说明：你改了什么、看到了什么
- 最简版 `AGENTS.md`
- 环境验收截图（见 `setup.md` 末尾"安装顺序速查"六步）

## 卡住了

- 安装包下不动：换校园网 / 手机热点
- `python` 不是 3.13：`conda config --set auto_activate_base false` 后重开终端，或重装勾选 Add to PATH
- Cursor 运行按钮灰：`Ctrl+Shift+P → Python: Select Interpreter` 选 `Python313`
- PowerShell 禁止 npm：用 `npm.cmd` 或 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- opencode 装不上：确认 `node -v` 能跑；仍失败带报错截图进课程群
- notebook 缺依赖：`python -m pip install jieba pandas matplotlib openai`；Part 4 需要 `DEEPSEEK_API_KEY`（没有可跳过，只做词典法部分）
- 卡住 → 问 AI（附报错）→ 同学互助解答 → 课程群提问
