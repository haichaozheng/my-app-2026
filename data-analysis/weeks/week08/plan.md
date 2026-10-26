# Week 08 教学计划

## 主题
MCP 与 Zotero：AI 辅助个人项目调研与写作

> **前置**：W2 已装 opencode（Node.js 环境）；课前装好 Zotero 7+；有开题备选方向者带着方向来（没有也可完成，按备选方向抓文献）。
>
> 本周教学内容已调整：聚焦 MCP、Zotero 文献管理、AI 辅助调研和写作。原文本分析主题压缩为「分词概念 + jieba 体验」，嵌入论文精读环节（《Strategic Directions for AI》正是用年报关键词测量 AI orientation）。

## 本周学习目标

- 能说清 MCP 解决什么问题（接口标准化）、三方架构（Host/Client/Server）、`local` 与 `remote` 两种服务器
- 能独立配置 tushare 与 zotero 两个 MCP（掌握 v2 的 `mcp.servers` 写法，能排查连不上的常见原因）
- 能用 zotero MCP 完成文献清点、单篇速读、文献综述草稿与选题评估，并对 AI 产出的引用逐条回 Zotero 核对
- 能精读一篇论文并抓住测量与结论（AI orientation：年报文本、7 类关键词、0/1 编码；CIO 与董事会的作用）
- 能说出分词是什么、为什么中文文本分析绕不开它，以及大模型时代优先调 API 而非自建分词
- 能写出一组合格的 APA「作者-日期」引注（文中引注 + 文末参考文献一一对应），并用 opencode 辅助加引用

## 预计投入

课堂 3×45 分钟。课外 4-6h（文献导入与补库、综述草稿核对、围绕选题的调研与写作）。

## 教学内容
1. MCP 概念与架构（Host/Client/Server；local/remote 两种服务器）
2. tushare MCP 配置与体验（金融数据零代码取数）
3. Zotero 文献管理与 zotero MCP（建库导入、清点、速读、综述草稿、选题评估）
4. 论文精读方法：以《Strategic Directions for AI》为例盯住「测量」与「结论」
5. 中文分词概念与 jieba 基础（精确/全模式之别；大模型时代的取舍）
6. APA 第 7 版引用规范与 AI 辅助写作（作者-日期制；防编造引用的核对）

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| 概念 | 薄幻灯 | MCP 三方架构与两种服务器（AI 世界的 USB-C）；APA 作者-日期制的两部分对应关系 |
| 现场主演示 | opencode + tushare / zotero MCP | 零代码取行情；当场生成综述草稿、当场回 Zotero 核对引用——把「AI 会编造引用」演给学生看 |
| 学生跟做 | opencode + Zotero | 全程跟做：各自配 token、连本地 Zotero、用自己的「项目文献」集合跑查询 |
| 论文精读 | 课程 PDF + Zotero | 《Strategic Directions for AI》导入后由 AI 读正文，挖测量方法与核心结论 |

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：opencode v2 已升级、两个 MCP 已配通；课程论文 PDF 已分发；Zotero 演示库已备好（含几条元数据不全的条目，用来演示「抓取失败 AI 读不出」）。主体实验为 `week08-mcp-project-proposal-lab.md`（约 105 分钟 + 选题交流），按「步骤 1-4 一节、步骤 5-7 一节、步骤 8-10 一节」推进。

**第1节 · MCP 概念与 tushare 配置体验（45 分钟）**（lab 步骤 1-4）

1. **升级 OpenCode v2（5 分钟）**：全班确认 `opencode --version` 为 v2；强调先关进程再装的 Windows 坑。
2. **理解 MCP 是什么（10 分钟）**：读官方入门两篇，用自己的话答三问（解决什么问题、三方架构、两种服务器）。
3. **配置 tushare MCP（10 分钟）**：各自注册取 MCP token，新建 `opencode.jsonc`；强调 `mcp.servers` 写法与 `oauth: false`，以及 token 安全红线。
4. **体验 tushare MCP（15 分钟）**：取行情、查项目标的、存 CSV 画走势图；观察「零代码取数」与结构化数据形态。限额提醒：每查询 1-2 次，别课堂刷积分。
5. **收束（5 分钟）**：local vs remote 各对应谁；当日在 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）。

