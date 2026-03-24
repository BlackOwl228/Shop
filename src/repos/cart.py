from sqlalchemy.orm import Session

from src.models.cart import CartItem
from src.models.products import ProductVariant
from src.rules.product_rules import available_products


class CartRepo:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def create(self, item: CartItem):
        self.db.add(item)

    def get(self, user_id: int, variant_id: int):
        return (
            self.db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.variant_id == variant_id)
            .first()
        )

    def get_all(self, user_id: int):
        return (
            available_products(self.db.query(CartItem).join(ProductVariant))
            .filter(CartItem.user_id == user_id)
            .all()
        )

    def delete(self, item: CartItem):
        self.db.delete(item)
