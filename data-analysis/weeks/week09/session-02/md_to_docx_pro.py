#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强版 Markdown 到 Word 转换器
支持：表格、代码块、标题层级、列表、样式优化
"""

import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_cell_border(cell, **kwargs):
    """设置表格单元格边框"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'start', 'bottom', 'end', 'left', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = OxmlElement(tag)
            for key in ['sz', 'val', 'color', 'space', 'shadow']:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), edge_data[key])
            tcBorders.append(element)
    tcPr.append(tcBorders)


def add_styled_table(doc, headers, rows):
    """添加样式化的表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # 设置表头
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        cell = hdr_cells[i]
        cell.text = header
        # 表头加粗、居中、背景色
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(11)
        # 设置表头背景色（浅灰）
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:val'), 'clear')
        shading_elm.set(qn('w:color'), 'auto')
        shading_elm.set(qn('w:fill'), 'D9E1F2')  # 浅蓝色
        cell._tc.get_or_add_tcPr().append(shading_elm)
    
    # 设置数据行
    for i, row_data in enumerate(rows):
        row_cells = table.rows[i + 1].cells
        for j, cell_data in enumerate(row_data):
            cell = row_cells[j]
            cell.text = str(cell_data)
            # 数据居中
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                for run in paragraph.runs:
                    run.font.size = Pt(10)
    
    # 设置表格宽度
    for row in table.rows:
        for cell in row.cells:
            cell.width = Cm(3)
    
    doc.add_paragraph()  # 表格后添加空行
    return table


def parse_markdown_table(lines, start_idx):
    """解析 Markdown 表格（改进版）"""
    # 第一行是表头
    header_line = lines[start_idx].strip()
    # 移除开头和结尾的 |，然后按 | 分割
    if header_line.startswith('|'):
        header_line = header_line[1:]
    if header_line.endswith('|'):
        header_line = header_line[:-1]
    headers = [h.strip() for h in header_line.split('|')]
    
    # 跳过分隔行（第二行，包含 ---）
    idx = start_idx + 2
    
    # 收集数据行
    rows = []
    while idx < len(lines) and lines[idx].strip().startswith('|'):
        row_line = lines[idx].strip()
        # 移除开头和结尾的 |
        if row_line.startswith('|'):
            row_line = row_line[1:]
        if row_line.endswith('|'):
            row_line = row_line[:-1]
        row_data = [cell.strip() for cell in row_line.split('|')]
        
        # 确保列数与表头一致
        while len(row_data) < len(headers):
            row_data.append('')
        row_data = row_data[:len(headers)]  # 截断多余的列
        
        rows.append(row_data)
        idx += 1
    
    return headers, rows, idx


def add_code_block(doc, code_lines):
    """添加代码块（带灰色背景）"""
    p = doc.add_paragraph()
    p.style = 'No Spacing'
    
    # 添加灰色背景（通过边框模拟）
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F5F5F5')  # 浅灰色背景
    pPr.append(shd)
    
    run = p.add_run('\n'.join(code_lines))
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    # 添加左边框（模拟代码块效果）
    pPr = p._p.get_or_add_pPr()
    pBorders = OxmlElement('w:pBorders')
    left_border = OxmlElement('w:left')
    left_border.set(qn('w:val'), 'single')
    left_border.set(qn('w:sz'), '12')
    left_border.set(qn('w:color'), '0070C0')  # 蓝色左边框
    pBorders.append(left_border)
    pPr.append(pBorders)
    
    doc.add_paragraph()  # 代码块后加空行


def convert_md_to_docx_pro(md_file, docx_file):
    """专业版 Markdown 到 Word 转换"""
    doc = Document()
    
    # 设置文档默认字体（宋体 for 中文）
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.font.size = Pt(11)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(6)
    
    # 添加页面设置
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        i = 0
        in_code_block = False
        code_lines = []
        
        while i < len(lines):
            line = lines[i].rstrip('\n')
            
            # 处理代码块
            if line.startswith('```'):
                if in_code_block:
                    # 代码块结束
                    add_code_block(doc, code_lines)
                    code_lines = []
                    in_code_block = False
                else:
                    # 代码块开始
                    in_code_block = True
                i += 1
                continue
            
            if in_code_block:
                code_lines.append(line)
                i += 1
                continue
            
            # 跳过空行
            if not line.strip():
                doc.add_paragraph()
                i += 1
                continue
            
            # 识别表格（以 | 开头且包含多个 |）
            if line.strip().startswith('|') and line.strip().count('|') >= 2:
                # 检查下一行是否是分隔行（|---|---|）
                if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1].strip()):
                    headers, rows, next_idx = parse_markdown_table(lines, i)
                    add_styled_table(doc, headers, rows)
                    i = next_idx
                    continue
            
            # 标题处理
            if line.startswith('# '):
                text = line[2:].strip()
                p = doc.add_heading(text, level=1)
                p.style.font.color.rgb = RGBColor(0x00, 0x70, 0xC0)  # 蓝色
            elif line.startswith('## '):
                text = line[3:].strip()
                p = doc.add_heading(text, level=2)
                p.style.font.color.rgb = RGBColor(0x00, 0x70, 0xC0)
            elif line.startswith('### '):
                text = line[4:].strip()
                p = doc.add_heading(text, level=3)
                p.style.font.color.rgb = RGBColor(0x00, 0x70, 0xC0)
            elif line.startswith('#### '):
                text = line[5:].strip()
                p = doc.add_heading(text, level=4)
            
            # 引用块
            elif line.startswith('> '):
                p = doc.add_paragraph(line[2:].strip())
                p.style = 'Intense Quote'
                p.paragraph_format.left_indent = Cm(1)
                p.paragraph_format.right_indent = Cm(1)
            
            # 无序列表
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                text = line.strip()[2:].strip()
                p = doc.add_paragraph(text, style='List Bullet')
                p.paragraph_format.space_after = Pt(3)
            
            # 有序列表
            elif re.match(r'^\d+\.\s', line.strip()):
                text = re.sub(r'^\d+\.\s', '', line.strip())
                p = doc.add_paragraph(text, style='List Number')
                p.paragraph_format.space_after = Pt(3)
            
            # 分隔线
            elif line.strip() == '---':
                doc.add_paragraph('_' * 50)
            
            # 普通段落
            else:
                # 处理粗体 **text**
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', line.strip())
                p = doc.add_paragraph(text)
                # 如果有粗体，需要单独处理（简化版）
                if '**' in line:
                    # 简化处理：移除 Markdown 标记
                    p.text = re.sub(r'\*\*', '', line.strip())
            
            i += 1
        
        # 保存文档
        doc.save(docx_file)
        print(f"✅ 成功生成专业版 Word 文档：{docx_file}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败：{e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python md_to_docx_pro.py input.md output.docx")
        sys.exit(1)
    
    md_file = sys.argv[1]
    docx_file = sys.argv[2]
    
    convert_md_to_docx_pro(md_file, docx_file)
