import markdown
from html2docx import html2docx
from pathlib import Path
import io

# 读取Markdown文件
md_file = Path("market_daily_20260616.md")
html_file = Path("market_daily_20260616.html")
docx_file = Path("market_daily_20260616.docx")

# 将Markdown转换为HTML
md_content = md_file.read_text(encoding="utf-8")
html_content = markdown.markdown(md_content, extensions=["extra", "codehilite", "tables"])

# 保存HTML文件（可选）
html_file.write_text(html_content, encoding="utf-8")

# 使用html2docx将HTML转换为docx
title = "股市日报 - 2026年6月16日"
docx_bytes = html2docx(html_content, title=title)

# 保存docx文件
with open(docx_file, "wb") as f:
    f.write(docx_bytes.getvalue())

# 输出转换结果
print(f"转换完成！")
print(f"Markdown文件：{md_file}")
print(f"HTML文件：{html_file}")
print(f"Word文档：{docx_file}")