# RAG原理与实践

> **引入时机**：W2 | **核心挑战**："如何构建一个能检索个人文献的AI知识库？向量数据库、文档切分、检索策略怎么选？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

社科博士生在文献阶段面临一个核心挑战：你读了几十篇甚至上百篇文献，但写综述时却找不到那篇关键文献的具体论点；你记得某个学者提出过某个理论，但翻遍Zotero也找不到出处；你想让AI基于你的文献库回答问题，但AI要么编造要么给出笼统的通用回答。这些问题的根源是：文献知识没有被结构化地存储和索引。

RAG（Retrieval-Augmented Generation，检索增强生成）解决的核心问题就是：让AI基于你的专属文献库回答问题，而非基于通用训练数据。当你问"有哪些研究讨论了数字经济对就业的替代效应？"，RAG系统会先从你的文献库中检索相关段落，然后让LLM基于这些真实文献生成回答——有出处、可溯源、不编造。

不理解RAG，你只能用通用LLM做文献问答，得到的是"看起来专业但无据可查"的回答；理解RAG后，你构建的个人文献知识库将成为整个AI4S工具栈的基石——文献综述、研究设计、论文写作都需要从知识库中检索信息。

## 这个知识点的核心内容

### RAG架构与流程

RAG的核心流程：用户提问→从知识库检索相关文档片段→将片段作为上下文拼入Prompt→LLM基于上下文生成回答

```
用户问题："布迪厄的文化资本理论在数字时代有哪些新发展？"
    ↓
[检索] 从文献知识库中查找包含"文化资本"+"数字"的文档片段
    ↓
[增强] 将检索到的文档片段作为上下文拼入Prompt
    ↓
[生成] LLM基于上下文生成回答："Ignatow & Robinson (2017)提出数字文化资本概念，
       认为数字素养已成为文化资本的新形态；Schimpfossl & Yablok (2014)..."
```

RAG vs 纯LLM对比：

| 维度 | 纯LLM | RAG |
|------|-------|-----|
| 知识来源 | 通用训练数据 | 你的专属文献库 |
| 准确性 | 可能编造 | 基于真实文档 |
| 可追溯性 | 无法溯源 | 可标注出处 |
| 更新性 | 训练截止日期 | 实时更新文献库 |
| 专业深度 | 通用知识 | 领域专业 |

### 文档处理（PDF/HTML文献的切分策略）

将原始文献转化为可检索的文本片段是RAG系统的第一步，也是最容易出问题的步骤。

**PDF文献提取**：

```python
import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def clean_academic_text(text):
    import re
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'第\d+页\s*共\d+页', '', text)
    text = re.sub(r'\d+\.\s*\.\s*\.\s*\d+', '', text)
    text = re.sub(r'参考文献.*?(?=$|$)', '', text, flags=re.DOTALL)
    text = text.strip()
    return text
```

**社科文献的特殊处理**：

社科文献（尤其是中文文献）有独特的结构特征，需要针对性处理：

- **中文期刊论文**：通常有"摘要""关键词""引言""文献综述""研究设计""实证分析""结论"等固定章节，按章节切分比按固定长度切分效果好得多
- **英文期刊论文**：Abstract、Introduction、Literature Review、Method、Results、Discussion，同样适合按章节切分
- **专著章节**：按章节和子标题切分
- **政策文件**：按条目/条款切分，保留完整条文

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "；", "，", " "],
    length_function=len
)

def split_academic_paper(text, paper_metadata):
    section_headers = ["摘要", "引言", "文献综述", "理论框架",
                       "研究设计", "实证分析", "讨论", "结论",
                       "Abstract", "Introduction", "Literature Review",
                       "Method", "Results", "Discussion", "Conclusion"]

    sections = {}
    for header in section_headers:
        idx = text.find(header)
        if idx != -1:
            sections[header] = text[idx:idx+2000]

    chunks = []
    for section_name, section_text in sections.items():
        section_chunks = text_splitter.split_text(section_text)
        for chunk in section_chunks:
            chunks.append({
                "text": chunk,
                "metadata": {
                    **paper_metadata,
                    "section": section_name
                }
            })
    return chunks
