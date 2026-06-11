import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # Data Fetch Playground

    Test fetching stock data through **akshare**.

    This notebook experiments with different akshare APIs for A-share data.
    Sina-based endpoints are used where East Money (em) endpoints are unreliable.
    """)
    return


@app.cell
def _():
    import akshare as ak
    import pandas as pd

    print(f"akshare version: {ak.__version__}")
    print(f"pandas version: {pd.__version__}")
    return (ak,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Stock List — A-Share (沪深A股)
    """)
    return


@app.cell
def _(ak, mo):
    # Fetch list of all A-share stocks
    stock_info = ak.stock_info_a_code_name()
    mo.ui.table(stock_info, page_size=10, label="A股列表")
    return (stock_info,)


@app.cell
def _(stock_info):
    print(f"Total A-share stocks: {len(stock_info)}")
    print(f"\nFirst 5 rows:")
    print(stock_info.head())
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Historical K-Line Data — Single Stock (Sina)
    """)
    return


@app.cell
def _(mo):
    exchange = mo.ui.dropdown(
        label="交易所",
        options=["sh", "sz"],
        value="sh",
    )
    stock_code = mo.ui.text(
        label="股票代码", value="600519", placeholder="e.g. 600519"
    )
    adjust = mo.ui.dropdown(
        label="复权方式",
        options=["", "qfq", "hfq"],
        value="qfq",
    )
    mo.hstack([exchange, stock_code, adjust], justify="start")
    return adjust, exchange, stock_code


@app.cell
def _(adjust, ak, exchange, stock_code):
    # Sina-based daily K-line data — more reliable than East Money
    symbol = f"{exchange.value}{stock_code.value}"
    df = ak.stock_zh_a_daily(symbol=symbol, adjust=adjust.value or "")
    print(f"Fetched {len(df)} rows for {symbol}")
    print(f"Date range: {df['date'].iloc[0]} ~ {df['date'].iloc[-1]}")
    df.tail(10)
    return (df,)


@app.cell
def _(df, mo):
    # Summary statistics
    numeric_cols = ["open", "close", "high", "low", "volume", "outstanding_share", "turnover"]
    available_cols = [c for c in numeric_cols if c in df.columns]

    summary = df[available_cols].describe()
    mo.ui.table(summary.round(2), label="数据统计摘要")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Real-time Quotes — 实时行情 (Sina)
    """)
    return


@app.cell
def _(ak, mo):
    # Sina-based real-time quotes — slower but more reliable
    spot = ak.stock_zh_a_spot()
    print(f"Total stocks in spot data: {len(spot)}")
    print(f"\nColumns: {list(spot.columns)}")
    mo.ui.table(spot.head(20), page_size=10, label="实时行情 (前20)")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Stock Sectors — 行业板块 (同花顺)
    """)
    return


@app.cell
def _(ak, mo):
    # THS industry sectors
    sectors = ak.stock_board_industry_name_ths()
    print(f"Total industry sectors: {len(sectors)}")
    mo.ui.table(sectors, page_size=10, label="行业板块列表")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Index Data — 指数
    """)
    return


@app.cell
def _(ak):
    # Major indices (CSI 300, SSE 50, etc.)
    index_list = [
        ("sh000300", "沪深300"),
        ("sh000001", "上证指数"),
        ("sz399001", "深证成指"),
        ("sh000016", "上证50"),
        ("sh000905", "中证500"),
    ]

    # Fetch daily data for 沪深300
    index_df = ak.stock_zh_index_daily(symbol="sh000300")
    print(f"沪深300 历史数据: {len(index_df)} 条")
    print(f"区间: {index_df['date'].iloc[0]} ~ {index_df['date'].iloc[-1]}")
    index_df.tail(10)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. Northbound Capital — 北向资金
    """)
    return


@app.cell
def _(ak):
    # Northbound capital flow (沪股通+深股通)
    hsgt_his = ak.stock_hsgt_hist_em(symbol="北向资金")
    print(f"北向资金历史数据: {len(hsgt_his)} 条")
    print(f"最近 10 天:")
    hsgt_his.head(10)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. Financial Statements — 财务数据
    """)
    return


@app.cell
def _(ak, mo):
    # Profit sheet for a stock
    profit_df = ak.stock_profit_sheet_by_report_em(symbol="SH600519")
    print(f"贵州茅台 利润表: {len(profit_df)} 条记录")
    mo.ui.table(profit_df, page_size=5, label="利润表 (前5条)")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Summary

    This notebook tested several akshare data fetching capabilities:

    | Section | API | Data Source |
    | --- | --- | --- |
    | Stock list | `ak.stock_info_a_code_name()` | Sina |
    | Historical K-line | `ak.stock_zh_a_daily()` | Sina |
    | Real-time quotes | `ak.stock_zh_a_spot()` | Sina (slower) |
    | Industry sectors | `ak.stock_board_industry_name_ths()` | THS |
    | Index data | `ak.stock_zh_index_daily()` | Sina |
    | Northbound capital | `ak.stock_hsgt_hist_em()` | East Money |
    | Financial statements | `ak.stock_profit_sheet_by_report_em()` | East Money |

    > **Note:** East Money (em) endpoints can be flaky and may return
    > `ConnectionError` intermittently. Sina-based APIs are more reliable
    > but may have slightly different data columns.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
