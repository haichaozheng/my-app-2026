# 大模型类人智能体数据采集（硅基样本）

> **引入时机**：W6 | **核心挑战**："如何用 persona-prompted LLM 作为问卷/实验被试生成数据，并论证其有效性？" | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

社科研究的经验数据，传统上靠**问卷调研**和**行为实验**获取——设计问卷、招募被试、伦理审批、发放回收、清洗编码。这条路成本高、周期长、样本小，伦理审查往往拖到研究设计稳定之后才能开展。当你处于研究设计阶段，想快速**预测试**问卷题项是否清晰、实验情境是否有效，或想在正式采样前**探索性**地看看变量关系的大致方向，传统流程往往跟不上节奏。

大模型带来一种新型**生成式数据源**：给 LLM 注入一个"人物画像"（persona），让它以该角色的身份回答问卷题项或参与实验情境，从而批量生成"合成应答数据"。这类数据被称为**硅基样本（silicon sample）**或 **LLM-as-subject / LLM-as-respondent** 数据。

掌握这个知识点后，你能：

- 在问卷正式投放前用硅基样本做**预测试**，发现题项歧义、天花板/地板效应
- 在因果探索阶段用硅基样本跑**联合分析（conjoint）/ vignette 实验**，快速检验假设方向
- 在已有小样本真人数据时，用硅基样本做**稳健性补充**，检验结论是否在更广 persona 分布下成立
- 清楚地说明硅基样本的**适用边界**——它不能替代具有外部代表性的真人样本做最终因果推断，但在设计的特定环节有明确价值

需要在一开始就强调：硅基样本是一种**数据源选项**，不是万灵药。它的有效性取决于 persona 设计质量、与真人样本的校准程度，以及你对偏误的自觉。用错了比不用更危险——它会给缺乏代表性的数据披上"大样本"的外衣。

## 这个知识点的核心内容

### 一、硅基样本是什么、不是什么

**是**：用 persona prompt 驱动 LLM 模拟特定人群的应答，**生成**结构化问卷/实验数据。本质是"用 LLM 的语言能力与角色扮演能力，在给定人物画像约束下，产出近似该人群作答模式的合成数据"。

**不是**：

- 不是"让 AI 帮你写问卷"（那是题项生成，产出是问卷，不是数据）
- 不是"用 Agent 编排数据采集流水线"（那是 `m4-4` 的内容，自动化的是获取真实数据的流程）
- 不是真人样本的等价替代——它没有真实人的异质性来源（生命经验、社会网络、即时情境），只有 prompt 注入的画像约束

**两种典型用法**：

| 用法 | 产出 | 在研究中的定位 |
|---|---|---|
| 问卷硅基预测试 | 合成应答数据 | 设计阶段验证题项质量、发现歧义 |
| 实验硅基模拟 | 实验条件下的应答 | 探索阶段检验假设方向、稳健性补充 |

### 二、Persona 设计：硅基样本有效性的根基

硅基样本的质量，90% 取决于 persona 设计。一个 persona 是对"被试是谁"的结构化描述，LLM 在其约束下作答。

**Persona 的关键维度**：

```python
PERSONA_SCHEMA = {
    "demographics": {                  # 人口统计
        "age": None,                   # 影响代际经验、风险偏好
        "gender": None,
        "education": None,
        "income_level": None,
        "region": None,                # 影响制度环境、文化语境
        "occupation": None
    },
    "role_context": {                  # 角色情境
        "identity": None,              # 如"中小企业主"/"基层公务员"
        "decision_stance": None,       # 该角色在研究问题中的典型立场
        "knowledge_level": None        # 对议题的熟悉程度，影响作答确定性
    },
    "psychographics": {                # 心理特征（影响量表应答）
        "risk_attitude": None,         # 风险偏好
        "time_horizon": None,          # 时间视野（短期/长期）
        "value_orientation": None      # 价值取向（个体/集体等）
    }
}
```

**Persona 生成示例**：

