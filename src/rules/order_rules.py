from enum import StrEnum

from models.orders import Order


class OrderStatus(StrEnum):
    CREATED = "created"
    PAID = "paid"
    COMPLETED = "completed"
    CANCELLED = "cancelled"  # Заказ отменен до оплаты, в будущем возможен возврат средств


def can_complete_order(order: Order):
    return order.status == OrderStatus.PAID


def can_cancel_order(order: Order):
    return order.status == OrderStatus.CREATED
