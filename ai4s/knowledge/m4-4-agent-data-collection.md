# Agent数据采集

> **引入时机**：W6 | **核心挑战**："如何让Agent自动执行数据采集流程？" | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

当你封装好数据采集Skill后，单个采集任务可以高效执行。但社科研究的数据采集往往是多步骤的：先从API获取宏观指标，再从政府网站提取政策文本，然后用NLP解析文本中的关键信息，最后将所有数据整合为分析面板。这些步骤之间有依赖关系——前一步的输出决定后一步的输入，某些步骤可能失败需要重试，某些决策点需要人工确认。

手动执行这些步骤既低效又容易出错——你可能忘了某个省份的数据还没采，或者在API返回异常时做了不一致的处理。Agent的引入正是为了解决这类多步骤、有依赖、需决策的数据采集编排问题。

掌握Agent数据采集后，你能定义一套"采集工作流"让Agent按规则自动执行，在关键决策点请求人工确认，在异常时按预设策略处理。Agent不是取代你的判断，而是按你的规则高效执行可自动化的环节，让你专注于策略设计而非机械操作。

## 这个知识点的核心内容

### 数据采集Agent的设计

数据采集Agent的核心是一个状态机，驱动数据从"原始来源"到"分析就绪"的完整流程：

```
[任务规划] → [API调用] → [数据验证] → [缺失处理] → [存储归档]
                ↓              ↓
            [重试/切换]    [人工确认]
```

**Agent设计要素：**

```python
class DataCollectionAgent:
    def __init__(self, config, skills, llm_client):
        self.config = config
        self.skills = skills
        self.llm = llm_client
        self.state = "planning"
        self.collected_data = {}
        self.log = []

    def run(self, task_description):
        plan = self._plan_task(task_description)
        self.log.append({"phase": "planning", "plan": plan})

        for step in plan:
            result = self._execute_step(step)

            if result["status"] == "needs_confirmation":
                user_decision = self._request_human_confirmation(result)
                if not user_decision["approved"]:
                    self.log.append({
                        "phase": "human_rejection",
                        "step": step["name"],
                        "reason": user_decision.get("reason", "")
                    })
                    continue

            if result["status"] == "failed":
                retry_result = self._handle_failure(step, result)
                if retry_result["status"] == "failed":
                    self.log.append({
                        "phase": "final_failure",
                        "step": step["name"],
                        "error": result["error"]
                    })
                    continue

            self.collected_data[step["output_key"]] = result["data"]
            self.log.append({
                "phase": "step_complete",
                "step": step["name"],
                "records": len(result["data"]) if hasattr(result["data"], "__len__") else 1
            })

        return {
            "data": self.collected_data,
            "log": self.log,
            "summary": self._generate_summary()
        }
```

### Agent的自主决策与人工干预

Agent需要在"自主执行"和"人工干预"之间取得平衡。核心原则：可预见的、低风险的决策自动执行；不可预见的、高风险的决策请求人工确认。

**决策点分类：**

| 决策类型 | 示例 | 处理方式 |
|---------|------|---------|
| 常规自动 | API调用参数填充、数据格式转换 | Agent自动执行 |
| 异常处理 | API返回空数据、爬虫被封 | Agent尝试预设策略（重试/切换源），失败则请求人工 |
| 质量判断 | 数据代表性不足、缺失值过多 | Agent生成评估报告，请求人工确认是否继续 |
| 伦理边界 | 采集到个人敏感信息 | 立即暂停，请求人工决策 |

