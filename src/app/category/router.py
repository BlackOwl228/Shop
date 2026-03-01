from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from core.db import get_db
from app.auth.security import get_current_seller
from models.users import User
from models.products import Product
from models.collections import Category

from .schemas import CategoriesPesponse

router = APIRouter(tags=["Category"])

#Пагинация при необходимости
@router.get('/categories', response_model=CategoriesPesponse)
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"categories": categories}

@router.post('/products/{product_id}/categories/{category_id}')
def add_product_to_category(product_id: int = Path(...),
                            category_id: int = Path(...),
                            seller: User = Depends(get_current_seller),
                            db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.seller_id!=seller.id:
        raise HTTPException(status_code=403, detail="This is not your product")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    product.category=category
    db.commit()