use stock_db


select
    ticker,
    avg(daily_return) as avg_return
from fact_stock_prices
group by ticker
order by avg_return desc;


select
    ticker,
    avg(abs(daily_return)) as volatility
from fact_stock_prices
group by ticker
order by volatility desc;


select
    ticker,
    avg([close]) as avg_close_price
from fact_stock_prices
group by ticker
order by avg_close_price desc;


select
    *
from fact_stock_prices
where date >= dateadd(day, -30, getdate())
order by date desc;


select
    ticker,
    max(volume) as highest_volume
from fact_stock_prices
group by ticker
order by highest_volume desc;


select
    ticker,
    avg(volume) as avg_volume
from fact_stock_prices
group by ticker
order by avg_volume desc;