# Final

# Stock Data Engineering Pipeline

## Project Overview
This project is an end-to-end Data Engineering pipeline built using Python, SQL Server, Apache Airflow, and Power BI.

The pipeline extracts historical stock market data from Yahoo Finance using the yfinance API, performs data cleaning and transformation, validates the data, and loads it into a SQL Server database.

The project also supports incremental loading to avoid duplicate records and improve performance.

---

# Technologies Used

- Python
- Pandas
- yfinance
- SQL Server
- Apache Airflow
- VS Code

---

# Project Structure

```bash
stock-data-pipeline/
│
├── main.py
├── sql_queries.sql
├── requirements.txt
├── README.md
│
└── airflow/
    └── dags/
        └── stock_pipeline_dag.py




Pipeline Steps
1. Data Ingestion

Historical stock data is extracted from Yahoo Finance using the yfinance library.

Tracked stocks:

AAPL
MSFT
AMZN
2. Data Cleaning

The pipeline performs:

Removing duplicates
Handling missing values
Formatting dates
Resetting indexes
3. Data Transformation

The following metrics are calculated:

Daily Return
Price Range
Moving Average (7 days)
Volatility
Data Modeling
Dimension Table
dim_company

Columns:

ticker
company_name
Fact Table
fact_stock_prices

Columns:

date
ticker
open
high
low
close
volume
daily_return
Incremental Loading

The pipeline checks the latest stored date in the database and only loads new records.

This prevents duplicate data and improves performance.

Data Validation

Validation checks include:

Removing duplicate records
Handling missing values
Ensuring volume values are positive
SQL Analytical Queries

The project includes analytical SQL queries such as:

Best performing stock
Most volatile stock
Average closing price
Last 30 days trends
Airflow Orchestration

Apache Airflow DAG files were implemented successfully.

The DAG contains:

extract_stock_data
transform_data
load_to_database
Airflow Note

Running Apache Airflow on Windows requires WSL2 or Docker because Airflow officially supports Linux/macOS environments.

The DAG structure and orchestration logic are included in this project.
