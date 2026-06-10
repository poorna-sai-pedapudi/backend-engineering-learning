-- Query 1, 

select 
	users.id, 
	users.name, 
	count(orders.id) as total_orders
from users
left join orders
on users.id = orders.user_id
group by users.id, users.name
order by total_orders desc;

-- Query 2

SELECT
    users.id,
    users.name,
    COALESCE(SUM(orders.price), 0) AS total_spent
FROM users
LEFT JOIN orders
ON users.id = orders.user_id
GROUP BY users.id, users.name
ORDER BY total_spent DESC;


-- Query 3
select 
	count(users.id) as total_users, 
	count(orders.id) as total_orders, 
	sum(orders.price) as total_revenue, 
	avg(orders.price) as average_order_price
from users
left join orders
on users.id = orders.user_id;


select 
	(select count(*) from users) as total_users,
	(select count(*) from orders) as total_orders,
	(select coalesce(sum(price), 0) from orders) as total_revenue,
	(select coalesce(avg(price), 0) from orders) as average_order_prices,
	(select coalesce(min(price), 0) from orders) as min_price,
	(select coalesce(max(price), 0) from orders) as max_price;


select count(*) from users;

select count(id) from users;
