import stripe

def create_payment(amount: int):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="rub",
        payment_method_types=["card"],  # для тестов
    )
    return intent.id, intent.client_secret

from typing import List, Dict
from decimal import Decimal

from fastapi import HTTPException

from models import Product, Order, OrderItem
from .schemas import ProductItem

def validate_order(products: List[ProductItem],
                   variants_map: Dict[int, Product]):
    for item in products:
        variant = variants_map.get(item.variant_id)

        if not variant:
            raise HTTPException(status_code=400, detail="Variant unavailable")

        if variant.price != item.client_price:
            raise HTTPException(status_code=400, detail="Price was changed")

        if variant.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Variant {variant.id} out of stock")

def add_products(products: List[ProductItem],
                 variants_map: Dict[int, Product],
                 order: Order):
    total = Decimal(0)
    for item in products:
        variant = variants_map[item.variant_id]
        
        order_item = OrderItem(
            variant_id=variant.id,
            quantity=item.quantity,
            unit_price=variant.price,
        )
        order.order_items.append(order_item)
        total += variant.price * item.quantity

        variant.stock -= item.quantity

    order.total_price = total

    return order