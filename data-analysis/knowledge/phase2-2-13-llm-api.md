# LangChain基础 + LLM API集成

> **引入时机**：W8 | **核心挑战**："如何用框架化的方式调用LLM、构建产品AI功能？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

现代数据产品不再只是"展示数据"，更需要"解读数据"。用户看到银行股暴跌5%，第一反应不是去看K线图，而是想知道"为什么跌了？"。LLM API让你的产品具备数据解读和自然语言交互能力——从"展示工具"进化为"分析助手"。不集成LLM API，你的产品永远只是个图表工具，无法满足用户更深层的分析需求。

在金融数据产品中集成LLM API并非简单的"调用API返回结果"。你需要设计合适的Prompt让LLM理解金融上下文、处理流式输出提升用户体验、控制Token消耗避免成本失控、处理API异常保证产品稳定。这些实战技能是做出可用AI数据产品的关键。

## 这个知识点的核心内容

### LLM API概览

| 提供商 | 模型 | 特点 | 定价 |
|--------|------|------|------|
| OpenAI | GPT-4o | 能力最强，生态最成熟 | $2.5-10/1M tokens |
| Anthropic | Claude 3.5 | 长上下文，推理强 | $3-15/1M tokens |
| 国内 | DeepSeek/通义 | 国内合规，延迟低 | ¥1-4/1M tokens |
| 开源 | Qwen/GLM | 可自部署，无审查 | 部署成本 |

选择建议：
- 原型阶段：用最方便的API（国内用DeepSeek，国际用OpenAI）
- 生产阶段：考虑合规和成本，国内产品优先国内API
- 教学演示：用DeepSeek（便宜且中文能力强）

### API调用基础

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"  # DeepSeek兼容OpenAI格式
)

# 基础调用
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个A股银行板块分析专家。"},
        {"role": "user", "content": "今天工商银行为什么下跌？"}
    ],
    temperature=0.3
)

answer = response.choices[0].message.content
print(answer)

# Token用量
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
```

### 产品中的Prompt设计

产品级Prompt与闲聊Prompt完全不同，需要结构化、可预测、可控：

```python
SYSTEM_PROMPT = """你是一个专业的A股银行板块分析助手。

你的职责：
1. 基于提供的数据和上下文回答用户关于银行股的问题
2. 给出客观、数据驱动的分析，不做投资建议
3. 如果数据不足以回答，明确说明而非编造

回答格式要求：
- 先给出直接回答（1-2句）
- 再提供数据支撑（引用具体数字）
- 最后给出相关延伸信息

注意：
- 中国A股市场：涨跌停限制±10%，T+1交易
- 中国市场惯例：红色表示上涨，绿色表示下跌
- 始终区分"相关性"和"因果关系"
"""

def build_context_message(stock_data, question):
    context = f"""
当前股票数据：
- 股票：{stock_data['name']}（{stock_data['code']}）
- 最新收盘价：{stock_data['close']:.2f}
- 日涨跌幅：{stock_data['change_pct']:.2f}%
- PE(TTM)：{stock_data['pe']}
- PB：{stock_data['pb']}
- 近5日涨跌幅：{stock_data['week_change']:.2f}%
- 近20日涨跌幅：{stock_data['month_change']:.2f}%
- 近20日波动率（年化）：{stock_data['volatility']:.2f}%
- 今日成交量：{stock_data['volume']:,.0f}
- 成交量较20日均值：{stock_data['volume_ratio']:.2f}倍

近期重要事件：
{stock_data['events']}

用户问题：{question}
"""
    return context
```

### 流式输出

流式输出让用户无需等待完整响应，大幅提升体验：

```python
# Streamlit中的流式输出
import streamlit as st

def stream_response(client, messages):
    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.3,
        stream=True
    )
    response = st.write_stream(
        (chunk.choices[0].delta.content or "" for chunk in stream)
    )
    return response

# 在Streamlit Chat组件中使用
if prompt := st.chat_input("输入你的问题"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_context_message(stock_data, prompt)}
        ]
        response = stream_response(client, messages)
