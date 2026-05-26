from fastapi import APIRouter, HTTPException, status, Query
from database import cursor, conn
from models import User, LoginUser, UpdateUser
from auth import hash_password, verify_password, authenticate_user
import logging
from utils import build_user_response

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
    logger.info(f"[Users] Fetch users page = {page}, limit = {limit}")

    offset = (page - 1) * limit
    cursor.execute("select id, name, email, age, created_at from users order by id limit %s offset %s", (limit, offset))
    
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
    logger.info(f"[Users] Search users by name = {name}")
    cursor.execute(
        """
        select id, name, email, age, created_at
        from users
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
    logger.info(f"[Users] Filter users by min_age = {min_age}")
    cursor.execute(
        """
        select id, name, email, age, created_at
        from users
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
    logger.info(f"[Users] Sort users order = {order}")

    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail = {"error": "Order must be asc or desc"}
        )
    
    query = f"""
        select id, name, email, age, created_at
        from users
        order by age {order.upper()}
        """
    
    cursor.execute(query)

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
    logger.info(f"[AUTH] Login attempt email={user.email}")

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
        logger.warning(f"[AUTH] Login failed user not found for email = {user.email}")
        raise HTTPException(
            status_code=404,
            detail={"error": "User not found"}
        )
    
    is_password_valid = verify_password(
        user.password,
        existing_user["password"]
    )

    if not is_password_valid:
        logger.warning(f"[AUTH] Login failed invalid password for email = {user.email}")
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid Password"}
        )
    
    logger.info(f"[AUTH] Login successful for email = {user.email}")

    # return {
    #     "message": "Login successful",
    #     "user": {
    #         "id": existing_user["id"],
    #         "name": existing_user["name"],
    #         "email": existing_user["email"],
    #         "age": existing_user["age"]
    #     }
    # }

    return {"user": build_user_response(existing_user)}


# me route API
@router.get("/me")
def get_current_user(email: str, password: str):
    logger.info(f"[AUTH] Fetch current user email = {email}")

    user = authenticate_user(email, password, cursor)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid email or password"}
        )
    
    # return {
    #     "id": user["id"],
    #     "name": user["name"],
    #     "email": user["email"],
    #     "age": user["age"]
    # }

    return build_user_response(user)



# GET user by id
# GET /users/ 1
#API 2

@router.get("/{id}")
def get_user(id: int):
    logger.info(f"[USERS] Fetch user id={id}")
    cursor.execute("select id, name, email, age, created_at from users where id = %s", (id,))
    user = cursor.fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail = {"error": "User not found"})
    
    return user


#Create user
# POST /create-user
#API 3

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    logger.info("[USERS] Create new user")

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
def update_user(id: int, user: UpdateUser):
    logger.info(f"[USERS] Update user id={id}")
    cursor.execute(
        """
        update users
        set name = %s, email = %s, age = %s
        where id = %s
        returning id, name, email, age
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
    logger.info(f"[USERS] Delete user id={id}")
    cursor.execute("delete from users where id = %s returning id, name, email, age", (id,))

    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user is None:
        raise HTTPException(status_code=404, detail = {"error": "User not found"})
    
    return deleted_user



# User Order count API
@router.get("/{id}/order-count")
def get_user_order_count(id: int):
    logger.info(f"[USERS] Fetch order count user_id={id}")
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

