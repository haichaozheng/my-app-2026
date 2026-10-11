# API Key 申请与额度策略

五个来源中,arXiv、CrossRef、OpenAlex 免费无 Key。Semantic Scholar 与 Google Scholar(经 SerpAPI)建议配 Key。

## 配置方式

仓库根目录 `.env`(运行脚本时在仓库根目录执行):

```text
S2_API_KEY=...
Serp_API_KEY=...
CONTACT_EMAIL=...   # 可选,让 CrossRef / OpenAlex 请求进入礼貌池(更稳定)
```

`.gitignore` 已覆盖 `.env`,Key 不会被提交到 git。脚本通过 `python-dotenv` 读取(已在 `requirements.txt`;未安装时也可用真实环境变量)。

## Semantic Scholar(`S2_API_KEY`)

- 免费申请:https://www.semanticscholar.org/product/api#api-key-form
- **没有 Key 也能用**:脚本自动限速(同源查询间隔)、延迟重试;仍失败时记入 `degraded`(信息级,不影响其他源——S2 与 OpenAlex 覆盖大量重叠)。但匿名额度很低,申请 Key 更稳。
- `--limit` 保持 20 即可,不要一次拉满 100。
- 课堂演示前先配好 Key。

## Google Scholar 经 SerpAPI(`Serp_API_KEY`)

- 免费注册:https://serpapi.com/manage-api-key (约 100 次/月)
- **同参数 1 小时内命中缓存不计费**,课堂重复演示基本不烧额度;但改检索词/参数就计费。
- **没有 Key 也能用**:脚本跳过 scholar 源并记入 `degraded`(信息级),其余来源不受影响。
- scholar 按次计费,多变体检索只扇出第一个变体(入口脚本已处理)。