```

切分策略的选择原则：
- **按章节切分**（推荐）：保留章节语义完整性，检索结果更有上下文
- **按固定长度切分**（备选）：适用于没有清晰章节结构的文档
- **按段落切分**：适用于综述性文章，但可能切得过碎
- 切分粒度：太粗→检索不精确，太细→丢失上下文。社科文献建议chunk_size=500-800字符

### 向量存储与Embedding

将文本片段转化为向量（Embedding），存入向量数据库，支持语义检索：

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5"
)

texts = [chunk["text"] for chunk in chunks]
metadatas = [chunk["metadata"] for chunk in chunks]

vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embedding_model,
    metadatas=metadatas,
    persist_directory="./literature_rag_db"
)
```

**中文文献的Embedding模型选择**：

| 模型 | 维度 | 中文能力 | 大小 | 推荐场景 |
|------|------|---------|------|---------|
| BAAI/bge-large-zh-v1.5 | 1024 | 很好 | 1.2GB | 首选，中文社科文献 |
| BAAI/bge-small-zh-v1.5 | 512 | 好 | 90MB | 资源有限时的替代 |
| shibing624/text2vec-base-chinese | 768 | 好 | 400MB | 轻量方案 |
| text-embedding-3-small (OpenAI) | 1536 | 好 | API调用 | 需要最佳效果且有API预算 |
| text-embedding-3-large (OpenAI) | 3072 | 很好 | API调用 | 对检索精度要求极高 |

向量数据库选择：

| 数据库 | 特点 | 适用场景 |
|--------|------|---------|
| Chroma | 轻量、本地、易上手 | 原型开发、个人文献库 |
| FAISS | 速度快、纯本地 | 大规模文献库 |
| Qdrant | 功能丰富、支持过滤 | 需要元数据过滤 |
| Pinecone | 云服务、免运维 | 团队共享知识库 |

### 检索策略

检索策略决定了RAG系统的效果上限。社科文献检索需要在语义相似性和关键词精确性之间找到平衡。

**语义检索 vs 关键词检索**：

| 策略 | 原理 | 优势 | 劣势 | 社科场景举例 |
|------|------|------|------|------------|
| 语义检索 | Embedding向量相似度 | 理解同义词和近义表达 | 可能遗漏关键术语 | "社会流动"→找到"阶层流动"的文献 |
| 关键词检索 | BM25等文本匹配 | 精确匹配专业术语 | 无法理解同义表达 | "DID"→精确找到提到DID的文献 |
| 混合检索 | 两者加权融合 | 兼顾语义和精确性 | 实现较复杂 | 最佳方案 |

**混合检索实现**：

```python
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever
from langchain.vectorstores import Chroma

vector_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

bm25_retriever = BM25Retriever.from_texts(
    texts=texts,
    metadatas=metadatas,
    k=5
)

ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)

results = ensemble_retriever.invoke("数字经济对就业的影响")
```

**社科文献检索的特殊考量**：

- 理论概念有多重表述："社会资本"="社会网络资源"="关系资本"，需要语义检索来桥接
- 方法论术语需要精确匹配："工具变量"≠"控制变量"，关键词检索更可靠
- 中文文献的术语翻译差异："数字鸿沟"="digital divide"="数字不平等"，需要跨语言检索能力

### 完整RAG Pipeline构建

将以上组件整合为完整的社科文献RAG系统：

