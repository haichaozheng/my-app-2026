#!/usr/bin/env python3
"""数据侦探：一眼看穿 — 终端小游戏。

四轮找茬，对应数据分析与可视化里最常见的四种「图在说谎」：
截断坐标轴、均值被极端值拉走、只截一段上涨、相关当成因果。
无需第三方库。运行：python hello_viz.py
"""

import os
import sys

os.system("")  # Windows 10+ 启用 ANSI 颜色
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RESET = "\033[0m"
GOLD = "\033[93m"
DIM = "\033[90m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def say(text, color=RESET):
    print(f"{color}{text}{RESET}")


def pause():
    input(f"\n{DIM}回车继续…{RESET}")


def ask(prompt, allowed):
    while True:
        ans = input(f"{CYAN}{prompt}{RESET} ").strip()
        if ans in allowed:
            return ans
        say(f"请输入 {' / '.join(allowed)}", DIM)


def bar(label, value, scale, start=0, width=24):
    """从 start 起画柱。start>0 就是截断坐标轴。"""
    span = max(scale - start, 1)
    n = max(0, int((value - start) / span * width))
    return f"  {label:<4} |{'█' * n}{'░' * (width - n)}  {value}"


def header():
    say("=" * 56, GOLD)
    say("  数据侦探 · 一眼看穿", GOLD + BOLD)
    say("  四张图，四句问。图很好看，不一定诚实。", DIM)
    say("=" * 56, GOLD)
    print()


def round_axis():
    say("第 1 轮  谁的开销最大？", GOLD + BOLD)
    say("下面这张图的纵轴从 80 开始（没有从 0 画）。\n", DIM)
    rows = [("奶茶", 92), ("吃饭", 88), ("交通", 84)]
    for name, val in rows:
        say(bar(name, val, scale=100, start=80), "\033[95m")
    say("  纵轴 →  80 -------- 100", DIM)
    print()
    ans = ask("看起来差很多。其实哪项最大？ 1奶茶  2吃饭  3交通  4差不多", ["1", "2", "3", "4"])
    say("\n揭晓：奶茶 92、吃饭 88、交通 84，只差几块钱。", GREEN)
    say("柱子差一截，是因为图从 80 起笔，把小差距放大了。", GREEN)
    say("启发：先看坐标轴从几开始。从 0 起笔，三根柱子几乎一样高。", CYAN)
    return ans == "4" or ans == "1"


def round_mean():
    say("第 2 轮  实习日薪「大概多少」？", GOLD + BOLD)
    pay = [180, 200, 190, 210, 2000]
    say("五位同学的日薪（元）：", DIM)
    say("  " + "  ".join(str(x) for x in pay), "\033[95m")
    mean = sum(pay) / len(pay)
    mid = sorted(pay)[len(pay) // 2]
    say(f"\n  平均数 = {mean:.0f}     中位数 = {mid}", DIM)
    print()
    ans = ask("跟朋友说「大家大概赚多少」，哪个更不骗人？ 1平均数  2中位数", ["1", "2"])
    say(f"\n揭晓：一个人 2000，把平均拉到 {mean:.0f}；多数人在 {mid} 左右。", GREEN)
    say("启发：均值会被极端值绑架。问「典型的人」时，先看中位数。", CYAN)
    return ans == "2"


def round_window():
    say("第 3 轮  这周指数在涨吗？", GOLD + BOLD)
    week = [100, 98, 95, 92, 90, 93, 96]
    days = "一二三四五六日"
    say("有人只截了周六→周日给你看：", DIM)
    say("  六 " + "█" * 9 + "  93", "\033[95m")
    say("  日 " + "█" * 12 + "  96   ← 涨了！", "\033[95m")
    print()
    ans = ask("只凭这两天，能说「这周行情在涨」吗？ 1能  2不能", ["1", "2"])
    say("\n完整一周（周一收在 100，周日 96）：", GREEN)
    for d, v in zip(days, week):
        n = v // 5 - 12
        say(f"  周{d} {'█' * max(n, 1)}  {v}", GREEN)
    say("启发：截一段时间，跌也能讲成涨。问一句：完整区间呢？", CYAN)
    return ans == "2"


def round_cause():
    say("第 4 轮  相关是不是因果？", GOLD + BOLD)
    say("某班数据：刷短视频越久，期末分数越低（负相关）。\n", DIM)
    say("  时长  ▁▂▃▄▅▆▇", "\033[95m")
    say("  分数  ▇▆▅▄▃▂▁", "\033[95m")
    print()
    ans = ask("禁短视频，分数就会涨吗？ 1会  2不一定", ["1", "2"])
    say("\n揭晓：相关只说「一起变」，没说「谁导致谁」。", GREEN)
    say("可能是本来就忙的人刷得少、考得好；禁视频未必提分。", GREEN)
    say("启发：产品里不要把相关写成功能承诺。先问：还有别的解释吗？", CYAN)
    return ans == "2"


def main():
    clear()
    header()
    say("你是数据侦探。每轮一张图、一个问题。", DIM)
    say("目标不是算得快，是看出图在隐瞒什么。\n", DIM)
    pause()

    rounds = [
        ("截断坐标轴", round_axis),
        ("均值陷阱", round_mean),
        ("时间窗口", round_window),
        ("相关≠因果", round_cause),
    ]
    score = 0
    for i, (title, fn) in enumerate(rounds, 1):
        clear()
        header()
        say(f"  （{i}/4  {title}）\n", DIM)
        if fn():
            score += 1
            say("\n这一轮你盯住了。", GOLD)
        else:
            say("\n这一轮图把你带走了，很常见。", GOLD)
        pause()

    clear()
    header()
    say(f"  四轮结束。看穿 {score} / 4 张图。\n", GOLD + BOLD)
    say("  数据分析与可视化，不是把数画漂亮。", CYAN)
    say("  是先问：这张图的轴从哪起？平均数代表谁？", CYAN)
    say("  截了哪段时间？相关会不会只是碰巧一起变？", CYAN)
    say("\n  本学期你的产品也会给人看图。侦探习惯从现在练。\n", DIM)
    say("=" * 56, GOLD)


if __name__ == "__main__":
    main()
