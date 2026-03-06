from fastapi import APIRouter, Depends, Path

from core.depends import get_current_user, get_favorites_service
from models.users import User
from services.favorites import FavoritesService

router = APIRouter(tags=["Favorites"])


@router.post("/favorites/{product_id}", status_code=204)
def add_product_to_favorites(
    product_id: int = Path(...), favorites_service: FavoritesService = Depends(get_favorites_service)
):
    favorites_service.add_to_favorites(product_id)


@router.get("/favorites", status_code=200)
def get_my_favorites(user: User = Depends(get_current_user)):
    return user.favorite_products


@router.delete("/favorites/{product_id}", status_code=204)
def delete_product_from_favorites(
    product_id: int = Path(...), favorites_service: FavoritesService = Depends(get_favorites_service)
):
    favorites_service.delete_from_favorites(product_id)
