# -*- coding: utf-8 -*-
"""
生成《个人项目开题报告》Word 模板（学生填写版）
课程：数据分析与可视化 · Week 07
用法：python _gen_docx.py
输出：开题报告-姓名-学号.docx
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------- 配色与字体 ----------------
C_MAIN = RGBColor(0x1F, 0x38, 0x64)      # 主色 深蓝
C_ACC = RGBColor(0x2E, 0x5C, 0x8A)       # 辅色 蓝
C_TEXT = RGBColor(0x1A, 0x1A, 0x1A)      # 正文 近黑
C_HINT = RGBColor(0x50, 0x50, 0x50)      # 提示 灰
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

CN_BODY = '宋体'
CN_HEAD = '黑体'
EN_FONT = 'Times New Roman'
CN_HINT = '楷体'

FILL_HEAD = '1F3864'   # 表头底色
FILL_ALT = 'EEF2F8'    # 表格隔行底色
FILL_HINT = 'F5F7FA'   # 提示框底色
BAR_HINT = '2E5C8A'    # 提示框左侧色条

PPR_ORDER = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl',
             'numPr', 'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens',
             'kinsoku', 'wordWrap', 'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN',
             'bidi', 'adjustRightInd', 'snapToGrid', 'spacing', 'ind', 'contextualSpacing',
             'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection', 'textAlignment',
             'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']


def _tag(el):
    return el.tag.split('}')[-1]


def _insert_ppr(pPr, el):
    for ch in list(pPr):
        if _tag(ch) == _tag(el):
            pPr.remove(ch)
    idx = PPR_ORDER.index(_tag(el))
    pos = len(pPr)
    for i, ch in enumerate(pPr):
        t = _tag(ch)
        if t in PPR_ORDER and PPR_ORDER.index(t) > idx:
            pos = i
            break
    pPr.insert(pos, el)


def _shade(el, fill):
    """给段落(w:p)或单元格(w:tc)加底纹"""
    pr = el.get_or_add_pPr() if _tag(el) == 'p' else el.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    if _tag(el) == 'p':
        _insert_ppr(pr, shd)
    else:
        for ch in list(pr):
            if _tag(ch) == 'shd':
                pr.remove(ch)
        pr.append(shd)


def _left_bar(p, color=BAR_HINT, sz='18'):
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), sz)
    left.set(qn('w:space'), '6')
    left.set(qn('w:color'), color)
    pBdr.append(left)
    _insert_ppr(pPr, pBdr)


def _cell_border(cell, edges=('bottom',), color='BFBFBF', sz='6'):
    tcPr = cell._tc.get_or_add_tcPr()
    for ch in list(tcPr):
        if _tag(ch) == 'tcBorders':
            tcPr.remove(ch)
    borders = OxmlElement('w:tcBorders')
    for e in edges:
        b = OxmlElement('w:' + e)
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:color'), color)
        b.set(qn('w:space'), '0')
        borders.append(b)
    tcPr.append(borders)


def _style_font(style, cn, en, size=None, bold=None, color=None):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    rf.set(qn('w:ascii'), en)
    rf.set(qn('w:hAnsi'), en)
    rf.set(qn('w:eastAsia'), cn)
    if size is not None:
        sz = rpr.find(qn('w:sz'))
        if sz is None:
            sz = OxmlElement('w:sz')
            rpr.append(sz)
        sz.set(qn('w:val'), str(int(size * 2)))
        szCs = rpr.find(qn('w:szCs'))
        if szCs is None:
            szCs = OxmlElement('w:szCs')
            rpr.append(szCs)
        szCs.set(qn('w:val'), str(int(size * 2)))
    if bold is not None:
        rpr.find(qn('w:b'))
        b = rpr.find(qn('w:b'))
        if b is None:
            b = OxmlElement('w:b')
            rpr.append(b)
        b.set(qn('w:val'), '1' if bold else '0')
    if color is not None:
        for ch in list(rpr):
            if _tag(ch) == 'color':
                rpr.remove(ch)
        c = OxmlElement('w:color')
        c.set(qn('w:val'), '%02X%02X%02X' % (color[0], color[1], color[2]))
        rpr.append(c)


def _run(run, cn=CN_BODY, en=EN_FONT, size=12, bold=False, color=None, italic=False):
    run.font.name = en
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    rf.set(qn('w:ascii'), en)
    rf.set(qn('w:hAnsi'), en)
    rf.set(qn('w:eastAsia'), cn)
    if color is not None:
        run.font.color.rgb = color
    return run


# ---------------- 段落构件 ----------------
def body(doc, text, size=12, indent=True, space_after=6, align=None, bold=False, color=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if align is not None:
        p.alignment = align
    _run(p.add_run(text), size=size, bold=bold, color=color)
    return p


def bullet(doc, text, size=11.5, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(0.9 + 0.6 * level)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(3)
    _run(p.add_run(text), size=size)
    return p


def h1(doc, text, page_break=False):
    if page_break:
        doc.add_page_break()
    p = doc.add_paragraph(style='Heading 1')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(10)
    _run(p.add_run(text), cn=CN_HEAD, en=EN_FONT, size=18, bold=True, color=C_MAIN)
    return p


def h2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    _run(p.add_run(text), cn=CN_HEAD, en=EN_FONT, size=14, bold=True, color=C_MAIN)
    return p


def h3(doc, text):
    p = doc.add_paragraph(style='Heading 3')
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    _run(p.add_run(text), cn=CN_HEAD, en=EN_FONT, size=12.5, bold=True, color=C_ACC)
    return p


def hint(doc, text, label='提示'):
    """灰色提示框：写什么 / 怎么写 / 示例"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.3)
    pf.right_indent = Cm(0.2)
    pf.space_before = Pt(4)
    pf.space_after = Pt(8)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.25
    _shade(p._p, FILL_HINT)
    _left_bar(p)
    _run(p.add_run(label + '：'), cn=CN_HINT, size=10.5, bold=True, color=C_ACC)
    _run(p.add_run(text), cn=CN_HINT, size=10.5, color=C_HINT)
    return p


def ask(doc, text):
    """本节要回答的核心问题"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(6)
    pf.left_indent = Cm(0.2)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    _shade(p._p, 'FFF8E7')
    _left_bar(p, color='C8963E')
    _run(p.add_run('本节要回答的核心问题：'), cn=CN_HEAD, size=11, bold=True, color=RGBColor(0xA0, 0x6A, 0x1B))
    _run(p.add_run(text), cn=CN_BODY, size=11, bold=True, color=RGBColor(0x7A, 0x55, 0x15))
    return p


def check(doc, items):
    """自检清单"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.left_indent = Cm(0.2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    _shade(p._p, 'F2F8F4')
    _left_bar(p, color='4E8A5B')
    _run(p.add_run('自检（完成后逐条打勾）：'), cn=CN_HEAD, size=10.5, bold=True,
         color=RGBColor(0x3C, 0x6B, 0x47))
    for it in items:
        r = p.add_run()
        r.add_break()
        _run(r, cn=CN_BODY, size=10.5, color=RGBColor(0x40, 0x40, 0x40))
        _run(p.add_run('□ ' + it), cn=CN_BODY, size=10.5, color=RGBColor(0x40, 0x40, 0x40))
    return p


