#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将股市日报Markdown内容转换为Word文档
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

def create_docx_from_markdown(md_content, output_path):
    doc = Document()
    
    # 设置默认字体
    style = doc.styles['Normal']
    font = style.font
    font.name = '宋体'
    font.size = Pt(11)
    
    lines = md_content.split('\n')
    
    for line in lines:
        line = line.rstrip()
        
        # 跳过空行
        if not line:
            continue
        
        # 文档标题 (# 开头)
        if line.startswith('# '):
            title_text = line[2:]
            p = doc.add_heading(title_text, level=0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue
        
        # 二级标题 (## 开头)
        if line.startswith('## '):
            section_text = line[3:]
            doc.add_heading(section_text, level=1)
            continue
        
        # 三级标题 (### 开头) - 如果有的话
        if line.startswith('### '):
            subsection_text = line[4:]
            doc.add_heading(subsection_text, level=2)
            continue
        
        # 列表项 (- 开头)
        if line.startswith('- '):
            item_text = line[2:]
            p = doc.add_paragraph(style='List Bullet')
            # 处理加粗文本
            add_formatted_text(p, item_text)
            continue
        
        # 普通段落
        p = doc.add_paragraph()
        add_formatted_text(p, line)
    
    doc.save(output_path)
    print(f"Word文档已保存至: {output_path}")

def add_formatted_text(paragraph, text):
    """处理加粗和斜体等格式"""
    # 简单处理加粗文本 (**...**)
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            # 加粗文本
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            # 普通文本
            paragraph.add_run(part)

if __name__ == "__main__":
    import sys
    
    # 默认输入输出路径
    default_input = r"C:\haichao\teaching\2026-finance-ai\session-03\daily_report_20260616.md"
    default_output = r"C:\haichao\teaching\2026-finance-ai\session-03\股市日报_20260616.docx"
    
    # 从命令行参数获取路径，或使用默认值
    input_file = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_file = sys.argv[2] if len(sys.argv) > 2 else default_output
    
    # 读取Markdown文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件时出错：{e}")
        sys.exit(1)
    
    create_docx_from_markdown(md_content, output_file)