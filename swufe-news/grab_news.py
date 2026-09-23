import re
import csv
import urllib.request
from urllib.parse import urljoin

URL = "https://www.swufe.edu.cn/index/xcyw.htm"
BASE = "https://www.swufe.edu.cn/index/"
OUT_CSV = "西财要闻.csv"
OUT_XLSX = "西财要闻.xlsx"
OUT_TXT = "西财要闻.txt"
HOST = "https://www.swufe.edu.cn"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8-sig")


def parse_items(html):
    items = []
    pattern = re.compile(
        r'<a href="([^"]+)" class="publine">.*?<span>(\d{4}-\d{2}-\d{2})</span>'
        r'.*?<h3>(.*?)</h3>.*?<p>(.*?)</p>',
        re.S,
    )
    for m in pattern.finditer(html):
        href, date, title, summary = m.groups()
        link = urljoin(BASE, href)
        title = re.sub(r"<[^>]+>", "", title).strip()
        summary = re.sub(r"<[^>]+>", "", summary).strip()
        items.append({"date": date, "title": title, "link": link, "summary": summary})
    return items


def main():
    html = fetch(URL)
    items = parse_items(html)

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["序号", "日期", "标题", "链接", "摘要"])
        for i, it in enumerate(items, 1):
            writer.writerow([i, it["date"], it["title"], it["link"], it["summary"]])

    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font

        wb = Workbook()
        ws = wb.active
        ws.title = "西财要闻"
        headers = ["序号", "日期", "标题", "链接", "摘要"]
        ws.append(headers)
        for c in ws[1]:
            c.font = Font(bold=True)
        for i, it in enumerate(items, 1):
            row = [i, it["date"], it["title"], it["link"], it["summary"]]
            ws.append(row)
            row_idx = i + 1
            cell = ws.cell(row=row_idx, column=4)
            cell.hyperlink = it["link"]
            cell.font = Font(color="0563C1", underline="single")
        for col, width in zip("ABCDE", (6, 12, 40, 40, 80)):
            ws.column_dimensions[col].width = width
        wb.save(OUT_XLSX)
    except ImportError:
        print("未安装 openpyxl，跳过 xlsx 输出")

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        for i, it in enumerate(items, 1):
            f.write(f"{i}. [{it['date']}] {it['title']}\n")
            f.write(f"   链接: {it['link']}\n")
            f.write(f"   摘要: {it['summary']}\n\n")

    print(f"抓取成功，共 {len(items)} 条新闻")
    print(f"已保存: {OUT_CSV}、{OUT_XLSX} 和 {OUT_TXT}")
    for i, it in enumerate(items, 1):
        print(f"{i}. {it['date']}  {it['title']}")


if __name__ == "__main__":
    main()