# W1 环境安装：Python + Cursor（不要装 Anaconda）

> 给谁：本周第一次上课、尤其没用过 Python 的同学。  
> 目标：电脑上有一个能跑脚本的 Python，IDE 能找到它。个人项目的虚拟环境放到 **W2 建仓库时**再配，本周不要装 Anaconda。

**IDE：鼓励用 Cursor。** 课堂主演示 [Cursor](https://cursor.com/cn)。登录或网络不顺时可用国内 [Trae](https://www.trae.ai)，课程同样认可，评分不扣。装一个即可，不要两个都装当作业。

Cursor（以及备选 Trae）都是编辑器，**不会自带 Python**。只装 IDE、不装 Python，AI 可以写出代码，但一点「运行」就会报找不到解释器。

---

## 为什么不用 Anaconda


|       | 官网 Python 3.13                                        | Anaconda                     |
| ----- | ----------------------------------------------------- | ---------------------------- |
| 体积    | 约 30 MB                                               | 数 GB                         |
| 课堂    | 10 分钟能装完                                              | 下载、选镜像、PATH 经常卡死             |
| 和本课后期 | `venv` + `requirements.txt`，部署到云/Streamlit Cloud 是同一套 | conda 环境与云端不一致，IDE 也容易选错解释器 |


已经装过 Anaconda 的：**不要卸载**。本课请在 IDE 里选官网 3.13，不要用 `base`。个人项目虚拟环境放到 **W2 建仓库时**再配（见 `weeks/week02/venv-setup.md`），不要在 `base` 里 `pip install` 一堆包。电脑上若同时有 Anaconda，见下面「选解释器」一节。

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

## 第二步：安装 Cursor（推荐），并选中刚才的 Python

- **推荐**：[Cursor](https://cursor.com/cn)
- **备选**（登录或网络不顺时）：[Trae](https://www.trae.ai)

1. 安装并登录 **Cursor**（走备选则装 Trae）。
2. 打开一个空文件夹（或教师发的财政数据文件夹）。
3. 按 `Ctrl+Shift+P`，输入并选择 **Python: Select Interpreter**（选择解释器）。选中第一步那个 3.13，路径里应有 `Python313`（例如 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python313\python.exe`），**不要**选 `anaconda3`，也**不要**选 WindowsApps 里的商店别名。只走命令面板这一条。
4. 关掉旧终端，新开一个，再跑 `python --version`，应看到 `3.13.x`。

### 选了解释器，终端仍是 Anaconda / 3.9 怎么办

电脑上若装过 Anaconda，它常会在终端里自动激活 `base`，把 `python` 抢回 3.9，这时「选择解释器」看起来选了 3.13，终端里一跑仍是旧版本。

- **Cursor**：机器上有 Anaconda 的，**可以第一步就关掉自动激活**（见下面命令），再选解释器，少走弯路。
- **Trae**：先按上面第 3 步选 3.13。若新开终端后 `python --version` 仍不是 3.13，再在终端执行下面命令。

```text
conda config --set auto_activate_base false
```

执行后：**关掉全部终端，再开一个新终端**（必要时关掉 IDE 重开）。Anaconda 不用卸载，只是不再一开终端就进 `base`。验收：`python --version` 为 3.13，或用 `py -3.13 --version` 确认 3.13 仍在。

---

## 第三步：本周先能跑 pandas（先装在这个 Python 上）

本周还没有个人项目仓库，先在当前 Python 里装上课要用的两个包（体积小）：

```text
python -m pip install pandas openpyxl
```

pandas **不能单独读 Excel**：`pd.read_excel()` 要另装引擎。本课财政数据是 `.xlsx`，引擎用 **openpyxl**。旧格式 `.xls` 才需要 `xlrd`，本周不用装。装完让 Cursor（或你装的 Trae）生成脚本：读取数据集、打印行数和列名，**必须点运行且终端无报错**。

个人项目的 `.venv` 不在本周做，步骤见 `weeks/week02/venv-setup.md`。

---

## 卡住了

- 安装包下不动：换校园网 / 手机热点；或用课程群里教师提供的离线安装包。
- `python` 不是 3.13：把安装目录（一般是 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python313\`）加到 PATH，或重装并勾选 Add to PATH。
- 运行按钮灰 / 提示 No interpreter：回到第二步，用 `Ctrl+Shift+P` → **Python: Select Interpreter** 选 `Python313`。
- 已选 3.13，终端仍显示 Anaconda / 3.9：执行 `conda config --set auto_activate_base false`，关掉终端再开（Cursor 可一开始就做这一步；Trae 选解释器无效后再做）。
- 装不上、电脑带不来：借互助组同学机器完成课堂演示，报错截图进课程群；本周交付不因安装失败清零。

