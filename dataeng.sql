use stock_db

SELECT Ticker, AVG(Daily_Return) AS avg_return
FROM stock_data
GROUP BY Ticker
ORDER BY avg_return DESC;



SELECT Ticker, AVG(Volatility_7) AS volatility
FROM stock_data
GROUP BY Ticker
ORDER BY volatility DESC;


SELECT 
    Ticker, 
    AVG([Close]) AS avg_close
FROM stock_data
GROUP BY Ticker;



SELECT *
FROM stock_data
WHERE Date >= DATEADD(DAY, -30, GETDATE());




CREATE TABLE dim_company (
    ticker VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(100)
);




CREATE TABLE fact_stock_prices (
    [date] DATE,
    ticker VARCHAR(10),
    [open] FLOAT,
    [high] FLOAT,
    [low] FLOAT,
    [close] FLOAT,
    volume BIGINT,
    daily_return FLOAT,
    PRIMARY KEY ([date], ticker),
    FOREIGN KEY (ticker) REFERENCES dim_company(ticker)
);