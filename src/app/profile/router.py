import os
from fastapi import APIRouter, HTTPException, UploadFile, BackgroundTasks, Depends, Form, File, Path
from sqlalchemy.orm import Session

from core.db import get_db
from app.auth.security import get_current_user, verify_password, hash_password
from core.media import save_image
from models.users import User, Seller
from models.products import Product

from ..auth.schemas import UserName, UserPassword

router = APIRouter(prefix='/me', tags=["Profile"])

@router.get('', status_code=200)
def get_profile(user: User = Depends(get_current_user)):
    return user.name, user.email, user.email_verified, user.avatar, user.created_at, user.is_admin

@router.patch('/name', status_code=200)
def change_name(new_name: UserName = Form(...),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    
    user.name = new_name

    db.commit()
    db.refresh(user)

    return {"status": "Name was changed", "new_name": user.name}

@router.patch('/avatar', status_code=202)
async def change_avatar(background_tasks: BackgroundTasks,
                        image: UploadFile = File(..., max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):

    img_path = os.path.join("media", "avatar", str(user.id))
    ext = image.filename.split('.')[-1]
    path = f"{img_path}.{ext}"
    user.avatar = path 

    background_tasks.add_task(save_image, image, path)

    db.commit()

@router.patch('/password', status_code=200)
def change_password(password: UserPassword = Form(...),
                    new_password: UserPassword = Form(...),
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if password == new_password:
        return {"status": "Passwords match"}

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    user.hashed_password = hash_password(new_password)

    db.commit()

    return {"status": "Password was changed"}

@router.get('/orders', status_code=200)
def get_my_orders(user: User = Depends(get_current_user)):
    return user.orders


@router.post('/seller-request', status_code=201)
def create_seller_request(company_name: str = Form(..., max_length=128),
                          user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    
    old_request = db.query(Seller).filter(Seller.user_id == user.id).first()
    if old_request:
        raise HTTPException(status_code=400, detail="request is already exists")

    request = Seller(user_id=user.id,
                     company_name=company_name)
    db.add(request)
    db.commit()

    return {"status": "Request was created, wait for approve"}


@router.post('/favorites/{product_id}', status_code=204)
def add_product_to_favorites(product_id: int = Path(...),
                             user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product in user.favorite_products:
        raise HTTPException(status_code=400, detail="Product already in favorites")

    user.favorite_products.append(product)

    db.commit()

@router.get('/favorites', status_code=200)
def get_my_favorites(user: User = Depends(get_current_user)):
    return user.favorite_products

@router.delete('/favorites/{product_id}', status_code=204)
def remove_product_from_favorites(product_id: int = Path(...),
                                  user: User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product not in user.favorite_products:
        raise HTTPException(status_code=404, detail="Product not in favorites")
    
    user.favorite_products.remove(product)
    
    db.commit()