# Agent编排分析流程

> **引入时机**：W7 | **核心挑战**："如何用Agent编排多步骤分析流程？" | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

当你封装好分析Skill后，单个分析步骤可以高效执行。但社科数据分析的典型场景是：基准回归→异质性分析→机制检验→稳健性检验→结果可视化→报告生成。这些步骤之间有严格的逻辑依赖——机制检验依赖于基准回归的发现方向，稳健性检验需要根据基准模型设定替代方案。手动编排这些步骤不仅耗时，更容易遗漏关键环节。

更严重的问题是，很多同学的分析流程是"线性"的——跑完基准回归发现不显著就换模型，跑完异质性发现结果不一致就放弃——这违背了"先设计后执行"的分析原则。Agent编排的核心价值在于：让你事先定义完整分析流程，按计划执行，避免"p-hacking"式的选择性报告。

Agent编排不是让AI替你做分析决策，而是让你把分析计划固化为可执行的流程，在关键决策节点由人工确认。这确保了分析的完整性和透明性——你知道自己做了什么，审稿人也能看到完整的分析路径。

## 这个知识点的核心内容

### 分析Agent的工作流编排

分析Agent的核心是一个有状态的工作流引擎，驱动数据从"原始"到"分析报告"的完整流程：

```
数据加载 → 预处理 → 描述统计 → 基准回归 → 诊断检验 → 异质性分析 → 机制检验 → 稳健性检验 → 结果整合 → 报告生成
              ↓          ↓          ↓           ↓
          [人工确认]  [人工确认]  [人工确认]   [人工确认]
```

