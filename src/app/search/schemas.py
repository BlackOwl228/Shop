from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from models import Product, ProductVariant


class OrderingParam(StrEnum):
    asc = "asc"
    desc = "desc"


class SortingProducts(StrEnum):
    price = "price"
    rating = "rating"
    created_at = "created_at"


ProductsMap = {
    SortingProducts.price: ProductVariant.price,
    SortingProducts.rating: Product.rating,
    SortingProducts.created_at: Product.created_at,
}


class SearchingProduct(BaseModel):
    id: int
    product_id: int
    name: str
    price: Decimal
    rating: float
    image: str | None
    stock: int
    category_id: int | None
    seller_id: int

    model_config = ConfigDict(from_attributes=True)


class SearchResponse(BaseModel):
    products: list[SearchingProduct]
    has_more: bool

    model_config = ConfigDict(from_attributes=True)
