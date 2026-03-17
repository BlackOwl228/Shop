from fastapi import APIRouter, Depends, Query

from src.core.dependencies.services import get_public_service
from src.services.public import PublicService

from .schemas import ProductSorting, SearchResponse

router = APIRouter(tags=["Search"])


@router.get("/search", status_code=200, response_model=SearchResponse)
def search_products(
    q: str | None = Query(None),
    category_id: int | None = Query(None),
    seller_id: int | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    sort: ProductSorting = Query(ProductSorting.relevance),
    page: int = Query(1, ge=1),
    size: int = Query(30, ge=1, le=100),
    public_service: PublicService = Depends(get_public_service),
):
    result, has_more = public_service.search_products(
        q=q,
        category_id=category_id,
        seller_id=seller_id,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        page=page,
        size=size,
    )

    return {"products": result, "has_more": has_more}
