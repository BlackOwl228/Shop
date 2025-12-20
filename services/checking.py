from fastapi import HTTPException

def check_user_exists(user):
    if not user:
        raise HTTPException(status_code=401, detail="User not found")