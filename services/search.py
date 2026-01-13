from sqlalchemy.orm import Session

from models import Product
from schemas.searching import OrderingParam, SortingProducts, ProductsMap, SearchingResponse

def _search_products(name: str | None,
                     price_from: float | None,
                     price_to: float | None,
                     seller_id: int | None,
                     sort: SortingProducts,
                     order: OrderingParam,
                     page: int,
                     db: Session):
    
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
    return query.all()