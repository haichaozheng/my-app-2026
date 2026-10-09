#!/usr/bin/env python3
"""基于 lab.md 生成格式完整的 Word 文档"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import re

doc = Document()

# ── 页面设置 ──
section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(2.54)
section.right_margin = Cm(2.54)

# ── 样式设置 ──
style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.35
style.paragraph_format.space_after = Pt(4)
# 中文 fallback
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

# Heading 样式
for level in range(1, 5):
    hs = doc.styles[f'Heading {level}']
    hs.font.name = 'Microsoft YaHei'
    hs.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    hs.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    if level == 1:
        hs.font.size = Pt(22)
        hs.font.bold = True
        hs.paragraph_format.space_before = Pt(18)
        hs.paragraph_format.space_after = Pt(10)
    elif level == 2:
        hs.font.size = Pt(17)
        hs.font.bold = True
        hs.paragraph_format.space_before = Pt(14)
        hs.paragraph_format.space_after = Pt(8)
    elif level == 3:
        hs.font.size = Pt(14)
        hs.font.bold = True
        hs.paragraph_format.space_before = Pt(10)
        hs.paragraph_format.space_after = Pt(6)
    elif level == 4:
        hs.font.size = Pt(12)
        hs.font.bold = True
        hs.paragraph_format.space_before = Pt(8)
        hs.paragraph_format.space_after = Pt(4)

# 代码样式
code_style = doc.styles.add_style('CodeBlock', WD_STYLE_TYPE.PARAGRAPH)
code_style.font.name = 'Consolas'
code_style.font.size = Pt(9)
code_style.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
code_style.paragraph_format.space_before = Pt(1)
code_style.paragraph_format.space_after = Pt(1)
code_style.paragraph_format.line_spacing = 1.15
code_style.paragraph_format.left_indent = Cm(0.5)

# 引用/提示样式
note_style = doc.styles.add_style('NoteBlock', WD_STYLE_TYPE.PARAGRAPH)
note_style.font.name = 'Microsoft YaHei'
note_style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
note_style.font.size = Pt(10)
note_style.font.italic = True
note_style.paragraph_format.left_indent = Cm(0.5)
note_style.paragraph_format.space_before = Pt(4)
note_style.paragraph_format.space_after = Pt(4)

# 列表项样式
list_style = doc.styles.add_style('ListItem', WD_STYLE_TYPE.PARAGRAPH)
list_style.font.name = 'Microsoft YaHei'
list_style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
list_style.font.size = Pt(11)
list_style.paragraph_format.left_indent = Cm(1.0)
list_style.paragraph_format.space_before = Pt(2)
list_style.paragraph_format.space_after = Pt(2)

# 子列表项样式
sublist_style = doc.styles.add_style('SubListItem', WD_STYLE_TYPE.PARAGRAPH)
sublist_style.font.name = 'Microsoft YaHei'
sublist_style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
sublist_style.font.size = Pt(11)
sublist_style.paragraph_format.left_indent = Cm(1.8)
sublist_style.paragraph_format.space_before = Pt(1)
sublist_style.paragraph_format.space_after = Pt(1)


# ── 辅助函数 ──

def add_heading(text, level=1):
    """添加标题"""
    doc.add_heading(text, level=level)

def add_para(text, bold=False, style_name=None):
    """添加段落"""
    p = doc.add_paragraph(style=style_name)
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.bold = bold
    return p

def add_rich_para(text, style_name=None):
    """添加带 **粗体** 标记的段落"""
    p = doc.add_paragraph(style=style_name)
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.bold = True
        else:
            run = p.add_run(part)
        run.font.name = 'Microsoft YaHei'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    return p

def add_code_block(code_text):
    """添加代码块（带灰色背景）"""
    # 添加一个单列表格作为代码块容器
    lines = code_text.strip('\n').split('\n')
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    # 设置单元格背景
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F5F5"/>')
    cell._tc.get_or_add_tcPr().append(shading)
    # 清除默认段落
    cell.paragraphs[0].text = ''
    for i, line in enumerate(lines):
        if i == 0:
            p = cell.paragraphs[0]
        else:
            p = cell.add_paragraph()
        run = p.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
    # 设置表格宽度
    tbl.columns[0].width = Cm(15.0)
    # 增加代码块后的间距
    doc.add_paragraph()

def add_table(headers, rows, col_widths=None):
    """添加表格"""
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # 表头
    for i, h in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Microsoft YaHei'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 表头背景
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="2C3E50"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    
    # 数据行
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(str(cell_text))
            run.font.name = 'Microsoft YaHei'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
            run.font.size = Pt(10)
            # 交替行背景
            if r_idx % 2 == 0:
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="EBF5FB"/>')
                cell._tc.get_or_add_tcPr().append(shading)
    
    # 设置列宽
    if col_widths:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = Cm(w)
    
    doc.add_paragraph()  # 表后间距
    return tbl

def add_bullet(text, level=0, checked=None):
    """添加列表项"""
    if checked is not None:
        prefix = '☑ ' if checked else '☐ '
        text = prefix + text
    p = doc.add_paragraph(style='ListItem' if level == 0 else 'SubListItem')
    # 处理粗体标记
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.bold = True
        else:
            run = p.add_run(part)
        run.font.name = 'Microsoft YaHei'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    return p

def add_numbered(text, number, level=0):
    """添加编号列表项"""
    prefix = f"{number}. "
    p = doc.add_paragraph(style='ListItem' if level == 0 else 'SubListItem')
    parts = re.split(r'(\*\*.*?\*\*)', text)
    run0 = p.add_run(prefix)
    run0.font.name = 'Microsoft YaHei'
    run0._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.bold = True
        else:
            run = p.add_run(part)
        run.font.name = 'Microsoft YaHei'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    return p

def add_note(text):
    """添加提示/注意框"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFF9E6"/>')
    cell._tc.get_or_add_tcPr().append(shading)
    cell.paragraphs[0].text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(10)
    run.italic = True
    tbl.columns[0].width = Cm(15.0)
    doc.add_paragraph()

