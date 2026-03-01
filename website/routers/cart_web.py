from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from src.models.users import User
from src.core.db import get_db
from app.auth.security import get_current_user_cookie
from ..config import templates

router = APIRouter(tags=["FOR WEBSITE"])

@router.get("/front/cart")
def cart_page(request: Request,
              user: User = Depends(get_current_user_cookie),
              db: Session = Depends(get_db)):
    cart_items = user.cart_products
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items})

@router.get("/front/favorites")
def cart_page(request: Request,
              user: User = Depends(get_current_user_cookie),
              db: Session = Depends(get_db)):
    fav_items = user.favorite_products
    return templates.TemplateResponse("favorites.html", {"request": request, "cart_items": fav_items})