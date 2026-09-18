# Week 02 课堂串讲

今天怎么走：收已带到的互助小组协议 → 装 opencode → 选模型 → 公约写进课程网站 → 数据从哪来 → 示范采集西财要闻 → 讲清本周作业 → 写当天日志。

## 本周学习目标

- 会用 opencode：选模型（默认免费即可）
- 和全班一起用 opencode 分析 W1 公约问卷，把课堂公约写进课程网站（改文件，不只对话）
- 能从生成、开放、成本、通道说清一份数据；不锁定选题
- 用 opencode 采集西财要闻。本周交 Word 实验报告；数据和代码下周课堂邀请同学展示运行

## 本周实验

跟做 `weeks/week02/lab.md` 里对应的部分：

1. 安装 opencode（`opencode-setup.md`）
2. 选模型、课堂公约（`opencode-class-norm-case.md`）
3. 用 opencode 采集类似 `swufe_xcyw_demo.jsonl` 的西财要闻。本周交 Word 实验报告；数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。模板：`weeks/week02/homework02-name-id.md`

卡住了：

```
问 AI（附报错）→ 互助组（盯着你自己键入，不代跑）→ 课程群（附截图）
```

课程群里已有：`lab.md`、`opencode-setup.md`、`opencode-class-norm-case.md`、`data-taxonomy.md`、`homework02-name-id.md`。展示站：[https://haichaozheng.github.io/data-analysis-showcase/](https://haichaozheng.github.io/data-analysis-showcase/)  
新闻页：[数博会一文](https://haichaozheng.github.io/data-analysis-showcase/news.html)　公约页：[rules.html](https://haichaozheng.github.io/data-analysis-showcase/rules.html)

本周起项目工作流主工具是 **opencode + Cursor**。

---

## 第 1 节 · 装 opencode + 公约

先收已带到的互助小组协议，再装 opencode、把课堂公约写进网站。

1. **收取已带到的互助小组协议纸质签字版**
  按组交一份 W1 打印的 `templates/group-agreement.md`，须全员签字。没带来的记下，本周补交纸质版，不影响后面安装。
2. **安装 opencode**
  按 `weeks/week02/opencode-setup.md`。官网 **LTS Node.js（24.x）**。然后：

  ```
  npm install -g opencode-ai
  opencode --version
  ```

  PowerShell 若提示无法加载 `npm.ps1`、禁止运行脚本：Node 已经装好了。用 `npm.cmd` 再装一次，或执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 后重开终端。

3. **初步使用**（必须在**项目根目录**打开，不要在别的文件夹。教师案例：`data-analysis-showcase`。跟做见 `opencode-class-norm-case.md`）
  - **选模型**：界面里选一个即可。**默认免费模型可以跟课。** 有付费模型或 token plan 的可自行接入。
  - **课堂公约**：把 W1 问卷汇总交给 opencode，一起讨论定稿；接着 **改 `rules.html` 并更新课程网站**，不只停在对话。学生可跟做分析与改文件；教师机改站点并推送。

这一节结束：多数人能打开 opencode、选好模型。装不上的先用 Trae 跟公约讨论。

---

## 第 2 节 · 数据全景

问：产品要用的数据从哪来、能不能拿到。

1. **产业新闻 + 数据从哪来**
  打开 [产业新闻](https://haichaozheng.github.io/data-analysis-showcase/news.html)，先看 **「数博会探寻数据要素价值释放新路径」**：高质量数据集、数据要素要流通才有用。**不另做幻灯，看白板。** 口述底稿：`weeks/week02/data-taxonomy.md`。  
   同一份数据会落在多条轴上，不是互斥菜单。先问四件事：从哪来、谁能看、花不花钱、怎么拿。

  | 轴 | 常见落点 |
  | --- | --- |
  | 生成 | 客观 / 合成（含仿真） |
  | 开放 | 公开 / 受限 / 私有 |
  | 成本 | 免费 / 付费 |
  | 通道 | API / 下载 / 自己采集 |

  产品要先找到能拿到、能用、能上线的数据。
2. **拉一次数据示范**
  不当场拆代码。打开 opencode，对着 [西财要闻](https://www.swufe.edu.cn/index/xcyw.htm) **全程对话**：说清要一页新闻 → 生成 `.py` → 当场跑通。学生跟做同一问话，方便带走这个文件。  
  **当堂只抓一页。** 具体代码下节课再学。课后用同一办法继续拉；本周交 **Word 实验报告**（见课后）。数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。

这一节结束：能说出一份数据落在哪几条轴上；手里有一个 opencode 生成的、能抓一页新闻的 `.py`。

---

## 第 3 节 · 作业说明与 journal

1. **西财要闻实验报告**
  对照 `weeks/week02/homework02-name-id.md`。必须用 **opencode + Cursor**。采集西财所有要闻：[https://www.swufe.edu.cn/index/xcyw.htm](https://www.swufe.edu.cn/index/xcyw.htm)。  
  **本周交 Word**；数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。在超星学习通提交，提交前检查内容，不要交错文件。文件名：`西财要闻采集实验报告-姓名-学号.docx`（把姓名改成你自己的名字，把 id 改成你的学号）。
2. **继续倾听**
  原话追加到同一份 `community.md`。W1 未满 3 条的本周必须补齐，**最好补到 10 条**。题目和方向可以换。
3. **写当天 `journal.md`（最后一项工作）**
  打开 `journal.md`，按五格追加今天 1 条：今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录。互助只写谁帮了你、对项目有何影响，没有则写「无」。W3 建仓时拷到 `docs/journal.md`。

---

## 课后

1. **课后作业 · 采集西财要闻（交 Word 实验报告）**：必须用 **opencode + Cursor** 做。模板与要求见 `weeks/week02/homework02-name-id.md`。范围：[西财要闻](https://www.swufe.edu.cn/index/xcyw.htm)。**本周交 Word 版实验报告**，须含：实验目标；opencode 使用过程截图（尽可能详细展示交互过程）；踩坑记录（1–3 条）；解决经验（写清问了 opencode、互助小组还是其他途径）；是否最终完成数据采集（采集了多少条，并给出最初 10 条的截图）。**数据和代码下周课堂邀请同学展示运行，本周作业不交这两样。** 在超星学习通提交。
2. **继续倾听**：原话追加到同一份 `community.md`。W1 未满 3 条的本周必须补齐，**最好补到 10 条**。题目和方向可以换。
