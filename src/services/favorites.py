from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.products import Product
from src.models.users import User


class FavoritesService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def product_by_id(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    def add_to_favorites(self, product: Product):
        if product in self.user.favorite_products:
            raise HTTPException(status_code=400, detail="Product already in favorites")

        self.user.favorite_products.append(product)
        self.db.commit()

    def delete_from_favorites(self, product: Product):
        if product not in self.user.favorite_products:
            raise HTTPException(status_code=400, detail="Product not in favorites")

        self.user.favorite_products.remove(product)
        self.db.commit()
