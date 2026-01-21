from typing import List

from fastapi import APIRouter, HTTPException, Depends, Path, Form
from sqlalchemy.orm import Session
from sqlalchemy import update

from core.security import get_db, get_current_user
from models import User, Product, cart
from .services import product_by_id
from ..search.schemas import SearchingProduct

router = APIRouter(prefix='/cart', tags=["Cart"])

@router.post('/cart/{product_id}', status_code=204)
def add_product_to_cart(product: Product = Depends(product_by_id),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    
    if product in user.cart_products:
        raise HTTPException(status_code=400, detail="Product already in cart")
    
    user.cart_products.append(product)

    db.commit()

@router.get('/cart', status_code=200, response_model=List[SearchingProduct])
def get_my_cart(user: User = Depends(get_current_user)):
    return user.cart_products

@router.patch('/cart/{product_id}', status_code=204)
def change_quantity(product_id: int = Path(..., ge=0),
                    quantity: int = Form(..., gt=0),
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    stmt = (
        update(cart)
        .where(
            cart.c.user == user.id,
            cart.c.product == product_id
        )
        .values(quantity=quantity)
    )

    result = db.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not in cart")
    db.commit()

@router.delete('/cart/{product_id}', status_code=204)
def remove_product_from_cart(product: Product = Depends(product_by_id),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    
    if product not in user.cart_products:
        raise HTTPException(status_code=404, detail="Product not in cart")
    
    user.cart_products.remove(product)

    db.commit()