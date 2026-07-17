# Skill封装可复用分析能力

> **引入时机**：W13 | **核心挑战**：如何把常用的分析流程封装为可复用模块？ | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

随着你的金融数据分析产品功能不断增长，你会发现很多分析流程是重复的：行业相关性分析、因子收益归因、组合风险测算……每次都从零编写这些流程不仅低效，还容易出错且难以维护。把这些常用的分析流程封装为可复用的模块（Skill），就像把常用函数封装为库一样——一次编写、多次调用、统一维护。

Skill封装不仅仅是代码复用。在Agent驱动的产品架构中，每个Skill就是Agent可以调用的一个"能力"。当Agent收到"帮我分析行业相关性"的请求时，它不需要知道如何获取数据、如何计算相关系数、如何绘制热力图——它只需要调用"行业相关性分析"这个Skill。清晰的Skill接口设计让你的产品模块化、可扩展、易于组合。

在团队协作的PBL项目中，Skill封装还能促进分工——每个成员负责开发和维护不同的Skill，通过统一的接口协议集成到产品中。这种模块化开发方式是软件工程的基本功，也是构建可维护产品的关键。

## 这个知识点的核心内容

### Skill概念

Skill是封装了完整分析流程的可复用模块，具备以下特征：

- **自包含**：每个Skill包含完成特定分析任务所需的全部逻辑（数据获取、处理、计算、输出）
- **标准化接口**：输入和输出遵循统一的格式约定，便于组合和调用
- **可配置**：通过参数控制分析行为（如时间范围、行业选择），而非硬编码
- **可文档化**：每个Skill有清晰的说明文档，描述其功能、输入、输出和使用示例

### 分析流程封装方法

将一个分析流程封装为Skill的标准步骤：

1. **识别可复用流程**：找到产品中多次使用的分析模式
2. **定义输入输出**：明确Skill需要什么输入、产生什么输出
3. **编写核心逻辑**：将流程代码从产品代码中抽取出来
4. **添加参数化**：将硬编码的值替换为可配置参数
5. **编写文档**：描述Skill的功能、参数、返回值和使用示例
6. **测试验证**：确保Skill在不同参数下都能正确运行

### 可复用模块设计原则

- **单一职责**：每个Skill只做一件事，做好一件事。不要把"行业分析"和"个股分析"混在一个Skill中
- **输入验证**：检查输入数据格式和参数范围，提供清晰的错误提示
- **默认值**：常用参数提供合理默认值，降低调用门槛
- **幂等性**：相同输入总是产生相同输出，便于测试和缓存
- **渐进复杂**：基础功能简单易用，高级功能通过可选参数暴露

### API设计

Skill的接口设计直接影响使用体验：

```python
class IndustryCorrelationSkill:
    def __init__(self, data_source="akshare"):
        self.data_source = data_source

    def run(self, industries=None, period="1y", method="pearson",
            plot=True, top_n=None) -> SkillResult:
        ...

    def get_schema(self) -> dict:
        return {
            "name": "industry_correlation",
            "description": "分析申万行业间的相关性",
            "inputs": {
                "industries": {"type": "list[str]", "required": False},
                "period": {"type": "str", "default": "1y"},
                "method": {"type": "str", "enum": ["pearson", "spearman"]},
            },
            "outputs": {
                "correlation_matrix": {"type": "DataFrame"},
                "high_pairs": {"type": "list[tuple]"},
                "plot": {"type": "Figure"},
            }
        }
```

### 文档规范

每个Skill应包含以下文档：

- **功能描述**：Skill做什么、解决什么问题
- **参数说明**：每个参数的类型、默认值、取值范围
- **输出说明**：返回值的结构和含义
- **使用示例**：至少一个完整可运行的示例
- **注意事项**：已知的限制和常见错误

## 关键细节与易错点

### 过度封装

不是每段代码都需要封装为Skill。只有被多次使用或可能被Agent调用的分析流程才值得封装。一次性分析直接写脚本即可，过度封装增加维护负担。

### 接口不稳定

Skill的接口一旦被其他模块或Agent使用，就不应随意更改。修改接口会导致所有调用方报错。遵循语义化版本：小修改增加补丁版本，新增参数增加次版本，破坏性修改增加主版本。

### 隐式依赖

Skill依赖外部数据源或库但未在文档中说明，导致其他环境无法运行。所有依赖应在`__init__`中声明或至少在文档中列出。

### 忽视异常处理

Skill内部的异常如果不处理，会直接抛出到调用方，可能导致整个产品崩溃。Skill应该捕获已知异常，返回包含错误信息的SkillResult，让调用方决定如何处理。

### 输出格式不统一

不同Skill返回不同格式的结果，调用方需要针对每个Skill写不同的解析逻辑。统一输出格式（如SkillResult类包含data、plot、summary、error字段）能大幅简化集成代码。

