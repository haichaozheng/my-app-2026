# W1 环境安装：Python + 自选 IDE（不要装 Anaconda）

> 给谁：本周第一次上课、尤其没用过 Python 的同学。  
> 目标：电脑上有一个能跑脚本的 Python，自选的 IDE 能找到它。个人项目的虚拟环境放到 **W2 建仓库时**再配，本周不要装 Anaconda。

**IDE 自选**：国内 [Trae](https://www.trae.ai) 与国外 [Cursor](https://cursor.com/cn) 课程都认，按偏好和网络选一个即可，不要两个都装当作业。课堂两边都会演示。

Trae / Cursor 都是编辑器，**不会自带 Python**。只装 IDE、不装 Python，AI 可以写出代码，但一点「运行」就会报找不到解释器。

---

## 为什么不用 Anaconda

| | 官网 Python 3.13 | Anaconda |
|---|---|---|
| 体积 | 约 30 MB | 数 GB |
| 课堂 | 10 分钟能装完 | 下载、选镜像、PATH 经常卡死 |
| 和本课后期 | `venv` + `requirements.txt`，部署到云/Streamlit Cloud 是同一套 | conda 环境与云端不一致，Trae 也容易选错解释器 |

已经装过 Anaconda 的：**不要卸载**。在自选 IDE 里选中它的 Python 即可；W2 仍然用 `python -m venv .venv` 给个人项目单独建环境，不要在 `base` 里 `pip install` 一堆包。

本课统一口径：**官网 Python + 项目内 `.venv`**，不引入 conda 作为默认路径。

---

## 第一步：安装 Python 3.13（本周必做）

全班统一 **3.13.x（该系列最新补丁）**。官网首页大按钮现在是 3.14，**不要点它**。3.14 已是正式版，但本课后面的 Streamlit / 部分金融数据包 / 云端镜像仍以 3.13 最省事。不要装 3.15（预发布），不要低于 3.11。

已装 3.12 且能跑 pandas 的：**不必重装**。已装 3.14 且 `pip install pandas streamlit` 一次成功的：可以继续用，出问题再改 3.13。

1. 打开 [Python 3.13 发布页](https://www.python.org/downloads/)，在页面里找 **3.13** 的 Windows installer（64-bit），不要选 embeddable、不要选 free-threaded（名字里带 `t` 的）。
2. 运行安装程序，**必须勾选** `Add python.exe to PATH`，再点 Install Now。
3. 关掉安装窗口后，打开 PowerShell 或「终端」，分别输入（各回车一次）：

```text
python --version
pip --version
```

应看到 `Python 3.13.x` 和一行 pip 版本。

**Windows 常见坑**：输入 `python` 却弹出微软应用商店。到「设置 → 应用 → 高级应用设置 → 应用执行别名」里，关掉 `python.exe` / `python3.exe` 两个开关，再重开终端试一次。

**验收一句**：`python --version` 能打印 3.13，本步才算过。把这行的截图留给「环境配置记录」。

Mac：同样装 3.13，用 `python3 --version` / `pip3 --version` 验收。

---

## 第二步：安装 Trae 或 Cursor，并选中刚才的 Python

二选一（都认）：

- 国内：[https://www.trae.ai](https://www.trae.ai)
- 国外：[https://cursor.com/cn](https://cursor.com/cn)

1. 安装并登录你选的那一个。
2. 打开一个空文件夹（或教师发的财政数据小仓库）。
3. 命令面板选解释器（或点右下角 Python 版本），选中第一步那个 3.13，路径里应有 `Python313`，**不要**选 WindowsApps 里的商店别名。
4. 在该 IDE 的终端里再跑一次 `python --version`，应与系统终端一致。

---

## 第三步：本周先能跑 pandas（先装在这个 Python 上）

本周还没有个人项目仓库，先在当前 Python 里装上课要用的两个包（体积小）：

```text
python -m pip install pandas openpyxl
```

`openpyxl` 用来读 `.xlsx` / `.xls` 财政数据。装完让自选 IDE 生成脚本：读取数据集、打印行数和列名，**必须点运行且终端无报错**。

有基础的同学可以本周就试 `python -m venv .venv`，但**全班统一要求从 W2 建仓周开始**，避免第一周概念过载。

---

## W2 才做：个人项目虚拟环境

建好个人 repo 之后，在项目根目录（有 `AGENTS.md` 的那一层）执行：

```text
python -m venv .venv
```

Windows 激活：

```text
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

还没有 `requirements.txt` 时，先 `python -m pip install pandas`，W7 起按产品需要追加（streamlit、plotly 等），并写进 `requirements.txt`。

把 IDE 解释器改为项目里的 `.venv`。把 `.venv/` 写进 `.gitignore`，不要提交虚拟环境文件夹。

此后每个项目只用自己的 `.venv`，不要往「系统 Python」里继续堆包——部署和同学复现都靠 `requirements.txt`。

---

## 卡住了

- 安装包下不动：换校园网 / 手机热点；或用课程群里教师提供的离线安装包。
- `python` 不是 3.13：把安装目录（一般是 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python313\`）加到 PATH，或重装并勾选 Add to PATH。
- 运行按钮灰 / 提示 No interpreter：回到第二步选解释器。
- 装不上、电脑带不来：借互助组同学机器完成课堂演示，报错截图进课程群；本周交付不因安装失败清零。
