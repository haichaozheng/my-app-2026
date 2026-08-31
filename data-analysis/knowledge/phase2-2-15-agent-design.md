# Agent设计产品智能功能

> **引入时机**：W8 | **核心挑战**："如何让产品自动执行任务？" | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

你的产品已经能展示数据、回答问题，但还缺少一个关键能力——自动执行任务。用户不想每天手动打开应用查看股票是否异常，他们希望产品能自动监控、检测异常、生成提醒。Agent（智能体）就是让产品从"被动工具"变成"主动助手"的关键——它能够感知环境、制定计划、执行动作、反思结果，像一个虚拟分析师一样自主工作。

在金融数据产品中，Agent的应用场景非常广泛：市场监控Agent自动扫描异动、风险预警Agent检测组合风险、研报Agent自动摘要生成。理解Agent的设计原理，你就能让你的产品从"人找数据"进化为"数据找人"。

## 这个知识点的核心内容

### Agent架构

Agent的核心是感知→规划→行动→反思的循环：

**感知（Perception）**
- 接收外部输入：用户指令、定时触发、数据变化
- 收集环境信息：市场数据、持仓状态、新闻事件

**规划（Planning）**
- 分解任务：将复杂目标拆分为可执行的子任务
- 选择工具：决定使用哪个工具完成子任务
- 制定步骤：确定执行顺序和条件

**行动（Action）**
- 调用工具：执行API调用、数据查询、发送通知
- 交互环境：更新状态、记录结果

**反思（Reflection）**
- 评估结果：行动是否达成了目标？
- 调整策略：如果未达成，应该如何修改计划？
- 积累经验：将成功/失败的模式存储为经验

```python
class Agent:
    def __init__(self, llm_client, tools):
        self.client = llm_client
        self.tools = tools
        self.memory = []

    def run(self, task):
        # 感知
        context = self.perceive(task)

        # 规划
        plan = self.plan(task, context)

        # 行动
        results = []
        for step in plan:
            result = self.act(step)
            results.append(result)

            # 反思
            if not self.reflect(step, result):
                plan = self.replan(task, results)

        return results

    def perceive(self, task):
        return {"task": task, "memory": self.memory}

    def plan(self, task, context):
        prompt = f"任务：{task}\n可用工具：{list(self.tools.keys())}\n请制定执行计划。"
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return self.parse_plan(response.choices[0].message.content)

    def act(self, step):
        tool_name = step["tool"]
        tool_input = step["input"]
        return self.tools[tool_name](**tool_input)

    def reflect(self, step, result):
        return result.get("success", True)
```

### 工具使用（Tool Use）

Agent的能力边界由可用工具决定。为金融Agent设计工具：

```python
def get_stock_price(code: str) -> dict:
    """获取股票最新价格和涨跌幅"""
    import akshare as ak
    df = ak.stock_zh_a_spot_em()
    row = df[df["代码"] == code].iloc[0]
    return {
        "code": code,
        "name": row["名称"],
        "price": float(row["最新价"]),
        "change_pct": float(row["涨跌幅"]),
        "volume": float(row["成交量"])
    }

def get_stock_history(code: str, days: int = 20) -> dict:
    """获取股票历史数据"""
    import akshare as ak
    import pandas as pd
    end = pd.Timestamp.now().strftime("%Y%m%d")
    start = (pd.Timestamp.now() - pd.Timedelta(days=days)).strftime("%Y%m%d")
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                            start_date=start, end_date=end, adjust="hfq")
    return {
        "code": code,
        "avg_price": df["收盘"].mean(),
        "max_price": df["收盘"].max(),
        "min_price": df["收盘"].min(),
        "volatility": df["收盘"].pct_change().std() * (252**0.5)
    }

def check_anomaly(code: str) -> dict:
    """检测股票异常"""
    data = get_stock_history(code, days=20)
    price = get_stock_price(code)
    is_anomaly = abs(price["change_pct"]) > 3  # 涨跌超3%
    return {
        "is_anomaly": is_anomaly,
        "reason": f"今日涨跌幅{price['change_pct']:.2f}%，" +
                  (f"超过3%阈值" if is_anomaly else "在正常范围"),
        "price": price["price"],
        "change_pct": price["change_pct"]
    }

def send_alert(message: str) -> dict:
    """发送预警通知"""
    print(f"[ALERT] {message}")
    return {"success": True, "message": "通知已发送"}

# 工具注册
TOOLS = {
    "get_stock_price": {"func": get_stock_price, "desc": "获取股票最新价格"},
    "get_stock_history": {"func": get_stock_history, "desc": "获取股票历史数据"},
    "check_anomaly": {"func": check_anomaly, "desc": "检测股票异常"},
    "send_alert": {"func": send_alert, "desc": "发送预警通知"}
}
```