def add_checklist_item(text, checked=False):
    """添加检查清单项"""
    mark = '✅' if checked else '☐'
    p = doc.add_paragraph(style='ListItem')
    run = p.add_run(f'{mark} {text}')
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    return p

# ══════════════════════════════════════════════════════════════
# 正式开始：第 3 次课上机实验
# ══════════════════════════════════════════════════════════════

# 标题
title = doc.add_heading('第 3 次课上机实验：Skill 与 Agent 开发', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 元信息
add_para('实验时长：75 分钟', bold=True)
add_para('实验目标：配置 MCP 服务、开发金融数据分析 Skill、创建自定义 Agent、体验 Skill + Agent + MCP 协同工作流')

doc.add_paragraph()  # 分隔

# ══════════════════════════════════════════════════════════════
# 实验环境准备
# ══════════════════════════════════════════════════════════════
add_heading('实验环境准备（5 分钟）', level=1)

add_heading('前置条件检查', level=3)

add_para('验证清单：')

add_table(
    ['检查项', '验证命令', '预期结果', '备注'],
    [
        ['opencode 已安装', 'opencode --version', '显示版本号', '如未安装，参考第1次课'],
        ['Python 已安装', 'python --version', 'Python 3.7+', '必需'],
    ],
    [4, 4, 3.5, 3.5]
)

add_heading('实验目录设置', level=3)

add_code_block('''# 1. 进入项目目录
cd C:\\haichao\\build\\finance-ai-coding

# 2. 创建本次实验的工作目录
mkdir teaching-materials\\session-03\\lab-work -Force

# 3. 进入实验目录
cd teaching-materials\\session-03\\lab-work

# 4. 启动 opencode
opencode''')

add_rich_para('**验证**：')

add_bullet('opencode TUI 界面成功启动')

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验一
# ══════════════════════════════════════════════════════════════
add_heading('实验一：MCP 配置练习（10 分钟）', level=1)

# 1.1
add_heading('1.1 配置 tushare MCP 到项目级 opencode.jsonc', level=2)

add_rich_para('**实验目的**：掌握项目级远程 MCP 的配置方法，理解 MCP 如何让 AI 零代码获取数据')

add_rich_para('**基础概念**：')

add_bullet('MCP（Model Context Protocol）是一套协议，让 AI 能直接调用外部工具，无需编写中间代码')
add_bullet('远程型 MCP（type: "remote"）通过 URL 连接服务，不需要本地安装')
add_bullet('项目级配置放在项目根目录的 opencode.jsonc 中，仅对当前项目生效')
add_bullet('Token 直接写在 MCP URL 中，opencode 会自动连接')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：在 opencode TUI 中输入以下指令：')

add_code_block('''请在当前目录创建 opencode.jsonc 文件，内容如下：

{
    "mcp": {
        "tushareMcp": {
            "type": "remote",
            "url": "https://api.tushare.pro/mcp/?token=5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521"
        }
    }
}''')

add_rich_para('**步骤 2**：观察 AI 的操作：')

add_bullet('AI 使用 write 工具创建 opencode.jsonc 文件')
add_bullet('确认 write 操作（输入 y）')

add_rich_para('**步骤 3**：验证文件创建成功：')

add_code_block('''# 退出 opencode 或另开终端
cat opencode.jsonc''')

add_rich_para('**预期输出**：')

add_code_block('''{
    "mcp": {
        "tushareMcp": {
            "type": "remote",
            "url": "https://api.tushare.pro/mcp/?token=5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521"
        }
    }
}''')

add_rich_para('**步骤 4**：重启 opencode 让 MCP 配置生效：')

add_code_block('''# 重新启动
opencode''')

add_rich_para('**步骤 5**：测试 MCP 功能——输入自然语言指令：')

add_code_block('获取贵州茅台（600519.SH）最近 10 个交易日的日线数据')

add_rich_para('**步骤 6**：观察 AI 行为：')

add_bullet('AI 发现 tushare MCP 工具可用')
add_bullet('AI 直接调用 MCP 工具，不再编写 Python 代码')
add_bullet('数据直接返回，无需运行脚本')

doc.add_paragraph()

# 1.2
add_heading('1.2 对比 MCP 与 Skill 的数据获取方式', level=2)

add_rich_para('**实验目的**：直观感受 MCP 和 Skill 两种数据获取方式的差异')

add_rich_para('**基础概念**：')

add_bullet('Skill 方式：AI 读 SKILL.md → 写 Python 代码 → 运行 → 解析结果（链路长，易出错）')
add_bullet('MCP 方式：AI 直接调用 MCP 工具 → 返回结果（零代码，低延迟）')
add_bullet('选型原则：纯数据获取用 MCP，多步骤分析用 Skill')

add_rich_para('**对比记录**：')

add_table(
    ['对比维度', 'Skill + SDK 方式', 'MCP 方式'],
    [
        ['操作步骤数', '（记录实际步骤数）', '（记录实际步骤数）'],
        ['是否编写 Python 代码', '', ''],
        ['响应速度（主观感受）', '', ''],
        ['出错可能性', '', ''],
        ['适用场景', '', ''],
    ],
    [4, 5.5, 5.5]
)

add_rich_para('**✅ 检查点**：')

add_bullet('tushare MCP 配置成功并能获取数据')
add_bullet('理解 MCP 和 Skill 数据获取的差异')

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验二
# ══════════════════════════════════════════════════════════════
add_heading('实验二：Skill 开发练习（30 分钟）', level=1)

# 2.0
add_heading('2.0 准备：安装 skill-creator 和 skill-improver 技能', level=2)

add_rich_para('**实验目的**：安装后续实验所需的 Skill 开发辅助工具，确保 skill-creator 和 skill-improver 可用')

add_rich_para('**基础概念**：')

add_bullet('**skill-creator**：Anthropic 提供的 Skill 创建辅助工具，可根据需求描述自动生成 SKILL.md 框架，包含 frontmatter、步骤大纲、示例占位符，大幅降低 Skill 开发门槛')
add_bullet('**skill-improver**：Skill 质量改进工具，读取改进计划文件（improvement-plan-{name}.md）并自动合并执行改进建议，支持按优先级分组处理冲突')
add_bullet('这两个 Skill 由老师分享，学生只需将其复制到项目的 .opencode/skills/ 目录即可安装，opencode 在启动时会自动加载该目录下的所有 Skill')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：确认老师在课堂上分享：')

add_bullet('skill-creator')
add_bullet('skill-improver')

add_rich_para('**步骤 2**：将 Skill 文件复制到项目的 .opencode/skills/ 目录。在 PowerShell 中执行（可以手动创建和拷贝）：')

add_code_block('''# 进入项目根目录
cd C:\\haichao\\build\\finance-ai-coding

# 创建目标目录（如已存在则跳过）
mkdir .opencode\\skills\\skill-creator -Force
mkdir .opencode\\skills\\skill-improver -Force

# 复制文件（将 <老师分享路径> 替换为实际路径）
Copy-Item <老师分享路径>\\skill-creator\\SKILL.md .opencode\\skills\\skill-creator\\SKILL.md
Copy-Item <老师分享路径>\\skill-improver\\SKILL.md .opencode\\skills\\skill-improver\\SKILL.md''')

add_rich_para('**步骤 3**：验证安装是否成功：')

add_code_block('''# 检查文件是否存在
ls .opencode\\skills\\skill-creator\\SKILL.md
ls .opencode\\skills\\skill-improver\\SKILL.md''')

add_rich_para('**预期输出**：两个文件均存在，路径分别为：')

add_bullet('.opencode/skills/skill-creator/SKILL.md')
add_bullet('.opencode/skills/skill-improver/SKILL.md')

add_rich_para('**步骤 4**：重启 opencode 以加载新 Skill：')

add_code_block('opencode')

add_rich_para('**步骤 5**：在 opencode TUI 中验证 Skill 可触发——输入以下测试指令：')

add_code_block('请使用 skill-creator 帮我创建一个简单的 Skill')

add_para('观察 AI 是否加载了 skill-creator Skill（日志中会显示相关提示），然后回复"暂不创建"即可退出。')

add_rich_para('**✅ 检查点**：')

add_bullet('skill-creator 的 SKILL.md 已复制到 .opencode/skills/skill-creator/')
add_bullet('skill-improver 的 SKILL.md 已复制到 .opencode/skills/skill-improver/')
add_bullet('重启 opencode 后 skill-creator 可正常触发')

doc.add_paragraph()

# 2.1
add_heading('2.1 使用 skill-creator 创建技术分析 Skill 框架', level=2)

add_rich_para('**实验目的**：学习使用 AI 辅助工具快速生成 SKILL.md 框架，降低 Skill 开发门槛')

add_rich_para('**基础概念**：')

add_bullet('skill-creator 是 Anthropic 提供的 Skill 开发辅助工具，能根据需求描述自动生成 SKILL.md 的基本结构')
add_bullet('生成的框架包含 frontmatter、步骤大纲、示例占位符，开发者只需补充具体细节')
add_bullet('这种"AI 辅助开发"模式是高效构建 Skill 的推荐路径')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：在 opencode TUI 中输入需求描述：')

add_code_block('''请使用 skill-creator 创建一个"股票技术分析 Skill"，功能要求如下：
- 名称：stock-tech-analysis
- 描述：计算股票均线/MACD/RSI等技术指标并生成分析图表，适用于技术分析场景
- 数据获取：优先使用 tushare MCP 获取日K线数据；若 MCP 不可用，则回退至 tushare skill
- 支持计算的指标：5日/10日/20日均线、MACD(12,26,9)、RSI(14)
- 输出：生成包含价格走势和指标的图表（PNG格式）''')

add_rich_para('**步骤 2**：观察 skill-creator 的工作过程：')

add_bullet('AI 加载 skill-creator Skill')
add_bullet('AI 根据需求生成 SKILL.md 框架')
add_bullet('框架包含 frontmatter、步骤大纲、示例占位符')

add_rich_para('**步骤 3**：确认 write 操作，将 SKILL.md 保存到 .opencode/skills/stock-tech-analysis/SKILL.md')

add_rich_para('**步骤 4**：检查生成的框架内容：')

add_code_block('请读取 .opencode/skills/stock-tech-analysis/SKILL.md 的内容')

add_rich_para('**步骤 5**：记录框架的结构要素：')

add_bullet('frontmatter 中 name 和 description 是什么？')
add_bullet('步骤有几个？每步的概述是什么？')
add_bullet('示例和注意事项是否完整？')

add_rich_para('**✅ 检查点**：')

add_bullet('skill-creator 成功触发')
add_bullet('SKILL.md 框架已生成')

doc.add_paragraph()

# 2.2
add_heading('2.2 填充技术指标计算指令和示例代码', level=2)

add_rich_para('**实验目的**：在生成的框架基础上补充具体的指令细节，使 Skill 具备完整的可执行性')

add_rich_para('**基础概念**：')

add_bullet('SKILL.md 的步骤指令需要足够具体，AI 才能据此编写正确的代码')
add_bullet('金融技术指标的计算有标准公式和参数，需要明确写出')
add_bullet('示例代码可以帮助 AI 理解预期的代码风格和输出格式')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：在 opencode TUI 中输入补充指令：')

add_code_block('''请编辑 .opencode/skills/stock-tech-analysis/SKILL.md，补充以下内容：

1. 在"步骤 3：指标计算"中，添加具体的计算指令：
   - 均线：使用 pandas 的 rolling(window).mean() 方法
   - MACD：使用 EMA 计算，参数为 fast=12, slow=26, signal=9
   - RSI：使用 14 日周期，公式为 RSI = 100 - 100/(1+RS)，RS = 平均涨幅/平均跌幅

2. 在"示例"部分，添加示例输入和预期输出：
   - 输入："分析贵州茅台（600519.SH）最近 60 天的技术指标"
   - 预期输出：包含价格、均线、MACD 三列子图的分析图片

3. 在"注意事项"中，添加以下错误处理：
   - 数据不足：MACD 至少需要 35 个交易日数据，RSI 至少需要 15 个交易日
   - 停牌日：检测交易日期是否连续，如有断层用前值填充
   - 除零风险：RSI 计算时平均跌幅可能为 0，需添加保护逻辑''')

add_rich_para('**步骤 2**：观察 AI 的编辑过程：')

add_bullet('AI 使用 edit 工具修改 SKILL.md')
add_bullet('确认 edit 操作')

add_rich_para('**步骤 3**：验证修改后的内容：')

add_code_block('请读取修改后的 SKILL.md，展示完整内容')

add_rich_para('**步骤 4**：检查关键要素是否完整：')

add_bullet('frontmatter 中 name 和 description 正确')
add_bullet('数据获取步骤标注了 MCP 优先、Skill 回退')
add_bullet('均线/MACD/RSI 的计算指令具体清晰')
add_bullet('示例输入输出完整')
add_bullet('错误处理覆盖数据不足、停牌、除零三种情况')

add_rich_para('**✅ 检查点**：')

add_bullet('SKILL.md 内容充实、步骤具体可执行')
add_bullet('错误处理已覆盖至少 3 种金融数据异常')

doc.add_paragraph()

# 2.3
add_heading('2.3 测试 Skill 的触发和执行', level=2)

add_rich_para('**实验目的**：验证自定义 Skill 的自动触发机制和执行流程是否正确')

add_rich_para('**基础概念**：')

add_bullet('Skill 的自动触发依赖于 description 字段与用户输入的语义匹配')
add_bullet('测试时应使用描述中包含的关键词触发，也测试不相关关键词触发作为对照')
add_bullet('执行流程应按照 SKILL.md 中的步骤依次进行')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：重启 opencode 以加载新 Skill：')

add_code_block('opencode')

add_rich_para('**步骤 2**：测试自动触发——输入包含技术分析关键词的指令：')

add_code_block('分析平安银行（000001.SZ）最近 60 天的技术指标，计算均线、MACD 和 RSI')

add_rich_para('**步骤 3**：观察触发行为：')

add_bullet('Skill 是否自动触发？（观察 AI 是否加载了 SKILL.md）')
add_bullet('AI 是否按照步骤执行：获取数据 → 清洗 → 计算指标 → 绘图？')

add_rich_para('**步骤 4**：验证输出文件：')

add_code_block('''ls *.png *.csv *.py
# 应看到技术分析图表文件''')

add_rich_para('**步骤 5**：测试对照——输入不相关的指令：')

add_code_block('读取 swufe_news.csv 文件，统计新闻数量')

add_rich_para('**步骤 6**：确认 Skill 没有被错误触发（这是预期行为）')

add_rich_para('**步骤 7**：记录测试结果：')

add_table(
    ['测试场景', '输入关键词', 'Skill 是否触发', '执行是否正确'],
    [
        ['技术分析（正向）', '技术指标、均线、MACD', '', ''],
        ['数据查询（对照）', '新闻、统计', '', ''],
    ],
    [3.5, 3.5, 3, 5]
)

add_rich_para('**✅ 检查点**：')

add_bullet('技术分析 Skill 在正确场景下自动触发')
add_bullet('执行流程按步骤进行并生成预期输出')
add_bullet('不相关场景下 Skill 未被错误触发')

doc.add_paragraph()

# 2.4
add_heading('2.4 使用 skill-improver 评估质量并改进', level=2)

add_rich_para('**实验目的**：学习使用 skill-improver 对 Skill 进行质量评估，并根据建议迭代改进')

add_rich_para('**基础概念**：')

add_bullet('skill-improver 是质量检查工具，从 description 准确性、内容组织、边界条件三个维度评估 Skill')
add_bullet('它输出的改进建议可以直接指导 SKILL.md 的修改')
add_bullet('迭代优化流程：创建 → 测试 → 评估 → 改进 → 再测试')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：在 opencode TUI 中输入评估请求：')

add_code_block('请使用 skill-improver 评估 .opencode/skills/stock-tech-analysis/SKILL.md 的质量，给出改进建议')

add_rich_para('**步骤 2**：观察评估输出，记录三项评估结果和改进建议：')

add_table(
    ['评估维度', '评分/评价', '改进建议'],
    [
        ['description 准确性', '', ''],
        ['内容组织', '', ''],
        ['边界条件', '', ''],
    ],
    [4, 5.5, 5.5]
)

add_rich_para('**步骤 3**：选取至少 2 条改进建议，让 AI 执行修改：')

add_code_block('''请根据 skill-improver 的建议，改进 SKILL.md：
1. [选择建议 1]
2. [选择建议 2]''')

add_rich_para('**步骤 4**：确认 edit 操作')

add_rich_para('**步骤 5**：重新测试 Skill 触发和执行，验证改进效果')

add_rich_para('**预期结果**：')

add_bullet('skill-improver 输出了评估结果和至少 3 条改进建议')
add_bullet('根据建议修改后 Skill 运行效果有所提升')

add_rich_para('**✅ 检查点**：')

add_bullet('skill-improver 成功运行并输出评估结果')
add_bullet('根据至少 2 条建议完成了改进')
add_bullet('改进后 Skill 功能正常')

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验三
# ══════════════════════════════════════════════════════════════
add_heading('实验三：Agent 创建练习（20 分钟）', level=1)

# 3.1
add_heading('3.1 使用 Markdown 方式创建数据合规检查子代理', level=2)

add_rich_para('**实验目的**：掌握使用 Markdown 方式创建子代理，理解 frontmatter 各字段的含义和作用')

add_rich_para('**基础概念**：')

add_bullet('Agent 是独立的智能体，有自己的 prompt、工具权限和运行模式')
add_bullet('子代理（mode: subagent）由主代理委派调用，自动匹配基于 description 字段')
add_bullet('tools 字段控制代理可以使用的工具，限制工具可以缩小代理的行为范围，使其更专注')
add_bullet('Markdown 方式与 Skill 风格统一，便于版本管理，推荐优先使用')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：在 opencode TUI 中输入创建指令：')

add_code_block('''请在 .opencode/agents/ 目录下创建 data-auditor.md 文件，内容如下：

---
description: 检查股票数据中的异常值，输出结构化合规报告
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
---

你是金融数据合规检查专员。读取给定的股票 CSV 数据，检查以下两类异常：
1. 负价格：收盘价 < 0
2. 涨跌幅超限：单日涨跌幅超过 ±10%

输出格式为 Markdown 表格，按异常类型分类列出。
若无异常，输出"数据合规，未发现异常"。''')

add_rich_para('**步骤 2**：确认 write 操作')

add_rich_para('**步骤 3**：验证文件创建：')

add_code_block('请读取 .opencode/agents/data-auditor.md 的内容')

add_rich_para('**步骤 4**：分析 frontmatter 各字段的作用：')

add_table(
    ['字段', '值', '作用'],
    [
        ['description', '', ''],
        ['mode', '', ''],
        ['tools.bash', '', ''],
        ['tools.write', '', ''],
    ],
    [4, 5.5, 5.5]
)

add_rich_para('**✅ 检查点**：')

add_bullet('data-auditor.md 已创建在正确位置')
add_bullet('frontmatter 各字段设置合理')

doc.add_paragraph()

# 3.2
add_heading('3.2 测试代理功能', level=2)

add_rich_para('**实验目的**：验证子代理能否正确执行数据合规检查任务')

add_rich_para('**基础概念**：')

add_bullet('子代理由主代理根据 description 自动委派，也可在对话中手动请求')
add_bullet('子代理只能使用 tools 中允许的工具（如本例中只有 bash 和 read）')
add_bullet('代理的 prompt 定义了它的行为逻辑和输出格式要求')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：确保有测试数据——如果要使用贵州茅台的 CSV 数据，先获取：')

add_code_block('获取贵州茅台（600519.SH）最近 60 天的日线数据并保存为 moutai_daily.csv')

add_rich_para('**步骤 2**：触发数据合规检查代理：')

add_code_block('请检查 moutai_daily.csv 的数据合规性，委派 data-auditor 代理执行')

add_rich_para('**步骤 3**：观察代理行为：')

add_bullet('主代理是否识别到数据合规检查需求？')
add_bullet('是否委派了 data-auditor 子代理？')
add_bullet('子代理是否按照 prompt 中的三类异常进行检查？')
add_bullet('输出格式是否为 Markdown 表格？')

add_rich_para('**步骤 4**：记录检查结果：')

add_table(
    ['异常类型', '是否发现异常', '详情'],
    [
        ['负价格', '', ''],
        ['涨跌幅超限', '', ''],
    ],
    [5, 5, 5]
)

add_rich_para('**✅ 检查点**：')

add_bullet('data-auditor 代理成功触发并执行')
add_bullet('输出格式符合预期（Markdown 表格或"数据合规"）')

doc.add_paragraph()

# 3.3
add_heading('3.3 修改 tools 配置，对比行为差异', level=2)

add_rich_para('**实验目的**：理解 tools 配置对代理行为范围的影响')

add_rich_para('**基础概念**：')

add_bullet('tools 字段限制了代理可以使用的工具')
add_bullet('设置 write: false 意味着代理不能创建或覆盖文件')
add_bullet('设置 edit: false 意味着代理不能修改已有文件')
add_bullet('合理限制工具范围可以让代理更专注于核心任务，避免误操作')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：修改 data-auditor.md，将 tools 中 bash 和 write 都设为 true：')

add_code_block('''请编辑 .opencode/agents/data-auditor.md，将 frontmatter 中的 tools 修改为：
tools:
  bash: true
  read: true
  write: true
  edit: false''')

add_rich_para('**步骤 2**：确认 edit 操作')

add_rich_para('**步骤 3**：重启 opencode 并重新测试：')

add_code_block('请检查 moutai_daily.csv 的数据合规性，委派 data-auditor 代理执行，同时将合规报告保存为 audit_report.md')

add_rich_para('**步骤 4**：观察行为差异：')

add_bullet('之前配置（write: false）：代理能否保存报告文件？')
add_bullet('修改后配置（write: true）：代理能否保存报告文件？')

add_rich_para('**步骤 5**：记录对比结果：')

add_table(
    ['配置', 'write 权限', '能否保存审计报告'],
    [
        ['修改前', 'false', ''],
        ['修改后', 'true', ''],
    ],
    [5, 5, 5]
)

add_rich_para('**✅ 检查点**：')

add_bullet('理解 tools 配置如何影响代理行为')
add_bullet('修改配置后代理行为确实发生变化')

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验四
# ══════════════════════════════════════════════════════════════
add_heading('实验四：构建"股票日报自动生成系统"——主代理 + 子代理协同（15 分钟）', level=1)

add_note('对应 lecture.md 案例四。本实验将创建一个完整的日报系统：一个主代理负责理解和编排任务，两个子代理分别负责数据采集和报告生成。')

# 4.1
add_heading('4.1 创建数据采集子代理', level=2)

add_rich_para('**实验目的**：创建专门负责金融数据采集的子代理，理解子代理的设计思路和工具配置')

add_rich_para('**基础概念**：')

add_bullet('子代理（mode: subagent）由主代理根据 description 自动委派调用')
add_bullet('数据采集代理的核心任务是通过 MCP 或 Skill 获取结构化金融数据')
add_bullet('给予 bash: true 权限，使其可在 MCP 不可用时回退到 tushare Skill 编写 Python 代码获取数据')
add_bullet('不给予 write: true 和 edit: true，避免采集过程中意外修改项目文件')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：了解要创建的文件。以下为 .opencode/agents/data-collector.md 的完整内容，请先阅读理解：')

add_code_block('''---
description: 采集股票指数行情和板块涨跌数据
mode: subagent
tools:
  bash: true
  read: true
  write: false
  edit: false
---

你是金融数据采集专员。收到采集任务后，按以下流程执行：

1. 明确数据需求：用户需要哪些指数、板块或个股的数据？时间范围是什么？
2. 优先使用 tushare MCP 直接获取数据（零代码、低延迟）
3. 如果 MCP 不可用或未配置，使用 tushare skill（编写 Python 代码调用 SDK）
4. 对获取的数据做基本校验：数据是否为空、日期是否合理、字段是否完整

输出格式为 JSON，结构如下：

{
  "indices": [
    {"name": "上证指数", "code": "000001.SH", "close": 3200.5, "pct_chg": 0.5},
    {"name": "深证成指", "code": "399001.SZ", "close": 10500.3, "pct_chg": -0.3}
  ],
  "sectors": [
    {"name": "银行", "pct_chg": 1.2},
    {"name": "房地产", "pct_chg": -0.8}
  ],
  "data_source": "tushare_mcp",
  "collect_time": "2026-06-12 15:30:00"
}

注意：
- 如果用户未指定具体指数，默认采集上证指数和深证成指
- 数据时间范围未指定时，默认取最近 1 个交易日
- 始终标注数据来源（mcp 或 skill）和采集时间''')

add_rich_para('**步骤 2**：在 opencode TUI 中输入以下指令创建文件（将步骤 1 中的完整内容粘贴到方括号位置）：')

add_code_block('''请在 .opencode/agents/ 目录下创建 data-collector.md，内容如下：

[粘贴步骤 1 中的完整文件内容]''')

add_rich_para('**步骤 3**：确认 write 操作（输入 y）')

add_rich_para('**步骤 4**：验证文件创建成功：')

add_code_block('请读取 .opencode/agents/data-collector.md 的内容，确认文件已正确创建')

add_rich_para('**步骤 5**：分析该代理的设计要点，填写以下表格：')

add_table(
    ['设计要点', '你的理解'],
    [
        ['为什么 tools 中 bash 设为 true？', ''],
        ['为什么 write 设为 false？', ''],
        ['为什么定义了 JSON 输出格式？', ''],
        ['为什么要标注数据来源和采集时间？', ''],
    ],
    [7, 8]
)

add_rich_para('**✅ 检查点**：')

add_bullet('data-collector.md 已创建在 .opencode/agents/ 目录下')
add_bullet('frontmatter 中 mode 为 subagent，tools 配置合理')
add_bullet('prompt 中包含双通道策略（MCP 优先、Skill 回退）')

doc.add_paragraph()

# 4.2
add_heading('4.2 创建报告生成子代理', level=2)

add_rich_para('**实验目的**：创建专门负责撰写日报的子代理，理解"数据采集"与"报告生成"职责分离的设计思路')

add_rich_para('**基础概念**：')

add_bullet('报告生成代理只负责将结构化数据转化为可读文案，不负责数据采集')
add_bullet('给予 write: true 权限，使其可以将生成的日报保存为文件')
add_bullet('不给予 bash: true，使其专注于文本撰写而非代码执行——职责越单一，输出越稳定')
add_bullet('日报格式统一为 Markdown，便于阅读和版本管理')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：了解要创建的文件。以下为 .opencode/agents/report-writer.md 的完整内容，请先阅读理解：')

add_code_block('''---
description: 根据采集的金融数据撰写结构化日报
mode: subagent
tools:
  bash: false
  read: true
  write: true
  edit: false
---

你是金融分析师，专注于根据数据撰写市场日报。

收到数据后，按以下结构撰写 Markdown 格式日报：

# 股市日报 - {日期}

## 行情概览
- 用 2-3 句话概括当日市场整体表现
- 列出主要指数收盘价和涨跌幅

## 板块分析
- 涨幅前 3 板块及简要原因分析
- 跌幅前 3 板块及简要原因分析

## 重点关注
- 提示 1-2 个值得关注的信号或事件
- 给出简短的操作建议（仅供参考）

## 免责声明
- 声明本报告仅为数据分析结果，不构成投资建议

格式要求：
- 使用二级标题（##）分隔各节
- 数据用列表形式呈现
- 总字数控制在 500 字以内
- 结论段落不超过 100 字

将生成的日报保存为文件，命名为 daily_report_{日期}.md''')

add_rich_para('**步骤 2**：在 opencode TUI 中输入以下指令创建文件（将步骤 1 中的完整内容粘贴到方括号位置）：')

add_code_block('''请在 .opencode/agents/ 目录下创建 report-writer.md，内容如下：

[粘贴步骤 1 中的完整文件内容]''')

add_rich_para('**步骤 3**：确认 write 操作')

add_rich_para('**步骤 4**：验证文件创建成功：')

add_code_block('请读取 .opencode/agents/report-writer.md 的内容，确认文件已正确创建')

add_rich_para('**步骤 5**：对比两个子代理的设计差异：')

add_table(
    ['对比维度', 'data-collector', 'report-writer'],
    [
        ['核心职责', '', ''],
        ['bash 权限', '', ''],
        ['write 权限', '', ''],
        ['输出格式', '', ''],
        ['为什么权限不同？', '', ''],
    ],
    [3.5, 5.75, 5.75]
)

add_rich_para('**✅ 检查点**：')

add_bullet('report-writer.md 已创建在 .opencode/agents/ 目录下')
add_bullet('frontmatter 中 mode 为 subagent，tools 配置与 data-collector 互补')
add_bullet('prompt 中包含完整的日报结构模板')

doc.add_paragraph()

# 4.3
add_heading('4.3 配置日报主代理', level=2)

add_rich_para('**实验目的**：创建日报主代理，理解主代理的角色——负责理解用户需求、拆分子任务、委派子代理、汇总结果')

add_rich_para('**基础概念**：')

add_bullet('主代理（mode: primary）是用户直接交互的入口，可通过 Tab 键切换选择')
add_bullet('主代理的 prompt 要明确描述任务分解和委派逻辑，否则 AI 可能自己直接做而非委派')
add_bullet('主代理需要知道有哪些子代理可用，以及何时委派给哪个子代理')
add_bullet('本实验使用 Markdown 配置主代理；也可选用 JSON 方式在 opencode.jsonc 中配置')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：了解要创建的文件。以下为 .opencode/agents/daily-report.md 的完整内容，请先阅读理解：')

add_code_block('''---
description: 生成股票市场日报，协调数据采集和报告撰写
mode: primary
---

你是日报主编，负责协调生成市场日报。

收到用户的日报请求后，按以下步骤执行：

**第 1 步：理解需求**
- 用户想要哪天的日报？如果未指定，默认为最近的交易日
- 是否需要特定板块或个股的数据？

**第 2 步：委派数据采集**
- 将数据需求整理后，委派给 data-collector 子代理
- 明确告知需要采集的指数、板块和时间范围
- 等待 data-collector 返回 JSON 格式的数据

**第 3 步：委派报告撰写**
- 将 data-collector 返回的数据传递给 report-writer 子代理
- 明确告知日报日期
- 等待 report-writer 生成 Markdown 格式的日报

**第 4 步：汇总输出**
- 检查报告内容是否完整（包含行情概览、板块分析、重点关注、免责声明）
- 如有缺失，补充完善
- 向用户展示最终日报内容

注意事项：
- 不要自己采集数据或撰写报告，必须委派给对应的子代理
- 如果子代理执行失败，尝试用更简单的需求重新委派
- 最终输出应包含日报全文和保存路径''')

add_rich_para('**步骤 2**：在 opencode TUI 中输入以下指令创建文件（将步骤 1 中的完整内容粘贴到方括号位置）：')

add_code_block('''请在 .opencode/agents/ 目录下创建 daily-report.md，内容如下：

[粘贴步骤 1 中的完整文件内容]''')

add_rich_para('**步骤 3**：确认 write 操作')

add_rich_para('**步骤 4**：验证文件创建成功：')

add_code_block('请读取 .opencode/agents/daily-report.md 的内容，确认文件已正确创建')

add_rich_para('**步骤 5**：确认三个代理文件都已就绪。退出 opencode 或另开终端执行：')

add_code_block('ls .opencode\\agents\\')

add_para('应看到：data-collector.md、data-auditor.md、report-writer.md、daily-report.md')

add_rich_para('**✅ 检查点**：')

add_bullet('daily-report.md 已创建在 .opencode/agents/ 目录下')
add_bullet('frontmatter 中 mode 为 primary，表示可作为主代理切换使用')
add_bullet('prompt 中明确描述了四步工作流程和数据委派逻辑')

doc.add_paragraph()

# 4.4
add_heading('4.4 测试完整的日报生成流程', level=2)

add_rich_para('**实验目的**：验证主代理 + 子代理协同机制，体验从数据采集到报告生成的端到端流程')

add_rich_para('**基础概念**：')

add_bullet('主代理切换方式：在 opencode TUI 中按 Tab 键循环切换可用的主代理')
add_bullet('主代理会根据 description 自动识别何时委派子代理')
add_bullet('完整数据流：用户 → 日报主代理 → data-collector（获取数据）→ report-writer（生成报告）→ 日报主代理 → 用户')

add_rich_para('**操作步骤**：')

add_rich_para('**步骤 1**：重启 opencode 以加载所有新建的代理：')

add_code_block('opencode')

add_rich_para('**步骤 2**：按 Tab 键切换到日报主代理，直到底部状态栏显示 daily-report（日报主编）')

add_rich_para('**步骤 3**：输入日报请求：')

add_code_block('生成今日股市日报')

add_rich_para('**步骤 4**：观察完整的协同执行流程，依次记录各阶段行为：')

add_table(
    ['执行阶段', '观察到的行为', '是否符合预期'],
    [
        ['1. 主代理理解需求', '主代理是否识别需要采集数据和撰写报告？', ''],
        ['2. 委派 data-collector', '是否将采集任务委派给了 data-collector？', ''],
        ['3. data-collector 执行', '使用了 MCP 还是 Skill 获取数据？返回了 JSON 吗？', ''],
        ['4. 委派 report-writer', '是否将数据和撰写任务委派给了 report-writer？', ''],
        ['5. report-writer 执行', '是否生成了 Markdown 格式的日报？保存了文件吗？', ''],
        ['6. 主代理汇总', '最终输出是否完整展示日报内容？', ''],
    ],
    [3.5, 7, 5.5]
)

add_rich_para('**步骤 5**：验证生成的日报文件：')

add_code_block('请读取刚才生成的日报文件内容')

add_rich_para('**步骤 6**：检查日报内容是否包含以下必要部分：')

add_bullet('标题（含日期）')
add_bullet('行情概览')
add_bullet('板块分析')
add_bullet('重点关注')
add_bullet('免责声明')

add_rich_para('**步骤 7**：尝试自定义需求，再次生成：')

add_code_block('生成今日股市日报，重点关注银行和科技板块，不要房地产板块')

add_rich_para('**步骤 8**：观察主代理是否能正确传递定制需求给子代理：')

add_table(
    ['定制需求', '是否传递给了对应子代理', '子代理是否响应了定制需求'],
    [
        ['重点关注银行和科技板块', '', ''],
        ['不要房地产板块', '', ''],
    ],
    [5, 5, 5]
)

add_rich_para('**预期结果**：')

add_bullet('按 Tab 键可切换到 daily-report 主代理')
add_bullet('主代理按流程依次委派 data-collector 和 report-writer')
add_bullet('最终生成包含完整结构的 Markdown 日报文件')

add_rich_para('**✅ 检查点**：')

add_bullet('成功切换到日报主代理')
add_bullet('主代理正确委派子代理，未自己直接采集数据或撰写报告')
add_bullet('日报文件生成且内容完整')

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验总结与验证
# ══════════════════════════════════════════════════════════════
add_heading('实验总结与验证（5 分钟）', level=1)

add_heading('验证清单', level=3)

add_table(
    ['实验内容', '完成状态', '验证结果'],
    [
        ['配置 tushare MCP 到 opencode.jsonc', '✅/❌', ''],
        ['通过 MCP 获取股票数据', '✅/❌', ''],
        ['对比 MCP 与 Skill 方式获取数据', '✅/❌', ''],
        ['安装 skill-creator 和 skill-improver 技能', '✅/❌', ''],
        ['使用 skill-creator 创建 Skill 框架', '✅/❌', ''],
        ['充实 Skill 内容（指令 + 示例 + 错误处理）', '✅/❌', ''],
        ['测试 Skill 触发和执行', '✅/❌', ''],
        ['使用 skill-improver 评估并改进', '✅/❌', ''],
        ['使用 Markdown 方式创建子代理', '✅/❌', ''],
        ['测试代理功能', '✅/❌', ''],
        ['修改 tools 配置对比行为差异', '✅/❌', ''],
        ['创建 data-collector 子代理', '✅/❌', ''],
        ['创建 report-writer 子代理', '✅/❌', ''],
        ['配置 daily-report 主代理', '✅/❌', ''],
        ['测试完整的日报生成流程', '✅/❌', ''],
    ],
    [8, 3.5, 3.5]
)

add_heading('实验成果展示', level=3)

add_para('退出 opencode 或另开终端，查看生成的文件：')

add_code_block('''ls
ls .opencode\\agents\\
ls .opencode\\skills\\stock-tech-analysis\\''')

add_para('应包含的文件：')

add_table(
    ['文件', '说明'],
    [
        ['opencode.jsonc', 'MCP 配置文件'],
        ['.opencode/skills/skill-creator/SKILL.md', 'Skill 创建辅助工具'],
        ['.opencode/skills/skill-improver/SKILL.md', 'Skill 改进辅助工具'],
        ['.opencode/skills/stock-tech-analysis/SKILL.md', '技术分析 Skill'],
        ['.opencode/agents/data-auditor.md', '数据合规检查代理'],
        ['.opencode/agents/data-collector.md', '数据采集子代理'],
        ['.opencode/agents/report-writer.md', '报告生成子代理'],
        ['.opencode/agents/daily-report.md', '日报主代理'],
        ['moutai_daily.csv', '茅台日线数据（如果生成）'],
        ['*.png', '技术分析图表（如果生成）'],
        ['audit_report.md', '合规报告（如果生成）'],
        ['daily_report_*.md', '日报文件（如果生成）'],
    ],
    [7, 8]
)

add_heading('实验反思', level=3)

add_numbered('MCP vs Skill：', 1)
add_bullet('MCP 的零代码数据获取体验如何？什么场景下更优？', level=1)
add_bullet('Skill 方式的代码执行有什么 MCP 不具备的优势？', level=1)

add_numbered('Skill 开发流程：', 2)
add_bullet('skill-creator 生成的框架质量如何？需要多少手动补充？', level=1)
add_bullet('skill-improver 的建议是否切实有用？', level=1)

add_numbered('Agent 的价值：', 3)
add_bullet('子代理相比在主代理中直接描述任务，有什么优势？', level=1)
add_bullet('tools 权限控制对代理行为有何影响？', level=1)

add_numbered('协同架构：', 4)
add_bullet('主代理 + 子代理的分工协作体验如何？主代理是否正确委派而非自己直接做？', level=1)
add_bullet('data-collector 和 report-writer 的权限差异设计是否合理？', level=1)
add_bullet('遇到了哪些困难？如何解决？', level=1)

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验常见问题
# ══════════════════════════════════════════════════════════════
add_heading('实验常见问题', level=1)

add_rich_para('**Q1: MCP 配置后 AI 仍然写 Python 代码获取数据？**')

add_para('原因可能：opencode 未重启、配置文件格式有误、MCP 连接失败。解决方法：')

add_numbered('确认已重启 opencode 会话', 1)
add_numbered('检查 cat opencode.jsonc 确保格式正确', 2)
add_numbered('在指令中明确指定："使用 tushare MCP 获取数据，不要写 Python 代码"', 3)

add_rich_para('**Q2: skill-creator 没有触发？**')

add_para('原因可能：skill-creator 未安装、description 匹配失败。解决方法：')

add_numbered('确认 skill-creator 已安装：ls .opencode\\skills\\skill-creator\\SKILL.md', 1)
add_numbered('使用明确的指令："请使用 skill-creator 创建一个..."', 2)
add_numbered('手动加载：在指令中提及"skill-creator"', 3)

add_rich_para('**Q3: 自定义 Agent 没有被自动调用？**')

add_para('原因可能：description 过于宽泛或过窄、mode 设置不对。解决方法：')

add_numbered('检查 description 是否准确描述了触发场景', 1)
add_numbered('确认 mode 设为 subagent', 2)
add_numbered('在主代理对话中明确请求委派："委派 data-auditor 代理执行数据检查"', 3)

add_rich_para('**Q4: 技术指标计算报错数据不足？**')

add_para('原因：MACD 需要至少 35 个交易日、RSI 需要至少 15 个交易日。解决方法：')

add_numbered('增大时间范围（如改为 90 天或 120 天）', 1)
add_numbered('在 SKILL.md 的注意事项中添加数据量检查逻辑', 2)
add_numbered('让 AI 在代码中添加数据量校验并提供友好提示', 3)

add_rich_para('**Q5: MCP 连接超时？**')

add_para('原因可能：网络问题、token 无效、tushare 服务暂时不可用。解决方法：')

add_numbered('检查网络连接', 1)
add_numbered('验证 MCP 配置：cat opencode.jsonc', 2)
add_numbered('等待后重试', 3)
add_numbered('若 MCP 不可用，回退到 Skill + SDK 方式获取数据', 4)

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# 实验延伸任务
# ══════════════════════════════════════════════════════════════
add_heading('实验延伸任务（可选）', level=1)

add_rich_para('**任务一：用 JSON 方式配置代理**')

add_para('参照实验三的 Markdown 配置，在 opencode.jsonc 中用 JSON 方式创建一个等效的 data-auditor-json 代理，对比两种配置的效果差异。')

add_rich_para('**任务二：添加风控预警子代理**')

add_para('在 .opencode/agents/risk-monitor.md 中创建一个风控预警子代理，用于检测个股异常波动（涨跌幅超限、成交量异常放大等），并将其集成到日报主代理的工作流中，形成"数据采集 → 报告撰写 → 风控预警"三步协同。')

add_rich_para('**任务三：优化 stock-tech-analysis Skill**')

add_bullet('添加布林带指标计算')
add_bullet('优化 description 提升触发准确率')
add_bullet('添加"数据缓存"逻辑（避免重复请求 API）')
add_bullet('使用 skill-improver 再次评估改进效果')

doc.add_paragraph()
add_para('实验结束，开始课后作业！', bold=True)

# ── 保存 ──
output_path = r"C:\haichao\teaching\2026-finance-ai\session-03\lab.docx"
doc.save(output_path)
print(f"Word 文档已保存到: {output_path}")
