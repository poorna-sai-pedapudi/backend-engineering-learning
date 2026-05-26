select * from users
order by id;

select * from orders
order by id;

-- Query 1, Daily User Creation Count

select 
	date(created_at) as created_date,
	count(*) as total_users_created
from users
group by date(created_at)
order by created_date desc;


-- Query 2, Revenue per day

select 
	date(users.created_at) as created_date,
	coalesce(sum(orders.price), 0) as total_revenue
from users
left join orders
on users.id = orders.user_id
group by date(users.created_at)
order by created_date desc;


-- Query 3, Top 5 Expensive Orders

select *
from orders
order by price desc
limit 5;


-- Query 4, Most Recent Users

select id, name, email, age, created_at
from users
order by created_at desc
limit 5;


-- Query 5, Users created in last 24 hours

select id, name, email, age, created_at
from users
where created_at >= now() - interval '24 hours'
order by created_by desc;


-- Query 6, Revenue by User age

select 
	users.age,
	coalesce(sum(orders.price), 0) as total_revenue
from users
left join orders
on users.id = orders.user_id
group by users.age
order by total_revenue desc;


-- Query 7, Detect Users without email

select id, name, email
from users
where email is null or email ='';


-- Query 8, Find inactive users

select users.id, users.name, users.email
from users
left join orders
on users.id = orders.user_id
where orders.id is null;