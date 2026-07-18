# Skill封装数据采集能力

> **引入时机**：W5 | **核心挑战**："如何把常用的数据采集流程封装为可复用Skill？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

在W5的数据采集实践中，你会发现一个规律：很多数据采集操作是重复的——每次分析都要重新写API调用代码、每次爬虫都要重新处理编码和延迟逻辑、每次文本提取都要重新设定解析规则。如果你把这些流程每篇文章都重新写一遍，不仅浪费时间，更严重的是：细微的参数差异可能导致数据不一致，破坏研究的可复现性。

没有Skill封装，你会陷入"复制粘贴式编程"——从上一个项目复制代码，改几个参数，遇到新的边界情况再打补丁。随着项目推进，你的数据采集代码变成一个难以维护的补丁集合，任何修改都可能引入隐蔽的bug。

将数据采集流程封装为Skill后，你获得三重收益：一是复用性——一次封装，多个项目使用；二是一致性——同一Skill产生的数据格式和标准统一；三是可审查性——数据采集的逻辑边界和参数都明确记录在Skill定义中，方便方法论审查和论文方法部分写作。

## 这个知识点的核心内容

### Skill封装的设计原则

Skill是AI工具栈中的可复用能力单元，数据采集Skill的设计遵循以下原则：

**输入/输出/边界三要素：**

| 要素 | 说明 | 示例 |
|------|------|------|
| 输入 | Skill接收的参数，包括必选和可选 | API名称、时间范围、国家代码 |
| 输出 | Skill产出的数据和元信息 | DataFrame + 采集日志 |
| 边界 | Skill的能力范围和限制 | 最大调用次数、支持的数据源、异常处理 |

**设计原则：**

1. **单一职责**：一个Skill只做一类数据采集，不混合API调用和爬虫
2. **参数化**：所有可能变化的配置都作为参数，不在Skill内硬编码
3. **幂等性**：相同参数多次调用应产生相同结果（或明确说明非幂等场景）
4. **可观测**：每次执行记录采集日志，包括时间、参数、结果摘要
5. **优雅失败**：遇到异常不崩溃，记录错误信息并返回部分结果

### 数据采集Skill示例

**API数据获取Skill：**

```yaml
name: world_bank_data_collector
description: 从世界银行API获取宏观经济指标数据
triggers:
  - 获取世界银行数据
  - WB数据
  - 宏观经济指标
parameters:
  required:
    - indicator: 世界银行指标代码
    - country: 国家代码，ISO2格式
  optional:
    - start_year: 起始年份，默认2010
    - end_year: 结束年份，默认2023
    - output_format: 输出格式，csv或dataframe，默认dataframe
output:
  type: dataframe
  columns: [year, indicator_value]
  metadata:
    - collection_timestamp
    - api_response_code
    - data_points_count
limits:
  max_retries: 3
  request_delay_seconds: 0.5
```

```python
import requests
import pandas as pd
import time
from datetime import datetime

def execute(indicator, country, start_year=2010, end_year=2023,
            output_format="dataframe"):
    url = "http://api.worldbank.org/v2/country/{}/indicator/{}".format(
        country, indicator
    )
    all_records = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        params = {
            "format": "json",
            "date": "{}:{}".format(start_year, end_year),
            "per_page": 500,
            "page": page
        }
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "metadata": {
                    "collection_timestamp": datetime.now().isoformat(),
                    "indicator": indicator,
                    "country": country
                }
            }

        if len(data) < 2 or data[1] is None:
            break

        total_pages = data[0].get("pages", 1)
        all_records.extend(data[1])
        page += 1
        time.sleep(0.5)

    df = pd.DataFrame(all_records)
    if df.empty:
        return {
            "success": True,
            "data": pd.DataFrame(columns=["year", "indicator_value"]),
            "metadata": {
                "collection_timestamp": datetime.now().isoformat(),
                "indicator": indicator,
                "country": country,
                "data_points_count": 0
            }
        }

    df = df[["date", "value"]].copy()
    df.columns = ["year", "indicator_value"]
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["indicator_value"] = pd.to_numeric(df["indicator_value"], errors="coerce")
    df = df.dropna().sort_values("year").reset_index(drop=True)

    if output_format == "csv":
        df.to_csv("wb_{}_{}.csv".format(indicator, country), index=False)

    return {
        "success": True,
        "data": df,
        "metadata": {
            "collection_timestamp": datetime.now().isoformat(),
            "indicator": indicator,
            "country": country,
            "data_points_count": len(df),
            "api_response_code": 200
        }
    }
```

