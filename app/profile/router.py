import os

from fastapi import APIRouter, HTTPException, UploadFile, BackgroundTasks, Depends, Form, File
from sqlalchemy.orm import Session

from core import get_db, get_current_user, verify_password, hash_password, save_avatar
from ..cart.services import product_by_id
from models import User, Product, Seller
from ..auth.schemas import UserName, UserPassword

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
async def change_avatar(background_tasks: BackgroundTasks,
                        avatar: UploadFile = File(..., max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    
    image_bytes = await avatar.read()

    img_path = os.path.join("media", "product", str(user.id))
    ext = avatar.filename.split('.')[-1]
    user.avatar = f"{img_path}.{ext}"  

    background_tasks.add_task(save_avatar, image_bytes, avatar.filename, user.id)

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