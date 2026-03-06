from fastapi import APIRouter, Depends, Path

from core.depends import get_admin_service
from services.admin import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.delete("/products/{product_id}/block")
def block_product(product_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)):
    product = admin_service.product_by_id(product_id)

    admin_service.block_product(product)


@router.patch("/products/{product_id}/unblock")
def unblock_product(product_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)):
    product = admin_service.product_by_id(product_id)

    admin_service.unblock_product(product)


@router.post("/sellers/{seller_id}")
def approve_seller_request(
    seller_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)
):
    seller = admin_service.seller_by_id(seller_id)

    admin_service.approve_seller(seller)

    return {"status": f"Seller {seller_id} was approved"}


@router.delete("/sellers/{seller_id}")
def suspend_seller(seller_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)):
    seller = admin_service.seller_by_id(seller_id)

    admin_service.suspend_seller(seller)

    return {"status": f"Seller {seller_id} was suspended"}


@router.patch("/orders/{order_id}/complete")
def complete_order(order_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)):
    order = admin_service.order_by_id(order_id)

    admin_service.complete_order(order)


@router.patch("/orders/{order_id}/cancel")
def cancel_order(order_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)):
    order = admin_service.order_by_id(order_id)

    admin_service.cancel_order(order)


@router.delete("/reviews/{review_id}")
def delete_review(review_id: int = Path(...), admin_service: AdminService = Depends(get_admin_service)):
    review = admin_service.review_by_id(review_id)

    admin_service.delete_review(review)


@router.post("/categories")
def create_category(name: str, admin_service: AdminService = Depends(get_admin_service)):
    admin_service.create_category(name)

    return {"status": "created"}


@router.post("/products/{product_id}/categories/{category_id}")
def add_product_to_category(
    product_id: int = Path(...),
    category_id: int = Path(...),
    admin_service: AdminService = Depends(get_admin_service),
):
    product = admin_service.product_by_id(product_id)

    admin_service.product_to_category(product=product, category_id=category_id)
