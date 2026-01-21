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
                   products_map: Dict[int, Product]):
    
    for item in products:
        product = products_map.get(item.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Product unavailable now")
        
        if product.price != item.client_price:
            raise HTTPException(status_code=400, detail="Price was changed")
        
        if product.stock >= item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {product.id} out of stock")

def add_products(products: List[ProductItem],
                 products_map: Dict[int, Product],
                 order: Order):

    total_amount = 0
    for item in products:
        product = products_map.get(item.product_id)
        
        order_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price)

        order.order_items.append(order_item)
        total_amount += Decimal(product.price) * item.quantity

    order.total_price = Decimal(total_amount)

    return order