```python
import pandas as pd
from enum import Enum

class AnalysisState(Enum):
    LOADING = "loading"
    PREPROCESSING = "preprocessing"
    DESCRIPTIVE = "descriptive"
    BASELINE = "baseline"
    DIAGNOSTICS = "diagnostics"
    HETEROGENEITY = "heterogeneity"
    MECHANISM = "mechanism"
    ROBUSTNESS = "robustness"
    SYNTHESIS = "synthesis"
    REPORTING = "reporting"
    COMPLETE = "complete"

class AnalysisAgent:
    def __init__(self, skills, llm_client, config):
        self.skills = skills
        self.llm = llm_client
        self.config = config
        self.state = AnalysisState.LOADING
        self.results = {}
        self.decisions = []
        self.data = None

    def run(self):
        workflow = [
            (AnalysisState.LOADING, self._load_data),
            (AnalysisState.PREPROCESSING, self._preprocess),
            (AnalysisState.DESCRIPTIVE, self._descriptive_stats),
            (AnalysisState.BASELINE, self._baseline_regression),
            (AnalysisState.DIAGNOSTICS, self._diagnostic_checks),
            (AnalysisState.HETEROGENEITY, self._heterogeneity_analysis),
            (AnalysisState.MECHANISM, self._mechanism_analysis),
            (AnalysisState.ROBUSTNESS, self._robustness_checks),
            (AnalysisState.SYNTHESIS, self._synthesize_results),
            (AnalysisState.REPORTING, self._generate_report),
        ]

        for state, action in workflow:
            self.state = state
            result = action()

            if result.get("needs_confirmation"):
                decision = self._request_confirmation(result)
                self.decisions.append({
                    "state": state.value,
                    "question": result["question"],
                    "decision": decision
                })
                if not decision.get("approved", True):
                    self.results[state.value] = {
                        "status": "skipped",
                        "reason": decision.get("reason", "User skipped")
                    }
                    continue

            self.results[state.value] = result

        self.state = AnalysisState.COMPLETE
        return self._compile_results()

    def _load_data(self):
        data_config = self.config["data"]
        if data_config["format"] == "stata":
            self.data = pd.read_stata(data_config["path"])
        elif data_config["format"] == "csv":
            self.data = pd.read_csv(data_config["path"])

        return {
            "status": "success",
            "rows": len(self.data),
            "columns": list(self.data.columns),
            "missing_overview": self.data.isnull().mean().to_dict()
        }

    def _preprocess(self):
        preprocess_config = self.config.get("preprocessing", {})
        if preprocess_config.get("drop_missing_vars"):
            self.data = self.data.dropna(
                subset=preprocess_config["drop_missing_vars"]
            )
        if preprocess_config.get("winsorize_vars"):
            for var, limits in preprocess_config["winsorize_vars"].items():
                lower, upper = limits
                self.data[var] = self.data[var].clip(
                    lower=self.data[var].quantile(lower),
                    upper=self.data[var].quantile(upper)
                )
        if preprocess_config.get("log_transform"):
            for var in preprocess_config["log_transform"]:
                self.data["log_{}".format(var)] = np.log1p(self.data[var])

        return {
            "status": "success",
            "rows_after": len(self.data),
            "transformations": list(preprocess_config.keys())
        }

    def _baseline_regression(self):
        baseline_config = self.config["baseline"]
        skill = self.skills["panel_regression"]
        result = skill.execute(
            data_path=self.config["data"]["path"],
            dep_var=baseline_config["dep_var"],
            core_var=baseline_config["core_var"],
            controls=baseline_config.get("controls", []),
            entity_var=baseline_config.get("entity_var", "id"),
            time_var=baseline_config.get("time_var", "year"),
            fe_type=baseline_config.get("fe_type", "entity"),
            cluster_var=baseline_config.get("cluster_var", "id")
        )

        core_coef = result["model"].params[baseline_config["core_var"]]
        core_pval = result["model"].pvalues[baseline_config["core_var"]]

        return {
            "status": "success",
            "core_coef": float(core_coef),
            "core_pval": float(core_pval),
            "model": result["model"],
            "report": result["report"],
            "diagnostics": result["diagnostics"],
            "needs_confirmation": core_pval > 0.1,
            "question": (
                "基准回归核心变量p值={:.3f}，不显著。"
                "是否继续后续分析？".format(core_pval)
            )
        }

    def _diagnostic_checks(self):
        baseline_result = self.results.get("baseline", {})
        if baseline_result.get("status") != "success":
            return {"status": "skipped", "reason": "No baseline model"}

        diagnostics = baseline_result.get("diagnostics", {})
        issues = []

        if diagnostics.get("high_vif"):
            issues.append(
                "多重共线性: {}".format(diagnostics["high_vif"])
            )

        return {
            "status": "success",
            "diagnostics": diagnostics,
            "issues": issues
        }

    def _heterogeneity_analysis(self):
        het_config = self.config.get("heterogeneity", [])
        if not het_config:
            return {"status": "skipped", "reason": "No heterogeneity config"}

        results = []
        for group_var in het_config:
            skill = self.skills["panel_regression"]
            for group_val in self.data[group_var].unique():
                subset = self.data[self.data[group_var] == group_val]
                temp_path = "./temp_subset_{}_{}.dta".format(
                    group_var, group_val
                )
                subset.to_stata(temp_path, write_index=False)

                result = skill.execute(
                    data_path=temp_path,
                    **self.config["baseline"]
                )
                results.append({
                    "group_var": group_var,
                    "group_val": group_val,
                    "coef": float(result["model"].params[
                        self.config["baseline"]["core_var"]
                    ]),
                    "pval": float(result["model"].pvalues[
                        self.config["baseline"]["core_var"]
                    ])
                })

        return {"status": "success", "results": results}

    def _mechanism_analysis(self):
        mech_config = self.config.get("mechanism", {})
        if not mech_config:
            return {"status": "skipped", "reason": "No mechanism config"}

        results = {}
        for mediator in mech_config.get("mediators", []):
            skill = self.skills["panel_regression"]
            result = skill.execute(
                data_path=self.config["data"]["path"],
                dep_var=mediator,
                core_var=self.config["baseline"]["core_var"],
                controls=self.config["baseline"].get("controls", []),
                entity_var=self.config["baseline"].get("entity_var", "id"),
                time_var=self.config["baseline"].get("time_var", "year"),
                fe_type=self.config["baseline"].get("fe_type", "entity"),
                cluster_var=self.config["baseline"].get("cluster_var", "id")
            )
            results[mediator] = {
                "coef": float(result["model"].params[
                    self.config["baseline"]["core_var"]
                ]),
                "pval": float(result["model"].pvalues[
                    self.config["baseline"]["core_var"]
                ])
            }

        return {"status": "success", "mediator_results": results}

    def _robustness_checks(self):
        robust_config = self.config.get("robustness", {})
        if not robust_config:
            return {"status": "skipped", "reason": "No robustness config"}

        results = {}

        if "alt_dep_vars" in robust_config:
            alt_results = []
            for alt_var in robust_config["alt_dep_vars"]:
                skill = self.skills["panel_regression"]
                result = skill.execute(
                    data_path=self.config["data"]["path"],
                    dep_var=alt_var,
                    **{k: v for k, v in self.config["baseline"].items()
                       if k != "dep_var"}
                )
                alt_results.append({
                    "dep_var": alt_var,
                    "coef": float(result["model"].params[
                        self.config["baseline"]["core_var"]
                    ]),
                    "pval": float(result["model"].pvalues[
                        self.config["baseline"]["core_var"]
                    ])
                })
            results["alt_dep_vars"] = alt_results

        if "alt_cluster" in robust_config:
            results["alt_cluster"] = self._run_alt_cluster(
                robust_config["alt_cluster"]
            )

        return {"status": "success", "results": results}

    def _synthesize_results(self):
        baseline = self.results.get("baseline", {})
        heterogeneity = self.results.get("heterogeneity", {})
        mechanism = self.results.get("mechanism", {})
        robustness = self.results.get("robustness", {})

        synthesis = {
            "baseline_significant": baseline.get("core_pval", 1) < 0.05,
            "baseline_direction": "positive" if baseline.get("core_coef", 0) > 0 else "negative",
            "heterogeneity_consistent": self._check_heterogeneity_consistency(heterogeneity),
            "mechanism_supported": self._check_mechanism_support(mechanism),
            "robustness_passed": self._check_robustness(robustness)
        }

        return {"status": "success", "synthesis": synthesis}

    def _generate_report(self):
        prompt = """基于以下分析结果，生成结构化分析报告摘要。

分析结果：{}

请包含：
1. 基准回归发现
2. 异质性分析结论
3. 机制检验结论
4. 稳健性检验结论
5. 总体评估与局限

注意使用审慎措辞，区分统计显著性和实际显著性。""".format(
            self.results
        )

        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return {
            "status": "success",
            "report": response.choices[0].message.content
        }
```

