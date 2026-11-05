# 股价波动预测 APP（进阶版）— my-app-2026

> Week10「GitHub 基础」的示例项目：用这个真实可运行的应用，当堂走完 git init → commit → push → GitHub 建仓 → 部署的全流程。
> 原型出处：课程仓库 `data-analysis/weeks/week07/week07-streamlit-app-advanced.md`（升级篇四步的配套成品）。

## 项目结构（GitHub 课的观察点）

```
my-app-2026/
├── app.py              # 主程序（Streamlit 应用）
├── requirements.txt    # 依赖清单——别人拿到仓库后 pip install -r 即可复现
├── README.md           # 项目说明书——仓库的"门面"
├── .gitignore          # 声明哪些文件不进 git（本项目的第一教学点）
└── .env                # 密钥——已被 .gitignore 忽略，永不入库（本地才有）
```

## 运行

```bash
cd my-app-2026
py -3.13 -m venv .venv          # 建虚拟环境（.venv 不入库，见 .gitignore）
.venv\Scripts\activate          # Mac: source .venv/bin/activate
pip install -r requirements.txt
# .env 需自己填：TUSHARE_TOKEN（公用 token 见实验文档 2.1）+ DEEPSEEK_API_KEY（platform.deepseek.com）
streamlit run app.py
```

## GitHub 课用它做什么

| 教学点 | 在本项目的位置 |
|---|---|
| `.gitignore` 为什么存在 | `.env`（密钥）、`.venv`（环境）、`__pycache__/`（缓存）都不该进仓库 |
| 提交的意义 | `git log` 能看到每次改动；`git diff` 看改了什么 |
| 仓库自解释 | 别人只看 GitHub 页面，就能凭 README + requirements.txt 复现你的应用 |
| 部署的地基 | W10 第 2 节 Streamlit Cloud 部署 = 直接连这个 GitHub 仓库一键部署 |

## 与文档四步的对应关系

| 文档步骤 | app.py 位置 |
|---|---|
| 步骤 1 提取 JSON | `extract_json()`（契约在 prompt，兜底在代码：`.get("up", 0)` + try/except） |
| 步骤 2 手写骨架 | UI 编排注释中的 骨架①-⑦ 标记 |
| 步骤 3 AI 组装 | 骨架之外由 AI 按"保留函数不动，只写 UI 编排"填充 |
| 步骤 4 验收清单 | 未点击引导 `st.info` / 取数失败 `st.warning` / 提取失败展示原始回复 |

内置进阶挑战：`@st.cache_data(ttl=3600)` 缓存（挑战 5）、plotly 概率条形图。

## 密钥安全

`.env` 已被 `.gitignore` 忽略，不会提交；不要把真实 key 发群里。若不慎已提交：立即换 key（撤销比删除更急），再用 `git rm --cached .env` 移出跟踪。
