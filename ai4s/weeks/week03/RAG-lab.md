# Week 03 课堂实验：手写最小 RAG

> 本实验配合 `lecture.md` 第2节"综述写作规范与RAG介绍"。`zotero-lab.md` 走 MCP 直连路线（AI 帮你检索 Zotero），本实验走 **手写 RAG** 路线——自己搭一遍切分→嵌入→存库→检索，理解 RAG 的每一步。两条路线对比见 `zotero-lab.md` 第8.8节。

## 实验目标

用 30 行代码搭一个能用的语义检索 demo，理解 RAG 的"检索"部分是怎么工作的。

## 背景概念

RAG = Retrieval-Augmented Generation，三步：

```
你的问题 → [检索] 从文献库找相关片段 → [增强] 把片段塞进 Prompt → [生成] LLM 基于片段回答
```

本实验只做**检索**这一步（切分→嵌入→存库→检索），生成部分留给 LLM。因为检索是 RAG 的核心瓶颈——检索不到，再强的 LLM 也编不出靠谱答案。

## 关于 sentence-transformers 模型共享

> **不同应用下载的 sentence-transformers 模型能通用吗？** 能。所有用 `sentence-transformers` 或 `transformers` 的程序共享同一个缓存目录：
>
> ```
> C:\Users\<用户名>\.cache\huggingface\hub\
> ```
>
> zotero-mcp 下载的模型，本实验的脚本直接复用，零额外下载。反过来也一样——你先跑本实验下载了模型，zotero-mcp 也能用。首次下载慢，之后所有应用都快。

## 实验步骤

### 第1步：安装依赖

在项目根目录激活 `.venv`：

```bash
.\.venv\Scripts\activate
python -m pip install chromadb sentence-transformers
```

就这两个包。`chromadb` 是向量数据库，`sentence-transformers` 是嵌入模型库。不需要 LangChain、不需要 FAISS、不需要 API Key。

> 如果你已经装了 `zotero-mcp-server[semantic]`（见 `zotero-lab.md` 第8步），这两个包已经包含了，不用重复装。

### 第2步：准备示例文本

不需要真实 PDF，先用几段示例文本跑通流程。新建 `rag_demo.py`：

```python
# rag_demo.py — 最小 RAG 检索 demo

documents = [
    {
        "text": "布迪厄将文化资本分为三种形态：身体化的文化资本（如教养、品味）、客体化的文化资本（如艺术品、书籍）、制度化的文化资本（如学历证书）。文化资本通过家庭教育传递，是阶层再生产的重要机制。",
        "metadata": {"author": "布迪厄", "title": "文化资本与社会再生产", "year": "1986"},
    },
    {
        "text": "数字鸿沟不仅指接入差距，更包括使用技能、信息素养和内容创造能力的差异。老年人、低收入群体和农村居民在数字技能方面显著落后，这加剧了既有的社会不平等。",
        "metadata": {"author": "van Dijk", "title": "数字鸿沟的深层结构", "year": "2020"},
    },
    {
        "text": "社会资本理论认为，个人的社会网络中蕴含的资源可以转化为经济收益和职业机会。弱关系（ acquaintances）比强关系（亲密朋友）更能提供非重复性信息，因此在求职中更有价值。",
        "metadata": {"author": "Granovetter", "title": "弱关系的力量", "year": "1973"},
    },
    {
        "text": "平台经济通过算法管理重新定义了劳动关系。外卖骑手虽然名义上是独立承包人，但平台通过派单算法、评分系统和时间监控实施着比传统雇主更精细的控制。",
        "metadata": {"author": "陈龙", "title": "算法控制与劳动异化", "year": "2023"},
    },
    {
        "text": "数字素养已成为新型文化资本。掌握数字工具的能力不仅影响就业前景，还塑造了个人在公共领域的表达能力和参与能力，形成新的社会区隔。",
        "metadata": {"author": "Ignatow", "title": "数字时代的文化资本", "year": "2017"},
    },
]
```

这是 5 段社科文献的摘要片段，覆盖了文化资本、数字鸿沟、社会资本、平台经济等主题。

### 第3步：嵌入并存入 ChromaDB

接着在 `rag_demo.py` 里加：

```python
import chromadb
from sentence_transformers import SentenceTransformer

# 1. 加载嵌入模型（首次运行自动下载，约 90MB，缓存到 ~/.cache/huggingface/）
print("加载嵌入模型...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 2. 连接 ChromaDB（本地文件存储，存在 ./rag_chroma_db/ 目录）
client = chromadb.PersistentClient(path="./rag_chroma_db")
collection = client.get_or_create_collection(name="literature")

# 3. 把文档嵌入并存入向量库
print("嵌入并存储文档...")
for i, doc in enumerate(documents):
    collection.add(
        ids=[f"doc_{i}"],
        documents=[doc["text"]],
        metadatas=[doc["metadata"]],
        embeddings=[embedder.encode(doc["text"]).tolist()],
    )

print(f"已存入 {collection.count()} 篇文档到 ChromaDB")
```

跑一下：

```bash
python rag_demo.py
```

首次运行会下载 `all-MiniLM-L6-v2` 模型（约 90MB），之后从缓存读。你应该看到 `已存入 5 篇文档到 ChromaDB`。

**发生了什么？**

```
文档文本 ──embedder.encode()──→ 384维向量 ──collection.add()──→ ChromaDB（本地磁盘）
```

ChromaDB 把向量、原文、元数据一起存在 `./rag_chroma_db/` 目录里，重启程序不丢失。

