from pydantic import BaseModel, Field

from src.models.products import ProductVariant


class ProductItemIn(BaseModel):
    variant_id: int
    quantity: int = Field(1, ge=1)
    client_price: float


class OrderLine:
    def __init__(self, variant: ProductVariant, quantity: int, unit_price: int):
        self.variant = variant
        self.quantity = quantity
        self.unit_price = unit_price


class CreatingOrderResponse(BaseModel):
    order_id: int
    total_amount: int
    payment_secret: str
