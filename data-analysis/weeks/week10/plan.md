# Week 10 教学计划

## 主题

GitHub 基础 + 打磨迭代 + 上线部署（首选 Streamlit Cloud）

> **前置**：须已完成 W9 同侪互评。本周先补上 GitHub 基础——第 1 节把第一个项目（练手项目 `my-first-github-project`）当堂推上 GitHub，第 2 节就在它上面加一个**无密钥的最小应用**并部署到 Streamlit Cloud（主干先通，不依赖课后作业）；第 3 节再部署带密钥的真项目 v0.4——密钥用平台 Secrets 管理。需要数据库写入、常驻进程或自定义域名的产品走腾讯云自建（进阶）。W11 只做验收与触达，不再新做部署工作。

## 本周学习目标

- 能独立走通"本地项目上 GitHub"六步（init → `.gitignore` → status 验证 → add → commit → 建远程仓库 → push），说清每条命令各做什么、`.gitignore` 为什么必须存在、`.env` 为什么永不入库（当堂以 `my-first-github-project` 练手，课后迁移到个人项目）
- 能按反馈优先级排序完成 v0.4 定向打磨，并说明"为什么先做这些"
- 能把最小应用（无密钥）部署到 Streamlit Cloud 并公网可访问：说清部署五步（代码上仓 → 依赖清单 → 平台配置 → 验证 URL）——第 2 节当堂以练手项目完成
- 能把带密钥的 v0.4 部署上线：密钥从本地 `.env` 换到平台 Secrets，说清与本地运行的关键区别
- 能说明 Streamlit Cloud 的三个约束（闲置休眠冷启动、资源限额、文件系统临时性）对产品的影响，以及什么时候才需要升级到自建服务器
- 能对照 DSR 七指导原则完成 MVP 阶段自检

## 预计投入
课堂 3×45 分钟。课外 8-10h（第 1、2 节当堂完成练手仓库的推送与最小应用部署，个人项目迁移课后完成；真项目部署本身 30 分钟内可完成；主要时间花在 v0.4 打磨——互评反馈优先级排序移至课外、写入 journal——与补齐"依赖、密钥、数据"三件事）

## 教学内容
1. GitHub 基础：一次性身份配置（`git config`）与 git 六步工作流（init / `.gitignore` / status / add、commit / 建远程仓库 / push），**逐条命令讲含义**；教师演示项目 `my-app-2026`（`.env` 密钥、`.venv` 环境、`__pycache__` 缓存三件套不入库），学生当堂练手项目 `my-first-github-project`（最小化：仅一个 README.md，个人项目迁移课后完成）
2. 据反馈定向打磨与技术债清理
3. Streamlit Cloud 部署（首选）：第 2 节以最小应用（无密钥）当堂走通五步（GitHub 仓库 → streamlit.io 一键部署）；第 3 节部署真项目，密钥用平台 Secrets 管理
4. 部署三件事：依赖（`requirements.txt` 冻结）、密钥（`.env` → 平台 Secrets，永不入库）、数据（随仓库 / 启动现场拉取 / 外部存储）；公网 vs 本地的关键区别
5. 托管平台约束：休眠冷启动、资源限额、临时文件系统（SQLite 只读可用，写入会丢）
6. 进阶自建路线：腾讯云轻量/CloudBase（校园免费额度；需数据库写入、常驻进程、自定义域名者）
7. 如何做阶段回顾：DSR 自检可写入本周提交的 `journal.md`，不另开反思文件

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| 概念 | 薄幻灯 + 白板 | 本地文件夹 vs git 仓库（`.git` = 时光机）；GitHub 是什么；公网 vs 本地；托管平台 vs 自建服务器；Streamlit Cloud 三约束（休眠/限额/临时文件系统） |
| 现场主演示（第1节） | 终端 + GitHub 网页 | 独立示例项目 `my-app-2026` 的**干净副本**（未 init，仓库外文件夹）：一次性身份配置 + git 六步当堂走完，最后一幕停在"仓库页面上看不到 `.env`" |
| 现场主演示（第2节） | 浏览器（streamlit.io） | 从练手仓库部署最小应用到 Streamlit Cloud：五步走完、当堂出公网 URL（无密钥版）；现场 `git push` 演示自动重新部署 |
| 现场主演示（第3节） | 浏览器（streamlit.io） | `my-app-2026` 演示密钥上云：Settings → Secrets（TOML 格式）配好密钥后 AI 功能生效——真项目与练手项目的唯一区别 |
| 学生跟做 | 浏览器 + 终端 | 第 1 节当堂以最小练手项目 `my-first-github-project` 走通 push（个人项目迁移为课后必做）；第 2 节当堂给它加最小应用并部署出 URL（无密钥）；第 3 节部署自己的 v0.4（含 Secrets）——人人出 URL |
| 不做 | 腾讯云控制台当场申请 | 自建路线的申请与排障留课后进阶（校园额度审核有等待期，选此路线者周初就申请） |

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前（教师）：`git --version` 可用；**备两份 `my-app-2026` 副本**——①已推上 GitHub 的（第 1 节打开仓库页面，给学生看"终局长什么样"）＋②未 `git init` 的干净副本（当堂从零演示六步用）；**最小应用示例仓库已推 GitHub 并已部署出 URL**（第 2 节演示对照：8 行复利计算器 + requirements.txt 一行 streamlit）；教师演示仓库可一键部署出 URL；`deployment-faq.md` 可投影；v0.4 演示产品能打开。课前（学生，提前 3 天课程群通知）：**装好 git**——Windows 到 <https://git-scm.com/download/win> 下载 Git for Windows，安装一路默认下一步，装完在终端输 `git --version` 能出版本号即成功（Git Bash 与 PowerShell 均可；镜像与详细步骤见 `weeks/week10/github-lab.md` 附录 A）；**确认 W2 建的 GitHub 账号能登录**——8 周未用，忘密码者先自行找回，登录不了的课前必须解决（本节全程依赖账号，账号不通等于缺席）；打开 `templates/dsr-checklist.md` 预览七原则。`github-lab.md` 课程群同步发放，学生跟做照它逐步执行。

