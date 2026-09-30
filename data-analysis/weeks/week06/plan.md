# Week 06 教学计划

## 主题
NumPy/Pandas 进阶与 Matplotlib 静态可视化（工具基础周）

> **前置**：须已完成 W5 EDA 报告。本周把支撑 EDA 的底层工具补扎实——NumPy 数组、pandas groupby 聚合、matplotlib 静态图——并把 W5 的发现固化到自己的项目数据上。
>
> **定位**：衔接周。上游是 W5 的三视角 EDA，下游是 W7 的产品原型。Streamlit 留到 W7，本周不讲。可视化方案设计（milestones §2.3）讲授安排顺延，本周不占该里程碑。

## 本周学习目标

- 能说清 NumPy 数组和 Python list 的差别（向量化运算、连续内存），并解释为什么 pandas/matplotlib 都建立在数组上
- 能用切片与布尔索引从二维数组中取子集，并算出分组统计量（如 Titanic 男女、舱位生还率差异）
- 能用 groupby（单列、多列）+ unstack 完成"按组汇总"，从数据里回答一个行为规律问题
- 能用 matplotlib / pandas.plot 画出回答明确问题的静态图，并说出"图—问题"的对应关系

## 预计投入
课堂 3×45 分钟。课外 4-6h

## 教学内容
1. NumPy 基础：ndarray vs list、数组属性与布尔索引、矩阵乘法（神经网络全连接层视角）、切片步长（图片变形）
2. pandas 数据预处理与 groupby：类型转换/排序/删列删行、Timestamp/Timedelta 与 apply、单列/多列分组聚合、MultiIndex 与 unstack
3. Matplotlib 静态可视化：pandas.plot 封装、多子图（subplots）

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| 概念 | 薄幻灯（≤6页） | 数组 vs list 内存示意；groupby 的 split-apply-combine 图；静态图与"回答什么问题"的绑定 |
| 现场主演示 | Jupyter Notebook | `numpy_pandas_plt.ipynb` 一份到底：NumPy → pandas 预处理 → groupby/可视化，同一份股吧数据从原始清洗到出图贯穿全程 |
| 学生跟做 | Jupyter | 关键格学生自己敲，每格停问"这格得到了什么"（同 W5 手敲要求） |

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：主演示笔记本 `numpy_pandas_plt.ipynb`（一份到底）在本文件夹已跑通；数据 `titanic.csv`、`300251.csv`、`swufeLogo.png` 就位，`cleaned_300251_comments.csv` 由笔记本第 2 节生成（也可直接用成品）。

**第 1 节 · NumPy：数组为什么快、怎么用（45 分钟）**

1. **list vs ndarray（10 分钟）**：百万元素各自乘 2，`%time` 计时对比；先看 `my_list * 2` 是"复制两份"不是逐元素运算，列表推导才是正确姿势。追问"为什么数组快"（连续内存 + 向量化，不用 Python 循环），顺带区分 CPU time 与 wall time。
2. **Titanic 数组案例（15 分钟）**：`np.loadtxt` 读入（`dtype=str`、`skiprows=1`）；用 Q1–Q4 问 `shape`/`dtype`/`size`/`ndim`；Q5 布尔索引切出男女乘客算生还率——女 0.74 / 男 0.19，一张"问出来的图"就有了。
3. **矩阵乘法一图（10 分钟）**：`np.dot`、`x @ W`、ReLU 激活，手算一个 3 维例子。点一句"神经网络全连接层就是这一步"（d2l 链接见学习资料），训练细节 W13 再讲。
4. **图形变形（10 分钟）**：`plt.imread` 读入 `swufeLogo.png`（三维数组：高×宽×通道）；剪切左上角 `im[:h//2, :w//2]`、右下角 `im[h//2:, w//2:]`；负步长 `im[::-1]` 上下翻转。一句收束："切片与步长就是数组的坐标系。"

**第 2 节 · pandas 预处理：从原始数据到干净数据（45 分钟）**

5. **DataFrame 构建（5 分钟）**：三个 Series 拼 `pd.DataFrame`——列是序列、表是字典。
6. **读原始数据（5 分钟）**：`300251.csv`（股吧原始评论，12.9 万行），`encoding="gbk"`、`names` 指定列名；`head`；`unique` 数独立作者。配 garbage in, garbage out 图。
7. **五步清洗（15 分钟）**：①`to_datetime` 转日期类型；②`sort_values` 与 `inplace=True` 三格连演（不接返回值=白排 → 接返回值 → 原地改，学生自己看出"pandas 多数操作返回新表"）；③`drop("url", axis=1)`；④布尔索引删官发"光线传媒资讯"；⑤`str.len() <= 1000` 删超长评论。全程 129856 → 124525。
8. **日期修正（10 分钟）**：`Timestamp`/`Timedelta` 预备知识；`modify_date` 函数（15 点停盘，之后的评论划到次日）；`apply` 沿列应用，得 `modified_date`。
9. **提取时间特征并保存（10 分钟）**：`dt.hour`（发帖时刻）、`modified_date.dt.dayofweek + 1`（周一=1...周日=7）、`dt.month`；切片选列存成 `cleaned_300251_comments.csv`——第 3 节从这份干净数据出发。

