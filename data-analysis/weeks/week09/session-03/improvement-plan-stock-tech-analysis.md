# Skill Improvement Plan: stock-tech-analysis

## 评估总结

**当前质量评分**: 72/100 (C+)

**评估维度**:
- Description Quality: 65/100
- Content Organization: 75/100
- Writing Style: 70/100
- Structural Integrity: 80/100

## Priority Summary
- **High Priority**: 3 items
- **Medium Priority**: 2 items
- **Low Priority**: 2 items

---

## High Priority Improvements

### 1. 增强 Description 触发词覆盖
**File**: SKILL.md:3:4
**Dimension**: Description Quality
**Impact**: +15 points

**Current**:
```yaml
---
name: stock-tech-analysis
description: |
  计算股票技术指标（均线、MACD、RSI）并生成可视化图表。当用户提到股票技术分析、技术指标计算、均线分析、MACD、RSI、K线图、股票图表、技术面分析时使用此技能。适用于个股或指数的技术面研究，支持A股市场。
---
```

**Suggested**:
```yaml
---
name: stock-tech-analysis
description: |
  计算股票技术指标（均线、MACD、RSI）并生成可视化图表。当用户提到股票技术分析、技术指标计算、均线分析、MACD、RSI、K线图、股票图表、技术面分析、个股走势、趋势判断、支撑压力、买卖信号、超买超卖时使用此技能。适用于个股或指数的技术面研究，支持A股和港股市场。即使用户没有明确要求生成图表，只要涉及股票技术面分析，都应使用此技能。
---
```

**Reason**: 扩展触发词覆盖范围，增加更多技术分析相关术语，提高技能触发率。明确支持港股市场。

### 2. 添加港股数据获取说明
**File**: SKILL.md:25:35
**Dimension**: Content Organization
**Impact**: +12 points

**Current**:
```
优先使用 **tushare MCP** 获取日K线数据：
...
**回退方案**：若 MCP 不可用，使用 tushare skill 获取数据。
```

**Suggested**:
```
优先使用 **tushare MCP** 获取日K线数据：

**A股数据获取**:
- 接口: tushareMcp_daily
- 参数: ts_code (如 600519.SH), start_date, end_date, fields

**港股数据获取**:
- 接口: tushareMcp_hk_daily
- 参数: ts_code (如 01810.HK), start_date, end_date

**回退方案**: 若 MCP 不可用，使用 tushare skill 获取数据。
```

**Reason**: 当前文档仅提及A股数据获取，需要补充港股数据获取方法，使技能支持更全面。

### 3. 添加技术面解读模板
**File**: SKILL.md:109:115
**Dimension**: Writing Style
**Impact**: +10 points

**Current**:
```
### 文字解读
图表生成后，应提供简要技术面解读：
- 当前价格与均线关系（多头/空头排列）
- MACD金叉/死叉信号
- RSI超买/超卖状态
- 综合技术面判断
```

**Suggested**:
```
### 技术面解读模板

图表生成后，按以下结构提供解读：

**1. 均线分析**
- 当前价格: XX.XX
- MA5: XX.XX | MA10: XX.XX | MA20: XX.XX
- 均线排列: [多头排列/空头排列/纠缠]
- 信号: [看多/看空/中性]

**2. MACD分析**
- DIF: XX.XX | DEA: XX.XX | MACD柱: XX.XX
- 信号: [金叉/死叉/粘合]
- 趋势: [上涨动能增强/减弱/下跌动能增强/减弱]

**3. RSI分析**
- RSI(14): XX.XX
- 状态: [超买(>70)/中性(30-70)/超卖(<30)]

**4. 综合判断**
- 技术面评级: [强势/偏强/中性/偏弱/弱势]
- 建议操作: [买入/持有/观望/减仓/卖出]
- 关键支撑: XX.XX | 关键压力: XX.XX
```

**Reason**: 提供结构化的解读模板，确保输出一致且专业。

---

## Medium Priority Improvements

### 4. 添加异常处理说明
**File**: SKILL.md
**Dimension**: Content Organization
**Impact**: +8 points

**Suggested Addition** (在"注意事项"之后):
```
## 异常处理

### 数据获取失败
- 检查股票代码格式是否正确（A股: XXXXXX.SH/SZ, 港股: XXXXX.HK）
- 确认日期范围是否有效（start_date < end_date）
- 验证网络连接是否正常

### 指标计算异常
- 确保数据量足够（至少60个交易日）
- 检查数据中是否存在空值或异常值
- 验证close列数据类型为数值型

### 图表生成失败
- 确认matplotlib已安装（pip install matplotlib）
- 检查中文字体配置
- 验证输出路径可写
```

