# # Stock Data Engineering Pipeline

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
- SQLAlchemy
- Apache Airflow
- Power BI
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
GOOGL
META
TSLA
NVDA
NFLX
INTC
AMD
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
Volatility (7 days)
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
Validating numerical columns
Ensuring volume values are positive
SQL Analytical Queries

The project includes analytical SQL queries such as:

Best performing stock
Most volatile stock
Average closing price
Last 30 days trends
Highest trading volume
Airflow Orchestration

Apache Airflow DAG files were implemented successfully.

The DAG contains:

extract_stock_data
transform_data
load_to_database
Airflow Note

Running Apache Airflow on Windows requires WSL2 or Docker because Airflow officially supports Linux/macOS environments.

The DAG structure and orchestration logic are included in this project.

Dashboard

A Power BI dashboard was created to visualize:

Stock price trends
Daily returns
Trading volume
Recent stock records
Architecture

The project follows a modern ETL pipeline architecture:

Extract stock data from Yahoo Finance.
Transform and clean data using Pandas.
Validate data quality.
Load processed data into SQL Server.
Execute analytical SQL queries.
Visualize insights using Power BI.
Orchestrate the workflow using Apache Airflow.
Challenges Faced

Several challenges were encountered during development:

Handling MultiIndex columns returned from yfinance.
Managing duplicate records during incremental loading.
Running Apache Airflow on Windows systems.
Validating missing and inconsistent stock records.
Ensuring SQL Server integration works correctly.

These challenges were resolved successfully during implementation.