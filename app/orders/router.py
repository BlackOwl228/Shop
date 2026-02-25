import stripe
from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core import get_db, get_current_user
from models import User, Seller, Product, ProductVariant, Order
from .schemas import ProductItemIn, CreatingOrderResponse
from .services import create_payment, validate_and_build_lines, apply_products
from rules.product_rules import available_products
from rules.order_rules import can_cancel_order, can_complete_order

router = APIRouter(prefix='/orders', tags=["Order"])

@router.post('', status_code=201, response_model=CreatingOrderResponse)
def create_order(products: List[ProductItemIn],
                 buyer: User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    variant_ids = [item.variant_id for item in products]

    variants = (available_products(db.query(ProductVariant))
                .filter(ProductVariant.id.in_(variant_ids))
                .all()
                )
    variants_map = {v.id: v for v in variants}
    order_lines = validate_and_build_lines(products, variants_map)

    order = apply_products(Order(buyer_id=buyer.id), order_lines)

    #order.payment_intent = create_payment(int(total_amount*100))
    #ВРЕМЕННАЯ ЗАМЕНА СТРАЙП
    order.payment_intent = "sjfew3y42iq820RWEUIDOSXCI"
    db.add(order)
    db.commit()

    return {"order_id": order.id, "total_amount": order.total_price, "payment_secret": order.payment_intent} #заглушка пока не верну страйп

@router.patch('/{order_id}/cancel', status_code=204)
def cancel_order(order_id: int = Path(..., ge=1),
                 buyer: User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    order = db.query(Order).filter(Order.id == order_id, Order.buyer_id == buyer.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not yours")
    if not can_cancel_order(order):
        raise HTTPException(status_code=400, detail="You cannot cancel order now")
    
    order.status = "canceled"

    db.commit()

@router.patch('/{order_id}/complete', status_code=201)
def complete_order(order_id: int = Path(..., ge=1),
                   buyer: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    order = db.query(Order).filter(Order.id == order_id, Order.buyer_id == buyer.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not yours")
    if not can_complete_order(order):
        raise HTTPException(status_code=400, detail="You cannot compete order before pay")
    
    order.status = "completed"

    db.commit()

    return {"status": "Order {order.id} completed"}

@router.post("/{order_id}/pay-test", status_code=201)
def pay_order(order_id: int = Path(..., ge=1),
              db: Session = Depends(get_db)
              ):
    order = db.query(Order).filter(Order.id == order_id).first()
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