# AI系统评估方法

> **引入时机**：W7 | **核心挑战**："AI辅助得出的分析结果可信吗？如何评估准确性、检测偏见、做稳健性检验？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

W7的核心问题是"做对"而非"做出来"。当你用AI辅助完成了数据分析——AI帮你生成代码、帮你解读结果、甚至帮你设计稳健性检验——一个根本性问题浮现：这些AI辅助产出的结果可信吗？AI的参与是否引入了系统性的偏见或错误？

这个问题并非杞人忧天。LLM可能在代码中引入隐蔽的统计错误（如错误的标准误计算），AI的解读可能带有确认偏差（顺着你期望的方向解释），AI生成的替代解释可能遗漏关键的竞争性假设。如果你不做系统性评估，这些隐蔽的问题可能让你的研究从"创新"变成"错误"。

AI系统评估不是对AI的不信任，而是对研究的负责。本知识点教你从三个维度评估AI辅助分析的可信度：结果可信度（AI产出的数字对不对）、偏见检测（AI是否系统性地偏向某个方向）、稳健性验证（结论在不同条件下是否成立）。这三个维度共同构成"做对"研究的质量保障体系。

## 这个知识点的核心内容

### AI系统评估的三维度

| 维度 | 核心问题 | 评估方法 | 关键指标 |
|------|---------|---------|---------|
| 结果可信度 | AI产出的结果是否准确？ | 交叉验证、人工抽样核查 | 准确率、一致率 |
| 偏见检测 | AI是否系统性地偏向某方向？ | 对比实验、方向偏差分析 | 偏差方向与幅度 |
| 稳健性验证 | 结论在不同条件下是否成立？ | 多模型、多参数、多子集 | 结论一致性 |

三个维度的关系：结果可信度是基础（结果都不对就没必要讨论偏见），偏见检测是深化（即使结果准确也可能有系统性偏向），稳健性验证是兜底（确保结论不仅在一个特定设定下成立）。

### 结果可信度评估方法

**交叉验证——检验AI编码/分类的准确性：**

```python
from sklearn.model_selection import KFold
import numpy as np

def cross_validate_ai_coding(texts, coding_scheme, ai_coder, human_coder,
                              n_folds=5):
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    fold_results = []

    for fold, (train_idx, test_idx) in enumerate(kf.split(texts)):
        train_texts = [texts[i] for i in train_idx]
        test_texts = [texts[i] for i in test_idx]

        for text in train_texts:
            ai_coder.learn_from_example(text, human_coder.code(text))

        ai_predictions = [ai_coder.code(t) for t in test_texts]
        human_labels = [human_coder.code(t) for t in test_texts]

        agreement = sum(
            1 for a, h in zip(ai_predictions, human_labels)
            if a == h
        ) / len(test_texts)

        fold_results.append({
            "fold": fold + 1,
            "agreement_rate": agreement,
            "n_test": len(test_texts)
        })

    return {
        "mean_agreement": np.mean([r["agreement_rate"] for r in fold_results]),
        "std_agreement": np.std([r["agreement_rate"] for r in fold_results]),
        "fold_details": fold_results
    }
```

**人工抽样核查——检验AI统计分析的准确性：**

```python
import random

def human_sampling_verification(ai_results, original_data, sample_size=30,
                                 check_items=None):
    if check_items is None:
        check_items = ["coefficient", "p_value", "r_squared"]

    sampled_indices = random.sample(
        range(len(ai_results)), min(sample_size, len(ai_results))
    )

    verification_results = []
    for idx in sampled_indices:
        ai_result = ai_results[idx]
        manual_result = _manual_recalculate(original_data, idx, check_items)

        verification = {"index": idx}
        for item in check_items:
            ai_val = ai_result.get(item)
            manual_val = manual_result.get(item)
            if ai_val is not None and manual_val is not None:
                if isinstance(ai_val, float):
                    rel_error = abs(ai_val - manual_val) / (
                        abs(manual_val) + 1e-10
                    )
                    verification[item] = {
                        "ai_value": ai_val,
                        "manual_value": manual_val,
                        "relative_error": rel_error,
                        "match": rel_error < 0.01
                    }
                else:
                    verification[item] = {
                        "ai_value": ai_val,
                        "manual_value": manual_val,
                        "match": ai_val == manual_val
                    }
        verification_results.append(verification)

    summary = {}
    for item in check_items:
        matches = sum(
            1 for v in verification_results
            if v.get(item, {}).get("match", False)
        )
        total = len(verification_results)
        summary[item] = {
            "accuracy_rate": matches / total if total > 0 else 0,
            "total_checked": total
        }

    return {
        "verification_results": verification_results,
        "summary": summary,
        "overall_accuracy": np.mean([
            s["accuracy_rate"] for s in summary.values()
        ])
    }

def _manual_recalculate(data, idx, check_items):
    return {"coefficient": 0.0, "p_value": 0.0, "r_squared": 0.0}
```

