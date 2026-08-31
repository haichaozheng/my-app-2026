# Prompt驱动EDA洞察

> **引入时机**：W5 | **核心挑战**："做了EDA但没发现有意思的结论，如何用Prompt引导？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

很多同学做完EDA后说"数据没什么特别的"——不是数据无聊，而是你的探索视角不够丰富。传统EDA依赖分析师的经验和直觉来决定看什么，但学生往往缺少这种直觉。大语言模型（LLM）可以作为你的"分析搭档"，通过精心设计的Prompt引导你从不同视角审视数据，发现你自己可能想不到的规律和假设。

Prompt驱动EDA不是让AI替你分析，而是用AI拓宽你的分析视野。你提供数据统计信息和业务背景，AI提供分析角度和假设方向，你负责验证和深入。这种人机协作模式让EDA从"拍脑袋决定看什么"变成"系统性地探索所有可能"。

## 这个知识点的核心内容

### LLM增强EDA的工作流程

1. **准备数据摘要**：将数据的统计摘要（非原始数据）整理为文本
2. **设计分析Prompt**：按视角构建引导性提问
3. **获取分析建议**：LLM返回可能的分析角度和假设
4. **执行验证**：用代码验证LLM提出的假设
5. **迭代深入**：基于验证结果设计新一轮Prompt

关键原则：永远不要把原始数据发送给LLM，只发送统计摘要和样本。既保护数据隐私，又控制Token消耗。

### 按视角设计Prompt模板

**分布视角Prompt**：

```
我正在分析A股{行业}板块{N}只股票{年份范围}的日收益率数据。
统计摘要：均值={X}, 中位数={Y}, 标准差={Z}, 偏度={S}, 峰度={K}
请从分布角度提出3-5个值得探索的假设，特别是关于尾部风险和非正态特征。
```

**相关视角Prompt**：

```
以下是我计算的{行业}板块股票收益率相关矩阵的统计特征：
平均相关系数={X}, 最高相关对={A-B: Y}, 最低相关对={C-D: Z}
请从相关性角度提出3-5个值得深入的问题，例如相关性是否存在时变特征或异常断裂。
```

**趋势视角Prompt**：

```
{行业}板块指数{年份范围}的年度收益率分别为：{列表}
关键事件：{列出重大政策或事件}
请分析这些趋势可能的结构性变化点，并提出3-5个可验证的假设。
```

**比较视角Prompt**：

```
{行业}板块中，国有大行和股份制银行的以下指标差异如下：
PE均值：国有{X} vs 股份制{Y}
ROE均值：国有{A} vs 股份制{B}
请分析这些差异可能反映的业务模式差异，提出3-5个可验证的假设。
```

**异常视角Prompt**：

```
在{行业}板块{年份范围}数据中，我发现了以下异常：
1. {异常描述1}
2. {异常描述2}
请分析这些异常可能的共同驱动因素，并提出3-5个深入分析方向。
```

### Prompt链示例：递进式分析

通过多轮Prompt实现从宏观到微观的递进分析：

**第1轮：行业分布特征**
```
分析A股银行板块8只代表性股票2020-2024年的数据，
告诉我应该首先关注哪些分布特征？有哪些行业特有的数据模式？
```

**第2轮：行业相关性**
```
基于第1轮分析，我发现银行股之间相关系数普遍较高（均值0.6），
但招商银行与其他银行相关性明显偏低（~0.4）。
请分析这种分化可能反映什么业务逻辑差异？我该如何验证？
```

**第3轮：2024年异常表现**
```
2024年9月银行板块出现异常波动，单日涨幅达5%+。
请分析可能的政策驱动因素，并建议我查看哪些具体指标来验证。
```

**第4轮：宏观政策关联**
```
我已经确认2024年9月的异常与降准降息政策相关。
请建议我如何系统性地分析货币政策与银行板块走势的关联，
包括应该获取哪些宏观数据、用什么方法分析。
```

### 数据摘要的最佳实践

高效地向LLM传递数据信息：

```python
def generate_data_summary(df, group_col=None):
    summary = f"数据形状: {df.shape[0]}行 × {df.shape[1]}列\n"
    summary += f"时间范围: {df.index.min()} ~ {df.index.max()}\n\n"

    for col in df.select_dtypes(include="number").columns:
        s = df[col].dropna()
        summary += f"## {col}\n"
        summary += f"  均值={s.mean():.4f}, 中位数={s.median():.4f}\n"
        summary += f"  标准差={s.std():.4f}, 偏度={s.skew():.4f}, 峰度={s.kurtosis():.4f}\n"
        summary += f"  最小值={s.min():.4f}, 最大值={s.max():.4f}\n\n"

    if group_col:
        for name, group in df.groupby(group_col):
            summary += f"## 组: {name}\n"
            for col in df.select_dtypes(include="number").columns:
                s = group[col].dropna()
                summary += f"  {col}: 均值={s.mean():.4f}, 标准差={s.std():.4f}\n"
            summary += "\n"

    return summary
```

