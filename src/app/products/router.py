from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Path, UploadFile

from src.core.dependencies.services import get_product_service
from src.core.dependencies.users import get_current_seller
from src.core.metrics import CACHE_HITS, CACHE_MISSES
from src.core.resources.db import get_redis
from src.core.resources.redis import RedisClient, RedisKeys
from src.models.users import Seller
from src.services.media import delete_image, save_image  # noqa: F401
from src.services.products import ProductService

from .schemas import ProductCartResponse

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("", status_code=201)
def create_product(
    name: str = Form(..., min_length=3, max_length=255),
    description: str | None = Form(None, max_length=500),
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(get_product_service),
):
    product = product_service.create_product(seller=seller, name=name, description=description)

    return {"status": "created", "product_id": product.id}


@router.post("/{product_id}/variants", status_code=201)
def create_variant(
    background_tasks: BackgroundTasks,
    product_id: int = Path(...),
    name: str = Form(..., min_length=3, max_length=32),
    price: float = Form(..., ge=1),
    stock: int = Form(0, ge=0),
    image: UploadFile | None = File(
        None, max_length=15 * 1024 * 1024, media_type=["image/png", "image/jpeg"]
    ),
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(get_product_service),
):
    variant = product_service.create_variant(
        seller=seller, product_id=product_id, name=name, price=price, stock=stock, image=image
    )

    if image is not None:
        background_tasks.add_task(save_image, image, variant.image)

    return {"status": "created", "product_id": product_id, "variant_id": variant.id}


@router.get("/{product_id}", status_code=200, response_model=ProductCartResponse)
def get_product(
    product_id: int = Path(..., ge=1),
    product_service: ProductService = Depends(get_product_service),
    redis: RedisClient = Depends(get_redis),
):
    product = redis.get_json(RedisKeys.product(product_id))
    if product is None:
        product = product_service.get_full_product_by_id(product_id)
        value = ProductCartResponse.model_validate(
            {"product": product, "variants": product.variants}
        ).model_dump()
        redis.set_json(RedisKeys.product(product.id), value, ttl=600)
        CACHE_MISSES.inc()
    else:
        CACHE_HITS.inc()

    return {"product": product, "variants": product.variants}


@router.patch("/{product_id}", status_code=204)
def change_product(
    product_id: int = Path(..., ge=1),
    name: str | None = Form(None, min_length=3, max_length=255),
    description: str | None = Form(None, max_length=500),
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(get_product_service),
):
    product_service.change_product(seller=seller, product_id=product_id, name=name, description=description)


@router.patch("/{product_id}/variants/{variant_id}", status_code=204)
def change_variant(
    background_tasks: BackgroundTasks,
    product_id: int = Path(...),
    variant_id: int = Path(...),
    name: str | None = Form(None, max_length=32),
    price: float | None = Form(None, gt=0),
    stock: int | None = Form(None, ge=0),
    image: UploadFile | None = File(
        None, max_length=15 * 1024 * 1024, media_type=["image/png", "image/jpeg"]
    ),
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(get_product_service),
):
    variant = product_service.change_variant(
        seller=seller,
        product_id=product_id,
        variant_id=variant_id,
        name=name,
        price=price,
        stock=stock,
        image=image,
    )

    if image is not None:
        background_tasks.add_task(save_image, image, variant.image)


@router.patch("/{product_id}/variants/{variant_id}/stock", status_code=204)
def change_stock(
    product_id: int = Path(...),
    variant_id: int = Path(...),
    stock_delta: int = Form(...),
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(get_product_service),
):
    product_service.change_stock(seller=seller, variant_id=variant_id, stock_delta=stock_delta)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int = Path(..., ge=1),
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(get_product_service),
):
    product_service.delete_product(seller=seller, product_id=product_id)


"""
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
    
    if variant.image:
        delete_image(variant.image)
    db.delete(variant)
    db.commit()
"""
