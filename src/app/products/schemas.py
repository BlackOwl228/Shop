from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductPesponse(BaseModel):
    name: str
    rating: float = Field(..., ge=0, le=5)
    description: str | None
    seller_id: int

    model_config = ConfigDict(from_attributes=True)


class VariantResponse(BaseModel):
    id: int
    price: Decimal = Field(..., gt=0)
    stock: int
    image: str | None

    model_config = ConfigDict(from_attributes=True)


class ProductCartResponse(BaseModel):
    product: ProductPesponse
    variants: list[VariantResponse]
