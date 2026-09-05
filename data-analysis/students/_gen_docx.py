# -*- coding: utf-8 -*-
"""
生成《(2026-2027-1)-数据分析与可视化-课程实施方案（郑海超）.docx》
要点：
  - Word 内置样式体系（Title / Heading 1-3），大纲级别规范
  - 表格宽度使用 dxa(twips) 正确单位，固定布局，总宽 8957（A4 版心）
  - 表头深蓝底白字、跨页自动重复；斑马纹；细边框；行禁拆分
  - 自动目录域（TOC）+ settings updateFields，打开文档自动生成带页码目录
  - 页眉 + 页脚居中页码域（PAGE）
  - 正文宋体小四、1.5 倍行距、首行缩进 2 字符、两端对齐
  - 18 个外部超链接
"""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE

OUT = Path(__file__).with_name("(2026-2027-1)-数据分析与可视化-课程实施方案（郑海超）.docx")

# ---------- 颜色 ----------
DEEP_BLUE = RGBColor(0x1F, 0x4E, 0x79)   # 主色：深蓝
MID_BLUE  = RGBColor(0x2F, 0x549, 0x6) if False else RGBColor(0x2F, 0x54, 0x96)
GRAY      = RGBColor(0x59, 0x59, 0x59)
LINK_BLUE = RGBColor(0x05, 0x63, 0xC1)

HEX_HEADER = "1F4E79"   # 表头深蓝
HEX_ZEBRA  = "EEF3FA"   # 斑马纹浅蓝
HEX_BORDER = "B8C6DB"   # 表格边框
HEX_LABEL  = "DCE6F1"   # 信息表标签列浅蓝
HEX_NOTE   = "F2F6FB"   # 求助路径底色

PAGE_W = 8957  # A4(11906) - 左右边距(1475x2) 版心宽度(dxa)


# ---------- 基础工具 ----------
def set_east_asian(style_or_run, east):
    rPr = style_or_run.element.get_or_add_rPr() if hasattr(style_or_run, "element") \
        else style_or_run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), east)


def style_font(style, east, latin, size, bold, color):
    style.font.name = latin
    style.font.size = size
    style.font.bold = bold
    style.font.color.rgb = color
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), east)


def first_line_chars(p, chars=200, twips=480):
    """中文规范的‘首行缩进 2 字符’"""
    p.paragraph_format.first_line_indent = Pt(24)  # 确保 w:ind 存在且顺序正确
    ind = p._p.get_or_add_pPr().find(qn("w:ind"))
    if ind is not None:
        ind.set(qn("w:firstLineChars"), str(chars))
        ind.set(qn("w:firstLine"), str(twips))


def body_para(doc, text="", indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.line_spacing = 1.5
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    if indent:
        first_line_chars(p)
    if text:
        add_rich(p, text)
    return p


BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
CODE_RE = re.compile(r"`([^`]+)`")


def add_rich(p, text, size=None, color=None, bold_all=False):
    """解析 **粗体** 与 `代码` 标记，逐段添加 run"""
    # 先按代码标记切，再对每段按粗体切
    segs = []
    for piece in CODE_RE.split(text):
        segs.append(("txt", piece)) if piece else None
    # 更简单：直接线性扫描两种标记
    segs = []
    pos = 0
    token_re = re.compile(r"\*\*(.+?)\*\*|`([^`]+)`")
    for m in token_re.finditer(text):
        if m.start() > pos:
            segs.append(("txt", text[pos:m.start()]))
        if m.group(1) is not None:
            segs.append(("bold", m.group(1)))
        else:
            segs.append(("code", m.group(2)))
        pos = m.end()
    if pos < len(text):
        segs.append(("txt", text[pos:]))

    for kind, seg in segs:
        if not seg:
            continue
        r = p.add_run(seg)
        r.font.name = "Times New Roman"
        r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")
        if size:
            r.font.size = size
        if color:
            r.font.color.rgb = color
        if kind == "bold" or bold_all:
            r.font.bold = True
        if kind == "code":
            r.font.name = "Consolas"
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(0x88, 0x4C, 0x1A)
    return p


def add_hyperlink(p, url, text=None):
    text = text or url
    r_id = p.part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hl = OxmlElement("w:hyperlink")
    hl.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")
    rPr.append(rFonts)
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "21"); rPr.append(sz)  # 10.5pt
    run.append(rPr)
    t = OxmlElement("w:t"); t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    hl.append(run)
    p._p.append(hl)
    return p