### Agent框架选择

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| LangChain Agent | 生态最全，组件丰富 | 复杂多步骤Agent |
| AutoGen | 多Agent协作 | 需要多角色协作的场景 |
| CrewAI | 角色化Agent | 模拟团队协作 |
| 自研 | 完全可控 | 简单场景，学习目的 |

教学推荐：先自研理解原理，再用LangChain提效。

### 市场监控Agent设计

以市场监控Agent为例，展示完整的Agent设计：

```python
from openai import OpenAI
import json

class MarketMonitorAgent:
    def __init__(self, api_key, base_url="https://api.deepseek.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.portfolio = ["601398", "600036", "601166"]
        self.tools = {
            "get_stock_price": get_stock_price,
            "check_anomaly": check_anomaly,
            "send_alert": send_alert
        }

    def monitor(self):
        """执行一次市场监控"""
        anomalies = []

        # Step 1: 检查组合中每只股票
        for code in self.portfolio:
            result = check_anomaly(code)
            if result["is_anomaly"]:
                anomalies.append(result)

        # Step 2: 如果有异常，让LLM分析
        if anomalies:
            analysis = self.analyze_anomalies(anomalies)
            send_alert(analysis)
            return analysis
        else:
            return "市场正常，组合内股票无异常波动。"

    def analyze_anomalies(self, anomalies):
        """让LLM分析异常原因并给出建议"""
        anomaly_text = "\n".join(
            f"- {a['price']}（涨跌幅{a['change_pct']:.2f}%）: {a['reason']}"
            for a in anomalies
        )

        prompt = f"""你是市场监控分析师。以下股票出现异常波动：

{anomaly_text}

请分析：
1. 可能的原因（政策/行业/个股）
2. 对投资组合的影响
3. 建议的行动

回答控制在200字以内。"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content

    def daily_report(self):
        """生成每日市场报告"""
        report_lines = ["📊 每日市场监控报告\n"]

        for code in self.portfolio:
            data = get_stock_price(code)
            report_lines.append(
                f"- {data['name']}({code}): "
                f"收盘{data['price']:.2f}, "
                f"涨跌{data['change_pct']:+.2f}%"
            )

        anomalies = [code for code in self.portfolio
                     if check_anomaly(code)["is_anomaly"]]

        if anomalies:
            report_lines.append(f"\n⚠️ 异常股票: {', '.join(anomalies)}")
        else:
            report_lines.append("\n✅ 组合内无异常")

        return "\n".join(report_lines)
```

### Agent的局限与安全

- **幻觉**：Agent可能编造不存在的工具调用结果
- **无限循环**：Agent可能陷入规划-行动的死循环，需设置最大步数
- **权限控制**：Agent不应有删除数据、发送资金的权限
- **成本控制**：每次Agent循环都消耗Token，需设置成本上限
- **人类监督**：关键决策前应请求人类确认（Human-in-the-loop）

## 关键细节与易错点

- **误区：Agent能自主解决一切问题**。Agent的能力受限于工具和LLM的推理能力，复杂任务仍需人类监督
- **误区：Agent不需要记忆**。没有记忆的Agent每次都从零开始，效率低且无法积累经验
- **易错：工具描述不清晰**。LLM根据工具描述选择工具，描述不清会导致选错工具
- **易错：不限制Agent步数**。Agent可能反复尝试失败的操作，必须设置max_steps
- **易错：Agent直接执行危险操作**。发送交易指令、删除数据等操作必须有人类确认环节

