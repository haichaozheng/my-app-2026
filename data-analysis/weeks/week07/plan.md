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
- React：https://react.dev/learn
- Vue：https://vuejs.org/guide/introduction.html
- FastAPI：https://fastapi.tiangolo.com/zh/tutorial/

## 课堂演示工具

| 环节 | 工具 | 用法 |
|---|---|---|
| 概念 | 薄幻灯（≤6页） | 为何选 Streamlit；数据加载→分析→可视化闭环 |
| 现场主演示 | Jupyter Notebook + Cursor/OpenCode + 浏览器 | `streamlit.ipynb` 案例「股价预测 APP」一条链到底：Streamlit 基础 → tushare 取数 → 大模型预测 → 课堂搭 APP；AI 辅助编程（Cursor/OpenCode），浏览器验收 |
| 学生跟做 | Cursor/OpenCode + Streamlit | 底线：能打开并展示一个核心分析 |
| 不做 | 只在 Jupyter 里交「产品」 | Notebook 是实验室，产品是店面 |

## 教学步骤

每周 3 节课，每节 45 分钟（课间另计）。课前：主演示笔记本 `streamlit.ipynb` 已跑通——tushare token、`DEEPSEEK_API_KEY` 已配入 `.env`（不入库、不发群里）；`mvp-template/` 可一键跑起（兜底用）。

**第1节 · Streamlit：从 Notebook 到店面（45 分钟）**

1. **分享上周 journal + 实验室 vs 店面（8 分钟）**：随机邀请同学分享上周 journal（3 问：补上了哪个缺口 / 哪个判断不稳 / 下周先解哪个卡点）。Notebook 交作业 ≠ 产品；本周底线 = 浏览器能打开并展示一个核心分析。
2. **Streamlit 入门（12 分钟）**：为何 Streamlit（本课程及以后其他课程的项目展示都用得上，docs：docs.streamlit.io/get-started）；`pip install streamlit`；`streamlit hello` 现场看案例展示；`streamlit run your_script.py` 是唯一的运行入口。
3. **Basic concepts 跟做（25 分钟）**：My first app（DataFrame 直接显示）；`st.table`（静态表）与 `st.line_chart`（一行出图）；`st.slider` widget + `st.session_state` 取值；`st.selectbox` 选项联动；`st.empty` + `st.progress` 做长计算进度条。每格停问"这格得到了什么"。收束一句："Streamlit = 把 notebook 的格子变成网页的元件。"

**第2节 · 案例：取数与大模型对话——股价预测的原材料（45 分钟）**

4. **tushare 取每日指标（15 分钟）**：`ts.set_token` + `pro.daily_basic` 单日取 000001.SZ（换手率/量比/PE/PB，doc_id=32）；再倒推 5 天循环取多天数据——`Timestamp`/`Timedelta` 正好接 W6，"循环取数+容错跳过"是接 API 的通用套路。
5. **chat with AI（12 分钟）**：课堂默认 **DeepSeek**（`DEEPSEEK_API_KEY` 放 `.env`，`load_dotenv` 读取，密钥永不硬编码）；兼容 OpenAI 接口，封装 `llm_chat`；先 `llm_chat("hello")` 跑通再谈业务。点一句换厂商的方法：只改 `base_url`、模型名和 API Key 环境变量（豆包等其他兼容 OpenAI 接口的服务同理），学生用哪家的 Key 都能跟。
6. **构造预测 prompt 并预测（18 分钟）**：问题（第五个交易日涨还是跌）+ 判断标准 + materials（`df.to_dict(orient='records')`）；7 步指令（重述问题 → 正反理由及强度 → 聚合 → 初始概率 → 反思 → 最终 JSON 概率，中文回答）。课堂跑一次，让学生看到大模型如何"像超级预测员一样"给出 up/down 概率。点一句：把 W6 的 groupby 结果当 materials 喂给大模型，就是同一个套路。

**第3节 · 从回答到应用：Streamlit + AI 辅助编程搭 APP（45 分钟）**

