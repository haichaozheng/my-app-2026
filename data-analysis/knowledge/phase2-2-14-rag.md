# RAG构建产品知识库

> **引入时机**：W8 | **核心挑战**："如何让产品回答金融数据相关问题？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

LLM的知识有截止日期，而且不了解你产品的具体数据。当用户问"招商银行2024年财报中不良贷款率是多少"时，通用LLM要么不知道，要么编造答案。RAG（Retrieval-Augmented Generation，检索增强生成）让LLM在回答前先从你的专属知识库中检索相关信息，然后基于真实文档生成回答——既保证准确性，又具备专业性。

金融数据产品尤其需要RAG。年报、研报、行业分析、政策文件——这些文档包含大量专业信息，用户的问题往往需要基于这些文档回答。没有RAG，你的AI助手只能是通用闲聊；有了RAG，它就能变成专业的金融分析助手。

## 这个知识点的核心内容

### RAG架构

RAG的核心流程：用户提问→检索相关文档→将文档作为上下文→LLM生成回答

```
用户问题："招商银行2024年净息差是多少？"
    ↓
[检索] 从知识库中查找包含"招商银行"+"净息差"+"2024"的文档片段
    ↓
[增强] 将检索到的文档片段作为上下文拼入Prompt
    ↓
[生成] LLM基于上下文生成回答："根据2024年半年报，招商银行净息差为2.01%"
```

RAG vs 纯LLM：
- 纯LLM：依赖训练数据，可能过时或编造
- RAG：基于你的文档，答案有出处、可溯源

### 文档处理

将原始文档转化为可检索的文本片段：

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def clean_financial_text(text):
    # 去除PDF提取的乱码
    text = re.sub(r'\s+', ' ', text)
    # 保留财务数字格式
    text = re.sub(r'(\d),(\d)', r'\1\2', text)  # 去千分位
    # 去除页眉页脚
    text = re.sub(r'第\d+页共\d+页', '', text)
    return text.strip()

# 文档切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # 每个片段约500字符
    chunk_overlap=50,     # 片段间重叠50字符，避免截断
    separators=["\n\n", "\n", "。", "；", "，", " "],
    length_function=len
)

chunks = text_splitter.split_text(clean_text)

# 金融文档的特殊处理：按章节切分比固定长度更好
def split_by_sections(text, section_headers):
    sections = []
    for i, header in enumerate(section_headers):
        start = text.find(header)
        if i + 1 < len(section_headers):
            end = text.find(section_headers[i + 1])
        else:
            end = len(text)
        if start != -1:
            sections.append(text[start:end].strip())
    return sections
```

金融文档切分策略：
- **年报**：按章节切分（管理层讨论、财务报表、附注）
- **研报**：按段落+核心观点切分
- **新闻**：按整篇切分（通常较短）
- 切分粒度：太粗→检索不精确，太细→丢失上下文

### 向量存储与Embedding

将文本片段转化为向量并存储，支持语义检索：

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 生成Embedding
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key="your-key"
)

# 也可以用国内免费方案
from langchain.embeddings import HuggingFaceEmbeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese"
)

# 存入向量数据库
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embedding_model,
    metadatas=[{"source": "招商银行2024年报", "section": "管理层讨论"} for _ in chunks],
    persist_directory="./chroma_db"
)

# 检索
results = vectorstore.similarity_search(
    "招商银行净息差",
    k=3  # 返回最相关的3个片段
)
for doc in results:
    print(f"[{doc.metadata['source']}] {doc.page_content[:100]}")
```

向量数据库选择：
- **Chroma**：轻量，适合原型，本地运行
- **FAISS**：Meta开源，速度快，纯本地
- **Pinecone/Weaviate**：云服务，适合生产

### Embedding模型选择

| 模型 | 维度 | 中文能力 | 成本 |
|------|------|----------|------|
| text-embedding-3-small | 1536 | 好 | $0.02/1M tokens |
| text-embedding-3-large | 3072 | 很好 | $0.13/1M tokens |
| bge-large-zh | 1024 | 很好 | 免费（本地） |
| text2vec-base-chinese | 768 | 好 | 免费（本地） |

原型阶段推荐：bge-large-zh（中文效果好、免费、本地运行）

### 完整RAG Pipeline

