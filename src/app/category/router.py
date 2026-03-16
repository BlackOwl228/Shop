from fastapi import APIRouter, Depends, Path

from src.core.depends import get_product_service, get_public_service
from src.services.products import ProductService
from src.services.public import PublicService

from .schemas import CategoriesPesponse

router = APIRouter(tags=["Category"])


# Пагинация при необходимости
@router.get("/categories", response_model=CategoriesPesponse)
def get_all_categories(public_service: PublicService = Depends(get_public_service)):
    categories = public_service.get_categories()
    return {"categories": categories}


@router.post("/products/{product_id}/categories/{category_id}", status_code=204)
def add_product_to_category(
    product_id: int = Path(...),
    category_id: int = Path(...),
    product_service: ProductService = Depends(get_product_service),
):
    product_service.change_product_category(product_id=product_id, category_id=category_id)
