import stripe
from decimal import Decimal
from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core import get_db, get_current_user
from models import User, Product, Order, OrderItem
from .schemas import ProductItem, CreatingOrderResponse
from .services import create_payment

router = APIRouter(prefix='/orders', tags=["Order"])

@router.post('', status_code=201, response_model=CreatingOrderResponse)
def create_order(products: List[ProductItem],
                 buyer: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    
    order = Order(buyer_id=buyer.id)
    total_amount = 0
    items_ids = [item.product_id for item in products]
    order_products = db.query(Product).filter(Product.id.in_(items_ids)).all()
    products_map = {p.id: p for p in order_products}

    for item in products:
        product = products_map.get(item.product_id)
        if not product:
            continue
        
        order_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price)

        order.order_items.append(order_item)
        total_amount += product.price * item.quantity

    order.total_price = Decimal(total_amount)
    #order.payment_intent = create_payment(int(total_amount*100))
    order.payment_intent = "sjfew3y42iq820RWEUIDOSXCI"
    db.add(order)
    db.commit()

    return {"order_id": order.id, "total_amount": total_amount}

@router.patch('/{order_id}/cancel', status_code=204)
def cancel_order(order_id: int = Path(..., ge=1),
                 buyer: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="You cannot cancel order now")
    if buyer.id != order.buyer_id:
        raise HTTPException(status_code=403, detail="This is not your order")
    
    order.status = "canceled"

    db.commit()

@router.patch('/{order_id}/complete', status_code=201)
def complete_order(order_id: int = Path(..., ge=1),
                   buyer: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "paid":
        raise HTTPException(status_code=400, detail="You cannot compete order before pay")
    if buyer.id != order.buyer_id:
        raise HTTPException(status_code=403, detail="This is not your order")
    
    order.status = "completed"

    db.commit()

    return {"status": "Order {order.id} completed"}

@router.post("/{order_id}/pay-test", status_code=201)
def pay_order(order_id: int = Path(..., ge=1),
              db: Session = Depends(get_db)):
    
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == "paid":
        return JSONResponse({"detail": "Order already paid"}, status_code=400)

    # подтверждаем тестовой картой pm_card_visa
    intent = stripe.PaymentIntent.confirm(
        order.payment_intent,
        payment_method="pm_card_visa"
    )

    if intent.status == "succeeded":
        order.status = "paid"
    else:
        raise HTTPException(status_code=400, detail=f"Payment failed: {intent.status}")
    
    db.commit()

    return {"order_id": order.id, "status": order.status, "payment_intent": order.payment_intent}