from decimal import Decimal

from pydantic import BaseModel


class CartVariant(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int
    image: str | None


class CartItemResponse(BaseModel):
    variant: CartVariant
    quantity: int
    subtotal: Decimal


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_price: Decimal
