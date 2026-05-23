from fastapi import APIRouter, HTTPException, status
from database import cursor, conn
from models import Order


router = APIRouter()


################################ ORDERS ########################################################

# API 1
# Get all orders
@router.get("/")
def get_orders(page: int = 1, limit: int = 5):
    print("Fetching all orders page:{page}, limit:{limit}")

    offset = (page - 1) * limit

    cursor.execute(
        """
        select * from orders
        order by id
        limit %s offset %s
        """,
        (limit, offset)
    )

    orders = cursor.fetchall()

    cursor.execute("select count(*) as total from orders")
    total = cursor.fetchone()["total"]
    
    return {
        "page": page,
        "limit": limit,
        "count": len(orders),
        "total": total,
        "data": orders
    }



################################ USERS & ORDERS ########################################################


# API 4
# Orders by user ID

@router.get("/user/{user_id}")
def orders_by_users(user_id: int):
    print(f"Fetching order with id: {id}")
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
        raise HTTPException(status_code=404, detail = {"error": "No Orders found for this user"})
    
    return {
        "filter": "user_id",
        "value": user_id,
        "count": len(orders),
        "data": orders
    }

# Add Sorting API

@router.get("/sorted")
def get_orders_sorted(order:str = "asc"):
    print(f"Fetching orders sorted by price, order = {order}")

    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail={"error": "Order must be asc or desc"}
        )
    
    cursor.execute(
        f"""
        select * from orders
        order by price {order.upper()}
        """
    )

    orders = cursor.fetchall()

    return {
        "sort_by": "price",
        "order": order,
        "count": len(orders),
        "data": orders
    }


# API 3
# Orders by minimum prices

@router.get("/filter/price")
def orders_by_price(min_price: float):
    print("Fetching all orders by minimum price...")
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
        raise HTTPException(status_code=404, detail = {"error": "No Orders found"})
    
    return {
        "filter": "min_price",
        "value": min_price,
        "count": len(orders),
        "data": orders
    }



# User Total Spent API
@router.get("/user/{user_id}/total")
def get_user_total(user_id: int):
    print("Fetching total amount spent by user...")
    cursor.execute(
        """
        select users.id as user_id,
            users.name, 
            coalesce(sum(orders.price), 0) as total_spent
        from users 
        left join orders
        on users.id = orders.user_id
        where users.id = %s
        group by users.id, users.name
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail={"error": "User not found"})
    
    return result



# API 2
# Get order by id
@router.get("/{id}")
def get_order(id: int):
    print("Fetching all orders...")
    cursor.execute("select * from orders where id = %s", (id,))
    order = cursor.fetchone()

    if order is None:
        raise HTTPException(status_code=404, detail = {"error": "Order not found"})
    
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
    print("Creating new order...")
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
    print(f"Deleting order with id: {id}")
    cursor.execute(
        "delete from orders where id = %s returning *", (id,)
    )

    deleted_order = cursor.fetchone()
    conn.commit()

    if deleted_order is None:
        raise HTTPException(status_code=404, detail = {"error": "Order not found"})
    
    return {
        "message": "Order deleted successfully",
        "deleted_order": deleted_order
    }




