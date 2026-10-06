# Week 03 课堂实验：Zotero MCP

> 本实验文档配合 `lab.md`（RAG 知识库）使用。`lab.md` 走本地向量库路线，本文档走 **MCP 直连 Zotero** 路线——两条路线都是"检索即用"范式的落地，选一条深入即可，有余力可对比。

## 实验目标

把 Zotero 文献库接入 OpenCode，让 AI 直接检索、阅读、标注你的文献，体会 MCP 如何把本地工具变成 AI 的"手和眼"。

## 背景概念

- **MCP（Model Context Protocol）**：AI 助手与外部工具通信的标准协议。AI 通过 MCP 调用工具（检索、读取、写入），无需你手动复制粘贴。
- **Zotero MCP**（[github.com/54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)）：把 Zotero 文献库暴露为 MCP 工具，AI 可检索文献、读 PDF 全文、提取标注、按 DOI 添加文献。
- **本地模式**（`ZOTERO_LOCAL=true`）：直接读本地 `zotero.sqlite`，离线、快、无需 API Key。

## 实验步骤

### 第1步：Zotero 准备

1. 确认 Zotero 已安装并在运行（W1 装好的）
2. 打开 **Settings → Advanced**，勾选 *Allow other applications on this computer to communicate with Zotero*
3. 确认 W2 的文献已导入（≥20 篇），W3 课堂上去重、打标签

### 第2步：安装 zotero-mcp

在项目根目录激活 `.venv`（见 `weeks/week01/python-setup.md`），然后安装：

```bash
.\.venv\Scripts\activate
python -m pip install zotero-mcp-server
```

验收：

```bash
zotero-mcp version
```

应输出 `Zotero MCP v0.13.x` 或更高。

### 第3步：配置 OpenCode 连接

