# 定性分析方法AI赋能

> **引入时机**：W7 | **核心挑战**："文本分析、内容分析、案例研究——如何用AI辅助定性分析？" | **层级**：Recommended

## 为什么要在项目阶段学习这个知识点？

并非所有社科研究问题都适合定量方法。当你研究"政策话语如何塑造公众认知"、"组织文化如何影响变革"或"国际规范如何在国内扩散"等问题时，定性分析——文本分析、内容分析、案例研究——是更合适的方法选择。然而，定性分析的传统痛点是：编码过程耗时且主观性强、跨案例比较缺乏系统框架、分析过程难以透明化。

AI为定性分析带来了三重变革潜力：文本处理能力的数量级提升（从手动编码几十篇到AI辅助处理上千篇）、编码一致性的可量化评估（人机编码一致性检验）、分析过程的可追溯性（每个编码决策都有AI辅助记录）。这些能力让定性研究从"少数样本深度解读"扩展到"大规模文本系统分析"，同时保持定性分析的理论敏感性。

但AI在定性研究中的角色边界比定量更微妙：AI可以作为编码助手帮你处理大量文本，但编码方案的理论基础、编码结果的学术解释、跨案例比较的理论提炼，这些体现研究贡献的核心环节必须由你完成。AI是"编码助手而非解释者"——这个定位必须贯穿始终。

## 这个知识点的核心内容

### AI辅助文本分析

文本分析是定性研究的核心方法之一，AI在此场景有三个层次的辅助：

**第一层：基础文本处理**

```python
import pandas as pd
from collections import Counter

class TextAnalyzer:
    def __init__(self, texts, llm_client=None):
        self.texts = texts if isinstance(texts, list) else [texts]
        self.llm = llm_client
        self.results = {}

    def keyword_frequency(self, keywords):
        freq_data = []
        for i, text in enumerate(self.texts):
            freq = {kw: text.count(kw) for kw in keywords}
            freq["text_id"] = i
            freq_data.append(freq)
        self.results["keyword_freq"] = pd.DataFrame(freq_data)
        return self.results["keyword_freq"]

    def extract_sentences_with_keywords(self, keywords, window=1):
        extracted = []
        for i, text in enumerate(self.texts):
            sentences = text.split("。")
            for j, sent in enumerate(sentences):
                if any(kw in sent for kw in keywords):
                    start = max(0, j - window)
                    end = min(len(sentences), j + window + 1)
                    context = "。".join(sentences[start:end])
                    extracted.append({
                        "text_id": i,
                        "sentence_idx": j,
                        "context": context,
                        "matched_keywords": [
                            kw for kw in keywords if kw in sent
                        ]
                    })
        self.results["keyword_contexts"] = pd.DataFrame(extracted)
        return self.results["keyword_contexts"]
```

