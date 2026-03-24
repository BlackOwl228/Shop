from fastapi import APIRouter, Depends, Form, Path

from src.core.dependencies.services import get_cart_service
from src.core.dependencies.users import get_current_user
from src.models.users import User
from src.services.cart import CartService

from .schemas import CartResponse

router = APIRouter(tags=["Cart"])


@router.post("/cart/{variant_id}", status_code=204)
def add_product_to_cart(
    variant_id: int = Path(...),
    quantity: int = Form(1, ge=1),
    user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    cart_service.add_to_cart(user_id=user.id, variant_id=variant_id, quantity=quantity)


@router.get("/cart", status_code=200, response_model=CartResponse)
def get_my_cart(
    user: User = Depends(get_current_user), cart_service: CartService = Depends(get_cart_service)
):
    result, total = cart_service.get_user_cart(user_id=user.id)

    return {"items": result, "total_price": total}


@router.patch("/cart/{variant_id}", status_code=204)
def change_quantity_in_cart(
    variant_id: int = Path(...),
    quantity: int = Form(..., gt=0),
    user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    item = cart_service.get_cart_item(user_id=user.id, variant_id=variant_id)

    cart_service.change_quantity(item=item, quantity=quantity)


@router.delete("/cart/{variant_id}", status_code=204)
def delete_product_from_cart(
    variant_id: int = Path(...),
    user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    item = cart_service.get_cart_item(user_id=user.id, variant_id=variant_id)

    cart_service.delete_from_cart(item)