**第2节 · Zotero 文献管理与 zotero MCP（45 分钟）**（lab 步骤 5-7）

6. **为 Zotero 准备文献（10 分钟）**：建「项目文献」集合，围绕选题导入 3-5 篇（Connector 抓取或拖 PDF）；检查元数据完整性。
7. **配置 Zotero MCP（10 分钟）**：开本地通讯开关、装 `zotero-mcp-server`、追加进 `opencode.jsonc`；`opencode mcp list` 见两条 connected。
8. **体验 zotero MCP（15 分钟）**：清点家底 → 单篇速读 → 300 字综述草稿 → 选题评估，四连问依次跑。
9. **必做核对（10 分钟）**：把 AI 综述里提到的每一篇回 Zotero 对一遍——本周最重要的一条经验：AI 会编造引用，核对结果是否可信是作者的责任。

**第3节 · 精读论文、APA 引用与选题交流（45 分钟）**（lab 步骤 8-10）

10. **精读《Strategic Directions for AI》（15 分钟）**：导入 PDF 后由 AI 读正文，盯住 AI orientation 的测量（年报、7 类关键词、0/1 编码）与核心结论（CIO、董事会调节、post hoc）；顺势讲分词概念、jieba 精确/全模式、大模型时代的取舍。
11. **APA 引用规范（10 分钟）**：作者-日期制两部分对应；用精读的这篇当示例写引注；再让 opencode 给综述草稿补 APA 引注（只准用库里的文献）。
12. **个人项目选题：调研、写作与老师交流（15 分钟）**：学生开始调研与写作，老师逐一单独交流选题（每人约 5 分钟）；交流意见当场记录。
13. **收束（5 分钟）**：对照 lab 自检清单过一遍；当日 `journal.md` 追加 1 条。互助记录只写「谁帮了你、对项目有何影响」，没有则写「无」。

## 项目活动

**必做**
1. 完成 `week08-mcp-project-proposal-lab.md` 全部 10 个步骤：两个 MCP 自己配出来、Zotero「项目文献」集合 3-5 篇、综述草稿及逐条核对、论文精读记录、APA 引注练习、与老师完成选题交流

**进阶（可选）**
2. 用 tushare 把项目关注标的的 60 日行情存 CSV 并画走势图，作为选题数据可行性的一手证据
3. 安装 `zotero-mcp-server[semantic]`，体验语义检索（按主题找文献）

**兜底**
- 当堂 MCP 配不通的学生：先记卡点进 `journal.md`，课后按 lab「高频卡点速查」自查，仍未解决走求助链

## 交付物（评分锚点）

- 实验记录（lab 各步骤要求：MCP 三问、步骤 4 三个观察、综述草稿与核对结果、论文精读与追问）+ Zotero「项目文献」集合

—— 达标线以 lab 文末「自检（达标线）」为准；计入平时成绩（形成性）。提交前自检：两个 MCP 都是「我自己配出来的」？AI 综述里每条引用都回 Zotero 核对过？token 没出现在任何提交物里？

## 卡住了找谁

卡住 → ①先问 AI（附报错与 `opencode mcp list` 输出，token 打码）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）。

## 课后任务
1. 完成 lab 未做完的步骤（可分两次：步骤 1-4 一次，步骤 5-10 一次）
2. 按与老师交流的意见继续选题调研与写作，文献库随调研扩充

## 学习资料
- `weeks/week08/week08-mcp-project-proposal-lab.md`（本周主体实验文档）
- `weeks/week08/STRATEGIC DIRECTIONS FOR AI.pdf`（精读论文）
- OpenCode v2 文档：https://opencode.ai/v2/docs/
- MCP 官网：https://modelcontextprotocol.io/
- 视频资料（超星学习通，详见 `video-resources.md`）：按需参考
