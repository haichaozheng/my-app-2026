# 股价波动预测 APP — Streamlit 案例

> 对应课堂演示 notebook：`../streamlit.ipynb`（同一链路的逐 cell 讲解版）

## 功能

输入股票代码 → tushare 取近5日指标（换手率/量比/PE/PB）→ DeepSeek 7步预测 → 概率图示 + 分析原因

## 运行

```bash
cd weeks/week07/cases

# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置密钥
cp .env.example .env
# 编辑 .env，填入你的 TUSHARE_TOKEN 和 DEEPSEEK_API_KEY

# 3. 启动
streamlit run app.py
```

打开 http://localhost:8501 即可使用。

## 预设股票

| ts_code | 名称 | 备注 |
|---|---|---|
| 000001.SZ | 平安银行 | |
| 600519.SH | 贵州茅台 | |
| 000858.SZ | 五粮液 | |
| 002594.SZ | 比亚迪 | |
| 688012.SH | 中微公司 | 半导体设备 |
| 688825.SH | 长鑫科技 | 国产DRAM，2026-07 上市 |
| 688836.SH | 宇树科技 | 人形机器人，2026-08 上市 |

侧栏也支持输入任意 ts_code（如 `300750.SZ`）。

## 与 notebook 的对应关系

| notebook 单元 | app.py 函数/位置 |
|---|---|
| tushare 单日取数 + 倒推5天循环 | `fetch_daily_basic()` |
| `llm_chat` 封装 + DeepSeek 调用 | `llm_chat()` |
| 7步预测 prompt 构造 | `build_prompt()` |
| `extract_json` 正则提取 | `extract_json()` |
| 使用 streamlit 构建应用展示 | UI 主区域（侧栏 + 三段式展示） |

## 改造指引（做个人 MVP）

1. **换数据源**：把 tushare 换成你 W4 落盘的数据集（读 CSV / DuckDB）
2. **换分析逻辑**：把 7步预测 prompt 换成你的业务场景（如行业景气度判断、舆情分析）
3. **换展示**：概率条形图换成你 W6 设计的图表（用 plotly 或 `st.line_chart`）

## 密钥安全

- `.env` 已在 `.gitignore`，不要提交到仓库
- 不要在代码中硬编码 token / API key
