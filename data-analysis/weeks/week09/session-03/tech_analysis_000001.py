import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 数据准备 - 平安银行(000001.SZ)最近60天数据
data = [
    {"ts_code": "000001.SZ", "trade_date": "20260616", "open": 11.05, "high": 11.12, "low": 10.91, "close": 10.94, "pre_close": 11.06, "change": -0.12, "pct_chg": -1.085, "vol": 942708.04, "amount": 1034554.24938},
    {"ts_code": "000001.SZ", "trade_date": "20260615", "open": 11.21, "high": 11.21, "low": 10.98, "close": 11.06, "pre_close": 11.24, "change": -0.18, "pct_chg": -1.6014, "vol": 1541304.95, "amount": 1711561.28657},
    {"ts_code": "000001.SZ", "trade_date": "20260612", "open": 11.0, "high": 11.25, "low": 10.88, "close": 11.24, "pre_close": 10.94, "change": 0.3, "pct_chg": 2.7422, "vol": 2032355.46, "amount": 2263042.93057},
    {"ts_code": "000001.SZ", "trade_date": "20260611", "open": 11.32, "high": 11.39, "low": 11.25, "close": 11.3, "pre_close": 11.32, "change": -0.02, "pct_chg": -0.1767, "vol": 1156222.22, "amount": 1308133.97213},
    {"ts_code": "000001.SZ", "trade_date": "20260610", "open": 11.07, "high": 11.35, "low": 11.07, "close": 11.32, "pre_close": 11.13, "change": 0.19, "pct_chg": 1.7071, "vol": 1543176.39, "amount": 1738056.71203},
    {"ts_code": "000001.SZ", "trade_date": "20260609", "open": 11.01, "high": 11.19, "low": 10.96, "close": 11.13, "pre_close": 11.03, "change": 0.1, "pct_chg": 0.9066, "vol": 1149672.34, "amount": 1277122.41579},
    {"ts_code": "000001.SZ", "trade_date": "20260608", "open": 10.97, "high": 11.1, "low": 10.96, "close": 11.03, "pre_close": 10.98, "change": 0.05, "pct_chg": 0.4554, "vol": 1090926.46, "amount": 1203946.343},
    {"ts_code": "000001.SZ", "trade_date": "20260605", "open": 10.83, "high": 11.03, "low": 10.83, "close": 10.98, "pre_close": 10.82, "change": 0.16, "pct_chg": 1.4787, "vol": 1003503.34, "amount": 1102446.143},
    {"ts_code": "000001.SZ", "trade_date": "20260604", "open": 10.91, "high": 10.97, "low": 10.77, "close": 10.82, "pre_close": 10.99, "change": -0.17, "pct_chg": -1.5469, "vol": 869270.83, "amount": 943329.311},
    {"ts_code": "000001.SZ", "trade_date": "20260603", "open": 11.03, "high": 11.06, "low": 10.92, "close": 10.99, "pre_close": 11.08, "change": -0.09, "pct_chg": -0.8123, "vol": 825271.72, "amount": 906870.268},
    {"ts_code": "000001.SZ", "trade_date": "20260602", "open": 10.98, "high": 11.1, "low": 10.94, "close": 11.08, "pre_close": 10.99, "change": 0.09, "pct_chg": 0.8189, "vol": 885428.42, "amount": 978159.337},
    {"ts_code": "000001.SZ", "trade_date": "20260601", "open": 10.9, "high": 10.99, "low": 10.81, "close": 10.99, "pre_close": 10.93, "change": 0.06, "pct_chg": 0.5489, "vol": 954595.69, "amount": 1042306.456},
    {"ts_code": "000001.SZ", "trade_date": "20260529", "open": 10.65, "high": 10.93, "low": 10.62, "close": 10.93, "pre_close": 10.66, "change": 0.27, "pct_chg": 2.5328, "vol": 1399367.8, "amount": 1515692.068},
    {"ts_code": "000001.SZ", "trade_date": "20260528", "open": 10.76, "high": 10.79, "low": 10.63, "close": 10.66, "pre_close": 10.76, "change": -0.1, "pct_chg": -0.9294, "vol": 900711.07, "amount": 963695.781},
    {"ts_code": "000001.SZ", "trade_date": "20260527", "open": 10.76, "high": 10.85, "low": 10.72, "close": 10.76, "pre_close": 10.79, "change": -0.03, "pct_chg": -0.278, "vol": 839727.18, "amount": 905710.898},
    {"ts_code": "000001.SZ", "trade_date": "20260526", "open": 10.71, "high": 10.83, "low": 10.66, "close": 10.79, "pre_close": 10.68, "change": 0.11, "pct_chg": 1.03, "vol": 837346.9, "amount": 900879.538},
    {"ts_code": "000001.SZ", "trade_date": "20260525", "open": 10.68, "high": 10.76, "low": 10.64, "close": 10.68, "pre_close": 10.68, "change": 0.0, "pct_chg": 0.0, "vol": 663102.95, "amount": 709614.128},
    {"ts_code": "000001.SZ", "trade_date": "20260522", "open": 10.7, "high": 10.73, "low": 10.65, "close": 10.68, "pre_close": 10.7, "change": -0.02, "pct_chg": -0.1869, "vol": 954132.73, "amount": 1020057.083},
    {"ts_code": "000001.SZ", "trade_date": "20260521", "open": 10.78, "high": 10.8, "low": 10.69, "close": 10.7, "pre_close": 10.77, "change": -0.07, "pct_chg": -0.65, "vol": 1110211.08, "amount": 1194144.112},
    {"ts_code": "000001.SZ", "trade_date": "20260520", "open": 10.86, "high": 10.88, "low": 10.76, "close": 10.77, "pre_close": 10.86, "change": -0.09, "pct_chg": -0.8287, "vol": 747632.14, "amount": 808079.589},
    {"ts_code": "000001.SZ", "trade_date": "20260519", "open": 10.83, "high": 10.92, "low": 10.83, "close": 10.86, "pre_close": 10.86, "change": 0.0, "pct_chg": 0.0, "vol": 793529.13, "amount": 862561.883},
    {"ts_code": "000001.SZ", "trade_date": "20260518", "open": 10.96, "high": 10.97, "low": 10.82, "close": 10.86, "pre_close": 10.99, "change": -0.13, "pct_chg": -1.1829, "vol": 856381.57, "amount": 931697.164},
    {"ts_code": "000001.SZ", "trade_date": "20260515", "open": 11.05, "high": 11.11, "low": 10.96, "close": 10.99, "pre_close": 11.05, "change": -0.06, "pct_chg": -0.543, "vol": 974741.76, "amount": 1074648.533},
    {"ts_code": "000001.SZ", "trade_date": "20260514", "open": 11.14, "high": 11.15, "low": 11.05, "close": 11.05, "pre_close": 11.14, "change": -0.09, "pct_chg": -0.8079, "vol": 794368.41, "amount": 881960.631},
    {"ts_code": "000001.SZ", "trade_date": "20260513", "open": 11.25, "high": 11.28, "low": 11.11, "close": 11.14, "pre_close": 11.25, "change": -0.11, "pct_chg": -0.9778, "vol": 1017973.92, "amount": 1136724.107},
    {"ts_code": "000001.SZ", "trade_date": "20260512", "open": 11.28, "high": 11.36, "low": 11.21, "close": 11.25, "pre_close": 11.28, "change": -0.03, "pct_chg": -0.266, "vol": 1029038.42, "amount": 1158241.866},
    {"ts_code": "000001.SZ", "trade_date": "20260511", "open": 11.29, "high": 11.31, "low": 11.16, "close": 11.28, "pre_close": 11.3, "change": -0.02, "pct_chg": -0.177, "vol": 931865.21, "amount": 1047435.369},
    {"ts_code": "000001.SZ", "trade_date": "20260508", "open": 11.34, "high": 11.42, "low": 11.3, "close": 11.3, "pre_close": 11.37, "change": -0.07, "pct_chg": -0.6157, "vol": 798819.86, "amount": 905737.835},
    {"ts_code": "000001.SZ", "trade_date": "20260507", "open": 11.37, "high": 11.39, "low": 11.3, "close": 11.37, "pre_close": 11.36, "change": 0.01, "pct_chg": 0.088, "vol": 936958.06, "amount": 1062755.239},
    {"ts_code": "000001.SZ", "trade_date": "20260506", "open": 11.5, "high": 11.5, "low": 11.3, "close": 11.36, "pre_close": 11.49, "change": -0.13, "pct_chg": -1.1314, "vol": 1216387.55, "amount": 1380730.921},
    {"ts_code": "000001.SZ", "trade_date": "20260430", "open": 11.5, "high": 11.6, "low": 11.46, "close": 11.49, "pre_close": 11.52, "change": -0.03, "pct_chg": -0.2604, "vol": 1139241.62, "amount": 1312827.776},
    {"ts_code": "000001.SZ", "trade_date": "20260429", "open": 11.43, "high": 11.54, "low": 11.39, "close": 11.52, "pre_close": 11.46, "change": 0.06, "pct_chg": 0.5236, "vol": 1378423.44, "amount": 1583294.869},
    {"ts_code": "000001.SZ", "trade_date": "20260428", "open": 11.36, "high": 11.46, "low": 11.32, "close": 11.46, "pre_close": 11.38, "change": 0.08, "pct_chg": 0.703, "vol": 1674258.83, "amount": 1908333.959},
    {"ts_code": "000001.SZ", "trade_date": "20260427", "open": 11.33, "high": 11.57, "low": 11.29, "close": 11.38, "pre_close": 11.0, "change": 0.38, "pct_chg": 3.4545, "vol": 3401275.67, "amount": 3891707.615},
    {"ts_code": "000001.SZ", "trade_date": "20260424", "open": 10.98, "high": 11.03, "low": 10.92, "close": 11.0, "pre_close": 11.0, "change": 0.0, "pct_chg": 0.0, "vol": 582710.12, "amount": 639781.173},
    {"ts_code": "000001.SZ", "trade_date": "20260423", "open": 10.98, "high": 11.03, "low": 10.93, "close": 11.0, "pre_close": 10.98, "change": 0.02, "pct_chg": 0.1821, "vol": 648066.61, "amount": 711757.543},
    {"ts_code": "000001.SZ", "trade_date": "20260422", "open": 11.08, "high": 11.09, "low": 10.95, "close": 10.98, "pre_close": 11.08, "change": -0.1, "pct_chg": -0.9025, "vol": 839053.99, "amount": 923203.009},
    {"ts_code": "000001.SZ", "trade_date": "20260421", "open": 11.04, "high": 11.16, "low": 11.03, "close": 11.08, "pre_close": 11.06, "change": 0.02, "pct_chg": 0.1808, "vol": 806946.34, "amount": 896659.539},
    {"ts_code": "000001.SZ", "trade_date": "20260420", "open": 11.01, "high": 11.07, "low": 10.96, "close": 11.06, "pre_close": 11.01, "change": 0.05, "pct_chg": 0.4541, "vol": 630033.66, "amount": 695097.194}
]

