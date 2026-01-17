from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from models import User
from core.db import get_db
from core.utils import templates
from core.security import get_current_user_cookie

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