from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.dependencies.users import get_current_admin
from src.core.resources.db import get_db, get_redis
from src.core.resources.redis import RedisClient
from src.models.users import User
from src.services.admin import AdminService
from src.services.auth import AuthService
from src.services.cart import CartService
from src.services.category import CategoryService
from src.services.favorites import FavoritesService
from src.services.orders import OrderService
from src.services.products import ProductService
from src.services.review import ReviewService
from src.services.search import SearchService
from src.services.tokens import TokenService
from src.services.users import UserService


def get_admin_service(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return AdminService(db)


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


def get_cart_service(db: Session = Depends(get_db)):
    return CartService(db)


def get_category_service(db: Session = Depends(get_db)):
    return CategoryService(db)


def get_favorites_service(db: Session = Depends(get_db)):
    return FavoritesService(db)


def get_order_service(db: Session = Depends(get_db)):
    return OrderService(db)


def get_product_service(db: Session = Depends(get_db)):
    return ProductService(db)


def get_review_service(db: Session = Depends(get_db)):
    return ReviewService(db)


def get_search_service(db: Session = Depends(get_db)):
    return SearchService(db)


def get_token_service(db: Session = Depends(get_db), redis: RedisClient = Depends(get_redis)):
    return TokenService(db, redis)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
