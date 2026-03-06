import os
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from models.tokens import RefreshToken

SecretKey = os.getenv("SECRET_KEY")
Algorithm = "HS256"
access_time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
RefreshTokenExpireDays = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class TokenService:
    def __init__(self, db: Session):
        self.db = db

    def create_access_token(user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=access_time)

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
        token = secrets.token_hex(32)
        expires_at = datetime.now(UTC) + timedelta(days=RefreshTokenExpireDays)
        new_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
        self.db.add(new_token)
        self.db.commit()

        return token

    def delete_refresh_token(self, token: str):
        refresh_token = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if refresh_token:
            self.db.delete(refresh_token)
            self.db.commit()
        else:
            HTTPException(status_code=401, detail="Invalid token")

    def check_refresh_token(self, token):
        refresh_token = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Wrong token, login again")

        return refresh_token.user_id
