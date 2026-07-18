# 定量分析方法AI赋能

> **引入时机**：W6 | **核心挑战**："回归、面板、时间序列——如何用AI辅助定量分析？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

W6进入分析实施阶段，你需要选择和执行定量分析方法。社科博士生的典型困境是：学过计量经济学，但面对真实数据时不知道选哪个模型；知道模型公式，但不确定前提假设是否满足；跑出了结果，但不清楚是否遗漏了关键检验步骤。这些问题不是"不会算"而是"不知道该算什么"——方法论选择和模型诊断的判断力，比计算能力更稀缺。

AI辅助定量分析的核心价值在于：帮你系统化地走完分析流程（而非遗漏关键步骤），帮你做模型选择和前提检验（而非凭感觉选模型），帮你解读和报告结果（而非只贴回归表）。但AI的角色是"帮你做对"，不是"替你做"——模型选择的方法论判断、前提违反的处理策略、结果的学术解释，这些核心决策必须由你做出。

本知识点的目标是让你建立"AI辅助但不替代"的定量分析工作流，确保每个分析方法的选择都有方法论依据，每个关键检验步骤都不遗漏。

## 这个知识点的核心内容

### AI辅助回归分析

回归分析是社科定量研究的基石，AI辅助的核心环节是模型选择、前提检验和结果解读：

**分析流程（AI应协助你走完每一步）：**

```
研究问题 → 变量选择 → 模型选择 → 前提检验 → 估计 → 诊断 → 解读
                ↑                            ↓
                └──── 前提违反则调整模型 ←────┘
```

**完整的AI辅助回归分析代码：**

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.stattools import durbin_watson
from scipy import stats

class RegressionAnalysis:
    def __init__(self, df, dep_var, core_var, controls=None):
        self.df = df.copy()
        self.dep_var = dep_var
        self.core_var = core_var
        self.controls = controls or []
        self.all_indep = [core_var] + self.controls
        self.diagnostics = {}

    def check_assumptions(self):
        y = self.df[self.dep_var]
        X = sm.add_constant(self.df[self.all_indep])
        model = sm.OLS(y, X).fit()
        residuals = model.resid

        self.diagnostics["multicollinearity"] = self._check_vif()
        self.diagnostics["heteroscedasticity"] = self._check_heteroscedasticity(
            y, X, residuals
        )
        self.diagnostics["normality"] = self._check_normality(residuals)
        self.diagnostics["autocorrelation"] = self._check_autocorrelation(residuals)

        return self.diagnostics

    def _check_vif(self):
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        X = sm.add_constant(self.df[self.all_indep])
        vif_data = {}
        for i, var in enumerate(self.all_indep):
            vif_data[var] = variance_inflation_factor(X.values, i + 1)
        return vif_data

    def _check_heteroscedasticity(self, y, X, residuals):
        bp_stat, bp_pval, _, _ = het_breuschpagan(residuals, X)
        white_stat, white_pval, _, _ = het_white(residuals, X)
        return {
            "breusch_pagan": {"statistic": bp_stat, "p_value": bp_pval},
            "white": {"statistic": white_stat, "p_value": white_pval},
            "heteroscedastic": bp_pval < 0.05
        }

    def _check_normality(self, residuals):
        stat, pval = stats.jarque_bera(residuals)
        return {"jarque_bera_stat": stat, "p_value": pval}

    def _check_autocorrelation(self, residuals):
        dw = durbin_watson(residuals)
        return {"durbin_watson": dw}

    def run_robust_regression(self, cluster_var=None):
        y = self.df[self.dep_var]
        X = sm.add_constant(self.df[self.all_indep])

        if cluster_var and cluster_var in self.df.columns:
            model = sm.OLS(y, X).fit(
                cov_type="cluster",
                cov_kwds={"groups": self.df[cluster_var]}
            )
        elif self.diagnostics.get("heteroscedasticity", {}).get("heteroscedastic"):
            model = sm.OLS(y, X).fit(cov_type="HC1")
        else:
            model = sm.OLS(y, X).fit()

        return model

    def generate_report(self, model):
        report = {
            "dep_var": self.dep_var,
            "core_var": self.core_var,
            "core_coef": float(model.params[self.core_var]),
            "core_se": float(model.bse[self.core_var]),
            "core_pval": float(model.pvalues[self.core_var]),
            "core_ci": model.conf_int().loc[self.core_var].tolist(),
            "r_squared": float(model.rsquared),
            "adj_r_squared": float(model.rsquared_adj),
            "n_obs": int(model.nobs),
            "controls": self.controls,
            "diagnostics": self.diagnostics
        }
        return report
```

### 面板数据分析

面板数据是社科研究中最常见的数据结构，核心决策是固定效应vs随机效应：

```python
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects

