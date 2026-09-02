# 大模型做数据分析（分析引擎）

> **引入时机**：W14 | **核心挑战**："如何让LLM本身成为数据分析/建模引擎？与传统ML如何互补？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

W11-W13你用传统ML建立了预测模型（回归/分类），W8用LangChain构建了LLM智能解读。现在面临一个问题：LLM能直接做数据分析吗？它和传统ML有什么区别和互补？

答案是：LLM不能替代传统ML（无法训练模型、无法处理结构化大规模数据），但它在以下场景远超传统ML：
- **解读已有模型的结果**：把训练好的模型输出、特征重要性等喂给LLM，让它生成人类可读的分析报告
- **代码生成做分析**：用LLM生成pandas/sklearn代码，加速探索性分析和建模迭代
- **洞察发现**：从非结构化文档（研报、年报）中提取规律和洞察
- **建模实验设计**：帮你规划"该试什么模型、该加什么特征"的实验路线

本知识点让你的AI能力从"W8的智能解读"升级为"W14的分析引擎"——LLM不再只是回答用户问题，而是主动参与数据分析和建模过程，成为你的"AI分析师"。

## 这个知识点的核心内容

### LLM做数据分析 vs 传统ML建模

| 维度 | LLM做数据分析 | 传统ML建模 |
|------|--------------|------------|
| 核心能力 | 文本理解、推理、代码生成 | 从数据中学习映射关系 |
| 输入 | 自然语言指令、文档、对话 | 结构化特征矩阵 |
| 输出 | 文字洞察、代码、报告 | 预测值/概率 |
| 数据要求 | 不需要训练数据，但需要领域上下文 | 需要标注好的训练数据 |
| 可解释性 | 高（自然语言解释） | 中（需要SHAP/LIME等） |
| 适用场景 | 洞察发现、报告生成、代码辅助、实验设计 | 预测任务、分类、回归 |

**关键认知：两者是互补而非替代**
- 传统ML负责"预测"（告诉你结果）
- LLM负责"解读"（告诉你为什么、怎么理解）
- 结合使用：ML出预测 → LLM解读 → 生成可读报告

### 用LLM做探索性分析

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="deepseek-chat", temperature=0.3, max_tokens=1500)
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深金融数据分析师。基于提供的数据摘要，给出深度分析洞察。
回答要求：
1. 先给出3-5个核心发现
2. 每个发现用数据支撑（引用具体数字）
3. 指出潜在的风险和异常
4. 给出下一步分析建议"""),
    ("user", "{data_summary}")
])

chain = prompt | llm | StrOutputParser()

# 用LLM分析EDA结果
eda_summary = """
银行板块2024年数据摘要：
- 工商银行：PE 5.2, PB 0.61, ROE 11.5%, 股息率5.8%, 年涨跌幅-8.3%
- 招商银行：PE 6.1, PB 0.92, ROE 15.2%, 股息率3.2%, 年涨跌幅+12.5%
- 兴业银行：PE 4.8, PB 0.52, ROE 10.8%, 股息率6.1%, 年涨跌幅-15.2%
- 行业平均PE 5.5, PB 0.68, ROE 12.5%
- 近3个月银行板块成交量放大35%，资金流入明显
"""
result = chain.invoke({"data_summary": eda_summary})
print(result)
```

### 用LLM生成分析代码

```python
code_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是Python数据分析代码助手。根据用户需求生成可运行的分析代码。
要求：
1. 使用pandas、matplotlib/plotly
2. 代码可直接复制运行
3. 包含注释说明每步操作"""),
    ("user", "{analysis_request}")
])

code_chain = code_prompt | llm | StrOutputParser()

result = code_chain.invoke({
    "analysis_request": """帮我分析data/bank_stocks.csv中银行股的：
1. 收益率分布直方图
2. 相关性矩阵热力图
3. 波动率排名
输出要求：保存为HTML文件方便查看"""
})
print(result)
# 生成的代码可直接运行
```

### 用LLM解读ML模型结果

```python
def explain_model_results(model, feature_names, X_test, y_test, y_pred):
    """用LLM解读模型预测结果"""
    from sklearn.metrics import accuracy_score, classification_report
    import pandas as pd
    
    report = classification_report(y_test, y_pred, target_names=["跌", "涨"])
    acc = accuracy_score(y_test, y_pred)
    
    prompt = f"""你是金融数据科学顾问。基于以下模型结果，给出深度解读：

模型类型：{type(model).__name__}
测试集准确率：{acc:.2%}
分类报告：
{report}
特征名：{feature_names}
模型特征重要性：{dict(zip(feature_names, getattr(model, 'feature_importances_', [0]*len(feature_names))))}

请解读：
1. 这个模型表现如何？从金融角度看意味着什么？
2. 哪些特征最重要？为什么这些特征有预测力？
3. 模型的主要局限是什么？如何改进？
4. 对投资/风控的实操建议是什么？"""
    
    response = llm.invoke([("user", prompt)])
    return response.content
```

### LLM分析实验框架

W14的核心任务是完成一个"LLM分析实验"，展示LLM如何与传统ML互补：

```python
# 实验1：LLM解读ML模型的预测结果
# 流程：ML预测 → LLM解读 → 生成分析报告

# 实验2：LLM辅助特征工程
# 流程：LLM建议特征 → 代码生成 → 验证效果

# 实验3：LLM从研报中提取洞察
# 流程：crawl4ai采集研报 → LLM分析 → 结构化输出
```

**实验报告模板**：
1. 实验目标：要解决什么问题
2. 方法对比：传统方法 vs LLM辅助方法
3. 结果对比：效果差异
4. 洞察：LLM的优势和局限

## 关键细节与易错点

- **易错：把LLM当万能分析师**。LLM擅长解读和生成，不擅长精确定量计算和大规模数据处理——数值计算交给pandas/sklearn
- **易错：忽略LLM幻觉**。LLM生成的分析可能包含不存在的数据点或错误计算——关键结论需用代码验证
- **易错：不做实验对比**。W14要求展示LLM vs 传统ML的适用边界，必须有实证对比而非主观判断
- **易错：用LLM直接训练模型**。LLM不是ML框架，无法训练sklearn/torch模型——LLM负责分析和解读，模型训练交给传统ML

## 拓展学习

- LangChain LLM应用开发教程——构建LLM分析Pipeline
- 《Building LLM Apps》LLM分析章节——LLM作为数据分析引擎的架构设计
- 金融AI应用场景——LLM在投行研报分析、投资组合解读中的真实案例

## 参考链接

- https://python.langchain.com/docs/tutorials/llm_chain/ — LangChain LLM Chain教程
- https://python.langchain.com/docs/tutorials/ — LangChain应用教程库
- https://python.langchain.com/docs/ — LangChain官方文档
