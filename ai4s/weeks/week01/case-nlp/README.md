# case-nlp：Week 01 NLP 实验 · 课堂展示版

基于 `week01-nlp-lab.ipynb` 制作的 Streamlit 演示应用，供课堂上边讲边操作。
数据文件与 `app.py` 同目录（`case-nlp/`）：`cleaned_300251_comments.csv`、
`300251_daily.csv`、`stopwordsHIT.txt`、`userdict.txt`、`zhang_unformal_pos/neg.txt`，无需复制。

全量双标签数据 `cleaned_300251_comments_scored.csv`（124,126 条的 `jieba_score` +
`llm_score`）由 `llm_jieba_score.py` 生成，Part 4/5/6 使用；缺失时对应页面会提示先生成。

## 运行

```bash
# 1. 激活项目虚拟环境（仓库根目录）
.\.venv\Scripts\activate

# 2. 启动（在 case-nlp 目录下）
cd ai4s/weeks/week01/case-nlp
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

## 页面结构（左侧栏切换）

| 页面 | 内容 | 对应实验 |
|---|---|---|
| Part 0 读数据 + 清洗 | 数据概览指标、预览、评论长度分布；发帖时间规律（按小时、按周几柱状图 + 周一到周日分日形态） | Part 0 |
| Part 1 分词 | 输入任意句子对比 userdict 前后切分；抽真实股评检查 | Part 1 |
| Part 2 停用词 + 词频 | 高频词 Top N 条形图（N 可调） | Part 2 |
| Part 3 词典法情感打分 | 情感分布指标、分数直方图、最正面/负面评论 | Part 3 |
| Part 4 LLM 情感分析 | 全量 12.4 万条双标签对比：分布、一致率 52.0%、混淆矩阵；**点选矩阵任一单元格查看该格评论**（3×3 可点击矩阵 + 换一批） | Part 4 |
| Part 5 每日情感分数 | 情绪曲线 + 滑动平均（窗口可调）；可切换 jieba / LLM **口径** 与 差值 / 比率 **度量**（比率 = (正面−负面)/(评论数+1)），双口径叠加对比 | Part 5 |
| Part 6 情绪 vs 股价波动幅度 | 口径 × 度量 4 组合的 Spearman ρ 表（当日 / 次日；不报告皮尔森、无移动平均）；当日 / 次日双散点图；动态数字结论区 | Part 6 |
| Part 7 情绪 vs 次日涨跌（0/1） | 把次日涨跌二值化（涨=1）；按情绪分五组（Q1–Q5）看次日上涨比例，与基准率红线对比的分组检验 | Part 7 |
| Part 8 情绪 vs 未来收益率 | 情绪 vs 次日 / 次周（5 交易日）/ 次月（20 交易日）收益率的 Spearman ρ 表 + 三张散点图 + 动态结论 | Part 8 |

## 侧边栏控件

- **抽样评论数**：仅 Part 2/3 的计算量控制（默认 30,000 条；拉满 124,126 条全量约需 2–3 分钟，首次计算后会被缓存）
- **随机种子**：默认 42，与实验文档/notebook 保持一致

Part 4/5/6 使用全量双标签数据，不受抽样数影响。

## 注意事项

- **无 API 依赖**：Part 4 直接展示 `llm_jieba_score.py` 提前跑好的全量 LLM 打标结果，课堂演示不需要任何 API Key 和外网调用。
- **缓存**：抽样数或种子改变后，首次进入 Part 2/3 会重新计算（侧边栏有进度提示）；同一参数下切换页面不重算。
- 学生实验仍以 `week01-nlp-lab.ipynb` 为准，本应用是教师的演示/讲解工具，不含练习空白格。