7. **extract_json 提取概率（8 分钟）**：大模型输出是长文本，用正则从中抠出 JSON（`re.search(r'\{.*\}', ...)`），得 up/down 概率。追问"为什么不直接信输出格式"——程序化消费 AI 输出的第一步。
8. **Streamlit 应用搭建 + AI 辅助编程（25 分钟）**：把"取数 → prompt → 预测 → 提取 → 展示"整条链搬进 `app.py`，**尽量在课堂完成**。`st.selectbox` 选股票、按钮触发预测、`st.progress` 显示等待、`st.write` 出概率结论。用 Cursor 或 OpenCode 辅助编程实现（在项目根目录把 `streamlit.ipynb` 里的链路代码和需求描述一起作为上下文交给 AI），验收时指出 AI 生成代码里必须手改的 1–2 处（token、`.env` 路径、列名）；鼓励学生从 tushare 取其他有价值指标提高预测准确性。
9. **收束 + lab 起笔（12 分钟）**：个人项目路径走 `mvp-template/` 三步填充法（迁自己的 W4 数据与 W6 图，不是课堂的股票案例），`lab.md` 当堂起笔。布置课后任务：实验——应用 Streamlit 和大模型做一个预测股价波动方向的 APP；以及**个人项目选题报告**（见下方课后作业块，含截止时间，布置和收束各说一遍）。当日 `journal.md` 追加 1 条（今天做了什么 / 关键决定 / 学习并掌握的新东西 / 卡点 / 互助记录）。互助记录只写「谁帮了你、对项目有何影响」，没有则写「无」。收集卡点（预计在 API key 配置与 JSON 提取）。

**课后作业 · 个人项目选题报告**

- **定位**：MVP 是壳，选题是魂。第一个完整产品周，用一份选题报告把前 6 周的探索收敛成定稿——W1-W3 的痛点验证、W4 的数据落地、W5 的 EDA 发现、W6 的可视化方案，最终回答"你的产品到底为谁解决什么问题"。它以 W3 已过审的 `docs/requirements.md` 为底稿**更新**（不是重写），标注「选题报告 v2」，作为 v0.1 迭代到期末路演的锚，也是教师深评点之一（W3 提案 → W7 选题定稿+v0.1 → W13 反馈分析）。
- **内容六项**：①选题名称 + 一句话定位（谁 × 在什么场景 × 解决什么问题）；②选题来源与痛点验证状态（命中三档来源中哪档；引用 `docs/community.md` 原话与访谈证据，如实标注哪些已验证、哪些仍是假设）；③数据方案（已落盘数据集与关键字段、来源与更新方式）；④核心功能清单（每个功能指回 W4/W5 已验证的哪个价值环节，标出 v0.1 先做哪个）；⑤技术与 AI 方案（框架选择理由、大模型在产品中的角色）；⑥风险与「不做」清单。
- **提交**：`docs/requirements.md` 更新版（模板见 `templates/requirements.md`）。**截止：2026年11月6日晚上8点。** 以整合已有文档为主，预计 1-2h，不与 MVP 抢时间——先写报告再迭代壳，反而省返工。

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
- 个人项目选题报告（`docs/requirements.md` 更新版「选题报告 v2」）

—— 规格与知识锚定：MVP 见 milestones §2.4；选题报告以 W3 提案（milestones §1.4）为底稿的期中定稿版。均计入平时成绩（形成性）。提交前自检：数据加载→分析→可视化闭环可用？核心功能对应手动分析已验证环节有说明？框架选择有理由？选题报告的验证/假设如实标注、「不做」清单已写？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

## 课后任务
1. 完成实验：应用 Streamlit 和大模型做一个预测股价波动方向的 APP（课堂案例 `streamlit.ipynb` 为底稿）
2. 搭建可运行的MVP原型并测试核心功能
3. 提交个人项目选题报告（`docs/requirements.md` 更新版「选题报告 v2」，内容六项见教学步骤课后作业块）——**截止：2026年11月6日晚上8点**

## 学习资料
- 本周演示笔记本：`streamlit.ipynb`（含 tushare 取数、DeepSeek 对话、预测 prompt、JSON 提取、APP 搭建全链）
- Streamlit 官方入门：https://docs.streamlit.io/get-started（main-concepts 一页讲完基础元件）
- tushare 每日指标接口文档：https://tushare.pro/document/2?doc_id=32
- `knowledge/phase2-2-10-rapid-prototyping.md`
- `knowledge/phase2-2-11-streamlit-gradio.md`
- `knowledge/phase2-2-12-ai-prototyping.md`
- `knowledge/phase3-3-6-skill-packaging.md`（Skill封装与复用，可选产品形式）
- `weeks/week07/mvp-template/`（最小骨架模板，兜底用）