在项目根目录的 `opencode.jsonc` 中添加 zotero MCP 服务器：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "zotero": {
        "type": "local",
        "command": ["zotero-mcp"],
        "environment": {
          "ZOTERO_LOCAL": "true",
          "PYTHONUTF8": "1"
        }
      }
    }
  }
}
```

> **Windows 必须加 `PYTHONUTF8: "1"`**。Windows 默认 stdout 编码是 GBK，zotero-mcp 通过 stdout 传输含中文/emoji 的文献数据时会触发 `UnicodeEncodeError` 崩溃。设 `PYTHONUTF8=1` 强制 Python 使用 UTF-8。

字段说明（参考 [OpenCode MCP 文档](https://opencode.ai/v2/docs/mcp-servers/)）：

| 字段 | 作用 |
|---|---|
| `type: "local"` | 本地 stdio 进程，OpenCode 自动启停 |
| `command` | 可执行文件 + 参数 |
| `environment` | 注入子进程的环境变量，覆盖继承值 |

### 第4步：验证连接

1. 重启 OpenCode（`opencode` 命令重开，或在 TUI 里 `/mcps`）
2. 在 OpenCode 里输入 `/mcps`，应看到 `zotero` 状态为 connected
3. 试一条简单指令：

```text
列出我 Zotero 文献库里的所有分类（collections）
```

AI 应调用 `zotero_list_libraries` 或 `zotero_get_collections`，返回你的分类列表。若报错见文末"卡住了"。

### 第5步：文献检索与阅读

用自然语言驱动 AI 检索和阅读文献，体会"检索即用"：

```text
1. 在我的 Zotero 库里搜索关键词 "digital media"，列出匹配的文献标题和作者
2. 读取其中 [某篇文献] 的摘要和全文，总结它的核心论点
3. 提取这篇文献 PDF 里的所有高亮标注
```

对应 MCP 工具链：

| 你说的话 | AI 调用的工具 |
|---|---|
| "搜索 XXX" | `zotero_search_items` |
| "读这篇的全文" | `zotero_get_item_fulltext` |
| "读第 3-5 页" | `zotero_read_pdf_pages` |
| "提取高亮标注" | `zotero_get_annotations` |
| "汇总标注" | `zotero_synthesize_annotations` |

### 第6步：用 AI 辅助文献库整理

这是 W3 plan.md 第1节"文献库整理与去重"的 AI 增强版：

```text
1. 检查我的 Zotero 库里有没有重复文献，列出疑似重复项
2. 把标签 "todo" 的文献按方法论类型分类，输出一张表
3. 把 W2 导入的文献里没打标签的全部标上 "unsorted"
```

对应工具：`zotero_find_duplicates`、`zotero_search_by_tag`、`zotero_update_item`。

#### 6.1 写入授权（做写入操作前必须先做一次）

上面的第 2、3 条（打标签、合并重复）是**写入操作**——会修改你的 Zotero 库。Zotero 的本地 API 默认只读，写入需要单独授权一次。

**为什么需要授权？** Zotero 本地 API 从设计上就是只读的，防止恶意程序乱改你的文献库。Zotero 10+ 加了本地写入端点，但要用户**显式授权**某个应用才能写——就像手机 App 请求权限一样，你点了"允许"它才能动手。

**前置条件**：Zotero 10 或更新版本。在 Zotero 里点 **Help → About Zotero** 确认版本号 ≥ 10。旧版本没有本地写入端点，只能走 Web API（需要云端 API Key，本实验不涉及）。

**操作步骤**：

1. 确保 Zotero 在运行
2. 在终端（`.venv` 激活状态）运行：

```bash
zotero-mcp authorize-local
```

3. Zotero 会弹出一个对话框，有三个按钮：

| 按钮 | 含义 | 推荐度 |
|---|---|---|
| **Always Allow** | 授权一次，永久有效，密钥存到 `~/.config/zotero-mcp/config.json` | ✅ **选这个** |
| **Allow** | 只授权这一次，关了就失效，不存盘 | 不推荐，每次都要点 |
| **Deny** | 拒绝授权 | — |

4. 点 **Always Allow**
5. 验证授权成功：

```bash
zotero-mcp authorize-local --status
```

应输出类似 `write path: local` 或 `can write: true`。

**授权信息存在哪里？** 密钥存在本地文件：

```
C:\Users\<用户名>\.config\zotero-mcp\config.json
```

这个文件只有你能读（owner-only 权限），不上云，和 Zotero 网站的 API Key 无关。

**如果授权失效了**（换了 Zotero 数据库、重装了 Zotero 等），重新跑一次 `zotero-mcp authorize-local` 即可。彻底撤销已存的密钥：

```bash
zotero-mcp authorize-local --revoke
```

或在 Zotero 里 **Settings → Advanced → Clear Write Authorizations**。

**不授权也能用**：第1步（查找重复）是只读操作，不需要授权。只有打标签、合并重复、添加文献等写入操作才需要。如果你只做检索和阅读，跳过这一节。

> 也可以让 AI 在对话里直接调用 `zotero_authorize_local_writes` 工具触发同样的弹窗——效果和命令行一样。详见 [配置文档](https://github.com/54yyyu/zotero-mcp/blob/main/docs/configuration.md#local-write-support)。

### 第7步：对比与反思

完成上述操作后，回答以下问题（写在实验记录里）：

1. **MCP vs 手动**：让 AI 直接读 Zotero，和"手动导出 PDF → 上传到 Kimi/智谱清言"相比，省了哪些步骤？哪些场景手动反而更好？
2. **MCP vs RAG**（与 `lab.md` 对比）：MCP 直连是实时检索原库，RAG 是预先嵌入再语义检索。两者在"找一篇我知道存在的文献"和"找概念相似但我不知道的文献"上各有什么优劣？
3. **写综述时用哪条路线**：你的研究方向下，哪条路线更适合综述写作？为什么？

### 第8步：向量检索（语义搜索）

前面第5步的关键词检索是"字面匹配"——换个说法就找不到。zotero-mcp 还支持**语义检索**：把文献全文嵌入成向量，按概念相似度排序，能找到"用词不同但概念相近"的文献。

#### 8.1 安装语义搜索组件

`zotero-mcp-server` 基础包不含语义检索依赖，需要额外安装 `[semantic]` extras：

```bash
.\.venv\Scripts\activate
python -m pip install "zotero-mcp-server[semantic]"
```

> `[semantic]` 是 pip 的 **extras 语法**：`pyproject.toml` 里声明了这组可选依赖包括 `chromadb`（向量数据库）、`sentence-transformers`（本地嵌入模型）等，pip 会把它们一起装进 `.venv`。

#### 8.2 选择嵌入模型

通过环境变量 `ZOTERO_EMBEDDING_MODEL` 配置，支持四种嵌入源：

| 值 | 模型 | 需要什么 | 适合场景 |
|---|---|---|---|
| `default`（不设） | 本地 `sentence-transformers` | 无需 API Key，首次自动下载模型 | **推荐入门**，离线、免费 |
| `openai` | `text-embedding-3-small` | `OPENAI_API_KEY` | 效果好，花钱，需联网 |
| `gemini` | `gemini-embedding-001` | `GEMINI_API_KEY` | 效果好，Google 免费额度 |
| `ollama` | `qwen3-embedding` 等 | 本地跑 Ollama 服务 | 完全离线，需 GPU |

**社科博士生推荐先用 `default`**（本地模型，零成本零配置），跑通后再按需换 OpenAI/Gemini。

在 `opencode.jsonc` 的 zotero 环境变量里加一行：

```jsonc
"environment": {
  "ZOTERO_LOCAL": "true",
  "PYTHONUTF8": "1",
  "ZOTERO_EMBEDDING_MODEL": "default"
}
```

> **`environment` 字段是什么意思？** OpenCode 启动 zotero-mcp 子进程时注入的环境变量，相当于启动前在终端敲 `set ZOTERO_EMBEDDING_MODEL=default`，只不过 OpenCode 自动做。三个变量的含义：
>
> | 变量 | 作用 |
> |---|---|
> | `ZOTERO_LOCAL=true` | 走本地模式，读本机 `zotero.sqlite` 和 Zotero 本地 API，不连云端 |
> | `PYTHONUTF8=1` | 强制 Python 用 UTF-8 编码（Windows 默认 GBK 会崩，见第3步说明） |
> | `ZOTERO_EMBEDDING_MODEL=default` | 语义检索用本地嵌入模型，不调外部 API |

#### 8.3 模型权重是谁下载的？

这里要区分两个层面：

- **Python 包**（`sentence-transformers` 代码）→ **pip** 从 PyPI 装，就是上面那行 `[semantic]` 命令
- **模型权重**（几百 MB 的神经网络参数）→ **`sentence-transformers` 库首次运行时自动下载**，不是 pip 装的

流程是：你跑 `zotero-mcp update-db` → zotero-mcp 调 `sentence-transformers` → 库发现本地没权重 → 从 **Hugging Face Hub**（`huggingface.co`）下载默认模型 → 缓存到本地：

```
C:\Users\<用户名>\.cache\huggingface\
```

之后不再重复下载。

#### 8.4 国内网络：设 Hugging Face 镜像

huggingface.co 国内访问慢或不通，**强烈建议提前设镜像**。在 `opencode.jsonc` 里加：

```jsonc
"environment": {
  "ZOTERO_LOCAL": "true",
  "PYTHONUTF8": "1",
  "ZOTERO_EMBEDDING_MODEL": "default",
  "HF_ENDPOINT": "https://hf-mirror.com"
}
```

`HF_ENDPOINT` 是 Hugging Face 官方支持的环境变量，指向国内镜像 `hf-mirror.com`，模型下载速度快很多。

#### 8.5 构建向量索引

安装好后，在终端运行一次索引构建（把文献全文切块、嵌入、存入 ChromaDB）：

```bash
zotero-mcp update-db --fulltext
```

| 参数 | 作用 |
|---|---|
| `--fulltext` | 提取 PDF 全文进行嵌入（不加则只索引元数据，语义检索效果差） |
| `--force-rebuild` | 强制完整重建（用于索引出问题时） |

- 你有 503 篇文献，首次构建可能需要几分钟到十几分钟（取决于本地模型速度）
- 之后每次 Zotero 有新文献，再跑一次 `zotero-mcp update-db` 增量更新即可
- 查看索引状态：`zotero-mcp db-status`

#### 8.6 用自然语言做语义检索

索引建好后重启 OpenCode，直接用自然语言问：

```text
我的文献库里哪些论文讨论了"集体决策中的信息聚合"？
```

AI 会调用 `zotero_semantic_search` 工具，按语义相似度返回文献——不需要标题或关键词精确匹配，只要概念相近就能找到。

#### 8.7 关键词检索 vs 语义检索

| | 关键词检索（`zotero_search_items`） | 语义检索（`zotero_semantic_search`） |
|---|---|---|
| 原理 | 标题/标签/全文里找字面匹配 | 文献全文嵌入成向量，按语义相似度排序 |
| 优势 | 精确，知道关键词时最快 | 能找到"概念相近但用词不同"的文献 |
| 劣势 | 换个说法就找不到 | 依赖嵌入模型质量，需先建索引 |
| 典型场景 | "找 Attention Is All You Need 这篇" | "找讨论协商民主与数字媒体交叉的文献" |

#### 8.8 与 lab.md 本地 RAG 的关系

这其实就是 `lab.md` RAG 路线的**自动化版本**——zotero-mcp 把"切分→嵌入→存向量库→检索"整套 pipeline 封装好了，不用自己写 LangChain + FAISS 代码：

| | lab.md（手写 RAG） | zotero-mcp 语义检索 |
|---|---|---|
| 嵌入 | 智谱 embedding API | 本地/OpenAI/Gemini |
| 向量库 | FAISS | ChromaDB |
| 文献来源 | 手动放 PDF | 直连 Zotero 库 |
| 维护 | 自己写代码 | `zotero-mcp update-db` 一条命令 |
| 可控性 | 高（可调 chunk size 等） | 低（封装好） |

## 实验交付

- `opencode.jsonc` 配置（含 zotero MCP 段）
- 3 条以上自然语言 → AI 调用 zotero 工具的交互截图
- 第7步反思记录（3 个问题各 2-3 句）
- **选做（第8步）**：语义检索索引构建截图 + 一次语义检索的交互截图

## 卡住了

- **`/mcps` 显示 zotero 未连接 / fail**
  - 确认 Zotero 在运行：任务管理器看 `zotero.exe` 进程
  - 确认本地 API 开了：浏览器访问 `http://localhost:23119/api/users/0/items?limit=1`，应返回 JSON
  - 确认 `zotero-mcp` 装在 `.venv` 里：`zotero-mcp version` 能跑
  - **Windows 崩溃 / 无输出**：检查 `opencode.jsonc` 里有没有 `"PYTHONUTF8": "1"`（不加必崩）