**第1节 · GitHub 基础：把项目推上 GitHub（45 分钟）**

1. **为什么需要 GitHub（7 分钟）**：不另做幻灯，白板画三格。①本地文件夹 vs git 仓库——`.git` 目录就是"时光机"，`commit` 是存档点，改坏了随时回退；②GitHub 是什么——git 仓库的云端托管 + 协作平台，`push` 把本地存档同步上云；③对本课程的两个真实用途：代码云端备份（毕业不丢）、**下节课部署的地基**（Streamlit Cloud 直连 GitHub 仓库一键部署）。用教师自己的 `my-app-2026` 现场打开 GitHub 页面佐证。
2. **主演示：一次性配置，然后 git 六步（15 分钟）**：在 `my-app-2026` **干净副本**（未 init 的文件夹，强调：它不在任何 git 仓库内，和学生将要建的练手文件夹一样）当堂走完。**每条命令单独敲、单独讲含义**——让学生知道每条命令"做什么、做完世界有什么变化"，而不是抄咒语。先讲"开场命令"（每台电脑只做一次）：
   ⓪ **一次性身份配置**：`git config --global user.name "你的名字"`、`git config --global user.email "你的邮箱"`——不做这个，后面第一次 `commit` 会被 git 拒绝（"Please tell me who you are"）。两行规则不同，向学生讲清：
   - `user.name`：**自由署名**，不是账号、无需注册、git 不验证——但会公开出现在提交历史里，填真实姓名或固定昵称（能对上人即可，互评追溯作者全靠它）；
   - `user.email`：**必须填 GitHub 账号绑定的注册邮箱**（不记得去 GitHub → Settings → Emails 查）——git 本身不验证，但 GitHub 靠邮箱匹配提交：对得上才关联你的头像和贡献绿格，对不上就是灰色无名作者（零基础学生随手填 QQ 邮箱然后困惑"为什么我的提交没有头像"是必踩坑，提前讲掉）。不想暴露真实邮箱者，用同一页面的隐私邮箱（形如 `12345+用户名@users.noreply.github.com`），效果等同。
   同时预告：**第一次 `push` 会弹出浏览器要求登录 GitHub，登录即认证通过，属正常现象**——注意 `git config` 只是署名、不负责验证权限，真正的验证就是这次浏览器登录；账号开了两步验证者，登录时按提示输一次验证码。**凭证登录后由系统缓存（每台电脑只此一次）**，之后每次 `git push` 静默通过、不再弹窗也不要验证码；只有换电脑/重装系统/凭证过期才需重新登录一次。
   六步正片（命令逐条讲，含义讲到"学生能向别人复述"的粒度）：
   ① `git init`
      ——在当前文件夹里创建一个隐藏的 `.git` 目录，从此这个文件夹是 git 仓库，git 开始记录其中一切变化。**只是"开始记账"，不上传任何东西**。
      `git branch -M main`
      ——把当前分支改名为 main（`-M`＝强制改名）。分支可先理解为"时间线的名字"；不同电脑默认名可能是 master 也可能是 main，统一成 main 是为了第 ⑥ 步 push 不报错。照抄即可，不展开原理。
   ② 写 `.gitignore`（非命令：编辑器里新建文件）——声明 `.env`（密钥泄露）/`.venv`（环境，换机器重新生成）/`__pycache__`（缓存）不入库。
   ③ `git status`
      ——查看"现在什么状态"：哪些文件变了、哪些还没被 git 跟踪。**无副作用、随时可敲**，是今后用得最多的命令；本节用它验证 `.gitignore` 生效：**列表里看不到 `.env`**。
   ④ `git add .`
      ——把当前文件夹的全部改动放进"暂存区"，相当于勾选"这次要存档哪些文件"（`.`＝全部；也可 `git add README.md` 只勾一个文件）。
      `git commit -m "第一版：股价波动预测 APP"`
      ——把暂存区打包成一个存档点（commit）；`-m` 后引号里是这一版的说明，写给未来的自己看。**commit 只发生在本地，不上传**。
   ⑤ GitHub 网页 New repository 建远程仓库（非命令；名字建议与文件夹同名；Public/Private 均可，下节课要部署者选 Public 最省事）。
   ⑥ `git remote add origin <URL>`
      ——登记远程仓库地址：`origin` 是给这个 URL 起的别名（惯例如此），以后不必再敲长 URL。**只是登记，不上传**。
      `git push -u origin main`
      ——真正上传：把本地 main 分支的全部 commit 发送到 origin；`-u`＝记住这对关联，**以后只敲 `git push` 即可**。
   板书一条主线帮学生建立整体图景：`add` 勾选 → `commit` 打包存档（本地，断网也能做）→ `push` 上传（云端，需要网络）。
   收束停在仓库页面：**能看到 app.py / README / requirements.txt，看不到 .env**——这一幕就是本节课的验收标准。
