#!/usr/bin/env python3
"""生成第3次课的课堂演示 PPT"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import copy

# ── 颜色方案 ──
C_BG_DARK    = RGBColor(0x1A, 0x1A, 0x2E)   # 深蓝黑
C_BG_SECTION = RGBColor(0x16, 0x21, 0x3E)   # 章节页背景
C_ACCENT     = RGBColor(0x00, 0xD2, 0xFF)   # 青蓝高亮
C_ACCENT2    = RGBColor(0xFF, 0x6B, 0x6B)   # 红色（涨）
C_ACCENT3    = RGBColor(0x51, 0xCF, 0x66)   # 绿色（跌）
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY       = RGBColor(0xB0, 0xB0, 0xC0)
C_LIGHT_BG   = RGBColor(0x22, 0x2B, 0x45)   # 卡片背景
C_YELLOW     = RGBColor(0xFF, 0xD4, 0x3B)   # 黄色强调
C_ORANGE     = RGBColor(0xFF, 0x9F, 0x43)   # 橙色

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── 辅助函数 ──
def add_bg(slide, color=C_BG_DARK):
    """添加纯色背景"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, color=C_BG_DARK):
    """用矩形覆盖整张幻灯片作为背景"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Emu(0), Emu(0), prs.slide_width, prs.slide_height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    # 发送到最底层
    sp = shape._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)

def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=C_WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                font_name="Microsoft YaHei", line_spacing=1.3):
    """添加文本框"""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    p.space_after = Pt(4)
    if line_spacing:
        p.line_spacing = Pt(font_size * line_spacing)
    return txBox

def add_multi_text(slide, left, top, width, height, lines, font_size=16,
                   color=C_WHITE, font_name="Microsoft YaHei",
                   line_spacing=1.4, bullet=False, alignment=PP_ALIGN.LEFT):
    """添加多行文本"""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = alignment
        p.space_after = Pt(4)
        if line_spacing:
            p.line_spacing = Pt(font_size * line_spacing)
    return txBox

def add_card(slide, left, top, width, height, color=C_LIGHT_BG):
    """添加圆角卡片"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    # 减小圆角
    shape.adjustments[0] = 0.05
    return shape

def add_accent_line(slide, left, top, width, color=C_ACCENT, height=0.04):
    """添加强调线"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_number_badge(slide, left, top, number, color=C_ACCENT):
    """添加数字徽章"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(left), Inches(top), Inches(0.5), Inches(0.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = str(number)
    p.font.size = Pt(16)
    p.font.color.rgb = C_BG_DARK
    p.font.bold = True
    p.font.name = "Arial"
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(0)
    return shape

def add_table(slide, left, top, width, height, rows, cols, data,
              header_color=C_ACCENT, col_widths=None):
    """添加表格"""
    table_shape = slide.shapes.add_table(rows, cols, Inches(left), Inches(top),
                                          Inches(width), Inches(height))
    table = table_shape.table
    
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = data[r][c] if r < len(data) and c < len(data[r]) else ""
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(13)
                paragraph.font.name = "Microsoft YaHei"
                paragraph.alignment = PP_ALIGN.LEFT
                if r == 0:
                    paragraph.font.color.rgb = C_BG_DARK
                    paragraph.font.bold = True
                else:
                    paragraph.font.color.rgb = C_WHITE
            # 头行着色
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_LIGHT_BG if r % 2 == 1 else RGBColor(0x2A, 0x33, 0x55)
    return table_shape

def add_code_block(slide, left, top, width, height, code_text, font_size=12):
    """添加代码块"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x0D, 0x11, 0x1A)
    shape.line.color.rgb = RGBColor(0x33, 0x3D, 0x5C)
    shape.adjustments[0] = 0.03
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)
    for i, line in enumerate(code_text.split('\n')):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = C_ACCENT
        p.font.name = "Consolas"
        p.font.bold = False
        p.space_after = Pt(1)
    return shape

def add_arrow(slide, left, top, width, height, color=C_ACCENT):
    """添加箭头"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

# ═══════════════════════════════════════════════
# 第 1 页：封面
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

# 顶部装饰线
add_accent_line(slide, 0.8, 0.5, 2, C_ACCENT, 0.06)

add_textbox(slide, 0.8, 0.7, 11, 1.2, "第 3 次课", 28, C_ACCENT, True)
add_textbox(slide, 0.8, 1.6, 11, 1.5, "Skill 与 Agent 开发", 52, C_WHITE, True)
add_accent_line(slide, 0.8, 3.2, 4, C_ACCENT, 0.04)

add_multi_text(slide, 0.8, 3.5, 8, 2.5, [
    "理解 MCP 的概念及其作为 Skill 工具扩展的价值",
    "掌握 MCP 配置方法与 SKILL.md 编写方法",
    "掌握金融数据分析 Skill 设计方法与错误处理",
    "理解 Agent 概念与创建配置方法",
    "理解 Skill + Agent + MCP 协同架构",
    "能够构建端到端的金融分析工作流"
], 16, C_GRAY)

# 右侧装饰
add_card(slide, 9.5, 1.2, 3.2, 4.5, RGBColor(0x15, 0x1D, 0x35))
add_textbox(slide, 9.7, 1.4, 2.8, 0.5, "课程信息", 14, C_ACCENT, True)
add_multi_text(slide, 9.7, 2.0, 2.8, 3.5, [
    "课时：85 分钟",
    "工具：OpenCode + tushare",
    "核心：MCP / Skill / Agent",
    "目标：从使用到开发"
], 14, C_GRAY)

add_textbox(slide, 0.8, 6.5, 8, 0.5, "金融 AI 编程 | 2026 春季", 14, RGBColor(0x66, 0x70, 0x90))

# ═══════════════════════════════════════════════
# 第 2 页：课前思考
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.6, "课前思考", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "回顾第 2 次课，引出新问题", 36, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 左侧卡片：回顾
add_card(slide, 0.8, 2.1, 5.5, 4.5, C_LIGHT_BG)
add_textbox(slide, 1.1, 2.3, 5, 0.5, "回顾第 2 次课", 20, C_YELLOW, True)
add_multi_text(slide, 1.1, 2.9, 5, 3.5, [
    "我们已经会用 tushare skill 获取股票数据了",
    "",
    "但它每次都要让 AI：",
    "  写 Python 代码 → 运行 → 解析结果",
    "",
    "链路长、容易出错：",
    "  ✗ 代码语法错误",
    "  ✗ 包版本不兼容",
    "  ✗ 网络超时",
    "  ✗ 返回数据格式不符预期",
], 15, C_GRAY)

