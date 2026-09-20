# 课堂教学案例：西财新闻怎么拉下来

> 给谁：W3 第 3 节「数据采集：requests + BeautifulSoup」。W2 只跟做对话拉一页、不当场拆代码；本周对照本页看 `requests` 拿、`BeautifulSoup` 拆，并邀请同学展示西财要闻数据和代码。装不上 opencode 的用 Trae 或自己敲。  
> 数据：[西财要闻](https://www.swufe.edu.cn/index/xcyw.htm)  
> 工具：`requests` 下载 HTML，`BeautifulSoup` 从 HTML 里取出标题、日期、链接、正文。  
> 当堂：跑通「列表首页 + 1 篇正文」。翻完全站、下完全文留课后（必须间隔请求，不要把学校网站打挂）。  
> 完整脚本：同目录 `swufe-news.py`（默认就是当堂模式）。

---

## 0. 先想清楚：分析西财近些年新闻，该如何做

不要一上来就写爬虫。先问四件事（对应 `data-taxonomy.md`）：

| 问 | 这份新闻大概是 |
|---|---|
| 从哪来 | **客观**（学校发过的稿），不是合成 |
| 谁能看 | **公开**（官网，不用登录） |
| 花不花钱 | **免费** |
| 怎么拿 | **网页通道**（没有现成 API，HTML 里就有） |
| 长什么样 | 列表是半结构化；正文是 **非结构化文本** |
| 能不能进产品 | 学习、分析可以；转载原文要看学校规定，默认只存自己用 |

分析路径也先写在纸上，再动手：

1. **列表**：每条新闻的日期、标题、链接  
2. **正文**：点进去拿到完整段落  
3. **落盘**：csv / jsonl，方便以后按年统计、做词频、选题  
4. **分析**（本周不必做完）：近年发稿量、主题词、哪些学院常出现——那是有了数据之后的事

本页只做到第 3 步。网页采集的系统讲法见 W4 的 `knowledge/phase1-1-4b-web-data-collection.md`。

环境（在项目 `.venv` 里）：

```text
python -m pip install requests beautifulsoup4 pandas
```

---

## 1. 两个工具各干什么

打开网页，浏览器其实做了两件事：向服务器要一份 HTML 文件，再把文件画成你看见的页面。

- **`requests`**：替你「要文件」。给一个网址，返回状态码和文本。它**不理解**标题在哪。  
- **`BeautifulSoup`**：替你「在这份 HTML 里找标签」。比如所有 `h3`、所有带 `class="publine"` 的链接。

口诀：**requests 负责拿，BeautifulSoup 负责拆。** 先拿后拆。编码不对会乱码，西财这站用 UTF-8：`resp.encoding = "utf-8"`。

礼貌：学校官网 `robots.txt` 当前是 404，仍要当客人——加 `User-Agent`、设 `timeout`、翻页时 `time.sleep`，课堂不要开多线程狂刷。

---

## 2. 浅：先把首页 HTML 拿到手

```python
import requests

URL = "https://www.swufe.edu.cn/index/xcyw.htm"
headers = {"User-Agent": "SWUFE-DA-class/0.1 (teaching; polite crawl)"}

resp = requests.get(URL, headers=headers, timeout=15)
resp.encoding = "utf-8"
print(resp.status_code)      # 200 才算拿到
print(resp.text[:400])       # 先看是不是 HTML，不要假设
```

`200` 再往下走。不是 200：把状态码记进可得性初验，换源或下课再试。

**encoding ≠ decoding。** encoding 是字→字节（网站按 UTF-8 编好再发出）；decoding 是字节→字（你必须用同一套规则解回来）。`resp.content` 是原始字节；`resp.encoding = "utf-8"` 是告诉 `requests` 按 UTF-8 **解码**。解错（例如 `decode("latin-1")`）就是乱码，`decode("utf-8")` 才是「西财要闻」。口诀：怎么 encode 的，就怎么 decode。

---

## 3. 拆列表：日期、标题、链接

用浏览器「检查」会看到每条新闻是：

```html
<a href="../info/1048/50992.htm" class="publine">
  <div class="date"><span>2026-09-12</span></div>
  <div class="info"><h3>标题</h3><p>摘要…</p></div>
</a>
```

相对路径要拼成绝对地址，用 `urljoin`，不要手搓。首页链接是 `../info/...`，翻到第 2 页会变成 `../../info/...`，层数不同，**必须**用当前列表页的完整 URL 去 join。

```python
from urllib.parse import urljoin
from bs4 import BeautifulSoup

soup = BeautifulSoup(resp.text, "html.parser")
rows = []
for a in soup.select("a.publine"):
    href = a.get("href")
    if not href:
        continue
    title = a.select_one("h3")
    date = a.select_one(".date span")
    rows.append({
        "date": date.get_text(strip=True) if date else "",
        "title": title.get_text(strip=True) if title else "",
        "url": urljoin(URL, href),
    })

print(len(rows))
print(rows[0])
```

当堂过关：能打印出大约 10 条（首页一页的条数），第一条有日期和标题。导航栏里也有链接，所以**只选 `a.publine`**，不要 `soup.select("a")` 一把抓。

---

## 4. 再深一点：一篇正文

列表页只有摘要。正文在 `https://www.swufe.edu.cn/info/1048/xxxxx.htm`，正文容器是 `.v_news_content`。

```python
import time  # 当堂只拉 1 篇，这里不用 sleep；翻很多页时再间隔请求

def fetch_article(url):
    # 列表页已经拿过 HTML；正文是另一个网址，再 requests 一次
    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"  # 和列表页一样，按 UTF-8 做 decoding
    s = BeautifulSoup(r.text, "html.parser")
    # select() 返回一串匹配；select_one() 只要第一个，找不到就是 None
    # .art-tit h3 = class="art-tit" 里面的 h3（正文页标题）
    h = s.select_one(".art-tit h3")
    # .v_news_content = class="v_news_content" 的正文容器
    body = s.select_one(".v_news_content")
    return {
        "url": url,
        "title": h.get_text(strip=True) if h else "",  # None 就不能 .get_text
        # 第一个参数是片段之间的分隔符：用换行把段落拼起来
        "text": body.get_text("\n", strip=True) if body else "",
    }

sample = fetch_article(rows[0]["url"])  # 用列表里第一条的链接
print(sample["title"])
print(sample["text"][:200])  # 先看前 200 字，确认有完整段落
```

当堂只拉 **1 篇**。确认有完整段落，再谈翻页。

---

## 5. 翻页：西财要闻「全部列表」

首页底栏类似：共 2400 余条、约 241 页。第一页是 `xcyw.htm`；第 2 页是 `xcyw/240.htm`，**尾页是 `xcyw/1.htm`**（页码倒着编）。数字以后会变，不要把 `240` 写死。

稳妥做法：解析「下页」的 `href`，跟到没有「下页」为止。

```python
def parse_list(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for a in soup.select("a.publine"):
        href = a.get("href")
        if not href:
            continue
        title = a.select_one("h3")
        date = a.select_one(".date span")
        items.append({
            "date": date.get_text(strip=True) if date else "",
            "title": title.get_text(strip=True) if title else "",
            "url": urljoin(page_url, href),
        })
    next_a = soup.select_one("span.p_next a")
    next_url = urljoin(page_url, next_a["href"]) if next_a and next_a.get("href") else None
    return items, next_url
```

课堂：`max_pages = 1`。课后下全列表：去掉限制，**每一页 `time.sleep(1)`**。两千多条列表只要两百来次列表请求，不要并行。

---

## 6. 深：列表 + 正文都落盘（课后）

思路：先收齐链接（去重），再逐篇要正文，写成 `swufe_xcyw.jsonl`（一行一篇，坏一篇不影响全部）。

```python
import json
from pathlib import Path

def get(url):
    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"
    r.raise_for_status()
    return r.text

def crawl_xcyw(max_pages=None, with_body=False, out="swufe_xcyw.jsonl"):
    url = "https://www.swufe.edu.cn/index/xcyw.htm"
    seen = []
    pages = 0
    while url:
        items, next_url = parse_list(get(url), url)
        seen.extend(items)
        pages += 1
        if max_pages and pages >= max_pages:
            break
        url = next_url
        if url:
            time.sleep(1)

    uniq = {row["url"]: row for row in seen}
    rows = list(uniq.values())

    path = Path(out)
    with path.open("w", encoding="utf-8") as f:
        for i, row in enumerate(rows, 1):
            if with_body:
                art = fetch_article(row["url"])
                row = {**row, "text": art["text"]}
                time.sleep(1)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            if i % 20 == 0:
                print(i, "/", len(rows))
    print("saved", path, "n=", len(rows))

# 当堂：1 页列表 + 这些条目的正文
crawl_xcyw(max_pages=1, with_body=True, out="swufe_xcyw_demo.jsonl")

# 课后：先全列表，确认条数后再拉正文（务必 sleep）
# crawl_xcyw(max_pages=None, with_body=False, out="swufe_xcyw_list.jsonl")
# crawl_xcyw(max_pages=None, with_body=True, out="swufe_xcyw.jsonl")
```

写进可得性初验：源 = 西财要闻；通道 = 网页；拿到多少条；失败原因（超时 / 选择器变了 / 校园网拦截）。

---

## 7. 「所有新闻」：不止要闻一栏

官网左侧同一套列表还有：学术讲座 `xsjz.htm`、通知公告 `tzgg.htm`、校园时讯 `xysx.htm`、科研动态 `kydt.htm`、西财人物 `xcrw.htm` 等，首页都在 `https://www.swufe.edu.cn/index/` 下。结构同类：`a.publine` + 倒序翻页。

进阶：把栏目做成列表，每个栏目走同一套 `parse_list`，文件名带栏目代码，例如 `swufe_xsjz.jsonl`。仍是一栏一栏跑、每请求睡 1 秒。**不要**一节课里把全站正文下完。

---

## 8. 拿到手之后可以问什么（启发，当堂一句）

有了按年的标题和正文，才谈「近些年」：

- 每年发稿量是升是降？  
- 标题里「调研 / 会议 / 表彰 / 合作」谁更多？  
- 哪些学院、哪些校外机构反复出现？

那是分析题，不是采集题。本周过关 = 文件里真有日期、标题、链接（加一篇正文更好）。

---

## 卡住了

- 乱码：`resp.encoding = "utf-8"`，不要迷信 `apparent_encoding`。  
- `rows` 是 0：学校改了 class。打开「检查」，确认还是不是 `a.publine`。  
- 相对链接打不开：`urljoin` 的底必须是**当前列表页**的完整 URL。  
- 超时 / 连不上：校园网或对方限流。记失败，不当堂死磕。  
- 想一次下两千篇正文：先只存列表；正文分批、必 `sleep`。把学校官网打挂 = 本课不合格。
