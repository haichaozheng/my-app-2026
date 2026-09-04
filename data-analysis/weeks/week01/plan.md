# Week 01 教学计划

## 主题

课程启动 + PBL方法论 + AI工具栈起步

## 本周学习目标

- 能用自己的话说明 Challenge→Gap→Knowledge→Apply 学习循环与"从知识接收者到问题解决者"的角色转变
- 能按自己的偏好选好集成开发环境（国内 Trae 或国外 Cursor，二选一即可），完成安装并选中 Python 3.13，用 AI 辅助编程跑通一次真实数据（国家财政数据集）的分析
- 能产出可指导 W2 行动的社区调研方法：选哪些社区、如何融入、观察什么、记录什么

> **编程小白**：不要求会写 Python。本周过关 = 自选的 IDE（Trae 或 Cursor）能打开文件夹 + 让 AI 读入财政数据并跑通 + 能说出自己改了哪一处。语法课不单独开。建组时每组至少 1 人能装环境。详见总方案「编程小白路径」。

> **IDE 自选（告知学生）**：集成开发环境按个人偏好选择即可——**国内 Trae**（[trae.ai](https://www.trae.ai)）与 **国外 Cursor**（[cursor.com/cn](https://cursor.com/cn)）课程都认，评分不偏哪一边。课堂演示两边都会用；学生跟自己装的那一边即可。选一个用熟，不要两个都装当任务。网络或登录哪边顺，就选哪边。

## 预计投入

课堂 3×45 分钟。课外 4-6h（起步周，以课堂实操为主）

## 教学内容

1. PBL学习方法论
   - 什么是PBL：以学生为中心、在做中学、真实问题驱动
   - Challenge→Gap→Knowledge→Apply 学习循环
   - 学生角色转变：从知识接收者 → 问题解决者 → 主动学习者
2. 课程框架与公约构建
   - 4阶段17周全景图（Idea→MVP→Launch→Scale）
   - "一人公司 + 互助小组"模式
   - 课程公约师生共建
3. AI辅助编程工具实操（Trae 与 Cursor 并列，学生自选）
   - **Python 3.13（官网安装，不要 Anaconda，不要点首页的 3.14）**：IDE 都不自带解释器，本周必须先装 Python 才能本地运行。步骤见 `weeks/week01/python-setup.md`。个人项目 `.venv` 留到 W2 建仓时再配
   - **Trae**（国内）：[https://www.trae.ai](https://www.trae.ai)，字节跳动 AI IDE
   - **Cursor**（国外）：[https://cursor.com/cn](https://cursor.com/cn)，基于 VS Code 的 AI-first IDE
   - 二者本课同等认可；课堂两套都会演示同一套财政数据操作。学生按偏好与网络情况选一个
   - **AI办公平台**（课外选做，不计入 IDE 必选）：TraeWork、workbuddy
   - 国家财政数据案例演示：同一 Prompt 分别在 Trae、Cursor 里跑通
   - Prompt三原则（清晰性、上下文、约束）在实操中自然体验，不单独讲解
   > 个人项目仓库与 AGENTS.md 有意安排在 W2 随 opencode 课堂创建（先创建、再被 opencode 读取），本周不需要。
4. 互助小组组建
5. 补充：常见数据分析社区（Kaggle、Hugging Face、雪球/股吧/知乎等国内社区）

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| 概念与公约 | [课程展示站](https://haichaozheng.github.io/data-analysis-showcase/)（替代表灯） | 固定点击顺序见下；学生手机同步打开。PBL 循环（Challenge→Gap→Knowledge→Apply）站点未单列，用白板画一轮即可 |
| 现场主演示 | Trae **和** Cursor（同一仓库、同一句 Prompt） | 国家财政数据探索；课前两套 IDE 都登录并能打开回退仓库，超时即切回退 |
| 学生跟做 | 自选 Trae 或 Cursor（跟教师演示中自己装的那一边） | 安装验证 + 提出 3 个问题 |
| 不做 | 另做一套概念 PPT；强制全班只用其中一家；TraeWork / workbuddy 当投影主工具；网页 Chat 代替写代码 | 进阶体验留课外 |

**展示站课堂点击顺序（约 20–25 分钟，勿六页都逛）：**

1. [首页](https://haichaozheng.github.io/data-analysis-showcase/)：一人一产品、公开路演——这就是学期终点的公众入口
2. [课程简介](https://haichaozheng.github.io/data-analysis-showcase/intro.html)：PBL + DSR、一人公司、AI 工具栈渐进融入（**跳过「评分结构一览」**，该段已过时，以实施方案为准：平时 50 + 个人项目 50）
3. [项目之旅](https://haichaozheng.github.io/data-analysis-showcase/timeline.html)：四阶段 17 周，停在 W1 本周要做什么
4. [课程公约](https://haichaozheng.github.io/data-analysis-showcase/rules.html)：师生共建——读 2–3 条，当场改，不要宣读全文
5. [精彩项目](https://haichaozheng.github.io/data-analysis-showcase/projects.html)：只用来说明「作品会挂在这里」；路演细则（海报展/精选 Demo）已改为全员路演+现场试用，口头一句即可

教室网络不稳时：课前把站点存成本地 `index.html` 或开一份离线备份。

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：在课程群发 `weeks/week01/python-setup.md`，要求带电脑前装好 Python 3.13，并自选装好 Trae **或** Cursor（不要两个都当作业）；展示站离线备份可打开；教师机 **Trae 与 Cursor 都已登录**，同一财政数据小仓库两边都能跑。

**第1节 · 定向（45 分钟）**

1. **开场（5 分钟）**：一句话点明学期终点（公开产品 + 路演）；并说清「小白第一胜是环境能跑 + 能判断 AI 对错，不是先学会 Python」。白板写求助四步；学生打开展示站。
2. **展示站走读（20 分钟）**：按上文点击顺序（首页 → 简介 → 项目之旅停在 W1 → 公约读 2–3 条 → 精彩项目一句）。跳过「评分结构一览」。
3. **白板画学习循环（12 分钟）**：Challenge→Gap→Knowledge→Apply，用「想看财政数据却不会读文件」举例；点明角色从听课转到做产品。
4. **公约共建（8 分钟）**：就 1 条有争议的公约当场改措辞，记入课程群；不宣读全文。

**第2节 · 演示（45 分钟）**

5. **Python 验收 + IDE 自选（15 分钟）**：先全班终端跑 `python --version`（须为 3.13.x）。当众说明：**Trae（国内）和 Cursor（国外）都认，按偏好与网络选一个，课堂两边都会演示。** 未装 Python 的按 `python-setup.md` 当场补；未装 IDE 的选一边安装。教师机先打开 Trae、再打开 Cursor，各演示一次「打开文件夹 / 选中 3.13 解释器」。不装 Anaconda、不点官网首页 3.14。小白只跟自己选的那一边的三步：打开文件夹 / 选解释器 / 把报错贴回去。
6. **财政数据演示（20 分钟）**：同一仓库、白板上同一句 Prompt，**先 Trae 跑一遍、再 Cursor 跑一遍**（各约 10 分钟）：读入、看一张表、提 1 个问题并让 AI 辅助出图；超时切回退仓库。Prompt 三原则只在这一问里点破。示范问话：「用 pandas 读取这个 csv，打印行数、列名和第 1 个数值列的均值」。
7. **学生开做（10 分钟）**：用自己选的 IDE、同一数据集先跑通「能读文件」。小白先复制教师问话再改一列名；会的人自己提问。

**第3节 · 跟做与组织（45 分钟）**

8. **探索与排障（18 分钟）**：每人起草 3 个有趣问题；教师巡视，安装问题走课程群。
9. **组建互助小组（15 分钟）**：鼓励 5 人一组；每人写背景/技能/兴趣 + 对「一人公司+互助小组」的一句话。
10. **社区调研方法（12 分钟）**：投影雪球/股吧/知乎各 1 例；示范记录（社区名、观察什么、记原话）。布置本周交付与作业；TraeWork 留课外。技能小练见 `lab.md`，本节已满 45 分钟，课后提交。

## 项目活动

**必做**
1. 按 `weeks/week01/python-setup.md` 安装 **Python 3.13（官网，不要 Anaconda，不要首页 3.14）**，并按偏好安装 **Trae 或 Cursor（二选一，都认）**；终端 `python --version` 能打印 3.13
2. 用AI辅助编程完成环境配置（在自选 IDE 里选中上述解释器；`pip install pandas openpyxl`）
3. 国家财政数据探索练习（用自选 IDE 实操），提出3个有趣问题
4. 小组活动：识别发现更多感兴趣的社区，注册并融入社区（设计社区调研方法：如何融入、观察什么、记录什么）

**进阶（可选）**
- 用 TraeWork / workbuddy 对自己感兴趣的财经话题做一次深度调研

**兜底**
- 电脑装不上环境/性能不足：先借机房或同学环境完成课堂演示，把报错截图带到课堂互助组，不影响本周交付
- **编程小白**（没写过 Python 也走主活动，不另开语法课）：本周只要求自选 IDE 能打开文件夹、让 AI 读财政数据并本地跑通、对 1 个结果写「信/不信，因为」。语法不讲；周末自愿看阅读材料里的 Python 入门即可。互助组混编（每组至少 1 人能装环境）。完整路径见总方案「编程小白路径」。

## 交付物（评分锚点）

- 互助小组名单（每人专业背景/技能优势/兴趣方向 + 对"一人公司+互助小组"模式的一句话理解 + 环境配置记录）
- 社区列表（发现并记录感兴趣的社区）
- 社区调研方法设计（如何融入社区、观察什么、记录什么）

—— 规格与知识锚定见 milestones §1.1；计入平时成绩（形成性）。提交前自检：名单是否含背景与互助设想？社区方法能否直接指导 W2 的"加入并倾听"？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。账号/安装类问题直接走 ③。

## 课后作业

1. 完成小组协议：团队成员、我们的约定、签字（提交打印版）
2. 完成环境配置并验证（`python --version` 截图 + 自选 IDE 能跑通读表脚本）
3. 用自选 IDE（Trae 或 Cursor）探索国家财政数据集，提出3个有趣问题
4. 阅读课程公约，思考个人学习目标

## 学习资料

- `weeks/week01/python-setup.md`（Python 3.13 官网安装 + Trae 或 Cursor 选解释器；**不要 Anaconda、不要点首页 3.14**；W2 再配项目 `.venv`）
- `knowledge/phase1-1-1-pbl-learning.md`
- `knowledge/phase1-1-2-ai-assisted-coding.md`
- 课程展示网站：[https://haichaozheng.github.io/data-analysis-showcase/](https://haichaozheng.github.io/data-analysis-showcase/)
- Python 官网：[https://www.python.org/downloads/](https://www.python.org/downloads/)
- Trae官网：[https://www.trae.ai](https://www.trae.ai)
- Cursor官网：[https://cursor.com/cn](https://cursor.com/cn)