```python
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from openai import OpenAI

class LiteratureRAG:
    def __init__(self, persist_dir, api_key=None, base_url=None):
        self.embedding = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-zh-v1.5"
        )
        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embedding
        )
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url or "https://api.deepseek.com"
        )

    def ingest_paper(self, text, metadata):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "；"]
        )
        chunks = text_splitter.split_text(text)
        metadatas = [{**metadata, "chunk_id": i} for i in range(len(chunks))]
        self.vectorstore.add_texts(chunks, metadatas)
        self.vectorstore.persist()

    def query(self, question, return_sources=True):
        docs = self.retriever.invoke(question)
        context = "\n\n---\n\n".join(
            f"[来源：{d.metadata.get('author', '')}({d.metadata.get('year', '')}), "
            f"《{d.metadata.get('title', '')}》, {d.metadata.get('section', '')}节]\n"
            f"{d.page_content}"
            for d in docs
        )

        prompt = f"""你是一位专业的社科研究文献助手。请基于以下文献片段回答问题。

要求：
1. 只基于提供的文献片段回答，不要编造信息
2. 如果文献中没有相关信息，明确说明
3. 引用信息时标注作者和年份
4. 区分不同文献的观点差异

文献片段：
{context}

问题：{question}"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=800
        )

        result = {"answer": response.choices[0].message.content}
        if return_sources:
            result["sources"] = [
                {
                    "author": d.metadata.get("author", ""),
                    "title": d.metadata.get("title", ""),
                    "year": d.metadata.get("year", ""),
                    "section": d.metadata.get("section", ""),
                }
                for d in docs
            ]
        return result


# 使用示例
rag = LiteratureRAG(
    persist_dir="./my_literature_db",
    api_key="your-key"
)

rag.ingest_paper(
    text=extracted_text,
    metadata={
        "author": "李强",
        "title": "数字经济与社会分层",
        "year": "2023",
        "journal": "社会学研究"
    }
)

result = rag.query("数字经济如何影响社会流动？")
print(result["answer"])
for src in result["sources"]:
    print(f"  - {src['author']}({src['year']}), 《{src['title']}》")
```

## 关键细节与易错点

- **易错：切分粒度不当导致关键信息丢失**。社科文献中的核心论点往往跨越多段，如果切分过细，"数字经济通过技能偏好型技术变革加剧收入不平等"这句话可能被截断，检索时找不到完整论点
- **易错：只做语义检索忽略关键词匹配**。方法论术语（如"DID""RDD""2SLS"）用语义检索效果差，需要关键词检索保障精确性。推荐使用混合检索
- **易错：不标注来源导致"幻觉"被误信**。RAG的回答必须标注信息出自哪篇文献的哪个章节，否则用户无法判断可信度。这是"做对"的核心保障
- **易错：PDF提取质量差导致检索失败**。中文社科期刊PDF的排版复杂（双栏、图表、脚注），提取的文本常有乱码和错位。建议先用PyMuPDF提取后人工抽检几篇，确认质量
- **易错：文献库不持续更新**。RAG知识库是动态的，每读一篇新文献就应入库。如果只在初始时构建，后续新文献不会被检索到，回答会过时

## 社科科研示例

**场景**：一位经济学博士生构建个人文献知识库，研究领域为"环境规制与企业创新"。

**Step 1：批量导入文献**

```python
import os

rag = LiteratureRAG(
    persist_dir="./env_regulation_db",
    api_key="your-key"
)

pdf_dir = "./papers/"
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        text = extract_pdf_text(pdf_path)
        text = clean_academic_text(text)

        metadata = parse_filename_metadata(filename)
        rag.ingest_paper(text, metadata)
        print(f"已入库：{filename}")
```

**Step 2：文献问答**

```python
result = rag.query("波特假说在中国的实证检验有哪些主要发现？")
print(result["answer"])
```

**Step 3：文献对比**

```python
result = rag.query(
    "对于环境规制对企业创新的影响，'波特假说'和'合规成本论'各自的实证证据如何？"
)
print(result["answer"])
```

**Step 4：辅助综述写作**

```python
result = rag.query(
    "请列出文献中关于'环境规制对全要素生产率影响'的研究，"
    "按研究结论（正向/负向/不确定）分类，每类列出作者、年份和核心发现"
)
```

## 拓展学习

- LangChain RAG教程——最系统的RAG构建指南
- LlamaIndex文档——专注RAG的框架，适合构建复杂文献检索系统
- RAGAS框架——评估RAG系统质量的指标体系，帮你判断RAG效果
- Chroma官方文档——轻量向量数据库使用指南
- BGE模型文档——中文Embedding模型的最佳实践

## 参考链接

- https://python.langchain.com/docs/tutorials/rag/ — LangChain RAG教程
- https://docs.llamaindex.ai/ — LlamaIndex官方文档
- https://www.trychroma.com/ — Chroma向量数据库
- https://docs.ragas.io/ — RAGAS评估框架
- https://huggingface.co/BAAI/bge-large-zh-v1.5 — BGE中文Embedding模型
