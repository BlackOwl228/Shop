from typing import List
from pydantic import BaseModel, Field

class ProductItem(BaseModel):
    product_id: int = Field(..., ge=1, example=7)
    quantity: int = Field(1, ge=1, example=2)

class CreatingOrderResponse(BaseModel):
    order_id: int = Field(..., example="5")
    total_amount: float = Field(..., example=12500)