# 右侧卡片：新思考
add_card(slide, 6.8, 2.1, 5.7, 4.5, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.1, 2.3, 5, 0.5, "本节课的新思考", 20, C_ACCENT, True)
add_multi_text(slide, 7.1, 2.9, 5.3, 3.5, [
    '❓ 如果 AI 能直接"调用接口"，',
    "    跳过写代码步骤，会不会更快？",
    "",
    "❓ 如何开发一个自己的 Skill？",
    "",
    "❓ 如何让多个 Skill 和工具协同",
    "    完成复杂金融分析任务？",
], 16, C_WHITE)

# 底部目标
add_card(slide, 0.8, 6.8, 11.7, 0.5, RGBColor(0x00, 0x2B, 0x45))
add_textbox(slide, 1.0, 6.8, 11, 0.5, "目标：学习 MCP → 开发 Skill → 理解 Agent → 构建协同架构", 14, C_ACCENT, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 3 页：章节一 - MCP
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_SECTION)

add_textbox(slide, 0.8, 0.6, 4, 0.5, "PART 01", 16, C_ACCENT, True)
add_textbox(slide, 0.8, 1.2, 11, 1.5, "MCP——Skill 的外部工具扩展", 44, C_WHITE, True)
add_accent_line(slide, 0.8, 2.8, 4, C_ACCENT, 0.06)
add_textbox(slide, 0.8, 3.2, 8, 0.8, "从 Skill 的痛点出发，引出 MCP 作为零代码数据获取方案", 20, C_GRAY)
add_textbox(slide, 0.8, 4.0, 3, 0.5, "20 分钟", 16, C_ACCENT, True)

# ═══════════════════════════════════════════════
# 第 4 页：Skill 的痛点
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "1.1 从 Skill 的痛点出发", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "Skill 方式的数据获取链路", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 流程图
steps = ["用户输入", "AI 读 SKILL.md", "写 Python 代码", "运行代码", "解析结果"]
for i, step in enumerate(steps):
    x = 0.8 + i * 2.4
    add_card(slide, x, 2.3, 2.0, 0.8, C_LIGHT_BG)
    add_textbox(slide, x + 0.1, 2.35, 1.8, 0.7, step, 13, C_WHITE, False, PP_ALIGN.CENTER)
    if i < len(steps) - 1:
        add_arrow(slide, x + 2.05, 2.5, 0.3, 0.3, C_ACCENT)

# 错误标注
errors = ["语法错误", "版本不兼容", "网络超时", "格式不符"]
for i, err in enumerate(errors):
    x = 2.8 + i * 2.4
    add_textbox(slide, x, 3.3, 2, 0.5, f"⚠ {err}", 12, C_ACCENT2)

add_multi_text(slide, 0.8, 4.2, 11, 2, [
    "每一步都可能出错，链路越长，可靠性越低",
    "",
    '核心问题：如果 AI 能直接"调用接口"，跳过写代码环节呢？'
], 18, C_GRAY)

# 底部高亮
add_card(slide, 0.8, 5.5, 11.7, 1.2, RGBColor(0x1A, 0x10, 0x00))
add_textbox(slide, 1.2, 5.7, 11, 0.8, "💡 理想状态：AI 直接调用外部工具 → 返回结果，零中间步骤", 20, C_YELLOW, True)

# ═══════════════════════════════════════════════
# 第 5 页：MCP 解决了什么问题
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "1.2 MCP 解决了什么问题", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "MCP：让 AI 直接调用外部工具", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 定义卡片
add_card(slide, 0.8, 2.1, 5.5, 2.2, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.2, 5, 0.5, "Skill 方式", 18, C_ACCENT2, True)
add_multi_text(slide, 1.0, 2.8, 5, 1.5, [
    "AI 读 SKILL.md → 写 Python → 运行 → 解析结果",
    "",
    "需要写代码，延迟较高"
], 14, C_GRAY)

add_card(slide, 6.8, 2.1, 5.7, 2.2, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 7.0, 2.2, 5, 0.5, "MCP 方式 ✦", 18, C_ACCENT, True)
add_multi_text(slide, 7.0, 2.8, 5.3, 1.5, [
    "AI 直接调用 MCP 工具 → 返回结果",
    "",
    "零代码，低延迟"
], 14, C_WHITE)

# 对比表格
add_textbox(slide, 0.8, 4.6, 5, 0.5, "Skill vs MCP 本质对比", 18, C_WHITE, True)
data = [
    ["维度", "Skill", "MCP"],
    ["本质", "告诉 AI \"怎么做\"的说明书", "给 AI \"直接用的工具\"的接口"],
    ["交互方式", "AI 写代码 → 运行 → 解析", "AI 发送请求 → 直接返回结果"],
    ["是否需要写代码", "是（中间步骤）", "否（零代码）"],
    ["延迟", "较高（代码执行开销）", "较低（直接调用）"],
    ["灵活性", "高（可自定义逻辑）", "中（取决于 MCP 接口）"],
]
add_table(slide, 0.8, 5.1, 11.7, 2.2, 6, 3, data, C_ACCENT, [1.5, 5.1, 5.1])

# ═══════════════════════════════════════════════
# 第 6 页：选型原则
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "1.2 续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "MCP vs Skill 选型原则", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 三张卡片
scenarios = [
    ("纯数据获取", "如获取日线行情", "推荐 MCP", "零代码、低延迟", C_ACCENT),
    ("多步骤分析", "如计算 MACD 后判断买卖信号", "推荐 Skill", "需要自定义逻辑", C_ORANGE),
    ("数据获取 + 复杂分析", "如获取数据并生成报告", "MCP + Skill", "MCP 获取数据，Skill 指导分析", C_YELLOW),
]
for i, (title, example, rec, reason, color) in enumerate(scenarios):
    x = 0.8 + i * 4.1
    add_card(slide, x, 2.2, 3.8, 3.8, C_LIGHT_BG)
    add_textbox(slide, x + 0.2, 2.4, 3.4, 0.5, title, 18, C_WHITE, True)
    add_textbox(slide, x + 0.2, 3.0, 3.4, 0.5, example, 14, C_GRAY)
    add_accent_line(slide, x + 0.2, 3.5, 2, color, 0.04)
    add_textbox(slide, x + 0.2, 3.7, 3.4, 0.5, rec, 22, color, True)
    add_textbox(slide, x + 0.2, 4.4, 3.4, 0.8, reason, 14, C_GRAY)

