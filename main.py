import http

from fastapi import FastAPI, HTTPException, status
from database import cursor, conn
from models import User, Order

app = FastAPI()

# @app.post("/create-user")
# def create_user(user: User):
#     return {
#         "name" : user.name,
#         "age" : user.age
#     }

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/hello")
def hello():
    return {"message" : "Hello Backend"}

@app.get("/search")
def search(name: str):
    return {"searching_for": name}

################################ USERS ########################################################

#we get all users 
# GET /users
#API 1

@app.get("/users")
def get_users():
    cursor.execute("select * from users order by id")
    users = cursor.fetchall()
    return users

# GET user by id
# GET /users/ 1
#API 2

@app.get("/users/{id}")
def get_user(id: int):
    cursor.execute("select * from users where id = %s", (id,))
    user = cursor.fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    
    return user


#Create user
# POST /create-user
#API 3

@app.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    cursor.execute("insert into users (name, email, age) values (%s, %s, %s) returning *",
        (user.name, user.email, user.age))
    
    new_user = cursor.fetchone()
    conn.commit() #to save the changes permanently

    return new_user

#Updating the user
# PUT /update-user/ 1
# API 4

@app.put("/update-user/{id}")
def update_user(id: int, user: User):
    cursor.execute(
        """
        update users
        set name = %s, email = %s, age = %s
        where id = %s
        returning *
        
        """,
        (user.name, user.email, user.age, id)
    )

    updated_user = cursor.fetchone()
    conn.commit()

    if updated_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    
    return updated_user
    

#Delete user
# DELETE / delete-user/ 7
# API 5

@app.delete("/delete-user/{id}")
def delete_user(id: int):
    cursor.execute("delete from users where id = %s returning *", (id,))

    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    
    return deleted_user




################################ ORDERS ########################################################

# API 1
# Get all orders
@app.get("/orders")
def get_orders():
    cursor.execute("select * from orders")
    orders = cursor.fetchall()
    
    return orders



# API 2
# Get order by id
@app.get("/orders/{id}")
def get_order(id: int):
    cursor.execute("select * from orders where id = %s", (id,))
    order = cursor.fetchone()

    if order is None:
        raise HTTPException(status_code=404, detail =  "Order not found")
    
    return order



# API3
# Get Orders for one user
@app.get("/users/{id}/orders")
def get_user_orders(id: int):
    cursor.execute(
        """
        select users.name, orders.id as order_id, orders.product_name, orders.price
        from users
        inner join orders
        on users.id = orders.user_id
        where users.id = %s
        order by orders.id
        """,
        (id,)
    )
    orders = cursor.fetchall()

    if len(orders) == 0:
        raise HTTPException(status_code=404, detail =  "No orders found for this user")
    
    return orders


# API 4
# Create Order

@app.post("/create-order", status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    cursor.execute(
        """
        insert into orders (user_id, product_name, price)
        values ( %s, %s, %s)
        returning *
        """,
        (order.user_id, order.product_name, order.price)
    )

    new_order = cursor.fetchone()
    conn.commit()

    return new_order


# API 5
# Delete Order

@app.delete("/delete-order/{id}")
def delete_order(id: int):
    cursor.execute(
        "delete from orders where id = %s returning *", (id,)
    )

    deleted_order = cursor.fetchone()
    conn.commit()

    if deleted_order is None:
        raise HTTPException(status_code=404, detail = "Order not found")
    
    return {
        "message": "Order deleted successfully",
        "deleted_order": deleted_order
    }


################################ USERS & ORDERS ########################################################

# API 1
# Search users by name

@app.get("/search-users")
def search_users(name: str):
    cursor.execute(
        """
        select * from users
        where name ilike %s
        order by id
        """,
        (f"%{name}%",)
    )

    users = cursor.fetchall()

    if len(users) == 0:
        raise HTTPException(status_code=404, detail = "No Users found")
    
    return users

# API 2
# Users by Minimum Age

@app.get("/users-age")
def users_by_age(min_age: int): 
    cursor.execute(
        """
        select * from users
        where age >= %s
        order by age
        """,
        (min_age,)
    )

    users = cursor.fetchall()

    if len(users) == 0:
        raise HTTPException(status_code=404, detail = "No Users found")
    
    return users


# API 3
# Orders by minimum prices

@app.get("/orders-by-price")
def orders_by_price(min_price: float):
    cursor.execute(
        """
        select * from orders
        where price >= %s
        order by price desc
        """,
        (min_price,)
    )

    orders = cursor.fetchall()

    if len(orders) == 0:
        raise HTTPException(status_code=404, detail = "No Orders found")
    
    return orders



# API 4
# Orders by user ID

@app.get("/orders-by-users/{user_id}")
def orders_by_users(user_id: int):
    cursor.execute(
        """
        select users.id as user_id, 
            users.name,
            orders.id as order_id,
            orders.product_name,
            orders.price
        from users
        inner join orders
        on users.id = orders.user_id
        where users.id = %s
        order by orders.id
        """,
        (user_id,)
    )

    orders = cursor.fetchall()

    if len(orders) == 0:
        raise HTTPException(status_code=404, detail = "No Orders found for this user")
    
    return orders