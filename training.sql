------------------------------------------------------------------------------------------------------------------
-- -- USERS TABLE
create table users (
	id serial primary key,
	name varchar(100),
	email varchar(100),
	age int
);

insert into users (name, email, age)
VALUES
('Harish', 'harish@example.com', 27),
('Rahul', 'rahul@example.com', 28),
('Divya', 'divya@example.com', 25),
('Sneha', 'sneha@example.com', 24),
('Arjun', 'arjun@example.com', 30);

select * from users;

select * from users 
where age > 26;

select * from users
order by age desc;

select * from users
limit 3;

update users 
set age  = 29
where name = 'Arjun';

INSERT INTO users (name, email, age)
VALUES ('Test User', 'test@example.com', 99);

delete from users
where name = 'Test User';

select last_value from users_id_seq;

select * from users 
order by id;

-- AND

select * from users
where age > 25 and name = 'Rahul';

-- OR
select * from users
where age > 25 or name = 'Rahul';

-- COUNt
select count(*) from users;

-- DISTINCT
INSERT INTO users (name, email, age)
VALUES
('Aman', 'aman@example.com', 27),
('Ravi', 'ravi@example.com', 27);

select distinct age from users;

-- LIKE - to search patterns or text
-- H% - starts with H
select * from users
where name like 'H%';

-- %a - ends with a
select * from users
where name like '%a';

-- %ar% - contains ar
select * from users
where name like '%ar%';

-- IN - checks multiple values easily
select * from users
where age in (24, 27, 28);

-- the above is same as below query but cleaner 
select * from users
where age = 24 or age = 27 or age = 28;

-- BETWEEN
select * from users
where age between 24 and 28; -- includes both 24, and 28

INSERT INTO users (name, email, age)
VALUES ('Null User', NULL, 40);

SELECT * FROM users
WHERE email IS NULL;

------------------------------------------------------------------------------------------------------------------

alter table users
add column password TEXT;

select id, name, email, age, password
from users
order by id;

select id, name, email, password
from users
where email = 'secure@example.com';

alter table users
add column created_at timestamp default now();


select * from users;

select * from orders;

create index idx_users_email
on users(email);

select * from pg_indexes 
where tablename = 'users';


explain analyze 
select *
from users
where email = 'harish.pedapudi@example.com';

explain analyze 
select *
from users
where age = 25;


select *
from orders
where user_id = 1;


select *
from orders
where user_id = 1
and price > 100;

create index idx_orders_user_price
on orders(user_id, price);


select indexname, indexdef
from pg_indexes
where tablename = 'orders';

explain analyze 
select *
from orders
where user_id = 1;


explain analyze 
select *
from orders
where user_id = 1
and price > 100;


explain analyze 
select *
from orders
where price > 100;


select 1;

select *
from users
order by id;