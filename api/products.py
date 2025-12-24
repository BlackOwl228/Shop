from fastapi import APIRouter, HTTPException, Form, Path, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user
from models.products import Product

router = APIRouter(prefix="/products", tags=["Product"])

@router.post('')
def create_product(name: str = Form(..., max_length=255),
                   description: str = Form('', max_length=500),
                   price: int = Form(...),
                   seller: int = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    new_product = Product(name = name, price = price, description = description, seller_id = seller.id)
    db.add(new_product)
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
                   name: str = Form(''),
                   description: str = Form(''),
                   price: int = Form(...),
                   seller: int = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    pass

@router.delete('/{product_id}')
def delete_product(product_id: int = Path(...),
                   seller: int = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="You cannot delete this product")
    db.delete(product)
    db.commit()

    return 204