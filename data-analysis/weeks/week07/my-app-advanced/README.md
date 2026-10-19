# 股价波动预测 APP（进阶版）

> 对应实验文档：`../week07-streamlit-app-advanced.md`（升级篇四步的配套成品）
> 对照成品：`../cases/app.py`

## 运行

```bash
cd my-app-advanced
pip install -r requirements.txt
# .env 已预置公用 TUSHARE_TOKEN；DEEPSEEK_API_KEY 需自己填（platform.deepseek.com）
streamlit run app.py
```

## 与文档四步的对应关系

| 文档步骤 | app.py 位置 |
|---|---|
| 步骤 1 提取 JSON | `extract_json()`（契约在 prompt，兜底在代码：`.get("up", 0)` + try/except） |
| 步骤 2 手写骨架 | UI 编排注释中的 骨架①-⑦ 标记 |
| 步骤 3 AI 组装 | 骨架之外由 AI 按"保留函数不动，只写 UI 编排"填充 |
| 步骤 4 验收清单 | 未点击引导 `st.info` / 取数失败 `st.warning` / 提取失败展示原始回复 |

内置进阶挑战：`@st.cache_data(ttl=3600)` 缓存（挑战 5）、plotly 概率条形图。

## 密钥安全

`.env` 已被仓库 `.gitignore` 忽略（`*.env`），不会提交；不要把真实 key 发群里。
