---
name: search-paper
description: >-
  按检索词从 arXiv、CrossRef、Semantic Scholar、OpenAlex、Google Scholar（经 SerpAPI）拉取文献元数据并输出去重合并列表。
  This skill should be used when the user asks to search papers, 查文献, 文献检索, 检索式, PRISMA 初筛,
  或从 arXiv/CrossRef/Semantic Scholar/OpenAlex/Google Scholar 搜论文。不导入数据库、不写 Zotero。
---

# Search Paper

输入检索词，输出带元数据的文献列表。人定纳入排除标准；本 skill 只检索与去重，初筛分类可由模型做，但不替用户决定取舍。

## 边界

- 做：公开库检索、多检索词扇出、跨源去重合并、按年份/来源过滤、输出表
- 不做：导入 Literature DB、上传 PDF、写 Zotero。用户要导入时改用 `literature-import`

## 前置

- 依赖 `httpx`、`python-dotenv`（读 `.env` 中的 Key；两者均已在仓库根 `requirements.txt`）
- Semantic Scholar（`S2_API_KEY`）与 Google Scholar（经 SerpAPI，`Serp_API_KEY`）建议在仓库根目录 `.env` 配 Key。**没有 Key 也能用**：S2 自动限速重试、scholar 跳过，均记入 `degraded`（信息级），其余来源不受影响。申请方法与额度策略见 `references/keys.md`
- 可选：`.env` 写入 `CONTACT_EMAIL=...`，让 CrossRef / OpenAlex 请求进入礼貌池（更稳定）
- Key 不要提交到 git（`.gitignore` 已覆盖 `.env`）

## 检索式写法（影响准确性）

- 检索词用**英文**；中文主题先翻译成领域术语。
- 短语加英文双引号做精确匹配：`"large language model"`。
- 支持布尔：`AND`、`OR`、`ANDNOT`（arXiv 语法，全大写）。
- **覆盖关键**：缩写与全称是两套词，各查一遍。`--query` 可重复传入 2–3 个变体，脚本会对每个源×每个变体都检索再合并（**例外：scholar 按次计费，只扇出第一个变体**），如：

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
| `--sources` | `arxiv,crossref,s2,openalex,scholar`（默认五者都查；去掉不想用的即可，如 `--sources arxiv,crossref,s2,openalex` 跳过按次计费的 scholar） |

## 工作流程

1. 向用户确认检索词、年份下限、每个源的条数、**文献来源**；来源用多选题让用户勾选（默认全五源），用户不选或说「都行」就按默认跑，勾了子集就传 `--sources`。未指定的其余项用默认。
2. **先构造检索式再跑脚本**：把主题译成英文术语；给出 2–3 个 `--query` 变体（缩写 + 全称 + 可能的同义说法）；核心概念用引号短语；需要排除时用 `ANDNOT`。不要现场重写 HTTP 调用。
3. 运行 `search.py`。脚本对每个源 × 每个检索词检索（scholar 只扇出第一个变体以省额度），然后跨源去重合并：
   - 合并键优先级：DOI → arXiv ID（忽略版本号）→ 规范化题名（近邻 ≥0.95 且年份兼容）
   - 合并时互补填充字段（摘要、PDF 链接、被引数等），并记录 `matched_sources` 与 `best_rank`
   - Scholar 记录没有 DOI、也没有完整摘要（GS snippet 是碎片），靠题名并入其他源的记录后互补补齐；独有条目（学位论文、报告等灰色文献）单独成行——这正是它的价值
4. 排序按各源相关性排名（`best_rank`）优先，同年份新者靠前，不再单纯按年份排。
5. 把结果整理成 Markdown 表，列：题名、作者、年份、venue、DOI、来源（`matched_sources`）、开放获取、被引数（仅 scholar 提供的 `cited_by`，有值时展示）、摘要前 200 字。
6. 若用户给了纳入排除标准（年份、方法、语言等），只在表上标注「拟纳入 / 拟排除 / 待定」并写一句理由。标准由人确认后再筛。
7. 不要编造 API 未返回的条目。
   - 某个源失败时（`errors` 字段）说明失败源，仍展示其余来源
   - S2 匿名 429 与 scholar 无 Key / SerpAPI 额度用尽进入 `degraded` 字段（非错误）：向用户说明该源被跳过或限流、结果完整性基本不受损（OpenAlex 兜底），并提示可免费申请 Key 或稍后重试

## 脚本

| 脚本 | 作用 |
|---|---|
| `scripts/search.py` | 统一入口：多检索词扇出、去重合并、排序；集中加载 `.env` |
| `scripts/common.py` | 共享工具：`.env` 加载（`load_env`）与 DOI 规范化（`normalize_doi`） |
| `scripts/arxiv_client.py` | arXiv 检索（字段化布尔查询 + 服务端年份过滤 + 重试） |
| `scripts/crossref_client.py` | CrossRef 检索（`query.bibliographic` 精确字段 + 礼貌池 + 重试） |
| `scripts/s2_client.py` | Semantic Scholar 检索（API Key + 429 退避） |
| `scripts/openalex_client.py` | OpenAlex 检索（免费无 Key、跨学科覆盖、重建倒排摘要、提取 arXiv ID 与 OA PDF） |
| `scripts/serpapi_client.py` | Google Scholar 检索（经 SerpAPI；被引数 `cited_by` 与 PDF 直链；`as_ylo` 年份过滤；无 Key 抛 `SerpApiKeyMissing` 由入口降级跳过） |
