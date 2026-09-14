#!/usr/bin/env python3
"""演示版：第 3 轮 - 时间窗口陷阱，无需交互。"""

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
say("  第 3 轮  时间窗口", GOLD + BOLD)
say("=" * 56, GOLD)
print()

say("这周指数在涨吗？", GOLD + BOLD)
week = [100, 98, 95, 92, 90, 93, 96]
days = "一二三四五六日"

say("有人只截了周六→周日给你看：\n", DIM)
say("  六 " + "█" * 9 + "  93", PURPLE)
say("  日 " + "█" * 12 + "  96   ← 涨了！", PURPLE)
print()

say("只凭这两天，能说「这周行情在涨」吗？", CYAN)
say("  1 能    2 不能", CYAN)
say("（示例回答：2 不能）", DIM)
print()

say("完整一周（周一收在 100，周日 96）：", GREEN)
for d, v in zip(days, week):
    n = v // 5 - 12
    say(f"  周{d} {'█' * max(n, 1)}  {v}", GREEN)

print()
say("其实整周从 100 跌到 96，整体是跌的。", GREEN)
say("只截周六→周日，跌也能讲成涨。", GREEN)
say("启发：问一句——完整区间呢？", CYAN)
print()

say("=" * 56, GOLD)
say("  完整游戏包含 4 轮，运行以下命令体验：", DIM)
say("  py -3.13 data-analysis/weeks/week02/hello_viz.py", DIM)
say("=" * 56, GOLD)
