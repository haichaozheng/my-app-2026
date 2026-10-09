"""获取上证指数日线数据并落盘为 CSV。

用 tushare pro_api 获取 000001.SH（上证指数）的日线行情数据，
保存为 sse_daily.csv，供 linear_regression.py 使用。

运行前：
  - 安装依赖：pip install tushare pandas python-dotenv
  - 配置密钥：在项目根目录 .env 文件中写入 TUSHARE_TOKEN=你的token
    （参考 weeks/week07/cases/.env.example）
"""

import os
from pathlib import Path

import pandas as pd
import tushare as ts
from dotenv import load_dotenv

DATA_DIR = Path(__file__).resolve().parent
load_dotenv(DATA_DIR.parent.parent.parent.parent / ".env")

TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")

INDEX_CODE = "000001.SH"
START_DATE = "20150101"
END_DATE = "20261009"


def fetch_index_daily() -> pd.DataFrame:
    """从 tushare 获取上证指数日线。"""
    if not TUSHARE_TOKEN:
        raise ValueError(
            "未找到 TUSHARE_TOKEN。请在项目根目录 .env 文件中配置：\n"
            "  TUSHARE_TOKEN=你的token\n"
            "参考 weeks/week07/cases/.env.example"
        )

    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()

    print(f"正在获取 {INDEX_CODE} 日线数据（{START_DATE} ~ {END_DATE}）…")
    df = pro.index_daily(
        ts_code=INDEX_CODE,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    if df is None or df.empty:
        raise RuntimeError("tushare 返回空数据，请检查 token 是否有效、是否有指数权限。")

    # tushare 默认按日期降序，改为升序
    df = df.sort_values("trade_date").reset_index(drop=True)

    print(f"获取成功：{len(df)} 条日线，"
          f"{df['trade_date'].iloc[0]} ~ {df['trade_date'].iloc[-1]}")
    return df


def main() -> None:
    df = fetch_index_daily()

    out_path = DATA_DIR / "sse_daily.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"已保存至 {out_path}")
    print(f"字段：{list(df.columns)}")
    print(f"前 5 行：")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