- **能连接但工具调用报错**
  - 看报错信息里的 `UnicodeEncodeError` → 确认 `PYTHONUTF8` 环境变量
  - 写入被拒（`write capabilities: none`）→ 运行 `zotero-mcp authorize-local` 授权，弹窗选 **Always Allow**（详见第6.1节）
  - 授权了但仍写入失败 → 确认 Zotero 版本 ≥ 10（旧版本不支持本地写入）；或重跑 `zotero-mcp authorize-local --revoke` 后重新授权
  - 找不到文献 → 确认 Zotero 里确实有文献，且不是空库
- **装不上 zotero-mcp-server**
  - 确认在 `.venv` 激活状态：终端前缀有 `(.venv)`
  - 网络问题换热点；pip 太慢加 `-i https://pypi.tuna.tsinghua.edu.cn/simple`
- **语义检索不可用 / `Semantic search is not available`**
  - 没装 `[semantic]` 组件：`python -m pip install "zotero-mcp-server[semantic]"`
  - `update-db` 卡住或超时：huggingface.co 国内不通 → 在 `opencode.jsonc` 加 `"HF_ENDPOINT": "https://hf-mirror.com"`
  - 磁盘空间不够：模型 + 503 篇文献向量索引需几个 GB，确认空间充足
  - 首次很慢正常：要下载模型 + 跑全文嵌入，后续增量更新很快
- 卡住 → 问 AI（附报错）→ 同学互助解答 → 举手教师

## 参考资料

- Zotero MCP 项目：[github.com/54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)
- Zotero MCP 工具列表：[docs/tools.md](https://github.com/54yyyu/zotero-mcp/blob/main/docs/tools.md)
- Zotero MCP 配置：[docs/configuration.md](https://github.com/54yyyu/zotero-mcp/blob/main/docs/configuration.md)
- OpenCode MCP 配置：[opencode.ai/v2/docs/mcp-servers](https://opencode.ai/v2/docs/mcp-servers/)
- 本项目 `opencode.jsonc`：仓库根目录
- Python 环境约定：`AGENTS.md` → "本地 Python 环境"一节
