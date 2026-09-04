# W2 个人项目虚拟环境

> 给谁：本周建好个人项目仓库之后。  
> 前提：已按 `weeks/week01/python-setup.md` 装好 **Python 3.13**，Cursor（或备选 Trae）能选中它。  
> 本周不要用 Anaconda / conda 当项目环境。

W1 装在系统里的 Python 只保证「电脑上有解释器」。个人项目的包装进仓库里的 `.venv`，以后部署、同学复现都靠 `requirements.txt`，不要再往系统 Python 里堆包。

## 为什么叫 `.venv`

`python -m venv` 后面必须跟一个目录名，叫什么都可以（`venv`、`env` 也能建出来）。**本课统一用 `.venv`**：前面的点在 Mac / Linux 里默认隐藏；Cursor 会自动去找项目根目录下的这个名字；常见 `.gitignore` 也写了 `.venv/`。课堂和作业不要改成别的名字，否则选解释器、互相看仓库会对不上。不要用 `.env` 当虚拟环境名——那个名字通常留给放密钥的配置文件。

---

## 在哪执行

打开个人项目仓库的**根目录**（有 `AGENTS.md` 的那一层），再开终端。不要在别的文件夹建 `.venv`。

若 `python --version` 仍不是 3.13（常见于装过 Anaconda），改用：

```text
py -3.13 -m venv .venv
```

Mac 一般用 `python3 -m venv .venv`。

---

## 步骤

**1. 建环境**

```text
python -m venv .venv
```

**2. 激活（建环境、在终端里装包时用；不是每次打开项目都要做）**

Windows（PowerShell）：

```text
.\.venv\Scripts\activate
```

含义（Windows 路径）：`.` 是当前文件夹 → `.venv` 是刚建的环境目录 → `Scripts` 里放 Windows 版的启动脚本 → `activate` 用来「启用」这个环境。启用后，本窗口里的 `python` / `pip` 指向 `.venv`，而不是系统或 Anaconda。提示符前出现 `(.venv)` 即成功。

若提示无法运行脚本：先执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，再重试激活。

Mac / Linux：

```text
source .venv/bin/activate
```

激活成功后，提示符前面会出现 `(.venv)`。再跑 `python --version`，应仍是 3.13。

**3. 装本课起步包**

在**已经出现 `(.venv)` 的终端**里装（还没激活就先做第 2 步）：

已有 `requirements.txt` 时：

```text
python -m pip install -r requirements.txt
```

还没有该文件时，先装包，再用下面任一方式生成 `requirements.txt`（在项目根目录、且终端已出现 `(.venv)`）：

```text
python -m pip install pandas openpyxl
python -m pip freeze > requirements.txt
```

`pip freeze` 会把当前环境里已装的包及版本写进文件。PowerShell 与 CMD 都可用 `>`。

也可用几行代码创建一份起步清单（不含版本号，同学装到当时的最新版）：

```python
from pathlib import Path

Path("requirements.txt").write_text("pandas\nopenpyxl\n", encoding="utf-8")
```

W7 起按产品需要追加 streamlit、plotly 等：再 `pip install`，然后重新执行一次 `python -m pip freeze > requirements.txt` 覆盖更新。

**4. 在 Cursor 里选解释器（日常用法，选一次会记住）**

创建 `.venv` 之后，**不要默认它会自动激活。** 以后做项目，在 Cursor 里用：

`Ctrl+Shift+P` → **Python: Select Interpreter** → 选项目里的 `.venv`（路径中应有 `.venv`）

这主要管**点「运行」用哪个 Python**，选一次会记住，换文件、下次打开这个仓库仍然有效。不要再选 Anaconda 的 `base`，也不要选系统里的 `Python313` 当本项目的日常解释器。

这样日常写代码、点运行，就不必每次打开项目都去执行 `.\.venv\Scripts\activate`。终端里若没有 `(.venv)` 是正常的：点运行仍然走你选中的解释器。只有要在终端里自己敲 `python` / `pip` 时，才再执行第 2 步。

**5. 不要提交虚拟环境文件夹**

把 `.venv/` 写进 `.gitignore`。仓库只提交 `requirements.txt`，不提交 `.venv`。

---

## 卡住了

- 终端里没有 `(.venv)`：正常，不要等自动激活。日常点运行靠第 4 步选过的解释器；只有在终端里敲 `python` / `pip` 时才做第 2 步。
- `python -m venv` 报错或建成的不是 3.13：先回到 W1 说明确认 `py -3.13 --version`，再用 `py -3.13 -m venv .venv`。
- 激活后仍是 Anaconda / 3.9：执行 `conda config --set auto_activate_base false`，关掉全部终端再开；Cursor 里重新选 `.venv` 解释器。
- 装包很慢或失败：换校园网 / 手机热点；或用课程群里的离线说明。
- 同学克隆你的仓库后跑不起来：检查是否提交了 `requirements.txt`、是否误提交了 `.venv/`。对方应自己在本地执行本页第 1–4 步。
