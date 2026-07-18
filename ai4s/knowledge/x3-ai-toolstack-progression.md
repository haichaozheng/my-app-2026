# Prompt→RAG→Agent→Skill→评估 渐进融入

> **引入时机**：W1 | **核心挑战**："AI工具栈应该按什么顺序融入科研流程？为什么是这个顺序？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

AI4S课程引入了一系列AI工具——Prompt Engineering、RAG、Agent、Skill、AI评估——这些工具不是一次性全部上手的，而是随科研流程自然深入、渐进融入的。理解这个渐进逻辑至关重要，因为顺序错误会导致效率低下甚至项目失败。

试想两种极端：一种是"全副武装"——在W1就把RAG、Agent、Skill全部搭好，结果发现大部分功能用不上，维护成本远超收益；另一种是"始终裸奔"——9周只靠Prompt，结果到写作阶段发现文献管理混乱、分析不可重复、工作流碎片化。正确的做法是在合适的时机引入合适的工具——这正是"渐进融入"的核心。

渐进融入的逻辑不是随意的，而是有明确的方法论基础：每一步的"不够用"恰好是下一步的引入动机。Prompt不够用了才需要RAG（从单次交互到持久知识库），RAG不够用了才需要Agent（从被动检索到主动推理），Agent不够用了才需要Skill（从临时流程到可复用能力），而评估贯穿全程确保"做对"。理解这个逻辑，你就不仅知道"怎么做"，还知道"为什么这样做"——这是方法论自觉的体现。

## 这个知识点的核心内容

### AI工具栈的渐进融入逻辑

工具栈的渐进融入遵循一个核心原则：**需求驱动，最小够用**。每个新工具的引入都源于当前工具在特定环节的"力不从心"。

```
Prompt Engineering
  ↓ 当交互需要持久化知识时不够用
RAG（检索增强生成）
  ↓ 当需要多步骤自主推理时不够用
Agent（智能体）
  ↓ 当流程需要封装复用时不够用
Skill（技能模块）
  ↓ 全程需要质量控制
评估（质量闭环）
```

为什么是这个顺序？因为每一层都是对前一层的增强，而非替代：

- Prompt是基础——与LLM交互的能力是所有上层工具的根基
- RAG增强了Prompt——通过知识库提供持久化的领域知识
- Agent增强了RAG——不仅能检索知识，还能基于知识自主推理和行动
- Skill增强了Agent——将Agent的能力固化为可复用的模块
- 评估贯穿全程——确保每一层的输出质量可控

### 从Prompt到RAG的进化

**Prompt的局限**：Prompt是与LLM的"单次交互"——每次对话都是独立的，LLM无法记住你之前的文献积累、理论选择或分析结果。在文献综述阶段，这意味着你每次都要重新告诉LLM你的研究背景。

**RAG的增强**：RAG将你的知识持久化——文献要点、理论框架、方法论文献都被存储在向量数据库中，每次与LLM交互时自动检索相关内容注入上下文。你不需要每次重复交代背景，RAG帮你"记住"。

**具体的进化场景**：

在W1，你用Prompt做文献综述：
```
请帮我总结这篇文献的核心观点：[粘贴摘要]
```
每篇文献都是独立处理，无法跨文献发现关联。

在W2，你用RAG做文献综述：
```python
from rag_system import RAGQuery

rag = RAGQuery(knowledge_base="literature_kb")
results = rag.search("政治参与的理论视角")
for doc in results:
    print(f"来源: {doc.metadata['title']}")
    print(f"相关度: {doc.score:.2f}")
    print(f"内容: {doc.content[:200]}")
```
RAG自动检索知识库中与"政治参与的理论视角"相关的所有文献段落，并可以跨文献发现理论对话关系。

**进化标志**：当你发现自己在反复向LLM交代相同的研究背景时，就是引入RAG的时机。

### 从RAG到Agent的进化

**RAG的局限**：RAG是"被动检索"——你提问，它返回相关内容。但科研中的许多任务需要"主动推理"——如基于理论框架推演研究假设、基于数据特征选择分析方法、基于审稿意见修改论文。这些任务不是简单的检索，而是多步骤的推理和决策。

