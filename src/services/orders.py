from decimal import Decimal

from sqlalchemy.orm import Session

from src.app.orders.schemas import OrderLine, ProductItemIn
from src.core.logs.exceptions import (
    InvalidOrderStateError,
    NotYourOrderError,
    OrderAlreadyPaidError,
    OrderNotFoundError,
    VariantOutOfStockError,
    VariantPriceChangedError,
    VariantUnavailableError,
)
from src.integrations.stripe import confirm_payment, create_payment  # noqa: F401
from src.models.orders import Order, OrderItem
from src.models.products import ProductVariant
from src.repos.orders import OrderRepo
from src.repos.products import ProductRepo
from src.rules.order_rules import can_cancel_order, can_complete_order


class OrderService:
    def __init__(self, db: Session):
        self.repo = OrderRepo(db)

    def test_confirm_payment(self, order_id: int):
        order = self.repo.get(order_id=order_id)
        if not order:
            raise OrderNotFoundError(order_id=order_id)
        if order.status == "paid":
            return OrderAlreadyPaidError(order_id=order_id)

        confirm_payment(order)
        self.repo.commit()
        return order

    def create_order(self, buyer_id: int, products: list[ProductItemIn]) -> Order:
        variant_ids = [item.variant_id for item in products]

        variants = ProductRepo(self.repo.db).get_available_variants_by_ids(variant_ids=variant_ids)
        variants_map = {v.id: v for v in variants}
        order_lines = self._validate_and_build_lines(items=products, variants_map=variants_map)

        order = self._apply_products(Order(buyer_id=buyer_id), order_lines)

        # order.payment_intent = create_payment(int(total_amount*100))
        # ВРЕМЕННАЯ ЗАМЕНА СТРАЙП
        order.payment_intent = "sjfew3y42iq820RWEUIDOSXCI"
        self.repo.create(order)
        self.repo.commit()
        return order

    def get(self, order_id: int):
        order = self.repo.get(order_id=order_id)
        if not order:
            raise OrderNotFoundError(order_id=order_id)
        return order

    def cancel_order(self, order: Order, buyer_id: int):
        if order.buyer_id != buyer_id:
            raise NotYourOrderError(order_id=order.id, user_id=buyer_id)
        if not can_cancel_order(order):
            raise InvalidOrderStateError(order_id=order.id, order_status=order.status)

        order.status = "canceled"
        self.repo.commit()

    def complete_order(self, order: Order, buyer_id: int):
        if order.buyer_id != buyer_id:
            raise NotYourOrderError(order_id=order.id, user_id=buyer_id)
        if not can_complete_order(order):
            raise InvalidOrderStateError(order_id=order.id, order_status=order.status)

        order.status = "completed"
        self.repo.commit()

    def _validate_and_build_lines(
        self, items: list[ProductItemIn], variants_map: dict[int, ProductVariant]
    ) -> list[OrderLine]:
        lines = []

        for item in items:
            variant = variants_map.get(item.variant_id)
            if not variant:
                raise VariantUnavailableError(variant_id=item.variant_id)

            if variant.price != item.client_price:
                raise VariantPriceChangedError(variant_id=variant.id, actual_price=variant.price)

            if variant.stock < item.quantity:
                raise VariantOutOfStockError(variant_id=variant.id, available_stock=variant.stock)

            lines.append(
                OrderLine(
                    variant=variant,
                    quantity=item.quantity,
                    unit_price=variant.price,
                )
            )

        return lines

    def _apply_products(self, order: Order, lines: list[OrderLine]):
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
