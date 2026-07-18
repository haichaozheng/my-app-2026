# LaTeX+AI

> **引入时机**：W8 | **核心挑战**："如何用AI辅助编程(LaTeX)进行论文排版？" | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

到了W8，论文内容逐渐成型，排版问题随之而来。Word在处理长文档、复杂公式、自动编号和参考文献管理时常常力不从心——格式崩溃、编号错乱、公式显示异常是每个用Word写过长论文的人都经历过的噩梦。LaTeX是学术排版的工业标准，但它有一套自己的标记语言语法，学习曲线陡峭。

这正是AI辅助编程的绝佳应用场景。LaTeX本质上是一种编程语言（标记语言），你完全可以用LLM帮你生成LaTeX代码，而不必从头学习所有命令。你只需要理解LaTeX的基本逻辑，具体的语法细节可以交给LLM处理。这就像你不需要记住Python的所有函数签名，只需要知道"我要做什么"，然后让AI帮你写出代码。

对于社科类博士生而言，LaTeX的必要性因学科而异。经济学、定量社会学等需要大量公式和表格的领域，LaTeX几乎是必备工具；质性研究为主的领域，Word或Overleaf的简单模板可能已经足够。但无论是否深度使用，了解LaTeX+AI的工作方式都能为你提供更多排版选择。

## 这个知识点的核心内容

### LaTeX基础与AI辅助

LaTeX的核心工作逻辑是"内容与格式分离"：你用标记命令描述文档的逻辑结构（这是标题、这是章节、这是公式），LaTeX编译器负责将其渲染为格式化的PDF。

**最小可用的LaTeX文档**：

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{geometry}
\geometry{margin=2.5cm}

\title{产业政策对企业创新的影响}
\author{张三 \\ 某某大学经济学院}
\date{\today}

\begin{document}
\maketitle
\begin{abstract}
本文研究......
\end{abstract}

\section{引言}
引言内容......

\section{理论框架}
理论框架内容......

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

**AI辅助生成LaTeX代码的Prompt模式**：

```
请帮我生成LaTeX代码，要求如下：
- 文档类型：article
- 字体大小：12pt
- 页面设置：A4纸，2.5cm边距
- 中文支持：使用ctex宏包
- 包含：标题、作者、摘要、三个章节、参考文献
```

LLM会生成完整的LaTeX代码，你只需复制到编辑器中编译即可。

### 社科论文LaTeX模板

社科论文不需要从零开始编写LaTeX模板，已有大量优质模板可直接使用：

**Overleaf模板库**（https://www.overleaf.com/latex/templates）：包含各主要期刊的投稿模板，直接搜索期刊名即可找到。

**常用社科模板**：
- 经济学：`economics` 文档类，或 AER、QJE 等期刊的官方模板
- 管理学：`amsart` 文档类或 Academy of Management 模板
- 社会学：`sociology` 文档类或 ASR 模板
- 政治学：`apsr` 文档类或 APSR 模板

**用LLM适配模板的Prompt**：

```
我需要在Overleaf上使用[期刊名]的LaTeX模板撰写论文。
我的论文结构是：摘要、引言、理论框架（含2个假设）、
研究方法、实证结果（含3个回归表和2个图）、
讨论、结论、参考文献。
请帮我：
1. 列出需要添加的宏包
2. 生成基本文档结构代码
3. 说明如何在该模板中插入表格和图片
```

### 公式、表格、引用的LaTeX编写

**公式编写**：

社科论文中常见的公式包括回归方程、理论模型等。用LLM生成公式代码：

```
请生成以下回归方程的LaTeX代码：
Y_it = α + β₁·Treatment_i × Post_t + β₂·X_it + μ_i + δ_t + ε_it
其中i表示企业，t表示年份，μ_i和δ_t分别表示企业和年份固定效应。
```

LLM生成：

```latex
\begin{equation}
\label{eq:did}
Y_{it} = \alpha + \beta_1 \cdot Treatment_i \times Post_t + \beta_2 \cdot X_{it} + \mu_i + \delta_t + \varepsilon_{it}
\end{equation}
```

**表格编写**：

社科论文中最常见的是回归结果表。用LLM生成：

```
请生成一个三列回归结果表的LaTeX代码，使用threeparttable宏包。
第(1)列是基准回归，第(2)列加入控制变量，第(3)列是稳健性检验。
每列需要报告系数、标准误（括号内）、显著性星号、观测数和R²。
```

LLM生成的代码会包含完整的表格结构，你只需填入具体的数值。

**引用管理**：

使用BibTeX管理引用是LaTeX的最佳实践。配合Zotero可以自动生成.bib文件：

```bibtex
@article{smith2023digital,
  title={Digital Platforms and Labor Relations},
  author={Smith, John A. and Wang, Li},
  journal={Journal of Labor Studies},
  volume={15},
  number={3},
  pages={123--145},
  year={2023},
  publisher={Springer}
}
```

