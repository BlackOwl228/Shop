from decimal import Decimal
from fastapi import HTTPException
from models import Product, Order, OrderItem, ProductVariant
from .schemas import ProductItemIn, OrderLine

def validate_and_build_lines(
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

def apply_products(order: Order, lines: list[OrderLine]):
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