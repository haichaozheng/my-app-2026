# 数据采集方法论

> **引入时机**：W5 | **核心挑战**："研究需要的数据在哪里？API/爬虫/NLP文本提取如何选择？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

进入研究方案实施阶段，你面临的第一道关卡就是数据采集。很多博士生在开题时对数据来源做了乐观假设——"用某数据库的数据"或"从网上抓取"，但真正动手时才发现：数据库权限受限、API有调用频率限制、目标网站有反爬机制、政策文件是扫描PDF而非结构化文本。数据采集的困难远超预期，而数据质量直接决定分析结论的可信度。

不系统掌握数据采集方法论，你会陷入两种困境：一是"有数据但不对"——采集到的数据在代表性、时效性或准确性上存在系统性偏差，导致后续分析"垃圾进垃圾出"；二是"数据在手但不够"——只知道一种采集方式，遇到数据壁垒就停步，无法通过多种数据源交叉验证来提升研究稳健性。

掌握数据采集方法论后，你能根据研究问题系统性地规划数据策略：哪些数据通过API获取最可靠？哪些场景需要爬虫但要注意伦理边界？哪些非结构化文本需要NLP提取？如何评估采集到的数据是否真正代表你想研究的总体？这些能力是"做对"研究的基础。

## 这个知识点的核心内容

### 社科研究数据源概览

社科研究的数据源可以分为以下几类：

| 数据源类型 | 典型来源 | 优势 | 局限 |
|-----------|---------|------|------|
| 公开数据库 | CPS、CHFS、CFPS、CGSS | 规范、可复现、有文档 | 变量受限、时间滞后 |
| API接口 | 世界银行、IMF、国家统计局 | 实时、结构化、可编程 | 调用限制、覆盖范围有限 |
| 网络爬虫 | 政府网站、新闻平台、社交媒体 | 灵活、定制化 | 法律/伦理风险、反爬壁垒 |
| 问卷调查 | 自行设计发放 | 针对性强、变量可控 | 成本高、样本代表性问题 |
| 文本数据 | 政策文件、新闻报道、司法判例 | 丰富的语义信息 | 非结构化、提取难度大 |
| 实验数据 | 田野实验、实验室实验 | 因果识别强 | 外部效度受限 |

### 数据采集方法的选择逻辑

选择数据采集方法时应遵循"需求驱动、质量优先"原则：

```
研究问题 → 所需数据类型 → 可用数据源评估 → 采集方法选择 → 数据质量评估
     ↑                                                         ↓
     └──────────── 质量不达标则回溯调整 ←──────────────────────┘
```

选择逻辑的核心判断标准：

1. **数据是否已存在？** 如果已有公开数据库满足需求，优先使用——可复现性最高
2. **数据是否可通过API获取？** API比爬虫更稳定、更合规，优先考虑
3. **数据是否只在网页上？** 爬虫是最后手段，需评估法律风险和伦理合规
4. **数据是否在非结构化文本中？** 需要NLP提取，额外考虑提取精度
5. **现有数据源都不满足？** 考虑问卷或实验，但注意成本与时间约束

### API数据获取

API（Application Programming Interface）是最规范的数据获取方式。社科研究常用的API：

**国际组织数据API：**

```python
import requests
import pandas as pd

def fetch_world_bank_data(indicator, country="CHN", date_range="2010:2023"):
    url = "http://api.worldbank.org/v2/country/{}/indicator/{}".format(
        country, indicator
    )
    params = {
        "format": "json",
        "date": date_range,
        "per_page": 500
    }
    response = requests.get(url, params=params)
    data = response.json()
    if len(data) < 2:
        return pd.DataFrame()
    records = data[1]
    df = pd.DataFrame(records)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_numeric(df["date"])
    return df[["date", "value"]].rename(columns={
        "date": "year",
        "value": indicator
    }).dropna()

gdp_data = fetch_world_bank_data("NY.GDP.MKTP.KD.ZG")
```

**国内数据API的注意事项：**
- 统计年鉴数据通常无官方API，需要通过网页提取或购买数据库权限
- CEIC、Wind等商业数据库提供API但需订阅
- 部分政府开放数据平台提供API（如data.gov.cn），但覆盖范围有限

### 网络爬虫的伦理与法律边界

爬虫在社科数据采集中有重要价值，但必须在法律和伦理框架内使用：

**法律红线：**
- 不得突破反爬技术措施（违反《计算机信息网络国际联网安全保护管理办法》）
- 不得采集个人敏感信息（违反《个人信息保护法》）
- 不得对目标网站造成实质性负担（高频请求可能构成非法侵入计算机信息系统罪）
- 遵守网站的robots.txt协议

**伦理原则：**
- 数据仅用于学术研究，不得商用或转售
- 涉及个人数据时应做脱敏处理
- 在论文中如实说明数据采集方式
- 评估数据代表性，明确采集偏差

**合规爬虫实践：**

```python
import time
import requests
from bs4 import BeautifulSoup

def crawl_with_ethics(url_list, delay=2):
    results = []
    for url in url_list:
        try:
            headers = {
                "User-Agent": "AcademicResearchBot/1.0 (contact: your@email.edu)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                results.append(soup)
            time.sleep(delay)
        except Exception as e:
            print("Error fetching {}: {}".format(url, e))
            continue
    return results
```

### NLP文本提取

政策文件、新闻报道等非结构化文本是社科研究的重要数据源：

**PDF文本提取：**

```python
import pdfplumber

def extract_policy_text(pdf_path):
    text_blocks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_blocks.append(text)
    full_text = "\n".join(text_blocks)
    return full_text

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)
    return tables
```