```python
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from openai import OpenAI

class FinanceRAG:
    def __init__(self, vectorstore, client):
        self.vectorstore = vectorstore
        self.client = client
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def query(self, question):
        # Step 1: 检索相关文档
        docs = self.retriever.invoke(question)
        context = "\n\n---\n\n".join(
            f"[来源：{d.metadata.get('source', '未知')}]\\n{d.page_content}"
            for d in docs
        )

        # Step 2: 构建增强Prompt
        prompt = f"""你是一个专业的金融分析助手。请基于以下参考文档回答用户问题。

参考文档：
{context}

用户问题：{question}

要求：
1. 只基于参考文档回答，不要编造信息
2. 如果参考文档中没有相关信息，明确说明
3. 引用信息时标注来源
4. 回答简洁，先直接回答再展开"""

        # Step 3: 调用LLM生成回答
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": [d.metadata for d in docs]
        }
```

## 关键细节与易错点

- **易错：切分粒度不当**。金融报表中"净息差1.53%"如果被切到不同片段，检索可能找不到
- **易错：只做关键词匹配不做语义检索**。用户问"银行赚钱能力"，文档写"ROE"，关键词匹配找不到
- **易错：不标注来源**。RAG回答必须标注信息出处，否则用户无法判断可信度
- **易错：检索结果太多塞满上下文**。3-5个片段足够，太多反而干扰LLM
- **易错：不做文档去重**。同一份年报可能在PDF和HTML版本都有，需要去重

## 金融数据分析示例

构建银行股RAG知识库，索引年报和行业分析：

```python
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from openai import OpenAI

# Step 1: 准备文档（模拟年报内容）
documents = [
    {
        "content": """招商银行2024年半年度报告摘要
一、总体经营情况
2024年上半年，本集团实现营业收入1,726.60亿元，同比下降3.09%；
实现归属于本行股东的净利润747.43亿元，同比下降1.73%。
二、净息差
2024年上半年净息差为2.01%，同比下降0.21个百分点。
净息差下降主要受LPR下调及存量房贷利率调整影响。
三、资产质量
不良贷款率0.94%，较上年末下降0.03个百分点；
拨备覆盖率437.68%，较上年末下降5.15个百分点。""",
        "source": "招商银行2024半年报",
        "section": "经营概况"
    },
    {
        "content": """工商银行2024年半年度报告摘要
一、经营业绩
2024年上半年，实现营业收入4,019.99亿元，同比下降6.06%；
净利润1,712.96亿元，同比下降1.92%。
二、净息差
净息差1.43%，同比下降0.21个百分点。
三、资产质量
不良贷款率1.36%，与上年末持平。
拨备覆盖率218.62%，较上年末下降4.72个百分点。""",
        "source": "工商银行2024半年报",
        "section": "经营概况"
    },
    {
        "content": """银行业2024年下半年展望
预计2024年下半年银行业净息差仍将承压，但下行幅度有望收窄。
政策面：央行可能进一步降准降息以支持实体经济。
风险面：房地产风险逐步出清，不良率有望保持稳定。
投资建议：银行板块估值处于历史低位，股息率优势明显，
建议关注零售业务占比高、净息差韧性强的银行。""",
        "source": "某券商银行业2024H2展望",
        "section": "行业分析"
    }
]

# Step 2: 切分文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, chunk_overlap=30,
    separators=["\n\n", "\n", "。", "；"]
)

all_chunks = []
all_metadatas = []
for doc in documents:
    chunks = text_splitter.split_text(doc["content"])
    all_chunks.extend(chunks)
    all_metadatas.extend([{"source": doc["source"], "section": doc["section"]}] * len(chunks))

# Step 3: 生成Embedding并存储
embedding = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
vectorstore = Chroma.from_texts(
    texts=all_chunks,
    embedding=embedding,
    metadatas=all_metadatas,
    persist_directory="./bank_rag_db"
)

# Step 4: 查询
rag = FinanceRAG(vectorstore, OpenAI(api_key="your-key", base_url="https://api.deepseek.com"))

result = rag.query("招商银行2024年净息差是多少？跟工商银行比如何？")
print("回答：", result["answer"])
print("来源：", result["sources"])
```

## 拓展学习

- LangChain RAG教程——最系统的RAG构建指南
- LlamaIndex文档——专注RAG的框架，比LangChain更聚焦
- 《Building LLM Apps》RAG章节——从架构到部署的完整RAG指南
- Chroma官方文档——轻量向量数据库使用指南
- RAG评估：RAGAS框架——评估RAG系统质量的指标体系

## 参考链接

- https://python.langchain.com/docs/tutorials/rag/ — LangChain RAG教程
- https://docs.llamaindex.ai/ — LlamaIndex官方文档
- https://www.trychroma.com/ — Chroma向量数据库
- https://docs.ragas.io/ — RAGAS：RAG评估框架