3. **学生跟做（18 分钟）**：**不用自己的项目**——先建最小练手项目走通全流程，流程长在手上，下一次才敢往真项目上用。
   - 新建文件夹 `my-first-github-project`，里面只放一个 `README.md`（内容一行字即可，如"我的第一个 GitHub 仓库"）；
   - 在该文件夹里走 ⓪—⑥（⓪ 已做的跳过）：`.gitignore` 照建——练手项目里暂时没东西可忽略，放到个人项目里马上就有用；commit 消息写"第一版：我的第一个 GitHub 项目"；GitHub 建仓时名字就叫 `my-first-github-project`；
   - push 成功的标志：刷新仓库页面，能看到自己的 README——举手示意，教师统计通过率。
   教师巡场，四类高频卡点现场答疑：课前没装 git（现场装：浏览器打开 <https://git-scm.com/download/win>，点击 **Click here to download** 下载，双击安装一路默认下一步，装完**重开一个终端**再敲 `git --version` 验证；若官网下载慢，用国内镜像 <https://npmmirror.com/mirrors/git-for-windows/> 选最新版 `64-bit.exe` 安装）、push 卡认证（弹浏览器登录 GitHub 即通过，预告过属正常）、`push -u origin main` 报错找不到分支（漏了 `git branch -M main`，或 remote URL 粘贴错）、远程仓库建错名字/公私选错（删了重建，30 秒的事）。
