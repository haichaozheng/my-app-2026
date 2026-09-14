#!/usr/bin/env python3
"""演示版：第 4 轮 - 相关≠因果，无需交互。"""

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
say("  第 4 轮  相关≠因果", GOLD + BOLD)
say("=" * 56, GOLD)
print()

say("相关是不是因果？", GOLD + BOLD)
say("某班数据：刷短视频越久，期末分数越低（负相关）。\n", DIM)
say("  时长  ▁▂▃▄▅▆▇", PURPLE)
say("  分数  ▇▆▅▄▃▂▁", PURPLE)
print()

say("禁短视频，分数就会涨吗？", CYAN)
say("  1 会    2 不一定", CYAN)
say("（示例回答：2 不一定）", DIM)
print()

say("揭晓：相关只说「一起变」，没说「谁导致谁」。", GREEN)
say("可能是本来就忙的人刷得少、考得好；禁视频未必提分。", GREEN)
print()

say("更直观的对比：", DIM)
say("  A：刷短视频多 → 分数低（观察到的相关）", PURPLE)
say("  B：刷短视频多 ← 本来就不爱学习 → 分数低", PURPLE)
say("       ↑ 真正的原因可能是「学习习惯」这个隐藏变量", DIM)
print()

say("启发：产品里不要把相关写成功能承诺。", GREEN)
say("先问：还有别的解释吗？", GREEN)
print()

say("=" * 56, GOLD)
say("  完整游戏包含 4 轮，运行以下命令体验：", DIM)
say("  py -3.13 data-analysis/weeks/week02/hello_viz.py", DIM)
say("=" * 56, GOLD)
