import os

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, Path, Depends, File, Form
from sqlalchemy.orm import Session

from core import get_db, save_product_image, delete_image
from core.security import get_current_seller
from models import User, Product, Seller
from domain.seller_rules import can_interact_product
from .schemas import CreatingProductDTO, CreatingProductResponse, PatchingProductDTO, GettingProductResponse

router = APIRouter(prefix="/products", tags=["Product"])

@router.post('', status_code=201, response_model=CreatingProductResponse)
async def create_product(background_tasks: BackgroundTasks,
                         product_data: CreatingProductDTO = Depends(),
                         image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                         seller: Seller = Depends(get_current_seller),
                         db: Session = Depends(get_db)
                         ):
    
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")
    
    if image is not None:
        image_bytes = await image.read()

    product = Product(name=product_data.name,
                      price=product_data.price,
                      description=product_data.description,
                      seller_id=seller.id)
    db.add(product)
    db.flush()

    if image is not None:
        img_path = os.path.join("media", "product", str(product.id))
        ext = image.filename.split('.')[-1]
        product.image = f"{img_path}.{ext}"

    db.commit()

    background_tasks.add_task(save_product_image, image_bytes, image.filename, product.id)

    return {"status": "created", "product_id": product.id}

@router.get('/{product_id}', status_code=200, response_model=GettingProductResponse)
def get_product(product_id: int = Path(..., ge=1),
                db: Session = Depends(get_db)):
    
    product = db.query(Product).filter(Product.id == product_id). first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"product": product}

@router.patch('/{product_id}', status_code=204)
async def change_product(background_tasks: BackgroundTasks,
                         product_id: int = Path(..., ge=1),
                         product_data: PatchingProductDTO = Depends(),
                         image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                         seller: Seller = Depends(get_current_seller),
                         db: Session = Depends(get_db)
                         ):
    
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product_data.name: product.name = product_data.name
    if product_data.description:product.description = product_data.description
    if product_data.price: product.price = product_data.price
    
    if image is not None:
        image_bytes = await image.read()

        img_path = os.path.join("media", "product", str(product.id))
        ext = image.filename.split('.')[-1]
        product.image = f"{img_path}.{ext}"

        background_tasks.add_task(save_product_image, image_bytes, image.filename, product.id)

    db.commit()

@router.patch('/{product_id}/stock', status_code=204)
async def change_stock(product_id: int = Path(..., ge=1),
                       stock_delta: int = Form(...),
                       price: float | None = Form(None, ge=0),
                       seller: Seller = Depends(get_current_seller),
                       db: Session = Depends(get_db)
                       ):
                         
    if not can_interact_product(seller):
        raise HTTPException(status_code=403, detail="You cannot interact with products now")
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.stock = max(0, product.stock + stock_delta)

    if price is not None: product.price = price

    db.commit()

@router.delete('/{product_id}', status_code=204)
async def delete_product(product_id: int = Path(..., ge=1),
                         seller: Seller = Depends(get_current_seller),
                         db: Session = Depends(get_db)
                         ):
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="You cannot delete this product")
    
    #ПРИ НАЛИЧИИ ЮЗЕРОВ ТАКОЕ НЕ РАБОТАЕТ В СИЛУ НЕВОЗМОЖНОСТИ УДАЛЯТЬ ОТКРЫТЫЕ ФАЙЛЫ НА ВИНДЕ
    if product.image:
        delete_image("product", product.image)
        
    db.delete(product)
    db.commit()