```python
import json, random

def generate_personas(population_spec, n=200, seed=None):
    """按目标人群规格生成 persona 池。

    population_spec: 描述目标人群的分布，用于抽样
    n: persona 数量
    """
    rng = random.Random(seed)
    personas = []

    for i in range(n):
        persona = {
            "persona_id": "P{:04d}".format(i),
            "demographics": {
                "age": rng.choices(
                    population_spec["age_bins"],
                    weights=population_spec["age_weights"]
                )[0],
                "gender": rng.choices(
                    ["male", "female"],
                    weights=population_spec.get("gender_ratio", [0.5, 0.5])
                )[0],
                "education": rng.choices(
                    population_spec["education_levels"],
                    weights=population_spec["education_weights"]
                )[0],
                "income_level": rng.choices(
                    population_spec["income_bins"],
                    weights=population_spec["income_weights"]
                )[0],
                "region": rng.choices(
                    population_spec["regions"],
                    weights=population_spec["region_weights"]
                )[0],
                "occupation": rng.choices(
                    population_spec["occupations"],
                    weights=population_spec["occupation_weights"]
                )[0]
            },
            "psychographics": {
                "risk_attitude": rng.choices(
                    ["risk_averse", "neutral", "risk_seeking"],
                    weights=[0.5, 0.3, 0.2]
                )[0],
                "value_orientation": rng.choices(
                    ["individualist", "collectivist", "mixed"],
                    weights=[0.4, 0.4, 0.2]
                )[0]
            }
        }
        personas.append(persona)

    return personas


# 目标人群：某市中小企业主
sme_owner_spec = {
    "age_bins": [28, 35, 42, 50, 58],
    "age_weights": [0.15, 0.30, 0.30, 0.15, 0.10],
    "education_levels": ["high_school", "bachelor", "master"],
    "education_weights": [0.3, 0.55, 0.15],
    "income_bins": ["low_mid", "mid", "high_mid", "high"],
    "income_weights": [0.2, 0.4, 0.3, 0.1],
    "regions": ["east_coast", "central", "western"],
    "region_weights": [0.6, 0.25, 0.15],
    "occupations": ["manufacturing_owner", "service_owner",
                    "tech_startup_founder", "retail_owner"],
    "occupation_weights": [0.3, 0.3, 0.2, 0.2]
}

personas = generate_personas(sme_owner_spec, n=200, seed=42)
print("生成 persona 数:", len(personas))
print("示例:", json.dumps(personas[0], ensure_ascii=False, indent=2))
```

**关键设计原则**：

- **分布对齐**：persona 池的人口统计分布应基于真实统计资料（普查、行业报告），而非随手编。这是有效性的第一道防线。
- **异质性注入**：除人口统计外，加入心理特征维度，避免同画像 persona 应答过度同质。
- **数量考量**：硅基样本"大样本"不等于高代表性——persona 池的设计质量比数量重要。200-500 个 persona 通常足以做预测试和探索性分析。
- **seed 固定**：用随机种子固定 persona 池，保证可复现。

### 三、问卷硅基预测试：可跑示例

**场景**：研究"中小企业主对数字化转型补贴政策的采纳意愿"，设计了一份 Likert 量表问卷，想在正式投放前预测试题项质量。

**步骤 1：构造 persona 作答 prompt**

```python
def build_respondent_prompt(persona, questionnaire, llm_client):
    """让单个 persona 作答问卷。"""
    persona_desc = (
        "你是一名{age}岁的{gender}，学历{education}，"
        "从事{occupation}，所在地区{region}，收入水平{income_level}。"
        "你的风险态度偏{risk}，价值取向偏{value}。"
        "请以这个身份如实回答以下问卷。"
    ).format(
        age=persona["demographics"]["age"],
        gender=persona["demographics"]["gender"],
        education=persona["demographics"]["education"],
        occupation=persona["demographics"]["occupation"],
        region=persona["demographics"]["region"],
        income_level=persona["demographics"]["income_level"],
        risk=persona["psychographics"]["risk_attitude"],
        value=persona["psychographics"]["value_orientation"]
    )

    items_text = "\n".join(
        "{}. {}".format(i + 1, item) for i, item in enumerate(questionnaire["items"])
    )

    instruction = (
        persona_desc + "\n\n"
        "问卷采用5点量表（1=非常不同意，5=非常同意）。\n"
        "请对每题给出1-5的整数评分，并简述你的考虑（不超过30字）。\n"
        "严格以JSON格式返回，字段：responses（数组，每项含item_id与score），"
        "rationale（数组，每项对应一句考虑）。\n\n"
        "问卷题项：\n{items}\n\n"
        "返回JSON："
    ).format(items=items_text)

    response = llm_client.chat.completions.create(
        model="glm-4.6",
        messages=[{"role": "user", "content": instruction}],
        temperature=0.7   # 略高温度增加应答多样性，模拟个体差异
    )
    return response.choices[0].message.content
```

