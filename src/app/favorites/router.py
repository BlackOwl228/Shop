from fastapi import APIRouter, Depends, Path

from src.core.dependencies.services import get_favorites_service
from src.core.dependencies.users import get_current_user
from src.models.users import User
from src.services.favorites import FavoritesService

router = APIRouter(tags=["Favorites"])


@router.post("/favorites/{product_id}", status_code=201)
def add_product_to_favorites(
    product_id: int = Path(...),
    user: User = Depends(get_current_user),
    favorites_service: FavoritesService = Depends(get_favorites_service),
):
    favorites_service.add_to_favorites(user_id=user.id, product_id=product_id)

    return {"status": f"Product {product_id} add to your favorites"}


# Нужно добавить респонс модель
@router.get("/favorites", status_code=200)
def get_my_favorites(
    user: User = Depends(get_current_user),
    favorites_service: FavoritesService = Depends(get_favorites_service),
):
    return favorites_service.get_favorites(user_id=user.id)


@router.delete("/favorites/{product_id}", status_code=204)
def delete_product_from_favorites(
    product_id: int = Path(...),
    user: User = Depends(get_current_user),
    favorites_service: FavoritesService = Depends(get_favorites_service),
):
    favorites_service.delete_from_favorites(user_id=user.id, product_id=product_id)

    return {"status": f"Product {product_id} delete from your favorites"}
