---
name: search-paper
description: >-
  按检索词从 arXiv、CrossRef、Semantic Scholar、OpenAlex 拉取文献元数据并输出去重合并列表。
  Use when the user asks to search papers, 查文献, 文献检索, 检索式, PRISMA 初筛,
  或从 arXiv/CrossRef/Semantic Scholar/OpenAlex 搜论文。不导入数据库、不写 Zotero。
---

# Search Paper

输入检索词，输出带元数据的文献列表。人定纳入排除标准；本 skill 只检索与去重，初筛分类可由模型做，但不替用户决定取舍。

## 边界

- 做：公开库检索、多检索词扇出、跨源去重合并、按年份/来源过滤、输出表
- 不做：导入 Literature DB、上传 PDF、写 Zotero。用户要导入时改用 `literature-import`

## 前置

- 已安装 `httpx`（`python -m pip install httpx`）
- Semantic Scholar：仓库根目录 `.env` 写入 `S2_API_KEY=...`。**没有 Key 也能用**：脚本会自动限速（同源查询间隔）、延迟重试，仍失败时记入 `degraded`（信息级，不影响其他源与结果完整性——S2 与 OpenAlex 覆盖大量重叠）。但匿名额度很低，免费申请更稳：https://www.semanticscholar.org/product/api#api-key-form 。申请后把 Key 放进 `.env`，不要提交到 git。课堂演示前先配好 Key。`--limit` 保持 20 即可，不要一次拉满 100。
- 可选：`.env` 写入 `CONTACT_EMAIL=...`，让 CrossRef / OpenAlex 请求进入礼貌池（更稳定）。

## 检索式写法（影响准确性）

- 检索词用**英文**；中文主题先翻译成领域术语。
- 短语加英文双引号做精确匹配：`"large language model"`。
- 支持布尔：`AND`、`OR`、`ANDNOT`（arXiv 语法，全大写）。
- **覆盖关键**：缩写与全称是两套词，各查一遍。`--query` 可重复传入 2–3 个变体，脚本会对每个源×每个变体都检索再合并，如：

```text
python .opencode/skills/search-paper/scripts/search.py \
  --query "LLM agent" \
  --query "large language model agent" \
  --limit 20 --from-year 2023
```

## 默认命令

在仓库根目录执行：

```text
python .opencode/skills/search-paper/scripts/search.py --query "YOUR QUERY" --limit 20
```

常用参数：

| 参数 | 含义 |
|---|---|
| `--query` | 检索词或简单布尔式（必填，**可重复**传入变体提高覆盖） |
| `--limit` | 每个来源每次查询最多条数，默认 20 |
| `--from-year` | 起始年份，含该年（arXiv 为服务端过滤，其余源同样在 API 层过滤） |
| `--sources` | `arxiv,crossref,s2,openalex`（默认四者都查） |

## 工作流程

1. 向用户确认检索词、年份下限、每个源的条数；未指定则用默认。
2. **先构造检索式再跑脚本**：把主题译成英文术语；给出 2–3 个 `--query` 变体（缩写 + 全称 + 可能的同义说法）；核心概念用引号短语；需要排除时用 `ANDNOT`。不要现场重写 HTTP 调用。
3. 运行 `search.py`。脚本会对每个源 × 每个检索词检索，然后跨源去重合并：按 DOI → arXiv ID（忽略版本号）→ 规范化题名（近邻 ≥0.95 且年份兼容）合并，合并时互补填充字段（摘要、PDF 链接等），并记录 `matched_sources` 与 `best_rank`。
4. 排序按各源相关性排名（`best_rank`）优先，同年份新者靠前，不再单纯按年份排。
5. 把结果整理成 Markdown 表，列：题名、作者、年份、venue、DOI、来源（`matched_sources`）、开放获取、摘要前 200 字。
6. 若用户给了纳入排除标准（年份、方法、语言等），只在表上标注「拟纳入 / 拟排除 / 待定」并写一句理由。标准由人确认后再筛。
7. 不要编造 API 未返回的条目。某个源失败时（errors 字段）说明失败源，仍展示其余来源。S2 匿名 429 会进入 `degraded` 字段（非错误）：向用户说明该源被限流、结果完整性基本不受损（OpenAlex 兜底），并提示可免费申请 Key 或稍后重试。

## 脚本

| 脚本 | 作用 |
|---|---|
| `scripts/search.py` | 统一入口：多检索词扇出、去重合并、排序 |
| `scripts/arxiv_client.py` | arXiv 检索（字段化布尔查询 + 服务端年份过滤 + 重试） |
| `scripts/crossref_client.py` | CrossRef 检索（`query.bibliographic` 精确字段 + 礼貌池 + 重试） |
| `scripts/s2_client.py` | Semantic Scholar 检索（API Key + 429 退避） |
| `scripts/openalex_client.py` | OpenAlex 检索（免费无 Key、跨学科覆盖、重建倒排摘要、提取 arXiv ID 与 OA PDF） |
