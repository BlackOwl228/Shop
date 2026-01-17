from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from core import get_db
from models import Product
from services.search import _search_products
from schemas.searching import OrderingParam, SortingProducts
from core.utils import templates

router = APIRouter(prefix='/front', tags=["FOR WEBSITE"])

@router.get("/search")
def search_page(
    request: Request,
    q: str | None = None,
    db: Session = Depends(get_db)
):
    products = []

    if q:
        products = (
            db.query(Product)
            .filter(Product.name.ilike(f"%{q}%"))
            .all()
        )

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "products": products,
            "query": q
        }
    )

@router.get("/search")
def advanced_search(name: str | None = Query(None),
                    price_from: float | None = Query(None),
                    price_to: float | None = Query(None),
                    seller_id: int | None = Query(None),
                    sort: SortingProducts = Query("created_at"),
                    order: OrderingParam = Query("asc"),
                    page: int = Query(ge=1, default=1),
                    db: Session = Depends(get_db)):
    return _search_products(name, price_from, price_to, seller_id, sort, order, page, Session)