### 偏见检测

AI的偏见可能从两个来源传导到你的研究：训练数据偏见和AI输出的系统性偏向。

**训练数据偏见的传导：**

LLM在大量文本上训练，这些文本可能包含社会科学中的特定范式偏好。例如，经济学领域的主流文献可能偏向新古典框架，导致LLM在解读结果时默认使用新古典逻辑，忽视制度经济学或政治经济学的替代解释。

```python
def detect_interpretation_bias(llm_interpretations, direction_hypothesis):
    directions = []
    for interp in llm_interpretations:
        positive_words = ["促进", "提升", "增加", "正向", "支持"]
        negative_words = ["抑制", "降低", "减少", "负向", "不支持"]
        neutral_words = ["不确定", "需进一步", "视情况"]

        pos_count = sum(interp.count(w) for w in positive_words)
        neg_count = sum(interp.count(w) for w in negative_words)
        neu_count = sum(interp.count(w) for w in neutral_words)

        if pos_count > neg_count and pos_count > neu_count:
            directions.append("positive")
        elif neg_count > pos_count and neg_count > neu_count:
            directions.append("negative")
        else:
            directions.append("neutral")

    direction_dist = {
        d: directions.count(d) / len(directions)
        for d in set(directions)
    }

    bias_detected = False
    if direction_hypothesis in direction_dist:
        if direction_dist[direction_hypothesis] > 0.7:
            bias_detected = True
            bias_message = (
                "AI解读偏向假设方向({})的比例达{:.0%}，"
                "可能存在确认偏差。建议使用中性提示重新解读。".format(
                    direction_hypothesis,
                    direction_dist[direction_hypothesis]
                )
            )

    return {
        "direction_distribution": direction_dist,
        "bias_detected": bias_detected,
        "bias_message": bias_message if bias_detected else "未检测到明显偏向"
    }
```

**AI输出的系统性偏向检测：**

```python
def systematic_bias_test(data, dep_var, core_var, controls, llm_client,
                          n_trials=5):
    results = []
    for trial in range(n_trials):
        prompt_variants = [
            "这个回归结果意味着什么？",
            "如何解读这个回归系数？",
            "请客观分析这个统计结果",
            "这个发现有哪些可能的解释？",
            "对以下回归结果进行中性解读"
        ]

        prompt = """回归结果：因变量={}, 核心系数={}, p值={}
{}
请解读。""".format(
            dep_var, "PLACEHOLDER", "PLACEHOLDER",
            prompt_variants[trial]
        )

        response = llm_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        results.append(response.choices[0].message.content)

    bias_test = detect_interpretation_bias(results, "positive")
    return {
        "interpretations": results,
        "bias_analysis": bias_test,
        "recommendation": (
            "使用temperature=0和明确中立提示以减少偏差"
            if bias_test["bias_detected"]
            else "当前解读一致性可接受"
        )
    }
```

### 稳健性验证

稳健性验证在AI辅助场景下有三个特殊维度：不同模型设定、不同AI参数、不同数据子集。

**不同AI参数的稳健性：**

```python
def ai_parameter_robustness(data, dep_var, core_var, controls,
                             llm_client):
    temperatures = [0.0, 0.3, 0.7]
    prompt_styles = [
        {"style": "neutral", "prefix": "请客观解读以下结果"},
        {"style": "critical", "prefix": "请批判性地审视以下结果，特别关注可能的替代解释"},
        {"style": "detailed", "prefix": "请详细解读以下结果，包含效应量评估和局限性"}
    ]

    results_matrix = []
    for temp in temperatures:
        for style in prompt_styles:
            prompt = "{}\n回归结果：...".format(style["prefix"])
            response = llm_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=temp
            )
            results_matrix.append({
                "temperature": temp,
                "prompt_style": style["style"],
                "interpretation": response.choices[0].message.content
            })

    consistency = _assess_interpretation_consistency(results_matrix)
    return {
        "results": results_matrix,
        "consistency_score": consistency["score"],
        "inconsistency_points": consistency["disagreements"],
        "recommendation": (
            "不同参数下解读高度一致，可信度较高"
            if consistency["score"] > 0.8
            else "不同参数下解读存在分歧，需人工审查分歧点"
        )
    }

def _assess_interpretation_consistency(results_matrix):
    interpretations = [r["interpretation"] for r in results_matrix]
    direction_mentions = []
    for interp in interpretations:
        if any(w in interp for w in ["正向", "促进", "增加", "positive"]):
            direction_mentions.append("positive")
        elif any(w in interp for w in ["负向", "抑制", "减少", "negative"]):
            direction_mentions.append("negative")
        else:
            direction_mentions.append("neutral")

    most_common = max(set(direction_mentions), key=direction_mentions.count)
    consistency = direction_mentions.count(most_common) / len(direction_mentions)

    return {
        "score": consistency,
        "most_common_direction": most_common,
        "disagreements": [
            results_matrix[i] for i, d in enumerate(direction_mentions)
            if d != most_common
        ]
    }
```

