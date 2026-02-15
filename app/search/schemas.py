from enum import Enum
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict
from models import Product, ProductVariant

class OrderingParam(str, Enum):
    asc = "asc"
    desc = "desc"

class SortingProducts(str, Enum):
    price = "price"
    rating = "rating"
    created_at = "created_at"
    
ProductsMap = {SortingProducts.price: ProductVariant.price,
               SortingProducts.rating: Product.rating,
               SortingProducts.created_at: Product.created_at}

class SearchingProduct(BaseModel):
    id: int
    product_id: int

    name: str
    price: Decimal
    rating: float
    image: str | None

    model_config = ConfigDict(from_attributes=True)

class SearchResponse(BaseModel):
    products: List[SearchingProduct]
    has_more: bool

    model_config = ConfigDict(from_attributes=True)