4. **收束（5 分钟）**：`git log` 看历史——每一次 commit 都是一条可回退的记录；一句话带走："**commit 是存档点，push 是同步到云端，`.env` 永不入库**"。布置迁移作业：把 ⓪—⑥ 原样用到自己的个人项目文件夹（第二次会快得多；即必做①，仓库需含 `README.md`、`requirements.txt`、`.gitignore`）。预告：下节课用你自己的 GitHub 仓库一键部署出公网 URL。

**第2节 · 最小应用上云：GitHub → Streamlit Cloud（45 分钟）**

5. **给练手项目加一个最小应用（15 分钟）**：上节课的 `my-first-github-project` 只有一个 README，今天给它加一个能跑的应用——**特意不用任何 API key / tushare token**：密钥上云是下节课的内容，本节先把"部署"这条主干走通。学生照 `Streamlit-Cloud-lab.md` 第 1-3 节逐步执行——一个 8 行的**复利计算器**（金融主题、带交互滑块、零密钥零外部数据），代码文档里有、复制粘贴即用：

   ```python
   import streamlit as st

   st.title("我的第一个云端应用")
   st.write("这是我在数据分析课上部署的第一个 Streamlit 应用。")

   years = st.slider("投资年限（年）", 1, 30, 10)
   rate = st.slider("年化收益率（%）", 1, 20, 5)
   result = 10000 * (1 + rate / 100) ** years
   st.metric("1 万元到期本息", f"{result:,.0f} 元")
   ```

   - 新建 `app.py` 粘贴保存；新建 `requirements.txt`，内容一行 `streamlit`——**这是部署平台的"购物清单"**：云端机器像酒店房间，Linux/Python/pip 等"水电家具"配好了，但你项目的包一件没有，构建时照清单装；清单上没有的包云端一概没有（缺了就报 `ModuleNotFoundError`）；
   - 本地验证（复用 W3 venv 技能，在项目文件夹）：`py -3.13 -m venv .venv` → 激活 → `pip install -r requirements.txt` → `streamlit run app.py`，浏览器自动打开本地页面，拖滑块看数字变；**教室网络慢、装不动的可跳过本地验证直接部署**——云端构建本身就是一次检验；
   - 第 2 次日常循环：`git status`（观察 app.py 此刻在 Untracked files）→ `git add .`（挪进 Changes to be committed）→ `git commit -m "新增：复利计算器应用"`（列表变干净）→ `git push`——上节课的 add/commit/Untracked 概念全部对上号。
6. **主演示：部署五步，无密钥版（12 分钟）**：教师用自己的最小应用仓库演示（与学生同路径）：
   ① 确认代码已 push（仓库页面能看到 `app.py` 和 `requirements.txt`）；
   ② 浏览器打开 streamlit.io → **Sign in with GitHub**（用 GitHub 账号登录，第一次会请求授权，点授权即可）；
   ③ New app → 选仓库 `my-first-github-project` → 分支 `main` → Main file path 填 `app.py`；
   ④ 无需任何密钥配置——最小应用不需要，真项目的 Secrets 下节课讲；
   ⑤ 点 Deploy，等 1-3 分钟构建，得到 `https://xxx.streamlit.app` 公网 URL。
   **wow 时刻（必演）**：当场改 app.py 一行字（如标题）→ `add` → `commit` → `push` → 回浏览器刷新，页面几十秒后自动更新——**git push 即上线**，这就是"部署连着 GitHub 仓库"的含义。
7. **公网 vs 本地的三个关键区别（5 分钟）**：趁学生刚看到部署，点三个概念（每个 1-2 分钟）：①无状态——容器重建即清，SQLite 只读可用、写入会丢；②休眠与冷启动——闲置后首访等 10-30 秒，路演前先预热；③密钥——本地靠 `.env`，云端要换到平台 Secrets（下节课真项目就要配）。收束："部署就三件事——依赖、密钥、数据；今天搞定了依赖，密钥下节课。"
8. **学生跟做部署（13 分钟）**：照 `Streamlit-Cloud-lab.md` 第 4-5 节部署自己的 `my-first-github-project`（上节课人人当堂 push 过，不依赖课后作业——这是用练手项目部署的最大好处）；出 URL 者当场发课程群（计当堂表现），并用**手机**打开自己的 URL——"我的应用全世界都能访问了"。高频报错对照 `deployment-faq.md` 现场答疑：仓库列表里找不到自己的仓库（GitHub 授权没给全，或仓库是 Private——去 GitHub 仓库 Settings 改 Public 最省事）、构建后页面报 `ModuleNotFoundError`（requirements.txt 没提交或漏写包）、页面一直 Preparing（首次构建慢，等 2-3 分钟再刷新）。