```python
def _execute_step(self, step):
    skill_name = step["skill"]
    params = step["params"]

    if skill_name in self.skills:
        skill = self.skills[skill_name]
        result = skill["execute"](**params)
    else:
        return {"status": "failed", "error": "Skill not found: {}".format(skill_name)}

    validation = self._validate_result(result, step.get("validation_rules", {}))

    if validation["quality_score"] < 0.5:
        return {
            "status": "needs_confirmation",
            "message": "数据质量评分: {:.2f}, 原因: {}".format(
                validation["quality_score"],
                validation["reasons"]
            ),
            "data": result
        }

    if result.get("success") is False:
        return {"status": "failed", "error": result.get("error", "Unknown error")}

    return {"status": "success", "data": result}

def _validate_result(self, result, rules):
    quality_score = 1.0
    reasons = []

    if rules.get("min_records"):
        count = result["metadata"].get("data_points_count", 0)
        if count < rules["min_records"]:
            quality_score -= 0.3
            reasons.append(
                "数据量不足: {} < {}".format(count, rules["min_records"])
            )

    if rules.get("max_missing_rate"):
        data = result.get("data")
        if hasattr(data, "isnull"):
            missing_rate = data.isnull().mean().mean()
            if missing_rate > rules["max_missing_rate"]:
                quality_score -= 0.3
                reasons.append(
                    "缺失率过高: {:.1%}".format(missing_rate)
                )

    if rules.get("required_time_coverage"):
        pass

    return {"quality_score": max(quality_score, 0), "reasons": reasons}
```

### 多步骤数据采集流程的编排

复杂的数据采集需要编排多个步骤，处理步骤间的依赖关系：

```python
def _plan_task(self, task_description):
    prompt = """你是一个社科数据采集Agent的任务规划器。
根据以下任务描述，生成数据采集步骤序列。

任务：{}

每步格式：
{{
    "step": 1,
    "name": "步骤名称",
    "skill": "skill名称",
    "params": {{}},
    "output_key": "数据存储键名",
    "validation_rules": {{
        "min_records": 最小记录数,
        "max_missing_rate": 最大缺失率
    }},
    "depends_on": [前序步骤编号列表]
}}

返回JSON数组。""".format(task_description)

    response = self.llm.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    import json
    try:
        plan = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        plan = [{"step": 1, "name": "manual_collection_required",
                 "skill": "none", "params": {},
                 "output_key": "raw_data", "depends_on": []}]
    return plan
```

**编排示例——数字经济研究数据采集：**

```python
DIGITAL_ECONOMY_COLLECTION_PLAN = [
    {
        "step": 1,
        "name": "获取宏观经济指标",
        "skill": "world_bank_data_collector",
        "params": {
            "indicator": "NY.GDP.MKTP.KD.ZG",
            "country": "CHN",
            "start_year": 2010,
            "end_year": 2023
        },
        "output_key": "macro_indicators",
        "validation_rules": {"min_records": 10},
        "depends_on": []
    },
    {
        "step": 2,
        "name": "提取数字经济政策文本",
        "skill": "gov_policy_extractor",
        "params": {
            "base_url": "http://www.gov.cn",
            "keywords": ["数字经济", "数字化转型"]
        },
        "output_key": "policy_texts",
        "validation_rules": {"min_records": 20},
        "depends_on": []
    },
    {
        "step": 3,
        "name": "结构化提取政策信息",
        "skill": "llm_structured_extractor",
        "params": {
            "texts_key": "policy_texts",
            "schema": "policy_metadata"
        },
        "output_key": "policy_structured",
        "validation_rules": {"min_records": 15},
        "depends_on": [2]
    },
    {
        "step": 4,
        "name": "整合分析面板",
        "skill": "data_merger",
        "params": {
            "sources": ["macro_indicators", "policy_structured"],
            "merge_keys": ["year", "province"]
        },
        "output_key": "analysis_panel",
        "validation_rules": {"min_records": 100},
        "depends_on": [1, 3]
    }
]
```

### Agent的数据质量控制

数据质量控制贯穿Agent采集的全流程：

