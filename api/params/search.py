from enum import Enum
from models.products import Product

class OrderingParam(str, Enum):
    asc = "asc"
    desc = "desc"

class SortingProducts(str, Enum):
    price = "price"
    created_at = "created_at"
ProductsMap = {SortingProducts.price: Product.price,
               SortingProducts.created_at: Product.created_at}