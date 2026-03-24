from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.app.search.schemas import ProductSorting, ProductsSortingMap
from src.models.products import Product, ProductVariant
from src.rules.product_rules import available_products


class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def search_products(
        self,
        q: str | None,
        category_id: int | None,
        seller_id: int | None,
        min_price: float | None,
        max_price: float | None,
        sort: ProductSorting,
        page: int,
        size: int,
    ):
        query = available_products(self.db.query(ProductVariant).options(joinedload(ProductVariant.product)))
        if q is not None:
            ts_query = func.plainto_tsquery("russian", q)
            rank = func.ts_rank(Product.search_vector, ts_query)
            if sort == ProductSorting.relevance:
                query = query.order_by(rank.desc(), Product.rating.desc())
            else:
                query = query.order_by(ProductsSortingMap[sort])
        elif sort != ProductSorting.relevance:
            query = query.order_by(ProductsSortingMap[sort])

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if seller_id:
            query = query.filter(Product.seller_id == seller_id)

        if min_price:
            query = query.filter(ProductVariant.price >= min_price)

        if max_price:
            query = query.filter(ProductVariant.price <= max_price)

        query = query.limit(size + 1).offset(size * (page - 1))
        result = query.all()

        has_more = len(result) > size
        result = result[:size]

        return result, has_more
