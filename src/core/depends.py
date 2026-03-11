from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.security import get_current_admin, get_current_seller, get_current_user
from core.db import get_db
from models.users import Seller, User
from services.admin import AdminService
from services.auth import AuthService
from services.favorites import FavoritesService
from services.orders import OrderService
from services.products import ProductService
from services.public import PublicService
from services.review import ReviewService
from services.tokens import TokenService
from services.users import UserService


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


def get_product_service(seller: Seller = Depends(get_current_seller), db: Session = Depends(get_db)):
    return ProductService(db, seller)


def get_token_service(db: Session = Depends(get_db)):
    return TokenService(db)


def get_cart_service(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ProductService(db, user)


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
