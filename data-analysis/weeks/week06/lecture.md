# Week 06 课堂串讲

今天怎么走：第 1 节 NumPy——数组为什么快、怎么切；第 2 节 pandas 预处理——把 12.9 万行原始股吧评论洗成干净数据；第 3 节 groupby 聚合 + matplotlib 静态图——从干净数据里问出"几点、周几最活跃"。Streamlit 本周不讲，产品化留到 W7。

**下课时你应能：** 说清 list 乘 2 与数组乘 2 的差别及原因（连续内存 + 向量化）；用布尔索引从 Titanic 二维数组切出男女乘客并算出生还率差；完成股吧数据五步清洗（129856 → 124525 行）并落盘干净版本；用 groupby（单列、双列 + unstack）回答"股吧评论几点、周几最活跃"，并画柱状图。

卡住了：

```
问 AI（附报错）→ 互助组（盯着你自己键入，不代跑）→ 课程群（附截图）
```

跟做：`weeks/week06/numpy_pandas_plt.ipynb`（一份到底：NumPy → pandas 预处理 → groupby/可视化）。数据 `titanic.csv`、`300251.csv`、`swufeLogo.png` 就在本文件夹；`cleaned_300251_comments.csv` 由第 2 节生成（也可直接用成品）。课前笔记本已跑通。

---

## 第 1 节 · NumPy：数组为什么快、怎么用（45 分钟）

1. **list vs ndarray（10 分钟）**
   百万元素各自乘 2，`%time` 计时对比。先看 `my_list * 2`——是"复制两份"，不是逐元素运算；列表推导 `[x * 2 for x in my_list]` 才是正确姿势。追问"为什么数组快"（连续内存 + 向量化，不用 Python 循环）；顺带区分 CPU time 与 wall time。
2. **Titanic 数组案例（15 分钟）**
   学生自己敲，每格停问"这格得到了什么"。这一段不请 AI 代写（同 W5 手敲要求）。

   | 格 | 得到什么 |
   | --- | --- |
   | `np.loadtxt(..., delimiter=",", skiprows=1, dtype=str)` | 887×8 的字符串数组 |
   | Q1–Q4：`shape` / `dtype` / `size` / `ndim` | 多少元素、几维；`887*8` 对上没有 |
   | Q5：布尔索引 `titanic_data[:,3]=="female"` | 布尔数组 → 切出女/男乘客 |
   | `[:,0].astype(float).mean()` | 女 0.74 / 男 0.19——一张"问出来的图"就有了，这就是 W5"分布对比"的数组版 |
3. **矩阵乘法一图（10 分钟）**
   `a * b`（逐元素）vs `np.dot(a,b)`（点积）；`x @ W` 形状对齐；`np.maximum(0, z)` 即 ReLU；手算一个 3 维例子。点一句：神经网络全连接层就是这一步，训练细节 W13 再讲（d2l 链接见 `plan.md` 学习资料）。
4. **图形变形（10 分钟）**
   `plt.imread` 读入 `swufeLogo.png`——三维数组：高×宽×通道。剪切左上角 `im[:h//2, :w//2]`、右下角 `im[h//2:, w//2:]`；负步长 `im[::-1]` 上下翻转。一句收束："切片与步长就是数组的坐标系。"

---

## 第 2 节 · pandas 预处理：从原始数据到干净数据（45 分钟）

要回答的问题（第 3 节回答）：股吧里的人几点、周几发言最活跃？数据是 `300251.csv`——股吧原始评论 12.9 万行。garbage in, garbage out：先洗再用。

5. **DataFrame 构建（5 分钟）**
   三个 Series 拼 `pd.DataFrame`——列是序列、表是字典。
6. **读原始数据（5 分钟）**
   `pd.read_csv("300251.csv", encoding="gbk", names=["date","author","url","comment"])`；`head`；`unique` 数独立作者。
7. **五步清洗（15 分钟）**
   `sort_values` 三格连演：不接返回值 = 白排 → 接返回值 → `inplace=True` 原地改——学生自己看出"pandas 多数操作返回新表"。

   | 步 | 操作 | 得到什么 |
   | --- | --- | --- |
   | ① | `to_datetime` | 日期列从字符串转日期类型 |
   | ② | `sort_values`（三格连演） | 按日期排序；体会返回新表 vs 原地改 |
   | ③ | `drop("url", axis=1)` | 删用不上的列 |
   | ④ | 布尔索引 `author != "光线传媒资讯"` | 删官方发布，只留用户评论 |
   | ⑤ | `str.len() <= 1000` | 删超长评论；全程 129856 → 124525 行 |
8. **日期修正（10 分钟）**
   `Timestamp` / `Timedelta` 预备知识；`modify_date` 函数（15 点停盘，之后的评论划到次日）；`apply` 沿列应用，得 `modified_date`。
9. **提取时间特征并保存（10 分钟）**
   `dt.hour`（发帖时刻）、`modified_date.dt.dayofweek + 1`（周一=1...周日=7）、`dt.month`；切片选列存成 `cleaned_300251_comments.csv`——第 3 节从这份干净数据出发。

---

## 第 3 节 · groupby 聚合与可视化（45 分钟）

10. **回读干净数据（5 分钟）**
    `index_col` / `parse_dates` / `usecols` 复习（W5 手敲内容回来验收）。
11. **value_counts 一问一图（7 分钟）**
    `hour_counts` 柱状图。哪小时最活跃？10 点（18776 条），前五 10/14/13/11/9——高峰在开盘后与尾盘前。学生自己把评论行为和交易时间挂上钩。
12. **groupby 引入：Titanic 分舱位（10 分钟）**
    `titanic.groupby("Pclass")["Survived"].mean().plot(kind="bar")`；`for` 循环看每组是一个子 DataFrame；split-apply-combine 图。点题：groupby 之前的 `.mean()` 是全局汇总，之后是分组汇总——"换问题"从换分组维度开始。
13. **按小时分组（8 分钟）**
    `groupby(["hour"])` + `aggregate(np.count_nonzero)` 计数 + `grouped_hour.comment.plot(kind="bar")`；对照另一种一行写法 `groupby(["hour"])["hour"].count()`——两种等价，选顺手的。
14. **双列分组与 unstack（10 分钟）**
    `groupby(["dayofweek","hour"])`，看 MultiIndex 长什么样；`unstack()` 转宽表（7 天 × 24 小时）；`.T.plot(kind="bar")` 对比周内各天。
15. **多子图收束（5 分钟）**
    `fig, ax = plt.subplots(4, 1, sharex=True)` 循环画每天 24 小时分布（数据有 7 组，改 4→7 看全周）。思考题收问："交易日和周末是不是同一套作息？"（开盘前后凸起 vs 夜间尖峰）。
    当日 `journal.md` 追加 1 条：今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录。互助记录只写"谁帮了你、对项目有何影响"，没有则写"无"。收集卡点（多数预计在时间列解析与 MultiIndex）。本周不讲 Streamlit，产品化留到 W7。

---

课后：完成项目数据聚合与静态图 Notebook（≥1 个 groupby + ≥2 张静态图，每张图配一句"回答什么问题"，见 `plan.md` 项目活动）；技能小练单独提交（见 `lab.md`）。按需补看视频（缺哪补哪）：NumPy 5.1-5.4、Pandas 6.1-6.2、可视化 7.1-7.3。
