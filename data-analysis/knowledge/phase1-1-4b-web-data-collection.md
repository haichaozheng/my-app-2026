# 网页数据采集（requests + crawl4ai）

> **引入时机**：W4 | **核心挑战**：有些数据没有现成API，如何从网页直接采集？ | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

W2 学过了 AKShare、Tushare 等金融数据 API，它们能覆盖行情、财报、宏观等结构化数据。但你的项目可能还需要 API 覆盖不到的数据：

- **B族项目**（家庭账单解读、买房租房决策）：贝壳/链家房价、招聘站薪资——这些网站没有免费 API
- **D族项目**（研报RAG、政策影响速读）：巨潮资讯公告正文、政府政策文件——API 只返回列表，正文需从网页提取
- **另类数据**：新闻舆情、社交媒体讨论、财经博客观点——天然散布在网页中

更关键的是，**W8 要构建 RAG 知识库**，而知识库的内容从哪来？从网页采集并转为 LLM 友好的 markdown，正是 crawl4ai 最擅长的场景。W4 学会采集，W8 就能直接用。

**判断标准**：如果你的项目数据全部可通过 AKShare/Tushare 等 API 获取，本知识点可跳过。但如果哪怕有一类数据需要从网页获取，本知识点就是必须的。

## 这个知识点的核心内容

### 数据获取三层策略

面对一个数据需求，按以下优先级选择获取方式：

| 优先级 | 方式 | 适用场景 | 本课程覆盖 |
|--------|------|----------|------------|
| 1 | API（AKShare/Tushare等） | 有现成结构化API | W2 已学 |
| 2 | requests + 解析 | 静态网页，数据在HTML中 | **本知识点** |
| 3 | crawl4ai | 动态网页（JS渲染）、需要LLM友好输出 | **本知识点** |

### requests + BeautifulSoup：静态页面采集基础

**核心概念**：网页本质是 HTML 文档。requests 负责下载 HTML，BeautifulSoup 负责解析和提取。

```python
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

url = "https://www.cninfo.com.cn/new/disclosure"
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = resp.apparent_encoding

soup = BeautifulSoup(resp.text, "html.parser")

titles = soup.select("div.title a")
for t in titles:
    print(t.get_text(strip=True), t.get("href"))
```

**金融场景示例**：从巨潮资讯网提取公告列表

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_cninfo_announcements(stock_code, page=1):
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    params = {
        "pageNum": page,
        "pageSize": 30,
        "stock": stock_code,
        "tabName": "fulltext",
        "column": "szse",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    }
    resp = requests.post(url, data=params, headers=headers, timeout=10)
    data = resp.json()
    announcements = []
    for item in data.get("announcements", []):
        announcements.append({
            "标题": item.get("announcementTitle"),
            "日期": item.get("announcementTime"),
            "链接": f"http://static.cninfo.com.cn/{item.get('adjunctUrl')}",
        })
    return pd.DataFrame(announcements)

df = fetch_cninfo_announcements("000001")
print(df.head())
time.sleep(1)
```

**关键要点**：
- 始终设置 `User-Agent`，否则可能被服务器拒绝
- 使用 `timeout` 防止请求挂起
- 注意 `resp.encoding`，中文网站常需 `resp.apparent_encoding` 或手动指定 `utf-8`/`gb2312`
- 批量请求必须加 `time.sleep()`，具体间隔见下方"爬虫合规"部分

### crawl4ai：动态页面采集与 LLM 友好输出

**为什么需要 crawl4ai**：
- 很多现代网站（贝壳、东方财富部分页面）使用 JavaScript 动态渲染，requests 只能拿到空壳 HTML
- crawl4ai 内置浏览器引擎（Playwright），能执行 JS 并获取渲染后的完整页面
- 输出 markdown 格式，天然适合 LLM 消费和 RAG 知识库构建

**安装**：

```bash
pip install crawl4ai
crawl4ai-setup
```

**基本用法**：

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://finance.eastmoney.com/a/202501011234.html")
        print(result.markdown)

asyncio.run(main())
```

**金融场景示例1**：采集财经新闻并生成 RAG 知识库素材

