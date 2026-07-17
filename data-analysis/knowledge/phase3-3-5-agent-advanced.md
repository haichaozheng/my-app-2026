# Agent驱动高级功能

> **引入时机**：W13 | **核心挑战**：如何让产品自动监控市场变化、自动生成报告？ | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

当你的金融数据分析产品有了基础的查询和可视化功能后，用户会期望更高级的体验：不是每次都手动查询，而是产品能主动推送关键信息；不是只看静态图表，而是能自动发现异常并解释原因；不是只回答单一问题，而是能执行多步骤的复杂分析任务。这些需求超出了简单工具的范畴，需要Agent（智能体）来自主规划和执行。

Agent是LLM应用的高级形态——它不再只是"输入问题、输出答案"，而是能自主分解任务、调用工具、根据中间结果调整策略，最终完成复杂目标。在金融领域，Agent的价值尤为突出：市场监控需要7x24不间断、信息解读需要多数据源交叉验证、报告生成需要结构化执行流程。这些恰好是Agent擅长的场景。

在PBL项目中，添加Agent驱动的功能能让你的产品从"被动工具"升级为"主动助手"，这是产品差异化的重要方向。理解Agent的工作模式和技术架构，也是理解AI应用发展趋势的关键。

## 这个知识点的核心内容

### Agent基础概念

Agent是一个能自主决策并执行操作的AI系统，核心组成：

- **LLM（大脑）**：理解任务、规划步骤、做出决策
- **工具（双手）**：Agent可以调用的外部能力，如搜索、数据库查询、图表生成
- **记忆（经验）**：短期记忆（对话上下文）和长期记忆（知识库）
- **规划（策略）**：将复杂任务分解为可执行的步骤序列

Agent与普通LLM调用的关键区别：Agent在执行过程中观察中间结果，动态调整下一步行动，而非一次性生成全部输出。

### Agent工作模式

常见的Agent工作模式：

- **ReAct模式**：Reason（推理当前状态）→ Act（选择并执行工具）→ Observe（观察结果）→ 循环。最经典的Agent框架
- **Plan-and-Execute模式**：先制定完整计划，再逐步执行。适合任务步骤确定、不需要频繁调整的场景
- **多Agent协作模式**：多个专精Agent分工协作，如一个负责数据获取、一个负责分析、一个负责报告生成

### 金融Agent常用工具

为Agent配备金融领域的专用工具：

- **行情查询工具**：获取实时/历史行情数据
- **财务数据工具**：查询公司财报、估值指标
- **新闻搜索工具**：搜索和摘要财经新闻
- **图表生成工具**：根据数据自动生成可视化图表
- **计算工具**：执行数学计算（夏普比率、相关性等）
- **报告生成工具**：将分析结果组装为结构化报告

### 定时任务与自动化

金融Agent的一个重要应用是定时自动化：

- **定时触发**：使用APScheduler、cron或云函数定时触发Agent任务
- **事件驱动**：当市场出现特定条件时触发Agent（如指数跌破关键点位）
- **结果推送**：Agent完成后通过邮件、微信、钉钉推送结果
- **异常告警**：Agent监控到异常时主动告警

### 报告生成Agent

报告生成是Agent在金融领域的高价值应用：

- **数据收集**：自动获取所需的行情、财务、新闻数据
- **分析执行**：按预设流程计算指标、识别模式、对比历史
- **图表生成**：自动生成关键图表嵌入报告
- **文字撰写**：用LLM将分析结果组织为可读文字
- **格式输出**：生成Markdown、PDF或HTML格式的报告

## 关键细节与易错点

### Agent陷入循环

Agent可能在ReAct循环中反复执行相同操作（如反复查询同一数据），消耗大量token而无法完成任务。解决方案：设置最大迭代次数、记录已执行操作避免重复、检测循环模式并强制终止。

### 工具调用失败未处理

Agent调用的工具可能失败（API超时、数据不存在），如果不处理失败，Agent可能基于空数据继续推理，产生幻觉结果。每个工具调用都需要错误处理和结果验证。

### 缺乏结构化输出

Agent的LLM输出是自由文本，如果不做结构化约束，很难保证输出格式一致。使用structured output（如function calling的JSON schema）或输出模板，确保Agent结果可被下游程序解析。

### 忽视成本控制

