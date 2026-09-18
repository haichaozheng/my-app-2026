# 项目概述

本项目服务于以下两门课程：

## 1. 数据分析与可视化

- **面向对象**：财经院校本科生
- **目标**：提高学生做金融数据分析应用与产品的能力，培养学生的创新与创业思维
- **目录**：`data-analysis/`

## 2. 人工智能大模型应用

- **面向对象**：社科类博士生
- **目标**：围绕学生个人科研项目构建AI4S工具栈，并应用该工具栈开展科研
- **目录**：`ai4s/`

# 共同培养目标

两门课程共享一个核心目标：**培养学生提出问题并应用技术（特别是人工智能）解决问题的能力**，使其有潜力产出高水平成果——包括但不限于公开产品和学术论文。

# 教学方法与设计

两门课程均采用 **Project Based Learning（PBL）** 教学方法，强调学生在真实、有意义的项目中主动学习，通过解决实际问题或回答复杂问题来掌握知识与技能。参考资料：https://www.pblworks.org/what-is-pbl

- 课程1：以公开产品为主要成果，鼓励兼产学术论文与参赛成果
- 课程2：以学术论文为主要成果

# 开发规范

- 代码应考虑学生受众的背景：无论是本科生还是博士生，都具有一定的编程能力和大模型应用能力
- 示例和案例优先使用金融/社科领域的数据与场景
- 教学材料应注重实用性，兼顾理论与实践
- 课程1侧重应用导向和产品思维，课程2侧重科研方法论与AI工具链
- PBL知识框架有机支撑：知识按项目阶段组织而非学科章节，通过里程碑制造知识缺口在需求时刻引入（Challenge→Gap→Knowledge→Apply），反思重构个人知识框架，交付物锚定核心知识概念

# 本地 Python 环境

本仓库以教学文稿为主，案例脚本（如 `data-analysis/weeks/week01/cases/`）需要 Python。约定如下，避免助手或本机终端误用 Anaconda。

- 解释器：用官网 **Python 3.13**（`py -3.13`）。不要用 Anaconda `base`（本机直接输入 `python` 常落到 3.9）。
- 虚拟环境目录名统一 **`.venv`**（已在 `.gitignore`）。创建：`py -3.13 -m venv .venv`。不要默认终端会自动激活。
- **Cursor**：`Ctrl+Shift+P` → **Python: Select Interpreter** → 选项目 `.venv`。这主要管点「运行」用哪个 Python，选一次会记住；日常不必每次 `activate`。
- **终端**里要自己敲 `python` / `pip` 时，再到仓库根目录执行 `.\.venv\Scripts\activate`（Mac：`source .venv/bin/activate`）。
- 依赖：根目录 `requirements.txt`。没有该文件时，在已激活的 `.venv` 里 `python -m pip freeze > requirements.txt`。
- 学生向逐步说明：`data-analysis/weeks/week01/python-setup.md`、`data-analysis/weeks/week03/venv-setup.md`。不要把 conda 写成全班默认路径。
