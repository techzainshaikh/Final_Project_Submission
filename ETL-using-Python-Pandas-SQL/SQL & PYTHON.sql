CREATE TABLE df_order (
    order_id INT PRIMARY KEY,
    order_date DATE,
    ship_mode VARCHAR(50),
    segment VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INT,
    region VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    discount FLOAT,
    sales_price FLOAT,
    profit FLOAT
);


select * from df_order;


-- find top 10 highest revenue generated product 

select top 10 product_id,sum(sales_price) as sales
from df_order
group by product_id
order by sales desc;

-- find top 5 for each region

with cte as(
select region, product_id,sum(sales_price) as sales
from df_order
group by region,product_id)
select * from(
select *
, row_number() over(partition by region order by sales desc) as rnk
from cte) A
where rnk<=5;


-- find month over month growth comparison 2022 and 2023 

with cte as(
select year (order_date) as order_year , month(order_date) as order_month,
sum(sales_price) as sales
from df_order
group by year(order_date),month(order_date)
)
select order_month
,sum(case when order_year=2022 then sales else 0 end) as sales_2022
,sum(case when order_year=2023 then sales else 0 end) as sales_2023
from cte
group by order_month
order by order_month


-- for each category which month had highest sales

with cte as(
select category,format(order_date,'yyyMM') as order_year_month
,sum(sales_price) as sales
from df_order
group by category,format(order_date,'yyyMM') 
)
select * from(
select *,
row_number() over(partition by category order by sales desc) as rnk
from cte
) a
where rnk=1


--  which sub category had highest growth by profit in 2023 compare to 2022


with cte as(
select sub_category,year (order_date) as order_year ,
sum(sales_price) as sales
from df_order
group by sub_category ,year(order_date)
)
, cte2 as (
select sub_category
,sum(case when order_year=2022 then sales else 0 end) as sales_2022
,sum(case when order_year=2023 then sales else 0 end) as sales_2023
from cte
group by sub_category
)
select top 1 * 
, (sales_2023-sales_2022)
from cte2
order by (sales_2023-sales_2022) desc