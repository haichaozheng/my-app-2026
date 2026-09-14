#!/usr/bin/env python3
"""演示版：第 2 轮 - 均值陷阱，无需交互。"""

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


os.system("cls" if os.name == "nt" else "clear")

say("=" * 56, GOLD)
say("  数据侦探 · 一眼看穿", GOLD + BOLD)
say("  第 2 轮  均值陷阱", GOLD + BOLD)
say("=" * 56, GOLD)
print()

say("实习日薪「大概多少」？", GOLD + BOLD)
pay = [180, 200, 190, 210, 2000]
say("五位同学的日薪（元）：", DIM)
say("  " + "  ".join(str(x) for x in pay), PURPLE)
mean = sum(pay) / len(pay)
mid = sorted(pay)[len(pay) // 2]
say(f"\n  平均数 = {mean:.0f}     中位数 = {mid}", DIM)
print()

say("跟朋友说「大家大概赚多少」，哪个更不骗人？", CYAN)
say("  1 平均数    2 中位数", CYAN)
say("（示例回答：2 中位数）", DIM)
print()

say(f"揭晓：一个人 2000，把平均拉到 {mean:.0f}；多数人在 {mid} 左右。", GREEN)
say("启发：均值会被极端值绑架。问「典型的人」时，先看中位数。", CYAN)
print()

# 可视化对比
say("直观对比：", DIM)
bar_avg = "█" * int(mean / 50)
bar_mid = "█" * int(mid / 50)
say(f"  平均数  {bar_avg}  {mean:.0f}", PURPLE)
say(f"  中位数  {bar_mid}  {mid}", PURPLE)
say("  ↑ 平均数被 2000 拉高，不代表大多数人", DIM)

print()
say("=" * 56, GOLD)
say("  完整游戏包含 4 轮，运行以下命令体验：", DIM)
say("  py -3.13 data-analysis/weeks/week02/hello_viz.py", DIM)
say("=" * 56, GOLD)
