import tushare as ts
import os, datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

pro = ts.pro_api(os.getenv('TUSHARE_TOKEN'))

end = datetime.datetime.now().strftime('%Y%m%d')
start = (datetime.datetime.now() - datetime.timedelta(days=120)).strftime('%Y%m%d')

df = pro.index_daily(ts_code='000001.SH', start_date=start, end_date=end)
df = df.sort_values('trade_date').tail(100)
df['trade_date'] = pd.to_datetime(df['trade_date'])

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df['trade_date'], df['close'], color='#e74c3c', linewidth=2, label='上证指数收盘价')
ax.fill_between(df['trade_date'], df['close'], alpha=0.15, color='#e74c3c')

ax.set_title('上证指数近100日走势', fontsize=16, fontweight='bold')
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('收盘价', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('shanghai_index_100d.png', dpi=150)
print(f'图表已保存，记录数: {len(df)}')
print(f'最新收盘: {df.iloc[-1]["close"]}，日期: {df.iloc[-1]["trade_date"].strftime("%Y-%m-%d")}')
print(f'最高: {df["close"].max():.2f}，最低: {df["close"].min():.2f}')
