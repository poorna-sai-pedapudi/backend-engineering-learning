from fastapi import APIRouter, HTTPException, status
from database import cursor, conn
from models import Order


router = APIRouter()


################################ ORDERS ########################################################

# API 1
# Get all orders
@router.get("/")
def get_orders():
    cursor.execute("select * from orders")
    orders = cursor.fetchall()
    
    return orders



################################ USERS & ORDERS ########################################################


# API 4
# Orders by user ID

@router.get("/user/{user_id}")
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



# API 3
# Orders by minimum prices

@router.get("/filter/price")
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



# API 2
# Get order by id
@router.get("/{id}")
def get_order(id: int):
    cursor.execute("select * from orders where id = %s", (id,))
    order = cursor.fetchone()

    if order is None:
        raise HTTPException(status_code=404, detail =  "Order not found")
    
    return order



# API 3
# Get Orders for one user
# @router.get("/user/{user_id}")
# def get_user_orders(id: int):
#     cursor.execute(
#         """
#         select users.name, orders.id as order_id, orders.product_name, orders.price
#         from users
#         inner join orders
#         on users.id = orders.user_id
#         where users.id = %s
#         order by orders.id
#         """,
#         (id,)
#     )
#     orders = cursor.fetchall()

#     if len(orders) == 0:
#         raise HTTPException(status_code=404, detail =  "No orders found for this user")
    
#     return orders


# API 4
# Create Order

@router.post("/", status_code=status.HTTP_201_CREATED)
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

@router.delete("/{id}")
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