### 数据获取与计算耦合

把数据获取和计算逻辑混在一起，导致想换数据源时需要修改计算逻辑。应该将数据获取层和计算层分离，通过标准数据格式对接。

## 金融数据分析示例

**场景**：将"行业相关性分析"封装为一个可复用Skill，供产品界面和Agent调用。

**Skill实现**：

```python
import pandas as pd
import numpy as np
import akshare as ak
import plotly.express as px
from dataclasses import dataclass

@dataclass
class SkillResult:
    data: dict
    plot: object = None
    summary: str = ""
    error: str = ""

class IndustryCorrelationSkill:
    def __init__(self, data_source="akshare"):
        self.data_source = data_source
        self.name = "industry_correlation"
        self.description = "分析申万行业ETF间的相关性，发现轮动和分化信号"

    def run(self, industries=None, period="1y",
            method="pearson", top_n=5, plot=True) -> SkillResult:
        try:
            df = self._fetch_data(industries, period)
            corr = df.pct_change().corr(method=method)
            high_pairs = self._find_high_pairs(corr, top_n)
            fig = self._plot_heatmap(corr) if plot else None
            summary = self._generate_summary(high_pairs, method)

            return SkillResult(
                data={
                    "correlation_matrix": corr.to_dict(),
                    "high_correlation_pairs": high_pairs,
                },
                plot=fig,
                summary=summary,
            )
        except Exception as e:
            return SkillResult(data={}, error=str(e))

    def _fetch_data(self, industries, period):
        period_map = {"1y": 250, "6m": 125, "3m": 60}
        count = period_map.get(period, 250)
        board = ak.stock_board_industry_name_em()
        targets = industries if industries else board["板块名称"].head(28).tolist()

        prices = {}
        for name in targets[:15]:
            try:
                hist = ak.stock_board_industry_hist_em(
                    symbol=name, period="日k", start_date="20250101", adjust=""
                )
                if len(hist) > count:
                    prices[name] = hist["收盘"].tail(count).values
            except Exception:
                continue

        return pd.DataFrame(prices)

    def _find_high_pairs(self, corr, top_n):
        pairs = []
        cols = corr.columns
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                pairs.append((cols[i], cols[j], corr.iloc[i, j]))
        pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        return [(a, b, round(c, 3)) for a, b, c in pairs[:top_n]]

    def _plot_heatmap(self, corr):
        fig = px.imshow(
            corr, text_auto=".2f", aspect="auto",
            color_continuous_scale="RdBu_r", range_color=[-1, 1],
            title="行业相关性热力图"
        )
        fig.update_layout(height=600)
        return fig

    def _generate_summary(self, high_pairs, method):
        if not high_pairs:
            return "未发现显著高相关行业对"
        top = high_pairs[0]
        return f"最高相关：{top[0]}与{top[1]}，相关系数{top[2]}（{method}）"
```

**在Streamlit中调用**：

```python
import streamlit as st

skill = IndustryCorrelationSkill()
period = st.selectbox("分析周期", ["1y", "6m", "3m"])
method = st.selectbox("相关方法", ["pearson", "spearman"])

result = skill.run(period=period, method=method)

if result.error:
    st.error(result.error)
else:
    st.markdown(result.summary)
    st.plotly_chart(result.plot, use_container_width=True)
    st.dataframe(pd.DataFrame(result.data["high_correlation_pairs"],
                               columns=["行业A", "行业B", "相关系数"]))
```

**在Agent中调用**：

```python
from langchain_core.tools import tool

@tool
def analyze_industry_correlation(period: str, method: str = "pearson") -> str:
    """分析行业间相关性，发现轮动和分化信号"""
    skill = IndustryCorrelationSkill()
    result = skill.run(period=period, method=method)
    return result.summary
```

## 拓展学习

- **设计模式**：策略模式、工厂模式、模板方法模式，在Skill设计中广泛应用
- **Plugin架构**：如何设计支持第三方扩展的插件系统
- **微服务拆分原则**：领域驱动设计（DDD）中的限界上下文概念，指导Skill的划分
- **OpenAPI/Swagger**：标准化API文档规范，让Skill接口可以被自动发现和调用
- **函数即服务（FaaS）**：将Skill部署为云函数，按需调用、自动扩缩容

## 参考链接

- https://docs.python.org/3/library/dataclasses.html - Python dataclass文档
- https://fastapi.tiangolo.com/tutorial/dependencies/ - FastAPI依赖注入设计
- https://swagger.io/specification/ - OpenAPI规范
- https://martinfowler.com/bliki/BoundedContext.html - 限界上下文概念
- https://plugins.jetbrains.com/docs/intellij/plugin-architecture.html - 插件架构设计参考