**Agent的增强**：Agent将LLM从"被动回答"升级为"主动行动"——它可以分解复杂任务、选择调用工具、评估中间结果、调整执行策略。

**具体的进化场景**：

在W3，你用RAG+Prompt做选题：
```
用户：请检索与"数字化转型与组织韧性"相关的文献。
RAG：[返回相关文献]
用户：[阅读后] 请基于这些文献，提出3个潜在的研究方向。
LLM：[提出3个方向]
用户：[逐一评估] 请评估第2个方向的可行性。
LLM：[评估]
```
整个过程中，你需要自己驱动每一步。

在W4，你用Agent做选题和设计：
```python
from agent import ResearchAgent

agent = ResearchAgent(
    knowledge_base="literature_kb",
    research_topic="数字化转型与组织韧性"
)

design = agent.run_task(
    "基于文献知识库，识别研究缺口，提出3个研究问题，"
    "评估每个问题的学术贡献和可行性，"
    "为最优问题设计研究方案，"
    "包括方法选择、数据需求和预期贡献。"
)

print(design.recommended_question)
print(design.research_plan)
print(design.methodology_justification)
```
Agent自主完成了"识别缺口→提出问题→评估→设计"的多步推理。

**进化标志**：当你发现自己需要手动驱动多轮对话来完成一个复杂任务时，就是引入Agent的时机。

### 从Agent到Skill的进化

**Agent的局限**：Agent适合处理"一次性"的复杂任务，但科研中有许多"重复性"任务——每次修改变量都需要重新跑回归，每次润色段落都需要写相似的Prompt，每次检查引用都需要执行相同的流程。Agent每次都要重新理解任务和规划步骤，效率低下。

**Skill的增强**：Skill将反复使用的流程固化为可复用的模块——预先定义好角色、规则和输出格式，每次调用只需提供变化的部分。

**具体的进化场景**：

在W6，你用Agent做数据分析：
```
用户：请帮我执行双重差分回归，因变量为innovation，
处理变量为treatment，控制变量为size和age。

Agent：[理解任务→规划步骤→生成代码→执行→返回结果]
```
每次分析都要重新说明任务和参数。

在W7，你用Skill做数据分析：
```python
from skill import DIDRegressionSkill

did_skill = DIDRegressionSkill(
    dependent_var="innovation",
    treatment_var="treatment",
    control_vars=["size", "age"],
    cluster_var="firm_id",
    fixed_effects=["firm_id", "year"]
)

result = did_skill.execute(data_path="data/cleaned.csv")
print(result.regression_table)
print(result.parallel_trend_test)
```
Skill封装了DID回归的完整流程（包括前提检验），调用只需改变参数。

**进化标志**：当你发现自己在重复执行相似的Agent任务时，就是封装Skill的时机。

### 从工具到评估的闭环

**评估的核心地位**：评估不是工具栈的"最后一层"，而是贯穿全程的"闭环机制"。每一层的输出都需要评估：

- Prompt的输出需要评估：LLM的回答是否准确、是否有幻觉、是否符合学术规范
- RAG的检索需要评估：检索到的文献是否相关、覆盖度是否足够、是否有重要遗漏
- Agent的决策需要评估：推理链路是否合理、方法选择是否有论证、是否遵守方法论约束
- Skill的执行需要评估：输出格式是否正确、结果是否可验证、是否满足质量标准

**评估的层次**：

```
层次1：输出质量评估
  - 结果是否正确（可验证性）
  - 格式是否符合预期（规范性）

层次2：过程质量评估
  - 方法选择是否合理（方法论锚定）
  - 推理链路是否完整（逻辑性）

层次3：方法论质量评估
  - 是否"做对"了（方法论自觉）
  - 是否可迁移到新场景（可迁移性）
```

**评估的具体实践**：

