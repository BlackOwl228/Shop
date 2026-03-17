from decimal import Decimal

from sqlalchemy.orm import Session

from src.core.logs.exceptions import VariantAlreadyInCartError, VariantNotFoundError, VariantNotInCartError
from src.models.collections import CartItem
from src.models.products import ProductVariant
from src.models.users import User
from src.rules.product_rules import available_products


class CartService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def get_cart_item(self, variant_id: int):
        item = (
            self.db.query(CartItem)
            .filter(CartItem.user_id == self.user.id, CartItem.variant_id == variant_id)
            .first()
        )
        if not item:
            raise VariantNotInCartError()

        return item

    def add_to_cart(self, variant_id: int, quantity: int):
        variant = self.db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
        if not variant:
            raise VariantNotFoundError(variant_id=variant_id)

        try:
            item = CartItem(user_id=self.user.id, variant_id=variant_id, quantity=quantity)
            self.db.add(item)
            self.db.commit()
        except Exception as e:
            raise VariantAlreadyInCartError() from e

    def get_user_cart(self) -> tuple:
        items = (
            available_products(self.db.query(CartItem).join(ProductVariant))
            .filter(CartItem.user_id == self.user.id)
            .all()
        )

        result = []
        total = Decimal(0)

        for item in items:
            subtotal = item.variant.price * item.quantity
            total += subtotal

            result.append({"variant": item.variant, "quantity": item.quantity, "subtotal": subtotal})

        return result, total

    def change_quantity(self, item: CartItem, quantity: int):
        item.quantity = quantity
        self.db.commit()

    def delete_from_cart(self, item: CartItem):
        self.db.delete(item)
        self.db.commit()
