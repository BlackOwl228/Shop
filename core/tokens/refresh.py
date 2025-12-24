from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.tokens import RefreshToken
from datetime import datetime, timedelta, timezone
import secrets, os

RefreshTokenExpireDays = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

def create_refresh_token(user_id: int,
                         db: Session
                         ) -> str:
    token = secrets.token_hex(64)
    expires_at = datetime.now(timezone.utc) + timedelta(days=RefreshTokenExpireDays)
    new_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(new_token)
    db.commit()

    return token

def delete_refresh_token(token: str,
                         db: Session):
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if refresh_token:
        db.delete(refresh_token)
        db.commit()
    else:
        HTTPException(status_code=401, detail="Invalid token")