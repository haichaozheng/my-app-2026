# AI辅助编程(Python/R/Stata)深度应用

> **引入时机**：W6 | **核心挑战**："代码量大、逻辑复杂，如何用LLM深度辅助编程？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

W5开始进入研究方案实施阶段，代码量骤增。你可能需要同时处理数据清洗、变量构造、多种模型回归、稳健性检验、结果可视化等十几个脚本。单纯让AI"帮我写个回归代码"已经不够——你需要的是AI深度参与多文件协作、上下文管理、代码质量保障的编程模式。

很多同学在用AI写代码时遇到一个瓶颈：单次交互能生成正确的代码片段，但多个片段组合后出bug；AI不知道项目其他文件中已定义的函数和变量；生成的代码"能跑"但缺乏错误处理和文档。这些问题的根源是：你把AI当作"代码生成器"而非"编程协作伙伴"，没有建立有效的上下文共享和质量保障机制。

掌握AI深度辅助编程后，你能让AI理解项目全局而非单个文件，生成可靠而非仅仅"能跑"的代码，并建立代码质量保障流程。这将让你的研究代码从"勉强可用"提升到"可复现、可维护、可审查"的学术标准。

## 这个知识点的核心内容

### 科研编程的AI深度辅助模式

从浅层到深层，AI辅助编程有三个模式：

**浅层模式：问答式**
- 场景：问AI"pandas如何做分组统计"
- 问题：AI不知道你的数据结构、变量命名、项目约定
- 适用：简单语法查询

**中层模式：上下文式**
- 场景：把当前文件发给AI，让它"帮我补全这个函数"
- 优势：AI知道当前文件的变量和逻辑
- 问题：不知道项目其他文件

**深层模式：项目式**
- 场景：AI理解整个项目结构，在多文件间协作
- 优势：生成的代码与项目一致、可跨文件调用
- 实现：使用opencode/cursor/trae的项目级上下文功能

```python
# 项目结构示例（AI需要理解全局）
# research_project/
# ├── config.py          # 全局配置
# ├── data_loader.py     # 数据加载
# ├── variables.py       # 变量构造
# ├── models.py          # 模型定义
# ├── analysis.py        # 分析主流程
# └── visualization.py   # 可视化
```

**深层模式的核心实践：**

1. 在`config.py`中定义所有路径和参数，AI在生成代码时引用这些配置
2. 每个模块有明确的输入输出接口，AI可以跨模块生成调用代码
3. 使用opencode的`@file`引用或cursor的`@codebase`让AI读取项目上下文

### Python数据分析

Python是社科AI4S的核心语言，以下是与AI协作的关键实践：

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def load_and_prepare(filepath, config):
    df = pd.read_stata(filepath)
    df = df[df["year"] >= config["start_year"]]
    df = df[df["province"].isin(config["provinces"])]
    return df

def construct_variables(df, var_config):
    if var_config["dep_var"] == "log_income":
        df["log_income"] = np.log(df["income"] + 1)
    if "interaction" in var_config:
        for inter in var_config["interaction"]:
            df["{}_x_{}".format(inter[0], inter[1])] = (
                df[inter[0]] * df[inter[1]]
            )
    return df

def panel_regression(df, dep_var, indep_vars, entity_var, time_var,
                     controls=None, fe_type="entity"):
    if controls is None:
        controls = []
    all_indep = indep_vars + controls
    formula = "{} ~ {}".format(dep_var, " + ".join(all_indep))
    if fe_type == "entity":
        formula += " + EntityEffects"
    elif fe_type == " "twoway"":
        formula += " + EntityEffects + TimeEffects"
    y = df[dep_var]
    X = sm.add_constant(df[all_indep])
    model = sm.OLS(y, X).fit(cov_type="cluster",
                              cov_kwds={"groups": df[entity_var]})
    return model

def check_vif(df, indep_vars):
    X = df[indep_vars]
    X = sm.add_constant(X)
    vif_data = pd.DataFrame()
    vif_data["variable"] = indep_vars
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i + 1)
        for i in range(len(indep_vars))
    ]
    return vif_data
