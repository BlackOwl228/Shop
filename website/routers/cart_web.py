from app.auth.security import get_current_user_cookie
from fastapi import APIRouter, Depends, Request

from src.models.users import User

from ..config import templates

router = APIRouter(tags=["FOR WEBSITE"])


@router.get("/front/cart")
def cart_page(request: Request, user: User = Depends(get_current_user_cookie)):
    cart_items = user.cart_products
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items})


@router.get("/front/favorites")
def favorites_page(request: Request, user: User = Depends(get_current_user_cookie)):
    fav_items = user.favorite_products
    return templates.TemplateResponse("favorites.html", {"request": request, "cart_items": fav_items})
