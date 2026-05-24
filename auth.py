import bcrypt

def hash_password(password: str):
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")

def verify_password(password: str, hashed_password: str):

    password_bytes = password.encode("utf-8")

    hashed_password_bytes = hashed_password.encode("utf-8")
    
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def authenticate_user(email: str, password: str, cursor):

    cursor.execute(
        """
        select id, name, email, age, password
        from users
        where email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    if user is None:
        return None
    
    is_password_valid = verify_password(password, user["password"])

    if not is_password_valid:
        return None
    
    return user
