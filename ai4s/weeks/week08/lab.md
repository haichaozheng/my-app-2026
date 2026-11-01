# Week 08 课堂实验

## 实验目标

运行写作-审计双 Agent 工作流完成论文初稿：Generator 起草、Auditor 核验引用与复现包、学生裁决，并起草 AI 使用声明、整合工具栈 v1。

## 实验步骤

1. 配置双 Agent（opencode agents primary/subagent）：Writing Generator（无网络与核验权限）+ Citation & Reproducibility Auditor（可调 Zotero MCP/学术搜索 MCP）
2. Generator 按章节起草 LaTeX 草稿（texai 类工作流：直接编辑 .tex，每一处修改在 PDF 上可见）
3. Auditor 逐条核验 Agent 插入引用的 DOI/元数据，输出引用核验报告（核验状态：通过/存疑/未通过）
4. 学生裁决：对存疑引用决定去留（替换为真实文献 / 删除 / 保留并标注）
5. Auditor 检查复现包完整性（代码、数据、环境说明、审计记录），产出完整性清单
6. AI 使用声明起草：对照 W1-W7 审计记录逐项写明各环节 AI 参与方式与人工裁决点
7. 五模块工具栈整合为可串联工作流（工具栈 v1），撰写案例与经验总结

## 实验交付

- 论文初稿（LaTeX+PDF，AI 修改可见）
- 引用核验报告（逐条 DOI/元数据核验状态）
- 复现包完整性清单
- AI 使用声明草稿
- AI4S 工具栈 v1 + 案例与经验总结
- 阶段反思日志（回应罗家德等（2026）第6章）

## 卡住了

- 卡住 → 问 AI（附上下文）→ 同学互助解答 → 举手教师
- 引用大量"未通过" → 正常现象：裁决去留，必要时回 Zotero 找真实文献替换
- Generator "自证核验通过" → 权限违例：它没有核验权，核验结论只能出自 Auditor
- .tex 编译报错 → 让 Generator 附上下文修复，修改须在 PDF 上可见