**网页数据提取Skill：**

```yaml
name: gov_policy_extractor
description: 从政府网站提取政策文本并结构化
triggers:
  - 提取政策文本
  - 政府政策采集
  - 政策文件提取
parameters:
  required:
    - base_url: 目标政府网站基础URL
    - keywords: 搜索关键词列表
  optional:
    - max_pages: 最大采集页数，默认10
    - delay_seconds: 请求间隔秒数，默认2
    - date_from: 起始日期，默认无限制
output:
  type: list[dict]
  fields: [title, url, publish_date, full_text, metadata]
limits:
  max_pages: 50
  delay_seconds: 2
```

```python
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

def execute(base_url, keywords, max_pages=10, delay_seconds=2, date_from=None):
    results = []
    headers = {
        "User-Agent": "AcademicResearchBot/1.0"
    }

    for page_num in range(1, max_pages + 1):
        search_url = "{}/search?page={}&keyword={}".format(
            base_url, page_num, "+".join(keywords)
        )
        try:
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
        except Exception as e:
            print("Page {} failed: {}".format(page_num, e))
            break

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".search-result-item")

        if not items:
            break

        for item in items:
            record = _extract_item(item, base_url, headers)
            if record:
                if date_from and record.get("publish_date"):
                    if record["publish_date"] < date_from:
                        continue
                results.append(record)

        time.sleep(delay_seconds)

    return {
        "success": True,
        "data": results,
        "metadata": {
            "collection_timestamp": datetime.now().isoformat(),
            "total_records": len(results),
            "keywords": keywords,
            "source_url": base_url
        }
    }

def _extract_item(item, base_url, headers):
    title_elem = item.select_one(".title a")
    if not title_elem:
        return None
    title = title_elem.get_text(strip=True)
    detail_url = base_url + title_elem.get("href", "")
    date_elem = item.select_one(".date")
    publish_date = date_elem.get_text(strip=True) if date_elem else None

    try:
        detail_resp = requests.get(detail_url, headers=headers, timeout=10)
        detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
        content_elem = detail_soup.select_one(".article-content")
        full_text = content_elem.get_text(strip=True) if content_elem else ""
    except Exception:
        full_text = ""

    time.sleep(1)
    return {
        "title": title,
        "url": detail_url,
        "publish_date": publish_date,
        "full_text": full_text,
        "metadata": {"source": base_url}
    }
```

### Skill的参数化与复用

参数化是Skill复用的关键。设计参数时应区分"必选"与"可选"，可选参数提供合理默认值：

```python
SKILL_REGISTRY = {
    "world_bank_data_collector": {
        "required_params": ["indicator", "country"],
        "optional_params": {
            "start_year": 2010,
            "end_year": 2023,
            "output_format": "dataframe"
        }
    },
    "gov_policy_extractor": {
        "required_params": ["base_url", "keywords"],
        "optional_params": {
            "max_pages": 10,
            "delay_seconds": 2,
            "date_from": None
        }
    }
}

def validate_params(skill_name, user_params):
    spec = SKILL_REGISTRY[skill_name]
    for req in spec["required_params"]:
        if req not in user_params:
            raise ValueError("缺少必选参数: {}".format(req))
    merged = dict(spec["optional_params"])
    merged.update(user_params)
    return merged
```

### Skill的测试与维护

数据采集Skill必须经过系统测试，确保在目标网站或API变更时能及时发现：

