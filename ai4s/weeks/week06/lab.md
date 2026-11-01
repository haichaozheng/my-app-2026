# Week 06 课堂实验

## 实验目标

按研究问题选择并论证数据来源路径，完成数据集构建与清洗，用 StatsPAI 实施实证估计并导出出版级表格，封装数据采集 Skill。

## 实验步骤

1. 路径选择论证：对照 W5 研究设计方案（方法条目与数据需求），确定自己的数据路径（第三方数据集 / 自采实验 / 智能体辅助生成类人数据），写下选择理由与一致性说明
2. 数据获取与清洗：按路径获取数据（第三方下载 / 一手采集 / persona prompt 批量生成）；变量操作化（理论概念→可分析变量）；缺失值、异常值、编码一致性检查
3. 安装 StatsPAI：`pip install statspai`；`sp.list_functions()` 浏览估计器清单，`sp.describe_function()` 查看用法
4. 锚定练习：用自带经典数据集（Card 1995 / LaLonde-NSW / mpdta）跑通 1-2 个估计器，观察 `validation_status`
5. 个人实证估计：以 W5 经审计确认的方法条目为准，选择对应估计器实施（回归/DID/IV/断点回归/合成控制/匹配/DML）
6. 导出出版级表格：`sp.regtable()` → Word/Excel/LaTeX
7. Skill 封装：把数据采集流程封装为数据 Skill（输入：数据源与参数；输出：清洗后数据集；边界清晰），在 opencode 中调用测试

## 实验交付

- 数据集（含数据来源路径选择说明）
- StatsPAI 实证代码与出版级表格（含 validation_status 说明）
- 数据 Skill 代码

## 卡住了

- 卡住 → 问 AI（附报错）→ 同学互助解答 → 举手教师
- 找不到合适估计器 → 先回 W5 方法条目，再 `sp.list_functions()` 对照；可用 `statspai-mcp` 让 opencode 里的智能体帮你 detect
- 硅基样本数据被质疑 → 检查是否有真实数据校准与生成属性声明（Argyle 2023 的适用边界）
