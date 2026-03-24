from decimal import Decimal

from sqlalchemy.orm import Session

from src.core.logs.exceptions import VariantAlreadyInCartError, VariantNotFoundError, VariantNotInCartError
from src.models.cart import CartItem
from src.repos.cart import CartRepo
from src.repos.products import ProductRepo


class CartService:
    def __init__(self, db: Session):
        self.repo = CartRepo(db)

    def get_cart_item(self, user_id: int, variant_id: int):
        item = self.repo.get(user_id=user_id, variant_id=variant_id)
        if not item:
            raise VariantNotInCartError()

        return item

    def add_to_cart(self, user_id: int, variant_id: int, quantity: int):
        variant = ProductRepo(self.repo.db).get_variant(variant_id=variant_id)
        if not variant:
            raise VariantNotFoundError(variant_id=variant_id)

        try:
            item = CartItem(user_id=user_id, variant_id=variant_id, quantity=quantity)
            self.repo.create(item)
            self.repo.commit()
        except Exception as e:
            raise VariantAlreadyInCartError() from e

    def get_user_cart(self, user_id: int) -> tuple:
        items = self.repo.get_all(user_id=user_id)

        result = []
        total = Decimal(0)

        for item in items:
            subtotal = item.variant.price * item.quantity
            total += subtotal

            result.append({"variant": item.variant, "quantity": item.quantity, "subtotal": subtotal})

        return result, total

    def change_quantity(self, item: CartItem, quantity: int):
        item.quantity = quantity
        self.repo.commit()

    def delete_from_cart(self, item: CartItem):
        self.repo.delete(item)
        self.repo.commit()
