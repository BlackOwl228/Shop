from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
SecretKey = os.getenv("SECRET_KEY")
Algorithm = "HS256"
AccessTokenExpireMinutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=AccessTokenExpireMinutes)

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