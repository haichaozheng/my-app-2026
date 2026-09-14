#!/usr/bin/env python3
"""演示版：只展示第 1 轮的内容，无需交互。"""

import os
import sys

os.system("")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RESET = "\033[0m"
GOLD = "\033[93m"
DIM = "\033[90m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
PURPLE = "\033[95m"


def say(text, color=RESET):
    print(f"{color}{text}{RESET}")


def bar(label, value, scale, start=0, width=24):
    span = max(scale - start, 1)
    n = max(0, int((value - start) / span * width))
    return f"  {label:<4} |{'█' * n}{'░' * (width - n)}  {value}"


os.system("cls" if os.name == "nt" else "clear")

say("=" * 56, GOLD)
say("  数据侦探 · 一眼看穿", GOLD + BOLD)
say("  第 1 轮  截断坐标轴", GOLD + BOLD)
say("=" * 56, GOLD)
print()

say("谁的开销最大？", GOLD + BOLD)
say("下面这张图的纵轴从 80 开始（没有从 0 画）。\n", DIM)

rows = [("奶茶", 92), ("吃饭", 88), ("交通", 84)]
for name, val in rows:
    say(bar(name, val, scale=100, start=80), PURPLE)

say("  纵轴 →  80 -------- 100", DIM)
print()

say("看起来差很多。其实哪项最大？ 1奶茶  2吃饭  3交通  4差不多", CYAN)
say("（示例回答：4 差不多）", DIM)
print()

say("揭晓：奶茶 92、吃饭 88、交通 84，只差几块钱。", GREEN)
say("柱子差一截，是因为图从 80 起笔，把小差距放大了。", GREEN)
say("启发：先看坐标轴从几开始。从 0 起笔，三根柱子几乎一样高。", CYAN)
print()
say("如果纵轴从 0 开始，同样的数据画出来是这样：\n", DIM)

for name, val in rows:
    say(bar(name, val, scale=100, start=0), PURPLE)

say("  纵轴 →  0 ------------------------- 100", DIM)
print()

say("三根柱子几乎一样高——因为差距只有 4~8 块钱。", GREEN)
say("结论：看图先看轴。从 0 起笔才诚实。", CYAN)
print()
say("=" * 56, GOLD)
