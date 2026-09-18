# W2 安装 opencode

> 给谁：本周第 1 节跟做安装。  
> 官网：[https://opencode.ai/](https://opencode.ai/)  
> 装不上：先用 Trae 跟后面的课堂演示，报错截图进课程群，周末按本页补齐。采集西财新闻必须用 opencode。

opencode 是命令行里的 AI 编程助手。本周起用它接管个人项目（读取 `AGENTS.md`）。它基于 Node.js，要先有 Node，再全局安装 `opencode-ai`（名字必须带 `-ai`，不要装成 `opencode`）。

课堂默认：**Windows 直接装 Node.js（不要先装 WSL）**，在 PowerShell 里验收。Mac 同样装官网 LTS，再用下面的 `npm` 命令。

---

## 1.1 安装 Node.js

### 方法一：直接安装（课堂推荐）

1. 打开 [https://nodejs.org](https://nodejs.org)
2. 下载 **LTS**（现在是 **24.x**，例如 24.21.0）。**不要点 Current**（现在是 26.x）。
3. 装完后，**关掉旧终端，新开一个** PowerShell（或 Mac 终端），分别输入：

```text
node -v
npm -v
```

应看到 `v24.x.x` 和一行 npm 版本。`npm` 是 Node 的包管理器。

Windows PowerShell 若出现「无法加载 `npm.ps1`，因为在此系统上禁止运行脚本」：**Node 已经装好了**（`npm.cmd -v` 能打出版本即可）。任选其一：

```text
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

输入 `Y`，关掉终端再开，再试 `npm -v`。不必开管理员。或者不改策略，后面一律用 `npm.cmd`（例如 `npm.cmd install -g opencode-ai`）。

已有 Node 18 / 20 且 `npm -v` 能跑的：先试第 1.3 步；装 `opencode-ai` 失败再改装 LTS 24。

### 方法二：用 nvm（需要并排多个 Node 版本时）

不需要多版本的同学跳过，用方法一即可。

**Mac / Linux：**

```text
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

**关掉终端再开**，然后：

```text
nvm install --lts
nvm use --lts
node -v
```

应看到 `v24.x.x`。不要装已停止维护的 Node 18。

**Windows：** 装 [nvm-windows](https://github.com/coreybutler/nvm-windows/releases)（下载 `nvm-setup.exe`）。装完在 **新的** PowerShell 里：

```text
nvm install 24
nvm use 24
node -v
```

---

## 1.2 Windows 特别说明

**本课课堂走方案二**（无 WSL）。WSL 要重启，10 分钟安装环节做不完。

### 方案一：WSL（可选，已有 Linux 子系统或课后想用 Linux 终端时）

在 **PowerShell（管理员）** 中：

```text
wsl --install
wsl --install -d Ubuntu-22.04
```

重启后设置 WSL 用户名和密码。之后在 **WSL 终端**里按 Linux 方式做 1.1 和 1.3，不要混用 Windows 的 PowerShell。

### 方案二：无 WSL，直接在 Windows 上安装（课堂默认）

1. 按 1.1 方法一安装 Node.js
2. 后续命令都在 **PowerShell** 里执行（不要用旧版 CMD 凑合）
3. 装好后用 `opencode` 启动终端界面（TUI）

---

## 1.3 安装 opencode

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

**第一次打开界面**：等到个人仓库建好，在仓库根目录（有 `AGENTS.md` 的那一层）输入：

```text
opencode
```

不要在别的文件夹里开。登录或模型连不上时，先用 Trae 跟课堂演示，装好后再补这一步。

---

## 1.4 装好后练几条命令

界面打开后，输入框里先打 `/`，再试下面几条（完整名是 `/models`、`/sessions`，打 `/model`、`/session` 一般也能对上）：

| 命令 | 做什么 |
|---|---|
| `/connect` | 接入模型服务商（登录或填 API key / token plan）。默认免费模型可以先不连 |
| `/model` | 查看并切换模型（默认免费模型可以跟课） |
| `/session` | 查看、切换对话；一次课里换话题可以用它，不必退出 |
| `/compact` | 把当前对话压短，腾出上下文。聊久了变慢或提示太长时用 |

然后直接输入下面这段提示词（不是斜杠命令），让它写小游戏。不要只画几根随机柱子。

```text
我是财经本科生，刚装好 Python。请在当前目录写一个能在终端里玩的小游戏，保存为 hello_viz.py。

游戏名：数据侦探 · 一眼看穿。不要第三方库，中文，有趣，不要说教腔。

四轮找茬，每轮一张 ASCII 图 + 一道选择题，答完立刻揭晓，并用一句话点明启发：
1. 坐标轴不从 0 起笔：奶茶/吃饭/交通开销其实只差几块钱，柱子却看起来差很多。
2. 均值陷阱：五人日薪 180、200、190、210、2000，问跟朋友说「大家大概赚多少」该看平均数还是中位数。
3. 时间窗口：只截指数周六到周日在涨，完整一周其实在跌。问能不能据此说「这周行情在涨」。
4. 相关不是因果：刷短视频越久分数越低，问禁短视频分数会不会涨。

最后统计看穿了几张图，收束一句：数据分析与可视化不是把数画漂亮，是先问这张图在隐瞒什么。
Windows 终端要能跑：python hello_viz.py
```

点运行玩一遍即可。这只是上手，本周正式练习仍按 `opencode-class-norm-case.md`。老师演示也可用仓库里的 `weeks/week02/hello_viz.py`。
