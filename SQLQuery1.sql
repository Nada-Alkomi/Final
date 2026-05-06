
use stock_db



select ticker, avg(daily_return) as avg_return
from fact_stock_prices
group by ticker
order by avg_return desc;


select ticker, avg(daily_return) as volatility
from fact_stock_prices
group by ticker
order by volatility desc;


select ticker, avg([close]) as avg_close
from fact_stock_prices
group by ticker;


select *
from fact_stock_prices
where date >= dateadd(day, -30, getdate());