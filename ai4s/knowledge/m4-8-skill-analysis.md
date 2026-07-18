# Skill封装分析能力

> **引入时机**：W6 | **核心挑战**："如何把分析流程封装为可复用Skill？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

进入W6的分析实施阶段，你会反复执行类似的分析操作：描述统计、回归分析、稳健性检验、可视化。每次分析都重新写代码不仅低效，更危险的是——细微的方法差异可能导致结果不可比。你在基准回归中用了固定效应+聚类标准误，但稳健性检验中忘了加聚类标准误，两者的p值差异可能来自标准误选择而非模型设定差异。

将分析流程封装为Skill，本质上是将"分析方法论"固化为"可执行的代码模板"。每个Skill背后是一个明确的方法论决策——用固定效应还是随机效应、用聚类标准误还是异方差稳健标准误、用哪种可视化类型。当这些决策固化在Skill中，你就不会在重复执行时遗漏关键步骤。

更重要的是，Skill封装让分析过程可审查。论文审稿人或导师检查你的分析时，不需要逐行读代码——Skill的接口定义本身就说明了方法论选择。这种透明性是"做对"研究的保障。

## 这个知识点的核心内容

### 分析Skill的设计

分析Skill的设计遵循"方法论驱动"原则——先明确方法论决策，再编码实现：

**回归分析Skill：**

```yaml
name: panel_regression_skill
description: 执行面板数据回归分析，含前提检验和标准误选择
triggers:
  - 面板回归
  - 固定效应回归
  - panel regression
parameters:
  required:
    - data_path: 数据文件路径
    - dep_var: 因变量名
    - core_var: 核心自变量名
  optional:
    - controls: 控制变量列表，默认[]
    - entity_var: 个体标识变量，默认province
    - time_var: 时间标识变量，默认year
    - fe_type: 固定效应类型，entity/twoway，默认entity
    - cluster_var: 聚类变量，默认与entity_var相同
    - include_hausman: 是否执行Hausman检验，默认true
output:
  type: dict
  fields:
    - model: 回归结果对象
    - report: 格式化报告
    - diagnostics: 前提检验结果
```

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

class PanelRegressionSkill:
    def execute(self, data_path, dep_var, core_var, controls=None,
                entity_var="province", time_var="year",
                fe_type="entity", cluster_var=None,
                include_hausman=True):
        if controls is None:
            controls = []
        if cluster_var is None:
            cluster_var = entity_var

        df = pd.read_stata(data_path)
        df = df.sort_values([entity_var, time_var])

        diagnostics = self._run_diagnostics(
            df, dep_var, [core_var] + controls
        )

        y = df[dep_var]
        X = sm.add_constant(df[[core_var] + controls])

        model = sm.OLS(y, X).fit(
            cov_type="cluster",
            cov_kwds={"groups": df[cluster_var]}
        )

        report = self._format_report(model, dep_var, core_var, controls,
                                     diagnostics, fe_type, cluster_var)

        return {
            "model": model,
            "report": report,
            "diagnostics": diagnostics
        }

    def _run_diagnostics(self, df, dep_var, indep_vars):
        diagnostics = {}
        X = sm.add_constant(df[indep_vars])
        vif_data = {}
        for i, var in enumerate(indep_vars):
            vif_data[var] = variance_inflation_factor(X.values, i + 1)
        diagnostics["vif"] = vif_data
        diagnostics["high_vif"] = {
            k: v for k, v in vif_data.items() if v > 10
        }

        y = df[dep_var]
        model = sm.OLS(y, X).fit()
        residuals = model.resid
        diagnostics["residual_stats"] = {
            "mean": float(residuals.mean()),
            "std": float(residuals.std()),
            "skew": float(residuals.skew()),
            "kurtosis": float(residuals.kurtosis())
        }

        return diagnostics

    def _format_report(self, model, dep_var, core_var, controls,
                       diagnostics, fe_type, cluster_var):
        lines = []
        lines.append("面板回归分析报告")
        lines.append("=" * 50)
        lines.append("因变量: {}".format(dep_var))
        lines.append("核心自变量: {}".format(core_var))
        lines.append("控制变量: {}".format(", ".join(controls) if controls else "无"))
        lines.append("固定效应: {}".format(fe_type))
        lines.append("聚类标准误: {}".format(cluster_var))
        lines.append("")
        lines.append("--- 核心结果 ---")
        lines.append("系数: {:.4f}".format(model.params[core_var]))
        lines.append("标准误: {:.4f}".format(model.bse[core_var]))
        lines.append("p值: {:.4f}".format(model.pvalues[core_var]))
        lines.append("95%CI: [{:.4f}, {:.4f}]".format(
            *model.conf_int().loc[core_var]
        ))
        lines.append("R-squared: {:.4f}".format(model.rsquared))
        lines.append("观测数: {}".format(int(model.nobs)))
        lines.append("")
        lines.append("--- 诊断检验 ---")
        if diagnostics.get("high_vif"):
            lines.append("警告: 存在高VIF变量:")
            for var, vif in diagnostics["high_vif"].items():
                lines.append("  {} = {:.1f}".format(var, vif))
        else:
            lines.append("VIF检验: 通过（所有VIF<10）")

        return "\n".join(lines)