Agent每次迭代都消耗LLM token，复杂任务可能消耗大量token。金融监控Agent如果每日高频运行，成本可能很高。控制方法：缓存中间结果、使用更便宜的小模型做简单判断、只在关键步骤调用大模型。

### Agent权限过大

Agent如果可以执行交易操作，必须设置严格的权限边界和审批流程。金融Agent应该默认只读，任何涉及实际操作的步骤都需要人工确认。

### 定时任务的重试与幂等性

定时Agent可能因网络问题执行失败，需要设计重试机制。同时，重试时必须保证幂等性——同一任务执行多次不应产生重复结果（如重复发送报告）。

## 金融数据分析示例

**场景**：构建一个每日市场晨报Agent，自动监控持仓股票、检测重大事件、生成晨间简报。

**Agent工具定义**：

```python
from langchain_core.tools import tool

@tool
def get_stock_data(symbol: str, days: int = 30) -> str:
    stock = ak.stock_zh_a_hist(symbol=symbol, period="daily", count=days)
    latest = stock.iloc[-1]
    change = (latest["close"] - stock.iloc[-2]["close"]) / stock.iloc[-2]["close"]
    return f"{symbol}: 收盘{latest['close']:.2f}, 涨跌幅{change:.2%}, 成交额{latest['amount']:.0f}元"

@tool
def check_price_alert(symbol: str, threshold: float = 0.03) -> str:
    stock = ak.stock_zh_a_hist(symbol=symbol, period="daily", count=2)
    change = (stock.iloc[-1]["close"] - stock.iloc[-2]["close"]) / stock.iloc[-2]["close"]
    if abs(change) > threshold:
        return f"ALERT: {symbol}涨跌幅{change:.2%}超过阈值{threshold:.0%}"
    return f"{symbol}涨跌幅{change:.2%}，正常"

@tool
def get_financial_news(keyword: str, count: int = 5) -> str:
    news = ak.stock_news_em(symbol=keyword)
    headlines = news["新闻标题"].head(count).tolist()
    return "\n".join(f"- {h}" for h in headlines)
```

**Agent工作流**：

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个金融晨报助手。根据用户持仓，执行以下步骤：
1. 查询每只股票的行情数据
2. 检查是否有涨跌幅超过3%的异常
3. 搜索相关财经新闻
4. 将结果整理为晨间简报，包含：市场概览、持仓变动、重要新闻、今日关注"""),
    ("human", "我的持仓：{portfolio}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_stock_data, check_price_alert, get_financial_news]
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, max_iterations=15)
```

**定时执行**：

```python
from apscheduler.schedulers.background import BackgroundScheduler

def generate_morning_brief():
    portfolio = "600519,000858,601318"
    result = executor.invoke({"portfolio": portfolio})
    send_notification(result["output"])

scheduler = BackgroundScheduler()
scheduler.add_job(generate_morning_brief, "cron", hour=8, minute=30)
scheduler.start()
```

**输出示例**：

```
【市场晨报 - 2026年7月17日】

一、市场概览
昨日A股三大指数涨跌互现，沪指微涨0.2%，创业板指跌0.5%。

二、持仓变动
- 600519（贵州茅台）：收盘1850.00，涨跌幅+0.8%，正常
- 000858（五粮液）：收盘162.50，涨跌幅-3.5%，⚠️超过3%阈值
- 601318（中国平安）：收盘48.20，涨跌幅+0.3%，正常

三、重要新闻
- 白酒板块承压，五粮液受渠道库存担忧影响下跌
- 保险板块受益于利率企稳预期

四、今日关注
五粮液跌幅超3%，建议关注后续走势及渠道库存数据
```

## 拓展学习

- **LangGraph**：LangChain的Agent编排框架，支持复杂的多步骤Agent工作流
- **AutoGen**：微软的多Agent框架，支持Agent间对话和协作
- **CrewAI**：角色扮演式多Agent框架，适合模拟团队协作场景
- **MCP（Model Context Protocol）**：Anthropic提出的Agent工具调用协议，标准化工具接口
- **Agent评估**：如何评估Agent的可靠性和效率，防止幻觉和错误操作

## 参考链接

- https://langchain-ai.github.io/langgraph/ - LangGraph官方文档
- https://microsoft.github.io/autogen/ - AutoGen官方文档
- https://docs.crewai.com/ - CrewAI官方文档
- https://modelcontextprotocol.io/ - MCP协议规范
- https://www.anthropic.com/research/building-effective-agents - Anthropic关于构建有效Agent的研究
