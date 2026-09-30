import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

s = "我想去成都玩"
edges = [
    (0, 0, "我"),
    (1, 1, "想"),
    (1, 2, "想去"),
    (2, 2, "去"),
    (3, 3, "成"),
    (3, 4, "成都"),
    (4, 4, "都"),
    (5, 5, "玩"),
]
chosen = {(0, 0), (1, 1), (2, 2), (3, 4), (5, 5)}

fig, ax = plt.subplots(figsize=(11, 5.4))
ax.set_xlim(-0.7, 5.7)
ax.set_ylim(-1.7, 3.2)
ax.axis("off")
ax.set_title('jieba.get_DAG("我想去成都玩")', fontsize=16, pad=6)

y = 0.2
for i, ch in enumerate(s):
    ax.add_patch(
        FancyBboxPatch(
            (i - 0.28, y - 0.32),
            0.56,
            0.64,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#1f4e79",
            edgecolor="none",
        )
    )
    ax.text(i, y, ch, ha="center", va="center", color="white", fontsize=16, fontweight="bold")
    ax.text(i, y - 0.58, str(i), ha="center", va="top", color="#666666", fontsize=11)

# 跨字的边画在字的上方。想去 span=1，成都 span=1，用不同弧度错开。
arc = {(1, 2): -0.55, (3, 4): -0.28}
label_y = {(1, 2): 1.55, (3, 4): 1.05}
for a, b, word in edges:
    if a == b:
        continue
    color = "#c45911" if (a, b) in chosen else "#7d8fa3"
    lw = 2.6 if (a, b) in chosen else 1.5
    ax.annotate(
        "",
        xy=(b, y + 0.36),
        xytext=(a, y + 0.36),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=lw,
            connectionstyle=f"arc3,rad={arc[(a, b)]}",
        ),
    )
    ax.text((a + b) / 2, label_y[(a, b)], word, ha="center", va="bottom", color=color, fontsize=14)

for a, b, word in edges:
    if a != b:
        continue
    color = "#c45911" if (a, b) in chosen else "#7d8fa3"
    ax.annotate(
        "",
        xy=(a + 0.22, y - 0.36),
        xytext=(a - 0.22, y - 0.36),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=1.8 if (a, b) in chosen else 1.2,
            connectionstyle="arc3,rad=0.85",
        ),
    )
    ax.text(a, -1.15, word, ha="center", va="center", color=color, fontsize=13)

ax.text(
    -0.4,
    2.85,
    "字下方的数字是下标。箭头从词的起点指向终点。",
    fontsize=11,
    color="#333333",
)
ax.text(-0.4, 2.45, "橙色：最终切分用到的边。灰色：词典里有，但这次没选。", fontsize=11, color="#333333")
ax.text(
    -0.4,
    -1.55,
    "返回值  {0: [0],  1: [1, 2],  2: [2],  3: [3, 4],  4: [4],  5: [5]}",
    fontsize=12,
    color="#1f4e79",
)

fig.tight_layout()
out = r"data-analysis/weeks/week06/jieba_dag_chengdu.png"
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
print(out)