def heading(doc, text, level, bottom_border=False):
    p = doc.add_paragraph(style=f"Heading {level}")
    r = p.add_run(text)
    if bottom_border:
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "8")
        bottom.set(qn("w:space"), "4")
        bottom.set(qn("w:color"), "1F4E79")
        pBdr.append(bottom)
        pPr.append(pBdr)
    return p


def bullet(doc, prefix="•"):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(4)
    pf.left_indent = Cm(0.85)
    pf.first_line_indent = Cm(-0.5)
    r = p.add_run(prefix + " ")
    r.font.name = "Times New Roman"
    r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")
    return p


def numbered(doc, num):
    """有序列表：保留原文数字，悬挂缩进"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(4)
    pf.left_indent = Cm(0.95)
    pf.first_line_indent = Cm(-0.7)
    r = p.add_run(f"{num}. ")
    r.font.name = "Times New Roman"
    r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")
    return p


def shaded_para(doc, fill):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)
    return p


# ---------- 表格 ----------
def set_table_borders(table, color=HEX_BORDER):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def set_cell_margins(table, top=50, bottom=50, left=90, right=90):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for tag, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{tag}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def cell_text(cell, text, bold=False, white=False, center=False, size=10.5, rich=False, link=None):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if rich:
        add_rich(p, text, size=Pt(size))
        if bold:
            for r in p.runs:
                r.font.bold = True
    else:
        r = p.add_run(text)
        r.font.bold = bold
        r.font.size = Pt(size)
        r.font.name = "Times New Roman"
        r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "黑体" if bold else "宋体")
        if white:
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    if link:
        add_hyperlink(p, link)
    return p


def make_table(doc, headers, rows, widths, center_cols=(0,), zebra=True, header_row=True):
    """规范表格：固定布局、总宽=版心、表头深蓝白字跨页重复、斑马纹、行禁拆分"""
    n_cols = len(widths)
    table = doc.add_table(rows=0, cols=n_cols)
    table.style = None  # 去掉默认样式干扰，全部自控
    tbl = table._tbl
    tblPr = tbl.tblPr

    # 固定布局 + 总宽
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed"); tblPr.append(layout)
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW"); tblPr.append(tblW)
    tblW.set(qn("w:w"), str(sum(widths)))
    tblW.set(qn("w:type"), "dxa")

    # 网格列宽
    grid = tbl.find(qn("w:tblGrid"))
    if grid is not None:
        tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(w))
        grid.append(gc)
    tbl.insert(list(tbl).index(tblPr) + 1, grid)

    set_table_borders(table)
    set_cell_margins(table)

    # 表头行
    if header_row and headers:
        row = table.add_row()
        trPr = row._tr.get_or_add_trPr()
        th = OxmlElement("w:tblHeader"); trPr.append(th)     # 跨页重复表头
        cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        for i, h in enumerate(headers):
            c = row.cells[i]
            c.width = Emu(0)  # 先清
            shade_cell(c, HEX_HEADER)
            cell_text(c, h, bold=True, white=True, center=True, size=10.5)

    # 数据行
    for ri, data in enumerate(rows):
        row = table.add_row()
        trPr = row._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        for i, val in enumerate(data):
            c = row.cells[i]
            if zebra and ri % 2 == 1:
                shade_cell(c, HEX_ZEBRA)
            link = None
            if isinstance(val, tuple):
                val, link = val
            if link:
                # 链接单元格：仅显示名称作为超链接文本
                cell_text(c, "", center=(i in center_cols))
                add_hyperlink(c.paragraphs[0], link, text=val)
            else:
                cell_text(c, val, center=(i in center_cols))

    # 每个单元格写 tcW（dxa）
    for row in table.rows:
        for i, c in enumerate(row.cells):
            tcPr = c._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW"); tcPr.append(tcW)
            tcW.set(qn("w:w"), str(widths[i]))
            tcW.set(qn("w:type"), "dxa")

    return table


# ---------- 域 ----------
def add_toc_field(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run()
    fld1 = OxmlElement("w:fldChar"); fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve")
    instr.text = ' TOC \\o "1-3" \\h \\z \\u '
    fld2 = OxmlElement("w:fldChar"); fld2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "（目录将在文档打开时自动更新；若未更新请全选后按 F9）"
    fld3 = OxmlElement("w:fldChar"); fld3.set(qn("w:fldCharType"), "end")
    r = run._r
    r.append(fld1); r.append(instr); r.append(fld2); r.append(t); r.append(fld3)
    return p


def enable_update_fields(doc):
    settings = doc.settings.element
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    settings.append(upd)


def add_page_field(p):
    run = p.add_run()
    r = run._r
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " PAGE "
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    r.append(f1); r.append(it); r.append(f2)
    for el in (f1, it, f2):
        pass
    run.font.size = Pt(9)
    run.font.color.rgb = GRAY


# ---------- 文档组装 ----------
def build():
    doc = Document()

    # 页面：A4
    sec = doc.sections[0]
    sec.page_width = Emu(11906 * 635)   # 21cm
    sec.page_height = Emu(16838 * 635)  # 29.7cm
    sec.left_margin = Cm(2.6)
    sec.right_margin = Cm(2.6)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.2)
    sec.header_distance = Cm(1.5)
    sec.footer_distance = Cm(1.2)

    # 样式体系
    normal = doc.styles["Normal"]
    style_font(normal, "宋体", "Times New Roman", Pt(12), False, RGBColor(0, 0, 0))
    normal.paragraph_format.line_spacing = 1.5

    style_font(doc.styles["Title"], "黑体", "Times New Roman", Pt(26), True, DEEP_BLUE)
    doc.styles["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    style_font(doc.styles["Heading 1"], "黑体", "Times New Roman", Pt(16), True, DEEP_BLUE)
    doc.styles["Heading 1"].paragraph_format.space_before = Pt(18)
    doc.styles["Heading 1"].paragraph_format.space_after = Pt(10)

    style_font(doc.styles["Heading 2"], "黑体", "Times New Roman", Pt(14), True, MID_BLUE)
    doc.styles["Heading 2"].paragraph_format.space_before = Pt(12)
    doc.styles["Heading 2"].paragraph_format.space_after = Pt(6)

    style_font(doc.styles["Heading 3"], "黑体", "Times New Roman", Pt(12.5), True, MID_BLUE)
    doc.styles["Heading 3"].paragraph_format.space_before = Pt(10)
    doc.styles["Heading 3"].paragraph_format.space_after = Pt(6)

    # 页眉
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hr = hp.add_run("金融数据分析与可视化 · 教学实施方案")
    hr.font.size = Pt(9)
    hr.font.color.rgb = GRAY
    hr.font.name = "Times New Roman"
    hr._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")
    pPr = hp._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "2"); bottom.set(qn("w:color"), "B8C6DB")
    pBdr.append(bottom); pPr.append(pBdr)

    # 页脚页码
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = fp.add_run("— ")
    r0.font.size = Pt(9); r0.font.color.rgb = GRAY
    add_page_field(fp)
    r1 = fp.add_run(" —")
    r1.font.size = Pt(9); r1.font.color.rgb = GRAY

    enable_update_fields(doc)

    # ===== 封面标题 =====
    t = doc.add_paragraph(style="Title")
    t.add_run("金融数据分析与可视化")
    t.paragraph_format.space_before = Pt(48)
    t.paragraph_format.space_after = Pt(6)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.paragraph_format.space_after = Pt(10)
    sr = sub.add_run("教学实施方案")
    sr.font.size = Pt(18); sr.font.bold = True
    sr.font.name = "Times New Roman"
    sr._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "黑体")
    sr.font.color.rgb = MID_BLUE

    sem = doc.add_paragraph()
    sem.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sem.paragraph_format.space_after = Pt(30)
    mr = sem.add_run("（2026—2027学年第1学期）")
    mr.font.size = Pt(12); mr.font.color.rgb = GRAY
    mr.font.name = "Times New Roman"
    mr._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")

    # ===== 目录 =====
    toc_h = doc.add_paragraph()
    toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    toc_h.paragraph_format.space_before = Pt(12)
    toc_h.paragraph_format.space_after = Pt(12)
    thr = toc_h.add_run("目  录")
    thr.font.size = Pt(16); thr.font.bold = True
    thr.font.color.rgb = DEEP_BLUE
    thr.font.name = "Times New Roman"
    thr._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "黑体")
    add_toc_field(doc)

    # 分页
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ===== 一、课程基本信息 =====
    heading(doc, "一、课程基本信息", 1, bottom_border=True)
    make_table(
        doc,
        headers=None,
        rows=[
            ("课程名称", "数据分析与可视化"),
            ("学分", "3"),
            ("学时", "3学时/课，17个教学周"),
            ("面向对象", "财经院校本科生"),
            ("教学方法", "Project Based Learning（PBL），方法论锚定设计科学研究（Design Science Research, DSR）"),
            ("课程展示", ("data-analysis-showcase", "https://haichaozheng.github.io/data-analysis-showcase")),
        ],
        widths=[1500, 7457],
        center_cols=(0,),
        zebra=True,
        header_row=False,
    )
    # 标签列着色加粗
    tbl1 = doc.tables[-1]
    for row in tbl1.rows:
        c0 = row.cells[0]
        shade_cell(c0, HEX_LABEL)
        for r in c0.paragraphs[0].runs:
            r.font.bold = True

    # ===== 二、任课教师、教室等情况 =====
    heading(doc, "二、任课教师、教室等情况", 1, bottom_border=True)
    for label, rest in [
        ("（一）任课教师：", "郑海超，西南财经大学管理科学与工程学院，教授"),
        ("（二）教室：", "颐德楼I401A（后期如有调整会在教学群通知）"),
        ("（三）上课时间：", "星期三第1-3节，第1-17周"),
    ]:
        p = body_para(doc)
        r = p.add_run(label)
        r.font.bold = True
        add_rich(p, rest)
    p = body_para(doc)
    r = p.add_run("（四）纪律：")
    r.font.bold = True
    for i, item in enumerate([
        "按时完成课后资料学习，及时与老师沟通进行答疑。",
        "无特殊情况，不迟到早退，不无故缺课。",
        "每次作业或测试须在规定时间完成并提交。",
        "课程基本教与学原则由师生在课程初期共同确定，形成课程公约，共同遵守。",
        "遵守数据采集合规与伦理要求，不滥用AI工具，不抄袭、不代做，学术诚信贯穿全程。",
    ], 1):
        p = numbered(doc, i)
        add_rich(p, item)
    p = body_para(doc)
    r = p.add_run("（五）求助路径（卡住时按顺序求助）：")
    r.font.bold = True
    box = shaded_para(doc, HEX_NOTE)
    box.paragraph_format.line_spacing = 1.5
    box.paragraph_format.space_before = Pt(4)
    box.paragraph_format.space_after = Pt(8)
    box.paragraph_format.left_indent = Cm(0.5)
    box.paragraph_format.right_indent = Cm(0.5)
    add_rich(box, "AI工具自助 → 互助小组 → 课程群提问（24小时内响应） → 课堂一对一交流。")

    # ===== 三、课程内容概要 =====
    heading(doc, "三、课程内容概要", 1, bottom_border=True)

    heading(doc, "（一）课程指导思想", 2)
    body_para(doc, "在新时代背景下，金融数据分析与可视化课程旨在培养具备深厚理论基础和实践能力的复合型、创新型人才。本课程紧密围绕国家金融战略需求与金融强国建设目标，注重理论与实践相结合，强调金融数据分析技术服务于金融安全、服务实体经济与防范化解金融风险的能力培养。")
    body_para(doc, "本学期课程全面升级为 **PBL（项目式学习）+ AI赋能** 模式：学生围绕金融领域的真实数据与真实用户需求，在17周内独立构建、上线并公开展示一个属于自己的金融数据分析产品。课程以设计科学研究（DSR）为方法论锚定，使项目实践既具教学真实性又具学术严谨性；通过“AI赋能的一人公司（OPC）+ 互助小组”组织形式，培养学生运用人工智能工具（AI辅助编程、Prompt Engineering、LangChain、RAG、Agent等）解决复杂问题的能力和创新创业思维，使学生有潜力产出公开产品乃至学术论文等高水平成果。")
    body_para(doc, "在教学过程中，教师始终坚持正确的政治方向，将思想政治教育贯穿课程各环节；课程同时强调金融伦理、数据合规与社会责任，引导学生树立正确的金融价值观和数据安全观，自觉维护国家金融安全，为构建和谐金融环境贡献力量。")

    heading(doc, "（二）课程思政", 2)
    for i, item in enumerate([
        "在课程内容中，融入中国数据分析科学发展史。以数据分析科学发展与时代划分的重要联系作为切入点，介绍数据分析科学发展与国民经济发展的重要关系，结合全国金融工作会议精神，强调金融是国家重要的核心竞争力、金融安全是国家安全的重要组成部分，引导学生学好专业课，为国家发展和社会进步贡献自己的力量，培养和树立社会责任感。",
        "将最新的金融数据分析新闻资讯、科研动态、应用实例引入课堂，以我国金融改革发展取得的新成就、人工智能自主创新进展为素材，激发学生的爱国热情和自豪感，激励其为国家振兴、民族强盛而努力学习。",
        "树立典型人物的励志故事，通过介绍取得重大科学技术成就并具有爱国热情的人物和事件，引导青年学生热爱祖国、热爱科学、珍惜美好的学习生活，激发学生爱国情怀以及在本专业创造人生成就的巨大热情。",
        "结合课程特点强化特色思政元素：数据采集合规与数据安全意识（数据安全法、个人信息保护）、科学严谨与诚实守信（批判性思维、不造假、评估有据）、创新创业服务国家需要（普惠金融、服务实体经济）、AI治理与负责任使用人工智能。",
    ], 1):
        p = numbered(doc, i)
        add_rich(p, item)

    heading(doc, "（三）课程目标", 2)
    for i, item in enumerate([
        "理解并掌握利用Python进行金融数据分析的基本思路和方法（采集→清洗→分析建模→可视化完整流程），提高动手能力及独立思考和分析能力。",
        "深入了解Python的各种基础功能以及与数据分析相关的工具：例如NumPy、Pandas、Scikit-learn、statmodels、Plotly、Pyecharts、Streamlit等。",
        "掌握利用API或爬虫等方式从网络获取金融数据的方法，理解数据采集的合规与伦理要求。",
        "掌握机器学习基础模型（线性/逻辑回归、朴素贝叶斯、SVM、决策树与随机森林、神经网络基础）和程序实现方法，能通过多模型公平对比选择模型，并能对模型进行合理评估。",
        "掌握AI赋能的编程工具（opencode、Cursor、Trae等）与AI应用开发技术栈（Prompt Engineering、LangChain、LLM API、RAG、Agent/Skill），能在产品中集成真实解决用户痛点的AI功能。",
        "掌握从真实需求出发发现、验证并产品化一个金融数据分析问题的完整方法（用户洞察、社区调研、快速原型、部署上线、获客与用户反馈迭代），培养创新与创业思维。",
    ], 1):
        p = numbered(doc, i)
        add_rich(p, item)

    heading(doc, "（四）课程要求", 2)
    for i, item in enumerate([
        "按时完成课程资料学习。",
        "按时提交作业。",
        "课程项目：采用“AI赋能的一人公司（OPC）+ 互助小组”模式。鼓励学生5人一组组成互助小组（组内不要求共享同一赛道或领域），**每人独立完成并交付一个属于自己的金融数据分析产品**，学期末公开路演展示。路演时产品须公网可访问，其他同学和观众可当场打开试用。选题来源为财经新闻驱动、真实需求驱动、个人爱好三档，须经用户访谈验证真实需求。",
        "项目工作流：以个人项目仓库（repo）为项目管理中枢，每轮迭代产出/更新 requirements → design → scope 三个文档，并维护一份稳定的 AGENTS.md；git提交历史即学习审计轨迹。",
        "反思与日志：个人仓库维护一份 journal.md（按学习日追加）；W3 / W10 / W15 / W17 提交截至当周的全文作为作业。",
        "学术诚信：所有AI辅助使用情况须如实记录；不得抄袭、代做；数据采集须合规。",
    ], 1):
        p = numbered(doc, i)
        add_rich(p, item)

    heading(doc, "（五）教学方法与组织形式", 2)
    for label, rest in [
        ("PBL六要素：", "真实问题（金融社区真实痛点）、持续探究（17周迭代）、学生自主权（三档选题+三选一实验）、反思（双层日志+DSR自检）、同伴互评（W9组内互评）、公开产品（公网部署+路演；路演现场其他人可打开产品）。"),
        ("知识组织方式：", "知识按项目阶段而非学科章节组织，按 Challenge→Gap→Knowledge→Apply 节奏在需求时刻引入。"),
        ("AI基础工具栈渐进融入：", "Prompt+AI辅助编程（起步）→ LangChain+LLM API（必做）→ RAG（选做升级）→ 建模增强（ML基础与基础模型地图 → 决策树与随机森林课堂讲授+朴素贝叶斯自学 → 对照大模型与传统分析+神经网络基础 → 多模型对比+SVM自学 → 模型评估与产品化）→ AI系统评估（贯穿全阶段）。"),
        ("DSR方法论锚定：", "以DSR三循环（相关性/严谨性/设计）与DSRM六步为方法论骨架；产品即artifact、评估即evaluation、用户反馈即相关性循环证据。全员必做“简短DSR定位 + ≥1条有效性（criterion validity）声明”。"),
    ]:
        p = bullet(doc, "•")
        r = p.add_run(label)
        r.font.bold = True
        add_rich(p, rest)

    heading(doc, "（六）教学内容与周次安排", 2)

    phase1 = [
        ("1", "课程导论（Trae安装与环境准备 + PBL循环）", "结合全国金融工作会议精神，强调金融是国家重要的核心竞争力、金融安全是国家安全的重要组成部分；介绍中国数据分析科学发展与国民经济发展的关系，树立社会责任感"),
        ("2", "进入数据与社区（opencode / AGENTS.md + 金融数据源）", "介绍党的十八大以来我国金融改革发展取得的重大成就、金融数据开放与普惠金融进展，增强“四个自信”"),
        ("3", "提出真问题（用户访谈 + 项目筛选框架）", "培养实事求是、科学决策的精神：痛点须经真实用户访谈验证而非凭空假设；做事要回归本源、服从服务于经济社会发展"),
    ]
    phase2 = [
        ("4", "动手跑通分析（API/网页采集 + 数据分析思维链）", "强化数据采集合规与数据安全意识（数据安全法、个人信息保护法）；倡导动手实践、先验证再行动的务实作风"),
        ("5", "清洗并自动转化（Pandas清洗 + EDA）", "培养严谨细致的科学精神与诚实守信的学术品格：数据处理有据可查、结论不造假"),
        ("6", "把数据讲成故事（可视化原则 + Plotly/Pyecharts）", "提升审美素养与叙事表达能力，学会用数据讲好中国金融发展故事"),
        ("7", "做出最小产品（Streamlit 原型）", "培育创新精神与创业意识；体验AI赋能个体的“一人公司”新形态，理解新质生产力"),
        ("8", "给产品加上智能解读（LangChain Chain + Prompt Template）", "了解我国人工智能自主创新进展，树立科技自立自强与负责任使用AI的意识"),
        ("9", "靠互评打磨一版（产品评审标准 + RAG选做）", "培养诚实守信、客观公正的品格（互评基于标准而非主观印象）；倡导知识共享、协作共赢"),
        ("10", "打磨到可上线（部署方案 + SQLite）", "培育精益求精的工匠精神与知行合一的实践观"),
    ]
    phase3 = [
        ("11", "产品上线（机器学习基础 + 训练测试划分 + 回归模型）", "服务国家数字经济战略，树立金融科技报国志向；部署成功即开始用户触达，体验服务社会的价值"),
        ("12", "改进模型并获客（特征工程 + 决策树/随机森林）", "理解普惠金融与服务实体经济的要求，让产品真正触达有需要的用户"),
        ("13", "对照大模型与传统分析（适用边界 + 神经网络基础）", "树立AI治理与负责任AI意识；培养辩证思维：理解新旧方法的边界与互补"),
        ("14", "用反馈迭代模型（多模型对比 + 交叉验证）", "践行以人民为中心的发展思想：用户价值优先，诚信经营，真诚倾听；培养严谨求实的科学精神：模型对比须公平（同划分/同指标）、选择须有证据"),
        ("15", "评估后嵌入产品（评估指标 + 有效性声明）", "强化规则意识与诚信合规：评估须有证据、结论可复核；进行数据安全与社会主义法治教育"),
    ]
    phase4 = [
        ("16", "公开路演（路演叙事 + 价值传达）", "营造创新创业文化，增强表达自信；把个人创新成果展示给真实受众，坚定“四个自信”"),
        ("17", "反思重构（知识框架重构 + DSR定位）", "引导学生把个人理想融入国家发展，立志为建设金融强国持续学习、贡献力量"),
    ]

    for title, rows in [
        ("Phase 1: Idea Stage（W1-3）— 发现问题、定义项目", phase1),
        ("Phase 2: MVP Stage（W4-10）— 构建最小可用产品", phase2),
        ("Phase 3: Launch Stage（W11-15）— 上线与迭代", phase3),
        ("Phase 4: Scale Stage（W16-17）— 展示与反思", phase4),
    ]:
        heading(doc, title, 3)
        make_table(
            doc,
            headers=["周次", "主题", "思政元素的融入和预期教学成效"],
            rows=rows,
            widths=[900, 3200, 4857],
            center_cols=(0,),
        )

    # ===== 四、考核方式 =====
    heading(doc, "四、考核方式", 1, bottom_border=True)
    body_para(doc, "采用“**总成绩 = 平时成绩(50分) + 个人项目(50分)**”结构。平时成绩含其他条目40分与协作互评10分。凡打分处一律采用百分制（0-100），评出的百分制分再折算为对应分数。")
    make_table(
        doc,
        headers=["考试形式", "考察内容", "考察方式", "分值"],
        rows=[
            ("平时 · 其他条目（形成性）", "出勤与参与、技能小练、阶段里程碑、反思与日志", "教师综合评分后折算（子项不细分）", "40%"),
            ("平时 · 协作互评", "组内互助贡献", "期末 360° 匿名互评", "10%"),
            ("个人项目（期末，终结性）", "产品质量、项目报告", "最终产品 + 公开路演（现场公网可访问） + 最终报告", "50%"),
        ],
        widths=[2100, 2300, 3350, 1207],
        center_cols=(3,),
    )

    # ===== 五、阅读材料 =====
    heading(doc, "五、阅读材料", 1, bottom_border=True)

    heading(doc, "（一）推荐教材", 2)
    body_para(doc, "《数据分析Python》，机械工业出版社，ISBN：978-7-111-77067-1，并结合符合要求的互联网参考资源。")

    heading(doc, "（二）参考教材（均可免费获取，课堂教学重点使用T1和T2，为了更好地提高数据分析能力，希望大家不断拓宽知识面）", 2)
    for pre, url in [
        ("T1《Python Data Science Handbook》，", "https://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/Index.ipynb"),
        ("T2《Introduction to Python for Econometrics, Statistics and Data Analysis》，Kevin Sheppard，", "https://www.kevinsheppard.com/Python_for_Econometrics"),
        ("《The elements of data analysis》，", "https://leanpub.com/datastyle"),
        ("《Natural Language Processing with Python》，", "http://www.nltk.org/book/"),
        ("Speech and Language Processing. ", "https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf"),
    ]:
        p = bullet(doc)
        add_rich(p, pre)
        add_hyperlink(p, url)
    p = bullet(doc)
    add_rich(p, "Hands-On Machine Learning with Scikit-Learn and TensorFlow, Aurélien Géron, O'Reilly Media, 2017")

    heading(doc, "（三）进一步阅读教材", 2)
    p = body_para(doc, "Python 基础相关教程：")
    for pre, url in [
        ("Learn Python the Hard Way: ", "http://learnpythonthehardway.org/book/"),
        ("Python Tutorial: ", "http://www.tutorialspoint.com/python/index.htm"),
        ("廖雪峰的官方网站：", "http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000"),
    ]:
        p = bullet(doc)
        add_rich(p, pre)
        add_hyperlink(p, url)
    for item in [
        "《图灵程序设计丛书：Python基础教程(第2版)》，人民邮电出版社",
        "《重视大脑的学习指南: Head First Python(中文版)》，中国电力出版社",
    ]:
        p = bullet(doc)
        add_rich(p, item)

    p = body_para(doc, "与数据分析相关Python教程：")
    for pre, url in [
        ("《Pandas Tutorial》: ", "http://pandas.pydata.org/pandas-docs/stable/index.html"),
        ("DATA 8：The Foundations of data science ", "http://data8.org/"),
        ("用Python玩转数据（南京大学 张莉）", "https://www.icourse163.org/course/NJU-1001571005"),
        ("Python数据分析与展示（北京理工大学 嵩天）", "https://www.icourse163.org/course/BIT-1001870002"),
        ("金融数据分析与可视化（微课课程）（西南财经大学 王俊、郑海超 等）", "https://www.xueyinonline.com/detail/244599764"),
    ]:
        p = bullet(doc)
        add_rich(p, pre)
        add_hyperlink(p, url)
    p = bullet(doc)
    add_rich(p, "Wes McKinney,《利用Python进行数据分析（Python for Data Analysis）》, O'Reilly Media")

    heading(doc, "（四）AI工具栈与项目方法资源（本学期新增重点）", 2)
    for pre, url in [
        ("PBLWorks - What is PBL：", "https://www.pblworks.org/what-is-pbl"),
        ("LangChain 官方文档：", "https://python.langchain.com/"),
        ("Streamlit 官方文档：", "https://docs.streamlit.io/"),
    ]:
        p = bullet(doc)
        add_rich(p, pre)
        add_hyperlink(p, url)
    for item in [
        "Andrew Ng - How to Build Your Career in AI（项目筛选框架）",
        "The Founder's Playbook: Building an AI-Native Startup（四阶段创业生命周期）",
        "The Minimalist Entrepreneur（社区先行、手动流程先行、先卖再建）",
        "设计科学研究（DSR）方法论文献：Hevner et al. (2004)、Hevner (2007)、Peffers et al. (2007)、Gregor & Hevner (2013)、Larsen et al. (2025)",
    ]:
        p = bullet(doc)
        add_rich(p, item)
    p = bullet(doc)
    add_rich(p, "视频资料库（超星学习通平台 ")
    add_hyperlink(p, "https://v8.chaoxing.com/")
    add_rich(p, "）：网络爬虫/词语切分/文本量化/NumPy/Pandas/数据可视化/数据库/机器学习/朴素贝叶斯/SVM/决策树随机森林/深度学习/自然语言技术系列视频的按需资源目录，含逐周映射与使用模式（课前预习/安排自学/按需补缺/进阶拓展/课后自愿）")
    p = bullet(doc)
    add_rich(p, "课程内文档：`data-analysis-teaching-plan.md`（总方案）、`knowledge-map.md`（知识地图）、`milestones.md`（里程碑）、`rubric.md`（评分标准）、`project-selection-guide.md`(选题指南)、各周 `weeks/weekXX/plan.md`（周计划，每周唯一准绳）")

    # 文档属性
    cp = doc.core_properties
    cp.title = "金融数据分析与可视化 教学实施方案"
    cp.author = "郑海超"
    cp.subject = "2026—2027学年第1学期"

    doc.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    build()