# 转换为DataFrame
df = pd.DataFrame(data)

# 按日期排序（从早到晚）
df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
df = df.sort_values('trade_date').reset_index(drop=True)

print(f"数据准备完成，共{len(df)}个交易日")
print(f"日期范围: {df['trade_date'].min().strftime('%Y-%m-%d')} 至 {df['trade_date'].max().strftime('%Y-%m-%d')}")

# 计算技术指标

# 1. 均线（MA）
df['MA5'] = df['close'].rolling(window=5).mean()
df['MA10'] = df['close'].rolling(window=10).mean()
df['MA20'] = df['close'].rolling(window=20).mean()

# 2. MACD（12,26,9）
ema_fast = df['close'].ewm(span=12, adjust=False).mean()
ema_slow = df['close'].ewm(span=26, adjust=False).mean()
df['DIF'] = ema_fast - ema_slow
df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
df['MACD'] = 2 * (df['DIF'] - df['DEA'])

# 3. RSI（14日）
delta = df['close'].diff()
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / (loss + 1e-10)  # 防止除零
df['RSI'] = 100 - (100 / (1 + rs))

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图表
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle('平安银行(000001.SZ) 技术分析图表', fontsize=16)

# 上方：K线 + 均线
ax1.plot(df['trade_date'], df['close'], 'b-', linewidth=1.5, label='收盘价')
ax1.plot(df['trade_date'], df['MA5'], 'r-', linewidth=1, label='MA5', alpha=0.8)
ax1.plot(df['trade_date'], df['MA10'], 'g-', linewidth=1, label='MA10', alpha=0.8)
ax1.plot(df['trade_date'], df['MA20'], 'm-', linewidth=1, label='MA20', alpha=0.8)
ax1.set_ylabel('价格')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_title('价格走势与均线')

