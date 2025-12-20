from fastapi import APIRouter, HTTPException, Form, Query, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user
from models.orders import Order, OrderItem
from models.products import Product

router = APIRouter(prefix='/orders', tags=["Order"])

@router.post('/')
def create_order(products: list = Query(...),
                 buyer: int = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    new_order = Order(user_id=buyer.id)
    total_amount = 0
    for item_id, quantity in products:
        product = db.query(Product).filter(Product.id == item_id).first()
        if not product:
            raise HTTPException(status_code=404)
        order_item = OrderItem(
        product_id=product.id,
        quantity=quantity,
        unit_price=product.price)

        new_order.order_items.append(order_item)
        total_amount += product.price * quantity
    new_order.total_price = total_amount
    db.add(new_order)
    db.commit()