```

**描述统计Skill：**

```yaml
name: descriptive_statistics_skill
description: 生成描述统计表，含分组统计和缺失值报告
triggers:
  - 描述统计
  - 描述性统计
  - summary statistics
parameters:
  required:
    - data_path: 数据文件路径
    - variables: 分析变量列表
  optional:
    - group_var: 分组变量，默认None
    - output_format: 输出格式，dataframe/latex/csv，默认dataframe
    - include_missing: 是否包含缺失统计，默认true
output:
  type: dict
  fields:
    - table: 描述统计表
    - missing_report: 缺失值报告
    - group_stats: 分组统计（如果指定group_var）
```

```python
class DescriptiveStatisticsSkill:
    def execute(self, data_path, variables, group_var=None,
                output_format="dataframe", include_missing=True):
        df = pd.read_stata(data_path)

        stats = df[variables].describe().T
        stats["skew"] = df[variables].skew()
        stats["kurtosis"] = df[variables].kurtosis()

        result = {"table": stats}

        if include_missing:
            missing = df[variables].isnull().sum()
            missing_pct = df[variables].isnull().mean() * 100
            result["missing_report"] = pd.DataFrame({
                "missing_count": missing,
                "missing_pct": missing_pct
            })

        if group_var and group_var in df.columns:
            group_stats = df.groupby(group_var)[variables].agg(
                ["mean", "std", "count"]
            )
            result["group_stats"] = group_stats

        if output_format == "latex":
            result["latex"] = stats.to_latex(
                float_format="%.2f",
                caption="描述统计表"
            )
        elif output_format == "csv":
            stats.to_csv("descriptive_stats.csv")

        return result
```

**可视化Skill：**

```yaml
name: regression_visualization_skill
description: 生成回归分析相关可视化
triggers:
  - 回归可视化
  - 系数图
  - 事件研究图
parameters:
  required:
    - model: 回归模型对象或结果字典
    - plot_type: 图表类型，coef_plot/event_study/scatter
  optional:
    - variables: 要展示的变量列表，默认展示所有
    - ci_level: 置信区间水平，默认0.95
    - output_path: 保存路径，默认None（显示）
    - figsize: 图表尺寸，默认(10, 6)
output:
  type: matplotlib.figure.Figure
