from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    CategoryNotFoundError,
    NotYourProductError,
    ProductNotFoundError,
)
from src.repos.category import CategoryRepo
from src.repos.products import ProductRepo


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepo(db)

    def get(self, category_id: int):
        category = self.repo.get(category_id=category_id)
        if not category:
            raise CategoryNotFoundError(category_id=category_id)
        return category

    def get_categories(self):
        return self.repo.get_all()

    def change_product_category(self, seller_id: int, product_id: int, category_id: int):
        product = ProductRepo(self.repo.db).get_product(product_id=product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        if product.seller_id != seller_id:
            raise NotYourProductError(seller_id=seller_id)

        category = self.repo.get(category_id=category_id)
        if not category:
            raise CategoryNotFoundError(category_id=category_id)

        product.category = category
        self.repo.commit()
