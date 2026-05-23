select * from users;

select * from orders;

-- Query 1, Top 3 most expensive orders
select *
from orders
order by price desc
limit 3;

-- Query 2, Users with no orders
select users.id, users.name, users.email
from users
left join orders
on users.id = orders.user_id
where orders.id is null;

-- Query 3, Total Spending per user
select users.id, users.name, coalesce(sum(orders.price), 0) as total_spent
from users
left join orders
on users.id = orders.user_id
group by users.id, users.name
order by total_spent desc;

-- Query 4, Avg Order Price
select avg(price) as avg_order_price
from orders;


-- Query 5, Youngest User
select *
from users
order by age
limit 1;

-- Query 6, Oldest User
select *
from users
order by age desc
limit 1;

-- Query 7, Order count per user
select users.id, users.name, count(orders.id) as total_orders
from users
left join orders
on users.id = orders.user_id
group by users.id, users.name
order by total_orders desc;

-- Query 8, Users with more than 2 orders
select users.id, users.name, count(orders.id) as total_orders
from users
inner join orders
on users.id = orders.user_id
group by users.id, users.name
having count(orders.id) >= 2;