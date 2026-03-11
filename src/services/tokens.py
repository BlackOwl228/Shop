import os
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from core.db import redis_delete, redis_get, redis_set
from models.users import User

SecretKey = os.getenv("SECRET_KEY")
Algorithm = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
EMAIL_TOKEN_EXPIRE_HOURS = int(os.getenv("VERIFICATION_EMAIL_TOKEN_HOURS"))


class TokenService:
    def __init__(self, db: Session):
        self.db = db

    def create_access_token(user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {"sub": str(user_id), "exp": expire, "iat": datetime.now(UTC)}

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
        except Exception as e:
            raise HTTPException(status_code=401, detail="Token isn't correct") from e

    def create_refresh_token(self, user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        key = "token:refresh:" + token
        token_ttl = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS).seconds
        redis_set(key, user_id, ttl=token_ttl)

        return token

    def delete_refresh_token(self, token: str):
        key = "token:refresh:" + token
        refresh_token = redis_get(key)
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Invalid token")

        redis_delete(token)

    def check_refresh_token(self, token: str):
        key = "token:refresh:" + token
        user_id_from_refresh = redis_get(key)
        if not user_id_from_refresh:
            raise HTTPException(status_code=401, detail="Wrong token, login again")

        return user_id_from_refresh

    def create_email_token(self, user_id: int):
        token = secrets.token_urlsafe(32)
        key = "token:email:" + token
        token_ttl = timedelta(hours=EMAIL_TOKEN_EXPIRE_HOURS).seconds
        redis_set(key, user_id, ttl=token_ttl)

        return token

    def verify_email_by_token(self, token: str):
        key = "token:email:" + token
        user_id_from_email = redis_get(key)
        if not user_id_from_email:
            raise HTTPException(status_code=404, detail="Token not found")

        user = self.db.query(User).filter(User.id == user_id_from_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.email_verified = True
        self.db.commit()

        redis_delete(key)
