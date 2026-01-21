from decimal import Decimal
from pydantic import BaseModel, Field

class CreatingProductDTO(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, example="IPhone 16 Pro")
    description: str | None = Field(None, max_length=500, example="Телефон от лучшего производителя смартфонов Apple")
    price: Decimal = Field(..., ge=1, example=54990)

class CreatingProductResponse(BaseModel):
    status: str = Field(..., max_length=30, example="created")
    product_id: int = Field(..., example=101)

class PatchingProductDTO(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=255, example="IPhone 17 Pro")
    description: str | None = Field(None, max_length=500, example="Телефон от лучшего производителя смартфонов Apple")
    price: Decimal | None = Field(None, ge=1, example=64990)

class GettingProductResponse(BaseModel):
    name: str = Field(..., example="AirPods 2")
    price: float = Field(..., ge=1, example=15500)
    stock: int = Field(..., ge=0)
    rating: float = Field(..., ge=0, le=5, example=4.8)
    description: str | None = Field(example="Телефон от лучшего производителя смартфонов Apple")
    image: str | None = Field(example="123.png")
    seller_id: int = Field(..., example=42)