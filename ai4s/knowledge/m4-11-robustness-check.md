# 稳健性检验

> **引入时机**：W7 | **核心挑战**："核心结果是否在不同条件下都成立？如何系统性地验证？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

W7的核心主题是"做对"研究，而稳健性检验是"做对"的终极保障。很多博士生对稳健性检验的理解停留在"我又跑了一遍，结果差不多"——这不是稳健性检验，这是重复。真正的稳健性检验是：系统性地挑战你的核心假设，检验结论在关键假设被放松或替代后是否仍然成立。

稳健性检验在AI辅助场景下有了新的重要性。AI让"跑一遍"变得极其容易——换个因变量、换个控制变量、换个样本子集，几秒钟就能得到新结果。但容易不等于正确。如果你没有系统性地设计稳健性检验方案，而是随性地"多试几种"，你可能只是在做数据挖掘——直到找到一个看起来稳健的结果。

本知识点教你从方法论逻辑出发设计稳健性检验，让AI帮你高效执行而非随意尝试。核心原则：稳健性检验不是"我又跑了一遍"，而是"我检验了关键假设是否成立"。

## 这个知识点的核心内容

### 稳健性检验的方法论逻辑

**错误理解：** 稳健性检验就是多跑几个模型，看看结果是否一致。

**正确理解：** 稳健性检验是系统性地检验支撑核心结论的关键假设是否成立。每个稳健性检验对应一个具体的假设威胁：

```
核心结论 ← 依赖于 → 关键假设1 → 替代假设1a → 检验：替换变量
                     关键假设2 → 替代假设2a → 检验：替换模型
                     关键假设3 → 替代假设3a → 检验：替换样本
                     关键假设4 → 替代假设4a → 检验：安慰剂检验
```

**从研究假设到稳健性检验的推导过程：**

1. 写出核心结论所依赖的每个关键假设
2. 对每个假设，思考"如果这个假设不成立，结论会如何变化？"
3. 设计一个检验来区分"原假设"和"替代假设"
4. 预先确定判断标准：什么程度的不一致算"不稳健"？

```python
def design_robustness_plan(research_context, llm_client):
    prompt = """你是一位方法论顾问。基于以下研究上下文，系统设计稳健性检验方案。

研究问题：{question}
核心发现：{finding}
核心模型：{model}
数据结构：{data_structure}
关键假设：
{assumptions}

请为每个关键假设设计至少一个稳健性检验，包含：
1. 被检验的假设
2. 替代假设
3. 检验方法
4. 预期结果（如果原假设成立vs如果替代假设成立）
5. 判断标准

注意：每个检验必须针对一个具体的方法论威胁，不能是"换个模型试试"这样的泛化检验。""".format(
        **research_context
    )

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

### 常见的稳健性检验类型

**1. 替换变量检验**

检验核心结论是否对变量的操作化方式敏感：

```python
def alternative_variable_robustness(data, dep_var_alternatives,
                                     core_var_alternatives, controls,
                                     model_func):
    results = {}

    for alt_dep in dep_var_alternatives:
        result = model_func(data, alt_dep, core_var_alternatives[0],
                           controls)
        results["dep_{}".format(alt_dep)] = {
            "coefficient": float(result.params[core_var_alternatives[0]]),
            "p_value": float(result.pvalues[core_var_alternatives[0]]),
            "r_squared": float(result.rsquared),
            "n_obs": int(result.nobs)
        }

    for alt_var in core_var_alternatives:
        result = model_func(data, dep_var_alternatives[0], alt_var,
                           controls)
        results["core_{}".format(alt_var)] = {
            "coefficient": float(result.params[alt_var]),
            "p_value": float(result.pvalues[alt_var]),
            "r_squared": float(result.rsquared),
            "n_obs": int(result.nobs)
        }

    baseline_sign = np.sign(
        results["dep_{}".format(dep_var_alternatives[0])]["coefficient"]
    )
    consistent_count = sum(
        1 for r in results.values()
        if np.sign(r["coefficient"]) == baseline_sign
    )

    return {
        "results": results,
        "consistency_rate": consistent_count / len(results),
        "assessment": (
            "替换变量后方向一致率{:.0%}".format(
                consistent_count / len(results)
            )
        )
    }
