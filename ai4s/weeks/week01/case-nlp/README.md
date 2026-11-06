# case-nlp：Week 09 NLP 实验 · 课堂展示版

基于 `../week09-nlp-lab.ipynb` 制作的 Streamlit 演示应用，供课堂上边讲边操作。
数据文件直接读取 `week09/` 根目录下的实验数据（`cleaned_300251_comments.csv`、
`300251_daily.csv`、`stopwordsHIT.txt`、`userdict.txt`、`zhang_unformal_pos/neg.txt`），无需复制。

## 运行

```bash
# 1. 激活项目虚拟环境（仓库根目录）
.\.venv\Scripts\activate

# 2. 启动（在 case-nlp 目录下）
cd data-analysis/weeks/week09/case-nlp
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

## 页面结构（左侧栏切换）

| 页面 | 内容 | 对应实验 |
|---|---|---|
| Part 0 读数据 + 清洗 | 数据概览指标、预览、评论长度分布 | Part 0 |
| Part 1 分词 | 输入任意句子对比 userdict 前后切分；抽真实股评检查 | Part 1 |
| Part 2 停用词 + 词频 | 高频词 Top N 条形图（N 可调） | Part 2 |
| Part 3 词典法情感打分 | 情感分布指标、分数直方图、最正面/负面评论 | Part 3 |
| Part 4 LLM 情感分析 | 按钮触发 DeepSeek 分析 10 条，与词典法并排对比 | Part 4 |
| Part 5 每日情感分数 | 情绪曲线 + 滑动平均（窗口可调）、极端日评论探查 | Part 5 |
| Part 6 情绪 vs 股价 | 三个相关系数指标 + 散点图 | Part 6 |

## 侧边栏控件

- **抽样评论数**：Part 2/3/5/6 的计算量控制（默认 30,000 条；拉满 124,125 条全量约需 2–3 分钟，首次计算后会被缓存）
- **随机种子**：默认 42，与实验文档/notebook 保持一致

## 注意事项

- **API Key**：Part 4 需要 `DEEPSEEK_API_KEY`。读取顺序：`week09/.env` 优先，找不到时向上逐级查找 `.env`（含仓库根目录的全局 `.env`）。见 `../llm-key-guide.md`。未配置时页面会提示，其余页面不受影响。
- **缓存**：抽样数或种子改变后，首次进入 Part 2/3/5/6 会重新计算（侧边栏有进度提示）；同一参数下切换页面不重算。
- 学生实验仍以 `week09-nlp-lab.ipynb` 为准，本应用是教师的演示/讲解工具，不含练习空白格。
