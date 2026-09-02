# Week 07 教学计划

## 主题
产品原型搭建 + AI辅助编程加速原型

> **前置**：须已完成 W6 可视化方案设计，本周将可视化迁移进产品框架（W6 未完成的交互式实现随本周合并完成）。

## 本周学习目标

- 能说明产品框架选择理由（为什么 Streamlit/Gradio/自选框架，而非"别人都在用"）
- 能把 W6 可视化方案迁移进可运行的产品原型，形成"数据加载→分析→可视化"基本闭环
- 能让 AI 辅助编程完成大部分原型代码，并指出哪些输出需要人工修改、为什么

## 预计投入

课外 10-12h（第一个完整产品周，投入峰值之一）

## 教学内容
1. Streamlit 快速原型（必做）
2. Gradio 快速原型（可选，适合AI交互类产品）
3. 用AI辅助编程加速原型搭建
4. Skill作为可选产品形式（把W4/W5已验证的分析流程封装为Skill，是产品展示形式之一，非必做）

**进阶自学**（有Web开发基础、追求更灵活定制的同学）：React/Vue前端 + FastAPI后端。参考资源：
- React：https://react.dev/learn
- Vue：https://vuejs.org/guide/introduction.html
- FastAPI：https://fastapi.tiangolo.com/zh/tutorial/

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

—— 规格与知识锚定见 milestones §2.4；计入平时成绩（形成性）。提交前自检：数据加载→分析→可视化闭环可用？核心功能对应手动分析已验证环节有说明？框架选择有理由？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。

## 课后作业
1. 搭建可运行的MVP原型
2. 测试核心功能

## 学习资料
- `knowledge/phase2-2-10-rapid-prototyping.md`
- `knowledge/phase2-2-11-streamlit-gradio.md`
- `knowledge/phase2-2-12-ai-prototyping.md`
- `knowledge/phase3-3-6-skill-packaging.md`（Skill封装与复用，可选产品形式）
- `weeks/week07/mvp-template/`（最小骨架模板，兜底用）
