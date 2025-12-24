from fastapi import APIRouter, HTTPException, Depends, Form, Path
from sqlalchemy.orm import Session
from models.users import User
from models.products import Product
from core.security import get_current_user, verify_password, hash_password
from core.db import get_db
from services.products import product_by_id

router = APIRouter(prefix='/me', tags=["Profile"])

@router.get('')
def get_profile(user: User = Depends(get_current_user)):
    return user.name, user.email

@router.patch('/name')
def change_name(new_name: str = Form(...),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    user.name = new_name
    db.commit()

    return 204

@router.patch('/password')
def change_password(password: str = Form(...),
                    new_password: str = Form(...),
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if not verify_password(password, user.hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    user.hash = hash_password(new_password)
    db.commit()

    return 204

@router.get('/orders')
def get_my_orders(user: User = Depends(get_current_user)):
    return user.orders

@router.post('/cart/{product_id}')
def add_product_to_cart(product: Product = Depends(product_by_id),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if product in user.cart:
        raise HTTPException(status_code=400, detail="Product already in cart")
    
    user.cart.append(product)
    db.commit()

    return 204

@router.get('/cart')
def get_my_cart(user: User = Depends(get_current_user)):
    return user.cart

@router.delete('/cart/{product_id}')
def remove_product_from_cart(product: Product = Depends(product_by_id),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    if product not in user.cart:
        raise HTTPException(status_code=404, detail="Product not in cart")
    
    user.cart.remove(product)
    db.commit()

    return 204


@router.post('/favorites/{product_id}')
def add_product_to_favorites(product: Product = Depends(product_by_id),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    if product in user.cart:
        raise HTTPException(status_code=400, detail="Product already in cart")

    user.favorites.append(product)
    db.commit()

    return 204

@router.get('/favorites')
def get_my_favorites(user: User = Depends(get_current_user)):
    return user.favorites

@router.delete('/favorites/{product_id}')
def remove_product_from_favorites(product: Product = Depends(product_by_id),
                                  user: User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    if product not in user.cart:
        raise HTTPException(status_code=404, detail="Product not in cart")
    
    user.favorites.remove(product)
    db.commit()

    return 204