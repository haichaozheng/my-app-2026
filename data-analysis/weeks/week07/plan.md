# Week 07 教学计划

## 主题

产品原型搭建 + AI辅助编程加速原型

> **前置**：须已完成 W6 可视化方案设计，本周将可视化迁移进产品框架（W6 未完成的交互式实现随本周合并完成）。

## 本周学习目标

- 能说明产品框架选择理由（为什么 Streamlit/Gradio/自选框架，而非"别人都在用"）
- 能把 W6 可视化方案迁移进可运行的产品原型，形成"数据加载→分析→可视化"基本闭环
- 能让 AI 辅助编程完成大部分原型代码，并指出哪些输出需要人工修改、为什么

## 预计投入

课堂 3×45 分钟。课外 10-12h（第一个完整产品周，投入峰值之一）

## 教学内容

1. Streamlit 快速原型（必做）
2. Gradio 快速原型（可选，适合AI交互类产品）
3. 用AI辅助编程加速原型搭建
4. Skill作为可选产品形式（把W4/W5已验证的分析流程封装为Skill，是产品展示形式之一，非必做）

**进阶自学**（有Web开发基础、追求更灵活定制的同学）：React/Vue前端 + FastAPI后端。参考资源：

- React：[https://react.dev/learn](https://react.dev/learn)
- Vue：[https://vuejs.org/guide/introduction.html](https://vuejs.org/guide/introduction.html)
- FastAPI：[https://fastapi.tiangolo.com/zh/tutorial/](https://fastapi.tiangolo.com/zh/tutorial/)



## 课堂演示工具


| 环节    | 工具                                       | 用法                                                                                                                    |
| ----- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 概念    | 薄幻灯（≤6页）                                 | 为何选 Streamlit；数据加载→分析→可视化闭环                                                                                           |
| 现场主演示 | Jupyter Notebook + Cursor/OpenCode + 浏览器 | `streamlit.ipynb` 案例「股价预测 APP」一条链到底：Streamlit 基础 → tushare 取数 → 大模型预测 → 第 3 节布置实验任务并演示；AI 辅助编程（Cursor/OpenCode），浏览器验收 |
| 学生跟做  | Cursor/OpenCode + Streamlit              | 底线：能打开并展示一个核心分析                                                                                                       |
| 不做    | 只在 Jupyter 里交「产品」                        | Notebook 是实验室，产品是店面                                                                                                   |




## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：主演示笔记本 `streamlit.ipynb` 已跑通——tushare token、`DEEPSEEK_API_KEY` 已配入 `.env`（不入库、不发群里）；`mvp-template/` 可一键跑起（兜底用）。

**第1节 · Streamlit：从 Notebook 到店面（45 分钟）**

1. **分享课后作业（上周 journal）+ 实验室 vs 店面（8 分钟）**：随机邀请同学分享上周 journal（3 问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点）。Notebook 交作业 ≠ 产品；本周底线 = 浏览器能打开并展示一个核心分析。
2. **Streamlit 入门（12 分钟）**：为何 Streamlit（本课程及以后其他课程的项目展示都用得上，docs：docs.streamlit.io/get-started）；`pip install streamlit`；`streamlit hello` 现场看案例展示；`streamlit run your_script.py` 是唯一的运行入口。
3. **Basic concepts 跟做（25 分钟）**：按实验文档 `week07-streamlit-app.md`「第 1 节实验」走——先给心智模型（官网三句定位 + "Streamlit 应用 = 每次用户交互都从头到尾重跑一遍的 Python 脚本"+ notebook 对照表），再一个 `app.py` 六步生长：跑起来 → `st.dataframe` → `st.line_chart` → `st.slider`（插入"时间戳 rerun 证据"，把机制做可见）→ `st.selectbox` 下拉选股票（与第 3 节 APP 侧栏同构的骨架）→ 选项联动合成迷你查看器；`st.table`、`st.session_state`、`st.progress`、侧栏为加餐。每步"猜→做→观察→检查"（检查题见文档）。收束一句："Streamlit = 把 notebook 的格子变成网页的元件。"

**第2节 · 案例：取数与大模型对话——股价预测的原材料（45 分钟）**

1. **tushare 取每日指标（15 分钟）**：`ts.set_token` + `pro.daily_basic` 单日取 000001.SZ（换手率/量比/PE/PB，doc_id=32）；再倒推 5 天循环取多天数据——`Timestamp`/`Timedelta` 正好接 W6，"循环取数+容错跳过"是接 API 的通用套路。
2. **chat with AI（12 分钟）**：课堂默认 **DeepSeek**（`DEEPSEEK_API_KEY` 放 `.env`，`load_dotenv` 读取，密钥永不硬编码）；兼容 OpenAI 接口，封装 `llm_chat`；先 `llm_chat("hello")` 跑通再谈业务。点一句换厂商的方法：只改 `base_url`、模型名和 API Key 环境变量（豆包等其他兼容 OpenAI 接口的服务同理），学生用哪家的 Key 都能跟。
3. **构造预测 prompt 并预测（18 分钟）**：问题（第五个交易日涨还是跌）+ 判断标准 + materials（`df.to_dict(orient='records')`）；7 步指令（重述问题 → 正反理由及强度 → 聚合 → 初始概率 → 反思 → 最终 JSON 概率，中文回答）。课堂跑一次，让学生看到大模型如何"像超级预测员一样"给出 up/down 概率。点一句：把 W6 的 groupby 结果当 materials 喂给大模型，就是同一个套路。

**第3节 · 从回答到应用：实验任务布置——组装 APP + AI 辅助编程（45 分钟）**

1. **extract_json 提取概率（8 分钟）**：大模型输出是长文本，用正则从中抠出 JSON（`re.search(r'\{.*\}', ...)`），得 up/down 概率。追问"为什么不直接信输出格式"——程序化消费 AI 输出的第一步。
2. **实验任务布置与演示（25 分钟）**：宣布本节课内容为**实验任务（可以课后完成）**——按 `week07-streamlit-app-advanced.md` 四步推进：提取 JSON → 手写骨架（约 20 行，必须自己写）→ 把零件 + 骨架交给 Cursor/OpenCode 组装（"保留我的函数不动，只写 UI 编排"）→ 验收（换股票复跑、失败不崩、找出必须手改的 1–2 处）。课堂演示教师跑通一轮（对照成品 `cases/app.py` 或 `my-app-advanced/app.py`），学生课后完成自己的版本；进阶挑战（部署 / 加指标 / session_state / 缓存）自选。
3. **收束 + lab 起笔（12 分钟）**：个人项目路径走 `mvp-template/` 三步填充法（迁自己的 W4 数据与 W6 图，不是课堂的股票案例），`lab.md` 当堂起笔。布置课后任务：实验任务（见第 8 步，按升级篇文档）；以及**个人项目开题报告**（见下方课后作业块，含截止时间，布置和收束各说一遍）。当日 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）。互助记录只写「谁帮了你、对项目有何影响」，没有则写「无」。收集卡点（预计在 API key 配置与 JSON 提取）。

**课后作业 · 个人项目开题报告**

- **内容八项**：
  1. **封面**：题目、个人姓名、学号
  2. **研究动机**：研究背景、项目要解决的问题、研究意义
  3. **项目调研**：线下调研 / 文献调研 / 大模型辅助调研——不要求全部都有，但要**有机地组织在一起**（如：访谈证据定痛点 → 文献定参照 → 大模型辅助扫描补盲区）
  4. **预期解决方案设计**：初步设计方案描述 + 初步技术选型（框架选择理由）
  5. **解决方案评估方法与评估指标**：怎么判断产品有效（如用户反馈方式、准确性/效率类指标）
  6. **数据方案**：已落盘数据集与关键字段、来源与更新方式——确保在成本可控范围内获取足够丰富的数据
  7. **项目风险评估**：细致、逐项地列出项目推进中可能遭遇的风险及对应应对措施——如数据获取失败或质量不足、关键技术难点卡壳、API/数据成本超支、个人时间与课业冲突、功能范围膨胀等，每项风险写清「如果发生，怎么办」；含「不做」清单
  8. **参考资料列表**：列出全部参考文献（含访谈、官方文档、论文与书籍）；**正文中须以（作者，年份）格式规范引用**，如"金融舆情的传染效应显著（Loughran & McDonald, 2011）"，做到文中有引、文末有列、一一对应
- **提交**：**Word 版开题报告**（`.docx`），**10 页以上**。文件名 `开题报告-姓名-学号.docx`——**提交前将文件名中的「姓名」「学号」替换为你的学号与姓名**。**截止：2026年10月30日晚上8点。**

## 项目活动

**必做**

1. 每人搭建个人MVP原型：将W6可视化迁移到Streamlit/自选框架，可运行、核心功能可用

**进阶（可选）**
2. 将W4/W5已验证的分析流程封装为Skill（可选产品形式，非必做集成）
3. 有 Web 基础者用 React/Vue+FastAPI 定制前端

**兜底**

- Streamlit 卡住：先取最小模板 `weeks/week07/mvp-template/`（README 含三步填充法），搭出"数据加载+1 张图"骨架，再让 AI 按 W6 方案逐步填充；本周可运行底线 = 能打开并展示一个核心分析

## 交付物（评分锚点）

- 个人MVP v0.1（可运行）
- 个人项目开题报告（**Word 版，10 页以上**；内容八项齐全、论证充分）

—— 规格与知识锚定：MVP 见 milestones §2.4；开题报告为 milestones §1.4 的期中定稿版。均计入平时成绩（形成性）。提交前自检：数据加载→分析→可视化闭环可用？框架选择有理由？评估指标可操作、「不做」清单已写、风险与应对逐项对应？格式自检：Word 版、10 页以上、八项齐全、正文有（作者，年份）格式的文献引用且与文末列表一一对应？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

## 课后任务

1. 完成实验：应用 Streamlit 和大模型做一个预测股价波动方向的 APP——基础篇 `weeks/week07/week07-streamlit-app.md`（第 1 节 Streamlit 基础 → 第 2 节 tushare + 大模型，含验收点与存档点）+ 课后练习任务按升级篇 `week07-streamlit-app-advanced.md`（JSON 提取 → 手写骨架 → AI 辅助组装 → 验收），课堂案例 `streamlit.ipynb` 为底稿，报告要求见基础篇文末
2. 搭建可运行的MVP原型并测试核心功能
3. 提交个人项目开题报告（**Word 版** `.docx`**、10 页以上**，按开题报告规范论证充分；内容八项见教学步骤课后作业块）——**截止：2026年10月30日晚上8点**

## 学习资料

- 开题报告底稿模板：`templates/开题报告-姓名-学号.md`（复制、替换姓名学号、按八项填充，另存为 Word 提交）
- 本周演示笔记本：`streamlit.ipynb`（含 tushare 取数、DeepSeek 对话、预测 prompt、JSON 提取、APP 搭建全链）
- 实验基础篇：`week07-streamlit-app.md`（第 1 节 Streamlit 基础六步跟做、第 2 节 tushare + 大模型；含验收点、常见坑；第 1 节最终版 `stock_viewer.py` 兜底）
- 实验升级篇：`week07-streamlit-app-advanced.md`（课后练习任务：JSON 提取 → 手写骨架 → AI 辅助组装 APP → 验收手改点；含进阶挑战：部署 / 加指标 / session_state / 缓存）
- Streamlit 官方入门：[https://docs.streamlit.io/get-started（main-concepts](https://docs.streamlit.io/get-started（main-concepts) 一页讲完基础元件）
- tushare 每日指标接口文档：[https://tushare.pro/document/2?doc_id=32](https://tushare.pro/document/2?doc_id=32)
- `knowledge/phase2-2-10-rapid-prototyping.md`
- `knowledge/phase2-2-11-streamlit-gradio.md`
- `knowledge/phase2-2-12-ai-prototyping.md`
- `knowledge/phase3-3-6-skill-packaging.md`（Skill封装与复用，可选产品形式）
- `weeks/week07/mvp-template/`（最小骨架模板，兜底用）

