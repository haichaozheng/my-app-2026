"""
生成小组项目 Presentation 要求文档
- Word (.docx)
- PPTX (.pptx)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ────────────────────────────────────────────────────────
# 辅助函数
# ────────────────────────────────────────────────────────

def set_east_asia_font(run, font_name):
    """安全地设置东亚（中文）字体。"""
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:eastAsiaTheme'), font_name)


def styled_run(para, text, size=11, bold=False, color=None, east_font='宋体', west_font='Calibri'):
    run = para.add_run(text)
    run.font.name = west_font
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    set_east_asia_font(run, east_font)
    return run


def set_cell_shading(cell, fill_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    # 替换已有 shd
    old = tcPr.find(qn('w:shd'))
    if old is not None:
        tcPr.remove(old)
    tcPr.append(shd)


def header_row(table, headers, fill='1F3864'):
    row = table.rows[0]
    for i, text in enumerate(headers):
        cell = row.cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        styled_run(p, text, size=10, bold=True,
                   color=(255, 255, 255), east_font='黑体')
        set_cell_shading(cell, fill)


def data_row(table, values, center_cols=None):
    row = table.add_row()
    center_cols = center_cols or []
    for i, text in enumerate(values):
        cell = row.cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in center_cols else WD_ALIGN_PARAGRAPH.LEFT
        styled_run(p, text, size=10)
    return row


def add_h1(doc, text, color=(31, 56, 100)):
    p = doc.add_heading(text, level=1)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(*color)
        set_east_asia_font(run, '黑体')
    return p


def add_h2(doc, text, color=(31, 56, 100)):
    p = doc.add_heading(text, level=2)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(*color)
        set_east_asia_font(run, '黑体')
    return p


def add_bullet(doc, text, indent=0.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(indent)
    styled_run(p, text, size=10.5)
    return p


# ────────────────────────────────────────────────────────
# 构建 Word 文档
# ────────────────────────────────────────────────────────
doc = Document()

# 页边距
from docx.shared import Inches
section = doc.sections[0]
section.top_margin    = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin   = Cm(2.5)
section.right_margin  = Cm(2.5)

# ── 封面
for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
styled_run(p, '小组项目期末汇报要求', size=22, bold=True,
           color=(31, 56, 100), east_font='黑体')

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
styled_run(p2, 'Presentation Requirements', size=14,
           color=(31, 56, 100))

doc.add_paragraph()
p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
styled_run(p3, '面向财经领域的人工智能应用', size=12, color=(89, 89, 89))

doc.add_page_break()

# ── 一、汇报概览
add_h1(doc, '一、汇报概览')

table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.columns[0].width = Cm(4)
table.columns[1].width = Cm(11)
header_row(table, ['项目', '说明'])

overview_data = [
    ('形式',   '现场口头报告 + 项目功能 Live Demo（不接受纯 PPT 汇报）'),
    ('时长',   '每组 10–15 分钟汇报 + 3–5 分钟问答'),
    ('PPT',    '建议 10–15 页（不含封面），图文并茂，须含封面信息（姓名/学号）'),
    ('截止',   '第 17 周周日晚 20:00 前提交报告和 PPT'),
    ('提交邮箱', '342497883@qq.com'),
]
for item, desc in overview_data:
    data_row(table, [item, desc], center_cols=[0])
doc.add_paragraph()

# ── 二、汇报结构与内容要求
add_h1(doc, '二、汇报结构与内容要求')
p = doc.add_paragraph()
styled_run(p, '每组汇报须按以下结构组织，各部分时间仅供参考，可根据项目特点适当调整。')
doc.add_paragraph()

sections_data = [
    ('1. 项目背景与价值（1–2 分钟）', [
        '简要介绍所解决的金融问题或场景',
        '说明项目的现实意义和目标用户',
        '一句话概括项目核心价值主张',
    ]),
    ('2. 竞品调研与创新点（1–2 分钟）', [
        '至少介绍 2–3 个同类工具或产品',
        '明确本项目的差异化优势与创新点',
        '可用对比表格辅助说明',
    ]),
    ('3. 技术方案（2–3 分钟）', [
        '数据来源与处理方式',
        '技术栈（模型、框架、API 等）',
        '系统架构图或流程图',
        '重点说明大模型 / AI 工具的使用方式',
    ]),
    ('4. 功能演示 Live Demo（3–5 分钟）', [
        '现场运行演示核心功能（不接受录屏替代）',
        '演示路径清晰，覆盖主要使用场景',
        '若现场网络/环境不稳定，可准备备用截图作辅助',
    ]),
    ('5. 结果分析与总结（1–2 分钟）', [
        '展示关键结果或测试数据',
        '反思遇到的困难与未解决问题',
        '说明改进方向与未来计划',
    ]),
]
for title, pts in sections_data:
    add_h2(doc, title)
    for pt in pts:
        add_bullet(doc, pt)
    doc.add_paragraph()

# ── 三、评分标准
add_h1(doc, '三、汇报评分标准')
p = doc.add_paragraph()
styled_run(p, '评分满分 100 分，分为以下五个维度：')
doc.add_paragraph()

score_table = doc.add_table(rows=1, cols=4)
score_table.style = 'Table Grid'
score_table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row(score_table, ['评分维度', '权重', '评分要点', '满分'])

score_data = [
    ('项目完成度', '30%', '核心功能实现完整，项目可运行演示，达到预期目标', '30'),
    ('技术方案',   '25%', '技术选型合理，大模型/AI工具应用到位，架构清晰', '25'),
    ('演示效果',   '20%', 'Live Demo 流畅，功能展示充分，能应对现场提问', '20'),
    ('创新与价值', '15%', '有明确的差异化亮点，具备实际应用价值', '15'),
    ('汇报表达',   '10%', 'PPT 结构清晰，口头表达流畅，时间控制良好', '10'),
]
for row_data in score_data:
    data_row(score_table, list(row_data), center_cols=[0, 1, 3])
doc.add_paragraph()

# ── 四、PPT 要求
add_h1(doc, '四、PPT 要求')
ppt_items = [
    '页数建议：10–15 页（不含封面和目录），避免文字堆砌',
    '封面须包含：项目名称、小组成员姓名与学号',
    '结构完整，图文并茂，核心功能截图或流程图不可缺少',
    '字体不小于 20pt，图表需有标题和必要说明',
    '格式：PPT（.pptx），与报告同时提交',
]
for item in ppt_items:
    add_bullet(doc, item)
doc.add_paragraph()

# ── 五、Live Demo 要求
add_h1(doc, '五、Live Demo 要求')
demo_items = [
    '必须现场运行演示，不接受纯 PPT 汇报或仅播放录屏',
    '演示设备提前测试，确保环境配置就绪（含必要 API Key、数据文件等）',
    '演示路径须覆盖项目核心功能，建议提前设计演示脚本',
    '若现场出现技术问题，可辅助使用截图/录屏，但不能完全替代实时演示',
    '代码和数据须提供可下载链接（如网盘），在报告中注明',
]
for item in demo_items:
    add_bullet(doc, item)
doc.add_paragraph()

# ── 六、学术诚信
add_h1(doc, '六、学术诚信')
integrity_items = [
    '项目须为本组原创工作，禁止直接复制他人代码或报告',
    '鼓励使用大模型 / AI 工具辅助编程（如 opencode、Cursor 等）',
    '须在报告"技术方案"部分说明使用了哪些 AI 工具及其作用',
    '发现学术不端行为，该小组项目成绩记为零分',
]
for item in integrity_items:
    add_bullet(doc, item)
doc.add_paragraph()

# ── 七、提交清单
add_h1(doc, '七、提交清单')
p = doc.add_paragraph()
styled_run(p, '截止时间：第 17 周周日晚 20:00  |  提交邮箱：342497883@qq.com',
           size=11, bold=True, color=(31, 56, 100))
doc.add_paragraph()

cl_table = doc.add_table(rows=1, cols=3)
cl_table.style = 'Table Grid'
cl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row(cl_table, ['提交物', '格式', '说明'])
checklist_data = [
    ('报告', 'PDF', '字数 ≥6000 字（10 页以上），含封面（项目名称、姓名、学号），须提供代码/数据下载链接'),
    ('PPT',  '.pptx', '结构完整，图文并茂，用于现场汇报演示'),
    ('演示', '现场', '汇报当天现场运行项目，展示核心功能（不接受录屏替代）'),
]
for row_data in checklist_data:
    data_row(cl_table, list(row_data), center_cols=[0, 1])
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
styled_run(p, '祝各组项目顺利，期待精彩的演示！', size=11, color=(89, 89, 89))

doc.save('presentation-requirements.docx')
print('Word saved.')

# ────────────────────────────────────────────────────────
# 构建 PPTX
# ────────────────────────────────────────────────────────
from pptx import Presentation
from pptx.util import Inches, Pt as PPTPt
from pptx.dml.color import RGBColor as PPTRGB
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# 颜色
C_DARK   = PPTRGB(0x1F, 0x38, 0x64)
C_MID    = PPTRGB(0x2E, 0x75, 0xB6)
C_LIGHT  = PPTRGB(0xBD, 0xD7, 0xEE)
C_WHITE  = PPTRGB(0xFF, 0xFF, 0xFF)
C_GRAY   = PPTRGB(0x59, 0x59, 0x59)
C_ACCENT = PPTRGB(0xED, 0x7D, 0x31)
C_BG     = PPTRGB(0xF5, 0xF5, 0xF5)

W = prs.slide_width
H = prs.slide_height
BLANK = prs.slide_layouts[6]


def slide_bg(slide, color):
    shp = slide.shapes.add_shape(1, 0, 0, W, H)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()


def rect(slide, x, y, w, h, color, line=False):
    shp = slide.shapes.add_shape(1, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if not line:
        shp.line.fill.background()
    return shp


def tb(slide, text, x, y, w, h, size=14, bold=False,
       color=C_WHITE, align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txb = slide.shapes.add_textbox(x, y, w, h)
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = PPTPt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = '微软雅黑'
    return txb


# ── Slide 1: 封面
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_DARK)
rect(sl, 0, H - Inches(1.1), W, Inches(1.1), C_MID)
tb(sl, '小组项目期末汇报要求', Inches(1), Inches(1.6), Inches(11.33), Inches(1.5),
   size=42, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
tb(sl, 'Presentation Requirements',
   Inches(1), Inches(3.15), Inches(11.33), Inches(0.75),
   size=22, color=C_LIGHT, align=PP_ALIGN.CENTER)
tb(sl, '面向财经领域的人工智能应用',
   Inches(1), Inches(4.0), Inches(11.33), Inches(0.6),
   size=16, color=PPTRGB(0xBF, 0xBF, 0xBF), align=PP_ALIGN.CENTER)
tb(sl, '第 17 周周日晚 20:00 截止  |  提交至 342497883@qq.com',
   Inches(1), Inches(6.45), Inches(11.33), Inches(0.45),
   size=12, color=C_WHITE, align=PP_ALIGN.CENTER)


# ── Slide 2: 汇报概览
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_BG)
rect(sl, 0, 0, W, Inches(1.25), C_DARK)
tb(sl, '汇报概览', Inches(0.5), Inches(0.22), Inches(12), Inches(0.8),
   size=28, bold=True, color=C_WHITE)

items = [
    ('形式', '现场口头报告 + 项目功能 Live Demo（不接受纯 PPT 汇报）'),
    ('时长', '每组 10–15 分钟汇报 + 3–5 分钟问答'),
    ('PPT',  '建议 10–15 页（不含封面），图文并茂，须含封面信息（姓名/学号）'),
    ('截止', '第 17 周周日晚 20:00 前提交报告和 PPT'),
    ('邮箱', '342497883@qq.com'),
]
y0 = Inches(1.4)
for i, (k, v) in enumerate(items):
    bg = PPTRGB(0xE8, 0xEE, 0xF6) if i % 2 == 0 else C_WHITE
    rect(sl, Inches(0.35), y0 + Inches(i * 1.0), Inches(12.63), Inches(0.92), bg)
    tb(sl, k, Inches(0.45), y0 + Inches(i * 1.0) + Inches(0.13),
       Inches(1.6), Inches(0.65), size=14, bold=True, color=C_DARK)
    tb(sl, v, Inches(2.15), y0 + Inches(i * 1.0) + Inches(0.13),
       Inches(10.7), Inches(0.65), size=13, color=C_GRAY)


# ── Slide 3: 汇报结构（时间线）
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_BG)
rect(sl, 0, 0, W, Inches(1.25), C_DARK)
tb(sl, '汇报结构（5 部分）', Inches(0.5), Inches(0.22), Inches(12), Inches(0.8),
   size=28, bold=True, color=C_WHITE)

steps = [
    ('01', '项目背景\n与价值',    '1–2 min'),
    ('02', '竞品调研\n与创新点',  '1–2 min'),
    ('03', '技术\n方案',          '2–3 min'),
    ('04', 'Live\nDemo',          '3–5 min'),
    ('05', '结果分析\n与总结',    '1–2 min'),
]
box_colors = [
    PPTRGB(0x1F, 0x38, 0x64), PPTRGB(0x2E, 0x75, 0xB6),
    PPTRGB(0x1A, 0x8C, 0x8C), PPTRGB(0xED, 0x7D, 0x31),
    PPTRGB(0x70, 0xAD, 0x47),
]
bw = Inches(2.3)
bh = Inches(4.8)
bx0 = Inches(0.35)
by0 = Inches(1.45)
for i, (num, title, dur) in enumerate(steps):
    bx = bx0 + Inches(i * 2.56)
    rect(sl, bx, by0, bw, bh, box_colors[i])
    tb(sl, num, bx, by0 + Inches(0.25), bw, Inches(0.85),
       size=32, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(sl, title, bx, by0 + Inches(1.2), bw, Inches(1.3),
       size=15, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(sl, dur, bx, by0 + Inches(3.9), bw, Inches(0.65),
       size=13, color=C_LIGHT, align=PP_ALIGN.CENTER)


# ── Slide 4: 各部分内容细节
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_BG)
rect(sl, 0, 0, W, Inches(1.25), C_DARK)
tb(sl, '各部分内容要求', Inches(0.5), Inches(0.22), Inches(12), Inches(0.8),
   size=28, bold=True, color=C_WHITE)

col_details = [
    ('① 背景与价值',
     '• 金融问题/场景描述\n• 目标用户与意义\n• 一句话价值主张'),
    ('② 竞品与创新',
     '• 2–3 个同类产品\n• 差异化优势\n• 建议用对比表'),
    ('③ 技术方案',
     '• 数据来源与处理\n• 技术栈/架构图\n• AI 工具使用方式'),
    ('④ Live Demo',
     '• 现场运行核心功能\n• 演示路径清晰\n• 备用截图（应急）'),
    ('⑤ 结果总结',
     '• 关键结果/数据\n• 困难与反思\n• 改进方向'),
]
cw = Inches(2.42)
cx0 = Inches(0.3)
cy = Inches(1.42)
for i, (title, content) in enumerate(col_details):
    cx = cx0 + Inches(i * 2.55)
    rect(sl, cx, cy, cw, Inches(0.48), box_colors[i])
    tb(sl, title, cx + Inches(0.05), cy + Inches(0.04), cw - Inches(0.1), Inches(0.4),
       size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(sl, content, cx + Inches(0.07), cy + Inches(0.55), cw - Inches(0.14), Inches(5.0),
       size=12, color=C_GRAY, align=PP_ALIGN.LEFT)


# ── Slide 5: 评分标准
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_BG)
rect(sl, 0, 0, W, Inches(1.25), C_DARK)
tb(sl, '评分标准（满分 100 分）', Inches(0.5), Inches(0.22), Inches(12), Inches(0.8),
   size=28, bold=True, color=C_WHITE)

score_data2 = [
    ('项目完成度', '30分', '核心功能实现完整，项目可运行演示，达到预期目标'),
    ('技术方案',   '25分', '技术选型合理，大模型/AI工具应用到位，架构清晰'),
    ('演示效果',   '20分', 'Live Demo 流畅，功能展示充分，能应对现场提问'),
    ('创新与价值', '15分', '有明确的差异化亮点，具备实际应用价值'),
    ('汇报表达',   '10分', 'PPT 结构清晰，口头表达流畅，时间控制良好'),
]
sc_colors = [
    PPTRGB(0x1F, 0x38, 0x64), PPTRGB(0x2E, 0x75, 0xB6),
    PPTRGB(0x1A, 0x8C, 0x8C), PPTRGB(0xED, 0x7D, 0x31),
    PPTRGB(0x70, 0xAD, 0x47),
]
sy0 = Inches(1.42)
for i, (dim, score, criteria) in enumerate(score_data2):
    sy = sy0 + Inches(i * 1.05)
    rect(sl, Inches(0.3), sy, Inches(2.5), Inches(0.88), sc_colors[i])
    tb(sl, dim, Inches(0.35), sy + Inches(0.09), Inches(2.4), Inches(0.7),
       size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(sl, score, Inches(2.85), sy + Inches(0.05), Inches(1.3), Inches(0.78),
       size=22, bold=True, color=sc_colors[i], align=PP_ALIGN.CENTER)
    tb(sl, criteria, Inches(4.2), sy + Inches(0.12), Inches(8.8), Inches(0.65),
       size=13, color=C_GRAY, align=PP_ALIGN.LEFT)


# ── Slide 6: Live Demo & PPT 要求
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_BG)
rect(sl, 0, 0, W, Inches(1.25), C_DARK)
tb(sl, 'Live Demo & PPT 要求', Inches(0.5), Inches(0.22), Inches(12), Inches(0.8),
   size=28, bold=True, color=C_WHITE)

# 左半：Live Demo
rect(sl, Inches(0.3), Inches(1.38), Inches(6.1), Inches(0.5), C_MID)
tb(sl, 'Live Demo 要求', Inches(0.4), Inches(1.41), Inches(5.9), Inches(0.44),
   size=15, bold=True, color=C_WHITE)
demo_pts2 = [
    '必须现场运行，不接受纯录屏替代',
    '演示设备提前测试（API Key、数据文件等）',
    '覆盖核心功能，建议设计演示脚本',
    '技术故障时可辅助使用截图，不可完全替代',
    '代码/数据须提供可下载链接（网盘等）',
]
for j, pt in enumerate(demo_pts2):
    tb(sl, f'• {pt}', Inches(0.4), Inches(2.0) + Inches(j * 0.86),
       Inches(5.9), Inches(0.8), size=13, color=C_GRAY)

# 右半：PPT
rect(sl, Inches(7.0), Inches(1.38), Inches(6.0), Inches(0.5), C_ACCENT)
tb(sl, 'PPT 要求', Inches(7.1), Inches(1.41), Inches(5.8), Inches(0.44),
   size=15, bold=True, color=C_WHITE)
ppt_pts2 = [
    '建议 10–15 页（不含封面和目录）',
    '封面含：项目名称、姓名与学号',
    '图文并茂，核心功能截图/流程图必须有',
    '字体不小于 20pt，图表须有标题',
    '格式：.pptx，与报告同时提交',
]
for j, pt in enumerate(ppt_pts2):
    tb(sl, f'• {pt}', Inches(7.1), Inches(2.0) + Inches(j * 0.86),
       Inches(5.8), Inches(0.8), size=13, color=C_GRAY)


# ── Slide 7: 提交清单 & 学术诚信
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_BG)
rect(sl, 0, 0, W, Inches(1.25), C_DARK)
tb(sl, '提交清单 & 学术诚信', Inches(0.5), Inches(0.22), Inches(12), Inches(0.8),
   size=28, bold=True, color=C_WHITE)

# 表格表头
col_xs = [Inches(0.3), Inches(2.15), Inches(4.0)]
col_ws = [Inches(1.8), Inches(1.8), Inches(9.0)]
ty = Inches(1.42)
for ci, hdr in enumerate(['提交物', '格式', '要求说明']):
    rect(sl, col_xs[ci], ty, col_ws[ci], Inches(0.48), C_DARK)
    tb(sl, hdr, col_xs[ci] + Inches(0.05), ty + Inches(0.05),
       col_ws[ci] - Inches(0.1), Inches(0.38), size=13, bold=True,
       color=C_WHITE, align=PP_ALIGN.CENTER)
cl2 = [
    ('报告', 'PDF',
     '字数 ≥6000 字（10 页以上），含封面（项目名称、姓名、学号），须提供代码/数据下载链接'),
    ('PPT',  '.pptx', '结构完整，图文并茂，用于现场汇报演示'),
    ('演示', '现场',  '汇报当天现场运行项目，展示核心功能（不接受录屏替代）'),
]
for ri, (item, fmt, desc) in enumerate(cl2):
    ry = ty + Inches(0.52) + Inches(ri * 0.72)
    bg = PPTRGB(0xE8, 0xEE, 0xF6) if ri % 2 == 0 else C_WHITE
    for ci in range(3):
        rect(sl, col_xs[ci], ry, col_ws[ci], Inches(0.68), bg)
    for ci, txt in enumerate([item, fmt, desc]):
        al = PP_ALIGN.CENTER if ci < 2 else PP_ALIGN.LEFT
        tb(sl, txt, col_xs[ci] + Inches(0.05), ry + Inches(0.08),
           col_ws[ci] - Inches(0.1), Inches(0.55), size=12,
           color=C_GRAY, align=al)

# 截止提示
rect(sl, Inches(0.3), Inches(4.15), Inches(12.73), Inches(0.55), C_MID)
tb(sl, '截止：第 17 周周日晚 20:00  |  提交邮箱：342497883@qq.com',
   Inches(0.4), Inches(4.19), Inches(12.5), Inches(0.45),
   size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

# 学术诚信
tb(sl, '学术诚信', Inches(0.3), Inches(4.9), Inches(4), Inches(0.45),
   size=15, bold=True, color=C_DARK)
integ = [
    '✅  鼓励使用 AI 辅助编程（opencode / Cursor 等），须在报告中说明使用方式',
    '❌  禁止直接复制他人代码或报告',
    '⚠️  学术不端一经发现，该组项目成绩记零分',
]
for j, pt in enumerate(integ):
    tb(sl, pt, Inches(0.3), Inches(5.45) + Inches(j * 0.56),
       Inches(12.7), Inches(0.5), size=12, color=C_GRAY)


# ── Slide 8: 结尾
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, C_DARK)
rect(sl, 0, Inches(2.7), W, Inches(2.1), C_MID)
tb(sl, '期待各组精彩演示！',
   Inches(0.5), Inches(2.82), Inches(12.33), Inches(1.3),
   size=40, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
tb(sl, '充分准备，展示你们用 AI 解决金融问题的实力',
   Inches(0.5), Inches(4.2), Inches(12.33), Inches(0.7),
   size=18, color=C_LIGHT, align=PP_ALIGN.CENTER)
tb(sl, '第 17 周周日晚 20:00 截止  |  342497883@qq.com',
   Inches(0.5), Inches(6.4), Inches(12.33), Inches(0.5),
   size=12, color=PPTRGB(0xBF, 0xBF, 0xBF), align=PP_ALIGN.CENTER)


prs.save('presentation-requirements.pptx')
print('PPTX saved.')