```python
import asyncio
from crawl4ai import AsyncWebCrawler
import os

async def collect_news_for_rag(urls, output_dir="data/rag_news"):
    os.makedirs(output_dir, exist_ok=True)
    async with AsyncWebCrawler() as crawler:
        for i, url in enumerate(urls):
            result = await crawler.arun(url=url)
            if result.success:
                filepath = os.path.join(output_dir, f"news_{i:03d}.md")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# Source: {url}\n\n")
                    f.write(result.markdown)
                print(f"已采集 {url} → {filepath}")
            else:
                print(f"采集失败 {url}: {result.error_message}")

news_urls = [
    "https://finance.eastmoney.com/a/202501011234.html",
    "https://finance.sina.com.cn/stock/...",
]
asyncio.run(collect_news_for_rag(news_urls))
```

**金融场景示例2**：用 CSS 选择器做结构化提取

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import CSSEXtractionStrategy

async def extract_structured_data():
    css_strategy = CSSEXtractionStrategy({
        "标题": "h1.article-title",
        "日期": "span.date",
        "正文": "div.article-content",
    })
    config = CrawlerRunConfig(
        extraction_strategy=css_strategy,
        cache_mode=CacheMode.BYPASS,
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com/finance-article",
            config=config,
        )
        print(result.extracted_content)

asyncio.run(extract_structured_data())
```

**crawl4ai vs requests 选择指南**：

| 场景 | 推荐工具 | 理由 |
|------|----------|------|
| 静态页面，数据在 HTML 中 | requests + BeautifulSoup | 轻量、快速、无浏览器依赖 |
| 动态页面（JS渲染） | crawl4ai | 内置浏览器引擎，能获取渲染后内容 |
| 需要页面交互（点击/滚动） | crawl4ai | 支持 JS 执行和页面交互 |
| 输出需供 LLM/RAG 使用 | crawl4ai | 直接输出高质量 markdown |
| 简单 API 调用（JSON 响应） | requests | 无需浏览器，最快最简单 |

### 爬虫伦理与合规

**这是本知识点的必修部分，不可跳过。**

#### 1. robots.txt 检查

每个网站根目录下的 `robots.txt` 声明了哪些页面允许/禁止爬取。访问方式：`https://example.com/robots.txt`

```python
import requests

def check_robots_txt(base_url):
    robots_url = f"{base_url.rstrip('/')}/robots.txt"
    resp = requests.get(robots_url, timeout=5)
    print(resp.text)

check_robots_txt("https://www.eastmoney.com")
```

**规则**：
- `Disallow: /` 表示禁止爬取所有页面——**不要爬**
- `Disallow: /api/` 表示禁止爬取 `/api/` 下的页面
- `Crawl-delay: 5` 表示请求间隔至少5秒——**必须遵守**
- 即使 `robots.txt` 允许，也须遵守网站服务条款

#### 2. 频率限制（Rate Limiting）

**最低标准**：
- 每次请求间隔 **≥1秒**（`time.sleep(1)`）
- 如果网站指定 `Crawl-delay`，按其要求
- 高峰时段（工作日 9:00-15:00）对金融网站应加大间隔
- 批量采集时，每50-100条暂停5-10分钟

```python
import time
import random

for url in urls:
    resp = requests.get(url, headers=headers, timeout=10)
    process(resp)
    delay = random.uniform(1.0, 3.0)
    time.sleep(delay)
```

#### 3. 网站服务条款与法律边界

**必须遵守**：
- **公开数据 ≠ 可随意爬取**：数据公开显示不等于授权批量采集
- **不得绕过技术保护措施**：验证码、登录墙、IP 封锁等是网站明确的技术边界
- **不得采集个人数据**：用户名、手机号、身份证号等敏感信息不可采集和存储
- **尊重版权**：采集的内容用于个人学习研究，不得原样分发或商用

**财经场景特殊注意**：
- **内幕信息红线**：未公开的上市公司信息（如提前获取的财报数据）不得采集和使用
- **行情数据版权**：实时行情数据通常有版权，仅限个人研究使用
- **研报知识产权**：券商研报内容受版权保护，用于 RAG 知识库需谨慎（建议只用摘要/标题）
- **用户评论隐私**：股吧/雪球用户评论可采集但需脱敏，不得关联到具体用户身份

#### 4. 课程否决清单关联

本课程否决清单（`project-selection-guide.md` 第6节）第8条要求"不涉资金交易、不泄露敏感个人数据"。网页采集时须额外注意：
- 不得采集需要登录才能访问的页面（绕过认证机制）
- 不得采集包含用户隐私数据的页面
- 采集的数据仅用于课程项目，项目路演时须说明数据来源和采集方式

#### 5. 合规自检清单

在编写数据采集脚本前，逐项确认：

