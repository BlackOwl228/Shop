from fastapi import APIRouter, Depends, Path

from core.depends import get_order_service
from services.orders import OrderService

from .schemas import CreatingOrderResponse, ProductItemIn

router = APIRouter(prefix="/orders", tags=["Order"])


@router.post("", status_code=201, response_model=CreatingOrderResponse)
def create_order(products: list[ProductItemIn], order_service: OrderService = Depends(get_order_service)):
    order = order_service.create_order(products)

    return {"order_id": order.id, "total_amount": order.total_price, "payment_secret": order.payment_intent}


@router.patch("/{order_id}/cancel", status_code=201)
def cancel_order(order_id: int = Path(..., ge=1), order_service: OrderService = Depends(get_order_service)):
    order_service.cancel_order_by_id(order_id)

    return {"status": "Order {order.id} cancelled"}


@router.patch("/{order_id}/complete", status_code=201)
def complete_order(order_id: int = Path(..., ge=1), order_service: OrderService = Depends(get_order_service)):
    order_service.complete_order_by_id(order_id)

    return {"status": "Order {order.id} completed"}


@router.post("/{order_id}/pay-test", status_code=201)
def pay_order(order_id: int = Path(..., ge=1), order_service: OrderService = Depends(get_order_service)):
    order = order_service.test_confirm_payment(order_id)

    return {"order_id": order.id, "status": order.status, "payment_intent": order.payment_intent}
