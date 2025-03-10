def map_user(db_user):
    return {
        "username": db_user["username"],
        "role": db_user["role"]
    }
