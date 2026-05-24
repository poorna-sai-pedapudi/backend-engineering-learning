select * from users
order by id;

select * from orders
order by id;

-- Query 1, Top spender

select users.id, users.name, coalesce(sum(orders.price), 0) as total_spent
from users
left join orders
on users.id = orders.user_id
group by users.id, users.name
order by total_spent desc
limit 1;


-- Query 2, Users with avergae order price > 100

select users.id, users.name, avg(orders.price) as avg_order_price
from users
inner join orders
on users.id = orders.user_id
group by users.id, users.name
having avg(orders.price) > 100;


-- Query 3, Total Revenue

select sum(price) as total_revenue
from orders;


-- Query 4, Most active user

select users.id, users.name, count(orders.id) as total_orders
from users
inner join orders
on users.id = orders.user_id
group by users.id, users.name
order by total_orders desc
limit 1;


-- Query 5, Revenue grouped by age

select 
	case
		when users.age < 25 then 'Under 25'
		when users.age between 25 and 30 then '25-30'
		else 'Above 30'
	end as age_range,
	coalesce(sum(orders.price), 0) as total_revenue
from users
left join orders
on users.id = orders.user_id
group by age_range
order by total_revenue desc;


-- Query 6, Duplicate email detection

select email, count(*) as email_count
from users
group by email
having count(*) > 1;


-- Query 7, find orphan orders

select orders.*
from orders
left join users
on orders.user_id = users.id
where users.id is null;


-- Query 8, Users with no password set

select id, name, email
from users
where password is null;
