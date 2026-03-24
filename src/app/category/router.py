from fastapi import APIRouter, Depends, Path

from src.core.dependencies.services import get_category_service
from src.core.dependencies.users import get_current_seller
from src.models.users import Seller
from src.services.category import CategoryService

from .schemas import CategoriesPesponse

router = APIRouter(tags=["Category"])


# Пагинация при необходимости
@router.get("/categories", response_model=CategoriesPesponse)
def get_all_categories(category_service: CategoryService = Depends(get_category_service)):
    categories = category_service.get_categories()
    return {"categories": categories}


@router.post("/products/{product_id}/categories/{category_id}", status_code=201)
def add_product_to_category(
    product_id: int = Path(...),
    category_id: int = Path(...),
    seller: Seller = Depends(get_current_seller),
    category_service: CategoryService = Depends(get_category_service),
):
    category_service.change_product_category(
        seller_id=seller.id, product_id=product_id, category_id=category_id
    )

    return {"status": f"Product {product_id} add to category {category_id}"}