**步骤 2：批量执行并结构化**

```python
import json, time

def run_silicon_survey(personas, questionnaire, llm_client, sleep=0.5):
    """对 persona 池批量跑问卷，返回结构化数据。"""
    records = []
    for p in personas:
        raw = build_respondent_prompt(p, questionnaire, llm_client)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"responses": [], "rationale": [], "parse_error": raw[:200]}

        for r in parsed.get("responses", []):
            records.append({
                "persona_id": p["persona_id"],
                "age": p["demographics"]["age"],
                "gender": p["demographics"]["gender"],
                "education": p["demographics"]["education"],
                "occupation": p["demographics"]["occupation"],
                "region": p["demographics"]["region"],
                "risk_attitude": p["psychographics"]["risk_attitude"],
                "item_id": r["item_id"],
                "score": r["score"]
            })
        time.sleep(sleep)   # 尊重 API 速率限制

    import pandas as pd
    return pd.DataFrame(records)


questionnaire = {
    "items": [
        "Q1: 如果政府提供数字化转型补贴，我愿意主动申请。",
        "Q2: 我认为数字化转型能显著提升我企业的经营效率。",
        "Q3: 担心转型过程中的数据安全风险让我犹豫是否采纳。",
        "Q4: 我所在行业的同行大多已在推进数字化转型。",
        "Q5: 缺乏懂技术的内部人才是我采纳数字技术的主要障碍。"
    ]
}

# 假设 llm_client 已配置好
# df = run_silicon_survey(personas[:50], questionnaire, llm_client)
# df.to_csv("silicon_survey_pilot.csv", index=False)
```

**步骤 3：预测试分析——发现题项问题**

```python
def pilot_analysis(df):
    """硅基预测试的题项诊断。"""
    import pandas as pd

    summary = df.groupby("item_id")["score"].agg(
        ["mean", "std", "min", "max", "count"]
    )
    summary["floor_pct"] = df.groupby("item_id")["score"].apply(
        lambda s: (s == 1).mean() * 100
    )
    summary["ceiling_pct"] = df.groupby("item_id")["score"].apply(
        lambda s: (s == 5).mean() * 100
    )

    flags = []
    for item, row in summary.iterrows():
        if row["std"] < 0.5:
            flags.append("{}: 应答变异过低（std={:.2f}），可能题项无区分度".format(
                item, row["std"]))
        if row["ceiling_pct"] > 60:
            flags.append("{}: 天花板效应（{:,.0f}%选5），题项可能过于宽泛".format(
                item, row["ceiling_pct"]))
        if row["floor_pct"] > 60:
            flags.append("{}: 地板效应（{:.0f}%选1），题项可能不被该人群认可".format(
                item, row["floor_pct"]))

    return {"summary": summary, "flags": flags}

# analysis = pilot_analysis(df)
# print(analysis["summary"])
# for f in analysis["flags"]:
#     print("⚠️", f)
```

预测试的价值：在正式投放前发现"Q2 可能天花板""Q5 在高教育 persona 中无区分度"等问题，据此修订题项，省钱省时。

### 四、实验硅基模拟：Vignette / 联合分析

**场景**：想检验假设"补贴力度 × 转型风险感知 → 采纳意愿"的交互方向，先用硅基样本做探索。