**LLM辅助结构化提取：**

```python
def extract_policy_metadata(text, llm_client):
    prompt = """从以下政策文本中提取结构化信息，以JSON格式输出：
{
    "title": "政策标题",
    "issuing_authority": "发文机关",
    "issue_date": "发文日期(YYYY-MM-DD)",
    "policy_type": "政策类型(法规/规划/通知/意见/办法)",
    "key_topics": ["主题1", "主题2"],
    "target_entities": ["适用对象1", "适用对象2"]
}

政策文本：
{}""".format(text[:3000])

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

### 数据代表性评估

采集到数据后，必须评估其代表性，这是"做对"研究的关键：

**评估维度：**

1. **时间代表性**：数据是否覆盖研究所需的时间范围？是否存在断点？
2. **空间代表性**：数据是否覆盖目标地理范围？是否有地区遗漏？
3. **群体代表性**：样本是否代表目标总体？是否存在选择偏差？
4. **变量完整性**：关键变量是否有缺失？缺失是随机的还是有模式的？

```python
def assess_data_representativeness(df, target_population_info):
    report = {}
    report["total_observations"] = len(df)
    report["missing_rate"] = df.isnull().mean().to_dict()
    report["time_coverage"] = {
        "start": df.index.min() if hasattr(df.index, "min") else None,
        "end": df.index.max() if hasattr(df.index, "max") else None,
        "gaps": None
    }
    for col in df.select_dtypes(include="number").columns:
        report["{}_stats".format(col)] = {
            "mean": df[col].mean(),
            "std": df[col].std(),
            "min": df[col].min(),
            "max": df[col].max()
        }
    return report
```

## 关键细节与易错点

- **易错：先选方法再想需求**。常见错误是"我会爬虫所以用爬虫"，而非"我需要什么数据所以用什么方法"。正确顺序永远是：研究问题→数据需求→采集方法
- **易错：忽视数据代表性偏差**。从社交媒体爬取的数据不代表总体人口——使用微博数据的论文不能声称结论适用于"中国网民"，更不能适用于"中国公众"。必须在论文中明确数据代表性边界
- **易错：低估数据清洗工作量**。实际数据采集项目中，清洗往往占60%-80%的工作量。API数据可能有字段不一致，爬虫数据可能有编码混乱，PDF提取可能有乱码。预留足够的清洗时间
- **易错：忽略API的调用限制**。世界银行API单次返回最多500条记录，需要分页；某些API有每日调用上限。在项目规划时就要计算总调用次数和所需时间
- **易错：爬虫不设延迟**。不设延迟的爬虫不仅不道德，还可能触发封禁导致数据采集中断。学术爬虫建议间隔至少1-3秒

## 社科科研示例

**场景**：一位社会学博士生研究"城市住房政策对居民定居意愿的影响"，需要采集三类数据：城市住房政策文本、城市统计指标、居民调查数据。

**数据采集方案设计：**

```python
class HousingPolicyDataCollector:
    def __init__(self, config):
        self.config = config
        self.collected = {}

    def collect_policy_texts(self, city_list):
        policy_texts = []
        for city in city_list:
            gov_url = self.config["gov_urls"].get(city)
            if not gov_url:
                continue
            pages = self._search_policy_pages(gov_url, "住房 保障 租赁")
            for page_url in pages:
                text = self._extract_page_text(page_url)
                metadata = extract_policy_metadata(text, self.llm_client)
                policy_texts.append({
                    "city": city,
                    "url": page_url,
                    "text": text,
                    "metadata": metadata
                })
                time.sleep(2)
        self.collected["policy_texts"] = policy_texts
        return policy_texts

    def collect_city_statistics(self, city_list, indicators):
        stats_data = []
        for city in city_list:
            for indicator in indicators:
                data = fetch_world_bank_data(indicator, country="CHN")
                stats_data.append(data)
                time.sleep(0.5)
        self.collected["city_stats"] = stats_data
        return stats_data

    def assess_coverage(self):
        expected_cities = len(self.config["city_list"])
        cities_with_policy = len(set(
            p["city"] for p in self.collected.get("policy_texts", [])
        ))
        coverage_rate = cities_with_policy / expected_cities
        print("政策文本覆盖率: {:.1%}".format(coverage_rate))
        if coverage_rate < 0.8:
            print("警告：覆盖率低于80%，需补充数据源或调整研究范围")
        return coverage_rate
```

**关键决策记录：**
- 政策文本选择爬虫而非手动收集：70+城市×年均5条政策=350+条，手动不可行
- 统计指标优先API：确保可复现性，且数据格式统一
- 居民调查使用CFPS公开数据：自行调查成本过高，CFPS有住房相关变量且代表性有保障
- 对比了三个数据源后，明确标注每个变量的数据来源和已知局限

## 拓展学习

- 《Web Data Collection for Social Scientists》——系统讲解社科研究中的网络数据采集方法论
- Python的`requests`+`BeautifulSoup`官方文档——爬虫技术基础
- 《数字时代的调查方法》——讨论传统调查与数字数据采集的融合
- APISecretary等API聚合平台——快速发现可用的数据API
- 国家统计局开放数据平台——国内宏观经济与人口数据的权威来源

## 参考链接

- https://data.worldbank.org/indicator — 世界银行开放数据API文档
- https://data.stats.gov.cn/ — 国家统计局数据平台
- https://www.icpsr.umich.edu/ — ICPSR社科数据仓储
- https://developers.google.com/search/docs/crawling-indexing/robots/intro — robots.txt协议规范
- https://www.personalinformationprotection.cn/ — 中国个人信息保护法解读