class PanelAnalysis:
    def __init__(self, df, dep_var, core_var, entity_var, time_var,
                 controls=None):
        self.df = df.set_index([entity_var, time_var])
        self.dep_var = dep_var
        self.core_var = core_var
        self.controls = controls or []
        self.all_indep = [core_var] + self.controls
        self.entity_var = entity_var
        self.time_var = time_var

    def hausman_test(self):
        y = self.df[self.dep_var]
        X = sm.add_constant(self.df[self.all_indep])

        fe_model = PanelOLS(y, X, entity_effects=True).fit()
        re_model = RandomEffects(y, X).fit()

        b_fe = fe_model.params[self.all_indep]
        b_re = re_model.params[self.all_indep]
        var_fe = fe_model.cov[self.all_indep].loc[self.all_indep]
        var_re = re_model.cov[self.all_indep].loc[self.all_indep]

        diff = b_fe - b_re
        var_diff = var_fe - var_re

        try:
            stat = float(diff.T @ np.linalg.inv(var_diff) @ diff)
            df = len(self.all_indep)
            pval = 1 - stats.chi2.cdf(stat, df)
        except np.linalg.LinAlgError:
            stat, pval = None, None

        recommendation = "fixed_effects" if pval and pval < 0.05 else "random_effects"

        return {
            "statistic": stat,
            "p_value": pval,
            "recommendation": recommendation,
            "interpretation": (
                "p<0.05拒绝原假设，个体效应与解释变量相关，应使用固定效应"
                if pval and pval < 0.05
                else "p>=0.05不能拒绝原假设，随机效应更有效率"
            )
        }

    def run_fixed_effects(self, time_effects=False, cluster=True):
        y = self.df[self.dep_var]
        X = sm.add_constant(self.df[self.all_indep])

        model = PanelOLS(
            y, X,
            entity_effects=True,
            time_effects=time_effects
        )

        if cluster:
            fit = model.fit(cov_type="clustered",
                           cluster_entity=True)
        else:
            fit = model.fit()

        return fit

    def run_random_effects(self):
        y = self.df[self.dep_var]
        X = sm.add_constant(self.df[self.all_indep])
        model = RandomEffects(y, X)
        return model.fit()
```

### 时间序列分析

时间序列分析的关键是区分平稳和非平稳过程，避免伪回归：

```python
from statsmodels.tsa.stattools import adfuller, kpss, coint
from statsmodels.tsa.api import VAR

class TimeSeriesAnalysis:
    def __init__(self, df, date_col):
        self.df = df.set_index(date_col)
        self.unit_root_results = {}

    def check_unit_root(self, var, test="adf", significance=0.05):
        series = self.df[var].dropna()

        if test == "adf":
            stat, pval, lags, nobs, critical, icbest = adfuller(
                series, autolag="AIC"
            )
            is_stationary = pval < significance
            test_name = "ADF"
        elif test == "kpss":
            stat, pval, lags, critical = kpss(
                series, regression="c", nlags="auto"
            )
            is_stationary = pval >= significance
            test_name = "KPSS"

        self.unit_root_results[var] = {
            "test": test_name,
            "statistic": stat,
            "p_value": pval,
            "is_stationary": is_stationary,
            "interpretation": (
                "{}检验: {}过程".format(
                    test_name,
                    "平稳" if is_stationary else "非平稳"
                )
            )
        }
        return self.unit_root_results[var]

    def check_cointegration(self, var1, var2):
        s1 = self.df[var1].dropna()
        s2 = self.df[var2].dropna()
        common_idx = s1.index.intersection(s2.index)
        s1, s2 = s1[common_idx], s2[common_idx]

        stat, pval, crit = coint(s1, s2)[:3]
        return {
            "statistic": stat,
            "p_value": pval,
            "critical_values": crit,
            "cointegrated": pval < 0.05,
            "interpretation": (
                "变量间存在协整关系（长期均衡关系）"
                if pval < 0.05
                else "变量间不存在协整关系"
            )
        }

    def run_var(self, variables, max_lags=4):
        data = self.df[variables].dropna()
        model = VAR(data)
        lag_order = model.select_order(maxlags=max_lags)
        selected_lag = lag_order.aic

        results = model.fit(selected_lag)
        irf = results.irf(periods=20)

        return {
            "model": results,
            "lag_order": selected_lag,
            "irf": irf,
            "granger_causality": self._granger_tests(results, variables)
        }

    def _granger_tests(self, var_result, variables):
        results = {}
        for caused in variables:
            for causing in variables:
                if caused != causing:
                    test = var_result.test_causality(caused, [causing])
                    results["{}->{}".format(causing, caused)] = {
                        "statistic": float(test.test_statistic),
                        "p_value": float(test.pvalue),
                        "granger_causes": test.pvalue < 0.05
                    }
        return results
