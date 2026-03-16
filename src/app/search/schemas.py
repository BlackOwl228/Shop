from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from src.models.products import Product, ProductVariant


class ProductSorting(StrEnum):
    relevance = "relevance"
    price_asc = "price_asc"
    price_desc = "price_desc"
    rating = "rating"
    newest = "newest"


ProductsSortingMap = {
    ProductSorting.price_asc: ProductVariant.price.asc(),
    ProductSorting.price_desc: ProductVariant.price.desc(),
    ProductSorting.rating: Product.rating.desc(),
    ProductSorting.newest: Product.created_at.desc(),
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
