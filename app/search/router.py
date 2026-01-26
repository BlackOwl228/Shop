from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from core import get_db
from .schemas import OrderingParam, SortingProducts, SearchResponse, ProductsMap
from models import Product, ProductVariant
from domain.product_rules import available_products

router = APIRouter(tags=["Search"])

@router.get('/search', status_code=200, response_model=SearchResponse)
def search_products(q: str | None = Query(None),
                    category_id: int | None = Query(None),
                    min_price: float | None = Query(None),
                    max_price: float | None = Query(None),
                    sort: SortingProducts = Query(SortingProducts.rating),
                    order: OrderingParam = Query(OrderingParam.desc),
                    page: int = Query(1, ge=1),
                    size: int = Query(30, ge=1, le=100),
                    db: Session = Depends(get_db)
                    ):
    query = available_products(db.query(ProductVariant)
                               .options(joinedload(ProductVariant.product))
                               )
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price:
        query = query.filter(ProductVariant.price >= min_price)

    if max_price:
        query = query.filter(ProductVariant.price <= max_price)

    column = ProductsMap[sort]
    query = query.order_by(column.desc() if order == OrderingParam.desc else column.asc())

    query = query.limit(size+1).offset(size*(page-1))
    result = query.all()

    has_more = len(result) > size
    result = result[:size]

    return {"products": result, "has_more": has_more}