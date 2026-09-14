#!/usr/bin/env python3
"""西财新闻采集：requests 拿 HTML，BeautifulSoup 拆列表和正文。

默认当堂模式（1 页列表 + 1 篇正文），不会把学校网站打挂。

    python swufe-news.py
    python swufe-news.py --pages 1 --body-limit 1

课后先拉全列表，确认条数后再拉正文（每请求间隔 1 秒）：

    python swufe-news.py --pages 0 --no-body -o swufe_xcyw_list.jsonl
    python swufe-news.py --pages 0 --body --body-limit 0 -o swufe_xcyw.jsonl

其他栏目（学术讲座、通知公告等）：

    python swufe-news.py --channel xsjz --pages 1
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请先安装：python -m pip install requests beautifulsoup4", file=sys.stderr)
    raise

INDEX = "https://www.swufe.edu.cn/index"
HEADERS = {"User-Agent": "SWUFE-DA-class/0.1 (teaching; polite crawl)"}
TIMEOUT = 15
SLEEP = 1.0

# 官网左侧同一套列表
CHANNELS = {
    "xcyw": "西财要闻",
    "xsjz": "学术讲座",
    "tzgg": "通知公告",
    "xysx": "校园时讯",
    "kydt": "科研动态",
    "xcrw": "西财人物",
}


def get(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.encoding = "utf-8"
    r.raise_for_status()
    return r.text


def list_start_url(channel: str) -> str:
    return f"{INDEX}/{channel}.htm"


def parse_list(html: str, page_url: str) -> tuple[list[dict], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for a in soup.select("a.publine"):
        href = a.get("href")
        if not href:
            continue
        title = a.select_one("h3")
        date = a.select_one(".date span")
        summary = a.select_one(".info p")
        items.append(
            {
                "date": date.get_text(strip=True) if date else "",
                "title": title.get_text(strip=True) if title else "",
                "summary": summary.get_text(strip=True) if summary else "",
                "url": urljoin(page_url, href),
            }
        )
    next_a = soup.select_one("span.p_next a")
    next_url = urljoin(page_url, next_a["href"]) if next_a and next_a.get("href") else None
    return items, next_url


def fetch_article(url: str) -> dict:
    s = BeautifulSoup(get(url), "html.parser")
    h = s.select_one(".art-tit h3")
    body = s.select_one(".v_news_content")
    return {
        "url": url,
        "title": h.get_text(strip=True) if h else "",
        "text": body.get_text("\n", strip=True) if body else "",
    }


def crawl(
    channel: str,
    max_pages: int | None,
    with_body: bool,
    body_limit: int | None,
    out: Path,
) -> list[dict]:
    url = list_start_url(channel)
    seen: list[dict] = []
    pages = 0
    while url:
        print(f"列表 {pages + 1}: {url}")
        items, next_url = parse_list(get(url), url)
        seen.extend(items)
        pages += 1
        if max_pages and pages >= max_pages:
            break
        url = next_url
        if url:
            time.sleep(SLEEP)

    rows = list({row["url"]: row for row in seen}.values())
    print(f"列表去重后 {len(rows)} 条")

    out.parent.mkdir(parents=True, exist_ok=True)
    n_body = 0
    with out.open("w", encoding="utf-8") as f:
        for i, row in enumerate(rows, 1):
            rec = dict(row)
            rec["channel"] = channel
            rec["channel_name"] = CHANNELS.get(channel, channel)
            if with_body and (body_limit is None or n_body < body_limit):
                try:
                    art = fetch_article(row["url"])
                    rec["text"] = art["text"]
                    if art["title"]:
                        rec["title"] = art["title"]
                except Exception as exc:
                    rec["text"] = ""
                    rec["error"] = str(exc)
                    print(f"正文失败 {row['url']}: {exc}", file=sys.stderr)
                n_body += 1
                time.sleep(SLEEP)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if i % 20 == 0:
                print(i, "/", len(rows))
    print("saved", out)
    return rows


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="采集西南财经大学官网新闻（礼貌、可限页）")
    p.add_argument(
        "--channel",
        default="xcyw",
        choices=sorted(CHANNELS),
        help="栏目代码，默认西财要闻",
    )
    p.add_argument(
        "--pages",
        type=int,
        default=1,
        help="最多翻几页列表；0 表示跟到没有「下页」（课后全量）",
    )
    p.add_argument(
        "--body",
        dest="body",
        action="store_true",
        default=True,
        help="拉正文（默认开；当堂请配合 --body-limit 1）",
    )
    p.add_argument("--no-body", dest="body", action="store_false", help="只存列表，不进正文")
    p.add_argument(
        "--body-limit",
        type=int,
        default=1,
        help="最多拉几篇正文；0 表示本批列表全部（课后）。当堂默认 1",
    )
    p.add_argument("-o", "--out", default="", help="输出 jsonl 路径")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    max_pages = None if args.pages == 0 else args.pages
    body_limit = None if args.body_limit == 0 else args.body_limit
    out = Path(args.out) if args.out else Path(f"swufe_{args.channel}.jsonl")
    if max_pages is None or (args.body and body_limit is None):
        print("全量模式：每请求间隔 1 秒，不要并行、不要反复重跑。", file=sys.stderr)

    crawl(
        channel=args.channel,
        max_pages=max_pages,
        with_body=args.body,
        body_limit=body_limit,
        out=out,
    )


if __name__ == "__main__":
    main()