**第二层：主题建模**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class TopicModeler:
    def __init__(self, texts, n_topics=5):
        self.texts = texts
        self.n_topics = n_topics
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            token_pattern=r"(?u)\b\w+\b"
        )
        self.dtm = self.vectorizer.fit_transform(texts)
        self.lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=50
        )
        self.doc_topic = self.lda.fit_transform(self.dtm)

    def get_topics(self, n_words=10):
        feature_names = self.vectorizer.get_feature_names_out()
        topics = {}
        for idx, topic in enumerate(self.lda.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            topics["topic_{}".format(idx + 1)] = [
                feature_names[i] for i in top_indices
            ]
        return topics

    def interpret_topics_with_llm(self, llm_client):
        topics = self.get_topics()
        prompt = """以下是从政策文本中提取的主题及其关键词，请为每个主题提供一个学术化的主题名称和简要描述。

主题关键词：
{}

请用JSON格式返回，每个主题包含name和description字段。注意：这是辅助命名，最终主题名称应由研究者根据理论框架确定。""".format(
            topics
        )

        response = llm_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
```

**第三层：话语分析**

```python
def discourse_analysis_with_llm(texts, research_question, llm_client):
    prompt = """你是一位话语分析顾问。请基于以下文本片段，分析其中的话语策略和意义建构方式。

研究问题：{}
文本片段：
{}

请从以下维度分析：
1. 话语主体与权威建构：谁在说话？如何建立权威性？
2. 框架策略：如何定义问题？使用了哪些隐喻和类比？
3. 排除与沉默：什么被选择性地忽略了？
4. 话语变迁：与早期文本相比，话语策略是否有变化？

注意：你的角色是辅助识别话语模式，不是替研究者做解释。所有发现的模式都需要回到理论框架中由研究者解读。""".format(
        research_question,
        "\n---\n".join(texts[:5])
    )

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
```

### AI辅助内容分析

内容分析的核心是编码方案的设计和应用：

**编码方案设计与AI协作：**

```python
def design_coding_scheme_with_llm(theoretical_framework, sample_texts,
                                   llm_client):
    prompt = """你是一位内容分析方法论顾问。请基于以下理论框架和样本文本，辅助设计编码方案。

理论框架：{}
样本文本（前3篇）：
{}

请提供：
1. 建议的编码维度（基于理论框架）
2. 每个维度下的编码类别定义
3. 编码规则说明（边界案例的处理方式）
4. 示例文本的初步编码结果

重要：编码方案的理论基础应由研究者确定，AI仅辅助将理论操作化为可编码的类别。最终编码方案必须经过研究者审查和试编码验证。""".format(
        theoretical_framework,
        "\n---\n".join(sample_texts[:3])
    )

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
```

**编码一致性检验：**

```python
from sklearn.metrics import cohen_kappa_score

def calculate_inter_coder_agreement(human_codes, ai_codes, level="nominal"):
    if level == "nominal":
        kappa = cohen_kappa_score(human_codes, ai_codes)
    elif level == "ordinal":
        from sklearn.metrics import cohen_kappa_score
        kappa = cohen_kappa_score(human_codes, ai_codes)

    agreement_pct = sum(
        1 for h, a in zip(human_codes, ai_codes) if h == a
    ) / len(human_codes)

    return {
        "cohen_kappa": float(kappa),
        "agreement_pct": float(agreement_pct),
        "interpretation": (
            "优秀(>0.8)" if kappa > 0.8
            else "良好(0.6-0.8)" if kappa > 0.6
            else "中等(0.4-0.6)" if kappa > 0.4
            else "偏低(<0.4)，需修订编码方案"
        )
    }

def iterative_coding_refinement(texts, coding_scheme, llm_client,
                                 max_rounds=3):
    for round_num in range(max_rounds):
        ai_codes = []
        for text in texts:
            code = _code_single_text(text, coding_scheme, llm_client)
            ai_codes.append(code)

        human_codes = []
        for text in texts:
            code = input("请对以下文本编码: {}...".format(text[:100]))
            human_codes.append(code)

        agreement = calculate_inter_coder_agreement(human_codes, ai_codes)
        print("第{}轮编码一致性: Kappa={:.3f} ({})".format(
            round_num + 1, agreement["cohen_kappa"],
            agreement["interpretation"]
        ))

        if agreement["cohen_kappa"] > 0.7:
            print("编码一致性达标")
            return coding_scheme, agreement

        coding_scheme = _refine_scheme_from_disagreements(
            coding_scheme, human_codes, ai_codes, texts, llm_client
        )

    return coding_scheme, agreement
```

### AI辅助案例研究

案例研究中的AI辅助主要体现在案例选择和跨案例比较：

```python
def ai_assisted_case_selection(population_data, selection_criteria,
                                llm_client):
    prompt = """你是一位案例研究方法论顾问。请基于以下总体数据和选择标准，辅助案例选择。

总体数据摘要：
{}

选择标准：
{}

请提供：
1. 基于选择标准的案例类型划分（如：典型案例、极端案例、最大差异案例等）
2. 每种类型的推荐案例（附带选择理由）
3. 案例数量建议（基于理论饱和原则）
4. 潜在的选择偏差及应对策略

注意：案例选择的最终决策必须由研究者基于研究目的做出。""".format(
        population_data, selection_criteria
    )

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def cross_case_comparison_with_llm(case_data, dimensions, llm_client):
    comparison_table = {}
    for case_name, data in case_data.items():
        comparison_table[case_name] = {}
        for dim in dimensions:
            comparison_table[case_name][dim] = data.get(dim, "N/A")

    prompt = """基于以下跨案例比较表，识别模式与差异：

{}

维度：{}

请分析：
1. 跨案例的共性模式
2. 关键差异点及其可能解释
3. 基于模式的初步类型学
4. 需要进一步调查的问题

注意：跨案例比较的理论解释应由研究者完成，AI仅辅助识别经验模式。""".format(
        comparison_table, dimensions
    )

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
```

### 定性研究中AI的角色

**核心定位：AI是编码助手而非解释者。**

| 研究环节 | AI的适当角色 | AI的不当角色 |
|---------|------------|------------|
| 编码方案设计 | 将理论操作化为编码类别 | 替研究者确定理论维度 |
| 文本编码 | 执行编码方案，标注文本 | 判断编码是否"正确" |
| 模式识别 | 识别文本中的重复模式 | 解释模式的深层含义 |
| 跨案例比较 | 系统化呈现案例异同 | 选择"正确"的解释框架 |
| 理论提炼 | 辅助梳理概念关系 | 替研究者做理论贡献判断 |

**研究透明性要求：** 使用AI辅助定性分析时，论文方法部分应说明：AI使用的环节和方式、编码方案的人工审查过程、人机编码一致性指标、AI辅助如何影响分析过程。

## 关键细节与易错点

- **易错：让AI自主编码而不建立编码方案**。没有理论驱动的编码方案，AI的编码会根据统计频率而非理论相关性分配代码，导致结果表面化。必须先建立理论驱动的编码方案，再让AI执行
- **易错：不检验人机编码一致性**。AI编码可能系统性偏移——比如倾向将模糊文本归入某一大类。必须通过Cohen's Kappa等指标量化人机一致性，低于0.6的编码方案需修订
- **易错：混淆主题建模与理论框架**。LDA提取的"主题"是统计模式，不是理论概念。将"topic_3: 数字、平台、数据"直接命名为"数字化转型"是过度解读。统计主题需要经过理论诠释才能成为学术概念
- **易错：AI辅助话语分析缺乏反思性**。话语分析本身就是反思性的方法——研究者的立场和偏见是分析的一部分。如果AI的话语分析没有体现这种反思性，结论可能过于"客观化"而失去话语分析的批判力度
- **易错：忽略小样本深度**。AI让大规模文本处理变得容易，但可能导致研究者追求样本量而牺牲分析深度。定性研究的价值在于理论深度而非统计代表性

## 社科科研示例

**场景**：一位传播学博士生研究"中国媒体如何建构'共同富裕'话语"，收集了2020-2023年间3家主流媒体共800篇相关报道。

```python
texts = [article["content"] for article in media_data]
analyzer = TextAnalyzer(texts, llm_client=llm)

freq_df = analyzer.keyword_frequency(
    ["共同富裕", "分配", "公平", "三次分配", "慈善", "税收", "橄榄型"]
)

topic_model = TopicModeler(texts, n_topics=6)
topics = topic_model.get_topics(n_words=15)
topic_names = topic_model.interpret_topics_with_llm(llm)

coding_scheme_text = design_coding_scheme_with_llm(
    theoretical_framework="""
    基于框架理论，关注：
    1. 问题定义框架（如何定义"共同富裕"的问题性质）
    2. 归因框架（将不平等归因于什么）
    3. 解决方案框架（提出何种实现路径）
    4. 道德评价框架（使用何种价值判断）
    """,
    sample_texts=texts[:5],
    llm_client=llm
)

discourse_results = discourse_analysis_with_llm(
    texts[:20],
    research_question="中国媒体如何建构共同富裕的话语框架",
    llm_client=llm
)
```

**方法论说明（论文方法部分参考）：** "本文采用计算辅助内容分析法。首先通过LDA主题建模初步识别话语维度，然后基于框架理论建立编码方案，使用LLM辅助执行编码，人工审查随机抽取的20%样本，人机编码一致性Kappa=0.74，达到良好水平。话语分析层面对关键词语境进行深度解读。"

## 拓展学习

- 《The Coding Manual for Qualitative Researchers》(Saldana)——定性编码方法经典
- 《Qualitative Data Analysis》(Miles, Huberman & Saldana)——定性分析系统方法
- 《Case Study Research and Applications》(Yin)——案例研究方法论权威
- 《Content Analysis》(Krippendorff)——内容分析方法论经典
- NVivo/MAXQDA文档——传统定性分析软件与AI辅助的结合

## 参考链接

- https://scikit-learn.org/stable/modules/decomposition.html — sklearn主题建模文档
- https://www.aclweb.org/anthology/ — ACL Anthology（NLP文本分析论文）
- https://qhr.sagepub.com/ — Qualitative Health Research期刊
- https://nsuworks.nova.edu/tqr/ — The Qualitative Report期刊
- https://github.com/explosion/spaCy — spaCy NLP库
