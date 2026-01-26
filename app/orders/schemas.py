from typing import List
from pydantic import BaseModel, Field

class ProductItem(BaseModel):
    product_id: int
    variant_id: int
    quantity: int = Field(1, ge=1, example=2)
    client_price: float

class CreatingOrderResponse(BaseModel):
    order_id: int
    total_amount: float
    payment_secret: str