```

### AI辅助统计建模的最佳实践

核心原则：**让AI帮写代码而非做判断。**

```python
def ai_assisted_modeling_workflow(research_context, llm_client):
    prompt = """基于以下研究上下文，生成Python分析代码框架。

研究问题：{question}
数据结构：{data_structure}
因变量：{dep_var}
核心自变量：{core_var}
控制变量：{controls}
研究设计：{design_type}

请生成代码，包含：
1. 前提检验（单位根/多重共线性/异方差等，根据数据类型选择）
2. 模型选择依据（固定效应vs随机效应需Hausman检验等）
3. 基准回归
4. 标准误选择说明
5. 关键统计量的导出

注意：
- 不要替研究者做模型选择判断，而是生成检验代码让结果说话
- 标准误选择应有依据（聚类、异方差稳健等）
- 每步都应有注释说明方法论原因
""".format(**research_context)

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
```

**实践清单：**

| 环节 | 让AI做 | 你自己做 |
|------|-------|---------|
| 代码编写 | 生成回归、检验、导出代码 | 审查代码逻辑是否正确 |
| 前提检验 | 运行检验并报告结果 | 判断前提是否满足、如何调整 |
| 模型选择 | 提供选择依据和检验工具 | 基于检验结果做最终选择 |
| 标准误 | 生成不同标准误的代码 | 选择合适的标准误类型 |
| 结果解读 | 辅助翻译统计指标 | 做出学科层面判断 |

## 关键细节与易错点

- **易错：让AI选择模型**。AI可能根据数据特征建议模型，但模型选择是方法论决策，必须由研究者做出。正确做法：让AI生成Hausman检验代码，你根据检验结果选择FE还是RE
- **易错：跳过前提检验**。AI生成的代码可能直接跳到回归，省略了多重共线性、异方差、自相关等前提检验。这些检验不是"可选"的，而是确保结果可信的必要步骤
- **易错：标准误选择随意**。面板数据默认用聚类标准误、异方差时用稳健标准误——这些不是"更严格"的选择，而是正确的选择。不正确的标准误导致p值不可信
- **易错：忽略固定效应的组内变换含义**。固定效应估计的是"组内变异"，你的核心自变量如果只有组间变异（如不随时间变化的制度变量），固定效应模型会将其完全吸收。AI可能不会提醒你这个关键问题
- **易错：时间序列不做单位根检验**。对非平稳序列做回归可能导致伪回归（spurious regression），即使t统计量很显著也没有意义。必须先做单位根检验

## 社科科研示例

**场景**：一位经济学博士生研究"财政分权对地方公共服务供给的影响"，使用省级面板数据（31省份×2010-2023年）。

```python
analysis = PanelAnalysis(
    df=panel_df,
    dep_var="public_service_index",
    core_var="fiscal_decentralization",
    entity_var="province",
    time_var="year",
    controls=["gdp_per_capita", "population_density", "urbanization_rate",
              "transfer_payment_ratio"]
)

assumptions = analysis.check_assumptions()
hausman = analysis.hausman_test()

print("Hausman检验: chi2={}, p={}".format(
    hausman["statistic"], hausman["p_value"]
))
print("建议: {}".format(hausman["recommendation"]))

if hausman["recommendation"] == "fixed_effects":
    model = analysis.run_fixed_effects(time_effects=True, cluster=True)
    print("固定效应+时间效应+聚类标准误")
else:
    model = analysis.run_random_effects()
    print("随机效应")

report = analysis.generate_report(model)
print("核心系数: {:.4f} (se={:.4f}, p={:.4f})".format(
    report["core_coef"], report["core_se"], report["core_pval"]
))
```

**关键决策记录：** Hausman检验p<0.05→选择固定效应；加入时间效应控制宏观经济周期；聚类标准误按省份聚类以处理组内自相关；财政分权指数使用收入端和支出端两个指标分别回归以检验稳健性。

## 拓展学习

- 《Introductory Econometrics: A Modern Approach》(Wooldridge)——计量经济学经典教材
- 《Mostly Harmless Econometrics》(Angrist & Pischke)——因果推断方法的实用指南
- 《Econometric Analysis of Cross Section and Panel Data》(Wooldridge)——面板数据方法权威参考
- linearmodels文档——Python面板数据估计库
- fixest文档——R语言高效面板回归包

## 参考链接

- https://www.statsmodels.org/ — statsmodels官方文档
- https://bashtage.github.io/linearmodels/ — linearmodels面板数据文档
- https://cran.r-project.org/package=fixest — R fixest包
- https://mixtape.scunning.com/ — Causal Inference: The Mixtape
- https://www.nber.org/resources — NBER工作论文（方法论参考）
