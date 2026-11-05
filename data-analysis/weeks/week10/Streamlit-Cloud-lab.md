# W10 实验二：把最小应用部署到 Streamlit Cloud

> 给谁：第 2 节当堂跟做，课后自己重走一遍也行。  
> 前提：已完成实验一（`github-lab.md`）——`my-first-github-project` 已 push 到 GitHub。  
> 产出：一个全世界都能访问的公网 URL（`https://xxx.streamlit.app`）——手机也能打开。  
> 全程约 30 分钟。

---

## 0. 三句话搞懂「部署」

- **部署** = 把你的应用放到一台 24 小时开机的云电脑上，任何人输入网址就能用——不再需要你开着终端跑 `streamlit run`。
- **Streamlit Cloud**：Streamlit 官方的免费托管平台，**直连 GitHub 仓库**——代码在仓库里，它负责运行；以后你 `git push`，网站自动更新。
- 本实验**不用任何密钥**（API key / token 都不需要）——先把「部署」这条主干走通；带密钥的真项目是下一个实验（`Streamlit-Cloud-secrets-lab.md`）。

> 类比：GitHub 仓库是「剧本」，Streamlit Cloud 是「剧场」——剧本更新了，剧场自动换新戏。

---

## 1. 给练手项目加一个最小应用

打开 `C:\my-first-github-project`，我们要加两个文件。

### 1.1 新建 app.py——应用本体

在文件夹里右键 → 新建 → 文本文档 → 命名 `app.py`，用记事本打开，粘贴以下代码，保存：

```python
import streamlit as st

st.title("我的第一个云端应用")
st.write("这是我在数据分析课上部署的第一个 Streamlit 应用。")

years = st.slider("投资年限（年）", 1, 30, 10)
rate = st.slider("年化收益率（%）", 1, 20, 5)
result = 10000 * (1 + rate / 100) ** years
st.metric("1 万元到期本息", f"{result:,.0f} 元")
```

代码在干什么（看得懂就行，不用会写）：

- `st.title` / `st.write`：页面上的大标题和一行文字；
- `st.slider`：两个可拖动的滑块（年限、收益率）——`1, 30, 10` 表示最小 1、最大 30、默认 10；
- `st.metric`：一个大数字卡片，按复利公式算 1 万元到期变成多少。

这是一个**复利计算器**：金融主题、有交互、但零密钥零外部数据——正适合走通部署。

### 1.2 新建 requirements.txt——云端的「购物清单」

同样方式新建 `requirements.txt`，内容只要一行：

```text
streamlit
```

**为什么必须有它**：云端那台机器像一个**酒店房间**——床、水电（Linux 系统、Python 解释器、pip 装包工具）都是配好的，但**你的行李一件没有**。Streamlit Cloud 构建时会照着 `requirements.txt` 这份清单，用 pip 把你项目用到的包装进去——**清单上没有的包，云端一概没有**，缺了运行就报 `ModuleNotFoundError`（本实验只用到 streamlit 一个包，所以只写一行；真项目的清单会长得多）。

> **细心的同学会问**：平台不是自带 streamlit 吗（不然它怎么运行你的应用），为什么清单里还要写？
> 你说得对——Streamlit Cloud 默认装好了 streamlit，**漏写它，应用也能跑**。但 `requirements.txt` 的服务对象不是这一个平台，而是**任何一台新机器**：同学克隆你的仓库想在本地跑 `pip install -r requirements.txt`（本地是裸环境，没有 streamlit）；你以后换部署平台（腾讯云等）也没有"自带"待遇；想锁定版本（如 `streamlit==1.65.0`）更必须写。
> 一句话：**清单写全，仓库才自解释**——别人拿到你的仓库，在任何机器上都能复现，这就是它存在的意义。

> ⚠️ **老坑重现（实验一提过）**：资源管理器若不显示文件扩展名，你新建的文件可能实际叫 `app.py.txt`、`requirements.txt.txt`——本地看不出破绽，但**云端严格按文件名找文件**，名字多一截就报「找不到 app.py」。不确定就先开「查看 → 勾选文件扩展名」，确认两个文件名干干净净、没有多余的 `.txt`。

---

## 2. 本地先跑一遍（可选；教室网络慢可跳过）

保险起见，先在自己电脑上确认应用能跑（复用 W3 的虚拟环境技能）。在项目文件夹打开终端（资源管理器进入 `C:\my-first-github-project` → 地址栏输 `powershell` → 回车），依次执行——**以下为 Windows 命令；Mac 的对应命令在本节末尾**：

```text
py -3.13 -m venv .venv
```

含义：在本文件夹建虚拟环境 `.venv`（W3 学过——包只装进本项目，不弄脏系统）。

```text
.\.venv\Scripts\activate
```

含义：激活环境，提示符前出现 `(.venv)` 即成功。若提示「禁止运行脚本」：先执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，回答 `Y`，再重新激活。

```text
pip install -r requirements.txt
streamlit run app.py
```

含义：照清单装包，然后启动应用。浏览器会自动打开 `http://localhost:8501`——拖动滑块，看数字变。**注意地址栏是 localhost（本地）——只有你自己能看，这就是为什么需要部署。** 看完回到终端按 `Ctrl + C` 停止。

**Mac 用户**：打开「终端」（聚焦搜索 `terminal`），`cd` 进入项目文件夹后依次执行（与 W3 一致）：

