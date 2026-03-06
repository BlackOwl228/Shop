from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.search.schemas import OrderingParam, ProductsMap, SortingProducts
from models.collections import Category
from models.products import Product, ProductVariant
from models.reviews import Review
from rules.product_rules import available_products


class PublicService:
    def __init__(self, db: Session):
        self.db = db

    def get_reviews_to_product(self, product_id: int, page: int, size: int, order: OrderingParam):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        reviews = (
            self.db.query(Review)
            .options(joinedload(Review.author))
            .filter(Review.product_id == product_id)
            .order_by(Review.created_at.desc() if order == OrderingParam.desc else Review.created_at.asc())
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
        min_price: float | None,
        max_price: float | None,
        sort: SortingProducts,
        order: OrderingParam,
        page: int,
        size: int,
    ):
        query = available_products(self.db.query(ProductVariant).options(joinedload(ProductVariant.product)))
        if q:
            query = query.filter(Product.name.ilike(f"%{q}%"))
            """
            query = query.filter(
                (Product.name.ilike(f"%{q}%")) | 
                (ProductVariant.name.ilike(f"%{q}%"))
            ) """  # Это доп вариант

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if min_price:
            query = query.filter(ProductVariant.price >= min_price)

        if max_price:
            query = query.filter(ProductVariant.price <= max_price)

        column = ProductsMap[sort]
        query = query.order_by(column.desc() if order == OrderingParam.desc else column.asc())

        query = query.limit(size + 1).offset(size * (page - 1))
        result = query.all()

        has_more = len(result) > size
        result = result[:size]

        return result, has_more