```

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

class RegressionVisualizationSkill:
    def execute(self, model, plot_type, variables=None,
                ci_level=0.95, output_path=None, figsize=(10, 6)):
        if plot_type == "coef_plot":
            fig = self._coef_plot(model, variables, ci_level, figsize)
        elif plot_type == "event_study":
            fig = self._event_study_plot(model, figsize)
        elif plot_type == "scatter":
            fig = None

        if output_path and fig:
            fig.savefig(output_path, dpi=300, bbox_inches="tight")
        return fig

    def _coef_plot(self, model, variables, ci_level, figsize):
        if variables is None:
            variables = [
                v for v in model.params.index
                if v != "const"
            ]

        coefs = model.params[variables]
        conf = model.conf_int(alpha=1 - ci_level).loc[variables]

        fig, ax = plt.subplots(figsize=figsize)
        y_pos = range(len(variables))

        ax.barh(y_pos, coefs, color="steelblue", alpha=0.7)
        ax.hlines(y_pos, conf[0], conf[1], colors="black", linewidth=1.5)

        ax.axvline(x=0, color="red", linestyle="--", linewidth=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.set_xlabel("系数值")
        ax.set_title("回归系数图（{}%置信区间）".format(int(ci_level * 100)))

        plt.tight_layout()
        return fig

    def _event_study_plot(self, model, figsize):
        event_vars = [
            v for v in model.params.index
            if v.startswith("t_") or v.startswith("post_") or v.startswith("pre_")
        ]

        if not event_vars:
            return None

        coefs = model.params[event_vars]
        conf = model.conf_int().loc[event_vars]

        fig, ax = plt.subplots(figsize=figsize)
        periods = range(len(event_vars))

        ax.plot(periods, coefs, "o-", color="steelblue", linewidth=2)
        ax.fill_between(
            periods, conf[0], conf[1],
            alpha=0.2, color="steelblue"
        )
        ax.axhline(y=0, color="red", linestyle="--", linewidth=0.8)
        ax.set_xlabel("时期")
        ax.set_ylabel("系数")
        ax.set_title("事件研究图")

        plt.tight_layout()
        return fig
```

### Skill的参数化

参数化是分析Skill可复用的关键。设计参数时区分三个层次：

1. **数据参数**：数据路径、变量名——每次分析都不同
2. **方法参数**：模型类型、标准误选择——影响方法论选择
3. **输出参数**：格式、路径——不影响分析结果

```python
PARAMETER_SPEC = {
    "data_path": {
        "type": "str",
        "required": True,
        "category": "data",
        "description": "数据文件路径"
    },
    "dep_var": {
        "type": "str",
        "required": True,
        "category": "data",
        "description": "因变量名"
    },
    "fe_type": {
        "type": "str",
        "required": False,
        "default": "entity",
        "category": "method",
        "options": ["entity", "twoway", "none"],
        "description": "固定效应类型，影响方法论选择"
    },
    "cluster_var": {
        "type": "str",
        "required": False,
        "default": "province",
        "category": "method",
        "description": "聚类标准误变量，影响推断"
    },
    "output_format": {
        "type": "str",
        "required": False,
        "default": "dataframe",
        "category": "output",
        "options": ["dataframe", "latex", "csv"],
        "description": "输出格式，不影响分析结果"
    }
}
```

### Skill链式调用

分析通常是多步骤流程，Skill可以链式调用：

```python
class AnalysisPipeline:
    def __init__(self, skills_registry):
        self.skills = skills_registry
        self.results = {}

    def run(self, pipeline_config):
        for step in pipeline_config:
            skill_name = step["skill"]
            params = step.get("params", {})

            for key, value in params.items():
                if isinstance(value, str) and value.startswith("$"):
                    ref_key = value[1:]
                    params[key] = self._resolve_reference(ref_key)

            skill = self.skills[skill_name]
            result = skill.execute(**params)
            self.results[step["name"]] = result

        return self.results

    def _resolve_reference(self, ref_key):
        parts = ref_key.split(".")
        obj = self.results[parts[0]]
        for part in parts[1:]:
            if isinstance(obj, dict):
                obj = obj[part]
            elif hasattr(obj, part):
                obj = getattr(obj, part)
        return obj

PIPELINE_CONFIG = [
    {
        "name": "desc_stats",
        "skill": "descriptive_statistics_skill",
        "params": {
            "data_path": "./data/panel.dta",
            "variables": ["log_wage", "education", "experience", "urban"]
        }
    },
    {
        "name": "baseline",
        "skill": "panel_regression_skill",
        "params": {
            "data_path": "./data/panel.dta",
            "dep_var": "log_wage",
            "core_var": "education",
            "controls": ["experience", "urban"]
        }
    },
    {
        "name": "coef_plot",
        "skill": "regression_visualization_skill",
        "params": {
            "model": "$baseline.model",
            "plot_type": "coef_plot",
            "output_path": "./output/baseline_coef.png"
        }
    }
]
```

