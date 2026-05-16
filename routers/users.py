from fastapi import APIRouter, HTTPException, status
from database import cursor, conn
from models import User

router = APIRouter()


################################ USERS ########################################################

#we get all users 
# GET /users
#API 1

@router.get("/")
def get_users():
    cursor.execute("select * from users order by id")
    users = cursor.fetchall()
    return users


################################ USERS & ORDERS ########################################################

# API 1
# Search users by name

@router.get("/search")
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

@router.get("/filter/age")
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




# GET user by id
# GET /users/ 1
#API 2

@router.get("/{id}")
def get_user(id: int):
    cursor.execute("select * from users where id = %s", (id,))
    user = cursor.fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    
    return user


#Create user
# POST /create-user
#API 3

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    cursor.execute("insert into users (name, email, age) values (%s, %s, %s) returning *",
        (user.name, user.email, user.age))
    
    new_user = cursor.fetchone()
    conn.commit() #to save the changes permanently

    return new_user

#Updating the user
# PUT /update-user/ 1
# API 4

@router.put("/{id}")
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

@router.delete("/{id}")
def delete_user(id: int):
    cursor.execute("delete from users where id = %s returning *", (id,))

    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    
    return deleted_user




