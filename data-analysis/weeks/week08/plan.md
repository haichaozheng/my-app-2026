# Week 08 教学计划

## 主题
LangChain入门 + 大模型赋能产品

> **前置**：须已完成 W7 MVP v0.1。本周为产品添加AI功能。

## 本周学习目标

- 能用 LangChain Chain + Prompt Template 构建 LLM 调用链，给 MVP 添加智能解读功能
- 能解释 Prompt Template 如何约束输出格式与可信度
- 能测试 AI 解读功能的 ≥2 个边界问题（幻觉/不准确/失效场景），并说明如何修正提示或流程

## 预计投入

课外 8-10h

## 教学内容
1. LangChain基础：Chain + Prompt Template
2. LLM API集成（通过LangChain调用LLM）——优先使用免费额度，费用注意事项见课程群公告；申请受阻走本周兜底
3. 用LangChain Chain构建LLM智能解读功能（产品AI功能的最小实现）

## 项目活动

**必做**
1. 学习LangChain基础，用Chain+Prompt Template构建LLM调用链
2. 给个人MVP添加LLM智能解读功能（如数据摘要、分析解读、智能问答），须绑定真实痛点而非锦上添花
3. 测试解读功能边界问题，记录可信度评估

**进阶（可选）**
- 提前把解读升级为 RAG 问答（W9 选做内容，知识库素材可直接用 W4/W5 积累）

**兜底**
- API Key 申请失败/额度用尽：用课程提供的演示 Key 完成本地功能验证（申请方式与使用规则见 `weeks/week08/llm-key-guide.md`），部署周（W10-W11）再换自己的 Key

## 交付物（评分锚点）

- 个人MVP v0.2（含LangChain LLM智能解读功能）

—— 规格与知识锚定见 milestones §2.5；计入平时成绩（形成性）。提交前自检：Chain 组织与 Template 约束有设计说明？AI 功能与痛点的关联讲得清？做过可信度测试并有记录？

## 卡住了找谁

卡住 → ①先问 AI（附报错与上下文截图）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）→ ④固定办公时间（1v1，时间见课程通知）。API Key 申请/额度问题直接走 ③（演示 Key 在课程群领取）。

## 课后作业
1. 集成LangChain LLM解读功能并测试
2. 记录AI功能的效果与边界（写入周反思日志 4.3 判断反思节）

## 学习资料
- `knowledge/phase2-2-13-llm-api.md`（含LangChain Chain + Prompt Template基础）
- `knowledge/phase2-2-14-rag.md`（提前选修：RAG构建产品知识库，W9正式引入）
- `weeks/week08/llm-key-guide.md`（API Key 三条获取路径 + 安全红线）
- 视频资料（超星学习通，详见 `video-resources.md`）：14.3 基于大模型API做开发（课前预习：对应本周 LLM API 集成）+ 14.4 提示词（prompt）设计（课前预习：对应本周 Prompt Template）；14.5 案例分析：基于财经新闻做股价涨跌预测（推荐观看：财经场景的 LLM 分析样例）
