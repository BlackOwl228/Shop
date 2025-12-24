from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Path
from core.db import get_db
from models.products import Product

def product_by_id(product_id: int = Path(...), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
