import os

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, Path, Depends, File, Form
from sqlalchemy.orm import Session, joinedload

from core import get_db, save_image, delete_image
from core.security import get_current_seller
from models import Product, ProductVariant, Seller
from domain.seller_rules import can_interact_product
from .schemas import ProductCartResponse

router = APIRouter(prefix="/products", tags=["Product"])

@router.post('', status_code=201)
def create_product(name: str = Form(..., min_length=3, max_length=255),
                   description: str | None = Form(None, max_length=500),
                   seller: Seller = Depends(get_current_seller),
                   db: Session = Depends(get_db)
                   ):
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")

    product = Product(name=name,
                      description=description,
                      seller_id=seller.id)
    db.add(product)
    db.commit()

    return {"status": "created", "product_id": product.id}

@router.post('/{product_id}/variants', status_code=201)
def create_variant(background_tasks: BackgroundTasks,
                   product_id: int = Path(...),
                   name: str = Form(..., min_length=3, max_length=255),
                   price: float = Form(..., ge=1),
                   stock: int = Form(0, ge=0),
                   image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                   seller: Seller = Depends(get_current_seller),
                   db: Session = Depends(get_db)
                   ):
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")

    variant = ProductVariant(name=name, price=price, product_id=product_id, stock=stock)
    db.add(variant)
    db.flush()

    if image is not None:
        img_path = os.path.join("media", "product", str(product_id), str(variant.id))
        ext = image.filename.split('.')[-1]
        path = f"{img_path}.{ext}"
        variant.image = path

    db.commit()

    if image is not None:
        background_tasks.add_task(save_image, image, path)

    return {"status": "created", "product_id": product_id, "variant_id": variant.id}

@router.get('/{product_id}', status_code=200, response_model=ProductCartResponse)
def get_product(product_id: int = Path(..., ge=1),
                db: Session = Depends(get_db)):
    
    product = (db.query(Product)
               .options(joinedload(Product.variants))
               .filter(Product.id == product_id)
               .first())
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"product": product, "variants": product.variants}

@router.patch('/{product_id}', status_code=204)
def change_product(product_id: int = Path(..., ge=1),
                   name: str | None = Form(None, min_length=3, max_length=255),
                   description: str | None = Form(None, max_length=500),
                   seller: Seller = Depends(get_current_seller),
                   db: Session = Depends(get_db)
                   ):
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if name: product.name = name
    if description:product.description = description
    db.commit()

@router.patch('/{product_id}/variants/{variant_id}', status_code=204)
def change_variant(background_tasks: BackgroundTasks,
                   product_id: int = Path(...),
                   variant_id: int = Path(...),
                   name: str | None = Form(None, max_length=32),
                   price: float | None = Form(None, gt=0),
                   stock: int | None = Form(None, ge=0),
                   image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                   seller: Seller = Depends(get_current_seller),
                   db: Session = Depends(get_db)
                   ):
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")
    
    variant = (db.query(ProductVariant)
               .join(Product)
               .filter(ProductVariant.id == variant_id,
                       ProductVariant.product_id == product_id,
                       Product.seller_id == seller.id)
               .first())
    if not variant:
        raise HTTPException(status_code=404, detail="Variant of product not found")
    
    if name: variant.name = name
    if price: variant.price = price
    if stock: variant.stock = stock

    if image is not None:
        img_path = os.path.join("media", "product", str(product_id), str(variant_id))
        ext = image.filename.split('.')[-1]
        path = f"{img_path}.{ext}"
        variant.image = path

        background_tasks.add_task(save_image, image, path)

    db.commit()

@router.patch('/{product_id}/variants/{variant_id}/stock', status_code=204)
def change_stock(product_id: int = Path(...),
                 variant_id: int = Path(...),
                 stock_delta: int = Form(...),
                 seller: Seller = Depends(get_current_seller),
                 db: Session = Depends(get_db)
                 ):           
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")
    
    variant = (db.query(ProductVariant)
               .join(Product)
               .filter(ProductVariant.id == variant_id,
                       ProductVariant.product_id == product_id,
                       Product.seller_id == seller.id)
               .first())
    if not variant:
        raise HTTPException(status_code=404, detail="Variant of product not found")
    
    variant.stock = max(0, variant.stock + stock_delta)
    db.commit()

@router.delete('/{product_id}', status_code=204)
def delete_product(product_id: int = Path(..., ge=1),
                   seller: Seller = Depends(get_current_seller),
                   db: Session = Depends(get_db)
                   ):
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="You cannot delete this product")
    
    db.delete(product)
    db.commit()

@router.delete('/{product_id}/variants/{variant_id}', status_code=204)
def delete_variant(product_id: int = Path(...),
                   variant_id: int = Path(...),
                   seller: Seller = Depends(get_current_seller),
                   db: Session = Depends(get_db)
                   ): 
    variant = (db.query(ProductVariant)
               .join(Product)
               .filter(ProductVariant.id == variant_id,
                       ProductVariant.product_id == product_id,
                       Product.seller_id == seller.id)
               .first())
    if not variant:
        raise HTTPException(status_code=404, detail="Variant of product not found")
    #ПРИ НАЛИЧИИ ЮЗЕРОВ ТАКОЕ НЕ РАБОТАЕТ В СИЛУ НЕВОЗМОЖНОСТИ УДАЛЯТЬ ОТКРЫТЫЕ ФАЙЛЫ НА ВИНДЕ
    if variant.image:
        delete_image(variant.image)
    db.delete(variant)
    db.commit()