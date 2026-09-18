import requests
from bs4 import BeautifulSoup
import csv
import re
import sys


def fetch_news():
    """采集西财新闻"""
    base_url = "https://www.swufe.edu.cn"
    list_url = f"{base_url}/index/xcyw.htm"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    resp = requests.get(list_url, headers=headers, timeout=15)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    news_items = []
    for li in soup.select("div.i-list ul li"):
        a = li.select_one("a.publine")
        if not a:
            continue
        href = a.get("href", "")
        h3 = a.select_one("h3")
        date_span = a.select_one("div.date span")
        if not h3 or not date_span:
            continue
        title = h3.get_text(strip=True)
        date = date_span.get_text(strip=True)
        if href.startswith(".."):
            link = base_url + href[2:]
        elif href.startswith("/"):
            link = base_url + href
        else:
            link = f"{base_url}/index/{href}"
        news_items.append({"title": title, "date": date, "link": link})

    print(f"找到 {len(news_items)} 条新闻")

    results = []
    for i, item in enumerate(news_items):
        try:
            print(f"采集第 {i+1}/{len(news_items)} 条: {item['title'][:40]}...")
            resp2 = requests.get(item["link"], headers=headers, timeout=15)
            resp2.encoding = "utf-8"
            soup2 = BeautifulSoup(resp2.text, "html.parser")

            content = ""
            vsb = soup2.select_one("#vsb_content")
            if vsb:
                content = vsb.get_text(separator="\n", strip=True)
            if not content:
                for sel in [".news-content", ".article-content", ".content",
                            ".v_news_content", "[class*='content']"]:
                    el = soup2.select_one(sel)
                    if el:
                        content = el.get_text(separator="\n", strip=True)
                        if len(content) > 20:
                            break
            if not content:
                paragraphs = soup2.select("p")
                content = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 10)

            results.append({
                "title": item["title"],
                "date": item["date"],
                "content": content[:3000]
            })
        except Exception as e:
            print(f"  采集失败: {e}")

    return results


def save_to_csv(data, filename="swufe_news_data.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "date", "content"])
        writer.writeheader()
        writer.writerows(data)
    print(f"\n已保存 {len(data)} 条新闻到 {filename}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("开始采集西南财经大学新闻...")
    news = fetch_news()
    if news:
        save_to_csv(news)
    else:
        print("未采集到新闻")