# ═══════════════════════════════════════════════
# 第 7 页：MCP 配置方法
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "1.3 MCP 配置方法", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "项目级 MCP 配置", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 两种类型
add_card(slide, 0.8, 2.2, 5.5, 2.0, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.3, 5, 0.5, "远程 URL 型（type: \"remote\"）", 16, C_ACCENT, True)
add_multi_text(slide, 1.0, 2.9, 5, 1.2, [
    "通过 URL 直接连接远程服务",
    "示例：tushare MCP",
    "无需本地安装，配置即用"
], 13, C_GRAY)

add_card(slide, 6.8, 2.2, 5.7, 2.0, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.0, 2.3, 5, 0.5, "本地命令型（type: \"local\"）", 16, C_ORANGE, True)
add_multi_text(slide, 7.0, 2.9, 5.3, 1.2, [
    "通过本地命令启动服务（stdio）",
    "示例：Zotero MCP",
    "需要本地安装对应软件"
], 13, C_GRAY)

# 配置文件位置
data2 = [
    ["配置级别", "文件位置", "作用范围"],
    ["项目级", "项目根目录 opencode.jsonc", "仅当前项目生效"],
    ["全局级", "~/.config/opencode/opencode.jsonc", "所有项目生效"],
]
add_table(slide, 0.8, 4.5, 11.7, 1.3, 3, 3, data2, C_ACCENT, [1.5, 5.1, 5.1])

# 安全提示
add_card(slide, 0.8, 6.0, 11.7, 1.2, RGBColor(0x2A, 0x15, 0x00))
add_textbox(slide, 1.0, 6.1, 11, 0.4, "🔒 安全注意事项", 16, C_ORANGE, True)
add_textbox(slide, 1.0, 6.5, 11, 0.5, "Token 不硬编码在配置文件中，使用环境变量引用：{env:TUSHARE_TOKEN}", 14, C_GRAY)

# ═══════════════════════════════════════════════
# 第 8 页：案例一 - 配置 tushare MCP
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "🎯 案例一", 14, C_YELLOW, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "配置 tushare MCP 获取金融数据", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_YELLOW, 0.04)

# 左侧：配置步骤
add_card(slide, 0.8, 2.1, 5.8, 5.0, C_LIGHT_BG)
add_textbox(slide, 1.1, 2.2, 5.3, 0.5, "配置步骤", 18, C_ACCENT, True)

steps_text = [
    "1. 在项目根目录创建/编辑 opencode.jsonc",
    "2. 在 mcp 字段中写入 tushareMcp 配置",
    "3. 重启 opencode 会话",
    "4. 输入自然语言指令测试",
    "5. 对比 Skill 方式获取同一数据"
]
add_multi_text(slide, 1.1, 2.8, 5.3, 3.5, steps_text, 15, C_GRAY, line_spacing=1.6)

# 右侧：配置代码
add_code_block(slide, 7.0, 2.1, 5.5, 2.5, '''{
    "mcp": {
        "tushareMcp": {
            "type": "remote",
            "url": "https://api.tushare.pro/mcp/
              ?token={env:TUSHARE_TOKEN}"
        }
    }
}''', 12)

# 测试指令
add_card(slide, 7.0, 4.9, 5.5, 1.5, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 7.2, 5.0, 5, 0.4, "测试指令", 14, C_ACCENT, True)
add_textbox(slide, 7.2, 5.4, 5, 0.8, "\"获取贵州茅台最近 30 天的日线数据\"", 16, C_WHITE, True)

# 教学目标
add_card(slide, 0.8, 6.5, 11.7, 0.7, RGBColor(0x00, 0x2B, 0x45))
add_textbox(slide, 1.0, 6.55, 11, 0.6, "🎯 教学目标：掌握项目级远程 MCP 配置方法，直观感受 MCP 与 Skill 的数据获取差异", 14, C_ACCENT, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 9 页：章节二 - Skill 开发实践
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_SECTION)

add_textbox(slide, 0.8, 0.6, 4, 0.5, "PART 02", 16, C_ACCENT, True)
add_textbox(slide, 0.8, 1.2, 11, 1.5, "Skill 开发实践", 44, C_WHITE, True)
add_accent_line(slide, 0.8, 2.8, 4, C_ACCENT, 0.06)
add_textbox(slide, 0.8, 3.2, 8, 0.8, "从\"使用 Skill\"过渡到\"开发 Skill\"，用 AI 辅助开发降低门槛", 20, C_GRAY)
add_textbox(slide, 0.8, 4.0, 3, 0.5, "30 分钟", 16, C_ACCENT, True)

# ═══════════════════════════════════════════════
# 第 10 页：SKILL.md 编写方法 - frontmatter
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "2.1 SKILL.md 编写方法", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "frontmatter 与 description 编写技巧", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# frontmatter 示例
add_code_block(slide, 0.8, 2.1, 5.5, 2.0, '''---
name: stock-tech-analysis
description: 计算股票均线/MACD/RSI等技术
  指标并生成分析图表，适用于技术分析场景
---''', 14)

# description 编写要点
add_card(slide, 6.8, 2.1, 5.7, 2.0, C_LIGHT_BG)
add_textbox(slide, 7.0, 2.2, 5, 0.5, "description 编写要点", 16, C_ACCENT, True)
add_multi_text(slide, 7.0, 2.7, 5.3, 1.3, [
    "✓ 准确描述适用场景（触发条件）",
    "✓ 包含关键动词（计算、分析、生成）",
    "✓ 包含领域关键词（均线、MACD、RSI）",
], 14, C_GRAY, line_spacing=1.5)

# 内容结构
add_textbox(slide, 0.8, 4.4, 5, 0.5, "SKILL.md 内容结构", 18, C_WHITE, True)
add_card(slide, 0.8, 4.9, 11.7, 2.3, C_LIGHT_BG)

