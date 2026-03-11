from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.products.schemas import ProductCartResponse
from app.search.schemas import ProductSorting, ProductsSortingMap
from core.db import cache_get, cache_set
from models.collections import Category
from models.products import Product, ProductVariant
from models.reviews import Review
from rules.product_rules import available_products


class PublicService:
    def __init__(self, db: Session):
        self.db = db

    def set_product_cache(self, id: int, data):
        product_dict = ProductCartResponse.model_validate(data).model_dump()
        cache_set(f"products:{id}", product_dict, ttl=600)

    def get_product_cache(self, id: int):
        return cache_get(f"products:{id}")

    def get_reviews_to_product(self, product_id: int, page: int, size: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        reviews = (
            self.db.query(Review)
            .options(joinedload(Review.author))
            .filter(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
            .limit(size + 1)
            .offset((page - 1) * size)
            .all()
        )
        has_more = True if len(reviews) > size else False

        return reviews[:size], has_more

    def get_full_product_by_id(self, product_id: int):
        product = (
            self.db.query(Product)
            .options(joinedload(Product.variants))
            .filter(Product.id == product_id)
            .first()
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    def get_categories(self):
        return self.db.query(Category).all()

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
        if q:
            ts_query = func.plainto_tsquery("russian", q)
            rank = func.ts_rank(Product.search_vector, ts_query)
            if sort == ProductSorting.relevance:
                query = query.order_by(rank.desc(), Product.rating.desc())
            else:
                query = query.order_by(ProductsSortingMap[sort])
        else:
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
