import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# ================= DB CONNECTION =================
engine = create_engine(
    "mssql+pyodbc://(localdb)\\MSSQLLocalDB/stock_db?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# ================= DIM COMPANY =================
companies = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOGL": "Google",
    "META": "Meta",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "NFLX": "Netflix",
    "INTC": "Intel",
    "AMD": "AMD"
}

dim_df = pd.DataFrame(
    list(companies.items()),
    columns=["ticker", "company_name"]
)

# ================= LOAD DIM COMPANY =================
try:
    existing_companies = pd.read_sql(
        "SELECT ticker FROM dim_company",
        engine
    )

    dim_df = dim_df[
        ~dim_df["ticker"].isin(existing_companies["ticker"])
    ]

    if not dim_df.empty:
        dim_df.to_sql(
            "dim_company",
            engine,
            if_exists="append",
            index=False
        )

except:
    pass

# ================= GET LAST DATE =================
query = "SELECT MAX(date) as last_date FROM fact_stock_prices"

try:
    last_date = pd.read_sql(query, engine).iloc[0, 0]
    last_date = pd.to_datetime(last_date)
except:
    last_date = pd.NaT

print("Last date in DB:", last_date)

# ================= EXTRACT =================
tickers = list(companies.keys())
all_data = []

for ticker in tickers:

    try:

        # incremental loading
        if pd.isna(last_date):
            df = yf.download(ticker, period="1mo")
        else:
            start_date = last_date + pd.Timedelta(days=1)

            if start_date > pd.Timestamp.today().normalize():
                continue

            df = yf.download(ticker, start=start_date)

        if df.empty:
            continue

        # fix multi index columns
        df.columns = df.columns.get_level_values(0)

        # reset index
        df = df.reset_index()

        # standardize date format
        df["Date"] = pd.to_datetime(df["Date"]).dt.date

        # add ticker
        df["Ticker"] = ticker

        all_data.append(df)

    except:
        continue

# no new data
if not all_data:
    print("No new data to insert.")
    exit()

# combine all stocks
final_df = pd.concat(all_data, ignore_index=True)

# ================= TRANSFORM =================
final_df = final_df.sort_values(
    by=["Ticker", "Date"]
)

# daily return
final_df["Daily_Return"] = (
    final_df.groupby("Ticker")["Close"]
    .pct_change()
)

# price range
final_df["Price_Range"] = (
    final_df["High"] - final_df["Low"]
)

# moving average
final_df["Moving_Avg_7"] = (
    final_df.groupby("Ticker")["Close"]
    .rolling(7)
    .mean()
    .reset_index(0, drop=True)
)

# volatility
final_df["Volatility_7"] = (
    final_df.groupby("Ticker")["Daily_Return"]
    .rolling(7)
    .std()
    .reset_index(0, drop=True)
)

# ================= FACT TABLE =================
fact_df = final_df[[
    "Date",
    "Ticker",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Daily_Return"
]]

fact_df.columns = [
    "date",
    "ticker",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "daily_return"
]

# ================= VALIDATION =================

# remove nulls
fact_df = fact_df.dropna(
    subset=["date", "ticker"]
)

# remove duplicates
fact_df = fact_df.drop_duplicates(
    subset=["date", "ticker"]
)

# validate numeric columns
fact_df = fact_df[
    (fact_df["open"] > 0) &
    (fact_df["high"] > 0) &
    (fact_df["low"] > 0) &
    (fact_df["close"] > 0) &
    (fact_df["volume"] >= 0)
]

print("Validation passed successfully!")

# ================= LOAD =================
fact_df.to_sql(
    "fact_stock_prices",
    engine,
    if_exists="append",
    index=False
)

print("Data inserted successfully!")






fact_df.to_csv("stock_data.csv", index=False)

print("CSV file exported successfully!")