items = [
    ("背景", "说明数据来源和分析场景"),
    ("步骤说明", "每个步骤都是 AI 可执行的指令；数据获取步骤标注 MCP / Skill 回退策略"),
    ("示例", "展示典型输入 → 输出"),
    ("注意事项", "错误处理要前置；列出常见边界条件"),
]
for i, (title, desc) in enumerate(items):
    y = 5.0 + i * 0.5
    add_number_badge(slide, 1.1, y, i + 1, C_ACCENT)
    add_textbox(slide, 1.7, y, 2, 0.5, title, 14, C_WHITE, True)
    add_textbox(slide, 3.5, y, 8.5, 0.5, desc, 13, C_GRAY)

# ═══════════════════════════════════════════════
# 第 11 页：SKILL.md 关键原则
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "2.1 续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "SKILL.md 编写关键原则", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

principles = [
    ("指令要具体", "不要说\"分析数据\"，要说\"计算 20 日均线、MACD(12,26,9)、RSI(14 日)\"", C_ACCENT),
    ("步骤要可执行", "每个步骤 AI 都能用工具完成，不要写无法实现的步骤", C_ORANGE),
    ("错误处理要前置", "在注意事项中提前说明可能的异常和处理方式", C_ACCENT2),
]
for i, (title, desc, color) in enumerate(principles):
    y = 2.2 + i * 1.6
    add_card(slide, 0.8, y, 11.7, 1.3, C_LIGHT_BG)
    add_number_badge(slide, 1.1, y + 0.3, i + 1, color)
    add_textbox(slide, 1.7, y + 0.2, 10, 0.5, title, 20, color, True)
    add_textbox(slide, 1.7, y + 0.7, 10, 0.5, desc, 15, C_GRAY)

# ═══════════════════════════════════════════════
# 第 12 页：金融 Skill 设计方法
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "2.2 金融 Skill 设计方法", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "设计流程与步骤拆解", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 设计流程
flow_steps = ["场景分析", "步骤拆解", "指令编写", "错误处理", "测试验证"]
for i, step in enumerate(flow_steps):
    x = 0.8 + i * 2.4
    add_card(slide, x, 2.1, 2.1, 0.7, C_LIGHT_BG)
    add_textbox(slide, x + 0.1, 2.15, 1.9, 0.6, step, 14, C_WHITE, True, PP_ALIGN.CENTER)
    if i < len(flow_steps) - 1:
        add_arrow(slide, x + 2.15, 2.25, 0.2, 0.3, C_ACCENT)

# 步骤拆解示例
add_textbox(slide, 0.8, 3.2, 5, 0.5, "股票技术分析步骤拆解", 18, C_WHITE, True)
data3 = [
    ["步骤", "操作", "工具/方法"],
    ["1. 数据获取", "获取日线行情数据", "优先 tushare MCP；回退 tushare skill"],
    ["2. 数据清洗", "处理缺失值、停牌日", "bash 运行 Python"],
    ["3. 指标计算", "计算均线/MACD/RSI", "bash 运行 Python"],
    ["4. 可视化", "绘制技术指标图表", "bash 运行 Python"],
    ["5. 输出结论", "生成分析报告", "直接输出文本"],
]
add_table(slide, 0.8, 3.7, 11.7, 2.0, 6, 3, data3, C_ACCENT, [1.5, 3.6, 6.6])

# ═══════════════════════════════════════════════
# 第 13 页：金融数据错误处理
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "2.2 续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "金融数据常见错误处理", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT2, 0.04)

data4 = [
    ["错误类型", "检测方法", "处理策略"],
    ["股票代码无效", "tushare 返回空数据", "提示用户检查代码格式（如 600519.SH）"],
    ["停牌日数据缺失", "交易日期不连续", "用前值填充或标注停牌"],
    ["数据为空", "DataFrame 为空", "提示\"该时间段无数据，请调整日期范围\""],
    ["API 限频", "返回错误码", "等待后重试，或降低请求频率"],
    ["数据不足计算指标", "数据行数 < 计算周期", "提示\"MACD 至少需要 35 个交易日\""],
]
add_table(slide, 0.8, 2.2, 11.7, 3.5, 6, 3, data4, C_ACCENT2, [2.5, 3.6, 5.6])

add_card(slide, 0.8, 6.0, 11.7, 1.0, RGBColor(0x2A, 0x15, 0x00))
add_textbox(slide, 1.0, 6.1, 11, 0.8, "⚠ 关键原则：错误处理要前置，在注意事项中提前说明可能的异常和处理方式", 16, C_ORANGE, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 14 页：AI 辅助 Skill 开发
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "2.3 AI 辅助 Skill 开发", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "迭代优化流程", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 循环流程
cycle_steps = ["创建", "测试", "评估", "改进"]
for i, step in enumerate(cycle_steps):
    x = 1.5 + i * 2.8
    add_card(slide, x, 2.2, 2.0, 0.8, C_LIGHT_BG)
    add_textbox(slide, x + 0.1, 2.25, 1.8, 0.7, step, 16, C_WHITE, True, PP_ALIGN.CENTER)
    if i < len(cycle_steps) - 1:
        add_arrow(slide, x + 2.05, 2.4, 0.3, 0.3, C_ACCENT)
# 回环箭头（用文字代替）
add_textbox(slide, 10.5, 2.3, 2, 0.5, "↺ 再测试", 14, C_ACCENT)

# 两个工具
add_card(slide, 0.8, 3.5, 5.5, 3.2, C_LIGHT_BG)
add_textbox(slide, 1.1, 3.6, 5, 0.5, "skill-creator", 20, C_ACCENT, True)
add_textbox(slide, 1.1, 4.1, 5, 0.4, "自动生成 SKILL.md 框架", 14, C_GRAY)
add_multi_text(slide, 1.1, 4.6, 5, 2, [
    "1. 输入需求描述",
    "2. 自动生成 frontmatter 和步骤框架",
    "3. 根据金融场景补充细节指令和示例代码",
], 14, C_GRAY, line_spacing=1.5)

add_card(slide, 6.8, 3.5, 5.7, 3.2, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.1, 3.6, 5, 0.5, "skill-improver", 20, C_ORANGE, True)
add_textbox(slide, 7.1, 4.1, 5, 0.4, "评估质量并给出改进建议", 14, C_GRAY)
add_multi_text(slide, 7.1, 4.6, 5.3, 2, [
    "1. 评估 description 准确性——能否正确触发",
    "2. 评估内容组织——步骤是否清晰可执行",
    "3. 评估边界条件——是否覆盖常见异常",
    "4. 输出改进建议",
], 14, C_GRAY, line_spacing=1.5)

# ═══════════════════════════════════════════════
# 第 15 页：案例二 - 开发股票技术分析 Skill
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "🎯 案例二", 14, C_YELLOW, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "开发\"股票技术分析 Skill\"（含 MCP 调用）", 28, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_YELLOW, 0.04)

