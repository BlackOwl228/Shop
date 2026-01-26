from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, Path, Form
from sqlalchemy.orm import Session

from core.security import get_db, get_current_user
from domain.product_rules import available_products
from models import User, ProductVariant, CartItem
from .schemas import CartResponse

router = APIRouter(tags=["Cart"])

@router.post('/cart/{variant_id}', status_code=204)
def add_product_to_cart(variant_id: int = Path(...),
                        quantity: int = Form(1, ge=1),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if variant in user.cart_items:
        raise HTTPException(status_code=400, detail="Product already in cart")
    
    item = CartItem(user_id=user.id, variant_id=variant_id, quantity=quantity)
    db.add(item)
    db.commit()

@router.get('/cart', status_code=200, response_model=CartResponse)
def get_my_cart(user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    items = (
        available_products(db.query(CartItem).join(ProductVariant))
        .filter(CartItem.user_id == user.id)
        .all()
    )

    total = Decimal(0)
    result = []

    for item in items:
        subtotal = item.variant.price * item.quantity
        total += subtotal

        result.append({
            "variant": item.variant,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "items": result,
        "total_price": total
    }


@router.patch('/cart/{variant_id}', status_code=204)
def change_quantity(variant_id: int = Path(...),
                    quantity: int = Form(..., gt=0),
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.user_id == user.id,
                                     CartItem.variant_id == variant_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    
    item.quantity = quantity
    db.commit()

@router.delete('/cart/{variant_id}', status_code=204)
def remove_product_from_cart(variant_id: int = Path(...),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.user_id == user.id,
                                     CartItem.variant_id == variant_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    
    db.delete(item)
    db.commit()