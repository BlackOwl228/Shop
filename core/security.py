from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.db import get_db

from datetime import datetime, timedelta
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow()}
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

from jose import jwt
def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id:
            return int(payload["sub"])
        else:
            raise Exception
    except Exception:
        raise HTTPException(status_code=401, detail="Token isn't correct")

from models.users import User
from services.checking import check_user_exists
def get_current_user(user_id: int = Depends(decode_access_token),
                     db: Session = Depends(get_db)):    
    user = db.query(User).filter(User.id == user_id).first()

    check_user_exists(user)

    return user

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)