# 六步流程
case2_steps = [
    ("使用 skill-creator\n生成框架", C_ACCENT),
    ("填充技术指标\n计算指令", C_ORANGE),
    ("标注双通道\n数据获取策略", C_ACCENT),
    ("使用 skill-improver\n评估质量", C_YELLOW),
    ("添加错误处理", C_ACCENT2),
    ("测试验证", C_ACCENT3),
]
for i, (text, color) in enumerate(case2_steps):
    x = 0.5 + i * 2.1
    add_card(slide, x, 2.2, 1.9, 1.4, C_LIGHT_BG)
    add_number_badge(slide, x + 0.1, 2.3, i + 1, color)
    add_textbox(slide, x + 0.7, 2.35, 1.1, 0.4, f"Step {i+1}", 10, color, True)
    add_multi_text(slide, x + 0.15, 2.8, 1.7, 0.8, text.split('\n'), 12, C_GRAY, line_spacing=1.3)
    if i < len(case2_steps) - 1:
        add_arrow(slide, x + 1.95, 2.7, 0.12, 0.2, color)

# 重点：双通道策略
add_card(slide, 0.8, 4.0, 11.7, 1.5, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 1.0, 4.1, 5, 0.5, "💡 双通道数据获取策略", 18, C_ACCENT, True)
add_multi_text(slide, 1.0, 4.6, 11, 0.8, [
    "优先使用 tushare MCP 获取日线数据（零代码，低延迟）→ 若 MCP 不可用，则回退至 tushare skill（编写 Python 代码获取）"
], 15, C_GRAY)

# 错误处理
add_card(slide, 0.8, 5.7, 11.7, 1.5, C_LIGHT_BG)
add_textbox(slide, 1.0, 5.8, 5, 0.5, "⚠ 错误处理要点", 16, C_ACCENT2, True)
add_multi_text(slide, 1.0, 6.3, 11, 0.8, [
    "停牌日数据缺失 → 前值填充  |  数据不足计算 MACD → 需至少 35 个交易日  |  RSI 计算除零风险 → 添加保护逻辑"
], 13, C_GRAY)

# ═══════════════════════════════════════════════
# 第 16 页：章节三 - Agent 与协同架构
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_SECTION)

add_textbox(slide, 0.8, 0.6, 4, 0.5, "PART 03", 16, C_ACCENT, True)
add_textbox(slide, 0.8, 1.2, 11, 1.5, "Agent 与协同架构", 44, C_WHITE, True)
add_accent_line(slide, 0.8, 2.8, 4, C_ACCENT, 0.06)
add_textbox(slide, 0.8, 3.2, 8, 0.8, "Agent 是\"调度者\"，编排 Skill 和 MCP 完成复杂任务", 20, C_GRAY)
add_textbox(slide, 0.8, 4.0, 3, 0.5, "35 分钟", 16, C_ACCENT, True)

# ═══════════════════════════════════════════════
# 第 17 页：Agent 基础概念
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "3.1 Agent 基础概念", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "什么是 Agent？", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

add_textbox(slide, 0.8, 2.0, 11, 0.6, "能自主规划、调用工具、返回结果的智能体", 22, C_ACCENT, True)

# 主代理 vs 子代理
add_card(slide, 0.8, 2.8, 5.5, 2.5, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.9, 5, 0.5, "主代理 (Primary)", 18, C_ACCENT, True)
add_multi_text(slide, 1.0, 3.5, 5, 1.5, [
    "用户直接交互",
    "Tab 键循环切换",
    "代表角色：Build、Plan",
    "拥有全部或大部分工具权限"
], 14, C_GRAY, line_spacing=1.4)

add_card(slide, 6.8, 2.8, 5.7, 2.5, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.0, 2.9, 5, 0.5, "子代理 (Subagent)", 18, C_ORANGE, True)
add_multi_text(slide, 7.0, 3.5, 5.3, 1.5, [
    "由主代理委派调用",
    "基于 description 自动选择",
    "专业助手（数据采集、报告生成）",
    "工具权限受限，职责更聚焦"
], 14, C_GRAY, line_spacing=1.4)

# 内置代理表
data5 = [
    ["代理", "模式", "定位", "工具权限"],
    ["Build", "primary", "默认主代理，启用所有工具", "全部开放"],
    ["Plan", "primary", "受限主代理，专注分析和规划", "文件编辑、bash 均设为 ask"],
]
add_table(slide, 0.8, 5.5, 11.7, 1.3, 3, 4, data5, C_ACCENT, [1.2, 1.5, 5.5, 3.5])

# ═══════════════════════════════════════════════
# 第 18 页：Agent vs Skill
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "3.1 续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "Agent 与 Skill 的本质区别", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

data6 = [
    ["维度", "Agent", "Skill"],
    ["本质", "独立的智能体，有自己的 prompt、工具、模型", "指令模板，指导 AI 如何使用工具"],
    ["能力", "可自主规划、调用工具、委派子代理、返回结果", "被动加载，提供步骤说明"],
    ["是否独立运行", "是，可作为主代理或子代理独立执行任务", "否，必须由 Agent 加载后才能生效"],
    ["配置内容", "prompt + tools + permission + model", "SKILL.md（步骤 + 示例 + 注意事项）"],
    ["类比", "有明确职责的\"专员\"", "给专员的\"操作手册\""],
]
add_table(slide, 0.8, 2.1, 11.7, 3.5, 6, 3, data6, C_ACCENT, [1.8, 5.0, 4.9])