# 中间：MACD
colors = ['red' if x >= 0 else 'green' for x in df['MACD']]
ax2.bar(df['trade_date'], df['MACD'], color=colors, alpha=0.6, label='MACD柱')
ax2.plot(df['trade_date'], df['DIF'], 'b-', linewidth=1.5, label='DIF')
ax2.plot(df['trade_date'], df['DEA'], 'r-', linewidth=1.5, label='DEA')
ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax2.set_ylabel('MACD')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_title('MACD指标 (12,26,9)')

# 下方：RSI
ax3.plot(df['trade_date'], df['RSI'], 'b-', linewidth=1.5, label='RSI(14)')
ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='超买线(70)')
ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='超卖线(30)')
ax3.fill_between(df['trade_date'], 70, 100, alpha=0.1, color='red')
ax3.fill_between(df['trade_date'], 0, 30, alpha=0.1, color='green')
ax3.set_ylabel('RSI')
ax3.set_xlabel('日期')
ax3.legend(loc='upper left')
ax3.grid(True, alpha=0.3)
ax3.set_title('RSI指标 (14日)')
ax3.set_ylim(0, 100)

# 格式化x轴日期
import matplotlib.dates as mdates
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('000001_SZ_tech_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

# 输出最新数据
print("\n=== 技术指标汇总（最新交易日） ===")
print(f"日期: {df['trade_date'].iloc[-1].strftime('%Y-%m-%d')}")
print(f"收盘价: {df['close'].iloc[-1]:.2f}")
print(f"MA5: {df['MA5'].iloc[-1]:.2f}")
print(f"MA10: {df['MA10'].iloc[-1]:.2f}")
print(f"MA20: {df['MA20'].iloc[-1]:.2f}")
print(f"DIF: {df['DIF'].iloc[-1]:.4f}")
print(f"DEA: {df['DEA'].iloc[-1]:.4f}")
print(f"MACD: {df['MACD'].iloc[-1]:.4f}")
print(f"RSI(14): {df['RSI'].iloc[-1]:.2f}")

# 趋势判断
print("\n=== 趋势分析 ===")
if df['close'].iloc[-1] > df['MA5'].iloc[-1] > df['MA10'].iloc[-1] > df['MA20'].iloc[-1]:
    print("均线多头排列：短期趋势向上")
elif df['close'].iloc[-1] < df['MA5'].iloc[-1] < df['MA10'].iloc[-1] < df['MA20'].iloc[-1]:
    print("均线空头排列：短期趋势向下")
else:
    print("均线交织：趋势不明确")

if df['DIF'].iloc[-1] > df['DEA'].iloc[-1]:
    print("MACD金叉状态：短期动能偏强")
else:
    print("MACD死叉状态：短期动能偏弱")

if df['RSI'].iloc[-1] > 70:
    print("RSI超买：注意回调风险")
elif df['RSI'].iloc[-1] < 30:
    print("RSI超卖：可能存在反弹机会")
else:
    print("RSI正常区间：市场相对平衡")