```python
class DataQualityController:
    def __init__(self, rules):
        self.rules = rules

    def check(self, data, step_name):
        issues = []

        if hasattr(data, "shape"):
            rows, cols = data.shape
            if rows < self.rules.get("min_rows", 10):
                issues.append({
                    "level": "warning",
                    "message": "{}: 记录数{}低于阈值{}".format(
                        step_name, rows, self.rules["min_rows"]
                    )
                })

            missing_pct = data.isnull().mean().mean() * 100
            if missing_pct > self.rules.get("max_missing_pct", 20):
                issues.append({
                    "level": "error",
                    "message": "{}: 缺失率{:.1f}%超过阈值{:.1f}%".format(
                        step_name, missing_pct, self.rules["max_missing_pct"]
                    )
                })

            for col in self.rules.get("no_missing_cols", []):
                if col in data.columns and data[col].isnull().any():
                    issues.append({
                        "level": "error",
                        "message": "{}: 关键列{}存在缺失".format(step_name, col)
                    })

            dup_rate = data.duplicated().mean()
            if dup_rate > 0.05:
                issues.append({
                    "level": "warning",
                    "message": "{}: 重复率{:.1%}偏高".format(step_name, dup_rate)
                })

        return {
            "passed": not any(i["level"] == "error" for i in issues),
            "issues": issues
        }

    def generate_report(self, all_checks):
        report_lines = ["数据质量控制报告", "=" * 40]
        for step, check in all_checks.items():
            status = "PASS" if check["passed"] else "FAIL"
            report_lines.append("[{}] {}".format(status, step))
            for issue in check["issues"]:
                report_lines.append("  - [{}] {}".format(
                    issue["level"].upper(), issue["message"]
                ))
        return "\n".join(report_lines)
```

## 关键细节与易错点

- **易错：让Agent完全自主决策**。数据采集中的某些决策（如是否使用某个数据源、如何处理伦理敏感数据）必须由人判断。Agent应该在这些点暂停并请求确认，而非自行决定
- **易错：Agent流程缺乏日志**。没有详细日志的Agent是一个"黑箱"——当数据出现问题时，无法追溯是哪个步骤出了错。每个步骤都应记录输入参数、输出摘要、耗时、异常信息
- **易错：忽视采集时点差异**。不同步骤在不同时间采集的数据可能存在时点不一致——宏观指标是2024年版，微观调查是2022年版。Agent应标注每批数据的采集时点和数据年份，方便后续分析
- **易错：过度编排**。不是所有数据采集都需要Agent。如果只是从单个API获取数据，直接用Skill更简单可靠。Agent适合3个以上步骤、有依赖关系、需异常处理的场景
- **易错：Agent流程不可中断**。长时间运行的Agent流程应支持断点续传——如果中途失败，不应从头开始，而应从失败步骤继续

## 社科科研示例

**场景**：一位管理学博士生研究"ESG评级对企业融资成本的影响"，需要从多个数据源采集数据并整合为面板数据。

**Agent采集流程：**

```python
esg_agent = DataCollectionAgent(
    config={
        "project_name": "esg_financing_cost",
        "data_dir": "./data",
        "quality_rules": {
            "min_rows": 500,
            "max_missing_pct": 15,
            "no_missing_cols": ["firm_id", "year"]
        }
    },
    skills={
        "wind_api_collector": wind_skill,
        "esg_rating_collector": esg_skill,
        "annual_report_extractor": report_skill,
        "data_merger": merger_skill
    },
    llm_client=llm_client
)

result = esg_agent.run(
    "采集A股上市公司2018-2023年ESG评级、融资成本及控制变量数据，"
    "整合为面板数据。数据源：Wind金融终端(财务数据)、华证ESG评级(ESG数据)、"
    "巨潮资讯网(年报文本)。关键变量不能有缺失。"
)

if result["summary"]["all_steps_completed"]:
    panel_data = result["data"]["analysis_panel"]
    print("面板数据维度:", panel_data.shape)
    print("质量控制报告:")
    print(esg_agent.quality_controller.generate_report(
        esg_agent.quality_checks
    ))
else:
    print("采集未完成，检查日志:")
    for entry in result["log"]:
        if entry.get("phase") in ["final_failure", "human_rejection"]:
            print("  - {}: {}".format(entry["phase"], entry))
```

## 拓展学习

- LangChain Agent文档——Agent编排框架的原理与实践
- 《Designing Data-Intensive Applications》——数据系统设计方法论
- Apache Airflow——工业级工作流编排工具
- Prefect——Python原生的数据流编排框架
- 《The Art of Scalable Data Collection》——大规模数据采集的工程实践

## 参考链接

- https://docs.langchain.com/oss/python/langchain/agents/ — LangChain Agent使用指南
- https://airflow.apache.org/ — Apache Airflow工作流平台
- https://prefect.io/ — Prefect数据流编排
- https://www.selenium.dev/ — Selenium浏览器自动化（处理动态网页）
- https://scrapy.org/ — Scrapy爬虫框架
