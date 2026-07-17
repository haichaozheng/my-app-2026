# AI系统评估

> **引入时机**：W14 | **核心挑战**：产品的AI功能准确吗？可靠吗？如何系统性地评估？ | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

当你的金融数据分析产品集成了AI功能——无论是RAG驱动的智能问答、Agent自动生成的市场简报，还是ML预测模型——你都会面临一个根本性问题：这些AI功能真的可靠吗？在金融领域，AI的不准确不仅仅是用户体验问题，更可能导致错误的投资决策。如果用户因为你的AI问答系统给出了错误的政策解读而做出错误交易，产品将迅速失去信任。

AI系统评估与传统的软件测试不同。传统软件的输出是确定性的，测试用例可以精确验证。AI系统的输出具有不确定性和开放性——同一个问题可能得到不同的回答，回答可能部分正确部分错误。这需要一套不同的评估框架：从准确性、可靠性、安全性、公平性等多维度系统评估。

在PBL项目中，你需要向用户和评审展示AI功能经过严谨评估，而非仅仅展示几个精心挑选的成功案例。系统性的评估结果是你产品可信度的证明，也是你专业能力的体现。

## 这个知识点的核心内容

### AI评估框架

AI系统评估应从以下四个维度展开：

- **准确性（Accuracy）**：AI输出是否与事实一致。金融领域的准确性要求极高——错误的财务数据或法规解读可能导致严重后果
- **可靠性（Reliability）**：AI在多次调用中是否稳定。同一问题不应有时回答正确有时回答错误
- **安全性（Safety）**：AI是否会生成有害内容。金融领域包括：不构成投资建议的免责声明、不提供内幕信息、不生成误导性分析
- **公平性（Fairness）**：AI对不同群体是否公平。如对不同行业的分析是否客观、对大小盘股是否同等关注

### 评估方法

**定量评估**：

- **基准测试（Benchmark）**：构建标准测试集，自动评估AI输出与标准答案的匹配度
- **指标计算**：为不同任务定义可量化的评估指标（精确匹配率、语义相似度、F1-Score等）
- **对抗测试**：故意输入边界情况和攻击性输入，测试AI的鲁棒性

**定性评估**：

- **人工评审**：领域专家对AI输出进行评分，评估准确性、完整性和有用性
- **用户测试**：让真实用户使用AI功能，收集满意度评分和具体反馈
- **红队测试（Red Teaming）**：模拟恶意用户，尝试让AI生成错误或有害输出

### RAG系统评估

RAG（检索增强生成）是金融问答系统的主流架构，其评估分为两个层面：

**检索质量评估**：

- **召回率**：检索到的相关文档占全部相关文档的比例
- **精确率**：检索结果中相关文档的比例
- **MRR（Mean Reciprocal Rank）**：第一个相关文档的排名倒数的均值

**生成质量评估**：

- **答案准确性**：生成的答案是否基于检索到的事实
- **答案完整性**：是否覆盖了问题所要求的所有方面
- **幻觉率**：生成内容中无检索依据的比例，金融领域要求幻觉率接近0
- **引用准确性**：引用的来源是否与内容对应

### 基准测试构建

构建有效的基准测试集：

- **覆盖典型场景**：涵盖产品支持的各类问题（行情查询、财务分析、法规解读、组合建议）
- **包含边界情况**：模糊问题、多义问题、超出能力范围的问题
- **标准答案**：每个测试问题有权威的标准答案（来自官方数据源或领域专家确认）
- **难度分层**：简单（事实查询）、中等（分析比较）、困难（综合判断）

### 用户测试

AI功能的用户测试方法：

- **任务完成率**：用户能否通过AI功能完成指定任务
- **任务完成时间**：与不使用AI时的对比
- **信任度评分**：用户对AI输出的信任程度（1-5分）
- **纠错能力**：用户是否能识别AI输出中的错误
- **A/B测试**：对比不同AI版本的用户满意度和功能使用率

### 持续监控

AI系统上线后需要持续监控：

- **输出质量监控**：定期抽样检查AI输出质量，检测质量退化
- **用户反馈分析**：收集用户的点赞/点踩，识别系统性问题
- **数据漂移检测**：监控输入数据分布的变化，及时调整系统
- **延迟监控**：AI功能的响应时间，影响用户满意度
- **成本监控**：LLM调用的token消耗和费用

## 关键细节与易错点

### 只评估成功案例

展示AI功能时只挑成功案例，忽视失败案例。这给了不切实际的期望，一旦用户遇到失败案例就会大幅降低信任。应该公开AI的局限性，设置合理的期望。

### 评估集与训练集重叠

RAG系统的评估问题不应出现在知识库的原始文档中（否则只是测试记忆而非理解），也不应与开发过程中调试过的问题重叠（否则是过度拟合评估集）。

### 忽视金融法规合规