**第3节 · 真项目上云：密钥 + 部署工作坊 + 方案自检（45 分钟）**

9. **部署前检查 + 密钥上云演示（12 分钟）**：学生照 `Streamlit-Cloud-secrets-lab.md` 推进。先做检查清单自查（2 分钟，对自己的 v0.4 文件夹）：
   - [ ] `requirements.txt` 存在且与本地 `pip list` 一致（注意 `python-dotenv` 别漏）
   - [ ] `.env` 在 `.gitignore` 中（第 1 节已建，`git status` 复核看不到）
   - [ ] 代码里无硬编码路径 `C:\...`（用 `pathlib.Path`）
   - [ ] 数据文件 >50MB 的不进 git（改为启动时拉取或手动上传）
   - [ ] 代码里 `os.getenv()` / `st.secrets` 读取密钥（未硬编码）
   主演示：真项目与上节课练手项目的**唯一区别 = 密钥**。本地靠 `.env`（被 `.gitignore` 挡在仓库外——所以云端根本拿不到）；云端配 **Secrets**：app 页面 Settings → Secrets，TOML 格式逐行写 `TUSHARE_TOKEN = "..."`、`DEEPSEEK_API_KEY = "..."`；代码端改为文档 2.2 节的**兼容写法**（`get_key()`：本地 `.env` 优先、云端 `st.secrets` 兜底，一份代码两头跑）。用 `my-app-2026` 演示配好 Secrets 后 AI 预测功能生效。
10. **部署工作坊（15 分钟）**：部署自己的 v0.4（个人项目还没推上 GitHub 的先花 3-5 分钟补推——第 1 节流程，第二次很快）；先过检查清单，再配 Secrets；已出 URL 者换手机热点/异地网络各验证一次，体验冷启动。卡住者自查四类：上节课三类报错 + 新增 **AI 功能失效**（Secrets 没配/键名不一致/TOML 格式错——等号、引号都不能少）；三招仍不通带"三件套"（报错截图、执行的命令、部署平台）走互助组/课程群；仍未通过的用 `mvp-template` 部署占位 URL 保底。
11. **部署方案文档（10 分钟）**：五部分——①部署目标与公网 URL；②路线选择理由（Streamlit Cloud 为何够用/何时不够）；③密钥管理方式（Secrets，无一入 git）；④数据方案（哪些随仓库、哪些启动现场拉取、哪些将来要外部存储）；⑤升级触发条件（什么情况才需要腾讯云：数据库写入、常驻进程、自定义域名）。当堂起笔写第①②部分，其余课后完成。
12. **DSR 自检与收束（8 分钟）**：学生对照 `templates/dsr-checklist.md` 七原则逐条给自己的 MVP 打 ✓/△/✗（3 分钟自评 + 2 分钟邻座互看）。写进本周提交的 `journal.md`，不另开反思文件。部署成功即触达起点——W11 当堂把链接发班级群/社区，反馈滚到 W14。腾讯云自建为进阶可选。当日在 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）。互助记录只写「谁帮了你、对项目有何影响」，没有则写「无」。提醒：本周提交截至今日的 `journal.md` 全文作为作业。本周无技能小练。

## 项目活动

**必做**
1. 把个人项目推上 GitHub 个人仓库：当堂已在 `my-first-github-project` 练手，课后把 ⓪—⑥ 迁移到个人项目；仓库含 `README.md`、`requirements.txt`、`.gitignore`，且 `.env` 未入库（`git status` 与仓库页面双重验证）
2. 完成根据互评反馈的定向打磨（反馈优先级排序——按"用户最痛 × 改动最小"排前 3 项，写入 `journal.md`——课外完成，作为打磨依据），产出 v0.4（可演示：主路径 3 分钟能走完、无阻塞报错）
3. 把 v0.4 部署到 Streamlit Cloud，公网可访问（提交 URL；自建路线部署成功验收等同。第 2 节已当堂完成练手项目的无密钥部署，本项为带密钥的真项目）
4. 撰写个人上线部署方案（五部分，见第 3 节第 11 步）

