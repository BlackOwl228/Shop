from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.core.logs.exceptions import InvalidTokenError
from src.core.resources.db import get_db
from src.core.security import get_admin_from_jwt, get_current_user_from_jwt, get_seller_from_jwt

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
        raise InvalidTokenError()
    return get_current_user_from_jwt(token, db)
