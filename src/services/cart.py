from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.collections import CartItem
from models.products import ProductVariant
from models.users import User
from rules.product_rules import available_products


class CartService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def get_cart_item(self, user_id: int, variant_id: int):
        item = (
            self.db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.variant_id == variant_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=404, detail="Item not in cart")

        return item

    def add_to_cart(self, variant_id: int, quantity: int):
        variant = self.db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
        if not variant:
            raise HTTPException(status_code=404, detail="Product not found")

        try:
            item = CartItem(user_id=self.user.id, variant_id=variant_id, quantity=quantity)
            self.db.add(item)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Product already in cart") from e

    def get_user_cart(self):
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