```python
def vignette_experiment(persona, conditions, llm_client):
    """对单个 persona 跑 vignette 实验。

    conditions: 实验情境列表，每个含 treatment 描述
    """
    results = []
    for cond in conditions:
        prompt = (
            "你是{desc}。请阅读以下情境并作答。\n\n"
            "情境：{scenario}\n\n"
            "你在接下来6个月内采纳该政策的意愿（1-7分）？"
            "返回JSON：{{\"willingness\": 分数, \"reason\": \"简述\"}}".format(
                desc=format_persona(persona),
                scenario=cond["text"]
            )
        )
        resp = llm_client.chat.completions.create(
            model="glm-4.6",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        try:
            data = json.loads(resp.choices[0].message.content)
        except json.JSONDecodeError:
            data = {"willingness": None, "reason": "parse_error"}
        data["condition"] = cond["name"]
        data["persona_id"] = persona["persona_id"]
        results.append(data)
    return results


conditions = [
    {"name": "high_subsidy_low_risk",
     "text": "政府提供覆盖转型成本60%的补贴；数据安全由第三方可信机构托管。"},
    {"name": "high_subsidy_high_risk",
     "text": "政府提供覆盖转型成本60%的补贴；但企业需自行承担数据泄露的全部责任。"},
    {"name": "low_subsidy_low_risk",
     "text": "政府提供覆盖转型成本15%的补贴；数据安全由第三方可信机构托管。"},
    {"name": "low_subsidy_high_risk",
     "text": "政府提供覆盖转型成本15%的补贴；但企业需自行承担数据泄露的全部全部责任。"}
]
```

跑完后用方差分析看主效应与交互方向，作为正式实验设计的参考。

### 五、有效性校准：硅基样本的方法论核心

这是硅基样本**最关键也最易被忽视**的部分。用硅基样本做研究，必须回答："我凭什么相信 LLM 模拟的应答能代表真实人群？"

**三层校准逻辑**：

1. **分布校准**：硅基应答的边际分布（如各题均值、方差）是否在真人预测试的合理区间内？显著偏离则 persona 设计有偏。
2. **关系校准**：硅基数据中的变量间关系方向（如相关系数符号）是否与已有实证文献一致？方向反了说明 LLM 的"常识"与该人群的真实机制不符。
3. **边界校准**：明确声明硅基数据用于什么、不用于什么。例如："本硅基数据仅用于问卷预测试题项诊断，不作为最终假设检验的数据基础。"

```python
def calibrate_against_human(silicon_df, human_benchmark, tolerance=0.3):
    """用小样本真人数据校准硅基应答分布。

    silicon_df: 硅基应答数据
    human_benchmark: 小样本真人预测试数据（即使n=30也有价值）
    tolerance: 允许的均值偏差
    """
    silicon_means = silicon_df.groupby("item_id")["score"].mean()
    human_means = human_benchmark.groupby("item_id")["score"].mean()

    calibration = []
    for item in human_means.index:
        s_mean = silicon_means.get(item)
        h_mean = human_means[item]
        if s_mean is None:
            continue
        diff = abs(s_mean - h_mean)
        calibration.append({
            "item_id": item,
            "silicon_mean": round(s_mean, 2),
            "human_mean": round(h_mean, 2),
            "diff": round(diff, 2),
            "within_tolerance": diff <= tolerance,
            "direction_consistent": (s_mean - 3) * (h_mean - 3) > 0  # 同向偏离中性
        })

    n_consistent = sum(c["direction_consistent"] for c in calibration)
    return {
        "item_level": calibration,
        "direction_agreement_rate": n_consistent / len(calibration) if calibration else 0,
        "verdict": "pass" if n_consistent / max(len(calibration), 1) >= 0.8 else "review_persona_design"
    }
```

### 六、数据获取的工程要点

- **批量调用**：用 persona 池循环调用 LLM API，注意速率限制与重试；可封装为 Skill（见 `m4-3`）。
- **结构化输出**：强制 JSON 输出，解析失败要记录原始响应用于排查。
- **可复现**：固定 persona 池 seed、记录每次调用的 model 与 temperature、保存原始响应日志。
- **成本意识**：persona×题项×实验条件的笛卡尔积会快速放大调用量，先用小规模试跑再放量。

## 关键细节与易错点

