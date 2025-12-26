from fastapi import APIRouter, HTTPException, UploadFile, Form, Path, Depends, File
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user
from core.media import save_product_image, delete_image
from models.products import Product
from models.users import User

router = APIRouter(prefix="/products", tags=["Product"])

@router.post('')
def create_product(name: str = Form(..., max_length=255),
                   description: str = Form('', max_length=500),
                   price: int = Form(...),
                   image: UploadFile = File(...),
                   seller: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    new_product = Product(name=name, price=price, description=description, seller_id=seller.id)
    db.add(new_product)
    db.flush()
    img = save_product_image(image, new_product.id)
    new_product.image = img
    db.commit()

    return 204

@router.get('/{product_id}')
def get_product(product_id: int = Path(...),
                db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id). first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch('/{product_id}')
def change_product(product_id: int = Path(...),
                   name: str = Form(),
                   description: str = Form(),
                   price: int = Form(),
                   image: UploadFile = File(),
                   seller: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id). first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if name: product.name = name
    if description:product.description = description
    if price: product.price = price
    if image:
        delete_image("product", product.image)
        product.image = save_product_image(image, product.id)

    db.commit()

    return 204

@router.delete('/{product_id}')
def delete_product(product_id: int = Path(...),
                   seller: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="You cannot delete this product")
    try:
        delete_image("product", product.image)
    finally:
        db.delete(product)
        db.commit()

    return 204