```

**与AI协作的关键提示模式：**

```
请基于项目中的config.py和data_loader.py，帮我写一个面板回归分析函数。
要求：
1. 支持固定效应和随机效应选择
2. 聚类标准误默认按省份聚类
3. 输出关键统计量（系数、标准误、p值、R-squared、观测数）
4. 返回结果对象而非直接打印
```

### R统计分析

R在统计方法上有丰富生态，以下是AI协作的典型场景：

```r
library(tidyverse)
library(fixest)
library(plm)
library(modelsummary)

load_data <- function(filepath) {
  df <- haven::read_dta(filepath)
  df <- df %>%
    filter(year >= 2010, !is.na(province))
  return(df)
}

run_panel_fe <- function(df, dep_var, indep_var, controls = NULL,
                         entity = "province", time = "year",
                         cluster = "province") {
  formula_str <- paste0(dep_var, " ~ ", indep_var)
  if (!is.null(controls)) {
    formula_str <- paste0(formula_str, " | ",
                         paste(controls, collapse = " + "))
  }
  formula_str <- paste0(formula_str, " | ", entity, " + ", time)

  model <- feols(
    as.formula(formula_str),
    data = df,
    cluster = cluster
  )
  return(model)
}

export_results <- function(model_list, output_path) {
  modelsummary(
    model_list,
    output = output_path,
    stars = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
    gof_map = c("nobs", "r.squared", "adj.r.squared", "FE:entity", "FE:time")
  )
}
```

### Stata自动化

Stata在经济学研究中仍然主流，AI可以辅助生成可复现的ado文件：

```stata
* research_main.do
clear all
set more off
global root "C:/research/project"
global data "$root/data"
global output "$root/output"