```text
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

其余步骤（git 命令、部署操作）Windows 与 Mac 完全相同。

> 顺手观察一个彩蛋：现在文件夹里多了 `.venv`（几百 MB），但敲 `git status` **看不到它**——实验一建的 `.gitignore` 一直在默默干活（它的三行名单里就有 `.venv/`）。跳过本地验证的同学也没关系：云端构建本身就是一次检验。

---

## 3. 第 3 次日常循环：把新文件推上 GitHub

还在项目文件夹的终端里（不放心就敲 `pwd` 确认结尾是 `my-first-github-project`；**跳过了第 2 节、终端没开的同学**：用实验一的老办法——资源管理器进入 `C:\my-first-github-project` → 地址栏输 `powershell` → 回车）：

```text
git status
```

观察：`app.py` 和 `requirements.txt` 出现在 **Untracked files**（git 看见了，还没管——实验一讲过的概念）。

```text
git add .
git commit -m "新增：复利计算器应用"
git push
```

含义：勾选 → 打包存档 → 上传（肌肉记忆三连击）。push 后再敲 `git status`，会看到 `nothing to commit, working tree clean`——全部归档，干干净净。

**push 成功的标志**：刷新 GitHub 仓库页面，能看到 `app.py` 和 `requirements.txt`。

---

## 4. 部署五步（无密钥版）

### 第 ① 步：打开 Streamlit Cloud，用 GitHub 登录

浏览器打开 <https://share.streamlit.io/>，点 **Sign in with GitHub**（也可能显示 **Continue with GitHub**，同一个东西——用 GitHub 账号登录）：

- 第一次登录会跳到 GitHub 的授权页，点绿色的 **Authorize Streamlit**；
- 之后可能让你填一个邮箱（填你的常用邮箱）→ 点 Continue。

### 第 ② 步：新建应用

点 **New app**（或 Create app）按钮。

### 第 ③ 步：填表——三处必选，一处可选

前三处是「告诉平台去哪拿代码、从哪个文件开始跑」：

- **Repository**：下拉选 `你的用户名/my-first-github-project`（列表里没有？看第 6 节第 1 条）；
- **Branch**：`main`；
- **Main file path**：`app.py`。

最后一处可选，决定你的网址：

- **App URL (optional)**——留空则用预填的随机子域名；想好记就自己填，如填 `zhangsan-my-first-app` → 网址就是 `https://zhangsan-my-first-app.streamlit.app`。规则：只能**小写字母、数字、短横线**；子域名在 streamlit.app **全球所有用户中唯一**，`compound` 这类大众词早被占了——**推荐「GitHub用户名-项目名」**，独一无二又好认；被占用会在 Deploy 时报错，换个名字重来即可。

### 第 ④ 步：点 Deploy，等 1-3 分钟

页面显示 Preparing → Running，**首次构建要 1-3 分钟，别关页面**。

### 第 ⑤ 步：拿到公网 URL

构建完成后自动跳转到你的应用——地址栏的 `https://xxx.streamlit.app` 就是**公网 URL**：复制发到课程群，任何人（不需要 GitHub 账号）点开就能用。

---

## 5. 验收 + 体验「git push 即上线」

**验收（两件事）**：

1. 用**手机**（不连和电脑同一个 Wi-Fi，直接用流量）打开你的 URL——能拖滑块、数字会变 → 部署成功。手机和电脑不在同一个网络也能访问，才证明它是真的挂在公网上，而不是只有你自己能看的 localhost；
2. 把 URL 发到课程群。

**必玩：见证自动化（30 秒）**——这是本周最值得记住的一幕：

1. 本地改 `app.py` 的一行字（如把标题改成 `"我的第一个云端应用 v2"`），保存；
2. 终端三连击：`git add .` → `git commit -m "改标题"` → `git push`；
3. 回浏览器刷新你的 URL——**几十秒后，页面自动变成新版**。

你没有做任何「重新部署」的动作：Streamlit Cloud 盯着你的 GitHub 仓库，push 即更新。**以后你的真项目改版上线，就是这三条命令的事。**

---

## 6. 常见问题速查

| 症状 | 原因 | 解法 |
|---|---|---|
| 第 ③ 步下拉列表里找不到自己的仓库 | 仓库是 Private，或授权时没给全权限 | 最快解法：GitHub 打开该仓库 → Settings → General → 拉到最底 Danger Zone → Change visibility → 改 Public；或 Streamlit 授权页重新授权 All repositories |
| 构建后页面报 `ModuleNotFoundError` | `requirements.txt` 没提交 / 漏写包 | 本地 `git status` 确认它在仓库里；检查清单里有没有漏掉代码 import 的包 |
| 页面一直 Preparing / Running | 首次构建慢 | 等 1-3 分钟再刷新 |
| 打开 URL 显示 "Zzz... this app is asleep" | 免费版闲置后会休眠（冷启动） | 等待 10-30 秒自动唤醒；重要演示前先点开预热 |
| 应用页面右下角有红色报错 | 代码运行出错 | 点右下角 **Manage app** 看日志，把报错截图发课程群 |
| 网页打开很慢、偶尔刷新不出来，但过会儿又能开 | 国内网络访问 `streamlit.app` 时快时慢，**不是你的部署坏了** | 等几秒重试；换网络（手机流量 / 其他 Wi-Fi）再开；路演前先预热并多备一个网络 |
| push 之后网站没更新 | 等的时间不够 / 没刷新 | 等 1 分钟再刷新；还不行看 Manage app 日志 |

---

## 7. 课后

- 体验冷启动：把应用晾 1 小时再打开，感受 10-30 秒的唤醒等待（免费版的代价，路演前要预热）；
- 下节课我们部署**你自己的真项目**——它有 API key / tushare token，密钥怎么安全地交给云端？见下一个实验 `Streamlit-Cloud-secrets-lab.md`。