- **易错：把硅基样本当真人样本做最终因果推断**。硅基数据没有真实的外部代表性，最终的因果结论须以真人数据为准。硅基适合预测试、探索、稳健性补充。
- **易错：persona 设计脱离真实分布**。随手编几个 persona 就开跑，应答分布会反映 LLM 的"常识刻板印象"而非目标人群。务必基于统计资料设分布。
- **易错：persona 同质化导致伪低方差**。所有 persona 共用一个粗略画像，应答高度一致，误以为"该人群意见高度一致"。其实是画像不够异质。
- **易错：忽视 LLM 的社会期许偏误与 sycophancy**。LLM 倾向于给出"政治正确""乐于助人"的应答，可能系统性高估积极态度、低估负面态度。需在 prompt 中明确"如实作答，包括负面态度"，并在校准中检查。
- **易错：温度设置不当**。temperature=0 会导致所有同画像 persona 应答几乎相同，失去个体差异模拟；过高则应答随机无意义。问卷预测试建议 0.6-0.8。
- **易错：不做有效性校准就用硅基数据下结论**。没有真人基准对照（哪怕小样本）或文献对照，硅基结论的可信度无法论证。
- **易错：混淆"生成数据"与"采集真实数据"**。在论文中必须如实说明数据来源是 LLM 模拟生成，不得表述为"调研数据"而隐去生成性质——这是学术诚信红线。
- **易错：忽视伦理边界**。即使被试是 LLM，若 persona 涉及敏感人群（如特定疾病患者、弱势群体），研究问题本身仍可能触及伦理审查范围。涉及真人对照数据时伦理审批照常适用。

## 社科科研示例

**场景**：一位公共管理博士生研究"基层公务员对数据共享政策的接受度及其影响因素"，设计了一份含 24 个 Likert 题项的问卷，准备在三个省份正式发放。在正式投放（涉及伦理审批、抽样、实地联系）前，希望先做预测试。

**硅基预测试流程**：

1. 基于三省份基层公务员的人口统计资料（年龄/学历/职级/部门分布），生成 300 个 persona。
2. 让每个 persona 作答 24 题项问卷，温度 0.7。
3. 跑 `pilot_analysis`：发现 Q7（"数据共享能提升我的工作效率"）天花板效应严重（78% 选 5），Q15（"我担心数据共享增加我的工作负担"）在高职级 persona 中几乎无变异——说明题项对该子群体无区分度。
4. 据此修订：Q7 加入限定条件"在现有系统兼容性下"，Q15 细化"短期 vs 长期负担"。
5. 用本课题组已有的 30 份真人预调研数据做 `calibrate_against_human`，方向一致率 0.83，通过校准。
6. 论文中方法部分明确写明："问卷题项经硅基样本预测试修订，并用 30 份真人预调研数据校准应答方向一致性（一致率 83%）；最终假设检验基于三省份正式抽样数据。"

这样硅基样本发挥了明确、有限、可论证的作用，且没有越界冒充真实调研数据。

## 拓展学习

- Argyle, L. C. et al. (2023). "Out of One, Many: Using Language Models to Simulate Human Samples." *Political Analysis*, 31(3). ——硅基样本范式奠基论文之一，讨论 persona 生成与有效性
- Horton, J. J. (2023). "Large Language Models as Simulated Economic Agents: Evidence from Experimental Economics." *NBER Working Paper*. ——LLM 作为经济学实验被试
- Aher, G. et al. (2023). "Using Large Language Models to Simulate Multiple Humans and Generate Human Synthetic Data." *arXiv:2306.04964*. ——联合分析等实验范式的硅基复现
- 国内综述可关注《管理世界》《心理学报》等关于 AI 辅助实验方法论的最新讨论

## 参考链接

- https://opencode.ai/docs/ — opencode Skill 文档（将硅基调研流程封装为 Skill）
- `knowledge/m4-3-skill-data-collection.md` — 数据采集 Skill 封装（硅基调研可作为其中一类 Skill）
- `knowledge/m4-4-agent-data-collection.md` — Agent 编排数据采集流水线（与本文互补：一个是自动化获取真实数据，一个是生成合成数据）
- `knowledge/m4-12-validity.md` — 有效性论证（硅基样本校准的理论基础）
