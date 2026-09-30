# Week 04 课堂串讲

今天怎么走：用自己的 `.venv` 打开 Jupyter，跟做 API 取财经数据 → 当堂开做「1 家公司 + 1 个问题」的 tushare 作业。用户需求分析这节没讲，改到第 5 周第 1 节。

**下课时你应能：** 笔记本内核路径里有 `.venv`；笔记本里已有公司名、问题和至少一张表。

卡住了：

```
问 AI（附报错）→ 互助组（盯着你自己键入，不代跑）→ 课程群（附截图）
```

跟做：`weeks/week04/structured_data.ipynb`。作业截止：**2026年10月16日晚上8点**。

---

## 第 1 节 · 应用 API 获取财经数据

要用 Jupyter，就选 W3 建好的项目 `.venv`。没把 `ipykernel` 装进这个环境，笔记本打得开，单元格跑不了，或跑到系统 Python / Anaconda `base` 上。

1. **激活** `.venv`
  项目根目录打开终端。Windows：`.\.venv\Scripts\activate`。Mac：`source .venv/bin/activate`。提示符前出现 `(.venv)` 再往下做。
2. **安装** `ipykernel`
  `python -m pip install ipykernel`，再 `python -m pip freeze > requirements.txt`。
3. **选解释器，跑一格**
  `Ctrl+Shift+P` → **Python: Select Interpreter** → 路径里有 `.venv` 的那一个。打开 `weeks/week04/structured_data.ipynb`，运行：

```python
import sys
print(sys.executable)
```

  输出路径里应有 `.venv`。对上即停。

内核确认后，按笔记本往下做：


| 块                           | 干什么          |
| --------------------------- | ------------ |
| How to build a career in AI | 职业成长，不展开成选题课 |
| 初步认识并应用 pandas              | 表怎么读、怎么看     |
| 使用 tushare 获取股票行情数据         | API 拿到一张行情表  |
| 应用 concurrent.futures 做并发操作 | 多只股票不要一张一张等  |


---



## 第 2 节 · 用户需求分析

课堂上没讲。整节改到第 5 周第 1 节，串讲见 `weeks/week05/lecture.md`。

---



## 第 3 节 · 动手感受 API 获取数据

**提交截止：2026年10月16日晚上8点。** 布置和收束各说一遍。

1. **布置作业（8 分钟）**
  自由选 1 家上市公司。针对这家公司提 1 个问题。用 tushare 取相关数据（行情、财务、宏观、新闻都可以）。用采到的数据回答这个问题。
  笔记本四部分：

  | 部分  | 写什么             |
  | --- | --------------- |
  | 公司  | 名称与基本简介         |
  | 问题  | 题目及其内涵          |
  | 采集  | 用 tushare 拿到的数据 |
  | 解答  | 用这些数据回答那个问题     |

2. **当堂开工（30 分钟）**
  在已选中 `.venv` 的笔记本里写下公司名和那一个问题，并成功拉下至少一张表。tushare 密钥已由教师写进课堂 Jupyter，本节不用 `.env`，也不要再装 `python-dotenv`。拉不通的记下报错，课后补。
3. **收束（7 分钟）**
  课上交不出完整分析。四部分课后补全，**2026年10月16日晚上8点**前提交。当日 `journal.md` 追加 1 条五格。互助：谁帮了你、对项目有何影响；没有则写「无」。

---



## 课后

1. 交齐作业笔记本（四部分）。**截止：2026年10月16日晚上8点**
2. 取数和分析里的判断与卡点写入 `journal.md`（本周不单独交日志）