```

**2. 替换模型检验**

检验核心结论是否对模型设定敏感：

```python
def alternative_model_robustness(data, dep_var, core_var, controls,
                                  entity_var, time_var):
    results = {}

    y = data[dep_var]
    X_base = data[[core_var] + controls]
    X_with_fe = data[[core_var] + controls + [entity_var, time_var]]

    import statsmodels.api as sm

    model_pooled = sm.OLS(y, sm.add_constant(X_base)).fit(
        cov_type="cluster",
        cov_kwds={"groups": data[entity_var]}
    )
    results["pooled_ols"] = {
        "coefficient": float(model_pooled.params[core_var]),
        "p_value": float(model_pooled.pvalues[core_var]),
        "model": "Pooled OLS + 聚类标准误"
    }

    from linearmodels.panel import PanelOLS
    panel_data = data.set_index([entity_var, time_var])
    y_panel = panel_data[dep_var]
    X_panel = sm.add_constant(panel_data[[core_var] + controls])

    model_fe = PanelOLS(y_panel, X_panel, entity_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    results["fe_entity"] = {
        "coefficient": float(model_fe.params[core_var]),
        "p_value": float(model_fe.pvalues[core_var]),
        "model": "个体固定效应"
    }

    model_fe2 = PanelOLS(
        y_panel, X_panel, entity_effects=True, time_effects=True
    ).fit(cov_type="clustered", cluster_entity=True)
    results["fe_twoway"] = {
        "coefficient": float(model_fe2.params[core_var]),
        "p_value": float(model_fe2.pvalues[core_var]),
        "model": "双向固定效应"
    }

    baseline_sign = np.sign(results["fe_entity"]["coefficient"])
    consistent = all(
        np.sign(r["coefficient"]) == baseline_sign
        for r in results.values()
    )

    return {
        "results": results,
        "direction_consistent": consistent,
        "assessment": (
            "所有模型设定下方向一致" if consistent
            else "不同模型设定下方向不一致，需进一步调查"
        )
    }
```

**3. 替换样本检验**

检验核心结论是否对样本选择敏感：

```python
def sample_robustness(data, dep_var, core_var, controls, model_func,
                       exclude_conditions):
    full_result = model_func(data, dep_var, core_var, controls)
    full_coef = full_result.params[core_var]
    full_sign = np.sign(full_coef)

    results = {"full_sample": {
        "coefficient": float(full_coef),
        "p_value": float(full_result.pvalues[core_var]),
        "n_obs": int(full_result.nobs)
    }}

    for condition_name, condition_func in exclude_conditions.items():
        subset = data[condition_func(data)]
        if len(subset) < 50:
            results[condition_name] = {
                "status": "skipped",
                "reason": "样本量不足(<50)"
            }
            continue

        result = model_func(subset, dep_var, core_var, controls)
        results[condition_name] = {
            "coefficient": float(result.params[core_var]),
            "p_value": float(result.pvalues[core_var]),
            "n_obs": int(result.nobs),
            "direction_consistent": np.sign(result.params[core_var]) == full_sign
        }

    return results

EXCLUDE_CONDITIONS = {
    "exclude_megacities": lambda df: df["population"] < df["population"].quantile(0.95),
    "exclude_western": lambda df: df["region"] != "西部",
    "exclude_covid_year": lambda df: df["year"] != 2020,
    "exclude_small_firms": lambda df: df["firm_size"] >= df["firm_size"].quantile(0.1),
}
```

**4. 安慰剂检验**

检验核心发现是否可能由未观测因素驱动：

```python
import numpy as np

def placebo_test(data, dep_var, core_var, controls, model_func,
                  n_placebo=500, placebo_type="randomize_treatment"):
    real_result = model_func(data, dep_var, core_var, controls)
    real_coef = real_result.params[core_var]

    placebo_coefs = []

    for i in range(n_placebo):
        data_placebo = data.copy()

        if placebo_type == "randomize_treatment":
            data_placebo[core_var] = np.random.permutation(
                data_placebo[core_var].values
            )
        elif placebo_type == "fake_treatment_year":
            years = data_placebo["year"].unique()
            fake_year = np.random.choice(years[:-2])
            data_placebo["placebo_treatment"] = (
                data_placebo["year"] >= fake_year
            ).astype(int)
            core_var = "placebo_treatment"

        try:
            placebo_result = model_func(data_placebo, dep_var, core_var,
                                        controls)
            placebo_coefs.append(float(placebo_result.params[core_var]))
        except Exception:
            continue

    placebo_coefs = np.array(placebo_coefs)
    p_value_placebo = np.mean(np.abs(placebo_coefs) >= np.abs(real_coef))

    return {
        "real_coefficient": float(real_coef),
        "placebo_mean": float(np.mean(placebo_coefs)),
        "placebo_std": float(np.std(placebo_coefs)),
        "placebo_p_value": float(p_value_placebo),
        "interpretation": (
            "安慰剂检验通过：真实系数在安慰剂分布中出现的概率p={:.3f}，"
            "拒绝'结果由随机因素驱动'的零假设".format(p_value_placebo)
            if p_value_placebo < 0.05
            else "安慰剂检验未通过：真实系数在安慰剂分布中不罕见，"
            "结果可能由未观测因素驱动".format(p_value_placebo)
        )
    }
```

### AI辅助稳健性检验的设计与执行

AI在稳健性检验中的核心价值是：帮你系统性地识别假设威胁并设计检验方案，而非随机尝试：

```python
def ai_assisted_robustness_design(research_context, baseline_result,
                                   llm_client):
    prompt = """基于以下研究设计和基准回归结果，设计系统性的稳健性检验方案。

研究问题：{question}
数据结构：{data_structure}
基准模型：{model_spec}
基准结果：核心系数={coef}, p={pval}
关键假设：
{assumptions}

请从以下维度各设计至少一个检验：
1. 变量操作化假设（因变量/自变量的测量是否有替代方案？）
2. 模型设定假设（固定效应/标准误/函数形式是否有替代方案？）
3. 样本选择假设（样本范围是否有替代方案？）
4. 内生性假设（是否有安慰剂检验/工具变量/falsification test？）

每个检验请说明：
- 检验的假设威胁是什么
- 具体的检验操作
- 如何判断通过/未通过

注意：不要建议"跑50种模型看哪个显著"——这不是稳健性检验，是数据挖掘。""".format(
        question=research_context["question"],
        data_structure=research_context["data_structure"],
        model_spec=research_context["model_spec"],
        coef=baseline_result["coef"],
        pval=baseline_result["pval"],
        assumptions=research_context["assumptions"]
    )

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

### 稳健性检验结果的解读

稳健性检验的解读不是简单的"一致/不一致"，而是评估不一致的来源和含义：

```python
def interpret_robustness_results(robustness_results, baseline_coef,
                                  baseline_pval):
    interpretation = {
        "overall_assessment": None,
        "details": []
    }

    n_total = len(robustness_results)
    n_consistent_direction = 0
    n_consistent_significance = 0

    baseline_sign = np.sign(baseline_coef)

    for name, result in robustness_results.items():
        if result.get("status") == "skipped":
            continue

        coef = result.get("coefficient", 0)
        pval = result.get("p_value", 1)
        direction_consistent = np.sign(coef) == baseline_sign
        sig_consistent = (pval < 0.05) == (baseline_pval < 0.05)

        if direction_consistent:
            n_consistent_direction += 1
        if sig_consistent:
            n_consistent_significance += 1

        interpretation["details"].append({
            "test": name,
            "coefficient": coef,
            "p_value": pval,
            "direction_consistent": direction_consistent,
            "significance_consistent": sig_consistent,
            "note": (
                "方向一致且显著" if direction_consistent and pval < 0.05
                else "方向一致但不显著" if direction_consistent and pval >= 0.05
                else "方向不一致" if not direction_consistent
                else ""
            )
        })

    dir_rate = n_consistent_direction / n_total if n_total > 0 else 0
    sig_rate = n_consistent_significance / n_total if n_total > 0 else 0

    if dir_rate >= 0.8 and sig_rate >= 0.6:
        interpretation["overall_assessment"] = "稳健"
    elif dir_rate >= 0.6:
        interpretation["overall_assessment"] = "基本稳健，但存在敏感性"
    else:
        interpretation["overall_assessment"] = "不稳健，结论对设定敏感"

    return interpretation
```

## 关键细节与易错点

- **易错：混淆"重复"和"稳健性检验"**。换个控制变量又跑一遍，结果差不多，这不叫稳健性检验。稳健性检验必须针对一个具体的方法论威胁——"如果X的测量有误差呢？""如果遗漏了某类固定效应呢？"
- **易错：只报告"通过"的检验**。这是选择性报告，本质上是另一种形式的p-hacking。所有设计的稳健性检验都应报告，包括"未通过"的，并解释不一致的原因
- **易错：安慰剂检验设计不当**。安慰剂检验的核心是"在逻辑上不应该有效应的设定下检验是否出现效应"。常见错误：随机化处理变量但没有保持面板结构，导致标准误被低估
- **易错：过度依赖AI设计检验方案**。AI可能建议你做"加入更多控制变量"——但这不是稳健性检验，这是模型扩展。稳健性检验应放松假设而非增加约束
- **易错：忽视效应量变化**。即使方向一致，如果系数大小变化巨大（基准0.5，稳健性0.05），说明结论对设定虽然方向稳健但效应量敏感，需要在论文中讨论

## 社科科研示例

**场景**：一位政治学博士生研究"互联网普及对政治参与的影响"，基准回归显示互联网普及率系数为0.234（p=0.004）。

```python
research_context = {
    "question": "互联网普及对政治参与的影响",
    "data_structure": "省级面板(31省×2012-2023)",
    "model_spec": "双向固定效应+省聚类标准误",
    "assumptions": [
        "政治参与的测量（投票率）是有效代理变量",
        "互联网普及率准确反映数字接入",
        "无遗漏时变变量",
        "因果方向是互联网→参与而非参与→互联网"
    ]
}

robustness_plan = ai_assisted_robustness_design(
    research_context,
    baseline_result={"coef": 0.234, "pval": 0.004},
    llm_client=llm
)

alt_var_results = alternative_variable_robustness(
    data=panel_df,
    dep_var_alternatives=["voting_rate", "petition_rate", "online_discussion_rate"],
    core_var_alternatives=["internet_penetration", "broadband_coverage", "smartphone_ownership"],
    controls=["gdp_per_capita", "education_level", "urbanization"],
    model_func=panel_regression_func
)

placebo_result = placebo_test(
    data=panel_df,
    dep_var="voting_rate",
    core_var="internet_penetration",
    controls=["gdp_per_capita", "education_level", "urbanization"],
    model_func=panel_regression_func,
    n_placebo=1000,
    placebo_type="randomize_treatment"
)

print("安慰剂检验p值: {:.3f}".format(placebo_result["placebo_p_value"]))
print(placebo_result["interpretation"])
```

## 拓展学习

- 《Mostly Harmless Econometrics》——稳健性检验在因果推断中的角色
- 《Mastering Metrics》——稳健性检验的实践指南
- 《The Effect》——效应量与稳健性的关系
- Angrist & Pischke的论文——经济学中稳健性检验的标杆
- 《Sensitivity Analysis》——敏感性分析方法论

## 参考链接

- https://mixtape.scunning.com/ — Causal Inference: The Mixtape
- https://www.theeffectbook.net/ — The Effect在线书
- https://www.nber.org/papers/w24392 — NBER关于稳健性检验的方法论讨论
- https://osf.io/ — Open Science Framework（预注册稳健性检验方案）
- https://EGAP.org/ — EGAP因果推断方法资源
