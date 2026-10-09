#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将 Markdown 文件转换为 Word (docx) 格式
"""

import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn


def add_markdown_content(doc, line):
    """将 Markdown 行添加到 Word 文档"""
    
    # 跳过空行
    if not line.strip():
        doc.add_paragraph()
        return
    
    # 标题
    if line.startswith('# '):
        p = doc.add_heading(line[2:].strip(), level=1)
    elif line.startswith('## '):
        p = doc.add_heading(line[3:].strip(), level=2)
    elif line.startswith('### '):
        p = doc.add_heading(line[4:].strip(), level=3)
    elif line.startswith('#### '):
        p = doc.add_heading(line[5:].strip(), level=4)
    
    # 代码块（以 ``` 开头）
    elif line.startswith('```'):
        # 代码块开始/结束标记，这里简单处理
        p = doc.add_paragraph(line)
        p.style = 'No Spacing'
        for run in p.runs:
            run.font.name = 'Courier New'
            run.font.size = Pt(9)
    
    # 表格（简单处理，以 | 分隔）
    elif line.startswith('|') and '|' in line[1:]:
        # 这里需要更复杂的表格处理逻辑
        # 暂时作为普通段落处理
        p = doc.add_paragraph(line)
        p.style = 'No Spacing'
        for run in p.runs:
            run.font.name = 'Courier New'
            run.font.size = Pt(9)
    
    # 引用
    elif line.startswith('> '):
        p = doc.add_paragraph(line[2:].strip())
        p.style = 'Intense Quote'
    
    # 列表项
    elif line.startswith('- ') or line.startswith('* '):
        p = doc.add_paragraph(line[2:].strip(), style='List Bullet')
    elif re.match(r'^\d+\.\s', line):
        p = doc.add_paragraph(re.sub(r'^\d+\.\s', '', line).strip(), style='List Number')
    
    # 普通段落
    else:
        p = doc.add_paragraph(line.strip())


def convert_md_to_docx(md_file, docx_file):
    """转换 Markdown 文件为 Word 文档"""
    doc = Document()
    
    # 设置文档默认字体（中文）
    doc.styles['Normal'].font.name = '宋体'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    doc.styles['Normal'].font.size = Pt(12)
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_code_block = False
        code_lines = []
        
        for line in lines:
            line = line.rstrip('\n')
            
            # 处理代码块
            if line.startswith('```'):
                if in_code_block:
                    # 代码块结束
                    p = doc.add_paragraph()
                    p.style = 'No Spacing'
                    run = p.add_run('\n'.join(code_lines))
                    run.font.name = 'Courier New'
                    run.font.size = Pt(9)
                    code_lines = []
                    in_code_block = False
                else:
                    # 代码块开始
                    in_code_block = True
                continue
            
            if in_code_block:
                code_lines.append(line)
            else:
                add_markdown_content(doc, line)
        
        # 保存文档
        doc.save(docx_file)
        print(f"✅ 成功生成 Word 文档：{docx_file}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败：{e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python md_to_docx.py input.md output.docx")
        sys.exit(1)
    
    md_file = sys.argv[1]
    docx_file = sys.argv[2]
    
    convert_md_to_docx(md_file, docx_file)