```

### 成本管理

LLM API按Token计费，不做管理可能产生意外账单：

```python
# Token预估
def estimate_tokens(text):
    """粗略估算：1个中文字≈2 tokens，1个英文单词≈1.3 tokens"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - chinese_chars
    return chinese_chars * 2 + other_chars * 0.5

# 成本控制策略
MAX_INPUT_TOKENS = 2000  # 限制输入长度
MAX_OUTPUT_TOKENS = 500  # 限制输出长度
COST_PER_SESSION = 0.01  # 单次调用成本上限

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    max_tokens=MAX_OUTPUT_TOKENS,
    temperature=0.3
)

# 记录用量
session_cost = (
    response.usage.prompt_tokens * 0.001 +  # input价格
    response.usage.completion_tokens * 0.002  # output价格
) / 1000  # 转换为美元
```

成本优化策略：
- 使用更短的模型名（如gpt-4o-mini代替gpt-4o）
- 缓存重复查询的响应
- 压缩上下文：只传关键数据而非全部历史
- 设置max_tokens避免输出过长

### 错误处理与降级

API调用必然失败，必须设计降级方案：

```python
import time
from openai import APIError, RateLimitError, APITimeoutError

def call_llm_with_retry(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.3,
                timeout=30
            )
            return response.choices[0].message.content

        except RateLimitError:
            wait_time = 2 ** attempt
            st.warning(f"API限流，{wait_time}秒后重试...")
            time.sleep(wait_time)

        except APITimeoutError:
            st.warning("API超时，正在重试...")

        except APIError as e:
            st.error(f"API错误：{e}")
            return "抱歉，AI分析服务暂时不可用，请稍后再试。"

    return "AI分析服务多次请求失败，请检查网络或稍后重试。"
```

### LangChain Chain + Prompt Template

直接调用 OpenAI API 需要手动管理 messages 拼接、重试逻辑、输出解析。LangChain 用 Chain 和 Prompt Template 将这些流程模板化，让代码更简洁、可维护。

**安装**：

```bash
pip install langchain langchain-openai langchain-core
```

**Prompt Template**：将 Prompt 模板化，参数可替换，避免字符串拼接：

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的A股{domain}分析助手。基于提供的数据回答用户问题。回答要求：客观、数据驱动、不做投资建议。"),
    ("user", "{question}\n\n数据上下文：\n{context}")
])

# 渲染
msgs = prompt.invoke({
    "domain": "银行板块",
    "question": "今天银行股为什么下跌？",
    "context": "工商银行收盘价5.42，涨跌幅-1.5%，PE 5.2"
})
print(msgs.messages[0].content)
```

**LLM Chain**：Prompt + LLM 串联为一条调用链，一行代码完成完整的 LLM 调用：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="your-api-key",
    base_url="https://api.deepseek.com",
    temperature=0.3,
    max_tokens=500
)

# 组装 Chain：Prompt → LLM
chain = prompt | llm
response = chain.invoke({
    "domain": "银行板块",
    "question": "今天银行股为什么下跌？",
    "context": "工商银行收盘价5.42，涨跌幅-1.5%，PE 5.2"
})
print(response.content)
```

**Chain 输出解析**：Chain 返回的是 LLM 原始对象，用 `StrOutputParser` 直接拿字符串：

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({...})
print(result)  # 直接是字符串，不需要 result.choices[0].message.content
```

**在 Streamlit 中集成**：

```python
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

client = ChatOpenAI(
    model="deepseek-chat",
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
    temperature=0.3, max_tokens=500
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的A股银行板块分析助手。基于提供的数据回答用户问题。"),
    ("user", "{question}\n\n数据上下文：\n{context}")
])

chain = prompt | client | StrOutputParser()

if prompt_input := st.chat_input("输入关于银行股的问题..."):
    with st.chat_message("assistant"):
        result = chain.invoke({
            "question": prompt_input,
            "context": f"工商银行：5.42元，-1.5%，PE 5.2，PB 0.61"
        })
        st.write(result)
```

**为什么用 LangChain 而不是直接调 API**：
- 模板化：Prompt 可复用、可测试，不用每次手动拼 messages
- 链式组合：Prompt → LLM → 解析 → 后处理，像水管一样串联
- 为 W9 RAG 打基础：RAG 只需在 Chain 前加一步检索（Retriever），无需重写 LLM 调用逻辑

## 关键细节与易错点

- **易错：将API Key硬编码在代码中**。必须使用环境变量或Streamlit secrets
- **易错：将大量原始数据作为Prompt**。应只传统计摘要和关键指标，控制Token消耗
- **易错：不设置max_tokens**。LLM可能生成冗长的回复，浪费Token且用户不愿读
- **易错：System Prompt太随意**。产品级System Prompt需要明确角色、输出格式和限制
- **易错：不做错误处理**。API调用在网络差时会失败，必须有降级方案

## 金融数据分析示例

在银行股仪表板中集成AI问答功能：

```python
import streamlit as st
from openai import OpenAI

# API配置（从secrets读取）
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """你是一个专业的A股银行板块分析助手。
基于提供的股票数据回答用户问题。
回答要求：客观、数据驱动、不做投资建议。
先直接回答，再提供数据支撑。"""

# 在Streamlit中构建AI分析标签页
with st.tab("🤖 AI分析"):
    st.subheader("AI智能问答")

    # 构建上下文
    context = f"""
当前数据：{name}（{selected}）
收盘价：{latest['收盘']:.2f}，涨跌幅：{change_pct:+.2f}%
PE：{latest.get('PE', 'N/A')}，PB：{latest.get('PB', 'N/A')}
近5日涨跌：{week_change:+.2f}%，近20日涨跌：{month_change:+.2f}%
"""

    # 快捷问题
    quick_questions = [
        "为什么今天银行股下跌？",
        "这只股票目前的估值水平如何？",
        "近期的波动率是否异常？",
        "与同业相比表现如何？"
    ]

    for q in quick_questions:
        if st.button(q, key=q):
            st.chat_message("user").write(q)
            with st.chat_message("assistant"):
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"{context}\n\n用户问题：{q}"}
                ]
                stream = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=500,
                    stream=True
                )
                response = st.write_stream(
                    chunk.choices[0].delta.content or ""
                    for chunk in stream
                )

    # 自由输入
    if prompt := st.chat_input("输入关于银行股的问题..."):
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{context}\n\n用户问题：{prompt}"}
            ]
            try:
                stream = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=500,
                    stream=True
                )
                response = st.write_stream(
                    chunk.choices[0].delta.content or ""
                    for chunk in stream
                )
            except Exception as e:
                st.error(f"AI服务暂时不可用：{e}")
```

## 拓展学习

- OpenAI API官方文档——最权威的API参考
- DeepSeek API文档——国内高性价比替代方案
- Prompt Engineering Guide——系统化Prompt设计方法
- 《Building LLM Apps》——构建LLM应用的实战指南
- LangChain文档——LLM应用开发框架

## 参考链接

- https://platform.openai.com/docs/api-reference — OpenAI API官方参考
- https://platform.deepseek.com/api-docs/ — DeepSeek API文档
- https://www.promptingguide.ai/ — Prompt Engineering Guide
- https://python.langchain.com/docs/ — LangChain Python文档