```python
class QualityEvaluator:
    def evaluate_output(self, output, criteria):
        results = {}
        for criterion in criteria:
            if criterion == "accuracy":
                results["accuracy"] = self._check_accuracy(output)
            elif criterion == "citation_validity":
                results["citation_validity"] = self._check_citations(output)
            elif criterion == "methodology_alignment":
                results["methodology_alignment"] = self._check_methodology(output)
        return results

    def _check_accuracy(self, output):
        pass

    def _check_citations(self, output):
        pass

    def _check_methodology(self, output):
        pass
```

**进化标志**：当你发现自己在每次产出后都要手动检查质量时，就是将评估流程系统化的时机。

## 关键细节与易错点

- **易错：跳级引入工具**。在Prompt还够用的阶段就引入RAG，在RAG还够用的阶段就引入Agent——这会导致过度工程化，增加维护成本而不增加价值。应该等到"不够用"的信号出现再引入。
- **易错：替代而非增强**。引入RAG后不再用纯Prompt，引入Agent后不再用RAG——这是错误的。新工具增强而非替代旧工具。最简单的任务用Prompt，需要知识库的任务用RAG，需要推理的任务用Agent，需要复用的任务用Skill——各司其职。
- **易错：忽视评估的持续性**。评估不是工具栈搭建完才做的事，而是每个环节都需要的质量保障。忽视评估会导致错误累积和放大。
- **易错：混淆"工具能力"和"方法论需求"**。引入新工具的决策应基于"方法论需要什么"而非"这个工具能做什么"。不是"Agent能做X所以我用它"，而是"我的研究需要X，Agent是满足这一需求的最优工具"。
- **易错：过早优化工具栈**。在科研早期阶段，工具栈应保持灵活，不要过早固化。只有当某种模式经过多次验证后，才值得封装为Skill。

## 社科科研示例

场景：一位传播学博士生研究"算法推荐对新闻消费多样性的影响"，展示工具栈的渐进融入过程。

**W1-W2：Prompt阶段**

初期只用Prompt做文献综述。每篇文献单独处理，用Prompt提取关键信息：
```
请提取这篇文献的理论视角、研究方法、核心发现。
```

**W2末：引入RAG**

当文献积累到80+篇，发现无法跨文献追踪理论脉络时，引入RAG。将所有文献笔记导入向量数据库，实现语义检索：
```
RAG检索："新闻多样性"相关的理论框架
→ 返回：议程设置理论、选择性暴露理论、信息茧房假说的相关段落
```

**W3：Prompt+RAG做选题**

用RAG检索研究缺口，用Prompt评估选题可行性。发现仍需手动驱动多轮对话。

**W4：引入Agent**

选题和设计环节需要多步推理（识别缺口→评估可行性→设计方案），引入设计Agent：
```python
agent.design_research(
    topic="算法推荐与新闻多样性",
    methodology_preference="因果推断",
    data_availability="用户行为日志+问卷调查"
)
# Agent自动完成：文献缺口分析→研究问题提出→方法选择→方案设计
```

**W6-W7：引入Skill**

数据分析环节发现重复性任务（多次修改模型、重新估计），封装分析Skill：
```python
ols_skill = OLSRegressionSkill(
    dep_var="news_diversity",
    indep_vars=["algorithm_exposure", "active_search", "media_literacy"],
    controls=["age", "education", "income"],
    robust_se=True
)
result = ols_skill.execute("data/survey.csv")
```

**W8：封装写作Skill**

写作环节发现反复润色、格式检查，封装写作Skill。

**全程：评估闭环**

每个环节都执行评估：
- RAG检索结果评估：相关度、覆盖度
- Agent决策评估：方法论合理性
- Skill输出评估：结果可验证性
- 论文质量评估：学术规范性

## 拓展学习

- LangChain教程 —— 理解RAG→Agent→Tool的技术实现链路
- "Chain-of-Thought Prompting" (Wei et al., 2022) —— 从Prompt到推理的进化
- "Toolformer" (Schick et al., 2023) —— LLM自主使用工具的能力

## 参考链接

- https://www.promptingguide.ai/ — Prompt到Agent的技术演进
- https://python.langchain.com/ — LangChain框架，RAG和Agent的实现参考
- https://docs.llamaindex.ai/ — LlamaIndex框架，RAG系统的实现参考