### 避免LLM分析的陷阱

- **幻觉问题**：LLM可能编造不存在的统计规律，所有结论必须用代码验证
- **过度解读**：LLM倾向于给每个模式找一个解释，但有些模式只是噪声
- **忽略领域知识**：LLM的金融领域知识可能过时或不准确，需要交叉验证
- **确认偏误放大**：如果你在Prompt中暗示了某个方向，LLM会顺着你说话

## 关键细节与易错点

- **误区：把原始数据直接粘贴给LLM分析**。隐私风险大、Token消耗高、效果不如统计摘要
- **误区：LLM说有规律就一定有规律**。必须用代码和统计方法验证，LLM只提供假设方向
- **易错：Prompt太宽泛**。如"帮我分析这些数据"，LLM会给出泛泛而谈的建议
- **易错：一次问太多问题**。每个Prompt聚焦一个视角，多轮递进比一次大Prompt效果好
- **易错：不提供足够的业务背景**。LLM不了解中国A股的特殊规则（涨跌停、T+1等），需在Prompt中说明

## 金融数据分析示例

用Prompt链驱动银行板块EDA：

```python
import akshare as ak
import pandas as pd
import numpy as np

# 准备数据
codes = {
    "601398": "工商银行", "601939": "建设银行",
    "600036": "招商银行", "601166": "兴业银行"
}

all_data = []
for code, name in codes.items():
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                            start_date="20200101", end_date="20241231", adjust="hfq")
    df["code"] = code
    df["name"] = name
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
data["date"] = pd.to_datetime(data["日期"])
data.rename(columns={"收盘": "close", "成交量": "volume"}, inplace=True)
data["return"] = data.groupby("code")["close"].pct_change()

# 生成数据摘要
def finance_summary(df):
    summary = "A股银行板块4只股票2020-2024日收益率数据摘要\n\n"
    for name, group in df.groupby("name"):
        r = group["return"].dropna()
        summary += f"### {name}\n"
        summary += f"  均值={r.mean():.4f}, 标准差={r.std():.4f}\n"
        summary += f"  偏度={r.skew():.2f}, 峰度={r.kurtosis():.2f}\n"
        summary += f"  最大单日涨幅={r.max():.4f}, 最大单日跌幅={r.min():.4f}\n\n"
    returns_wide = df.pivot_table(values="return", index="date", columns="name")
    corr = returns_wide.corr()
    summary += "### 相关系数矩阵关键信息\n"
    summary += f"  平均相关系数={corr.values[np.triu_indices_from(corr.values, k=1)].mean():.4f}\n"
    summary += f"  最低相关对: {corr.unstack().idxmin()} = {corr.unstack().min():.4f}\n"
    return summary

summary_text = finance_summary(data)

# 将summary_text粘贴到ChatGPT/Claude中，使用Prompt模板提问
# 例如：
prompt = f"""
{summary_text}

请从趋势视角提出3-5个值得探索的假设，特别关注：
1. 是否存在结构性变化时点
2. 波动率是否有聚类特征
3. 不同银行之间的分化趋势

注意：这是中国A股数据，有10%涨跌停限制和T+1交易制度。
"""

# 将LLM返回的假设逐一用代码验证
# 假设1验证：2024年9月是否存在结构性变化
sep_2024 = data[(data["date"] >= "2024-09-01") & (data["date"] <= "2024-09-30")]
print("2024年9月银行股收益率统计：")
print(sep_2024.groupby("name")["return"].describe())
```

## 拓展学习

- Prompt Engineering Guide——系统性的Prompt设计方法论
- 《Co-Intelligence》——Ethan Mollock著，人机协作思维模式
- ChatGPT Code Interpreter——直接上传数据进行交互式EDA
- OpenAI官方Prompt最佳实践——Prompt设计的原则和技巧
- PandasAI库——用自然语言查询DataFrame的AI工具

## 参考链接

- https://www.promptingguide.ai/ — Prompt Engineering Guide，系统性Prompt设计
- https://platform.openai.com/docs/guides/prompt-engineering — OpenAI官方Prompt工程指南
- https://github.com/gventuri/pandas-ai — PandasAI：用自然语言查询Pandas DataFrame
- https://cookbook.openai.com/ — OpenAI Cookbook，实用的API使用案例
