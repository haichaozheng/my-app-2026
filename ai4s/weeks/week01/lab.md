# Week 01 课堂实验

## 实验目标

验证 AI 工作环境可用，用 wbgapi 拉取世界银行数据完成第一个 Prompt 驱动的科研脚本，写最简版 `AGENTS.md`。

## 实验步骤

### 第1步：Python 3.13 + Cursor（按 `setup.md` 第一、二部分）

1. 终端跑 `python --version`，须为 3.13.x
2. 安装 Cursor 并登录
3. `Ctrl+Shift+P → Python: Select Interpreter`，选路径里有 `Python313` 的
4. 装包：`python -m pip install wbgapi pandas`

### 第2步：opencode（按 `setup.md` 第三部分）

5. 安装 Node.js LTS（24.x）：`node -v` 验收
6. `npm install -g opencode-ai`（PowerShell 禁止脚本则用 `npm.cmd`）
7. `opencode --version` 验收
8. 建项目文件夹，在里面输入 `opencode` 启动 TUI
9. 选模型（默认免费可跟课）
10. 练四条命令：`/connect` `/model` `/session` `/compact`

### 第3步：第一个脚本

11. 在 opencode 输入框里打提示词，让它生成 `wb_explore.py`：

```text
我是社科博士生，刚装好 Python 和 wbgapi。请在当前目录写一个脚本 wb_explore.py，用 wbgapi 拉取世界银行数据。

要求：
1. 拉取中国（CHN）近 10 年的人均 GDP（NY.GDP.PCAP.CD）和 GDP 增长率（NY.GDP.MKTP.KD.ZG）
2. 输出一个 pandas DataFrame，年份作为行，两个指标作为列
3. 打印表格，并简单标注最高增长率的年份
4. 用 wbgapi 库，不要用 requests 自己调 API
5. Windows 终端要能跑：python wb_explore.py
```

12. 确认 opencode 写入文件后，**点运行**，终端无报错

### 第4步：换成自己的指标

13. 浏览 [世界银行指标](https://data.worldbank.org/indicator)，找出与自己研究方向相关的 3-5 个指标，记下指标代码（如 `SE.XPD.TOTL.GD.ZS` 教育支出占 GDP 比重、`SI.POV.GINI` 基尼系数、`SP.DYN.LE00.IN` 预期寿命）
14. 让 opencode 改 `wb_explore.py`，换成自己选的指标和国家，再跑一遍

### 第5步：AGENTS.md

15. 在项目根目录建 `AGENTS.md`，写最简版（3-5 行）：
    - 项目目标（一句话）
    - 技术栈（Python 3.13、wbgapi、pandas 等）
    - 目录结构约定
16. 退出 opencode 再重新打开，确认它读到了 `AGENTS.md`

### 第6步：互查

17. 同学互助解答：每人机器跑通 `wb_explore.py`
18. 卡住先问同学（对方口述步骤、盯着自己键入）；两分钟仍卡再举手

## 实验交付（当堂自查留存，本周不提交）

- `wb_explore.py`（代码 + 运行截图）
- `AGENTS.md`（最简版）
- 选定指标列表（3-5 个，含指标代码与含义）
- 环境验收截图（见 `setup.md` 末尾"安装顺序速查"六步）

## 卡住了

- 安装包下不动：换校园网 / 手机热点
- `python` 不是 3.13：`conda config --set auto_activate_base false` 后重开终端，或重装勾选 Add to PATH
- Cursor 运行按钮灰：`Ctrl+Shift+P → Python: Select Interpreter` 选 `Python313`
- PowerShell 禁止 npm：用 `npm.cmd` 或 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- opencode 装不上：确认 `node -v` 能跑；仍失败带报错截图进课程群
- wbgapi 调不通：确认 `pip install wbgapi` 成功；网络问题换热点重试
- 卡住 → 问 AI（附报错）→ 同学互助解答 → 举手教师