```python
def test_world_bank_collector():
    result = execute(
        indicator="NY.GDP.MKTP.KD.ZG",
        country="CHN",
        start_year=2020,
        end_year=2023
    )
    assert result["success"] is True
    assert result["metadata"]["data_points_count"] > 0
    df = result["data"]
    assert "year" in df.columns
    assert "indicator_value" in df.columns
    assert df["year"].min() >= 2020
    assert df["year"].max() <= 2023
    print("世界银行数据采集Skill测试通过")

def test_skill_idempotency():
    r1 = execute(indicator="SP.POP.TOTL", country="CHN",
                 start_year=2022, end_year=2022)
    r2 = execute(indicator="SP.POP.TOTL", country="CHN",
                 start_year=2022, end_year=2022)
    assert r1["data"].equals(r2["data"])
    print("幂等性测试通过")
```

**维护策略：**
- 每月运行一次回归测试，检测API/网站变更
- 记录每次执行的日志，统计成功率
- 当目标网站结构变更时，更新Skill的CSS选择器或解析逻辑

## 关键细节与易错点

- **易错：Skill内硬编码参数**。将API密钥、文件路径、特定国家的参数硬编码在Skill中，导致其他项目无法复用。所有项目相关的配置都应通过参数传入
- **易错：忽略异常处理**。API可能超时、网站可能宕机、数据格式可能不符预期。Skill必须在每个可能失败的环节做异常处理，返回结构化的错误信息而非抛出未捕获的异常
- **易错：Skill粒度过大**。一个Skill同时做"搜索→提取→清洗→存储"，任何一个环节变更都需要修改整个Skill。应按单一职责拆分为多个Skill，通过链式调用组合
- **易错：不记录采集元数据**。缺少采集时间、API版本、参数快照等元数据，论文方法部分无法完整描述数据来源。每个Skill都应返回metadata字段
- **易错：测试用例覆盖不足**。只测试正常路径，不测试网络异常、空数据、格式变更等边界情况。数据采集Skill至少需要正常路径测试、异常路径测试和幂等性测试

## 社科科研示例

**场景**：一位政治学博士生研究"中国地方政府信息公开的影响因素"，需要从31个省级政府网站采集信息公开年度报告。

**Skill封装方案：**

```python
PROVINCE_CONFIG = {
    "beijing": {"url": "http://www.beijing.gov.cn", "search_path": "/search"},
    "shanghai": {"url": "http://www.shanghai.gov.cn", "search_path": "/search"},
}

def collect_transparency_reports(provinces=None, year_range=None):
    if provinces is None:
        provinces = list(PROVINCE_CONFIG.keys())

    all_reports = []
    collection_log = []

    for province in provinces:
        config = PROVINCE_CONFIG.get(province)
        if not config:
            collection_log.append({
                "province": province,
                "status": "config_not_found"
            })
            continue

        result = gov_policy_extractor_execute(
            base_url=config["url"],
            keywords=["信息公开", "年度报告"],
            max_pages=5,
            date_from=year_range[0] if year_range else None
        )

        if result["success"]:
            for record in result["data"]:
                record["province"] = province
                all_reports.append(record)
            collection_log.append({
                "province": province,
                "status": "success",
                "count": len(result["data"])
            })
        else:
            collection_log.append({
                "province": province,
                "status": "failed",
                "error": result.get("error", "unknown")
            })

    return {
        "reports": all_reports,
        "log": collection_log,
        "summary": {
            "total_provinces": len(provinces),
            "success_count": sum(
                1 for l in collection_log if l["status"] == "success"
            ),
            "total_reports": len(all_reports)
        }
    }
```

**论文方法部分可直接引用：** "省级政府信息公开年度报告通过自建Skill从各省市政府网站采集，采集时间2025年X月X日，共覆盖31个省份，其中X个省份采集成功（成功率X%），采集参数为：关键词'信息公开''年度报告'，每页请求间隔2秒。"

## 拓展学习

- opencode Skill开发文档——Skill定义规范与最佳实践
- 《API Design Principles》——API设计原则适用于Skill接口设计
- Scrapy框架文档——复杂爬虫场景的专业框架
- 《Building Data Pipelines》——数据管道设计方法论
- Apache Airflow——大规模数据采集流程编排工具

## 参考链接

- https://docs.python-requests.org/ — requests库文档
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/ — BeautifulSoup文档
- https://github.com/jsvine/pdfplumber — pdfplumber PDF提取库
- https://api.worldbank.org/v2/doc — 世界银行API文档
- https://scrapy.org/ — Scrapy爬虫框架