**Reason**: 完善异常处理说明，提高技能的健壮性。

### 5. 添加更多使用示例
**File**: SKILL.md
**Dimension**: Content Organization
**Impact**: +5 points

**Suggested Addition**:
```
### 示例3：指数分析

**用户输入**：
```
分析上证指数的技术走势
```

**执行步骤**：
1. 调用 `tushareMcp_index_daily` 获取 000001.SH 近3个月日K线
2. 运行 `scripts/indicators.py` 计算指标
3. 运行 `scripts/generate_chart.py` 生成图表
4. 给出指数技术面解读

### 示例4：特定时间段分析

**用户输入**：
```
帮我看看比亚迪最近一个月的MACD变化
```

**执行步骤**：
1. 获取002594.SZ近1个月日K线数据
2. 计算技术指标
3. 生成图表（重点展示MACD）
4. 解读MACD变化趋势
```

**Reason**: 丰富使用场景，帮助用户更好理解技能功能。

---

## Low Priority Improvements

### 6. 添加references目录文档
**File**: references/technical-indicators.md (new file)
**Dimension**: Structural Integrity
**Impact**: +5 points

**Suggested Content**:
```markdown
# 技术指标详解

## 移动平均线 (MA)

### 计算公式
MA(n) = (C1 + C2 + ... + Cn) / n

### 应用场景
- 短期MA上穿长期MA → 金叉（看多信号）
- 短期MA下穿长期MA → 死叉（看空信号）
- 价格在MA上方运行 → 多头趋势
- 价格在MA下方运行 → 空头趋势

## MACD

### 计算公式
- DIF = EMA(12) - EMA(26)
- DEA = DIF的EMA(9)
- MACD柱 = (DIF - DEA) * 2

### 应用场景
- DIF上穿DEA → 金叉（买入信号）
- DIF下穿DEA → 死叉（卖出信号）
- MACD柱由负转正 → 动能转强
- MACD柱由正转负 → 动能转弱

## RSI

### 计算公式
RSI = 100 - 100/(1+RS)
RS = 平均上涨幅度 / 平均下跌幅度

### 应用场景
- RSI > 70 → 超买区域，可能回调
- RSI < 30 → 超卖区域，可能反弹
- RSI与价格背离 → 趋势可能反转
```

**Reason**: 提供技术指标的详细说明，作为参考资料。

### 7. 优化evals.json测试用例
**File**: evals/evals.json
**Dimension**: Structural Integrity
**Impact**: +3 points

**Suggested**:
```json
{
  "skill_name": "stock-tech-analysis",
  "evals": [
    {
      "id": 1,
      "prompt": "帮我分析贵州茅台（600519）最近3个月的技术走势",
      "expected_output": "生成包含MA5/MA10/MA20均线、MACD、RSI的PNG图表，并给出结构化技术面解读",
      "files": []
    },
    {
      "id": 2,
      "prompt": "计算比亚迪（002594.SZ）的技术指标，我要看MACD和RSI",
      "expected_output": "生成比亚迪的技术分析图表，包含MACD和RSI指标",
      "files": []
    },
    {
      "id": 3,
      "prompt": "对比宁德时代和比亚迪的技术面",
      "expected_output": "分别生成两只股票的技术分析图表，并进行技术面对比",
      "files": []
    },
    {
      "id": 4,
      "prompt": "小米集团最近跌得很厉害，帮我看看技术面有没有超卖",
      "expected_output": "生成01810.HK的技术分析图表，重点分析RSI指标，给出超卖判断",
      "files": []
    },
    {
      "id": 5,
      "prompt": "上证指数今天大涨，技术面转好了吗",
      "expected_output": "生成000001.SH的技术分析图表，分析均线、MACD、RSI，给出趋势判断",
      "files": []
    }
  ]
}
```

**Reason**: 增加港股和指数的测试用例，提高测试覆盖率。

---

## Estimated Time to Complete
- High Priority: 1 hour
- Medium Priority: 30 minutes
- Low Priority: 30 minutes
- **Total**: 2 hours

## Expected Score Improvement
- Current: 72/100 (C+)
- After High Priority: 85/100 (B)
- After All: 90/100 (A-)
