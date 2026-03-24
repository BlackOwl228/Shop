from fastapi import APIRouter, Depends, Form, Path

from src.core.dependencies.services import (
    get_admin_service,
    get_category_service,
    get_order_service,
    get_product_service,
    get_review_service,
    get_user_service,
)
from src.services.admin import AdminService
from src.services.category import CategoryService
from src.services.orders import OrderService
from src.services.products import ProductService
from src.services.review import ReviewService
from src.services.users import UserService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/products/{product_id}/block", status_code=200)
def block_product(
    product_id: int = Path(...),
    product_service: ProductService = Depends(get_product_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    product = product_service.get_product(product_id=product_id)

    admin_service.block_product(product=product)

    return {"status": f"Product {product_id} was blocked"}


@router.post("/products/{product_id}/unblock", status_code=200)
def unblock_product(
    product_id: int = Path(...),
    product_service: ProductService = Depends(get_product_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    product = product_service.get_product(product_id=product_id)

    admin_service.unblock_product(product)

    return {"status": f"Product {product_id} was unblocked"}


@router.post("/sellers/{seller_id}", status_code=201)
def approve_seller_request(
    seller_id: int = Path(...),
    user_service: UserService = Depends(get_user_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    seller = user_service.get_seller(seller_id=seller_id)

    admin_service.approve_seller(seller)

    return {"status": f"Seller {seller_id} was approved"}


@router.delete("/sellers/{seller_id}", status_code=200)
def suspend_seller(
    seller_id: int = Path(...),
    user_service: UserService = Depends(get_user_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    seller = user_service.get_seller(seller_id=seller_id)

    admin_service.suspend_seller(seller)

    return {"status": f"Seller {seller_id} was suspended"}


@router.patch("/orders/{order_id}/complete", status_code=200)
def complete_order(
    order_id: int = Path(...),
    order_service: OrderService = Depends(get_order_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    order = order_service.get(order_id=order_id)

    admin_service.complete_order(order)

    return {"status": f"Order {order_id} was completed"}


@router.patch("/orders/{order_id}/cancel", status_code=200)
def cancel_order(
    order_id: int = Path(...),
    order_service: OrderService = Depends(get_order_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    order = order_service.get(order_id=order_id)

    admin_service.cancel_order(order)

    return {"status": f"Order {order_id} was cancelled"}


@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(
    review_id: int = Path(...),
    review_service: ReviewService = Depends(get_review_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    review = review_service.get(review_id=review_id)

    admin_service.delete_review(review)


@router.post("/categories", status_code=201)
def create_category(name: str = Form(...), admin_service: AdminService = Depends(get_admin_service)):
    admin_service.create_category(name=name)

    return {"status": "created"}


@router.post("/products/{product_id}/categories/{category_id}", status_code=204)
def add_product_to_category(
    product_id: int = Path(...),
    category_id: int = Path(...),
    product_service: ProductService = Depends(get_product_service),
    category_service: CategoryService = Depends(get_category_service),
    admin_service: AdminService = Depends(get_admin_service),
):
    product = product_service.get_product(product_id=product_id)

    category = category_service.get(category_id=category_id)

    admin_service.product_to_category(product=product, category=category)
