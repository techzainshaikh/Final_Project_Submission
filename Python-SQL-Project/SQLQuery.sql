create table crypto_info (
	coins varchar(50) primary key,
	usd decimal(12,2) check(usd > -1),
	usd_market_cap bigint  check (usd_market_cap > -1),
	usd_24h_vol bigint check (usd_24h_vol > -1),
	usd_24h_change decimal(5,2),
	last_updated_at datetime
);

select * from crypto_info;

-- List the top 10 crypto coins with the highest USD market capitalization (usd_market_cap), ordered from highest to lowest.
select top (10) *
from crypto_info
order by usd_market_cap desc;

-- Calculate the average 24-hour trading volume (usd_24h_vol) across all coins.
select avg(usd_24h_vol) as trading_volume
from crypto_info;

-- Identify the coin with the highest positive 24-hour percentage change (usd_24h_change) and the coin with the lowest (most negative) 24-hour percentage change.
select coins, usd_24h_change
from crypto_info
where usd_24h_change = (select MAX(usd_24h_change) from crypto_info)
or usd_24h_change = (select MIN(usd_24h_change) from crypto_info);

-- For each coin, calculate the ratio of usd_market_cap to usd_24h_vol and order the results in descending order by this ratio.
select coins, 
case 
	when usd_24h_vol = 0 then null
	else (usd_market_cap/usd_24h_vol) 
	end as MC_Vol_Ratio
from crypto_info;

-- Count how many coins experienced a 24-hour percentage change (usd_24h_change) of less than -5%.
select coins, usd_24h_change
from crypto_info
where usd_24h_change < -5;

-- Calculate the total usd_market_cap and usd_24h_vol for all coins, then compute the percentage of the total market cap that each coin contributes.
SELECT 
    coins, 
    CAST(usd_market_cap AS FLOAT) / NULLIF((SELECT SUM(usd_market_cap) FROM crypto_info), 0) AS mc_contribution, 
    CAST(usd_24h_vol AS FLOAT) / NULLIF((SELECT SUM(usd_24h_vol) FROM crypto_info), 0) AS vol_contribution
FROM crypto_info
ORDER BY mc_contribution DESC;

-- Show coins with 24h price changes is greater than the average volatility, ordered by market cap
select coins, usd_24h_change
from crypto_info
where abs(usd_24h_change) > (select AVG(ABS(usd_24h_change)) from crypto_info)
order by usd_24h_change;


-- Find coins where 24h volume exceeds 20% of their market cap, indicating unusual trading activity
select coins, usd_24h_vol
from crypto_info
where usd_24h_vol > usd_market_cap * 0.2
order by usd_24h_vol;