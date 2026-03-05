from typing import List
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import User
from models.products import ProductVariant
from models.orders import Order, OrderItem
from rules.product_rules import available_products
from rules.order_rules import can_cancel_order, can_complete_order
from integrations.stripe import create_payment, confirm_payment
from app.orders.schemas import ProductItemIn, OrderLine

class OrderService():
    def __init__(self, db: Session, buyer: User):
        self.db = db
        self.buyer = buyer

    def test_confirm_payment(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status == "paid":
            return HTTPException(status_code=400, detail="Order already paid")

        confirm_payment(order)
        self.db.commit()
        return order

    def create_order(self, products: List[ProductItemIn]) -> Order:
        variant_ids = [item.variant_id for item in products]

        variants = (available_products(self.db.query(ProductVariant))
                    .filter(ProductVariant.id.in_(variant_ids))
                    .all()
                    )
        variants_map = {v.id: v for v in variants}
        order_lines = self._validate_and_build_lines(products, variants_map)

        order = self._apply_products(Order(buyer_id=self.buyer.id), order_lines)

        #order.payment_intent = create_payment(int(total_amount*100))
        #ВРЕМЕННАЯ ЗАМЕНА СТРАЙП
        order.payment_intent = "sjfew3y42iq820RWEUIDOSXCI"
        self.db.add(order)
        self.db.commit()
        return order

    def cancel_order_by_id(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id, Order.buyer_id == self.buyer.id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or not yours")
        if not can_cancel_order(order):
            raise HTTPException(status_code=400, detail="You cannot cancel order now")
        
        order.status = "canceled"
        self.db.commit()

    def complete_order_by_id(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id, Order.buyer_id == self.buyer.id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or not yours")
        if not can_complete_order(order):
            raise HTTPException(status_code=400, detail="You cannot compete order before pay")
        
        order.status = "completed"
        self.db.commit()

    def _validate_and_build_lines(
        items: list[ProductItemIn],
        variants_map: dict[int, ProductVariant],
    ) -> list[OrderLine]:
        lines = []

        for item in items:
            variant = variants_map.get(item.variant_id)
            if not variant:
                raise HTTPException(400, "Variant unavailable")

            if variant.price != item.client_price:
                raise HTTPException(409, "Price changed")

            if variant.stock < item.quantity:
                raise HTTPException(409, "Out of stock")

            lines.append(
                OrderLine(
                    variant=variant,
                    quantity=item.quantity,
                    unit_price=variant.price,
                )
            )

        return lines

    def _apply_products(order: Order, lines: list[OrderLine]):
        total = Decimal(0)
        for line in lines:
            order_item = OrderItem(
                variant_id=line.variant.id,
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
            order.order_items.append(order_item)

            total += line.unit_price * line.quantity
            line.variant.stock -= line.quantity

        order.total_price = total

        return order