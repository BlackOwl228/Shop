from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.app.search.schemas import OrderingParam, ProductsMap, SortingProducts
from src.core.resources.db import get_db
from src.models.products import Product
from src.rules.product_rules import available_products

from ..config import templates

router = APIRouter(prefix="/front", tags=["FOR WEBSITE"])


@router.get("/search")
def search_page(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    products = []

    if q:
        products = db.query(Product).filter(Product.name.ilike(f"%{q}%")).all()

    return templates.TemplateResponse("search.html", {"request": request, "products": products, "query": q})


@router.get("/search")
def advanced_search(
    name: str | None = Query(None),
    price_from: float | None = Query(None),
    price_to: float | None = Query(None),
    seller_id: int | None = Query(None),
    sort: SortingProducts = Query("created_at"),
    order: OrderingParam = Query("asc"),
    page: int = Query(ge=1, default=1),
    db: Session = Depends(get_db),
):
    query = available_products(db.query(Product))

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

    query = query.limit(50).offset(50 * (page - 1))
    result = query.all()

    if result:
        return result
    else:
        return None
