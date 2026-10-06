# W1 环境安装：Python + Cursor + opencode

> 给谁：AI4S 课程第1周，社科类博士生。  
> 目标：电脑上有一个能跑科研脚本的 Python，Cursor 能找到它，opencode 能在项目里接管工作流。  
> 先修假设：你有一定 Python 基础和大模型使用经验。本文只装环境，不讲语法。

本课程统一口径：**官网 Python 3.13 + 项目内 `.venv` + Cursor（编辑器）+ opencode（命令行 AI 助手）**。不引入 Anaconda 作为默认路径，不用 Trae 备选。

---

## 第一部分：安装 Python 3.13

全班统一 **3.13.x（该系列最新补丁）**。官网首页大按钮现在是 3.14，**不要点它**——后面部分金融/社科数据包、云端镜像仍以 3.13 最省事。不要装低于 3.11 的版本。

### 1.1 下载与安装

1. 打开 [Python 3.13 发布页](https://www.python.org/downloads/)，在页面里找 **3.13** 的 Windows installer（64-bit）。不要选 embeddable、不要选 free-threaded（名字里带 `t` 的）。
2. 运行安装程序，**必须勾选** `Add python.exe to PATH`，再点 Install Now。
3. Mac 同样装 3.13，用 `python3 --version` 验收。

### 1.2 验收

关掉安装窗口后，打开 PowerShell（Windows）或终端（Mac），分别输入：

```text
python --version
pip --version
```

应看到 `Python 3.13.x` 和一行 pip 版本。

**Windows 常见坑**：输入 `python` 却弹出微软应用商店。到「设置 → 应用 → 高级应用设置 → 应用执行别名」里，关掉 `python.exe` / `python3.exe` 两个开关，再重开终端试一次。

**已装过 Anaconda 的**：不要卸载。本课在 IDE 里选官网 3.13，不要用 `base`。若终端里 `python` 总是落到 Anaconda 3.9，执行：

```text
conda config --set auto_activate_base false
```

关掉全部终端再开一个新终端。验收：`python --version` 为 3.13，或用 `py -3.13 --version` 确认 3.13 仍在。

**验收一句**：`python --version` 能打印 3.13，本步才算过。把这行截图留给环境记录。

---

## 第二部分：安装 Cursor 并选中 Python

[Cursor](https://cursor.com/cn) 是基于 VS Code 的 AI-first 编辑器，课堂主演示用它。它**不自带 Python**——只装 Cursor、不装 Python，AI 能写代码但一点"运行"就报找不到解释器。

### 2.1 安装与登录

1. 打开 [https://cursor.com/cn](https://cursor.com/cn)，下载并安装。
2. 首次打开时登录（可用 Google / GitHub 账号）。

### 2.2 选中 Python 解释器

这是本周最容易出错的一步，务必当堂完成。

1. 打开一个空文件夹（或教师发的示例项目文件夹）。
2. 按 `Ctrl+Shift+P`（Mac：`Cmd+Shift+P`），输入并选择 **Python: Select Interpreter**。
3. 选中第一步装的 3.13，路径里应有 `Python313`（例如 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python313\python.exe`）。
   - **不要**选 `anaconda3`
   - **不要**选 WindowsApps 里的商店别名
4. 关掉旧终端，新开一个，再跑 `python --version`，应看到 `3.13.x`。

> 只走命令面板（`Ctrl+Shift+P`）这一条路。不要去改系统 PATH 或 settings.json，容易选错。

### 2.3 先装本周要用的包

本周还没有个人项目仓库，先在当前 Python 里装科研脚本要用的包：

```text
python -m pip install wbgapi pandas
```

- **wbgapi**：世界银行数据 API 的 Python 客户端，免费、无需 API key，一行代码拉取各国宏观经济与社会指标
- **pandas**：数据分析基础库，wbgapi 返回的就是 pandas DataFrame

装完让 Cursor 生成脚本：用 wbgapi 拉取中国近 5 年的人均 GDP，打印表格，**必须点运行且终端无报错**。

个人项目的 `.venv` 虚拟环境留到下面第三部分建仓库时再配。

---

## 第三部分：安装 opencode

[opencode](https://opencode.ai/) 是命令行里的 AI 编程助手。本课程从 W1 起用它接管个人项目（读取 `AGENTS.md`、对话生成代码、直接改文件并运行）。它基于 Node.js，要先有 Node，再全局安装 `opencode-ai`（名字必须带 `-ai`，不要装成 `opencode`）。

### 3.1 安装 Node.js

1. 打开 [https://nodejs.org](https://nodejs.org)
2. 下载 **LTS**（现在是 **24.x**，例如 24.21.0）。**不要点 Current**（现在是 26.x）。
3. 装完后，**关掉旧终端，新开一个** PowerShell（或 Mac 终端），分别输入：

```text
node -v
npm -v
```

应看到 `v24.x.x` 和一行 npm 版本。`npm` 是 Node 的包管理器。

**Windows PowerShell 常见坑**：若出现"无法加载 `npm.ps1`，因为在此系统上禁止运行脚本"——**Node 已经装好了**（`npm.cmd -v` 能打出版本即可）。任选其一修复：

```text
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

输入 `Y`，关掉终端再开，再试 `npm -v`。不必开管理员。或者不改策略，后面一律用 `npm.cmd`（例如 `npm.cmd install -g opencode-ai`）。

已有 Node 18 / 20 且 `npm -v` 能跑的：先试 3.2 步；装 `opencode-ai` 失败再改装 LTS 24。

### 3.2 安装 opencode

Node 验收通过后，在同一终端执行：

```text
npm install -g opencode-ai
```

若 PowerShell 仍禁止运行脚本，改用：

```text
npm.cmd install -g opencode-ai
```

验证：

```text
opencode --version
opencode --help
```

能打印版本号，且 help 里能看到用法，本步才算过。把 `--version` 那行截图留给环境记录。

### 3.3 第一次打开 opencode

**必须在项目根目录打开**（有 `AGENTS.md` 的那一层），不要在别的文件夹。本周先建一个练习用的项目文件夹：

```text
mkdir ai4s-my-project
cd ai4s-my-project
```

在这个文件夹里输入：

```text
opencode
```

会打开终端界面（TUI）。第一次打开需要选模型/登录：

- **默认免费模型可以跟课**
- 有付费模型或 token plan 的，可自行接入

### 3.4 装好后练几条命令

界面打开后，输入框里先打 `/`，再试下面几条：

| 命令 | 做什么 |
|---|---|
| `/connect` | 接入模型服务商（登录或填 API key / token plan）。默认免费模型可以先不连 |
| `/model` | 查看并切换模型（默认免费模型可以跟课） |
| `/session` | 查看、切换对话；一次课里换话题可以用它，不必退出 |
| `/compact` | 把当前对话压短，腾出上下文。聊久了变慢或提示太长时用 |

### 3.5 opencode 的工作模式：对话→改文件→运行

opencode 不只是聊天，它能**直接改文件、运行脚本**。这是科研编程的关键工作模式，与网页版 Chat 的核心区别。

试一下：在 opencode 输入框里直接打下面这段提示词（不是斜杠命令）：

```text
我是社科博士生，刚装好 Python 和 wbgapi。请在当前目录写一个脚本 wb_explore.py，用 wbgapi 拉取世界银行数据。

要求：
1. 拉取中国（CHN）近 10 年的人均 GDP（NY.GDP.PCAP.CD）和 GDP 增长率（NY.GDP.MKTP.KD.ZG）
2. 输出一个 pandas DataFrame，年份作为行，两个指标作为列
3. 打印表格，并简单标注最高增长率的年份
4. 用 wbgapi 库，不要用 requests 自己调 API
5. Windows 终端要能跑：python wb_explore.py
```

opencode 会生成文件、可以让你确认后直接写入磁盘。**点运行**，终端无报错，本步才算过。

拉到数据后，可以继续让 opencode 改脚本——比如换成你自己感兴趣的国家或指标。世界银行有 1400+ 指标，覆盖经济、教育、健康、性别、贫困、环境、科技等 19 个主题，浏览全部指标：[https://data.worldbank.org/indicator](https://data.worldbank.org/indicator)。

### 3.6 AGENTS.md：让 opencode 懂你的项目

在项目根目录建一个 `AGENTS.md`，写清楚：

- 项目目标（一句话）
- 技术栈（Python 3.13、pandas、openai 等）
- 目录结构约定
- 代码风格偏好

opencode 打开时会自动读取这个文件，作为后续所有对话的上下文。这是 opencode 区别于普通 Chat 的关键——它"记得"你的项目。详细规则见 [opencode 文档：AGENTS.md 与 `/init`](https://opencode.ai/docs/zh-cn/rules/#%E5%88%9D%E5%A7%8B%E5%8C%96)。

本周先写一个最简版 `AGENTS.md`（3-5 行即可），后续随项目演进逐步完善。

---

## 安装顺序速查

| 步骤 | 验收命令 | 截图留档 |
|---|---|---|
| 1. Python 3.13 | `python --version` → 3.13.x | ✅ |
| 2. Cursor + 选解释器 | `Ctrl+Shift+P → Python: Select Interpreter` 选 Python313 | ✅ |
| 3. 装包 wbgapi + pandas | `pip install wbgapi pandas` 无报错 | — |
| 4. Node.js LTS | `node -v` → v24.x | — |
| 5. opencode | `opencode --version` | ✅ |
| 6. 第一个脚本跑通 | `python wb_explore.py` 打印世界银行数据 | ✅ |

---

## 卡住了

- **安装包下不动**：换校园网 / 手机热点；或用课程群里教师提供的离线安装包。
- **`python` 不是 3.13**：把安装目录加到 PATH，或重装并勾选 Add to PATH；已装 Anaconda 的执行 `conda config --set auto_activate_base false` 后重开终端。
- **Cursor 运行按钮灰 / 提示 No interpreter**：`Ctrl+Shift+P → Python: Select Interpreter` 选 `Python313`。
- **PowerShell 禁止运行 npm**：用 `npm.cmd` 代替 `npm`，或执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 后重开终端。
- **opencode 装不上**：先确认 `node -v` 能跑；仍失败带报错截图进课程群，周末补齐。
- **模型连不上**：先用默认免费模型；有 API key 的按 `/connect` 指引接入。
- **电脑装不上环境**：借同学机器完成课堂演示，报错截图进课程群；本周交付不因安装失败清零，但须本周内补齐。

---

## 参考资源

- [opencode 官网](https://opencode.ai/) / [opencode 文档](https://opencode.ai/docs/) / [AGENTS.md 规则](https://opencode.ai/docs/zh-cn/rules/)
- [Cursor 官网](https://cursor.com/cn) / [Cursor 文档](https://docs.cursor.com/)
- [Python 官网](https://www.python.org/downloads/)
- [Node.js 官网](https://nodejs.org/)
- [wbgapi PyPI](https://pypi.org/project/wbgapi/) / [wbgapi GitHub](https://github.com/tgherzog/wbgapi)
- [世界银行指标浏览](https://data.worldbank.org/indicator)（19 个主题、1400+ 指标，先浏览再选自己研究方向相关的）
- 本科生课程同名材料（含更多排障细节，可参考）：`data-analysis/weeks/week01/python-setup.md`、`data-analysis/weeks/week02/opencode-setup.md`