### Agent的决策节点设计

决策节点是Agent工作流中"自动"与"人工"的分界线。设计原则：**统计学上可以自动判断的让Agent做，方法论上需要人类判断的请求人工确认。**

```python
DECISION_RULES = {
    "baseline_not_significant": {
        "trigger": lambda r: r.get("core_pval", 0) > 0.1,
        "auto_action": None,
        "human_question": "基准回归不显著，是否继续后续分析？",
        "options": ["continue_anyway", "revise_model", "stop"]
    },
    "high_multicollinearity": {
        "trigger": lambda r: any(v > 10 for v in r.get("vif", {}).values()),
        "auto_action": "warn",
        "human_question": "存在高VIF变量，是否需要处理？",
        "options": ["drop_variable", "combine_variables", "ignore"]
    },
    "data_quality_warning": {
        "trigger": lambda r: r.get("missing_rate", 0) > 0.2,
        "auto_action": "log_warning",
        "human_question": "缺失率超过20%，如何处理？",
        "options": ["impute", "drop_missing", "use_available"]
    }
}
```

### 多步骤分析的容错与重试

```python
class RobustWorkflowExecutor:
    def __init__(self, max_retries=2):
        self.max_retries = max_retries
        self.execution_log = []

    def execute_step(self, step_func, step_name, **kwargs):
        for attempt in range(self.max_retries + 1):
            try:
                result = step_func(**kwargs)
                self.execution_log.append({
                    "step": step_name,
                    "attempt": attempt + 1,
                    "status": "success"
                })
                return result
            except Exception as e:
                self.execution_log.append({
                    "step": step_name,
                    "attempt": attempt + 1,
                    "status": "failed",
                    "error": str(e)
                })
                if attempt == self.max_retries:
                    return {
                        "status": "failed",
                        "error": str(e),
                        "fallback": True
                    }
                continue

    def execute_with_fallback(self, primary, fallback, step_name, **kwargs):
        primary_result = self.execute_step(primary, step_name, **kwargs)
        if primary_result.get("status") == "failed":
            return self.execute_step(fallback, step_name + "_fallback", **kwargs)
        return primary_result
```

