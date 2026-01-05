from fastapi import APIRouter, HTTPException, UploadFile, Depends, Form, File
from sqlalchemy.orm import Session

from core import get_db, get_current_user, verify_password, hash_password, save_avatar, delete_image
from services.products import product_by_id
from models import User, Product
from schemas.auth import UserName, UserPassword

router = APIRouter(prefix='/me', tags=["Profile"])

@router.get('', status_code=200)
def get_profile(user: User = Depends(get_current_user)):
    return user.name, user.email, user.email_verified, user.avatar, user.created_at

@router.patch('/name', status_code=200)
def change_name(new_name: str = UserName,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    
    user.name = new_name

    db.commit()
    db.refresh(user)

    return {"status": "Name was changed", "new_name": user.name}

@router.patch('/avatar', status_code=202)
async def change_avatar(new_avatar: UploadFile = File(),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    
    if user.avatar: await delete_image("avatar", user.avatar)
    user.avatar = await save_avatar(new_avatar, user.id)

    db.commit()

@router.patch('/password', status_code=200)
def change_password(password: str = UserPassword,
                    new_password: str = UserPassword,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    
    if not verify_password(password, user.hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    user.hash = hash_password(new_password)

    db.commit()

    return {"status": "Password was changed"}

@router.get('/orders', status_code=200)
def get_my_orders(user: User = Depends(get_current_user)):
    return user.orders

@router.post('/cart/{product_id}', status_code=204)
def add_product_to_cart(product: Product = Depends(product_by_id),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    
    if product in user.cart_products:
        raise HTTPException(status_code=400, detail="Product already in cart")
    
    user.cart_products.append(product)

    db.commit()

@router.get('/cart', status_code=200)
def get_my_cart(user: User = Depends(get_current_user)):
    return user.cart_products

@router.delete('/cart/{product_id}', status_code=204)
def remove_product_from_cart(product: Product = Depends(product_by_id),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    
    if product not in user.cart_products:
        raise HTTPException(status_code=404, detail="Product not in cart")
    
    user.cart_products.remove(product)

    db.commit()

@router.post('/favorites/{product_id}', status_code=204)
def add_product_to_favorites(product: Product = Depends(product_by_id),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    
    if product in user.favorite_products:
        raise HTTPException(status_code=400, detail="Product already in favorites")

    user.favorite_products.append(product)

    db.commit()

@router.get('/favorites', status_code=200)
def get_my_favorites(user: User = Depends(get_current_user)):
    return user.favorite_products

@router.delete('/favorites/{product_id}', status_code=204)
def remove_product_from_favorites(product: Product = Depends(product_by_id),
                                  user: User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    
    if product not in user.favorite_products:
        raise HTTPException(status_code=404, detail="Product not in favorites")
    
    user.favorite_products.remove(product)
    
    db.commit()