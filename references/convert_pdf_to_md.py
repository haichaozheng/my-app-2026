import pymupdf
import re

pdf_path = r"C:\haichao\teaching\2026-fall\references\build caree in AI era.pdf"
output_md = r"C:\haichao\teaching\2026-fall\references\build-career-in-ai-era.md"

doc = pymupdf.open(pdf_path)

# Extract lines with position/font info, sorted by y
all_pages = []
for i in range(doc.page_count):
    page = doc[i]
    page_num = i + 1
    d = page.get_text("dict")
    
    lines = []
    for block in d["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(span["text"] for span in spans).strip()
            if not text:
                continue
            font_size = max(span["size"] for span in spans)
            font_name = spans[0].get("font", "")
            x0 = line["bbox"][0]
            y0 = line["bbox"][1]
            y1 = line["bbox"][3]
            
            # Classify
            ltype = "body"
            # First check: skip known title/footer texts regardless of font
            if text in (
                "Three Steps to Career Growth",
                "Learning Technical Skills For a Promising AI Career",
                "Should you Learn Math to Get a Job in AI?",
                "Should You Learn Math to Get a Job in AI?",
                "Scoping Successful AI Projects",
                "Finding Projects that Compliment Your Career Goals",
                "Finding Projects that Complement Your Career Goals",
                "Building a Portfolio of Projects That Shows Skill Progression",
                "A Simple Framework for Starting You AI Job Search",
                "Using Informational Interviews to Find the Right Job",
                "Finding the Right AI Job For You",
                "Keys to Building a Career in AI",
                "Overcoming Imposter Syndrome",
                "Overcoming Uncertainty",
                "Coding AI Is the New Literacy",
                "Make Every Day Count",
                "Introduction",
                "Final Thoughts",
            ):
                ltype = "skip"
            elif re.match(r'^PAGE \d+$', text) or font_size < 7:
                ltype = "skip"
            elif font_size >= 17 and "Poppins-Bold" in font_name:
                ltype = "step"
            elif font_size >= 14 and "Poppins-Bold" in font_name:
                ltype = "skip"  # Section labels
            elif font_size >= 14 and "Inter-Regular" in font_name:
                ltype = "sidebar"
            elif "Poppins-Medium" in font_name:
                ltype = "callout"
            elif y0 < 58 and "Poppins-Bold" in font_name:
                ltype = "skip"  # Footer
            elif re.match(r'^CHAPTER \d+$', text):
                ltype = "skip"
            elif text in ("LEARNING", "PROJECTS", "JOBS", "JOB"):
                ltype = "skip"
            # Skip diagram labels on page 6
            elif page_num == 6 and x0 > 50:
                ltype = "skip"
            # Skip diagram labels on pages 25-26
            elif page_num in (25, 26) and text in ("TECH", "FINANCIAL SERVICES", "ANALYST",
                    "MACHINE LEARNING ENGINEER", "Role & Industry Switch",
                    "Role Switch", "Industry Switch", "Job Search",
                    "Job", "MACHINE LEARNING", "Search", "ENGINEER",
                    "FINANCIAL", "SERVICES"):
                ltype = "skip"
            # Skip standalone checkmarks
            elif text == "✓":
                ltype = "skip"
            # Skip footer chapter titles
            elif text in (
                "Three Steps to Career Growth",
                "Learning Technical Skills For a Promising AI Career",
                "Should you Learn Math to Get a Job in AI?",
                "Should You Learn Math to Get a Job in AI?",
                "Scoping Successful AI Projects",
                "Finding Projects that Compliment Your Career Goals",
                "Finding Projects that Complement Your Career Goals",
                "Building a Portfolio of Projects That Shows Skill Progression",
                "A Simple Framework for Starting You AI Job Search",
                "Using Informational Interviews to Find the Right Job",
                "Finding the Right AI Job For You",
                "Keys to Building a Career in AI",
                "Overcoming Imposter Syndrome",
                "Overcoming Uncertainty",
                "Coding AI Is the New Literacy",
                "Make Every Day Count",
                "Introduction",
                "Ready, Fire, Aim",
            ):
                ltype = "skip"
            # Skip standalone numbers on page 27 (diagram labels)
            elif page_num == 27 and re.match(r'^\d+$', text):
                ltype = "skip"
            
            lines.append({
                "text": text,
                "type": ltype,
                "y": y0,
                "y_end": y1,
                "x": x0,
                "size": font_size,
                "font": font_name,
            })
    
    lines.sort(key=lambda l: l["y"])
    all_pages.append(lines)

page_count = doc.page_count
doc.close()

# Skip title pages, TOC, etc.
skip_pages = {1, 2, 3, 5, 8, 12, 14, 17, 21, 24, 28, 31, 34, 37, 41}

chapter_headers = {
    4: "# Introduction: Coding AI Is the New Literacy",
    6: "# Chapter 1. Three Steps to Career Growth",
    9: "# Chapter 2. Learning Technical Skills for a Promising AI Career",
    13: "# Chapter 3. Should You Learn Math to Get a Job in AI?",
    15: "# Chapter 4. Scoping Successful AI Projects",
    18: "# Chapter 5. Finding Projects that Complement Your Career Goals",
    22: "# Chapter 6. Building a Portfolio of Projects that Shows Skill Progression",
    25: "# Chapter 7. A Simple Framework for Starting Your AI Job Search",
    29: "# Chapter 8. Using Informational Interviews to Find the Right Job",
    32: "# Chapter 9. Finding the Right AI Job for You",
    35: "# Chapter 10. Keys to Building a Career in AI",
    38: "# Chapter 11. Overcoming Imposter Syndrome",
    40: "# Final Thoughts: Make Every Day Count",
}

# Fix encoding
def clean(text):
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2014', '—').replace('\u2013', '–')
    text = text.replace('\u2026', '…')
    text = text.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    return text

def merge_paragraphs(lines):
    """Merge text lines into paragraphs using y-gap detection"""
    result = []
    current_texts = []
    current_type = None
    prev_y_end = None
    
    for line in lines:
        if line["type"] == "skip":
            # Don't flush paragraph, just skip this line
            continue
        
        text = line["text"]
        ltype = line["type"]
        y = line["y"]
        y_end = line["y_end"]
        
        # Determine if new paragraph needed
        need_new = False
        if current_type is None:
            current_type = ltype
        elif ltype != current_type:
            need_new = True
        elif prev_y_end is not None:
            gap = y - prev_y_end
            # Lines within a paragraph have gap < ~25
            # Paragraph breaks have gap >= 25
            if gap >= 25:
                need_new = True
        
        if need_new:
            if current_texts:
                result.append((current_type or "body", " ".join(current_texts)))
            current_texts = [text]
            current_type = ltype
        else:
            current_texts.append(text)
        
        prev_y_end = y_end
    
    if current_texts:
        result.append((current_type or "body", " ".join(current_texts)))
    
    return result

# Build markdown
md = []

# Title
md.append("# How to Build Your Career in AI")
md.append("")
md.append("**A Simple Guide**")
md.append("")
md.append("*By Andrew Ng, Founder of DeepLearning.AI*")
md.append("")
md.append('> "AI is the new electricity. It will transform and improve all areas of human life."')
md.append("> — Andrew Ng")
md.append("")
md.append("---")
md.append("")

# TOC
md.append("## Table of Contents")
md.append("")
toc = [
    "Introduction: Coding AI Is the New Literacy",
    "Chapter 1: Three Steps to Career Growth",
    "Chapter 2: Learning Technical Skills for a Promising AI Career",
    "Chapter 3: Should You Learn Math to Get a Job in AI?",
    "Chapter 4: Scoping Successful AI Projects",
    "Chapter 5: Finding Projects that Complement Your Career Goals",
    "Chapter 6: Building a Portfolio of Projects that Shows Skill Progression",
    "Chapter 7: A Simple Framework for Starting Your AI Job Search",
    "Chapter 8: Using Informational Interviews to Find the Right Job",
    "Chapter 9: Finding the Right AI Job for You",
    "Chapter 10: Keys to Building a Career in AI",
    "Chapter 11: Overcoming Imposter Syndrome",
    "Final Thoughts: Make Every Day Count",
]
for item in toc:
    md.append(f"- {item}")
md.append("")
md.append("---")
md.append("")

# Page 27 manual content (diagram is too complex to parse)
page27 = """There's a lot we don't know about the future: When will we cure Alzheimer's disease? Who will win the next election? Or, in a business context, how many customers will we have next year? With so many changes going on in the world, many people are feeling stressed about the future, especially when it comes to finding a job. I have a practice that helps me regain a sense of control. Faced with uncertainty, I try to:

1. Make a list of plausible scenarios, acknowledging that I don't know which will come to pass.
2. Create a plan of action for each scenario.
3. Start executing actions that seem reasonable.
4. Review scenarios and plans periodically as the future comes into focus.

For example, during the Covid-19 pandemic back in March 2020, I did this scenario planning exercise. I imagined quick (three months), medium (one year), and slow (two years) recoveries from Covid-19 and made plans for managing each case. These plans have helped me prioritize where I can.

The same method can apply to personal life, too. If you're not sure you'll pass an exam, get a job offer, or be granted a visa — all of which can be stressful — you can write out what you'd do in each of the likely scenarios. Thinking through the possibilities and following through on plans can help you navigate the future effectively no matter what it brings.

**Bonus:** With training in AI and statistics, you can calculate a probability for each scenario. I'm a fan of the Superforecasting methodology, in which the judgments of many experts are synthesized into a probability estimate."""

for pg_idx in range(page_count):
    pg_num = pg_idx + 1
    if pg_num in skip_pages:
        continue
    
    if pg_num == 27:
        md.append(page27)
        md.append("")
        continue
    
    lines = all_pages[pg_idx]
    
    if pg_num in chapter_headers:
        md.append(chapter_headers[pg_num])
        md.append("")
    
    paragraphs = merge_paragraphs(lines)
    
    for ptype, text in paragraphs:
        text = clean(text).strip()
        if not text:
            continue
        
        if ptype == "step":
            md.append(f"### {text}")
            md.append("")
        elif ptype == "sidebar":
            md.append(f"**{text}**")
            md.append("")
        elif ptype == "callout":
            # Callout header - output as regular text (will merge with following paragraph naturally)
            md.append(text)
            md.append("")
        else:
            # Remove any remaining ✓ marks from text
            text = text.replace('✓', '').strip()
            text = re.sub(r'\s+', ' ', text)
            if text:
                md.append(text)
                md.append("")

final_text = "\n".join(md)
final_text = re.sub(r'\n{3,}', '\n\n', final_text)
final_text = final_text.strip() + "\n"

with open(output_md, "w", encoding="utf-8") as f:
    f.write(final_text)

print(f"Done! {len(final_text)} chars, {final_text.count(chr(10))} lines")