### Agent输出的人审机制

Agent生成的所有分析结果必须经过人工审查。审查机制不应是"全部重看"，而是聚焦关键决策点和异常结果：

```python
def generate_review_checklist(results):
    checklist = []

    baseline = results.get("baseline", {})
    if baseline.get("status") == "success":
        checklist.append({
            "item": "基准回归模型设定",
            "check_points": [
                "固定效应类型是否正确",
                "聚类标准误是否合理",
                "控制变量是否完整"
            ],
            "priority": "high"
        })

    diagnostics = results.get("diagnostics", {})
    if diagnostics.get("issues"):
        checklist.append({
            "item": "诊断检验异常",
            "check_points": diagnostics["issues"],
            "priority": "high"
        })

    robustness = results.get("robustness", {})
    if robustness.get("status") == "success":
        checklist.append({
            "item": "稳健性检验一致性",
            "check_points": [
                "替代因变量结果是否方向一致",
                "替代标准误结果是否一致"
            ],
            "priority": "medium"
        })

    return checklist
```

## 关键细节与易错点

- **易错：Agent流程缺乏灵活性**。硬编码的分析流程无法应对意外发现——比如基准回归不显著时，应该继续还是修改？正确做法：在关键决策点设人工确认，允许研究者灵活调整
- **易错：Agent做了方法论判断**。Agent不应该自主决定"换模型""加变量"——这些是方法论决策，必须由人做出。Agent应该报告事实（如"p值不显著"），由人决定下一步
- **易错：忽视分析顺序的因果逻辑**。机制检验必须在基准回归之后，稳健性检验应在机制检验之后。不合理的顺序（如先做稳健性再做基准）会导致方法论问题
- **易错：Agent报告缺乏可追溯性**。每个分析结果都应标注"由哪个Skill在什么参数下产出"，否则无法追溯结果的来源和可靠性
- **易错：人工审查流于形式**。如果审查只是"点确认"而非"审视方法论合理性"，Agent编排就失去了质量保障意义。审查清单应聚焦方法论决策而非代码细节

## 社科科研示例

**场景**：一位经济学博士生研究"最低工资上调对就业的影响"，使用DID设计，需要完整分析流程。

```python
config = {
    "data": {
        "path": "./data/min_wage_panel.dta",
        "format": "stata"
    },
    "baseline": {
        "dep_var": "employment_rate",
        "core_var": "min_wage_increase",
        "controls": ["gdp_growth", "industry_mix", "population_density"],
        "entity_var": "city",
        "time_var": "year",
        "fe_type": "twoway",
        "cluster_var": "city"
    },
    "heterogeneity": ["industry_type", "firm_size_group"],
    "mechanism": {
        "mediators": ["firm_exit_rate", "automation_investment"]
    },
    "robustness": {
        "alt_dep_vars": ["youth_employment", "low_skill_employment"],
        "alt_cluster": "province",
        "placebo_test": True
    }
}

agent = AnalysisAgent(
    skills=skill_registry,
    llm_client=llm,
    config=config
)

results = agent.run()

review = generate_review_checklist(results.results)
for item in review:
    print("[{}] {}".format(item["priority"], item["item"]))
    for cp in item["check_points"]:
        print("  - {}".format(cp))
```

## 拓展学习

- Prefect/Airflow——工作流编排框架的设计理念
- 《Workflow Patterns》——工作流模式的系统分类
- LangChain——Agent编排的实践参考
- 《The Pragmatic Programmer》——自动化流程设计的工程思维
- DAG（有向无环图）——分析步骤依赖关系的建模方法

## 参考链接

- https://docs.prefect.io/ — Prefect工作流编排
- https://airflow.apache.org/ — Apache Airflow
- https://www.langchain.com/ — LangChain Agent框架
- https://docs.prefect.io/ — 工作流状态管理
- https://www.researchgate.net/ — 科研工作流与协作资源
