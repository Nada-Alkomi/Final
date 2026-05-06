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
    "AMZN": "Amazon"
}

dim_df = pd.DataFrame(list(companies.items()), columns=["ticker", "company_name"])

try:
    dim_df.to_sql("dim_company", engine, if_exists="append", index=False)
except:
    pass

# ================= GET LAST DATE =================
query = "SELECT MAX(date) as last_date FROM fact_stock_prices"
last_date = pd.read_sql(query, engine).iloc[0, 0]


last_date = pd.to_datetime(last_date)

print("Last date in DB:", last_date)

# ================= EXTRACT =================
tickers = list(companies.keys())
all_data = []

for ticker in tickers:

    if pd.isna(last_date):
        df = yf.download(ticker, period="1mo")
    else:
        start_date = last_date + pd.Timedelta(days=1)

        
        if start_date > pd.Timestamp.today().normalize():
            continue

        try:
            df = yf.download(ticker, start=start_date)
        except:
            continue

    if df.empty:
        continue

    df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    df["Ticker"] = ticker

    all_data.append(df)


if not all_data:
    print("No new data to insert.")
    exit()

final_df = pd.concat(all_data, ignore_index=True)

# ================= TRANSFORM =================
final_df = final_df.sort_values(by=["Ticker", "Date"])

final_df["Daily_Return"] = final_df.groupby("Ticker")["Close"].pct_change()

# ================= FACT =================
fact_df = final_df[[
    "Date", "Ticker", "Open", "High", "Low", "Close", "Volume", "Daily_Return"
]]

fact_df.columns = [
    "date", "ticker", "open", "high", "low", "close", "volume", "daily_return"
]

fact_df = fact_df.drop_duplicates(subset=["date", "ticker"])


# ================= VALIDATION =================

fact_df = fact_df.dropna(subset=["date", "ticker"])


fact_df = fact_df.drop_duplicates(subset=["date", "ticker"])


fact_df = fact_df[fact_df["volume"] >= 0]

print("Validation passed successfully!")


# ================= LOAD =================
fact_df.to_sql("fact_stock_prices", engine, if_exists="append", index=False)

print("Data inserted successfully!")