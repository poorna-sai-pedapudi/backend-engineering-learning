def build_user_response(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "age": user["age"], 
        "created_at": user.get("created_at")
    }