def fill_line(doc, label, width_chars=26):
    """填空下划线行"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(10)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    _run(p.add_run(label), cn=CN_HEAD, size=12, bold=True, color=C_MAIN)
    _run(p.add_run('　' + '＿' * width_chars), cn=CN_BODY, size=12, color=C_TEXT)
    return p


# ---------------- 表格 ----------------
def table(doc, headers, rows, widths=None, font_size=10, alt=True, head_fill=FILL_HEAD):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    hdr = t.rows[0]
    for i, htxt in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        _run(p.add_run(htxt), cn=CN_HEAD, size=font_size, bold=True, color=C_WHITE)
        _shade(cell._tc, head_fill)
        cell.vertical_alignment = 1
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            cell = cells[ci]
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            _run(p.add_run(str(val)), cn=CN_BODY, size=font_size)
            cell.vertical_alignment = 1
            if alt and ri % 2 == 1:
                _shade(cell._tc, FILL_ALT)
    if widths:
        # 页面可用宽度 = 21.0 - 2.6*2 = 15.8 cm，超出时按比例缩放
        usable = 15.8
        total = sum(widths)
        if total > usable:
            widths = [w * usable / total for w in widths]
        tblPr = t._tbl.tblPr
        for ch in list(tblPr):
            if _tag(ch) == 'tblLayout':
                tblPr.remove(ch)
        layout = OxmlElement('w:tblLayout')
        layout.set(qn('w:type'), 'fixed')
        tblPr.append(layout)
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    return t


def add_toc(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    f1 = OxmlElement('w:fldChar')
    f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText')
    it.set(qn('xml:space'), 'preserve')
    it.text = r'TOC \o "1-3" \h \z \u'
    f2 = OxmlElement('w:fldChar')
    f2.set(qn('w:fldCharType'), 'separate')
    t = OxmlElement('w:t')
    t.text = '（在 Word 中右键此处 → "更新域"，自动生成目录）'
    f3 = OxmlElement('w:fldChar')
    f3.set(qn('w:fldCharType'), 'end')
    for el in (f1, it, f2, t, f3):
        run._r.append(el)
    _run(run, cn=CN_BODY, size=11, color=C_HINT)
    return p


def setup_page(doc):
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.6)
    sec.right_margin = Cm(2.6)
    sec.top_margin = Cm(2.4)
    sec.bottom_margin = Cm(2.2)
    sec.header_distance = Cm(1.2)
    sec.footer_distance = Cm(1.2)

    # 页眉
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _run(hp.add_run('数据分析与可视化 · 个人项目开题报告（模板）'), cn=CN_BODY, size=9, color=C_HINT)
    hpPr = hp._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single')
    b.set(qn('w:sz'), '4')
    b.set(qn('w:space'), '2')
    b.set(qn('w:color'), 'BFBFBF')
    pbdr.append(b)
    _insert_ppr(hpPr, pbdr)

    # 页脚页码
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = _run(fp.add_run('— '), cn=CN_BODY, size=9, color=C_HINT)
    r = fp.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'PAGE'
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
    for el in (f1, it, f2):
        r._r.append(el)
    _run(r, cn=CN_BODY, size=9, color=C_HINT)
    _run(fp.add_run(' —'), cn=CN_BODY, size=9, color=C_HINT)


def setup_styles(doc):
    st = doc.styles['Normal']
    _style_font(st, CN_BODY, EN_FONT, size=12)
    st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    st.paragraph_format.space_after = Pt(6)
    for name, cn, sz, color in (('Heading 1', CN_HEAD, 18, C_MAIN),
                                ('Heading 2', CN_HEAD, 14, C_MAIN),
                                ('Heading 3', CN_HEAD, 12.5, C_ACC)):
        s = doc.styles[name]
        _style_font(s, cn, EN_FONT, size=sz, bold=True,
                    color=(color[0], color[1], color[2]))


# =========================================================
#  文档正文
# =========================================================
def build():
    doc = Document()
    setup_page(doc)
    setup_styles(doc)

    # ---------- 封面 ----------
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p.add_run('数据分析与可视化'), cn=CN_HEAD, size=16, bold=True, color=C_ACC)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    _run(p.add_run('个人项目开题报告'), cn=CN_HEAD, size=32, bold=True, color=C_MAIN)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    _run(p.add_run('Proposal for the Individual Data-Analysis Project'),
         en='Times New Roman', size=12, italic=True, color=C_HINT)

    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p.add_run('─── 课 后 作 业 · Week 07 ───'), cn=CN_BODY, size=12, color=C_ACC)

    for _ in range(3):
        doc.add_paragraph()

    # 封面信息表（无框 + 底部下划线）
    info = [('题　　目', 5), ('姓　　名', 3), ('学　　号', 3),
            ('专业 / 班级', 4), ('指导教师', 3), ('提交日期', 3)]
    t = doc.add_table(rows=0, cols=2)
    for label, _ in info:
        row = t.add_row()
        c0, c1 = row.cells
        c0.width = Cm(3.0)
        c1.width = Cm(11.0)
        c0.text = ''
        pp = c0.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pp.paragraph_format.space_after = Pt(12)
        _run(pp.add_run(label + '：'), cn=CN_HEAD, size=12.5, bold=True, color=C_MAIN)
        c1.text = ''
        pp = c1.paragraphs[0]
        pp.paragraph_format.space_after = Pt(12)
        _run(pp.add_run('　'), size=12.5)
        _cell_border(c1, edges=('bottom',), color='808080', sz='6')
        _cell_border(c0, edges=(), color='FFFFFF', sz='0')

    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p.add_run('西南财经大学'), cn=CN_HEAD, size=14, bold=True, color=C_MAIN)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p.add_run('2026 – 2027 学年　第一学期'), cn=CN_BODY, size=12, color=C_TEXT)

    # ---------- 使用说明 + 目录 ----------
    h1(doc, '本模板使用说明', page_break=True)
    hint(doc, '本文件是"可直接填写"的开题报告底稿。正文中的灰色提示框、橙色"核心问题"框、绿色"自检"框都是给你的写作脚手架——'
              '正式提交前请全部删除，只保留你自己写的内容与章节标题。')
    body(doc, '三类辅助标记的含义：')
    table(doc, ['标记', '作用', '提交时的处理'],
          [['灰色「提示」框', '告诉你这一节写什么、怎么写，并给出示例句式', '删除'],
           ['橙色「核心问题」框', '本节必须回答清楚的那个问题，回答不了就说明还没想透', '删除（但内容必须写进正文）'],
           ['绿色「自检」框', '写完后的逐条打勾清单', '删除'],
           ['表格中的示例行', '灰色斜体标注的示范内容，告诉你该填成什么样', '替换为你自己的真实内容']],
          widths=[3.4, 8.0, 4.4], font_size=10)

    body(doc, '建议的写作顺序（不要从头写到尾）：')
    bullet(doc, '① 先写第 2 章"研究动机"——把"我要解决谁的什么问题"一句话说清楚，后面所有章节都由它推导出来。')
    bullet(doc, '② 再写第 6 章"数据方案"——先确认数据真的拿得到、拿得起，方案才不是空中楼阁。')
    bullet(doc, '③ 然后写第 4 章"解决方案设计"和第 5 章"评估指标"，这两章互为镜像：指标要能验证方案。')
    bullet(doc, '④ 接着写第 3 章"项目调研"——用证据支撑第 2 章的动机。')
    bullet(doc, '⑤ 最后写第 7 章"风险评估"和第 8 章"参考资料"。')
    hint(doc, '篇幅不是靠凑字堆出来的。10 页的合理构成是：有证据（调研）、有设计（方案）、有对照（评估指标）、'
              '有退路（风险与不做清单）。空话写得再多也不算数。')

    h1(doc, '目　录', page_break=False)
    add_toc(doc)

    # ================= 第一部分 作业要求 =================
    h1(doc, '第一部分　作业要求', page_break=True)
    ask(doc, '这次作业到底要交什么？老师按什么标准看？')

    h2(doc, '一、作业目标')
    body(doc, '开题报告回答的是一个问题：你的个人项目值不值得做、能不能做完。它不是项目总结，而是项目开工前的自我论证——'
              '你要用证据说明"这个问题真实存在"，用设计说明"我有办法解决"，用指标说明"做完了能验证"，'
              '用风险清单说明"万一出事我有退路"。')
    body(doc, '对应到本课程的语境：你已经完成了 W4 的数据获取与清洗、W6 的可视化方案设计、W7 的 Streamlit 原型搭建。'
              '开题报告要把这些散落的成果收拢成一个有头有尾的项目叙事。')

    h2(doc, '二、内容八项与篇幅建议')
    body(doc, '下表是作业的硬性清单，八项缺一不可。建议篇幅按"正文 10 页以上"（约 4000–5000 字）分配，可按需微调。')
    table(doc, ['序号', '内容项', '必须回答的核心问题', '建议篇幅'],
          [['1', '封面', '题目、姓名、学号是否齐全', '1 页'],
           ['2', '研究动机', '为什么要做？解决谁的什么问题？', '1 – 1.5 页'],
           ['3', '项目调研', '凭什么说这个问题真实存在、值得做？', '1.5 – 2 页'],
           ['4', '预期解决方案设计', '做成什么样？为什么选这套技术？', '1.5 – 2 页'],
           ['5', '评估方法与评估指标', '做完之后，怎么证明它有效？', '1 – 1.5 页'],
           ['6', '数据方案', '数据从哪来、有哪些字段、怎么更新、多少钱？', '1 – 1.5 页'],
           ['7', '项目风险评估', '什么会出岔子？出岔子了怎么办？不做什么？', '1.5 – 2 页'],
           ['8', '参考资料列表', '依据来自哪里？正文引用是否一一对应？', '0.5 – 1 页']],
          widths=[1.3, 3.6, 7.7, 3.2], font_size=10)

    h2(doc, '三、提交要求')
    body(doc, '提交规范如下，提交前逐条核对：')
    table(doc, ['项目', '要求'],
          [['文件格式', 'Microsoft Word 文档（.docx）'],
           ['篇幅', '正文 10 页以上（封面与目录不计入）'],
           ['文件命名', '开题报告-姓名-学号.docx　——请把"姓名""学号"替换为你自己的真实姓名与学号'],
           ['截止时间', '2026 年 10 月 30 日（周五）晚上 20:00'],
           ['提交方式', '按课程群通知的学习平台 / 邮箱提交，逾期按课程规定处理'],
           ['语言与排版', '中文撰写；正文宋体小四、1.5 倍行距；标题层级清晰；图表有编号与标题'],
           ['引用规范', '正文用（作者，年份）格式引用；文末列出全部参考文献；文中有引、文末有列、一一对应']],
          widths=[3.2, 12.6], font_size=10)

    h2(doc, '四、评分关注点（老师重点看什么）')
    table(doc, ['维度', '看什么', '常见失分'],
          [['问题是否真实', '动机有具体场景与证据，不是"我觉得挺有意思"', '泛泛而谈，没有具体用户与场景'],
           ['调研是否扎实', '三类调研有机组织，而非简单罗列', '只做大模型的"一键生成调研"，无人证与文献'],
           ['设计是否具体', '功能、数据流、技术选型都有明确决定', '只写"用 Python 做一个系统"，无技术选型理由'],
           ['指标是否可操作', '指标有定义、有算法、有目标值、有数据来源', '写"提升用户体验"这类不可测量的指标'],
           ['数据是否落地', '数据集已落盘，字段清晰，成本可控', '数据尚未获取，且未说明获取路径'],
           ['风险是否诚实', '逐条列出并给出可执行的应对与降级', '风险写成"我会努力克服"，无具体动作'],
           ['引用是否规范', '文中有引、文末有列、一一对应', '只有文末列表，正文无一处引用']],
          widths=[2.8, 7.4, 5.6], font_size=10)

    h2(doc, '五、提交前格式自检清单')
    check(doc, [
        '文件已另存为 .docx，文件名已改为 开题报告-姓名-学号.docx',
        '正文（不含封面、目录、本模板说明）达到 10 页以上',
        '八项内容齐全，顺序与要求一致',
        '所有灰色提示框、核心问题框、自检框已删除',
        '正文至少出现 5 处（作者，年份）格式的引用',
        '文末参考资料列表覆盖了正文出现的每一个引用，无遗漏、无多余',
        '所有表格、图片都有编号与标题（如表 3-1、图 4-2）',
        '完成了一次通读，无错别字、无残留的占位文字',
    ])

    # ================= 第二部分 正文框架 =================
    h1(doc, '第二部分　开题报告正文（照此框架填写）', page_break=True)
    hint(doc, '以下第 1 – 8 章即正式报告的正文框架。章节编号与标题可直接使用；每章下的小节标题可按你的项目实际调整，'
              '但"核心问题"框中提出的问题必须在正文中得到明确回答。')

    # ---- 第 1 章 ----
    h2(doc, '第 1 章　封面')
    ask(doc, '（封面已在本文档第 1 页，填写题目、姓名、学号即可，此处无需另写内容。）')
    body(doc, '题目命名建议采用「对象 + 方法/视角 + 场景」的结构，避免过大过空。')
    table(doc, ['不推荐的题目', '推荐的题目', '差异'],
          [['股票分析系统', '基于 Tushare 与 Streamlit 的 A 股个股技术面自助诊断工具', '明确了数据、技术、对象与形态'],
           ['校园数据可视化', '面向本校学生的食堂人流高峰可视化与错峰就餐建议工具', '明确了用户、数据、价值'],
           ['电影数据分析', '豆瓣电影评分与口碑背离现象的识别与可视化分析', '明确了分析切入的现象']],
          widths=[3.6, 8.2, 4.0], font_size=10)

    # ---- 第 2 章 ----
    h2(doc, '第 2 章　研究动机')
    ask(doc, '你要解决谁的什么问题？这个问题为什么现在值得解决？解决了有什么意义？')

    h3(doc, '2.1　研究背景')
    body(doc, '〈此处写 300–500 字。从一个可观察的真实现象或你亲身经历的场景切入，不要从"随着大数据时代的到来"写起。〉')
    hint(doc, '写什么：你注意到的事实或反常现象；它发生的场景与频率；现有手段为什么没解决。'
              '怎么写：现象 → 数据/事实佐证 → 现有方案的不足。至少引用 1 条可核查的资料（行业报告、统计数据、论文），'
              '格式如"……日均活跃用户已超过 X 万（CNNIC, 2025）"。示例句式："我在 XX 场景中反复遇到 XX 问题，'
              '现有工具 A 只能做到 XX，而 B 需要 XX 成本，因此……"')

    h3(doc, '2.2　问题陈述')
    body(doc, '〈此处用一段话把问题说死。建议套用下面的句式，填完后再润色。〉')
    hint(doc, '推荐句式：对于【目标用户】，他们想要【核心需求】，但现有方式存在【具体障碍】；'
              '本项目拟做【产品形态】，提供【核心价值】，因为【与现有方案的差异点】。'
              '要求：目标用户必须具体到可访谈（如"本校大三学生"而非"年轻人"）；障碍必须是你调研中真实听到的，不是想象的。')

    h3(doc, '2.3　研究意义')
    body(doc, '〈分三个层面各写 100–150 字：对用户的意义、对本课程/学科的意义、对我个人的意义。〉')
    hint(doc, '对用户：省了什么时间、降低了什么成本、避免了什么错误——能量化就量化。'
              '对学科：你的分析视角或可视化方法对同类问题有无可复用之处。'
              '对个人：与你的专业方向、职业规划的关系，以及想在本项目中刻意练就的能力。')

    check(doc, [
        '目标用户具体到"能找到人访谈"的程度',
        '问题陈述用一句话说清了"谁 + 什么障碍 + 什么价值"',
        '背景部分至少有一处（作者，年份）引用',
        '没有出现"随着大数据时代的到来"这类空话',
    ])

    # ---- 第 3 章 ----
    h2(doc, '第 3 章　项目调研')
    ask(doc, '凭什么说这个问题真实存在？别人做到哪一步了？你的切入点与他们的差别在哪？')
    hint(doc, '三类调研不要求全做，但做了的必须"有机组织"在一起，而不是并列罗列三块内容。'
              '推荐主线：访谈证据定痛点（确认需求真实）→ 文献定参照（知道别人做到哪）→ 大模型辅助扫描补盲区（查漏）。'
              '每一步的结论都要指向下一步，形成一条推理链。')

    h3(doc, '3.1　调研设计与方法概述')
    body(doc, '〈用 200 字说明你做了哪几类调研、各自回答什么问题、彼此如何衔接。配一张调研路径表。〉')
    table(doc, ['调研类型', '回答的问题', '具体做法', '样本/规模'],
          [['线下调研', '痛点是否真实？', '〈如：半结构化访谈 5 人〉', '〈5 人〉'],
           ['文献调研', '别人做到哪一步？', '〈如：CNKI 检索 + 滚雪球〉', '〈8 篇〉'],
           ['大模型辅助调研', '有哪些我没想到的盲区？', '〈如：多轮提问 + 交叉验证〉', '〈3 轮〉']],
          widths=[2.8, 3.6, 6.4, 3.0], font_size=10)

    h3(doc, '3.2　线下调研（访谈 / 观察）')
    body(doc, '〈说明访谈对象与选取理由、访谈提纲、关键发现。至少给出 3 条可直接引用的原始证据。〉')
    hint(doc, '关键发现的写法：事实 + 出处。例："8 位受访者中有 6 位表示「看盘时最困扰的是指标太多不知道看哪个」（受访者 C，2026）。"'
              '访谈提纲（3–5 个问题）要作为附录或表格列出，体现你的提问是有设计的，不是闲聊。'
              '没做访谈的同学可用问卷调查、实地观察、公开评论区文本分析替代，但必须说清方法与样本。')

    h3(doc, '3.3　文献调研')
    body(doc, '〈说明检索策略（数据库、检索式、筛选标准），然后综述 3–5 篇核心文献，最后指出研究空白。〉')
    hint(doc, '综述不是摘要拼接，要按"主题"或"方法"组织，并做比较。推荐句式：'
              '"A（2020）从 X 角度解决了 Y，但未考虑 Z；B（2022）在 Z 上做了改进，但其数据仅覆盖……"'
              '最后必须落到一句"因此，在【你的场景】下，尚缺乏……的研究"——这就是你的立足点。'
              '检索式要真实可复现，如：CNKI，主题 = ("可视化" AND "个人理财")，时间 2020–2026，筛选后余 12 篇。')

    h3(doc, '3.4　大模型辅助调研')
    body(doc, '〈说明你向大模型提了什么问题、得到什么线索、如何交叉验证、补上了哪些盲区。〉')
    hint(doc, '大模型是"扫描仪"不是"判官"。写法要点：① 给出你的提问策略（角色 + 任务 + 约束 + 要求列出来源）；'
              '② 说明你如何验证它的输出（回到官方文档/原始文献核对，或直接说"该说法未找到原始出处，暂不采纳"）；'
              '③ 明确它帮你补上了哪几个你原本没想到的方向。'
              '注意：大模型给出的文献可能不存在，凡未经核实的，一律不得进入第 8 章的参考资料列表。')

    h3(doc, '3.5　调研结论')
    body(doc, '〈用一张表把"调研前假设"与"调研后结论"对照，明确哪些被证实、哪些被修正、哪些被放弃。〉')
    table(doc, ['调研前的假设', '调研结果', '对本项目的决策'],
          [['〈假设 1〉', '〈已证实 / 已修正 / 已否定〉', '〈保留该需求并优先实现〉'],
           ['〈假设 2〉', '〈已修正为……〉', '〈调整功能定义〉'],
           ['〈假设 3〉', '〈已否定：用户其实不需要〉', '〈移入「不做」清单〉']],
          widths=[4.6, 6.0, 5.2], font_size=10)

    check(doc, [
        '三类调研之间有明确的推理链，不是三块并列的内容',
        '至少 3 条来自真实访谈/观察的原始证据',
        '文献综述做了横向比较，并指出了研究空白',
        '大模型的输出经过核实，未核实的未进入参考文献',
    ])

    # ---- 第 4 章 ----
    h2(doc, '第 4 章　预期解决方案设计')
    ask(doc, '你要做成什么样的东西？用户怎么用它？为什么选这套技术而不是别的？')

    h3(doc, '4.1　方案总体描述')
    body(doc, '〈先用一句话说清产品形态，再用一段典型使用流程（用户故事）把它展开：谁、在什么场景、做了什么、得到了什么。〉')
    hint(doc, '示例："本项目是一个基于 Streamlit 的网页应用。用户打开页面后，在侧栏选择股票代码与时间区间，'
              '页面主区域立即展示该区间的量价走势与技术指标；点击「生成解读」按钮后，系统调用大模型输出一段结构化解读。"'
              '避免写成功能清单——先讲一个完整的故事，再拆功能。')

    h3(doc, '4.2　核心功能清单')
    body(doc, '〈列出功能并标注优先级。P0 = 没有它项目就不成立；P1 = 有则更好；P2 = 锦上添花。〉')
    table(doc, ['编号', '功能', '优先级', '说明', '对应第 5 章指标'],
          [['F1', '〈数据加载与缓存〉', 'P0', '〈……〉', '〈加载耗时〉'],
           ['F2', '〈核心分析计算〉', 'P0', '〈……〉', '〈准确率〉'],
           ['F3', '〈主可视化图表〉', 'P0', '〈……〉', '〈任务完成率〉'],
           ['F4', '〈交互筛选控件〉', 'P1', '〈……〉', '〈—〉'],
           ['F5', '〈结果导出 / 分享〉', 'P2', '〈……〉', '〈—〉']],
          widths=[1.3, 3.8, 1.6, 5.4, 3.7], font_size=10)

    h3(doc, '4.3　系统架构与数据流')
    body(doc, '〈画出或描述"数据加载 → 清洗 → 分析 → 可视化 → 交互"的闭环，并说明每个环节的输入输出。〉')
    hint(doc, '至少用文字描述清楚五段链路，若能画图更佳（图要有编号与标题，如图 4-1 系统数据流图）。'
              '关键是要体现"闭环"：不是跑一次脚本出一张图就结束，而是用户改变输入后能重新计算并刷新结果。'
              '这一点是 W7 原型与 W4/W5 作业的本质区别——Notebook 是实验室，产品是店面。')

    h3(doc, '4.4　技术选型与选择理由')
    body(doc, '〈逐个环节说明候选方案、最终选择与理由。这是本章最有分量的一节，务必写足。〉')
    table(doc, ['环节', '候选方案', '最终选择', '选择理由', '为什么放弃其他'],
          [['应用框架', 'Streamlit / Gradio / Flask+前端', '〈Streamlit〉', '〈纯 Python、元件齐全、30 行可跑起来、本课程后续项目可复用〉', '〈Gradio 更适合模型演示；Flask+前端工作量超出单人力度〉'],
           ['数据来源', 'Tushare / AkShare / 爬虫 / 手工整理', '〈Tushare Pro〉', '〈接口稳定、字段规范、有免费额度〉', '〈爬虫维护成本高且有合规风险〉'],
           ['分析与建模', 'Pandas 统计 / 机器学习模型 / 大模型 API', '〈……〉', '〈……〉', '〈……〉'],
           ['可视化', 'Matplotlib / Plotly / ECharts / 原生 st.chart', '〈……〉', '〈……〉', '〈……〉'],
           ['部署方式', '本地运行 / Streamlit Cloud / 服务器', '〈……〉', '〈……〉', '〈……〉']],
          widths=[2.2, 3.6, 2.4, 4.6, 3.0], font_size=9)
    hint(doc, '判断标准：理由必须来自你项目的约束（时间、能力、成本、维护量），而不是"别人都在用""老师推荐"。'
              '被放弃的方案也要写清为什么——这恰恰体现你做过比较。'
              '若你选择了课堂上没讲的技术，请额外说明你的学习成本与兜底方案（并写入第 7 章风险表）。')

    h3(doc, '4.5　与已有方案的差异')
    body(doc, '〈把你的方案与调研中发现的现有方案做对比，明确差异化。〉')
    table(doc, ['对比维度', '现有方案 A', '现有方案 B', '本项目'],
          [['目标用户', '〈……〉', '〈……〉', '〈……〉'],
           ['数据覆盖', '〈……〉', '〈……〉', '〈……〉'],
           ['核心能力', '〈……〉', '〈……〉', '〈……〉'],
           ['使用门槛', '〈……〉', '〈……〉', '〈……〉']],
          widths=[3.0, 4.2, 4.2, 4.4], font_size=10)

    check(doc, [
        '有一段完整的用户使用流程描述（不是功能罗列）',
        '功能清单标注了 P0/P1/P2 优先级',
        '数据流闭环（加载→分析→可视化→交互）表述清楚',
        '技术选型逐环节给出了理由与放弃理由，理由来自项目约束',
    ])

    # ---- 第 5 章 ----
    h2(doc, '第 5 章　解决方案评估方法与评估指标')
    ask(doc, '做完之后，用什么方法、什么指标、跟什么基线比，来判断它真的有效？')
    hint(doc, '指标要"可操作"：有明确定义、有计算公式、有目标值、有数据来源。'
              '"提升用户体验""界面美观"这类不可测量的表述不计入指标。'
              '同时要有基线——没有对照的指标等于没有指标。')

    h3(doc, '5.1　评估思路')
    body(doc, '〈说明由谁评（自己 / 目标用户 / 专家）、在什么时间点评、用什么方式评。〉')
    bullet(doc, '自评：功能是否按设计跑通、指标是否达到目标值。')
    bullet(doc, '用户评：邀请 X 位目标用户完成 Y 项任务，观察与记录。')
    bullet(doc, '对照评：与人工方式 / 现有工具 / 简单基线做比较。')

    h3(doc, '5.2　用户侧评估方法')
    body(doc, '〈说明可用性测试或问卷的具体设计：任务、样本量、记录什么、怎么判定成功。〉')
    table(doc, ['任务', '操作步骤', '成功判定标准', '记录数据'],
          [['任务 1：〈……〉', '〈3–5 步〉', '〈在 X 分钟内独立完成且结果正确〉', '完成时长 / 是否求助 / 主观难度 1–5 分'],
           ['任务 2：〈……〉', '〈……〉', '〈……〉', '〈……〉']],
          widths=[3.6, 4.0, 4.6, 3.6], font_size=10)
    hint(doc, '样本量：5 位用户足以发现 80% 以上的可用性问题（Nielsen, 2000）。'
              '问卷若使用成熟量表（如 SUS 系统可用性量表），须在正文引用出处并在第 8 章列出。')

    h3(doc, '5.3　技术侧量化指标')
    body(doc, '〈按准确性、效率、覆盖与稳定性四类给出指标，每张表都要有目标值。〉')
    table(doc, ['类别', '指标', '定义与计算方式', '目标值', '数据来源'],
          [['准确性', '〈如：方向判断准确率〉', '正确次数 / 总次数', '≥ 〈60%〉', '〈回测日志〉'],
           ['准确性', '〈如：数值预测 MAE〉', 'mean(|预测值 − 真实值|)', '≤ 〈…〉', '〈回测日志〉'],
           ['效率', '〈如：首屏加载耗时〉', '从请求到图表渲染完成的秒数', '≤ 〈3 秒〉', '〈埋点计时〉'],
           ['效率', '〈如：单次任务完成时长〉', '用户完成核心任务的中位时长', '≤ 〈…〉', '〈可用性测试记录〉'],
           ['覆盖', '〈如：数据覆盖率〉', '成功获取数据的标的数 / 目标标的数', '≥ 〈95%〉', '〈数据管道日志〉'],
           ['稳定性', '〈如：异常请求占比〉', '失败请求 / 总请求', '≤ 〈2%〉', '〈运行日志〉']],
          widths=[1.8, 3.4, 4.6, 2.6, 4.2], font_size=9)

    h3(doc, '5.4　基线与对照')
    body(doc, '〈明确"跟什么比"。没有基线，指标数字无意义。〉')
    table(doc, ['指标', '基线（现有方式）', '本项目目标', '提升幅度'],
          [['〈如：完成一次分析所需时间〉', '〈人工整理约 30 分钟〉', '〈≤ 3 分钟〉', '〈约 10 倍〉'],
           ['〈如：信息获取的完整性〉', '〈……〉', '〈……〉', '〈……〉']],
          widths=[4.4, 4.4, 4.0, 3.0], font_size=10)

    h3(doc, '5.5　评估计划')
    body(doc, '〈说明在什么时间点做哪一次评估，以及评估结果如何反哺迭代。〉')
    table(doc, ['时间节点', '评估内容', '评估方式', '产出'],
          [['〈W8〉', '原型可用性', '〈5 人任务测试〉', '〈问题清单 + 修改优先级〉'],
           ['〈W11〉', '核心功能达标情况', '〈指标自测〉', '〈指标实测表〉'],
           ['〈W14〉', '整体有效性', '〈用户复评 + 基线对照〉', '〈最终评估结论〉']],
          widths=[2.6, 4.2, 4.6, 4.4], font_size=10)

    check(doc, [
        '每个指标都有定义、计算方式、目标值、数据来源四要素',
        '至少有一个用户侧的定性/定量评估方法',
        '明确了基线与对照对象',
        '评估时间点与项目里程碑对齐',
    ])

    # ---- 第 6 章 ----
    h2(doc, '第 6 章　数据方案')
    ask(doc, '数据从哪来？已经拿到手了吗？有哪些字段？怎么更新？要花多少钱？')
    hint(doc, '这一章最容易被写成"计划"，但要求写的是"已落盘数据集"。'
              '如果目前还没拿到数据，必须写明：获取路径、预计获取时间、拿不到时的替代方案（并同步写入第 7 章风险表）。')

    h3(doc, '6.1　数据需求清单')
    table(doc, ['数据项', '用途', '来源', '获取方式', '成本', '更新频率'],
          [['〈如：个股日线行情〉', '〈画走势与计算指标〉', '〈Tushare Pro〉', '〈API 脚本批量拉取〉', '〈免费额度内〉', '〈每日〉'],
           ['〈如：每日指标（PE/PB/换手率）〉', '〈估值与热度分析〉', '〈同上〉', '〈同上〉', '〈…〉', '〈每日〉'],
           ['〈如：用户访谈记录〉', '〈需求与痛点证据〉', '〈本人采集〉', '〈录音转写〉', '〈0〉', '〈一次性〉']],
          widths=[3.6, 3.4, 2.6, 3.2, 2.2, 2.0], font_size=9)

    h3(doc, '6.2　已落盘数据集说明')
    body(doc, '〈逐个列出你已经存到本地的数据文件。没有落盘的数据不能算数。〉')
    table(doc, ['编号', '文件名 / 表名', '格式', '记录数', '时间范围', '大小'],
          [['D1', '〈daily_price.csv〉', 'CSV', '〈约 12,000 行〉', '〈2019-01-01 至 2026-10-15〉', '〈1.8 MB〉'],
           ['D2', '〈daily_basic.csv〉', 'CSV', '〈……〉', '〈……〉', '〈……〉'],
           ['D3', '〈interview_notes.xlsx〉', 'XLSX', '〈……〉', '〈……〉', '〈……〉']],
          widths=[1.2, 3.4, 1.8, 2.6, 4.4, 2.4], font_size=9)

    h3(doc, '6.3　关键字段字典')
    body(doc, '〈挑出与核心分析直接相关的 6–12 个字段，逐个说明含义、类型与取值口径。〉')
    table(doc, ['字段', '中文含义', '类型', '取值说明 / 单位', '备注'],
          [['ts_code', '股票代码', '文本', '如 000001.SZ', '主键之一'],
           ['trade_date', '交易日期', '日期', 'YYYYMMDD', '主键之一'],
           ['close', '收盘价', '数值', '元', '前复权'],
           ['turnover_rate', '换手率', '数值', '%', '—'],
           ['pe_ttm', '滚动市盈率', '数值', '倍', '负值表示亏损'],
           ['〈…〉', '〈…〉', '〈…〉', '〈…〉', '〈…〉']],
          widths=[2.8, 3.0, 1.8, 4.4, 3.8], font_size=9)

    h3(doc, '6.4　获取与更新机制')
    body(doc, '〈说明数据是怎么拿到的、以后怎么增量更新、失败怎么重试。〉')
    hint(doc, '推荐写法：给出脚本名与运行方式（如 `python fetch_data.py --since 2026-01-01`），'
              '说明幂等性（重复运行不产生重复行）、重试与容错（单日失败跳过并记日志，不中断整批）、'
              '更新触发方式（手动 / 定时任务 / 每次启动应用时检查）。'
              '注意：API Key 一律放在 .env 文件中用环境变量读取，不得写入代码或报告，不得上传公开仓库。')

    h3(doc, '6.5　数据质量与清洗规则')
    table(doc, ['问题类型', '发现情况', '处理规则'],
          [['缺失值', '〈如：停牌日无行情〉', '〈按标的前向填充不超过 1 日，否则剔除该样本〉'],
           ['异常值', '〈如：PE 为负或极端大〉', '〈保留但标记，分析时单独分组，不静默删除〉'],
           ['口径不一致', '〈如：复权方式前后不同〉', '〈统一为前复权并重算〉'],
           ['重复记录', '〈如：重复拉取导致主键重复〉', '〈按主键去重，保留最新一条〉']],
          widths=[3.0, 5.4, 7.4], font_size=10)

    h3(doc, '6.6　成本与合规')
    body(doc, '〈估算数据获取与 API 调用的实际花费，并说明合规与隐私处理。〉')
    table(doc, ['项目', '单价 / 费率', '预计用量', '预计花费', '控制措施'],
          [['〈Tushare 积分 / 会员〉', '〈…〉', '〈…〉', '〈…〉', '〈设置调用上限与缓存〉'],
           ['〈大模型 API〉', '〈元 / 百万 token〉', '〈约 X 万 token〉', '〈…〉', '〈结果缓存 + 限制单次输入长度〉'],
           ['〈托管 / 域名〉', '〈…〉', '〈…〉', '〈…〉', '〈优先免费额度〉']],
          widths=[3.6, 3.0, 3.0, 2.6, 4.4], font_size=9)
    hint(doc, '合规要点：遵守数据源的使用条款与调用频率限制；涉及个人信息（访谈、问卷）须匿名化处理并在报告中声明；'
              '不抓取明确禁止抓取的站点；数据仅用于课程作业，不用于商业分发。')

    check(doc, [
        '至少有一个数据集已真实落盘，并写清记录数与时间范围',
        '关键字段字典覆盖了核心分析所依赖的字段',
        '更新机制说明了失败重试与幂等处理',
        '成本有明确估算与控制措施',
        '合规与隐私处理已声明',
    ])

    # ---- 第 7 章 ----
    h2(doc, '第 7 章　项目风险评估')
    ask(doc, '什么最可能出岔子？出岔子之后具体怎么办？最坏情况下我还能交出什么？你明确不做什么？')
    hint(doc, '这是最能体现项目成熟度的一章。要求"细致、逐项"，每项都要写清"如果发生，怎么办"——'
              '一句话的"我会努力克服"不算应对措施。应对措施必须是可执行的动作，且要有降级方案（Plan B）。')

    h3(doc, '7.1　风险登记表')
    table(doc, ['编号', '风险事件与触发信号', '应对措施（如果发生，怎么办）', '兜底降级方案'],
          [['R1', '数据获取失败或质量不足：接口限流、停更、字段缺失、样本量不足',
            '启动备用数据源（表 6-1 中的备选）；改用低频/低精度字段；缩小标的范围保证深度',
            '用公开静态数据集或手工整理的 200–500 条样本完成核心分析，并在报告中说明局限'],
           ['R2', '关键技术难点卡壳：框架 API 不理解、大模型输出解析失败、部署报错',
            '先问 AI（附完整报错与上下文）→ 互助组 → 课程群（24h 内响应）→ 教师办公时间；卡点超过 48 小时即触发降级',
            '退回课堂兜底模板 mvp-template/，只保留"数据加载 + 1 张图"的最小可运行骨架'],
           ['R3', 'API / 数据成本超支：token 消耗失控、付费额度用尽',
            '加结果缓存与请求节流；缩短输入上下文；设置每日调用上限与金额告警',
            '改为离线预计算 + 静态展示，或只用免费额度内的本地模型与本地计算'],
           ['R4', '个人时间与课业冲突：期中考试、其他课程 ddl 集中',
            '按 7.3 里程碑表提前 1 周启动；每周固定 6–8 小时投入；P2 功能首先被砍',
            '只交付 P0 三件事（数据加载 / 核心分析 / 主可视化），其余列为"后续工作"'],
           ['R5', '功能范围膨胀：越做越大，核心功能反而没做透',
            '严格执行 P0/P1/P2 优先级；新增需求一律先入"待办池"，P0 未达标前不开新功能',
            '冻结需求：以本报告表 4-2 的功能清单为范围上限，超出部分一律不做'],
           ['R6', '第三方服务变更或失效：模型下线、接口改版、API Key 过期',
            '封装统一调用层，换厂商只改 base_url 与模型名；关键调用保留本地快照',
            '改用本地可运行的规则/统计方法给出结果，页面中标注"离线模式"'],
           ['R7', '可视化与交互效果不达预期：图表难读、加载慢、交互逻辑混乱',
            '回归 W6 的可视化选型依据重做图表；用 5 人快速可用性测试定位问题',
            '降级为静态图表 + 简单筛选，保证"看得懂"优先于"好看"'],
           ['R8', '评估结果不利：指标未达标、用户反馈差',
            '如实报告实测值并分析原因，把"为什么没达标"作为结论的一部分',
            '不以美化数据的方式达标；将未达标项转为第 7 章的风险复盘与后续改进方向'],
           ['R9', '环境与协作风险：依赖版本冲突、设备损坏、文件丢失',
            'requirements.txt 锁定版本；Git 或网盘每日提交；关键数据双备份',
            '保留一份可运行的最小环境与样例数据，随时可在一台新机器上重建'],
           ['R10', '〈你自己的项目特有的风险〉', '〈……〉', '〈……〉']],
          widths=[1.2, 5.0, 5.6, 4.4], font_size=9)
    hint(doc, '表格已给出 9 条常见风险作为示范。请保留与你项目相关的条目并改写为你的具体情况，'
              '删掉无关的，并至少补充 1 条你项目特有的风险（如"标注数据不足""访谈对象难以约到"等）。'
              '每条应对措辞要具体到"谁在什么时候做什么"，能落地才算数。')

    h3(doc, '7.2　「不做」清单')
    body(doc, '〈明确写出本项目不做的事。这是防止范围膨胀最有效的一节，也是老师重点看的。〉')
    hint(doc, '每条"不做"最好附一句"为什么不做"，体现这是权衡后的决定而非偷懒。下列示范条目可直接选用或改写。')
    table(doc, ['编号', '不做的事', '为什么不做'],
          [['N1', '不做用户注册 / 登录与账号体系', '需要后端与数据库，超出单人单机项目的必要范围，且与核心分析价值无关'],
           ['N2', '不做移动端适配', '优先保证桌面端核心流程可用，移动端留待后续'],
           ['N3', '不做实时流式数据', '实时链路的成本与稳定性风险高，批量更新已能满足分析需求'],
           ['N4', '不训练自己的模型', '调用现成 API 或统计方法即可达成指标，自研模型的时间成本不可控'],
           ['N5', '不做付费部署与域名', '使用免费托管额度，把预算留给 API 调用'],
           ['N6', '〈你补充〉', '〈……〉'],
           ['N7', '〈你补充〉', '〈……〉'],
           ['N8', '〈你补充〉', '〈……〉']],
          widths=[1.2, 6.6, 8.4], font_size=9)

    h3(doc, '7.3　里程碑与缓冲')
    table(doc, ['周次', '主要任务', '交付物', '缓冲安排'],
          [['W8', '〈……〉', '〈MVP v0.1 可运行〉', '〈预留 2 天〉'],
           ['W10', '〈……〉', '〈核心分析完成〉', '〈预留 2 天〉'],
           ['W12', '〈……〉', '〈可视化与交互完成〉', '〈预留 3 天〉'],
           ['W14', '〈……〉', '〈评估与迭代〉', '〈预留 3 天〉'],
           ['W15', '〈……〉', '〈最终交付〉', '〈预留 2 天〉']],
          widths=[1.8, 5.6, 5.8, 3.0], font_size=10)

    check(doc, [
        '风险逐项列出，每项都有"如果发生，怎么办"的具体动作',
        '每条风险都有兜底降级方案（Plan B）',
        '「不做」清单不少于 5 条，且附有理由',
        '里程碑有明确的时间缓冲',
    ])

    # ---- 第 8 章 ----
    h2(doc, '第 8 章　参考资料列表')
    ask(doc, '你的依据来自哪里？正文每一处引用，是否都能在这份列表里找到对应条目？反之亦然？')
    hint(doc, '硬性要求：正文用（作者，年份）格式规范引用，如"金融舆情的传染效应显著（Loughran & McDonald, 2011）"；'
              '文末列表覆盖正文所有引用，且列表中没有正文未引用的条目——做到"文中有引、文末有列、一一对应"。'
              '最低要求：正文至少 5 处引用，参考资料不少于 8 条，且必须包含至少 1 篇学术文献。')

    h3(doc, '8.1　引用规范')
    body(doc, '正文中的引用格式示例：')
    table(doc, ['引用情形', '正文中写法', '文末列表写法'],
          [['单作者', '……显著提升了判断准确率（张伟, 2023）。', '张伟. (2023). 〈文章标题〉. 〈期刊名〉, 〈卷(期)〉, 〈页码〉.'],
           ['两位作者', '……传染效应显著（Loughran & McDonald, 2011）。', 'Loughran, T., & McDonald, B. (2011). When is a liability not a liability? Journal of Finance, 66(1), 35–65.'],
           ['三位及以上', '……效果有限（陈明等, 2022）。', '陈明, 李华, 王芳. (2022). 〈标题〉. 〈期刊〉, 〈卷〉, 〈页〉.'],
           ['机构 / 官方报告', '……用户规模持续增长（CNNIC, 2025）。', '中国互联网络信息中心(CNNIC). (2025). 第 5X 次中国互联网络发展状况统计报告.'],
           ['官方文档', '……见接口文档说明（Tushare, 2026）。', 'Tushare. (2026). Tushare Pro 接口文档 · 每日指标. https://tushare.pro/document/2?doc_id=32'],
           ['访谈证据', '……最困扰的是指标太多（受访者 C, 2026）。', '受访者 C. (2026). 半结构化访谈记录（本人采集，已匿名化）.'],
           ['书籍', '……可用性原则已形成共识（Nielsen, 1994）。', 'Nielsen, J. (1994). Usability Engineering. Morgan Kaufmann.']],
          widths=[2.6, 6.8, 6.8], font_size=9)

    h3(doc, '8.2　参考资料列表')
    body(doc, '〈删除下列示例条目，替换为你自己真实阅读或查阅过的文献。列表按作者姓氏拼音/字母排序或按正文出现顺序编号均可，'
              '但全文须保持一致。〉')
    hint(doc, '下面的条目仅为格式示范，请勿直接照抄——老师会核对正文引用与列表的一一对应关系，'
              '抄入未读过的文献属于学术不端。')
    table(doc, ['编号', '类型', '参考资料（按 8.1 的格式书写）', '在正文中的引用位置'],
          [['[1]', '论文', 'Loughran, T., & McDonald, B. (2011). 〈……〉', '第 2.1 节'],
           ['[2]', '论文', '〈作者〉. (2024). 〈标题〉. 〈期刊〉.', '第 3.3 节'],
           ['[3]', '官方报告', '〈机构〉. (2025). 〈报告名〉.', '第 2.1 节'],
           ['[4]', '官方文档', '〈项目〉. (2026). 〈文档名〉. 〈URL〉', '第 4.4 节'],
           ['[5]', '书籍', '〈作者〉. (〈年份〉). 〈书名〉. 〈出版社〉.', '第 5.2 节'],
           ['[6]', '访谈', '〈受访者代号〉. (2026). 半结构化访谈记录（本人采集）.', '第 3.2 节'],
           ['[7]', '数据集', '〈数据提供方〉. (2026). 〈数据集名称〉. 〈获取日期〉.', '第 6.2 节'],
           ['[8]', '网页', '〈作者/机构〉. (〈年份〉). 〈标题〉. 〈URL〉（访问日期：〈…〉）', '第 〈…〉 节']],
          widths=[1.2, 2.0, 8.8, 4.2], font_size=9)

    check(doc, [
        '正文中至少 5 处（作者，年份）格式的引用',
        '参考资料不少于 8 条，且包含至少 1 篇学术文献',
        '列表覆盖了正文所有引用，无遗漏',
        '列表中没有正文未引用的多余条目',
        '访谈、官方文档、论文、书籍等类型齐全',
    ])

    # ================= 附录 =================
    h1(doc, '附录 A　常见扣分点与规避方法', page_break=True)
    table(doc, ['扣分点', '典型表现', '怎么改'],
          [['动机空泛', '"随着大数据时代的到来，数据分析越来越重要"', '换成具体场景 + 具体用户 + 可核查的事实与数据'],
           ['调研是拼盘', '访谈、文献、AI 结果三段并列，互不相干', '用一条推理链串起来：定痛点 → 定参照 → 补盲区'],
           ['技术选型无理由', '"本项目使用 Streamlit，因为它简单易用"', '给出比较对象与放弃理由，理由来自项目约束'],
           ['指标不可测', '"提升用户体验，使界面更加美观"', '改成有定义、算法、目标值、数据来源的指标'],
           ['数据未落盘', '"计划从某某网站爬取数据"', '先拉下来存本地，写清记录数、时间范围、关键字段'],
           ['风险无动作', '"如果数据获取失败，我会努力想办法解决"', '写清触发信号、具体动作、兜底方案'],
           ['没有不做清单', '功能越列越多，看不出边界', '明确列出至少 5 条"不做"及理由'],
           ['引用不对应', '文末列了 10 篇，正文一处没引', '写完正文立刻回填引用，再核对一遍列表'],
           ['把 Notebook 当产品', '提交一段脚本截图作为"产品"', '强调可交互闭环：改输入 → 重算 → 刷新结果'],
           ['篇幅靠凑', '大量复制粘贴背景介绍', '宁可少写，也要保证每句话都在推进你的论证']],
          widths=[2.6, 6.6, 7.0], font_size=9)

    h1(doc, '附录 B　常用写作句式库', page_break=False)
    body(doc, '下列句式可直接套用，填好括号内容后再润色为你自己的表达。')
    table(doc, ['写作场景', '可套用的句式'],
          [['陈述现象', '在【场景】中，【对象】普遍面临【问题】，其直接后果是【影响】。'],
           ['引用佐证', '已有研究表明，【结论】（作者, 年份）；然而该研究主要聚焦于【范围】，对【你的场景】关注不足。'],
           ['指出空白', '综上，现有工作已在【A】方面取得进展，但在【B】条件下仍缺乏【C】的针对性方案。'],
           ['陈述设计', '针对上述空白，本项目拟构建【产品形态】，通过【关键机制】实现【核心价值】。'],
           ['说明选型', '在【环节】上，候选方案为【甲/乙/丙】；考虑到【约束条件】，本项目选择【甲】，其代价是【取舍】。'],
           ['定义指标', '本文以【指标名】衡量【对象】，定义为【计算公式】，目标值为【阈值】，数据来源于【来源】。'],
           ['陈述风险', '若【风险事件】发生（表现为【触发信号】），本项目将【具体动作】；最坏情况下回退至【降级方案】。'],
           ['声明不做', '本项目不做【事项】，原因是【权衡理由】；该能力将列入后续工作。']],
          widths=[2.6, 13.2], font_size=10)

    h1(doc, '附录 C　十页篇幅分配与两周写作计划', page_break=False)
    table(doc, ['建议用时', '写作任务', '产出'],
          [['第 1 天（2h）', '确定题目与问题陈述，完成第 2 章', '动机章节 1–1.5 页'],
           ['第 2 天（2h）', '拉取并落盘数据，完成第 6 章', '数据方案 1–1.5 页 + 数据集'],
           ['第 3 天（2h）', '整理原型功能与选型，完成第 4 章', '方案设计 1.5–2 页'],
           ['第 4 天（1.5h）', '设计指标与基线，完成第 5 章', '评估章节 1–1.5 页'],
           ['第 5 天（2h）', '补做访谈与文献检索，完成第 3 章', '调研章节 1.5–2 页'],
           ['第 6 天（1.5h）', '梳理风险与不做清单，完成第 7 章', '风险章节 1.5–2 页'],
           ['第 7 天（1h）', '回填引用，完成第 8 章与通读校对', '参考资料 0.5–1 页 + 定稿']],
          widths=[3.0, 7.4, 5.4], font_size=10)

    h1(doc, '附录 D　提交前十分钟终检', page_break=False)
    check(doc, [
        '文件名已改为 开题报告-姓名-学号.docx',
        '正文（不含封面、目录、本模板说明与附录）达到 10 页以上',
        '八项内容齐全，顺序正确',
        '所有提示框、问题框、自检框已删除干净',
        '全文通读一遍，无错别字、无残留占位符〈〉',
        '引用与参考资料一一对应',
        '另存一份 PDF 备份，防止格式错乱',
    ])

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p.add_run('—— 祝写作顺利。有问题先问 AI，再问互助组，最后找老师。——'),
         cn=CN_HINT, size=11, italic=True, color=C_HINT)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '开题报告-姓名-学号.docx')
    doc.save(out)
    print('已生成：', out)


if __name__ == '__main__':
    build()