**不同数据子集的稳健性：**

```python
def subset_robustness_check(data, dep_var, core_var, controls,
                              subset_vars, model_func):
    full_sample_result = model_func(data, dep_var, core_var, controls)
    full_coef = full_sample_result.params[core_var]
    full_sign = np.sign(full_coef)

    subset_results = []
    for var in subset_vars:
        for val in data[var].unique():
            subset = data[data[var] == val]
            if len(subset) < 50:
                continue
            result = model_func(subset, dep_var, core_var, controls)
            coef = result.params[core_var]
            pval = result.pvalues[core_var]
            subset_results.append({
                "subset_var": var,
                "subset_value": val,
                "n_obs": len(subset),
                "coefficient": float(coef),
                "p_value": float(pval),
                "direction_consistent": np.sign(coef) == full_sign
            })

    direction_consistency = sum(
        1 for r in subset_results if r["direction_consistent"]
    ) / len(subset_results) if subset_results else 0

    return {
        "full_sample_coef": float(full_coef),
        "subset_results": subset_results,
        "direction_consistency_rate": direction_consistency,
        "assessment": (
            "子样本方向一致率{:.0%}，结论稳健".format(direction_consistency)
            if direction_consistency > 0.8
            else "子样本方向存在分歧，需进一步调查异质性"
        )
    }
```

## 关键细节与易错点

- **易错：只验证AI代码的正确性，不验证AI解读的可靠性**。代码可能有bug但解读问题更大——AI可能从正确的统计结果推导出有偏的结论。两者都需要验证
- **易错：抽样核查样本量太小**。只检查3-5个结果就说"AI结果准确"，统计上没有意义。建议至少30个样本的抽样核查
- **易错：偏见检测只看"方向"不看"程度"**。AI可能90%的情况解读正确，但10%的情况系统性地偏向某方向——在社科研究中，这10%的偏向可能恰好影响关键结论
- **易错：将AI参数稳健性与统计稳健性混淆**。"不同temperature下AI解读一致"不等于"不同模型设定下统计结论稳健"——前者是AI系统的稳健性，后者是研究结论的稳健性，两者都需要但不可互相替代
- **易错：忽视LLM版本更新的影响**。你用GPT-4做的分析，换成GPT-4o或Claude可能得到不同解读。论文中应注明使用的LLM版本，关键结论应在至少两个LLM上交叉验证

## 社科科研示例

**场景**：一位社会学博士生用AI辅助编码了500篇政策文本，需要评估AI编码的可信度。

```python
from sklearn.metrics import cohen_kappa_score

human_coded_sample = {
    idx: human_codes[idx]
    for idx in random.sample(range(500), 50)
}

ai_coded_sample = {
    idx: ai_codes[idx]
    for idx in human_coded_sample.keys()
}

human_labels = [human_coded_sample[i] for i in sorted(human_coded_sample.keys())]
ai_labels = [ai_coded_sample[i] for i in sorted(ai_coded_sample.keys())]

kappa = cohen_kappa_score(human_labels, ai_labels)
agreement_pct = sum(1 for h, a in zip(human_labels, ai_labels) if h == a) / len(human_labels)

print("人机编码一致性:")
print("  Cohen's Kappa: {:.3f}".format(kappa))
print("  一致率: {:.1%}".format(agreement_pct))

if kappa < 0.6:
    print("  警告：一致性偏低，需修订编码方案或重新训练AI编码器")
elif kappa < 0.8:
    print("  一致性良好，建议对不一致样本进行逐案审查")
else:
    print("  一致性优秀，AI编码可信度较高")

bias_check = detect_interpretation_bias(
    [ai_interpretations[i] for i in range(len(ai_interpretations))],
    direction_hypothesis="positive"
)
print("\nAI解读偏见检测:")
print("  {}".format(bias_check["bias_message"]))
```

## 拓展学习

- 《AI Auditing》——AI系统审计方法论
- Fairlearn——机器学习公平性评估工具
- 《Handbook of Research on AI Bias》——AI偏见研究手册
- 《Robustness in Statistical Analysis》——统计稳健性方法论
- AI Model Cards（Mitchell et al.）——AI模型文档化标准

## 参考链接

- https://fairlearn.org/ — Fairlearn公平性评估框架
- https://arxiv.org/abs/1810.03993 — Model Cards论文
- https://www.microsoft.com/en-us/ai/responsible-ai — 微软负责任AI资源
- https://pair.withgoogle.com/ — Google PAIR人机交互研究
- https://aif360.readthedocs.io/en/latest/ — IBM AI Fairness 360工具包
