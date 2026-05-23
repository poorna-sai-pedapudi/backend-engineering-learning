from fastapi import APIRouter, HTTPException, status, Query
from database import cursor, conn
from models import User, LoginUser
from auth import hash_password, verify_password
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


################################ USERS ########################################################

#we get all users 
# GET /users
#API 1

@router.get("/")
def get_users(
    page:int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=50)
    ):
    logger.info(f"Fetching all users page = {page}, limit = {limit}")

    offset = (page - 1) * limit
    cursor.execute("select * from users order by id limit %s offset %s", (limit, offset))
    
    users = cursor.fetchall()
    cursor.execute("select count(*) as total from users")
    total = cursor.fetchone()["total"]

    return {
        "page": page,
        "limit": limit,
        "count": len(users),
        "total": total,
        "data": users
    }


################################ USERS & ORDERS ########################################################

# API 1
# Search users by name

@router.get("/search")
def search_users(name: str):
    print("Fetching user by name...")
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
    
    return {
        "filter": "name",
        "value": name, 
        "count": len(users),
        "data": users
    }

# API 2
# Users by Minimum Age

@router.get("/filter/age")
def users_by_age(min_age: int): 
    print("Fetching by user age...")
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
    
    return {
        "filter": "min_age",
        "value": min_age,
        "count": len(users),
        "data": users
    }


# Adding USER sorting API
@router.get("/sorted")
def get_users_sorted(order: str = "asc"):
    print(f"Fetching users sorted by age, order = {order}")

    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail = {"error": "Order must be asc or desc"}
        )
    
    cursor.execute(
        """
        select * from users
        order by age {order.upper()}
        """
    )

    users = cursor.fetchall()

    return {
        "sort_by": "age",
        "order": order,
        "count": len(users),
        "data": users
    }


# Login API for users
@router.post("/login")
def login_user(user: LoginUser):
    print("Logging in user..")

    cursor.execute(
        """
        select id, name, email, age, password
        from users
        where email = %s
        """,
        (user.email,)
    )

    existing_user = cursor.fetchone()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "User not found"}
        )
    
    is_password_valid = verify_password(
        user.password,
        existing_user["password"]
    )

    if not is_password_valid:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid Password"}
        )
    

    return {
        "message": "Login successful",
        "user": {
            "id": existing_user["id"],
            "name": existing_user["name"],
            "email": existing_user["email"],
            "age": existing_user["age"]
        }
    }


# GET user by id
# GET /users/ 1
#API 2

@router.get("/{id}")
def get_user(id: int):
    logger.info(f"Fetching user with id= {id}")
    cursor.execute("select * from users where id = %s", (id,))
    user = cursor.fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail = {"error": "User not found"})
    
    return user


#Create user
# POST /create-user
#API 3

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    logger.info("Creating new user")

    hashed_password = hash_password(user.password)
    cursor.execute(
        """
        insert into users (name, email, age, password) 
        values (%s, %s, %s, %s) 
        returning id, name, email, age
        """,
        (user.name, user.email, user.age, hashed_password)
    )
    
    new_user = cursor.fetchone()
    conn.commit() #to save the changes permanently

    return new_user

#Updating the user
# PUT /update-user/ 1
# API 4

@router.put("/{id}")
def update_user(id: int, user: User):
    print(f"Updating user with id: {id}")
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
        raise HTTPException(status_code=404, detail = {"error": "User not found"})
    
    return updated_user
    

#Delete user
# DELETE / delete-user/ 7
# API 5

@router.delete("/{id}")
def delete_user(id: int):
    print(f"Deleting user with id: {id}")
    cursor.execute("delete from users where id = %s returning *", (id,))

    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user is None:
        raise HTTPException(status_code=404, detail = {"error": "User not found"})
    
    return deleted_user



# User Order count API
@router.get("/{id}/order-count")
def get_user_order_count(id: int):
    print("Fetching the count...")
    cursor.execute(
        """
        SELECT users.id AS user_id,
               users.name,
               COUNT(orders.id) AS total_orders
        FROM users
        LEFT JOIN orders
        ON users.id = orders.user_id
        WHERE users.id = %s
        GROUP BY users.id, users.name
        """,
        (id,)
    )

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail={"error": "User not found"})

    return result

