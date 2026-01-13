from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from core import get_db
from models import Product
from schemas.searching import OrderingParam, SortingProducts, SearchingResponse
from services.search import _search_products

router = APIRouter(tags=["Search"])

@router.get('/search', status_code=200, response_model=SearchingResponse)
def search_products(name: str | None = Query(None, example="Keyboard"),
                    price_from: float | None = Query(None, example=5000),
                    price_to: float | None = Query(None, example=15000),
                    seller_id: int | None = Query(None, example=123),
                    sort: SortingProducts = Query("created_at"),
                    order: OrderingParam = Query("asc"),
                    page: int = Query(ge=1, default=1),
                    db: Session = Depends(get_db)):
    return _search_products(name, price_from, price_to, seller_id, sort, order, page, Session)

@router.get('/home', status_code=200, response_model=SearchingResponse)
def search_products(db: Session = Depends(get_db)):
    products = db.query(Product).order_by(func.random()).limit(20).all()
    return {"products": products}