**第 3 节 · groupby 聚合与可视化（45 分钟）**

10. **回读干净数据（5 分钟）**：`index_col`/`parse_dates`/`usecols` 复习。
11. **value_counts 一问一图（7 分钟）**：`hour_counts` 柱状图。哪小时最活跃？10 点（18776 条），前五 10/14/13/11/9——高峰在开盘后与尾盘前，学生自己把评论行为和交易时间挂上钩。
12. **groupby 引入：Titanic 分舱位（10 分钟）**：`titanic.groupby("Pclass")["Survived"].mean().plot(kind="bar")`；`for` 循环看每组是一个子 DataFrame；split-apply-combine 图。
13. **按小时分组（8 分钟）**：`groupby(["hour"])`、`aggregate(np.count_nonzero)` 计数、`grouped_hour.comment.plot(kind="bar")`；对照另一种一行写法 `groupby(["hour"])["hour"].count()`——两种等价，选顺手的。
14. **双列分组与 unstack（10 分钟）**：`groupby(["dayofweek","hour"])`，看 MultiIndex；`unstack()` 转宽表（7 天 × 24 小时）；`.T.plot(kind="bar")` 对比周内各天。
15. **多子图收束（5 分钟）**：`fig, ax = plt.subplots(4, 1, sharex=True)` 循环画每天 24 小时分布（数据有 7 组，改 4→7 看全周）。思考题收问："交易日和周末是不是同一套作息？"（开盘前后凸起 vs 夜间尖峰）。当日 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录；互助记录只写"谁帮了你、对项目有何影响"，没有则写"无"）。收集卡点（多数预计在时间列解析与 MultiIndex）。本周不讲 Streamlit，产品化留到 W7。

**课后自学 · 大模型 API（不在课堂展开）**

- `llm_api.ipynb`（大模型API接入）留作课后自学：大模型辅助企业降本增效的应用场景、DeepSeek API 的获取与调用（API 密钥管理、`openai` SDK 对接 deepseek、封装 `deepseek_chat` 函数），以及"品牌起名"实战——把课程一直强调的"需求 → 提示词 → 输出"闭环迁移到 LLM 场景，为 W7 产品原型中接入大模型能力做铺垫。
- 自学要求：课前准备好自己的 DeepSeek API key，跑通"保存密钥（推荐 `.env` 方式）→ 调用 API → 完成课堂练习（新闻关键词提取 + 一句话摘要）"；LOGO 生成为选学。
- 卡点按"卡住了找谁"流程处理，AI 使用与密钥安全问题（不要把密钥硬编码提交到仓库）随 W7 一并强调。

## 项目活动

**必做**
1. 项目数据聚合与静态图 Notebook：≥1 个 groupby 聚合 + ≥2 张 matplotlib 静态图，每张图配一句"回答什么问题"，图之间不要求叙事（那是可视化方案周的事）

**进阶（可选）**
2. 用 NumPy 布尔索引（不经 pandas）复现 W5 的一个 EDA 结论，并与 pandas 结果对照

**兜底**
- 项目数据未就绪：用 `titanic.csv` 或 `cleaned_300251_comments.csv` 完成同规格任务（问题自拟，不抄课堂原题）

## 交付物（评分锚点）

- 项目数据聚合与静态图 Notebook（含每图的"回答什么"一句话）——计入平时成绩（形成性）；作为后续可视化方案（milestones §2.3）的图表素材储备。
- 技能小练单独提交（见 `lab.md`）。

提交前自检：每张图的标题能让读者看出结论？分组维度选得有理由（为什么按这个分）？聚合数值抽查过 1 个组？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

## 课后任务
1. 完成项目数据聚合与静态图 Notebook
2. 按需补看视频（缺哪补哪，不刷序列）：NumPy 5.1-5.4、Pandas 6.1-6.2、可视化 7.1-7.3
3. 自学 `llm_api.ipynb`：跑通 DeepSeek API 调用并完成其中的课堂练习（关键词提取 + 一句话摘要），为 W7 产品原型接入大模型能力做准备

## 学习资料
- 本周演示笔记本：`numpy_pandas_plt.ipynb`（含数据 `titanic.csv`、`300251.csv`、`swufeLogo.png`、`cleaned_300251_comments.csv`）
- 课后自学笔记本：`llm_api.ipynb`（大模型API接入，DeepSeek 官方文档 <https://api-docs.deepseek.com/zh-cn/>；需自备 API key）
- `knowledge/phase2-2-3-pandas-advanced.md`
- `knowledge/phase2-2-7-visualization-principles.md`（图表类型选择）
- 视频资料（超星学习通，详见 `video-resources.md`）：系列 5 Numpy（5.1-5.4）、系列 6 Pandas（6.1-6.2）、系列 7 数据可视化（7.1-7.3）——本周均为按需补缺
- 动手学深度学习·多层感知机（仅第 1 节矩阵乘法延伸，选看）：<https://zh.d2l.ai/chapter_multilayer-perceptrons/mlp.html>