- [ ] 已检查目标网站的 `robots.txt`，未违反 Disallow 规则
- [ ] 请求间隔 ≥1秒，且遵守 Crawl-delay（如有）
- [ ] 未绕过登录/验证码等技术保护措施
- [ ] 不采集个人隐私数据（手机号、身份证、住址等）
- [ ] 采集内容仅用于课程项目学习研究
- [ ] 项目提案中已说明数据来源和采集方式

## 关键细节与易错点

### 反爬机制应对

金融网站通常有较强的反爬措施：

| 反爬方式 | 应对方法 | 注意事项 |
|----------|----------|----------|
| User-Agent 检测 | 设置真实浏览器 User-Agent | 不是绕过，是正常声明身份 |
| IP 频率限制 | 降低请求频率、使用 `time.sleep()` | 优先方案，不要用代理池绕过 |
| Cookie/Session | 使用 `requests.Session()` 保持会话 | 正常行为，非绕过 |
| JavaScript 渲染 | 使用 crawl4ai 代替 requests | crawl4ai 有完整浏览器引擎 |
| 验证码 | **放弃，换数据源** | 课程项目不应绕过验证码 |

**核心原则**：如果网站主动阻止你采集（返回403/封IP/弹验证码），说明它不希望被批量采集——**尊重这个信号，寻找替代数据源**。

### 静态 vs 动态页面判断

不确定用 requests 还是 crawl4ai？用这个简单判断法：

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(resp.text, "html.parser")
body_text = soup.get_text(strip=True)

if len(body_text) < 200:
    print("大概率是动态页面，需要 crawl4ai")
else:
    print("大概率是静态页面，可以用 requests")
```

如果 requests 拿到的页面文字极少，说明内容是 JS 渲染的，需要 crawl4ai。

### 数据落盘格式

| 采集目的 | 推荐格式 | 理由 |
|----------|----------|------|
| 结构化数据（行情/公告列表） | CSV / DuckDB | 与 API 数据统一管理 |
| RAG 知识库素材 | Markdown 文件 | crawl4ai 直接输出，LLM 友好 |
| 网页原文存档 | JSON（含 URL + HTML + 时间戳） | 可追溯、可重新提取 |
| 新闻/舆情 | JSON Lines（每行一条） | 适合流式追加 |

```python
import json
import os

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/rag", exist_ok=True)

article = {
    "url": url,
    "title": title,
    "content_md": markdown_content,
    "crawled_at": "2026-09-02T10:30:00",
    "source": "eastmoney",
}

with open("data/raw/news_001.json", "w", encoding="utf-8") as f:
    json.dump(article, f, ensure_ascii=False, indent=2)

with open("data/rag/news_001.md", "w", encoding="utf-8") as f:
    f.write(f"# {article['title']}\n\n")
    f.write(f"> 来源: {article['url']}\n")
    f.write(f"> 采集时间: {article['crawled_at']}\n\n")
    f.write(article["content_md"])
```

### 与 W8 RAG 知识库的衔接

W4 采集的 markdown 文件可直接作为 W8 RAG 的知识库素材：

```
W4 采集流程:
  网页 URL → crawl4ai.arun() → result.markdown → 保存为 .md 文件

W8 RAG 构建:
  .md 文件 → 加载 + 分块 → 向量化 → 存入向量库 → 供 LLM 检索问答
```

**建议**：W4 采集时就按 RAG 友好格式存储（文件名有意义、保留来源 URL、正文纯净 markdown），W8 就能直接加载，无需二次处理。

## 拓展学习

- **crawl4ai 官方文档**：https://docs.crawl4ai.cn/ — 完整的安装、配置和示例
- **crawl4ai 快速入门**：https://docs.crawl4ai.cn/core/quickstart/ — 10分钟上手教程
- **crawl4ai 代码示例**：https://docs.crawl4ai.cn/core/examples/ — 各类场景的代码模板
- **Requests 官方文档**：https://requests.readthedocs.io/ — HTTP 库完整参考
- **BeautifulSoup 文档**：https://www.crummy.com/software/BeautifulSoup/bs4/doc/ — HTML 解析库参考
- **robots.txt 说明**：https://developers.google.com/search/docs/crawling-indexing/robots/intro — robots.txt 协议详解

## 参考链接

- https://docs.crawl4ai.cn/ - crawl4ai 官方文档
- https://github.com/unclecode/crawl4ai - crawl4ai GitHub 仓库
- https://requests.readthedocs.io/ - Requests 官方文档
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/ - BeautifulSoup 文档