### 第4步：语义检索

接着加检索代码：

```python
# 4. 语义检索
query = "数字技术加剧了什么样的不平等？"
print(f"\n问题：{query}")

# 把问题也嵌入成向量，和文档向量算相似度
query_embedding = embedder.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,  # 返回最相似的 3 段
)

# 打印结果
print("\n检索结果（按相似度排序）：")
for i, (doc, meta, dist) in enumerate(zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
)):
    print(f"\n[{i+1}] 相似度距离: {dist:.4f}")
    print(f"    来源：{meta['author']}({meta['year']}), 《{meta['title']}》")
    print(f"    内容：{doc[:80]}...")
```

跑一下，你应该看到排名靠前的是 van Dijk 的"数字鸿沟"和 Ignatow 的"数字时代的文化资本"——**即使你的问题里没有"鸿沟""素养"这些词**，模型理解了"数字技术加剧不平等"和"数字鸿沟""数字素养"是语义相近的。

这就是语义检索和关键词检索的核心区别。

### 第5步：对比关键词检索

在脚本末尾加一段关键词检索对比：

```python
# 5. 对比：ChromaDB 的关键词检索（where_document）
print(f"\n--- 关键词检索对比 ---")
kw_results = collection.query(
    query_texts=["文化资本"],  # 用文本而非向量
    n_results=3,
)
print("搜索 '文化资本' 的结果：")
for doc, meta in zip(kw_results["documents"][0], kw_results["metadatas"][0]):
    print(f"  - {meta['author']}({meta['year']}): {doc[:60]}...")
```

你会发现关键词检索只能精确匹配"文化资本"这几个字，而语义检索能找到"数字素养"这种概念相近但用词不同的文献。

### 第6步：观察与记录

跑完 demo 后回答以下问题（写在实验记录里）：

1. **语义检索 vs 关键词检索**：用你自己的话说明，为什么"数字技术加剧不平等"这个问题，语义检索能找到"数字鸿沟"的文献，而关键词检索找不到？
2. **向量是什么**：`embedder.encode("一段文本")` 返回的是一个 384 维的浮点数列表。你觉得这 384 个数字代表了什么？
3. **换模型**：把 `all-MiniLM-L6-v2` 换成 `BAAI/bge-small-zh-v1.5`（中文优化模型），检索结果有变化吗？为什么？（提示：MiniLM 是多语言通用模型，bge-small-zh 专注中文）

## 完整代码

把上面的片段拼起来就是完整的 `rag_demo.py`（约 50 行）。也可以让 OpenCode 帮你生成：

```text
在当前目录写一个 rag_demo.py，用 chromadb 和 sentence-transformers 做最小 RAG 检索 demo。
要求：
1. 内置 5 段社科文献摘要文本（含 author/title/year 元数据）
2. 用 all-MiniLM-L6-v2 嵌入，存入本地 ChromaDB（PersistentClient，路径 ./rag_chroma_db）
3. 支持语义检索：输入问题 → 嵌入 → 查询向量库 → 返回 top3 结果（含相似度距离）
4. 附带关键词检索对比（query_texts 方式）
5. Windows 终端能跑：python rag_demo.py
```

## 实验交付

- `rag_demo.py`（代码 + 运行截图）
- `./rag_chroma_db/` 目录（向量库，本地生成）
- 第6步观察记录（3 个问题各 2-3 句）

## 卡住了

- **模型下载慢 / 超时**
  - huggingface.co 国内不通 → 设环境变量：`set HF_ENDPOINT=https://hf-mirror.com` 后再跑
  - 或在代码里加：`export HF_ENDPOINT="https://hf-mirror.com"`（Linux/Mac）
- **`chromadb` 装不上**
  - 确认在 `.venv` 激活状态
  - 网络问题加镜像：`pip install chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple`
- **`SentenceTransformer` 报错 `OSError: Model not found`**
  - 首次下载需要网络，确认能访问 huggingface.co 或已设镜像
- **检索结果不对 / 全是距离很大的**
  - 检查 `embedder.encode()` 是否对 query 和 document 用了同一个模型
  - `all-MiniLM-L6-v2` 对中文支持一般，换 `BAAI/bge-small-zh-v1.5` 试试
- 卡住 → 问 AI（附报错）→ 同学互助解答 → 举手教师

## 进阶（可选）

跑通 demo 后，可以往真实方向扩展：

1. **换成真实文献**：用 PyMuPDF 从 Zotero 导出的 PDF 提取文本，替换示例文本
2. **加入切分**：一篇论文太长，用 `RecursiveCharacterTextSplitter` 或自己按段落切分后再嵌入
3. **接入 LLM 生成**：把检索到的片段拼进 Prompt，调 LLM API 生成回答——这就完成了 RAG 的"G"部分
4. **对比 zotero-mcp 语义检索**：把同样的 5 段文本导入 Zotero，用 `zotero_semantic_search` 检索，对比结果

进阶路线详见 `knowledge/m1-5-rag.md`（完整 LangChain + Chroma Pipeline）。

## 参考资料

- ChromaDB 文档：[trychroma.com](https://www.trychroma.com/)
- sentence-transformers 文档：[sbert.net](https://www.sbert.net/)
- Hugging Face 镜像：[hf-mirror.com](https://hf-mirror.com/)
- RAG 原理详解：`knowledge/m1-5-rag.md`
- MCP 直连路线：`weeks/week03/zotero-lab.md`
- Python 环境约定：`AGENTS.md` → "本地 Python 环境"一节