**进阶（可选）**
5. 自建路线（腾讯云轻量/CloudBase，校园免费额度——**审核有等待期，周初就申请**）：适合需要数据库写入、常驻进程、自定义域名的产品；两条都走通者写一段资源/运维/成本对比
6. 绑定自定义域名、挂 UptimeRobot 免费可用性监控

**兜底**
- 当堂未出 URL：课后 48h 内对照 `weeks/week10/deployment-faq.md` 排障；仍不通先用 `mvp-template` 部署一个占位 URL 保底，再排查自己的 v0.4；W11 录屏兜底须附补齐计划

## 交付物（评分锚点）

- GitHub 个人仓库 URL（含 README、requirements.txt、.gitignore；.env 未入库）
- 个人MVP v0.4（打磨版，可演示）
- 公网可访问的部署 URL（首选 Streamlit Cloud）
- 个人上线部署方案（路线理由 + 密钥管理 + 数据方案 + 升级触发条件）

—— 规格与知识锚定见 milestones §2.7；计入平时成绩（形成性）。提交前自检：仓库里看不到 `.env`？打磨项有优先级排序与理由？路线选择是"够用优先"而非"听说高级"？密钥无一硬编码、无一入 git？数据方案考虑了 W11 触达与 W12-W15 建模增强的集成？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。git 卡点（认证/分支名/身份配置）优先对照第 1 节四类高频卡点自查；部署排障先查《部署排障 FAQ》第一/四/五类；选腾讯云进阶路线者，额度审核类问题直接走 ③ 并注明时限。

## 课后任务
1. 给互评反馈项排序（"用户最痛 × 改动最小"排前 3），写入 `journal.md`，据此完成产品打磨
2. 完成部署并测试公网访问（手机热点/异地网络各一次），提交 URL
3. 完成部署方案；提交个人仓库 `journal.md`（截至本周的全文，作为作业）

## 学习资料
- `weeks/week10/github-lab.md`（实验一·**学生跟做主文档**：⓪—⑥ 逐条命令含义、常见报错速查、课后迁移指引、7 条命令速查卡；课前随通知发放）
- `weeks/week10/Streamlit-Cloud-lab.md`（实验二·第 2 节学生跟做主文档：最小应用代码 + 部署五步无密钥版 + "push 即上线"体验）
- `weeks/week10/Streamlit-Cloud-secrets-lab.md`（实验三·第 3 节学生跟做主文档：**本地 `.env` / 云端 Secrets 兼容写法** `get_key()`、Secrets 配置指引、密钥体检开关）
- 教师示例仓库：<https://github.com/haichaozheng/my-app-2026>（第 1 节主演示对照用；学生当堂练手项目为自建的 `my-first-github-project`）
- git 官方教程（Pro Git 中文版，读第 1-2 章）：<https://git-scm.com/book/zh/v2>
- GitHub 官方上手指南（Hello World / 管理仓库）：<https://docs.github.com/zh/get-started>
- Streamlit Community Cloud 官方部署文档：<https://docs.streamlit.io/deploy/streamlit-community-cloud>（Deploy an app 一页走完五步）；Secrets 管理：<https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/secrets>
- `templates/journal.md`（本周提交仓库中截至当周的全文）；`templates/journal-rules.md`（交法）
- `knowledge/phase3-3-1-cloud-deployment.md`（部署方案对比、工作流、易错点）
- `weeks/week10/deployment-faq.md`（部署排障 FAQ：试部署与 W11 验收随查）
- 视频资料（超星学习通，详见 `video-resources.md`）：8.1 数据库基础 + 8.2 关系数据库标准语言SQL（推荐：SQLite 随仓库/随镜像做只读数据时的底子）；8.3 Python操作MySQL（进阶：自建路线选 MySQL 者再学）