## 金融数据分析示例

市场监控Agent：检查组合→检测异常→生成预警

```python
import streamlit as st
from openai import OpenAI
import akshare as ak
import pandas as pd

st.set_page_config(page_title="银行股监控Agent", page_icon="🤖")
st.title("🤖 银行股智能监控Agent")

# 配置
PORTFOLIO = ["601398", "600036", "601166"]
PORTFOLIO_NAMES = {"601398": "工商银行", "600036": "招商银行", "601166": "兴业银行"}

@st.cache_data(ttl=300)
def get_realtime_data():
    df = ak.stock_zh_a_spot_em()
    result = {}
    for code in PORTFOLIO:
        row = df[df["代码"] == code].iloc[0]
        result[code] = {
            "name": row["名称"],
            "price": float(row["最新价"]),
            "change_pct": float(row["涨跌幅"]),
            "volume": float(row["成交量"]),
            "turnover": float(row["换手率"])
        }
    return result

# 手动触发监控
if st.button("🔍 执行市场监控", type="primary"):
    with st.spinner("Agent正在执行监控..."):
        data = get_realtime_data()

        # Step 1: 展示组合状态
        st.subheader("组合状态")
        for code, info in data.items():
            icon = "🔴" if info["change_pct"] < -2 else "🟢" if info["change_pct"] > 2 else "⚪"
            st.write(f"{icon} **{info['name']}** ({code}): "
                     f"{info['price']:.2f} ({info['change_pct']:+.2f}%)")

        # Step 2: 检测异常
        anomalies = {code: info for code, info in data.items()
                     if abs(info["change_pct"]) > 2}

        if anomalies:
            st.subheader("⚠️ 异常检测")
            for code, info in anomalies.items():
                st.warning(f"{info['name']} 涨跌幅 {info['change_pct']:+.2f}%，超过2%阈值")

            # Step 3: AI分析异常原因
            st.subheader("🤖 AI分析")
            anomaly_desc = "\n".join(
                f"- {info['name']}: {info['price']:.2f}元, 涨跌幅{info['change_pct']:+.2f}%, "
                f"换手率{info['turnover']:.2f}%"
                for info in anomalies.values()
            )

            client = OpenAI(
                api_key=st.secrets["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com"
            )

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user",
                    "content": f"""你是A股银行板块分析专家。以下银行股出现异常波动：

{anomaly_desc}

请简要分析：
1. 可能的原因（政策面/资金面/基本面）
2. 对银行板块整体的影响
3. 投资者应关注的要点

控制在150字以内。"""
                }],
                temperature=0.3,
                max_tokens=300
            )
            st.info(response.choices[0].message.content)
        else:
            st.success("✅ 组合内股票表现正常，无异常波动。")

# 每日报告
if st.button("📋 生成每日报告"):
    data = get_realtime_data()
    report = "📊 **银行股每日监控报告**\n\n"
    for code, info in data.items():
        report += f"- {info['name']}({code}): {info['price']:.2f} ({info['change_pct']:+.2f}%)\n"
    st.markdown(report)
```

## 拓展学习

- LangChain Agent文档——最成熟的Agent框架
- AutoGen多Agent框架——微软开源的多Agent协作框架
- 《Building LLM Apps》Agent章节——Agent设计的实战指南
- ReAct论文——Agent"推理+行动"范式的原始论文
- OpenAI Function Calling——理解Agent工具调用的底层机制

## 参考链接

- https://python.langchain.com/docs/modules/agents/ — LangChain Agent文档
- https://microsoft.github.io/autogen/stable/ — AutoGen多Agent框架
- https://arxiv.org/abs/2210.03629 — ReAct论文：Agent的推理与行动范式
- https://platform.openai.com/docs/guides/function-calling — OpenAI Function Calling文档