program define panel_analysis, rclass
    syntax varlist(min=2), DEPvar(string) CLUSTERvar(string) [CONTROLS(string)]
    
    local indep_var : word 1 of `varlist'
    
    * 固定效应回归
    reghdfe `dep_var' `indep_var' `controls', absorb(id year) vce(cluster `clustervar')
    
    * 存储结果
    return scalar coef = _b[`indep_var']
    return scalar se = _se[`indep_var']
    return scalar pval = 2 * ttail(e(df_r), abs(_b[`indep_var'] / _se[`indep_var']))
    return scalar r2 = e(r2)
    return scalar N = e(N)
end

* 执行分析
use "$data/panel_data.dta", clear
panel_analysis treatment, depvar(log_wage) clustervar(province) controls(education experience)
```

**AI辅助Stata编程的要点：**
- 让AI生成完整的do文件而非单条命令，确保可复现
- 用`program define`封装分析逻辑，提升复用性
- 让AI帮助编写`log`和`capture`语句，确保错误可追溯

### 代码质量保障

科研代码的质量直接影响研究可复现性和可信度：

**测试：**

```python
def test_variable_construction():
    df = pd.DataFrame({
        "income": [1000, 2000, 0, np.nan],
        "age": [25, 35, 45, 55]
    })
    result = construct_variables(df, {
        "dep_var": "log_income",
        "interaction": [["log_income", "age"]]
    })
    assert result["log_income"].iloc[0] == np.log(1001)
    assert pd.isna(result["log_income"].iloc[3])
    assert "log_income_x_age" in result.columns
    print("变量构造测试通过")

test_variable_construction()
```

**版本控制：**

```python
# .gitignore for research project
# *.dta
# *.csv
# *.xlsx
# output/figures/
# __pycache__/
# .env
```

**文档规范：**

```python
def panel_regression(df, dep_var, indep_vars, entity_var, time_var,
                     controls=None, fe_type="entity"):
    """
    执行面板数据固定效应回归。

    Parameters
    ----------
    df : pd.DataFrame
        面板数据，需包含entity_var和time_var列
    dep_var : str
        因变量列名
    indep_vars : list[str]
        核心自变量列名列表
    entity_var : str
        个体标识列名
    time_var : str
        时间标识列名
    controls : list[str], optional
        控制变量列名列表
    fe_type : str
        固定效应类型，"entity"或"twoway"

    Returns
    -------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        回归结果对象，可调用.summary()查看完整结果

    Notes
    -----
    默认使用个体聚类标准误。如需双向聚类，请使用
    cov_type="cluster", cov_kwds={"groups": (df[entity_var], df[time_var])}
    """
    pass
```

## 关键细节与易错点

- **易错：给AI的上下文不足**。AI不知道你的变量命名、数据结构、项目约定时，生成的代码几乎必然需要大量修改。解决方案：在对话开头提供关键上下文（变量列表、数据结构、项目约定），或使用opencode/cursor的项目级上下文功能
- **易错：不验证AI生成代码的正确性**。AI可能生成"看起来对但逻辑有误"的代码——比如pandas的`groupby`后忘记`reset_index`，或者Stata的`reghdfe`中交互项的设定错误。每段AI生成的代码都必须人工审查逻辑
- **易错：混用多种语言而不统一接口**。有些同学Python、R、Stata混用，导致分析流程难以复现。建议：主分析流程用一种语言（推荐Python），仅在需要特定统计方法时调用R或Stata，并通过文件或API统一接口
- **易错：不保存代码运行环境**。Python包版本、R包版本差异可能导致结果不同。使用`pip freeze > requirements.txt`或`renv::snapshot()`记录环境
- **易错：忽视随机种子设定**。涉及随机抽样、交叉验证等环节时，不设随机种子导致结果不可复现。在分析脚本开头统一设定`np.random.seed(42)`

## 社科科研示例

**场景**：一位经济学博士生研究"数字经济对区域创新的影响"，需要用Python完成从数据清洗到面板回归的全流程。

**AI协作流程：**

1. **项目初始化**：在opencode中描述项目结构，让AI理解全局
2. **数据清洗**：让AI基于原始数据字典编写清洗脚本
3. **变量构造**：与AI讨论操作化方案，生成代码后审查逻辑
4. **基准回归**：AI生成面板回归代码，你审查模型设定和标准误选择
5. **稳健性检验**：AI生成多种替代设定的回归代码
6. **结果导出**：AI生成格式化的回归结果表

```python
# analysis.py - 主分析流程
import numpy as np
import pandas as pd
from config import Config
from data_loader import load_and_prepare
from variables import construct_all_variables
from models import run_baseline, run_robustness

np.random.seed(Config.RANDOM_SEED)

df = load_and_prepare(Config.DATA_PATH, Config)
df = construct_all_variables(df, Config.VAR_CONFIG)

baseline = run_baseline(
    df,
    dep_var="log_patent",
    core_var="digital_index",
    controls=Config.CONTROLS,
    entity="city",
    time="year",
    cluster="province"
)

robustness_results = run_robustness(
    df,
    dep_var="log_patent",
    core_var="digital_index",
    controls=Config.CONTROLS,
    entity="city",
    time="year",
    cluster="province",
    alt_dep_vars=["log_invention", "log_utility"],
    alt_models=["random_effect", "heckman"],
    placebo=True
)

from visualization import plot_event_study, plot_coefficient
plot_event_study(baseline, output=Config.OUTPUT_DIR + "/event_study.png")
plot_coefficient(robustness_results, output=Config.OUTPUT_DIR + "/coef_plot.png")
```

## 拓展学习

- 《The Missing Semester of Your CS Education》——MIT课程，科研编程必备技能
- Python for Data Analysis (Wes McKinney)——pandas作者的数据分析经典
- R for Data Science (Hadley Wickham)——tidyverse生态权威指南
- Stata编程手册——ado文件编程和自动化
- 《Writing Good Code for Science》——科研代码质量规范

## 参考链接

- https://docs.python.org/3/ — Python官方文档
- https://lrberge.github.io/fixest/ — R fixest包文档（高效面板回归）
- https://github.com/sergiocorreia/reghdfe — Stata reghdfe命令文档
- https://cookiecutter-data-science.drivendata.org/ — 数据科学项目模板规范
- https://the-turing-way.netlify.app/ — Turing Way可复现研究指南
