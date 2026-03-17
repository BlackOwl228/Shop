from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.dependencies.users import get_current_admin, get_current_seller, get_current_user
from src.core.resources.db import get_db, get_redis
from src.core.resources.redis import RedisClient
from src.models.users import Seller, User
from src.services.admin import AdminService
from src.services.auth import AuthService
from src.services.cart import CartService
from src.services.favorites import FavoritesService
from src.services.orders import OrderService
from src.services.products import ProductService
from src.services.public import PublicService
from src.services.review import ReviewService
from src.services.tokens import TokenService
from src.services.users import UserService


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


def get_product_service(seller: Seller = Depends(get_current_seller), db: Session = Depends(get_db)):
    return ProductService(db, seller)


def get_token_service(db: Session = Depends(get_db), redis: RedisClient = Depends(get_redis)):
    return TokenService(db, redis)


def get_cart_service(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CartService(db, user)


def get_review_service(author: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReviewService(db, author)


def get_user_service(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db, user)


def get_favorites_service(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return FavoritesService(db, user)


def get_admin_service(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return AdminService(db, admin)


def get_public_service(db: Session = Depends(get_db)):
    return PublicService(db)


def get_order_service(buyer: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return OrderService(db, buyer)
