#!/usr/bin/env python3
"""Convert The Founder's Playbook PDF to clean Markdown."""

import pymupdf
import re

PDF_PATH = "The Founder\u2019s Playbook.pdf"
OUTPUT_PATH = "the-founders-playbook.md"

# Chapter divider pages (1-indexed) - skip these, content starts on next page
DIVIDER_PAGES = {3, 5, 8, 15, 21, 25, 31, 33}
# Skip page 36 (just "claude.ai")
SKIP_PAGES = {36}
# Page 11 has a table we need to filter
TABLE_PAGE = 11

# Chapter titles (in order of appearance on content pages)
CHAPTER_TITLES = {
    4: ("Chapter 1", "The startup lifecycle, rebooted for 2026"),
    6: ("Chapter 2", "What it means to be a founder is changing"),
    7: ("Chapter 2", None),
    9: ("Chapter 3", "Idea Stage"),
    10: ("Chapter 3", None),
    11: ("Chapter 3", None),
    12: ("Chapter 3", None),
    13: ("Chapter 3", None),
    14: ("Chapter 3", None),
    16: ("Chapter 4", "MVP Stage"),
    17: ("Chapter 4", None),
    18: ("Chapter 4", None),
    19: ("Chapter 4", None),
    20: ("Chapter 4", None),
    22: ("Chapter 5", "Launch stage"),
    23: ("Chapter 5", None),
    24: ("Chapter 5", None),
    26: ("Chapter 6", "Scale stage"),
    27: ("Chapter 6", None),
    28: ("Chapter 6", None),
    29: ("Chapter 6", None),
    30: ("Chapter 6", None),
    32: ("Chapter 7", "Same job, new rules"),
    34: (None, "Resources"),
    35: (None, None),
}


def classify_span(font_name, font_size, text, x0, y0, page_num):
    """Classify a text span by its role in the document."""
    text = text.strip()
    if not text:
        return "skip"

    # Page numbers (bottom right, small)
    if font_size <= 7.5:
        return "skip"

    # Book title (page 1)
    if font_size >= 50:
        return "book_title"

    # Chapter title on divider pages (48pt)
    if font_size >= 40:
        return "chapter_divider_title"

    # Chapter title on content pages (30pt Serif)
    if font_size >= 25 and "Serif" in font_name:
        return "chapter_title"

    # Section headers (13pt Sans)
    if font_size >= 12.5 and "Sans" in font_name:
        return "section_header"

    # TOC entries (12pt Sans on page 2)
    if font_size >= 11.5 and "Sans" in font_name:
        return "toc_entry"

    # "Chapter X" label (11pt Sans, starts with "Chapter")
    if font_size >= 10.5 and "Sans" in font_name and text.startswith("Chapter"):
        return "chapter_label"

    # Sub-section headers (11pt Sans)
    if font_size >= 10.5 and "Sans" in font_name:
        return "subsection_header"

    # 9pt Sans: could be table content or sub-sub-section headers
    if font_size <= 9.5 and "Sans" in font_name:
        if page_num == TABLE_PAGE:
            return "table_content"
        # Short standalone phrases are sub-sub-section headers
        if len(text) < 60 and not text.endswith(",") and not text.endswith("."):
            return "subsub_header"
        return "table_content"

    # Body text (9pt Serif)
    if "Serif" in font_name:
        # Check for bullet points
        if text in ("\u2022", "\u2023", "\u25e6", "-"):
            return "bullet"
        # Check for numbered list items
        if re.match(r'^\d+\.\s*$', text) or re.match(r'^\d+\.\t', text):
            return "number_bullet"
        return "body"

    return "skip"