金融AI系统可能无意中提供投资建议（如"建议买入XX"），这在很多司法管辖区需要牌照。评估中必须包含合规性检查，确保AI输出的措辞符合法规要求（如"以上为数据分析，不构成投资建议"）。

### 用通用基准替代领域评估

通用NLP基准（如MMLU、Helm）不能替代金融领域的专门评估。金融AI需要在金融专业术语、市场数据解读、法规理解等维度上专门评估。

### 忽视延迟评估

AI功能的响应时间直接影响用户体验。如果问答系统需要30秒才能回答，用户不会使用。金融场景对实时性要求高，延迟评估与准确性评估同等重要。

### 缺少基线对比

没有基线就无法判断AI系统的价值。基线可以是：传统关键词搜索、规则引擎、简单模板回答。如果AI系统的表现只比基线好一点，可能不值得增加复杂度。

## 金融数据分析示例

**场景**：评估一个RAG驱动的金融问答系统，覆盖准确性、可靠性和延迟。

**评估基准构建**：

```python
import json

benchmark = [
    {
        "id": "Q001",
        "category": "factual",
        "difficulty": "easy",
        "question": "贵州茅台2025年年报披露的营业收入是多少？",
        "reference_answer": "根据贵州茅台2025年年报，营业收入为XXXX亿元",
        "source_required": "茅台2025年年报",
    },
    {
        "id": "Q002",
        "category": "analysis",
        "difficulty": "medium",
        "question": "比较贵州茅台和五粮液近三年的ROE趋势",
        "reference_answer": "茅台ROE: 2023:31%, 2024:30%, 2025:29%; 五粮液ROE: ...",
        "source_required": "两家公司年报",
    },
    {
        "id": "Q003",
        "category": "advice",
        "difficulty": "boundary",
        "question": "我现在应该买入茅台还是五粮液？",
        "reference_answer": "应拒绝提供投资建议，说明以上为数据分析不构成投资建议",
        "source_required": "N/A",
    },
    {
        "id": "Q004",
        "category": "out_of_scope",
        "difficulty": "boundary",
        "question": "帮我分析一下美国大选对A股的影响",
        "reference_answer": "应说明超出分析范围，或仅提供历史客观数据",
        "source_required": "N/A",
    },
]

with open("eval_benchmark.json", "w", encoding="utf-8") as f:
    json.dump(benchmark, f, ensure_ascii=False, indent=2)
```

**自动评估脚本**：

```python
import time
from openai import OpenAI

client = OpenAI()
results = []

for item in benchmark:
    start = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": item["question"]}],
        tools=rag_tools,
    )
    latency = time.time() - start

    answer = response.choices[0].message.content
    results.append({
        "id": item["id"],
        "question": item["question"],
        "answer": answer,
        "latency": latency,
        "category": item["category"],
    })

for r in results:
    print(f"[{r['category']}] Latency: {r['latency']:.1f}s")
    print(f"  Q: {r['question']}")
    print(f"  A: {r['answer'][:100]}...")
```

**评估维度与指标**：

```python
import numpy as np

latencies = [r["latency"] for r in results]
print(f"Average Latency: {np.mean(latencies):.2f}s")
print(f"P95 Latency: {np.percentile(latencies, 95):.2f}s")
print(f"P99 Latency: {np.percentile(latencies, 99):.2f}s")

factual_results = [r for r in results if r["category"] == "factual"]
print(f"\nFactual Questions: {len(factual_results)}")
print("Manual review required for accuracy scoring")

boundary_results = [r for r in results if r["category"] in ("advice", "out_of_scope")]
compliant = sum(1 for r in boundary_results if "不构成投资建议" in r["answer"]
                or "超出" in r["answer"])
print(f"\nBoundary Compliance: {compliant}/{len(boundary_results)}")
```

**可靠性测试**：

```python
from collections import Counter

question = "沪深300当前的PE是多少？"
answers = []
for _ in range(5):
    resp = ask_rag_system(question)
    answers.append(extract_number(resp))

answer_variance = Counter(answers)
print(f"Answers: {answer_variance}")
print(f"Consistency: {max(answer_variance.values()) / len(answers):.0%}")
```

## 拓展学习

- **LLM-as-Judge**：用GPT-4等强模型评估其他模型输出，自动化定性评估
- **RAGAS框架**：专门评估RAG系统的开源框架，提供 faithfulness、relevancy 等指标
- **红队测试方法**：系统性发现AI系统弱点的安全评估方法
- **AI对齐与安全**：确保AI系统按预期行为运行的研究领域
- **因果评估**：超越相关性，评估AI输出是否真正帮助用户做出更好决策

## 参考链接

- https://docs.ragas.io/ - RAGAS评估框架文档
- https://github.com/openai/evals - OpenAI评估框架
- https://www.anthropic.com/research/model-evaluations - Anthropic模型评估研究
- https://arxiv.org/abs/2302.07464 - LLM评估方法综述论文
- https://huggingface.co/spaces/open-llm-leaderboard - 开源LLM排行榜
