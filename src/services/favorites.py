from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    ProductAlreadyInFavoritesError,
    ProductNotFoundError,
    ProductNotInFavoritesError,
)
from src.models.products import Product
from src.models.users import User


class FavoritesService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def product_by_id(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        return product

    def add_to_favorites(self, product: Product):
        if product in self.user.favorite_products:
            raise ProductAlreadyInFavoritesError()

        self.user.favorite_products.append(product)
        self.db.commit()

    def delete_from_favorites(self, product: Product):
        if product not in self.user.favorite_products:
            raise ProductNotInFavoritesError()

        self.user.favorite_products.remove(product)
        self.db.commit()