在正文中引用：`\cite{smith2023digital}`

### AI辅助LaTeX排版的最佳实践

**实践1：用LLM做"LaTeX翻译器"**

不要记忆LaTeX命令，而是用自然语言描述你想要的效果，让LLM生成代码：

```
我想要一个两栏布局的表格，左栏是变量名，右栏是定义。
表格需要有灰色表头行，行间交替着色。
```

**实践2：用LLM做"错误诊断器"**

LaTeX编译错误信息往往难以理解。将错误信息复制给LLM：

```
我编译LaTeX时遇到以下错误：
! LaTeX Error: Too many }'
请帮我诊断问题。以下是我的代码：
[粘贴代码]
```

**实践3：用Overleaf+AI的协作流程**

1. 在Overleaf上选择期刊模板
2. 用LLM生成各部分的LaTeX代码框架
3. 将代码粘贴到Overleaf中
4. 在Overleaf中编辑内容、实时预览
5. 遇到格式问题时，将问题描述给LLM，获取解决方案

**实践4：将常用LaTeX片段保存为Skill**

将常用的LaTeX代码模板（如回归表、描述性统计表、摘要页）保存为Skill片段，在写作时直接调用：

```
你是一个社科论文LaTeX排版助手。
当我说"回归表"时，生成一个标准的三列回归结果表LaTeX代码。
当我说"描述性统计"时，生成描述性统计表LaTeX代码。
当我说"摘要页"时，生成包含标题、作者、摘要的首页代码。
所有表格使用threeparttable和booktabs宏包。
```

## 关键细节与易错点

- **易错：中文编码问题**。使用LaTeX处理中文必须加载ctex宏包，且编译器应使用XeLaTeX或LuaLaTeX，而非pdfLaTeX。Overleaf中可在菜单设置里切换编译器。
- **易错：表格溢出页面宽度**。社科论文常有变量名较长的宽表格，需要在tabular环境中使用`p{宽度}`列格式或`tabularx`宏包自动换行。用LLM生成表格时，在Prompt中说明"表格需适应页面宽度"。
- **易错：公式编号与引用不一致**。使用`\label{eq:xxx}`和`\ref{eq:xxx}`管理公式交叉引用，不要手动输入公式编号。
- **易错：BibTeX条目格式错误**。从数据库导出的.bib条目偶尔会有字段缺失或格式错误，编译前用LLM检查：`请检查以下BibTeX条目是否有格式错误：[粘贴条目]`。
- **易错：过度定制格式**。投稿期刊有固定模板时，不要试图"微调"模板格式。期刊编辑部会做最终排版，你只需要确保内容正确、结构清晰。

## 社科科研示例

场景：一位经济学博士生需要将Word论文迁移到LaTeX，使用AI辅助完成迁移。

**第一步：生成文档框架**

```
用户：我需要将以下论文结构转换为LaTeX：
标题、作者（两位，不同单位）、摘要、关键词、
JEL分类、引言、文献综述、理论模型、实证策略、
数据、结果（5个表+2个图）、稳健性检验、
结论、附录、参考文献。
请生成完整LaTeX代码，使用economics文档类，
支持中文，12pt字号。

LLM：（生成完整LaTeX框架代码）
```

**第二步：迁移回归表**

```
用户：请将以下Word中的回归表转换为LaTeX代码：
[描述或粘贴表格内容]
使用booktabs和threeparttable宏包，
标准误放在括号内，显著性用*标记。

LLM：（生成LaTeX表格代码）
```

**第三步：迁移公式**

```
用户：请将以下理论模型转换为LaTeX方程：
企业i在t期的创新产出Y_it由以下生产函数决定：
Y_it = A_it · K_it^α · L_it^(1-α)
其中A_it = A_0 · e^(γ·Subsidy_it) · e^(ε_it)

LLM：（生成LaTeX公式代码）
```

**完整工作流**：Word内容 → 逐部分复制给LLM → 生成LaTeX代码 → 粘贴到Overleaf → 编译预览 → 用LLM修复编译错误 → 迭代完善

## 拓展学习

- Overleaf Learn LaTeX in 30 Minutes —— LaTeX入门速成
- 《LaTeX入门》（刘海洋）—— 中文LaTeX最系统教材
- lshort-zh-cn（一份不太简短的LaTeX2e介绍）—— 中文社区维护的LaTeX入门文档

## 参考链接

- https://www.overleaf.com/learn — Overleaf官方教程，最实用的LaTeX学习资源
- https://www.overleaf.com/latex/templates — Overleaf模板库，涵盖各学科期刊模板（直接搜索期刊名）
- https://detexify.kirelabs.org/ — 手绘符号识别LaTeX命令
- https://tex.stackexchange.com/ — LaTeX问答社区