add_card(slide, 0.8, 5.9, 11.7, 1.2, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 1.0, 6.0, 11, 0.9, "💡 记忆：Agent 是\"专员\"，Skill 是\"操作手册\"，MCP 是\"直接调用的工具\"\n三者协同才能完成复杂金融分析任务", 16, C_YELLOW, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 19 页：Agent 创建与配置
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "3.2 Agent 创建与配置", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "两种配置方式", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 左：Markdown 方式
add_card(slide, 0.8, 2.1, 5.5, 4.5, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.2, 5, 0.5, "Markdown 方式（推荐）", 18, C_ACCENT, True)
add_textbox(slide, 1.0, 2.7, 5, 0.4, "文件位置：.opencode/agents/{name}.md", 13, C_GRAY)
add_code_block(slide, 1.0, 3.2, 5.1, 3.2, '''---
description: 描述代理功能与使用场景
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
permission:
  bash: allow
---
你是 [角色描述]。[具体指令]。''', 11)

# 右：JSON 方式
add_card(slide, 6.8, 2.1, 5.7, 4.5, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.0, 2.2, 5, 0.5, "JSON 方式", 18, C_ORANGE, True)
add_textbox(slide, 7.0, 2.7, 5, 0.4, "文件位置：opencode.jsonc 的 agent 字段", 13, C_GRAY)
add_code_block(slide, 7.0, 3.2, 5.3, 3.2, '''{
  "agent": {
    "data-auditor": {
      "description": "检查股票数据中的异常值",
      "mode": "subagent",
      "prompt": "你是金融数据合规检查专员...",
      "tools": {
        "bash": true,
        "read": true,
        "write": false
      }
    }
  }
}''', 11)

# 底部对比
data7 = [
    ["对比维度", "Markdown 方式", "JSON 方式"],
    ["风格", "与 Skill 风格统一", "配置集中"],
    ["版本管理", "友好（纯文本）", "一般（JSON 格式）"],
    ["适合场景", "prompt 内容长时更清晰", "简单代理"],
]
add_table(slide, 0.8, 6.0, 11.7, 1.3, 4, 3, data7, C_ACCENT, [1.5, 5.1, 5.1])

# ═══════════════════════════════════════════════
# 第 20 页：Agent 关键字段
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "3.2 续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "Agent 配置关键字段", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

fields = [
    ("mode", "primary / subagent / all", "决定代理的角色类型", C_ACCENT),
    ("model", "可选，不指定时用全局配置", "控制代理使用的模型", C_ORANGE),
    ("description", "必填！决定子代理何时被自动调用", "触发条件描述", C_YELLOW),
    ("tools", "bash / read / write / edit", "控制代理可用的工具", C_ACCENT3),
    ("permission", "ask / allow / deny", "控制工具权限级别", C_ACCENT2),
]
for i, (field, value, desc, color) in enumerate(fields):
    y = 2.2 + i * 1.0
    add_card(slide, 0.8, y, 11.7, 0.8, C_LIGHT_BG)
    add_textbox(slide, 1.1, y + 0.1, 2.2, 0.6, field, 18, color, True)
    add_textbox(slide, 3.5, y + 0.1, 4.5, 0.6, value, 14, C_WHITE)
    add_textbox(slide, 8.5, y + 0.1, 3.5, 0.6, desc, 13, C_GRAY)

# ═══════════════════════════════════════════════
# 第 21 页：Skill + Agent + MCP 协同架构
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "3.3 Skill + Agent + MCP 协同架构", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "三者关系", 32, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 三者关系卡片
add_card(slide, 0.8, 2.2, 3.5, 2.5, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.3, 3, 0.5, "Agent（调度）", 18, C_ACCENT, True)
add_multi_text(slide, 1.0, 2.9, 3, 1.5, [
    "决定\"做什么\"",
    "编排执行顺序",
    "委派子代理"
], 14, C_GRAY, line_spacing=1.5)

add_card(slide, 4.8, 2.2, 3.5, 2.5, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 5.0, 2.3, 3, 0.5, "Skill（方法）", 18, C_ORANGE, True)
add_multi_text(slide, 5.0, 2.9, 3, 1.5, [
    "指导\"怎么做\"",
    "提供步骤指令",
    "提供示例和注意事项"
], 14, C_GRAY, line_spacing=1.5)

add_card(slide, 8.8, 2.2, 3.7, 2.5, RGBColor(0x1A, 0x10, 0x30))
add_textbox(slide, 9.0, 2.3, 3.3, 0.5, "MCP（工具）", 18, C_YELLOW, True)
add_multi_text(slide, 9.0, 2.9, 3.3, 1.5, [
    "提供\"直接调用的接口\"",
    "零代码获取外部数据",
    "低延迟"
], 14, C_GRAY, line_spacing=1.5)

# 三种设计模式
add_textbox(slide, 0.8, 5.0, 5, 0.5, "三种设计模式", 18, C_WHITE, True)
data8 = [
    ["模式", "结构", "适用场景"],
    ["Skill 驱动", "Agent 加载 Skill → 用内置工具执行", "数据清洗、技术分析"],
    ["MCP 增强", "Agent 加载 Skill → 调 MCP 获取数据 → 分析", "实时行情查询"],
    ["全链路协同", "Agent 编排多个 Skill + 多个 MCP", "端到端金融分析报告"],
]
add_table(slide, 0.8, 5.5, 11.7, 1.6, 4, 3, data8, C_ACCENT, [1.5, 5.1, 5.1])

# ═══════════════════════════════════════════════
# 第 22 页：金融分析端到端工作流
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "3.3 续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "金融分析端到端工作流示例", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 流程图 - 用卡片和箭头表示
add_card(slide, 0.8, 2.2, 2.0, 0.8, C_LIGHT_BG)
add_textbox(slide, 0.9, 2.25, 1.8, 0.7, "用户输入", 14, C_WHITE, True, PP_ALIGN.CENTER)
add_arrow(slide, 2.9, 2.4, 0.3, 0.3, C_ACCENT)

add_card(slide, 3.3, 2.0, 3.0, 1.2, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 3.5, 2.1, 2.6, 0.5, "日报 Agent（主代理）", 14, C_ACCENT, True)
add_textbox(slide, 3.5, 2.6, 2.6, 0.5, "理解需求 · 编排任务", 12, C_GRAY)

# 子代理1
add_card(slide, 1.5, 3.8, 4.5, 2.5, C_LIGHT_BG)
add_textbox(slide, 1.7, 3.9, 4, 0.5, "数据采集子代理", 16, C_ORANGE, True)
add_multi_text(slide, 1.7, 4.4, 4, 1.8, [
    "├ tushare MCP（零代码获取行情）",
    "├ tushare Skill（分析方法指导）",
    "└ 返回结构化数据"
], 13, C_GRAY, line_spacing=1.5)

# 子代理2
add_card(slide, 7.0, 3.8, 5.0, 2.5, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.2, 3.9, 4.6, 0.5, "报告生成子代理", 16, C_YELLOW, True)
add_multi_text(slide, 7.2, 4.4, 4.6, 1.8, [
    "├ 接收结构化数据",
    "├ 撰写行情概览/板块分析",
    "└ 输出日报文案"
], 13, C_GRAY, line_spacing=1.5)

# 连线用文字表示
add_textbox(slide, 3.5, 3.2, 2, 0.5, "▼ 委派", 12, C_ACCENT, True, PP_ALIGN.CENTER)
add_textbox(slide, 8.0, 3.2, 2, 0.5, "▼ 委派", 12, C_ACCENT, True, PP_ALIGN.CENTER)

# 设计原则
add_card(slide, 0.8, 6.5, 11.7, 0.7, RGBColor(0x00, 0x2B, 0x45))
add_textbox(slide, 1.0, 6.55, 11, 0.6, "设计原则：① 单一职责  ② 松耦合  ③ 渐进增强（Skill 驱动 → MCP 增强 → 全链路协同）", 14, C_ACCENT, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 23 页：案例三 - 金融数据合规检查代理
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "🎯 案例三", 14, C_YELLOW, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "创建\"金融数据合规检查代理\"", 28, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_YELLOW, 0.04)

# 左：Markdown 方式
add_card(slide, 0.8, 2.1, 5.5, 4.0, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.2, 5, 0.5, "方式一：Markdown（推荐）", 16, C_ACCENT, True)
add_textbox(slide, 1.0, 2.7, 5, 0.3, "文件：.opencode/agents/data-auditor.md", 12, C_GRAY)
add_code_block(slide, 1.0, 3.1, 5.1, 2.8, '''---
description: 检查股票数据中的异常值，
  输出结构化合规报告
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
---
你是金融数据合规检查专员。
检查三类异常：
1. 负价格：收盘价 < 0
2. 日期不连续：交易日缺漏
3. 涨跌幅超限：单日超过 ±10%
输出 Markdown 表格。''', 11)

# 右：JSON 方式
add_card(slide, 6.8, 2.1, 5.7, 4.0, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.0, 2.2, 5, 0.5, "方式二：JSON", 16, C_ORANGE, True)
add_textbox(slide, 7.0, 2.7, 5, 0.3, "文件：opencode.jsonc 的 agent 字段", 12, C_GRAY)
add_code_block(slide, 7.0, 3.1, 5.3, 2.8, '''{
  "agent": {
    "data-auditor": {
      "description": "检查股票数据中的异常值",
      "mode": "subagent",
      "prompt": "你是金融数据合规检查专员...",
      "tools": {
        "bash": true,
        "read": true,
        "write": false,
        "edit": false
      }
    }
  }
}''', 11)

# 测试提示
add_card(slide, 0.8, 6.3, 11.7, 0.9, RGBColor(0x00, 0x2B, 0x45))
add_textbox(slide, 1.0, 6.35, 11, 0.8, "🎯 教学目标：掌握 Agent 两种配置方式，亲手完成第一个代理的创建与测试\n分别用两种方式创建同一个代理，观察两者行为是否一致", 14, C_ACCENT, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 24 页：案例四 - 日报自动生成系统
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "🎯 案例四", 14, C_YELLOW, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "构建\"股票日报自动生成系统\"", 28, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_YELLOW, 0.04)

# 角色分工表
data9 = [
    ["角色", "模式", "职责", "依赖"],
    ["日报 Agent（主代理）", "primary", "接收指令、拆分子任务、委派、汇总", "—"],
    ["数据采集子代理", "subagent", "获取指数行情、板块涨跌数据", "tushare MCP + Skill"],
    ["报告生成子代理", "subagent", "解读数据，撰写结构化日报", "—"],
]
add_table(slide, 0.8, 2.0, 11.7, 1.8, 4, 4, data9, C_YELLOW, [2.5, 1.8, 4.0, 3.4])

# 架构图
add_card(slide, 0.8, 4.1, 11.7, 3.0, C_LIGHT_BG)
add_textbox(slide, 1.0, 4.2, 3, 0.5, "协同架构", 16, C_ACCENT, True)

# 用户输入
add_card(slide, 1.0, 4.9, 1.8, 0.7, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 1.1, 4.95, 1.6, 0.6, "用户输入", 12, C_WHITE, True, PP_ALIGN.CENTER)

add_arrow(slide, 2.9, 5.05, 0.3, 0.3, C_ACCENT)

# 日报Agent
add_card(slide, 3.3, 4.7, 2.5, 1.1, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 3.5, 4.8, 2.1, 0.5, "日报 Agent", 13, C_ACCENT, True)
add_textbox(slide, 3.5, 5.2, 2.1, 0.5, "主编 · 调度", 11, C_GRAY)

# 数据采集
add_card(slide, 6.2, 4.7, 2.3, 1.1, C_LIGHT_BG)
add_textbox(slide, 6.3, 4.8, 2.1, 0.5, "数据采集", 13, C_ORANGE, True)
add_textbox(slide, 6.3, 5.2, 2.1, 0.5, "MCP + Skill", 11, C_GRAY)

# 报告生成
add_card(slide, 9.0, 4.7, 2.3, 1.1, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 9.1, 4.8, 2.1, 0.5, "报告生成", 13, C_YELLOW, True)
add_textbox(slide, 9.1, 5.2, 2.1, 0.5, "撰写日报", 11, C_GRAY)

add_textbox(slide, 5.9, 5.1, 0.4, 0.4, "→", 16, C_ACCENT, True)
add_textbox(slide, 8.6, 5.1, 0.4, 0.4, "→", 16, C_ACCENT, True)

# 演示步骤
add_textbox(slide, 1.0, 6.0, 11, 0.5, "演示步骤", 14, C_ACCENT, True)
add_multi_text(slide, 1.0, 6.4, 11.3, 0.8, [
    "1. 创建 data-collector.md（数据采集子代理）  2. 创建 report-writer.md（报告生成子代理）  3. 配置日报主代理",
    "4. Tab 键切换到日报主代理  5. 输入\"生成今日股市日报\"  6. 观察主代理逐步委派子代理并汇总结果"
], 12, C_GRAY)

# ═══════════════════════════════════════════════
# 第 25 页：本次课总结
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "四、本次课总结", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "核心要点回顾", 36, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

points = [
    ("MCP 的价值", "让 AI 直接调用外部工具，实现零代码数据获取，弥补 Skill 需要写代码的短板", C_ACCENT),
    ("选型原则", "纯数据获取优先 MCP，多步骤分析优先 Skill，复杂任务两者协同", C_ORANGE),
    ("Skill 开发流程", "场景分析 → 步骤拆解 → 指令编写 → 错误处理 → AI 辅助迭代", C_YELLOW),
    ("Agent 的角色", "调度者，编排 Skill 和 MCP 完成复杂任务的关键枢纽", C_ACCENT3),
    ("协同架构", "Skill 驱动、MCP 增强、全链路协同三种模式，根据任务复杂度选用", C_ACCENT2),
]
for i, (title, desc, color) in enumerate(points):
    y = 2.1 + i * 1.0
    add_card(slide, 0.8, y, 11.7, 0.8, C_LIGHT_BG)
    add_number_badge(slide, 1.1, y + 0.15, i + 1, color)
    add_textbox(slide, 1.7, y + 0.05, 3, 0.4, title, 16, color, True)
    add_textbox(slide, 4.5, y + 0.05, 7.5, 0.7, desc, 14, C_GRAY)

# ═══════════════════════════════════════════════
# 第 26 页：协作全景图
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "四、续", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "Skill + Agent + MCP 协作全景", 36, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

# 全景图 - 用卡片表示
# 顶层：Agent
add_card(slide, 3.5, 2.2, 6.3, 1.5, RGBColor(0x0A, 0x1A, 0x2A))
add_textbox(slide, 3.8, 2.4, 5.8, 0.5, "Agent（调度）", 22, C_ACCENT, True, PP_ALIGN.CENTER)
add_textbox(slide, 3.8, 2.9, 5.8, 0.5, "决定\"做什么\"、编排执行顺序", 14, C_GRAY, False, PP_ALIGN.CENTER)

# 连线
add_textbox(slide, 4.0, 3.8, 2, 0.5, "▼", 20, C_ACCENT, True, PP_ALIGN.CENTER)
add_textbox(slide, 7.5, 3.8, 2, 0.5, "▼", 20, C_ACCENT, True, PP_ALIGN.CENTER)

# 底层左：Skill
add_card(slide, 1.5, 4.3, 5.0, 1.8, C_LIGHT_BG)
add_textbox(slide, 1.8, 4.5, 4.5, 0.5, "Skill（方法）", 20, C_ORANGE, True, PP_ALIGN.CENTER)
add_multi_text(slide, 1.8, 5.0, 4.5, 1.0, [
    "指导\"怎么做\"",
    "提供步骤指令"
], 14, C_GRAY, line_spacing=1.3, alignment=PP_ALIGN.CENTER)

# 底层右：MCP
add_card(slide, 7.0, 4.3, 5.0, 1.8, RGBColor(0x1A, 0x10, 0x30))
add_textbox(slide, 7.3, 4.5, 4.5, 0.5, "MCP（工具）", 20, C_YELLOW, True, PP_ALIGN.CENTER)
add_multi_text(slide, 7.3, 5.0, 4.5, 1.0, [
    "提供\"直接调用的接口\"",
    "零代码获取外部数据"
], 14, C_GRAY, line_spacing=1.3, alignment=PP_ALIGN.CENTER)

# 底部渐进增强
add_card(slide, 1.5, 6.4, 10.5, 0.8, RGBColor(0x00, 0x2B, 0x45))
add_textbox(slide, 1.7, 6.45, 10, 0.6, "渐进增强路径：Skill 驱动（先跑通） → MCP 增强（提效率） → 全链路协同（端到端）", 15, C_ACCENT, True, PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# 第 27 页：参考资料
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_textbox(slide, 0.8, 0.4, 5, 0.5, "参考资料", 14, C_ACCENT, True)
add_textbox(slide, 0.8, 0.9, 11, 0.8, "延伸阅读与工具", 30, C_WHITE, True)
add_accent_line(slide, 0.8, 1.7, 3, C_ACCENT, 0.04)

add_card(slide, 0.8, 2.1, 5.5, 4.5, C_LIGHT_BG)
add_textbox(slide, 1.0, 2.2, 5, 0.5, "官方文档", 18, C_ACCENT, True)
add_multi_text(slide, 1.0, 2.8, 5, 3.5, [
    "• OpenCode MCP 服务器文档",
    "  opencode.ai/docs/zh-cn/mcp-servers/",
    "",
    "• OpenCode 代理文档",
    "  opencode.ai/docs/zh-cn/agents/",
    "",
    "• MCP 协议规范",
    "  modelcontextprotocol.io",
], 14, C_GRAY, line_spacing=1.4)

add_card(slide, 6.8, 2.1, 5.7, 4.5, RGBColor(0x1A, 0x25, 0x40))
add_textbox(slide, 7.0, 2.2, 5, 0.5, "Skill 开发工具", 18, C_ORANGE, True)
add_multi_text(slide, 7.0, 2.8, 5.3, 3.5, [
    "• Anthropic skill-creator",
    "  github.com/anthropics/skills",
    "",
    "• Claude Scholar skill-improver",
    "  github.com/Galaxy-Dawn/claude-scholar",
    "",
    "• gstack skillify",
    "  github.com/garrytan/gstack",
], 14, C_GRAY, line_spacing=1.4)

# ═══════════════════════════════════════════════
# 第 28 页：结束页
# ═══════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_shape_bg(slide, C_BG_DARK)

add_accent_line(slide, 4.5, 2.5, 4.3, C_ACCENT, 0.06)
add_textbox(slide, 2, 3.0, 9, 1.5, "开始上机实验！", 48, C_WHITE, True, PP_ALIGN.CENTER)
add_accent_line(slide, 4.5, 4.5, 4.3, C_ACCENT, 0.06)
add_textbox(slide, 2, 5.0, 9, 0.8, "实验内容：MCP 配置 → Skill 开发 → Agent 创建 → 协同工作流", 18, C_GRAY, False, PP_ALIGN.CENTER)

# ── 保存 ──
output_path = r"C:\haichao\teaching\2026-finance-ai\session-03\lecture-slides.pptx"
prs.save(output_path)
print(f"PPT 已保存到: {output_path}")
print(f"共 {len(prs.slides)} 页")