### Skill与Agent的配合

Skill提供原子能力，Agent提供编排逻辑：

```python
def agent_orchestrated_analysis(agent, research_question, data_path):
    plan = agent.plan_analysis(research_question, data_path)

    for step in plan:
        skill = step["skill"]
        params = step["params"]

        result = skill.execute(**params)

        if step.get("requires_review"):
            review = agent.review_result(result, step["review_criteria"])
            if not review["approved"]:
                params = agent.adjust_params(params, review["suggestions"])
                result = skill.execute(**params)

    return agent.synthesize_results()
```

## 关键细节与易错点

- **易错：Skill封装粒度过细或过粗**。过细（每个统计检验一个Skill）导致调用繁琐；过粗（整个分析流程一个Skill）失去灵活性。推荐粒度：一个Skill对应一个"方法论决策单元"——比如"面板回归"是一个决策单元，但"数据清洗"不应与"回归"混在同一个Skill
- **易错：方法参数使用了错误默认值**。如果面板回归Skill默认不加聚类标准误，使用者可能不知道需要手动指定。方法参数的默认值应是"方法论最佳实践"而非"最简实现"
- **易错：Skill输出缺乏方法论文档**。只输出系数表但没有说明用了什么固定效应、什么标准误——这样的结果无法被审稿人审查。Skill输出必须包含方法论文档
- **易错：链式调用中参数传递出错**。前一步输出的列名与后一步期望的列名不一致，导致静默错误。链式调用时应做接口校验
- **易错：Skill不支持方法论变体**。同一个回归分析可能需要不同变体（FE vs RE、不同聚类层级），如果Skill只支持一种，分析者会在Skill之外手写代码，破坏一致性

## 社科科研示例

**场景**：一位管理学博士生研究"数字化转型对企业绩效的影响"，需要执行基准回归、异质性分析、机制检验和稳健性检验。

```python
skills = {
    "panel_regression": PanelRegressionSkill(),
    "descriptive_stats": DescriptiveStatisticsSkill(),
    "regression_viz": RegressionVisualizationSkill()
}

pipeline = AnalysisPipeline(skills)

results = pipeline.run([
    {
        "name": "desc",
        "skill": "descriptive_stats",
        "params": {
            "data_path": "./data/firm_panel.dta",
            "variables": ["roa", "digital_index", "size", "leverage", "age"],
            "group_var": "industry",
            "output_format": "latex"
        }
    },
    {
        "name": "baseline",
        "skill": "panel_regression",
        "params": {
            "data_path": "./data/firm_panel.dta",
            "dep_var": "roa",
            "core_var": "digital_index",
            "controls": ["size", "leverage", "age"],
            "fe_type": "twoway",
            "cluster_var": "industry"
        }
    },
    {
        "name": "baseline_plot",
        "skill": "regression_viz",
        "params": {
            "model": "$baseline.model",
            "plot_type": "coef_plot",
            "output_path": "./output/baseline_coef.png"
        }
    }
])

print(results["baseline"]["report"])
```

## 拓展学习

- 《Design Patterns》——软件设计模式，理解Skill封装的抽象原则
- scikit-learn Pipeline——sklearn的管道设计，分析Skill链式调用的参考
- 《The Art of Readable Code》——代码可读性，Skill代码质量保障
- Python `dataclasses`与`typing`——Skill参数的类型安全设计
- 《Refactoring》——代码重构，Skill迭代优化的方法论

## 参考链接

- https://scikit-learn.org/stable/modules/compose.html — sklearn Pipeline文档
- https://docs.python.org/3/library/dataclasses.html — Python dataclasses
- https://matplotlib.org/ — matplotlib可视化库
- https://seaborn.pydata.org/ — seaborn统计可视化
- https://cran.r-project.org/package=stargazer — Python回归结果格式化
