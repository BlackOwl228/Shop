from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from core.db import get_db

from .token.access import get_current_user_from_jwt, get_seller_from_jwt, get_admin_from_jwt

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(
    token: str = Depends(oauth_scheme),
    db: Session = Depends(get_db),
):
    return get_current_user_from_jwt(token, db)

def get_current_seller(
    token: str = Depends(oauth_scheme),
    db: Session = Depends(get_db),
):
    return get_seller_from_jwt(token, db)

def get_current_admin(
    token: str = Depends(oauth_scheme),
    db: Session = Depends(get_db),
):
    return get_admin_from_jwt(token, db)


def get_current_user_cookie(
    request: Request,
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)
    return get_current_user_from_jwt(token, db)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)