def extract_page_lines(page, page_num):
    """Extract and sort text lines from a page, handling two-column layout."""
    d = page.get_text("dict")
    lines = []

    for block in d["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            spans_data = []
            combined_text = ""
            for span in line["spans"]:
                text = span["text"]
                if text.strip():
                    spans_data.append({
                        "font": span["font"],
                        "size": round(span["size"], 1),
                        "x0": round(span["bbox"][0], 1),
                        "y0": round(span["bbox"][1], 1),
                        "text": text,
                    })
                    combined_text += text

            if not spans_data:
                continue

            first = spans_data[0]
            full_text = combined_text.strip()
            if not full_text:
                continue

            ltype = classify_span(
                first["font"], first["size"], full_text,
                first["x0"], first["y0"], page_num
            )

            col = "left" if first["x0"] < 200 else "right"

            lines.append({
                "text": full_text,
                "type": ltype,
                "x0": first["x0"],
                "y0": first["y0"],
                "col": col,
                "page": page_num,
            })

    return lines


def merge_body_lines(lines):
    """Merge consecutive body lines into paragraphs based on y-gap.
    
    Key rule: bullet/number markers always start a new paragraph.
    """
    result = []
    current_para = []
    current_col = None
    prev_y = None
    prev_type = None

    for line in lines:
        ltype = line["type"]

        if ltype in ("body", "bullet", "number_bullet"):
            # Determine if we need to start a new paragraph
            need_new = False

            # Always start new paragraph for bullet markers
            if ltype in ("bullet", "number_bullet"):
                need_new = True
            elif current_col != line["col"]:
                need_new = True
            elif prev_type is not None and prev_type != ltype:
                need_new = True
            elif prev_y is not None:
                gap = abs(line["y0"] - prev_y)
                if gap > 20:
                    need_new = True

            if need_new and current_para:
                result.append(("para", current_col, " ".join(current_para)))
                current_para = []

            current_col = line["col"]
            current_para.append(line["text"])
            prev_y = line["y0"]
            prev_type = ltype
        else:
            # Flush current paragraph
            if current_para:
                result.append(("para", current_col, " ".join(current_para)))
                current_para = []
            current_col = line["col"]

            result.append((ltype, line["col"], line["text"]))
            prev_y = line["y0"]
            prev_type = ltype

    if current_para:
        result.append(("para", current_col, " ".join(current_para)))

    return result


def process_page(page, page_num):
    """Process a single page and return markdown lines."""
    lines = extract_page_lines(page, page_num)

    # Sort by column (left first, then right), then by y0 within each column
    left_lines = [l for l in lines if l["col"] == "left"]
    right_lines = [l for l in lines if l["col"] == "right"]
    left_lines.sort(key=lambda l: l["y0"])
    right_lines.sort(key=lambda l: l["y0"])
    sorted_lines = left_lines + right_lines

    merged = merge_body_lines(sorted_lines)

    md_lines = []
    for item_type, col, text in merged:
        if item_type == "skip":
            continue
        elif item_type == "book_title":
            md_lines.append(f"# {text}")
        elif item_type == "chapter_title":
            pass  # handled via CHAPTER_TITLES
        elif item_type == "chapter_label":
            pass
        elif item_type == "chapter_divider_title":
            pass
        elif item_type == "section_header":
            md_lines.append(f"## {text}")
        elif item_type == "subsection_header":
            md_lines.append(f"### {text}")
        elif item_type == "subsub_header":
            md_lines.append(f"**{text}**")
        elif item_type == "toc_entry":
            if not text.strip().isdigit():
                md_lines.append(f"- {text}")
        elif item_type == "table_content":
            # Skip table content from page 11
            pass
        elif item_type == "para":
            text = text.strip()
            if text:
                if text.startswith("\u2022") or text.startswith("\u2023") or text.startswith("\u25e6"):
                    bullet_text = text[1:].strip()
                    if bullet_text:
                        md_lines.append(f"- {bullet_text}")
                elif re.match(r'^\d+\.\s', text) or re.match(r'^\d+\.\t', text):
                    md_lines.append(text)
                else:
                    md_lines.append(text)
        elif item_type == "bullet":
            pass  # handled in para
        elif item_type == "number_bullet":
            pass  # handled in para

    return md_lines


def post_process(md_lines):
    """Post-process markdown lines to fix common issues."""
    result = []
    i = 0
    while i < len(md_lines):
        line = md_lines[i]

        # Merge consecutive ### headers
        if line.startswith("### ") and i + 1 < len(md_lines):
            # Look ahead: skip blank lines and merge next ### header
            j = i + 1
            while j < len(md_lines) and not md_lines[j].strip():
                j += 1
            if j < len(md_lines) and md_lines[j].startswith("### "):
                # Merge the two headers
                merged_text = line[4:].rstrip() + " " + md_lines[j][4:]
                result.append(f"### {merged_text}")
                i = j + 1
                continue

        # Split bullets embedded in paragraph text or existing bullet lines
        if "\u2022" in line and not line.startswith("### ") and not line.startswith("## "):
            parts = line.split("\u2022")
            if len(parts) > 1:
                # First part: may already start with "- " or be regular text
                first_part = parts[0].strip().replace("\t", " ").strip()
                if first_part:
                    result.append(first_part)
                # Remaining parts are new bullets
                for part in parts[1:]:
                    bullet_text = part.strip()
                    if bullet_text:
                        bullet_text = bullet_text.replace("\t", " ").strip()
                        result.append(f"- {bullet_text}")
                i += 1
                continue

        # Fix "Note:" spacing
        if "Note:AI" in line:
            line = line.replace("Note:AI", "Note: AI")
        if "Note: Using" in line and "Note: Using" not in line:
            pass  # already fine

        result.append(line)
        i += 1

    # Second pass: merge continuation lines into preceding bullets
    # A continuation line starts with a lowercase letter and follows a bullet line
    final = []
    for line in result:
        stripped = line.strip()
        if not stripped:
            final.append(line)
            continue
        # Check if this is a continuation of the previous bullet
        if (stripped[0].islower() and
                final and final[-1].startswith("- ")):
            final[-1] = final[-1] + " " + stripped
        else:
            final.append(line)

    return final


def filter_table_content(md_lines):
    """Filter out table content from page 11.
    
    Only filter exact matches of table cell content, not headers that happen
    to contain the same words.
    """
    # Exact table cell texts to skip
    exact_skips = {
        "If the task is...", "Reach for", "Why",
        "Chat", "Claude Cowork", "Claude Code",
    }
    # Table cell fragments (multi-line cells) - must match exactly
    cell_fragments = {
        "A question, a rewrite,",
        "a quick brainstorm",
        "Research, analysis, or",
        "a finished document",
        "built from your files",
        "and systems",
        "Writing, testing, or",
        "shipping software",
        "Fast, conversational,",
        "no setup",
        "Folder access,",
        "connectors, skills,",
        "scheduled runs",
        "Codebase access,",
        "diffs, git, dev",
        "environments",
    }
    result = []
    for line in md_lines:
        stripped = line.strip()
        if stripped in exact_skips:
            continue
        if stripped in cell_fragments:
            continue
        result.append(line)
    return result


def main():
    doc = pymupdf.open(PDF_PATH)
    page_count = doc.page_count

    output_lines = []

    # Page 1: Title page
    page = doc[0]
    d = page.get_text("dict")
    title_parts = []
    for block in d["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if span["size"] >= 50:
                    title_parts.append(span["text"].strip())
    full_title = " ".join(title_parts)
    output_lines.append(f"# {full_title}")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")

    # Page 2: TOC
    page = doc[1]
    lines = extract_page_lines(page, 2)
    toc_entries = []
    for l in lines:
        if l["type"] == "toc_entry" and not l["text"].strip().isdigit():
            toc_entries.append(l["text"].strip())
    output_lines.append("## Table of Contents")
    output_lines.append("")
    for entry in toc_entries:
        output_lines.append(f"- {entry}")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")

    # Process content pages
    for i in range(2, page_count):
        page_num = i + 1

        if page_num in SKIP_PAGES:
            continue
        if page_num in DIVIDER_PAGES:
            continue

        chapter_info = CHAPTER_TITLES.get(page_num)
        if chapter_info:
            chapter_label, chapter_title = chapter_info
            if chapter_title:
                if chapter_label:
                    output_lines.append(f"\n# {chapter_label}: {chapter_title}\n")
                else:
                    output_lines.append(f"\n# {chapter_title}\n")

        page = doc[i]
        md_lines = process_page(page, page_num)

        if page_num == TABLE_PAGE:
            md_lines = filter_table_content(md_lines)

        for line in md_lines:
            if line.strip():
                output_lines.append(line)

    doc.close()

    # Post-process: fix bullets, merge headers, etc.
    output_lines = post_process(output_lines)

    # Clean up: remove excessive blank lines
    cleaned = []
    prev_blank = False
    for line in output_lines:
        if line.strip():
            cleaned.append(line)
            prev_blank = False
        else:
            if not prev_blank:
                cleaned.append("")
            prev_blank = True

    # Write output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))
        f.write("\n")

    print(f"Done: {OUTPUT_PATH} ({len(cleaned)} lines)")


if __name__ == "__main__":
    main()
