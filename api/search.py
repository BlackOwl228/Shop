from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.users import User
from models.products import Product
from .params.search import OrderingParam, SortingProducts, ProductsMap
from core.db import get_db

router = APIRouter(prefix='/search', tags=["Search"])

@router.get('')
def search_products(name: str | None = Query(None),
                    price_from: float | None= Query(None),
                    price_to: float | None= Query(None),
                    seller_id: int | None= Query(None),
                    sort: SortingProducts = Query("created_at"),
                    order: OrderingParam = Query("asc"),
                    page: int = Query(ge=1, default=1),
                    db: Session = Depends(get_db)):
    query = db.query(Product)

    if name is not None:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if price_from is not None:
        query = query.filter(Product.price >= price_from)
    if price_to is not None:
        query = query.filter(Product.price <= price_to)
    if seller_id is not None:
        query = query.filter(Product.seller_id == seller_id)

    column = ProductsMap[sort]
    query = query.order_by(column.desc() if order == OrderingParam.desc else column.asc())

    query = query.limit(50).offset(50*(page-1))
    result = query.all()

    return result