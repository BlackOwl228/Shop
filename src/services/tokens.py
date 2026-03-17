import os
import secrets
from datetime import UTC, datetime, timedelta

from jose import jwt
from sqlalchemy.orm import Session

from src.core.logs.exceptions import InvalidTokenError, UserNotFoundError
from src.core.resources.redis import RedisClient, RedisKeys
from src.models.users import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
EMAIL_TOKEN_EXPIRE_HOURS = int(os.getenv("VERIFICATION_EMAIL_TOKEN_HOURS"))


class TokenService:
    def __init__(self, db: Session, redis: RedisClient):
        self.db = db
        self.redis = redis

    @staticmethod
    def create_access_token(user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {"sub": str(user_id), "exp": expire, "iat": datetime.now(UTC)}

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> int:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError()

        return int(user_id)

    def create_refresh_token(self, user_id: int) -> str:
        refresh_token = secrets.token_urlsafe(32)
        key = RedisKeys.refresh_token(refresh_token)
        token_ttl = REFRESH_TOKEN_EXPIRE_DAYS * 86400
        self.redis.set(key, user_id, ttl=token_ttl)

        return refresh_token

    def delete_refresh_token(self, refresh_token: str):
        key = RedisKeys.refresh_token(refresh_token)
        stored_token = self.redis.get(key)
        if not stored_token:
            raise InvalidTokenError()

        self.redis.delete(key)

    def check_refresh_token(self, refresh_token: str):
        key = RedisKeys.refresh_token(refresh_token)
        user_id_from_refresh = self.redis.get(key)
        if not user_id_from_refresh:
            raise InvalidTokenError()

        return int(user_id_from_refresh)

    def create_email_token(self, user_id: int):
        email_token = secrets.token_urlsafe(32)
        key = RedisKeys.email_token(email_token)
        token_ttl = EMAIL_TOKEN_EXPIRE_HOURS * 3600
        self.redis.set(key, user_id, ttl=token_ttl)

        return email_token

    def verify_email_by_token(self, email_token: str):
        key = RedisKeys.email_token(email_token)
        user_id_from_email = int(self.redis.get(key))
        if not user_id_from_email:
            raise InvalidTokenError()

        user = self.db.query(User).filter(User.id == user_id_from_email).first()
        if not user:
            raise UserNotFoundError(user_id=user_id_from_email)
        user.email_verified = True
        self.db.commit()

        self.redis.delete(key)
