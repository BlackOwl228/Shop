from datetime import datetime, timedelta, timezone
import os

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from jose import jwt

SecretKey = os.getenv("SECRET_KEY")
Algorithm = "HS256"
access_time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_time)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc)}
    
    return jwt.encode(payload, SecretKey, algorithm=Algorithm)

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            SecretKey,
            algorithms=[Algorithm],
        )
        user_id = payload.get("sub")
        if user_id:
            return int(payload["sub"])
        else:
            raise Exception
    except Exception:
        raise HTTPException(status_code=401, detail="Token isn't correct")
    
from models import User
    
def get_current_user_from_jwt(token: str, db: Session):
    user_id = decode_access_token(token)
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_seller_from_jwt(token: str, db: Session):
    user_id = decode_access_token(token)
    user = db.query(User).options(joinedload(User.seller)).filter(User.id == user_id).first()
    if not user or not user.seller:
        raise HTTPException(status_code=403, detail="User is not a seller")
    return user.seller

def get_admin_from_jwt(token: str, db: Session):
    user_id = decode_access_token(token)
    admin = db.query(User).filter(User.id==user_id, User.is_admin==True).first()
    if not admin:
        raise HTTPException(status_code=401, detail="You aren't admin")
    return admin