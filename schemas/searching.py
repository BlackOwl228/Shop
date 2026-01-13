from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from models import Product

class OrderingParam(str, Enum):
    asc = "asc"
    desc = "desc"

class SortingProducts(str, Enum):
    price = "price"
    created_at = "created_at"
    
ProductsMap = {SortingProducts.price: Product.price,
               SortingProducts.created_at: Product.created_at}

class SearchingProduct(BaseModel):
    name: str = Field(..., example="Keyboard")
    price: int = Field(..., ge=1, example=10500)
    rating: float = Field(..., ge=0, le=5, example=4.6)
    image: str | None = Field(example="204.jpg")

class SearchingResponse(BaseModel):
    products: List[SearchingProduct]