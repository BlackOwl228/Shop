from argon2 import PasswordHasher
from sqlalchemy.orm import Session, joinedload

from src.core.logs.exceptions import SellerNotFoundError, UserNotFoundError
from src.core.ratelimit import rate_limit_redis
from src.models.users import User
from src.services.tokens import TokenService


def get_current_user_from_jwt(token: str, db: Session):
    user_id = TokenService.decode_access_token(token)
    user = db.query(User).get(user_id)
    if not user:
        raise UserNotFoundError(user_id=user_id)
    rate_limit_redis(user_id=user_id)
    return user


def get_seller_from_jwt(token: str, db: Session):
    user_id = TokenService.decode_access_token(token)
    user = db.query(User).options(joinedload(User.seller)).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(user_id=user_id)
    if not user.seller:
        raise SellerNotFoundError(seller_id=user.seller.id)
    return user.seller


def get_admin_from_jwt(token: str, db: Session):
    user_id = TokenService.decode_access_token(token)
    admin = db.query(User).filter(User.id == user_id, User.is_admin).first()
    if not admin:
        raise UserNotFoundError(user_id=user_id)
    return admin


ph = PasswordHasher()


def hash_password(password: str):
    return ph.hash(password)


def check_password(password: str, hashed_password: str):
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False
