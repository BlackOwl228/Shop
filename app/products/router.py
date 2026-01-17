import os

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, Path, Depends, File
from sqlalchemy.orm import Session

from core import get_db, get_current_user, save_product_image, delete_image
from models import User, Product
from .schemas import CreatingProductDTO, CreatingProductResponse, PatchingProductDTO, GettingProductResponse

router = APIRouter(prefix="/products", tags=["Product"])

@router.post('', status_code=201, response_model=CreatingProductResponse)
async def create_product(background_tasks: BackgroundTasks,
                         product_data: CreatingProductDTO = Depends(),
                         image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                         seller: User = Depends(get_current_user),
                         db: Session = Depends(get_db)
                         ):
    # ИСПРАВИТЬ КОД ДЛЯ ФОТОК
    product = Product(name=product_data.name,
                      price=product_data.price,
                      description=product_data.description,
                      seller_id=seller.id)
    db.add(product)
    db.flush()

    #img_path = os.path.join("media", "product", str(product.id))
    #ext = image.filename.split('.')[-1]
    #product.image = f"{img_path}.{ext}"     
    db.commit()

    #background_tasks.add_task(save_product_image(image, product.id))

    return {"status": "created", "product_id": product.id}

@router.get('/{product_id}', status_code=200, response_model=GettingProductResponse)
def get_product(product_id: int = Path(..., ge=1),
                db: Session = Depends(get_db)):
    
    product = db.query(Product).filter(Product.id == product_id). first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.patch('/{product_id}', status_code=204)
async def change_product(product_id: int = Path(..., ge=1),
                         product_data: PatchingProductDTO = Depends(),
                         image: UploadFile | None = File(None, max_length=15 *1024*1024, media_type=['image/png', 'image/jpeg']),
                         seller: User = Depends(get_current_user),
                         db: Session = Depends(get_db)
                         ):
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product_data.name: product.name = product_data.name
    if product_data.description:product.description = product_data.description
    if product_data.price: product.price = product_data.price
    
    if image:
        await delete_image("product", product.image)
        product.image = await save_product_image(image, product.id)

    db.commit()

@router.delete('/{product_id}', status_code=204)
async def delete_product(product_id: int = Path(..., ge=1),
                         seller: User = Depends(get_current_user),
                         db: Session = Depends(get_db)
                         ):
    
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="You cannot delete this product")
    
    if product.image:
        await delete_image("product", product.image)
        
    db.delete(product)
    db.commit()